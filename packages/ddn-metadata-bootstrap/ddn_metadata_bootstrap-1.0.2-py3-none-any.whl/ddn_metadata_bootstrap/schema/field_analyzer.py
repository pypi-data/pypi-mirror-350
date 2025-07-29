#!/usr/bin/env python3

"""
Field analysis and key detection for schema elements.
Analyzes field structures to identify primary keys, foreign keys, and field capabilities.
"""

import logging
from typing import Dict, List, Optional, Any

from ..config import config

logger = logging.getLogger(__name__)


class FieldAnalyzer:
    """
    Analyzes schema fields to identify keys, relationships, and capabilities.

    This class provides functionality to analyze field structures and determine
    which fields can have descriptions, what their roles are (primary key,
    foreign key, etc.), and how they relate to the schema structure.
    """

    def __init__(self):
        """Initialize the field analyzer."""
        self.generic_fields_lower = [gf.lower() for gf in config.generic_fields]
        self.domain_identifiers_lower = [di.lower() for di in config.domain_identifiers]

    def analyze_field_names_for_keys(self, field_names: List[str],
                                     entity_name: str) -> Dict[str, List[str]]:
        """
        Analyze field names to identify potential primary and foreign keys.

        Args:
            field_names: List of field names to analyze
            entity_name: Name of the entity containing these fields

        Returns:
            Dictionary with 'potential_primary_keys' and 'potential_foreign_keys' lists
        """
        keys = {
            'potential_primary_keys': [],
            'potential_foreign_keys': []
        }

        if not entity_name or not field_names:
            return keys

        # Prepare entity name variations for analysis
        table_base_name = entity_name.split('_')[-1] if '_' in entity_name else entity_name
        entity_name_lower = entity_name.lower()
        table_base_name_lower = table_base_name.lower()

        for field_name_orig in field_names:
            if not field_name_orig:
                continue

            field_name = field_name_orig.lower()

            # Primary key detection patterns
            if self._is_potential_primary_key(field_name, entity_name_lower, table_base_name_lower):
                keys['potential_primary_keys'].append(field_name_orig)

            # Foreign key detection patterns
            elif self._is_potential_foreign_key(field_name, entity_name_lower):
                keys['potential_foreign_keys'].append(field_name_orig)

        return keys

    def analyze_for_keys(self, data: Dict) -> Dict[str, List[str]]:
        """
        Analyze a schema element for key fields.

        Args:
            data: Schema element data

        Returns:
            Dictionary with potential key analysis results
        """
        keys = {
            'potential_primary_keys': [],
            'potential_foreign_keys': []
        }

        # Extract element name
        element_name = self._get_element_name(data)
        if not element_name:
            return keys

        # Extract field definitions
        field_defs = self._extract_field_definitions(data)
        field_names = [f['name'] for f in field_defs if f.get('name')]

        if not field_names:
            return keys

        return self.analyze_field_names_for_keys(field_names, element_name)

    def can_have_description(self, data: Dict, context: Optional[Dict] = None) -> bool:
        """
        Check if a schema element can have a description.

        Args:
            data: Schema element data
            context: Optional context information about the element

        Returns:
            True if element can have a description
        """
        if context is None:
            context = {}

        element_kind = data.get('kind', context.get('kind'))
        parent_path = context.get('parent_path', '')
        parent_kind = context.get('parent_kind')
        ancestor_kind = context.get('ancestor_kind')
        effective_parent_kind = parent_kind if parent_kind else ancestor_kind

        # Skip certain kinds that shouldn't have descriptions
        excluded_kinds = {
            "DataConnectorScalarRepresentation",
            "InputObjectField",
            "ScalarTypeValue"
        }
        if element_kind in excluded_kinds:
            return False

        # Skip certain nested elements based on path patterns
        excluded_path_patterns = ['/orderableFields/', '/comparableFields/', '/permissions/']
        if any(pattern.strip('/') in parent_path for pattern in excluded_path_patterns):
            if 'fieldName' in data or 'relationshipName' in data:
                return False

        # OpenDD kinds can have descriptions
        if element_kind in config.opendd_kinds:
            return True

        # Check for field-like elements
        is_field_like = self._is_field_like_element(data, element_kind)
        if is_field_like:
            return self._can_field_have_description(data, context, effective_parent_kind, parent_path)

        # Check for enum values
        if self._is_enum_value(data, parent_path):
            return True

        return False

    def get_field_type_info(self, field_data: Dict) -> Dict[str, Any]:
        """
        Extract detailed type information from a field.

        Args:
            field_data: Field data to analyze

        Returns:
            Dictionary with type information
        """
        type_info = {
            'raw_type': None,
            'base_type': None,
            'is_array': False,
            'is_nullable': True,
            'is_primitive': False,
            'formatted_type': 'Unknown'
        }

        # Get type from various possible locations
        raw_type = field_data.get('type') or field_data.get('outputType')
        if not raw_type:
            return type_info

        type_info['raw_type'] = raw_type

        if isinstance(raw_type, str):
            # Parse GraphQL-style type notation
            type_info.update(self._parse_graphql_type(raw_type))
        else:
            # Handle object-style type definitions
            type_info['formatted_type'] = str(raw_type)

        return type_info

    @staticmethod
    def identify_field_patterns(field_names: List[str]) -> Dict[str, List[str]]:
        """
        Identify common field patterns in a collection of fields.

        Args:
            field_names: List of field names to analyze

        Returns:
            Dictionary mapping pattern types to matching field names
        """
        patterns = {
            'audit_fields': [],
            'identifier_fields': [],
            'temporal_fields': [],
            'status_fields': [],
            'relationship_fields': [],
            'descriptive_fields': [],
            'quantitative_fields': []
        }

        for field_name in field_names:
            if not field_name:
                continue

            field_lower = field_name.lower()

            # Audit fields
            if any(audit in field_lower for audit in
                   ['created_at', 'updated_at', 'created_by', 'updated_by', 'modified']):
                patterns['audit_fields'].append(field_name)

            # Identifier fields
            elif any(id_pattern in field_lower for id_pattern in ['id', 'uuid', 'guid', 'key']):
                patterns['identifier_fields'].append(field_name)

            # Temporal fields
            elif any(time_pattern in field_lower for time_pattern in ['date', 'time', 'timestamp', 'when']):
                patterns['temporal_fields'].append(field_name)

            # Status fields
            elif any(status in field_lower for status in ['status', 'state', 'active', 'enabled', 'deleted', 'flag']):
                patterns['status_fields'].append(field_name)

            # Relationship fields (foreign keys)
            elif field_lower.endswith('_id') and field_lower != 'id':
                patterns['relationship_fields'].append(field_name)

            # Descriptive fields
            elif any(desc in field_lower for desc in ['name', 'title', 'description', 'comment', 'note', 'label']):
                patterns['descriptive_fields'].append(field_name)

            # Quantitative fields
            elif any(qty in field_lower for qty in ['count', 'total', 'sum', 'amount', 'quantity', 'number', 'size']):
                patterns['quantitative_fields'].append(field_name)

        return patterns

    def analyze_field_relationships(self, field_names: List[str],
                                    entity_name: str) -> List[Dict[str, Any]]:
        """
        Analyze fields to identify potential relationships to other entities.

        Args:
            field_names: List of field names to analyze
            entity_name: Name of the containing entity

        Returns:
            List of potential relationship descriptors
        """
        relationships = []

        for field_name in field_names:
            if not field_name:
                continue

            relationship_info = self._analyze_single_field_relationship(field_name, entity_name)
            if relationship_info:
                relationships.append(relationship_info)

        return relationships

    @staticmethod
    def _is_potential_primary_key(field_name: str, entity_name_lower: str,
                                  table_base_name_lower: str) -> bool:
        """Check if a field name indicates a potential primary key."""
        return (
                field_name == 'id' or
                field_name == f"{table_base_name_lower}_id" or
                field_name == f"{entity_name_lower}_id" or
                field_name.endswith('_pk') or
                (field_name.endswith('_key') and not field_name.endswith('_foreign_key'))
        )

    @staticmethod
    def _is_potential_foreign_key(field_name: str, entity_name_lower: str) -> bool:
        """Check if a field name indicates a potential foreign key."""
        return (
                field_name.endswith('_id') and
                field_name not in ['id', f"{entity_name_lower}_id"] and
                not field_name.endswith('_pk')
        )

    @staticmethod
    def _get_element_name(data: Dict) -> Optional[str]:
        """Extract element name from schema data."""
        if isinstance(data.get('definition'), dict):
            name = data['definition'].get('name')
            if name:
                return name
        return data.get('name')

    @staticmethod
    def _extract_field_definitions(data: Dict) -> List[Dict]:
        """Extract field definitions from schema element."""
        field_defs = []

        if isinstance(data.get('definition'), dict):
            definition = data['definition']

            # Regular fields
            fields = definition.get('fields', [])
            if isinstance(fields, list):
                field_defs.extend([f for f in fields if isinstance(f, dict)])

            # Model source properties
            if data.get('kind') == 'Model':
                source = definition.get('source', {})
                if isinstance(source, dict):
                    properties = source.get('properties', [])
                    if isinstance(properties, list):
                        field_defs.extend([p for p in properties if isinstance(p, dict)])

        return field_defs

    @staticmethod
    def _is_field_like_element(data: Dict, element_kind: Optional[str]) -> bool:
        """Check if element is field-like (has name and type but no kind)."""
        return (
                'name' in data and
                ('type' in data or 'outputType' in data) and
                not element_kind
        )

    @staticmethod
    def _can_field_have_description(data: Dict, context: Dict,
                                    effective_parent_kind: Optional[str],
                                    parent_path: str) -> bool:
        """Check if a field-like element can have a description."""
        # Check if we're in a fields or arguments array
        field_path_patterns = ['/fields[', '/arguments[']
        definition_field_patterns = ['/definition/fields[', '/definition/arguments[']

        is_in_field_array = (
                any(pattern in parent_path for pattern in field_path_patterns) or
                any(pattern in parent_path for pattern in definition_field_patterns)
        )

        # Check if parent is a type that can have field descriptions
        valid_parent_kinds = {"ObjectType", "Model", "InputObjectType", "Command", "Type"}
        has_valid_parent = effective_parent_kind in valid_parent_kinds

        if is_in_field_array and has_valid_parent:
            return True

        # Check for legacy path patterns
        legacy_patterns = ['/fields', '/arguments']
        if any(parent_path.endswith(pattern) for pattern in legacy_patterns) and has_valid_parent:
            return True

        return False

    @staticmethod
    def _is_enum_value(data: Dict, parent_path: str) -> bool:
        """Check if element is an enum value."""
        return (
                'value' in data and
                ('/enumValues[' in parent_path or parent_path.endswith('/enumValues'))
        )

    @staticmethod
    def _parse_graphql_type(type_str: str) -> Dict[str, Any]:
        """Parse GraphQL-style type notation."""
        type_info = {
            'base_type': type_str,
            'is_array': False,
            'is_nullable': True,
            'is_primitive': False,
            'formatted_type': type_str
        }

        # Check for non-nullable (!)
        is_nullable = not type_str.endswith('!')
        base_type = type_str.rstrip('!')

        # Check for array ([])
        is_array = base_type.startswith('[') and base_type.endswith(']')
        if is_array:
            inner_type = base_type[1:-1].rstrip('!')
            formatted = f"Array of {inner_type}"
            if not inner_type.endswith('s') and len(inner_type) > 1:
                formatted += 's'
        else:
            inner_type = base_type
            formatted = base_type

        # Check if primitive type
        is_primitive = inner_type in config.primitive_types

        # Add nullability info
        nullable_text = 'nullable' if is_nullable else 'non-nullable'
        formatted += f" ({nullable_text})"

        type_info.update({
            'base_type': inner_type,
            'is_array': is_array,
            'is_nullable': is_nullable,
            'is_primitive': is_primitive,
            'formatted_type': formatted
        })

        return type_info

    def _analyze_single_field_relationship(self, field_name: str,
                                           entity_name: str) -> Optional[Dict[str, Any]]:
        """Analyze a single field for relationship patterns."""
        field_lower = field_name.lower()

        # Foreign key pattern
        if field_lower.endswith('_id') and field_lower != 'id':
            # Extract potential target entity name
            target_entity_base = field_lower[:-3]  # Remove '_id'

            return {
                'field_name': field_name,
                'relationship_type': 'foreign_key',
                'target_entity_guess': target_entity_base,
                'confidence': 'high' if target_entity_base not in self.generic_fields_lower else 'medium'
            }

        # Domain identifier pattern
        for domain_id in self.domain_identifiers_lower:
            if domain_id in field_lower:
                return {
                    'field_name': field_name,
                    'relationship_type': 'domain_identifier',
                    'identifier_type': domain_id,
                    'confidence': 'medium'
                }

        return None


def create_field_analyzer() -> FieldAnalyzer:
    """
    Create a FieldAnalyzer instance.

    Returns:
        Configured FieldAnalyzer instance
    """
    return FieldAnalyzer()
