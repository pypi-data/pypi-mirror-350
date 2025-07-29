#!/usr/bin/env python3

"""
Relationship YAML generation for creating OpenDD relationship definitions.
Converts detected relationships into proper YAML relationship structures.
"""

import logging
from typing import Dict, List, Any, Optional, Set, Tuple

from ..utils.text_utils import to_camel_case, smart_pluralize

logger = logging.getLogger(__name__)


class RelationshipGenerator:
    """
    Generates YAML relationship definitions from detected relationship patterns.

    This class takes the output from relationship detection and creates properly
    formatted OpenDD Relationship kind definitions that can be added to schema files.
    """

    def __init__(self):
        """Initialize the relationship generator."""
        self.generated_relationships: List[Dict[str, Any]] = []
        self.relationship_signatures: Set[Tuple] = set()

    def generate_foreign_key_relationships(self, fk_relationships: List[Dict[str, Any]],
                                           entities_map: Dict[str, Dict]) -> List[Dict[str, Any]]:
        """
        Generate relationship YAML definitions for foreign key relationships.

        Args:
            fk_relationships: List of detected foreign key relationships
            entities_map: Map of entity qualified names to entity info

        Returns:
            List of relationship definition dictionaries
        """
        generated = []

        for fk_rel in fk_relationships:
            # Generate forward relationship (many-to-one or one-to-one)
            forward_rel = self._generate_forward_relationship(fk_rel, entities_map)
            if forward_rel:
                generated.append(forward_rel)

            # Generate reverse relationship (one-to-many)
            reverse_rel = self._generate_reverse_relationship(fk_rel, entities_map)
            if reverse_rel:
                generated.append(reverse_rel)

        logger.info(f"Generated {len(generated)} foreign key relationship definitions")
        return generated

    def generate_shared_field_relationships(self, shared_relationships: List[Dict[str, Any]],
                                            entities_map: Dict[str, Dict]) -> List[Dict[str, Any]]:
        """
        Generate relationship YAML definitions for shared field relationships.

        Args:
            shared_relationships: List of detected shared field relationships
            entities_map: Map of entity qualified names to entity info

        Returns:
            List of relationship definition dictionaries
        """
        generated = []

        for shared_rel in shared_relationships:
            # Generate bidirectional many-to-many relationships
            rel1 = self._generate_shared_field_relationship(
                shared_rel['from_entity'], shared_rel['to_entity'],
                shared_rel['shared_field'], entities_map
            )
            if rel1:
                generated.append(rel1)

            rel2 = self._generate_shared_field_relationship(
                shared_rel['to_entity'], shared_rel['from_entity'],
                shared_rel['shared_field'], entities_map
            )
            if rel2:
                generated.append(rel2)

        logger.info(f"Generated {len(generated)} shared field relationship definitions")
        return generated

    @staticmethod
    def generate_relationship_name(target_entity_name: str,
                                   relationship_type: str = "single") -> str:
        """
        Generate appropriate relationship names based on target entity and cardinality.

        Args:
            target_entity_name: Name of the target entity
            relationship_type: "single" for one-to-one/many-to-one, "multiple" for one-to-many/many-to-many

        Returns:
            Appropriately named relationship in camelCase
        """
        if not target_entity_name:
            return ""

        base_name = to_camel_case(target_entity_name, first_char_lowercase=True)

        if relationship_type == "multiple":
            return smart_pluralize(base_name)
        else:
            return base_name

    @staticmethod
    def check_relationship_conflicts(entity_info: Dict,
                                     proposed_relationship_name: str) -> bool:
        """
        Check if a proposed relationship name conflicts with existing fields.

        Args:
            entity_info: Entity information dictionary
            proposed_relationship_name: Proposed relationship name

        Returns:
            True if there's a conflict, False otherwise
        """
        existing_field_names = {f.get('name', '').lower() for f in entity_info.get('fields', [])}
        return proposed_relationship_name.lower() in existing_field_names

    @staticmethod
    def create_relationship_yaml_structure(relationship_def: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create the complete YAML structure for a relationship definition.

        Args:
            relationship_def: Relationship definition dictionary

        Returns:
            Complete YAML structure with kind, version, and definition
        """
        return {
            "kind": "Relationship",
            "version": "v1",
            "definition": relationship_def
        }

    @staticmethod
    def group_relationships_by_file(relationships: List[Dict[str, Any]],
                                    entities_map: Dict[str, Dict]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group generated relationships by their target file paths.

        Args:
            relationships: List of relationship definitions with metadata
            entities_map: Map of entity qualified names to entity info

        Returns:
            Dictionary mapping file paths to lists of relationships
        """
        grouped = {}

        for rel_item in relationships:
            if isinstance(rel_item, dict) and 'target_file_path' in rel_item:
                file_path = rel_item['target_file_path']
                if file_path not in grouped:
                    grouped[file_path] = []
                grouped[file_path].append(rel_item['relationship_definition'])

        return grouped

    def deduplicate_relationships(self, relationships: List[Dict[str, Any]],
                                  existing_signatures: Set[Tuple]) -> List[Dict[str, Any]]:
        """
        Remove duplicate relationships based on their signatures.

        Args:
            relationships: List of relationship definitions
            existing_signatures: Set of existing relationship signatures

        Returns:
            Deduplicated list of relationships
        """
        deduplicated = []
        seen_signatures = existing_signatures.copy()

        for rel_item in relationships:
            signature = self._extract_relationship_signature(rel_item)
            if signature and signature not in seen_signatures:
                deduplicated.append(rel_item)
                seen_signatures.add(signature)
            elif not signature:
                # If we can't create a signature, include it with a warning
                logger.warning(f"Could not create signature for relationship, including anyway: {rel_item}")
                deduplicated.append(rel_item)

        logger.info(f"Deduplicated {len(relationships)} relationships to {len(deduplicated)}")
        return deduplicated

    def _generate_forward_relationship(self, fk_rel: Dict[str, Any],
                                       entities_map: Dict[str, Dict]) -> Optional[Dict[str, Any]]:
        """Generate forward (many-to-one or one-to-one) relationship."""
        source_qnk = fk_rel['from_entity']
        target_qnk = fk_rel['to_entity']
        from_field = fk_rel['from_field']
        to_field = fk_rel['to_field_name']

        source_info = entities_map.get(source_qnk, {})
        target_info = entities_map.get(target_qnk, {})

        source_name = source_info.get('name')
        target_name = target_info.get('name')

        if not source_name or not target_name:
            return None

        # Generate relationship name (singular for forward relationship)
        rel_name = self.generate_relationship_name(target_name, "single")

        # Check for naming conflicts
        if self.check_relationship_conflicts(source_info, rel_name):
            logger.debug(f"Skipping forward relationship '{rel_name}' due to field name conflict")
            return None

        # Build target block
        target_block = {
            "name": target_name,
            "relationshipType": "Object"
        }

        # Add subgraph if cross-subgraph relationship
        if target_info.get('subgraph') and target_info.get('subgraph') != source_info.get('subgraph'):
            target_block['subgraph'] = target_info.get('subgraph')

        # Build relationship definition
        relationship_def = {
            "name": rel_name,
            "sourceType": source_name,
            "target": {"model": target_block},
            "mapping": [{
                "source": {"fieldPath": [{"fieldName": from_field}]},
                "target": {"modelField": [{"fieldName": to_field}]}
            }]
        }

        return {
            'target_file_path': source_info.get('file_path'),
            'relationship_definition': self.create_relationship_yaml_structure(relationship_def)
        }

    def _generate_reverse_relationship(self, fk_rel: Dict[str, Any],
                                       entities_map: Dict[str, Dict]) -> Optional[Dict[str, Any]]:
        """Generate reverse (one-to-many) relationship."""
        source_qnk = fk_rel['from_entity']
        target_qnk = fk_rel['to_entity']
        from_field = fk_rel['from_field']
        to_field = fk_rel['to_field_name']

        source_info = entities_map.get(source_qnk, {})
        target_info = entities_map.get(target_qnk, {})

        source_name = source_info.get('name')
        target_name = target_info.get('name')

        if not source_name or not target_name:
            return None

        # Generate relationship name (plural for reverse relationship)
        rel_name = self.generate_relationship_name(source_name, "multiple")

        # Check for naming conflicts
        if self.check_relationship_conflicts(target_info, rel_name):
            logger.debug(f"Skipping reverse relationship '{rel_name}' due to field name conflict")
            return None

        # Build target block
        target_block = {
            "name": source_name,
            "relationshipType": "Array"
        }

        # Add subgraph if cross-subgraph relationship
        if source_info.get('subgraph') and source_info.get('subgraph') != target_info.get('subgraph'):
            target_block['subgraph'] = source_info.get('subgraph')

        # Build relationship definition
        relationship_def = {
            "name": rel_name,
            "sourceType": target_name,
            "target": {"model": target_block},
            "mapping": [{
                "source": {"fieldPath": [{"fieldName": to_field}]},
                "target": {"modelField": [{"fieldName": from_field}]}
            }]
        }

        return {
            'target_file_path': target_info.get('file_path'),
            'relationship_definition': self.create_relationship_yaml_structure(relationship_def)
        }

    def _generate_shared_field_relationship(self, source_qnk: str, target_qnk: str,
                                            shared_field: str,
                                            entities_map: Dict[str, Dict]) -> Optional[Dict[str, Any]]:
        """Generate a shared field (many-to-many) relationship."""
        source_info = entities_map.get(source_qnk, {})
        target_info = entities_map.get(target_qnk, {})

        source_name = source_info.get('name')
        target_name = target_info.get('name')

        if not source_name or not target_name:
            return None

        # Find original case field names
        source_field_name = self._find_original_field_name(shared_field, source_info)
        target_field_name = self._find_original_field_name(shared_field, target_info)

        if not source_field_name or not target_field_name:
            return None

        # Generate relationship name with shared field context
        base_target_name = self.generate_relationship_name(target_name, "multiple")
        shared_field_suffix = to_camel_case(shared_field, first_char_lowercase=False)
        rel_name = f"{base_target_name}By{shared_field_suffix}"

        # Check for naming conflicts
        if self.check_relationship_conflicts(source_info, rel_name):
            logger.debug(f"Skipping shared field relationship '{rel_name}' due to field name conflict")
            return None

        # Build target block
        target_block = {
            "name": target_name,
            "relationshipType": "Array"  # Many-to-many relationship
        }

        # Add subgraph if cross-subgraph relationship
        if target_info.get('subgraph') and target_info.get('subgraph') != source_info.get('subgraph'):
            target_block['subgraph'] = target_info.get('subgraph')

        # Build relationship definition
        relationship_def = {
            "name": rel_name,
            "sourceType": source_name,
            "target": {"model": target_block},
            "mapping": [{
                "source": {"fieldPath": [{"fieldName": source_field_name}]},
                "target": {"modelField": [{"fieldName": target_field_name}]}
            }]
        }

        return {
            'target_file_path': source_info.get('file_path'),
            'relationship_definition': self.create_relationship_yaml_structure(relationship_def)
        }

    @staticmethod
    def _find_original_field_name(field_name_lower: str, entity_info: Dict) -> Optional[str]:
        """Find the original case field name from entity info."""
        for field in entity_info.get('fields', []):
            if field.get('name', '').lower() == field_name_lower:
                return field.get('name')
        return None

    @staticmethod
    def _extract_relationship_signature(rel_item: Dict[str, Any]) -> Optional[Tuple]:
        """Extract a unique signature from a relationship definition."""
        try:
            if 'relationship_definition' in rel_item:
                rel_def = rel_item['relationship_definition']
            else:
                rel_def = rel_item

            definition = rel_def.get('definition', {})
            source_type = definition.get('sourceType')
            mapping = definition.get('mapping', [])

            if not source_type or not mapping:
                return None

            canonical_mapping_parts = []
            for m_item in mapping:
                if isinstance(m_item, dict):
                    # Extract source field path
                    source_fp = m_item.get('source', {}).get('fieldPath', [])
                    source_field_names = tuple(
                        fp.get('fieldName', fp) if isinstance(fp, dict) else fp
                        for fp in source_fp
                    )

                    # Extract target field path (prioritize modelField)
                    target_block = m_item.get('target', {})
                    target_fp = target_block.get('modelField', target_block.get('fieldPath', []))
                    target_field_names = tuple(
                        fp.get('fieldName', fp) if isinstance(fp, dict) else fp
                        for fp in target_fp
                    )

                    canonical_mapping_parts.append((source_field_names, target_field_names))

            canonical_mapping_parts.sort()
            return source_type, frozenset(canonical_mapping_parts)

        except Exception as e:
            logger.warning(f"Could not create signature for relationship: {e}")
            return None

    def generate_relationship_descriptions(self, relationships: List[Dict[str, Any]],
                                           entities_map: Dict[str, Dict]) -> List[Dict[str, Any]]:
        """
        Generate descriptions for relationship definitions.

        Args:
            relationships: List of relationship definitions
            entities_map: Map of entity qualified names to entity info

        Returns:
            List of relationships with added descriptions
        """
        enhanced_relationships = []

        for rel_item in relationships:
            enhanced_rel = rel_item.copy()

            # Extract relationship info
            rel_def = rel_item.get('relationship_definition', {}).get('definition', {})
            rel_name = rel_def.get('name', '')
            source_type = rel_def.get('sourceType', '')
            target_info = rel_def.get('target', {}).get('model', {})
            target_name = target_info.get('name', '')
            relationship_type = target_info.get('relationshipType', 'Object')

            # Generate description
            description = self._generate_relationship_description(
                rel_name, source_type, target_name, relationship_type
            )

            if description:
                # Add description to relationship definition
                if 'relationship_definition' in enhanced_rel:
                    enhanced_rel['relationship_definition']['definition']['description'] = description
                else:
                    enhanced_rel['definition']['description'] = description

            enhanced_relationships.append(enhanced_rel)

        return enhanced_relationships

    @staticmethod
    def _generate_relationship_description(rel_name: str, source_type: str,
                                           target_name: str, relationship_type: str) -> str:
        """Generate a description for a relationship."""
        if relationship_type == "Array":
            return f"Collection of {target_name} entities related to this {source_type}."
        else:
            return f"Reference to the associated {target_name} entity."

    def get_generation_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about relationship generation.

        Returns:
            Dictionary with generation statistics
        """
        return {
            'total_generated': len(self.generated_relationships),
            'unique_signatures': len(self.relationship_signatures),
            'relationships_by_type': self._count_by_relationship_type(),
            'cross_subgraph_count': self._count_cross_subgraph_relationships()
        }

    def _count_by_relationship_type(self) -> Dict[str, int]:
        """Count relationships by their target relationship type."""
        counts = {}
        for rel in self.generated_relationships:
            rel_def = rel.get('relationship_definition', {}).get('definition', {})
            rel_type = rel_def.get('target', {}).get('model', {}).get('relationshipType', 'Unknown')
            counts[rel_type] = counts.get(rel_type, 0) + 1
        return counts

    def _count_cross_subgraph_relationships(self) -> int:
        """Count relationships that cross subgraph boundaries."""
        count = 0
        for rel in self.generated_relationships:
            rel_def = rel.get('relationship_definition', {}).get('definition', {})
            if 'subgraph' in rel_def.get('target', {}).get('model', {}):
                count += 1
        return count


def create_relationship_generator() -> RelationshipGenerator:
    """
    Create a RelationshipGenerator instance.

    Returns:
        Configured RelationshipGenerator instance
    """
    return RelationshipGenerator()
