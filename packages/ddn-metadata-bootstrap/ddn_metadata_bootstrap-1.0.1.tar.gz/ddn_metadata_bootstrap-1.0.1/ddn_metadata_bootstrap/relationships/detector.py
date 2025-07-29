#!/usr/bin/env python3

"""
Relationship detection logic for identifying connections between schema entities.
Analyzes foreign keys, shared fields, and naming patterns to detect relationships.
"""

import logging
import re
from typing import Dict, List, Set, Optional, Tuple, Any

from ..config import config

logger = logging.getLogger(__name__)


class RelationshipDetector:
    """
    Detects relationships between schema entities through various analysis methods.

    This class implements multiple detection strategies:
    - Foreign key template matching
    - Shared field analysis
    - Naming pattern recognition
    - Domain-specific relationship hints
    """

    def __init__(self):
        """Initialize the relationship detector with parsed templates."""
        self.parsed_fk_templates = self._parse_fk_templates()
        self.generic_fields_lower = [gf.lower() for gf in config.generic_fields]
        self.domain_identifiers = config.domain_identifiers

    def detect_foreign_key_relationships(self, entities_map: Dict[str, Dict]) -> List[Dict[str, Any]]:
        """
        Detect foreign key relationships using template matching.

        Args:
            entities_map: Dictionary mapping qualified entity names to entity info

        Returns:
            List of detected foreign key relationships
        """
        relationships = []

        logger.info(f"Analyzing {len(entities_map)} entities for foreign key relationships")

        for source_qnk, source_info in entities_map.items():
            source_subgraph = source_info.get('subgraph')

            for field in source_info.get('fields', []):
                field_name = field.get('name', '')
                if not field_name:
                    continue

                field_name_lower = field_name.lower()

                # Try each FK template
                for template_info in self.parsed_fk_templates:
                    fk_regex = template_info['fk_regex']
                    pk_template_str = template_info['pk_template_str']

                    match = fk_regex.match(field_name_lower)
                    if match:
                        relationship = self._process_fk_template_match(
                            match, source_qnk, source_info, field_name, pk_template_str, entities_map
                        )
                        if relationship:
                            relationships.append(relationship)
                            break  # Stop after first successful template match

        logger.info(f"Detected {len(relationships)} foreign key relationships")
        return relationships

    def detect_shared_field_relationships(self, entities_map: Dict[str, Dict]) -> List[Dict[str, Any]]:
        """
        Detect relationships based on shared field names.

        Args:
            entities_map: Dictionary mapping qualified entity names to entity info

        Returns:
            List of detected shared field relationships
        """
        relationships = []

        # Build field mapping for efficient lookup
        entity_fields_map = {}
        for qnk, info in entities_map.items():
            field_names = {f['name'].lower() for f in info.get('fields', []) if f.get('name')}
            entity_fields_map[qnk] = field_names

        # Compare all entity pairs
        entity_keys = list(entity_fields_map.keys())
        for i, qnk1 in enumerate(entity_keys):
            for qnk2 in entity_keys[i + 1:]:
                shared_relationships = self._analyze_shared_fields(
                    qnk1, qnk2, entity_fields_map[qnk1], entity_fields_map[qnk2], entities_map
                )
                relationships.extend(shared_relationships)

        logger.info(f"Detected {len(relationships)} shared field relationships")
        return relationships

    def detect_naming_pattern_relationships(self, entities_map: Dict[str, Dict]) -> List[Dict[str, Any]]:
        """
        Detect relationships based on naming patterns and conventions.

        Args:
            entities_map: Dictionary mapping qualified entity names to entity info

        Returns:
            List of detected naming pattern relationships
        """
        relationships = []

        # Analyze entity names for hierarchical patterns
        entity_names = [(qnk, info.get('name', '')) for qnk, info in entities_map.items()]

        for qnk1, name1 in entity_names:
            for qnk2, name2 in entity_names:
                if qnk1 >= qnk2 or not name1 or not name2:
                    continue

                pattern_relationship = self._analyze_naming_patterns(qnk1, name1, qnk2, name2, entities_map)
                if pattern_relationship:
                    relationships.append(pattern_relationship)

        logger.info(f"Detected {len(relationships)} naming pattern relationships")
        return relationships

    def find_referenced_entity(self, ref_entity_name_guess: str,
                               explicit_target_subgraph: Optional[str],
                               source_entity_qnk: str, entities_map: Dict[str, Dict],
                               source_entity_subgraph: Optional[str]) -> Optional[str]:
        """
        Find the best matching entity for a reference guess.

        Args:
            ref_entity_name_guess: Guessed entity name from field analysis
            explicit_target_subgraph: Explicit subgraph hint from template
            source_entity_qnk: Qualified name of source entity
            entities_map: Map of all entities
            source_entity_subgraph: Subgraph of source entity

        Returns:
            Qualified name of best matching target entity or None
        """
        if not ref_entity_name_guess:
            return None

        ref_lower = ref_entity_name_guess.lower()
        possible_targets = []

        for target_qnk, target_info in entities_map.items():
            target_name = target_info.get('name', '')
            if not target_name:
                continue

            target_name_lower = target_name.lower()
            target_subgraph = target_info.get('subgraph')
            target_kind = target_info.get('kind')

            score, match_details = self._calculate_entity_match_score(
                ref_lower, target_name_lower, target_subgraph, target_kind,
                explicit_target_subgraph, source_entity_subgraph
            )

            if score > 0:
                possible_targets.append({
                    'qnk': target_qnk,
                    'score': score,
                    'match_details': match_details
                })

        if not possible_targets:
            return None

        # Return the highest scoring match
        possible_targets.sort(key=lambda t: t['score'], reverse=True)
        best_match = possible_targets[0]

        logger.debug(f"Best match for '{ref_entity_name_guess}': {best_match['qnk']} "
                     f"(score: {best_match['score']}, details: {best_match['match_details']})")

        return best_match['qnk']

    def scan_for_existing_relationships(self, file_paths: List[str]) -> Set[Tuple]:
        """
        Scan files for existing relationship definitions to avoid duplicates.

        Args:
            file_paths: List of file paths to scan

        Returns:
            Set of relationship signatures (source_type, canonical_mapping)
        """
        from ..utils.yaml_utils import load_yaml_documents

        existing_signatures = set()

        logger.info(f"Scanning {len(file_paths)} files for existing relationships...")

        for file_path in file_paths:
            try:
                documents = load_yaml_documents(file_path)
                for doc in documents:
                    if isinstance(doc, dict) and doc.get('kind') == 'Relationship':
                        signature = self._extract_relationship_signature(doc)
                        if signature:
                            existing_signatures.add(signature)
            except Exception as e:
                logger.error(f"Error scanning file {file_path} for existing relationships: {e}")

        logger.info(f"Found {len(existing_signatures)} existing relationship signatures")
        return existing_signatures

    @staticmethod
    def _parse_fk_templates() -> List[Dict]:
        """Parse foreign key templates from configuration."""
        parsed_templates = []

        if not config.fk_templates_string:
            logger.warning("No FK templates string provided.")
            return parsed_templates

        template_pairs = config.fk_templates_string.split(',')

        # Build regex patterns
        pt_re = r"(?P<primary_table>\w+?)"
        ps_re = r"(?P<primary_subgraph>\w+?)"
        fs_re = r"(?P<foreign_subgraph>\w+?)"

        sorted_generic_fields = sorted(config.generic_fields, key=len, reverse=True)
        gi_re_options = "|".join(re.escape(gf) for gf in sorted_generic_fields)
        gi_re = f"(?P<generic_id>(?:{gi_re_options}))"

        for tpl_pair_str in template_pairs:
            tpl_pair_str = tpl_pair_str.strip()
            if not tpl_pair_str or '|' not in tpl_pair_str:
                continue

            pk_tpl_str, fk_tpl_str_orig = [part.strip() for part in tpl_pair_str.split('|', 1)]

            # Build regex pattern
            fk_regex_str = fk_tpl_str_orig
            fk_regex_str = fk_regex_str.replace("{fs}", fs_re)
            fk_regex_str = fk_regex_str.replace("{ps}", ps_re)
            fk_regex_str = fk_regex_str.replace("{pt}", pt_re)
            fk_regex_str = fk_regex_str.replace("{gi}", gi_re)
            fk_regex_str = f"^{fk_regex_str}$"

            try:
                compiled_regex = re.compile(fk_regex_str)
                parsed_templates.append({
                    'pk_template_str': pk_tpl_str,
                    'fk_template_str_orig': fk_tpl_str_orig,
                    'fk_regex': compiled_regex
                })
                logger.debug(f"Parsed FK template: PK='{pk_tpl_str}', FK='{fk_tpl_str_orig}'")
            except re.error as e:
                logger.error(f"Failed to compile regex for FK template '{fk_tpl_str_orig}': {e}")

        return parsed_templates

    def _process_fk_template_match(self, match, source_qnk: str, source_info: Dict,
                                   field_name: str, pk_template_str: str,
                                   entities_map: Dict[str, Dict]) -> Optional[Dict[str, Any]]:
        """Process a successful foreign key template match."""
        match_groups = match.groupdict()
        guessed_primary_table = match_groups.get('primary_table')
        guessed_generic_id = match_groups.get('generic_id')
        explicit_target_subgraph = match_groups.get('primary_subgraph')
        source_subgraph = source_info.get('subgraph')

        if not guessed_primary_table:
            return None

        # Generate entity name variations to check
        forms_to_check = {guessed_primary_table.lower()}
        if guessed_primary_table.lower().endswith('s') and len(guessed_primary_table) > 1:
            forms_to_check.add(guessed_primary_table.lower()[:-1])  # Singular
        else:
            forms_to_check.add(guessed_primary_table.lower() + 's')  # Plural

        forms_to_check.discard("")  # Remove empty strings

        # Find best matching target entity
        for form in forms_to_check:
            target_qnk = self.find_referenced_entity(
                form, explicit_target_subgraph, source_qnk, entities_map, source_subgraph
            )

            if target_qnk and target_qnk != source_qnk:
                target_info = entities_map.get(target_qnk, {})

                # Determine target field name
                to_field_name = self._determine_target_field_name(
                    pk_template_str, guessed_generic_id, target_info
                )

                return {
                    'from_entity': source_qnk,
                    'from_field': field_name,
                    'to_entity': target_qnk,
                    'to_field_name': to_field_name,
                    'relationship_type': 'foreign_key_template',
                    'confidence': 'high',
                    'cross_subgraph': source_subgraph != target_info.get('subgraph'),
                    'template_used': pk_template_str
                }

        return None

    def _analyze_shared_fields(self, qnk1: str, qnk2: str, fields1: Set[str],
                               fields2: Set[str], entities_map: Dict[str, Dict]) -> List[Dict[str, Any]]:
        """Analyze shared fields between two entities."""
        relationships = []
        common_fields = fields1.intersection(fields2)

        entity1_info = entities_map[qnk1]
        entity2_info = entities_map[qnk2]
        entity1_pks = {pk.lower() for pk in entity1_info.get('primary_keys', [])}
        entity2_pks = {pk.lower() for pk in entity2_info.get('primary_keys', [])}

        for field_lower in common_fields:
            # Skip generic fields and primary keys
            if (field_lower in self.generic_fields_lower or
                    field_lower in entity1_pks or field_lower in entity2_pks):
                continue

            # Check if this relationship already exists as a foreign key
            if self._is_existing_fk_relationship(qnk1, qnk2, field_lower, entities_map):
                continue

            # Determine confidence based on field characteristics
            confidence = self._calculate_shared_field_confidence(field_lower)

            relationship = {
                'from_entity': qnk1,
                'to_entity': qnk2,
                'shared_field': field_lower,
                'relationship_type': 'shared_field',
                'confidence': confidence,
                'cross_subgraph': entity1_info.get('subgraph') != entity2_info.get('subgraph')
            }

            relationships.append(relationship)

        return relationships

    def _analyze_naming_patterns(self, qnk1: str, name1: str, qnk2: str, name2: str,
                                 entities_map: Dict[str, Dict]) -> Optional[Dict[str, Any]]:
        """Analyze naming patterns between two entities."""
        name1_lower = name1.lower()
        name2_lower = name2.lower()

        # Check for hierarchical patterns (parent-child naming)
        if self._is_hierarchical_naming(name1_lower, name2_lower):
            entity1_info = entities_map[qnk1]
            entity2_info = entities_map[qnk2]

            return {
                'from_entity': qnk1,
                'to_entity': qnk2,
                'relationship_type': 'naming_hierarchy',
                'confidence': 'medium',
                'cross_subgraph': entity1_info.get('subgraph') != entity2_info.get('subgraph'),
                'pattern_type': 'hierarchical_naming'
            }

        return None

    @staticmethod
    def _calculate_entity_match_score(ref_name: str, target_name: str,
                                      target_subgraph: Optional[str], target_kind: str,
                                      explicit_subgraph: Optional[str],
                                      source_subgraph: Optional[str]) -> Tuple[int, str]:
        """Calculate matching score between reference and target entity."""
        score = 0
        match_details = []

        # Direct name match
        if target_name == ref_name:
            score += 15
            match_details.append("exact_name")

        # Prefix match (subgraph_entityname pattern)
        elif target_name.endswith(f"_{ref_name}"):
            potential_prefix = target_name[:-len(f"_{ref_name}")]
            score += 12
            match_details.append("prefix_match")

            # Bonus if prefix matches target's subgraph
            if target_subgraph and potential_prefix == target_subgraph.lower():
                score += 10
                match_details.append("prefix_matches_subgraph")

            # Bonus if prefix matches source's subgraph
            if source_subgraph and potential_prefix == source_subgraph.lower():
                score += 25
                match_details.append("prefix_matches_source_subgraph")

        # Plural/singular variations
        if len(ref_name) > 1:
            if target_name == ref_name + "s":
                score = max(score, 9)
                if not match_details:
                    match_details.append("plural_target")
            elif target_name + "s" == ref_name:
                score = max(score, 7)
                if not match_details:
                    match_details.append("plural_reference")

        # Subgraph bonuses
        if score > 0:
            if explicit_subgraph and target_subgraph and explicit_subgraph.lower() == target_subgraph.lower():
                score += 200
                match_details.append("EXPLICIT_SUBGRAPH_MATCH")
            elif source_subgraph and target_subgraph == source_subgraph:
                score += 100
                match_details.append("SAME_SUBGRAPH")

        # Kind bonuses
        if target_kind == 'ObjectType':
            score += 20
        elif target_kind == 'Model':
            score += 10

        return score, ", ".join(match_details)

    @staticmethod
    def _determine_target_field_name(pk_template: str, guessed_generic_id: Optional[str],
                                     target_info: Dict) -> str:
        """Determine the target field name for a relationship."""
        if pk_template == "{gi}" and guessed_generic_id:
            return guessed_generic_id
        elif pk_template and pk_template != "{gi}":
            return pk_template
        else:
            # Use primary key or fallback to 'id'
            target_pks = target_info.get('primary_keys', [])
            if target_pks:
                return target_pks[0]
            elif any(f.get('name', '').lower() == 'id' for f in target_info.get('fields', [])):
                return "id"
            elif guessed_generic_id:
                return guessed_generic_id
            else:
                return "id"  # Default fallback

    @staticmethod
    def _is_existing_fk_relationship(qnk1: str, qnk2: str, field_name: str,
                                     entities_map: Dict[str, Dict]) -> bool:
        """Check if a foreign key relationship already exists for this field."""
        # This would check against detected FK relationships
        # For now, return False (can be enhanced)
        return False

    def _calculate_shared_field_confidence(self, field_name: str) -> str:
        """Calculate confidence level for shared field relationships."""
        if any(domain_id in field_name for domain_id in self.domain_identifiers):
            return 'medium'
        return 'low'

    @staticmethod
    def _is_hierarchical_naming(name1: str, name2: str) -> bool:
        """Check if two names follow a hierarchical pattern."""
        # Simple patterns: one name contains the other
        return (name1 in name2 and name1 != name2) or (name2 in name1 and name1 != name2)

    @staticmethod
    def _extract_relationship_signature(relationship_doc: Dict) -> Optional[Tuple]:
        """Extract a signature from an existing relationship document."""
        try:
            definition = relationship_doc.get('definition', {})
            source_type = definition.get('sourceType')
            mapping = definition.get('mapping', [])

            if not source_type or not mapping:
                return None

            canonical_mapping_parts = []
            for m_item in mapping:
                if isinstance(m_item, dict):
                    source_fp = m_item.get('source', {}).get('fieldPath', [])
                    target_block = m_item.get('target', {})
                    target_fp = target_block.get('modelField', target_block.get('fieldPath', []))

                    # Convert to tuples for hashing
                    source_tuple = tuple(fp.get('fieldName', fp) if isinstance(fp, dict) else fp for fp in source_fp)
                    target_tuple = tuple(fp.get('fieldName', fp) if isinstance(fp, dict) else fp for fp in target_fp)

                    canonical_mapping_parts.append((source_tuple, target_tuple))

            canonical_mapping_parts.sort()
            return source_type, frozenset(canonical_mapping_parts)

        except Exception as e:
            logger.warning(f"Could not extract signature from relationship: {e}")
            return None


def create_relationship_detector() -> RelationshipDetector:
    """
    Create a RelationshipDetector instance.

    Returns:
        Configured RelationshipDetector instance
    """
    return RelationshipDetector()
