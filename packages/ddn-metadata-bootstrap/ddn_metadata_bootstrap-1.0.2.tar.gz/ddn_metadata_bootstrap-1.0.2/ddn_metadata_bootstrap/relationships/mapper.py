#!/usr/bin/env python3

"""
Relationship mapping and context generation for schema entities.
Builds comprehensive relationship maps and provides context for description enhancement.
"""

import logging
from typing import Dict, List, Optional, Any

from .detector import RelationshipDetector
from .generator import RelationshipGenerator

logger = logging.getLogger(__name__)


class RelationshipMapper:
    """
    Builds comprehensive relationship maps and provides relationship context.

    This class takes detected relationships and creates structured maps that can be
    used to enhance entity descriptions with relationship information and generate
    relationship definitions for the schema.
    """

    def __init__(self):
        """Initialize the relationship mapper."""
        self.relationship_detector = RelationshipDetector()
        self.relationship_generator = RelationshipGenerator()

    def build_relationship_map(self, schema_metadata: Dict[str, Dict]) -> Dict[str, Any]:
        """
        Build a comprehensive relationship map from collected schema metadata.

        Args:
            schema_metadata: Dictionary mapping file paths to their metadata

        Returns:
            Comprehensive relationship map with entities and relationships
        """
        # Extract and organize entities
        entities_map = self._build_entities_map(schema_metadata)

        # Detect all types of relationships
        all_relationships = []

        # 1. Foreign key relationships
        fk_relationships = self.relationship_detector.detect_foreign_key_relationships(entities_map)
        all_relationships.extend(fk_relationships)

        # 2. Shared field relationships
        shared_relationships = self.relationship_detector.detect_shared_field_relationships(entities_map)
        all_relationships.extend(shared_relationships)

        # 3. Naming pattern relationships
        naming_relationships = self.relationship_detector.detect_naming_pattern_relationships(entities_map)
        all_relationships.extend(naming_relationships)

        # Deduplicate relationships
        unique_relationships = self._deduplicate_relationships(all_relationships)

        # Generate relationship YAML definitions
        generated_yaml = self._generate_relationship_yaml(unique_relationships, entities_map)

        # Build the final relationship map
        relationship_map = {
            'entities': entities_map,
            'relationships': unique_relationships,
            'generated_yaml': generated_yaml,
            'statistics': self._calculate_map_statistics(entities_map, unique_relationships)
        }

        logger.info(
            f"Built relationship map with {len(entities_map)} entities and {len(unique_relationships)} relationships")
        return relationship_map

    def get_entity_relationships(self, entity_name: str, entity_kind: str,
                                 subgraph: Optional[str],
                                 relationship_map: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get all relationships for a specific entity.

        Args:
            entity_name: Name of the entity
            entity_kind: Kind of the entity
            subgraph: Subgraph of the entity
            relationship_map: The comprehensive relationship map

        Returns:
            List of relationships involving this entity
        """
        # Build qualified name for lookup
        entity_qnk = self._build_qualified_name(entity_name, entity_kind, subgraph)

        if entity_qnk not in relationship_map.get('entities', {}):
            logger.warning(f"Entity {entity_qnk} not found in relationship map")
            return []

        relationships = []

        for rel in relationship_map.get('relationships', []):
            enriched_rel = self._enrich_relationship_for_entity(rel, entity_qnk, relationship_map)
            if enriched_rel:
                relationships.append(enriched_rel)

        # Deduplicate and sort
        unique_relationships = self._deduplicate_entity_relationships(relationships)

        return unique_relationships

    def format_relationships_for_prompt(self, relationships: List[Dict[str, Any]],
                                        relationship_map: Dict[str, Any],
                                        current_entity_qnk: str) -> str:
        """
        Format relationships for inclusion in AI prompts.

        Args:
            relationships: List of relationships to format
            relationship_map: The comprehensive relationship map
            current_entity_qnk: Qualified name of the current entity

        Returns:
            Formatted string describing the relationships
        """
        if not relationships:
            return ""

        # Group relationships by type and direction
        outgoing_fk = []
        incoming_fk = []
        shared_fields = []
        other_rels = []

        for rel in relationships:
            rel_type = rel.get('relationship_type', 'unknown')
            direction = rel.get('direction', 'unknown')

            if rel_type.startswith('foreign_key') and direction == 'outgoing':
                outgoing_fk.append(rel)
            elif rel_type.startswith('foreign_key') and direction == 'incoming':
                incoming_fk.append(rel)
            elif rel_type == 'shared_field':
                shared_fields.append(rel)
            else:
                other_rels.append(rel)

        # Format each group
        sections = []

        if outgoing_fk:
            section = self._format_outgoing_relationships(outgoing_fk, relationship_map)
            sections.append(f"Outgoing References (->):\n{section}")

        if incoming_fk:
            section = self._format_incoming_relationships(incoming_fk, relationship_map)
            sections.append(f"Incoming References (<-):\n{section}")

        if shared_fields:
            section = self._format_shared_field_relationships(shared_fields, relationship_map)
            sections.append(f"Shared Fields (<->):\n{section}")

        if other_rels:
            section = self._format_other_relationships(other_rels, relationship_map)
            sections.append(f"Other Relationships:\n{section}")

        return "\n\n".join(sections) if sections else ""

    @staticmethod
    def get_relationship_statistics(relationship_map: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get comprehensive statistics about the relationship map.

        Args:
            relationship_map: The relationship map to analyze

        Returns:
            Dictionary with detailed statistics
        """
        entities = relationship_map.get('entities', {})
        relationships = relationship_map.get('relationships', [])

        stats = {
            'entity_count': len(entities),
            'relationship_count': len(relationships),
            'entities_by_kind': {},
            'entities_by_subgraph': {},
            'relationships_by_type': {},
            'cross_subgraph_relationships': 0,
            'entities_with_relationships': 0,
            'avg_relationships_per_entity': 0.0,
            'most_connected_entities': []
        }

        # Analyze entities
        entity_connection_counts = {}
        for qnk, entity_info in entities.items():
            kind = entity_info.get('kind', 'Unknown')
            subgraph = entity_info.get('subgraph', 'None')

            stats['entities_by_kind'][kind] = stats['entities_by_kind'].get(kind, 0) + 1
            stats['entities_by_subgraph'][subgraph] = stats['entities_by_subgraph'].get(subgraph, 0) + 1

            entity_connection_counts[qnk] = 0

        # Analyze relationships
        for rel in relationships:
            rel_type = rel.get('relationship_type', 'unknown')
            stats['relationships_by_type'][rel_type] = stats['relationships_by_type'].get(rel_type, 0) + 1

            # Check for cross-subgraph
            if rel.get('cross_subgraph', False):
                stats['cross_subgraph_relationships'] += 1

            # Count entity connections
            from_entity = rel.get('from_entity')
            to_entity = rel.get('to_entity')

            if from_entity in entity_connection_counts:
                entity_connection_counts[from_entity] += 1
            if to_entity in entity_connection_counts:
                entity_connection_counts[to_entity] += 1

        # Calculate connection statistics
        connected_entities = sum(1 for count in entity_connection_counts.values() if count > 0)
        stats['entities_with_relationships'] = connected_entities

        if len(entities) > 0:
            total_connections = sum(entity_connection_counts.values())
            stats['avg_relationships_per_entity'] = total_connections / len(entities)

        # Find most connected entities
        sorted_entities = sorted(entity_connection_counts.items(), key=lambda x: x[1], reverse=True)
        stats['most_connected_entities'] = [
            {'entity': qnk, 'connection_count': count}
            for qnk, count in sorted_entities[:5]  # Top 5
        ]

        return stats

    def _build_entities_map(self, schema_metadata: Dict[str, Dict]) -> Dict[str, Dict]:
        """Build a unified entities map from file metadata."""
        entities_map = {}
        total_entities = 0

        for file_path, file_metadata in schema_metadata.items():
            subgraph = file_metadata.get('subgraph')

            for entity_data in file_metadata.get('entities', []):
                total_entities += 1
                entity_name = entity_data.get('name')
                entity_kind = entity_data.get('kind', 'UnknownKind')

                if not entity_name:
                    continue

                # Build qualified name
                qnk = self._build_qualified_name(entity_name, entity_kind, subgraph)

                if qnk in entities_map:
                    logger.warning(f"Duplicate entity qualified name '{qnk}'. Overwriting.")

                # Enhance entity data with file path
                enhanced_entity_data = {**entity_data, 'file_path': file_path}
                entities_map[qnk] = enhanced_entity_data

        logger.info(f"Built entities map with {len(entities_map)} unique entities from {total_entities} total")
        return entities_map

    @staticmethod
    def _build_qualified_name(entity_name: str, entity_kind: str,
                              subgraph: Optional[str]) -> str:
        """Build a qualified name for an entity."""
        if subgraph:
            return f"{subgraph}/{entity_kind}/{entity_name}"
        else:
            return f"{entity_kind}/{entity_name}"

    @staticmethod
    def _deduplicate_relationships(relationships: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate relationships based on their characteristics."""
        unique_relationships = []
        seen_keys = set()

        for rel in relationships:
            # Create a unique key based on relationship characteristics
            if rel['relationship_type'] == 'shared_field':
                # For shared fields, key by entities and field name
                key = (
                    tuple(sorted([rel['from_entity'], rel['to_entity']])),
                    rel.get('shared_field'),
                    rel['relationship_type']
                )
            else:
                # For other relationships, key by from/to entities and fields
                key = (
                    rel['from_entity'],
                    rel.get('from_field'),
                    rel['to_entity'],
                    rel.get('to_field_name'),
                    rel['relationship_type']
                )

            if key not in seen_keys:
                seen_keys.add(key)
                unique_relationships.append(rel)

        logger.debug(f"Deduplicated {len(relationships)} to {len(unique_relationships)} relationships")
        return unique_relationships

    def _generate_relationship_yaml(self, relationships: List[Dict[str, Any]],
                                    entities_map: Dict[str, Dict]) -> List[Dict[str, Any]]:
        """Generate YAML definitions for all relationships."""
        generated_yaml = []

        # Separate relationships by type
        fk_relationships = [r for r in relationships if r['relationship_type'].startswith('foreign_key')]
        shared_relationships = [r for r in relationships if r['relationship_type'] == 'shared_field']

        # Generate foreign key relationships
        fk_yaml = self.relationship_generator.generate_foreign_key_relationships(fk_relationships, entities_map)
        generated_yaml.extend(fk_yaml)

        # Generate shared field relationships
        shared_yaml = self.relationship_generator.generate_shared_field_relationships(shared_relationships,
                                                                                      entities_map)
        generated_yaml.extend(shared_yaml)

        logger.info(f"Generated {len(generated_yaml)} relationship YAML definitions")
        return generated_yaml

    @staticmethod
    def _calculate_map_statistics(entities_map: Dict[str, Dict],
                                  relationships: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate basic statistics for the relationship map."""
        return {
            'total_entities': len(entities_map),
            'total_relationships': len(relationships),
            'fk_relationships': len([r for r in relationships if r['relationship_type'].startswith('foreign_key')]),
            'shared_field_relationships': len([r for r in relationships if r['relationship_type'] == 'shared_field']),
            'cross_subgraph_relationships': len([r for r in relationships if r.get('cross_subgraph', False)])
        }

    @staticmethod
    def _enrich_relationship_for_entity(rel: Dict[str, Any], entity_qnk: str,
                                        relationship_map: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Enrich a relationship with entity-specific context."""
        from_qnk = rel.get('from_entity')
        to_qnk = rel.get('to_entity')
        entities_map = relationship_map.get('entities', {})

        enriched_rel = rel.copy()

        # Determine direction relative to the current entity
        if from_qnk == entity_qnk:
            enriched_rel['direction'] = 'outgoing'
            # Add target entity info
            target_info = entities_map.get(to_qnk, {})
            enriched_rel.update({
                'to_entity_simple_name': target_info.get('name', '?'),
                'to_entity_kind': target_info.get('kind', '?'),
                'to_entity_subgraph': target_info.get('subgraph')
            })
            return enriched_rel

        elif to_qnk == entity_qnk:
            enriched_rel['direction'] = 'incoming'
            # Add source entity info
            source_info = entities_map.get(from_qnk, {})
            enriched_rel.update({
                'from_entity_simple_name': source_info.get('name', '?'),
                'from_entity_kind': source_info.get('kind', '?'),
                'from_entity_subgraph': source_info.get('subgraph')
            })
            return enriched_rel

        elif rel.get('relationship_type') == 'shared_field':
            # For shared fields, determine the other entity
            other_qnk = from_qnk if to_qnk == entity_qnk else to_qnk
            if other_qnk != entity_qnk:
                enriched_rel['direction'] = 'shared_field'
                enriched_rel['other_entity_qnk'] = other_qnk

                other_info = entities_map.get(other_qnk, {})
                enriched_rel.update({
                    'other_entity_simple_name': other_info.get('name', '?'),
                    'other_entity_kind': other_info.get('kind', '?'),
                    'other_entity_subgraph': other_info.get('subgraph')
                })
                return enriched_rel

        return None

    @staticmethod
    def _deduplicate_entity_relationships(relationships: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate relationships for a specific entity."""
        unique_relationships = []
        seen_keys = set()

        for rel in relationships:
            # Create unique key based on relationship characteristics
            key_parts = [
                rel.get('relationship_type'),
                rel.get('direction'),
                rel.get('to_entity') if rel.get('direction') in ('outgoing', 'shared_field') else rel.get(
                    'from_entity'),
                rel.get('from_field'),
                rel.get('to_field_name'),
                rel.get('shared_field')
            ]

            key = tuple(key_parts)
            if key not in seen_keys:
                seen_keys.add(key)
                unique_relationships.append(rel)

        return unique_relationships

    @staticmethod
    def _format_outgoing_relationships(relationships: List[Dict[str, Any]],
                                       relationship_map: Dict[str, Any]) -> str:
        """Format outgoing foreign key relationships."""
        lines = []
        for rel in relationships:
            from_field = rel.get('from_field', '?')
            target_name = rel.get('to_entity_simple_name', '?')
            target_subgraph = rel.get('to_entity_subgraph', '')
            target_pk = rel.get('to_field_name', 'id')

            target_prefix = f"{target_subgraph}." if target_subgraph else ""
            lines.append(f"- {from_field} -> {target_prefix}{target_name}.{target_pk}")

        return "\n".join(sorted(list(set(lines))))

    @staticmethod
    def _format_incoming_relationships(relationships: List[Dict[str, Any]],
                                       relationship_map: Dict[str, Any]) -> str:
        """Format incoming foreign key relationships."""
        lines = []
        for rel in relationships:
            source_name = rel.get('from_entity_simple_name', '?')
            source_subgraph = rel.get('from_entity_subgraph', '')
            source_fk = rel.get('from_field', '?')
            current_pk = rel.get('to_field_name', 'id')

            source_prefix = f"{source_subgraph}." if source_subgraph else ""
            lines.append(f"- {source_prefix}{source_name}.{source_fk} <- {current_pk}")

        return "\n".join(sorted(list(set(lines))))

    @staticmethod
    def _format_shared_field_relationships(relationships: List[Dict[str, Any]],
                                           relationship_map: Dict[str, Any]) -> str:
        """Format shared field relationships."""
        lines = []
        for rel in relationships:
            shared_field = rel.get('shared_field', '?')
            other_name = rel.get('other_entity_simple_name', '?')
            other_subgraph = rel.get('other_entity_subgraph', '')

            other_prefix = f"{other_subgraph}." if other_subgraph else ""
            lines.append(f"- {shared_field} <-> {other_prefix}{other_name}.{shared_field}")

        return "\n".join(sorted(list(set(lines))))

    @staticmethod
    def _format_other_relationships(relationships: List[Dict[str, Any]],
                                    relationship_map: Dict[str, Any]) -> str:
        """Format other types of relationships."""
        lines = []
        for rel in relationships:
            rel_type = rel.get('relationship_type', 'unknown')
            direction = rel.get('direction', 'unknown')

            if direction == 'outgoing':
                target_name = rel.get('to_entity_simple_name', '?')
                lines.append(f"- {rel_type} -> {target_name}")
            elif direction == 'incoming':
                source_name = rel.get('from_entity_simple_name', '?')
                lines.append(f"- {rel_type} <- {source_name}")
            else:
                lines.append(f"- {rel_type} relationship")

        return "\n".join(sorted(list(set(lines))))


def create_relationship_mapper() -> RelationshipMapper:
    """
    Create a RelationshipMapper instance.

    Returns:
        Configured RelationshipMapper instance
    """
    return RelationshipMapper()
