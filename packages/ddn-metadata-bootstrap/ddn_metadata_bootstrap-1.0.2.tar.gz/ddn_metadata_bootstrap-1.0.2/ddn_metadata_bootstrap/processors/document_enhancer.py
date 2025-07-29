#!/usr/bin/env python3

"""
YAML document structure enhancement for adding AI-generated descriptions.
Handles the traversal and enhancement of YAML/HML document structures.
"""

import logging
from typing import Dict, List, Any, Optional

from ..ai.description_generator import DescriptionGenerator
from ..config import config
from ..schema.field_analyzer import FieldAnalyzer

logger = logging.getLogger(__name__)


class DocumentEnhancer:
    """
    Enhances YAML document structures by adding AI-generated descriptions.

    This class traverses YAML/HML document structures, identifies elements that
    can have descriptions, generates appropriate descriptions using AI, and
    integrates relationship information into the descriptions.
    """

    def __init__(self, description_generator: DescriptionGenerator):
        """
        Initialize the document enhancer.

        Args:
            description_generator: AI description generator instance
        """
        self.description_generator = description_generator
        self.field_analyzer = FieldAnalyzer()

    def enhance_yaml_structure(self, data: Any, parent_path: str = "",
                               parent_info: Optional[Dict] = None,
                               dict_key: Optional[str] = None) -> Any:
        """
        Enhance a YAML structure by adding descriptions to eligible elements.

        Args:
            data: YAML data structure to enhance
            parent_path: Current path in the structure
            parent_info: Information about the parent element
            dict_key: Key name if this element is a dictionary value

        Returns:
            Enhanced YAML structure with added descriptions
        """
        if parent_info is None:
            parent_info = {}

        # Skip excluded kinds entirely
        if parent_info.get('kind') in config.excluded_kinds:
            return data

        # Skip if current element is excluded (for root-level or nested excluded elements)
        if isinstance(data, dict) and data.get('kind') in config.excluded_kinds:
            return data

        if isinstance(data, dict):
            return self._enhance_dict_structure(data, parent_path, parent_info, dict_key)
        elif isinstance(data, list):
            return self._enhance_list_structure(data, parent_path, parent_info, dict_key)
        else:
            return data

    def enhance_with_relationships(self, documents: List[Any],
                                   relationship_map: Dict[str, Any],
                                   subgraph: Optional[str] = None) -> List[Any]:
        """
        Enhance documents by adding relationship information to descriptions.

        Args:
            documents: List of YAML documents to enhance
            relationship_map: Comprehensive relationship map
            subgraph: Optional subgraph context

        Returns:
            List of enhanced documents with relationship information
        """
        enhanced_documents = []

        for doc in documents:
            if doc is None:
                enhanced_documents.append(None)
                continue

            enhanced_doc = self._process_document_for_relationships(
                doc, relationship_map, subgraph
            )
            enhanced_documents.append(enhanced_doc)

        return enhanced_documents

    def can_have_description(self, data: Dict, context: Optional[Dict] = None) -> bool:
        """
        Check if a schema element can have a description.

        Args:
            data: Schema element data
            context: Optional context information

        Returns:
            True if element can have a description
        """
        return self.field_analyzer.can_have_description(data, context)

    @staticmethod
    def should_generate_description(existing_description: str) -> bool:
        """
        Check if we should generate/regenerate a description.

        Args:
            existing_description: Current description content

        Returns:
            True if description should be generated
        """
        if not existing_description or not existing_description.strip():
            return True
        if existing_description.strip().startswith('!'):
            return True
        return False

    @staticmethod
    def clean_description_for_regeneration(existing_description: str) -> str:
        """
        Clean description for regeneration by removing '!' prefix if present.

        Args:
            existing_description: Description to clean

        Returns:
            Cleaned description
        """
        if not existing_description:
            return ""
        cleaned = existing_description.strip()
        if cleaned.startswith('!'):
            return cleaned[1:].strip()
        return cleaned

    def _enhance_dict_structure(self, data: Dict, parent_path: str,
                                parent_info: Dict, dict_key: Optional[str]) -> Dict:
        """Enhance a dictionary structure."""
        current_kind = data.get('kind')
        current_name = data.get('definition', {}).get('name', data.get('name', ''))

        # Build current path segment
        if current_kind in config.opendd_kinds:
            current_path_segment = current_name if current_name else current_kind
        elif dict_key:
            current_path_segment = dict_key
        else:
            current_path_segment = current_name if current_name else "dict_node"

        # Build the current path
        current_path = f"{parent_path}/{current_path_segment}".strip('/') if parent_path else current_path_segment

        # Determine effective kind and ancestor kind
        effective_kind = current_kind if current_kind else parent_info.get('ancestor_kind')
        ancestor_kind = current_kind if current_kind in config.opendd_kinds else parent_info.get('ancestor_kind')

        # Build current element context
        current_element_context = {
            'name': current_name,
            'kind': current_kind,
            'type': data.get('type', data.get('outputType')),
            'parent_name': parent_info.get('name'),
            'parent_kind': parent_info.get('kind'),
            'ancestor_kind': ancestor_kind,
            'path': current_path,
            'parent_path': parent_path
        }

        # Handle OpenDD kinds specially
        if current_kind in config.opendd_kinds:
            return self._enhance_opendd_kind(data.copy(), current_element_context)

        # Handle field-like objects
        is_field_like = self._is_field_like_element(data, current_kind)
        if is_field_like:
            return self._enhance_field_like_element(data.copy(), current_element_context)

        # Handle regular dictionaries
        enhanced_dict = {}
        for key, value in data.items():
            enhanced_dict[key] = self.enhance_yaml_structure(
                value, current_path, current_element_context, key
            )

        return enhanced_dict

    def _enhance_list_structure(self, data: List, parent_path: str,
                                parent_info: Dict, dict_key: Optional[str]) -> List:
        """Enhance a list structure."""
        # Incorporate dict_key if provided
        if dict_key:
            list_path = f"{parent_path}/{dict_key}".strip('/')
        else:
            list_path = parent_path

        enhanced_list = []
        for i, item in enumerate(data):
            item_path = f"{list_path}[{i}]"
            enhanced_item = self.enhance_yaml_structure(item, item_path, parent_info, None)
            enhanced_list.append(enhanced_item)

        return enhanced_list

    def _enhance_opendd_kind(self, data_copy: Dict, context: Dict) -> Dict:
        """Enhance an OpenDD kind element."""
        kind = context.get('kind')

        # Ensure definition structure exists for most OpenDD kinds
        if ('definition' not in data_copy and
                kind not in ['Subgraph', 'Supergraph', 'Role'] and
                kind in config.opendd_kinds):
            data_copy['definition'] = {}

        # Move description to definition if needed
        if ('description' in data_copy and
                isinstance(data_copy.get('definition'), dict) and
                'description' not in data_copy['definition']):
            data_copy['definition']['description'] = data_copy.pop('description')

        # Generate description if needed
        if self.can_have_description(data_copy, context):
            current_description = self._get_current_description(data_copy)

            if self.should_generate_description(current_description):
                description_text = self.description_generator.generate_kind_description(data_copy, context)
                if description_text:
                    # Add marker to signal that relationships should be added in second pass
                    description_with_marker = f"{description_text}\n{config.relationship_marker}"
                    self._set_description(data_copy, description_with_marker)

        # Process other keys recursively
        for key, value in list(data_copy.items()):
            if key not in ['kind', 'version', 'name', 'description']:
                data_copy[key] = self.enhance_yaml_structure(
                    value, context['path'], context, key
                )

        return data_copy

    def _enhance_field_like_element(self, field_copy: Dict, context: Dict) -> Dict:
        """Enhance a field-like element."""
        if self.can_have_description(field_copy, context):
            current_description = field_copy.get('description', '')

            if self.should_generate_description(current_description):
                description = self.description_generator.generate_field_description(field_copy, context)
                if description:
                    # Add marker to signal that relationships should be added in second pass
                    field_copy['description'] = f"{description}\n{config.relationship_marker}"

        # Process other field properties recursively
        enhanced_dict = {}
        for key, value in field_copy.items():
            if key != 'description':
                enhanced_dict[key] = self.enhance_yaml_structure(
                    value, context['path'], context, key
                )
            else:
                enhanced_dict[key] = field_copy[key]

        return enhanced_dict

    def _process_document_for_relationships(self, document: Any,
                                            relationship_map: Dict[str, Any],
                                            subgraph: Optional[str]) -> Any:
        """Process a document to add relationship information to descriptions."""

        def process_element(element_data, current_path_str=""):
            if isinstance(element_data, dict):
                element_data = self._process_dict_element_relationships(
                    element_data, relationship_map, subgraph, current_path_str
                )

                # Recursively process nested elements
                element_name = element_data.get('definition', {}).get('name', element_data.get('name'))
                element_kind = element_data.get('kind')
                path_segment = element_name if element_name else element_kind if element_kind else "item"
                new_path = f"{current_path_str}/{path_segment}".strip('/')

                for key, value in list(element_data.items()):
                    if key == 'description' and (isinstance(element_data.get('definition'), dict) or element_kind):
                        continue  # Skip description as it's already processed
                    element_data[key] = process_element(value, new_path)

            elif isinstance(element_data, list):
                element_data = [process_element(item, f"{current_path_str}[{i}]")
                                for i, item in enumerate(element_data)]

            return element_data

        return process_element(document)

    def _process_dict_element_relationships(self, element_data: Dict,
                                            relationship_map: Dict[str, Any],
                                            subgraph: Optional[str],
                                            current_path_str: str) -> Dict:
        """Process a dictionary element for relationship information."""
        element_kind = element_data.get('kind')

        # Skip excluded kinds entirely - don't add any descriptions
        if element_kind and element_kind in config.excluded_kinds:
            return element_data

        element_name = element_data.get('definition', {}).get('name', element_data.get('name'))

        # Check if this element has a description with marker
        current_description = self._get_current_description(element_data)
        has_marker = config.relationship_marker in current_description if current_description else False
        cleaned_description = (current_description.replace(f"\n{config.relationship_marker}", "")
                               .replace(config.relationship_marker, "") if current_description else "")

        final_description_content = cleaned_description

        # Add relationships if this is an OpenDD kind with marker and we have relationships
        if element_kind and element_name and has_marker:
            from ..relationships.mapper import RelationshipMapper
            relationship_mapper = RelationshipMapper()

            entity_relationships = relationship_mapper.get_entity_relationships(
                element_name, element_kind, subgraph, relationship_map
            )

            if entity_relationships:
                current_qnk = (f"{subgraph}/{element_kind}/{element_name}"
                               if subgraph else f"{element_kind}/{element_name}")
                relationship_text = relationship_mapper.format_relationships_for_prompt(
                    entity_relationships, relationship_map, current_qnk
                )

                if relationship_text and relationship_text.strip():
                    separator = "\n\n" if final_description_content.strip() else ""
                    final_description_content += f"{separator}Key Relationships:\n{relationship_text}"

        # For field-like elements, just remove marker without adding relationships
        elif has_marker and not element_kind:
            # This is a field - just clean the marker
            pass

        # Update the element with final description (only if we have meaningful content)
        self._set_description(element_data, final_description_content)

        return element_data

    @staticmethod
    def _is_field_like_element(data: Dict, element_kind: Optional[str]) -> bool:
        """Check if element is field-like (has name and type but no kind)."""
        return (
                'name' in data and
                ('type' in data or 'outputType' in data) and
                not element_kind
        )

    @staticmethod
    def _get_current_description(data: Dict) -> str:
        """Get the current description from various possible locations."""
        if isinstance(data.get('definition'), dict):
            return data['definition'].get('description', "")
        elif 'description' in data:
            return data.get('description', "")
        return ""

    @staticmethod
    def _set_description(data: Dict, description: str) -> None:
        """Set description in the appropriate location."""
        # Don't set empty or whitespace-only descriptions
        if not description or not description.strip():
            return

        if isinstance(data.get('definition'), dict):
            data['definition']['description'] = description
        elif 'description' in data or description:
            data['description'] = description

    def get_enhancement_statistics(self, original_data: Any, enhanced_data: Any) -> Dict[str, Any]:
        """
        Get statistics about the enhancement process.

        Args:
            original_data: Original YAML data
            enhanced_data: Enhanced YAML data

        Returns:
            Dictionary with enhancement statistics
        """
        stats = {
            'elements_processed': 0,
            'descriptions_added': 0,
            'descriptions_updated': 0,
            'field_descriptions': 0,
            'kind_descriptions': 0,
            'elements_with_markers': 0
        }

        def count_elements(data, is_enhanced=False):
            if isinstance(data, dict):
                stats['elements_processed'] += 1

                # Check for descriptions
                description = self._get_current_description(data)
                if description:
                    if is_enhanced:
                        if config.relationship_marker in description:
                            stats['elements_with_markers'] += 1

                        # Determine if this is a field or kind description
                        if data.get('kind'):
                            stats['kind_descriptions'] += 1
                        elif 'name' in data and ('type' in data or 'outputType' in data):
                            stats['field_descriptions'] += 1

                # Recurse into nested structures
                for value in data.values():
                    count_elements(value, is_enhanced)

            elif isinstance(data, list):
                for item in data:
                    count_elements(item, is_enhanced)

        # Count original elements
        original_descriptions = stats['kind_descriptions'] + stats['field_descriptions']
        count_elements(original_data, False)

        # Count enhanced elements
        stats['kind_descriptions'] = 0
        stats['field_descriptions'] = 0
        count_elements(enhanced_data, True)
        enhanced_descriptions = stats['kind_descriptions'] + stats['field_descriptions']

        # Calculate additions and updates
        stats['descriptions_added'] = max(0, enhanced_descriptions - original_descriptions)

        return stats


def create_document_enhancer(description_generator: DescriptionGenerator) -> DocumentEnhancer:
    """
    Create a DocumentEnhancer instance.

    Args:
        description_generator: AI description generator instance

    Returns:
        Configured DocumentEnhancer instance
    """
    return DocumentEnhancer(description_generator)
