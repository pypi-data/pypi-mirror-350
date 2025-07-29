#!/usr/bin/env python3

"""
AI-powered description generation for schema elements.
Handles communication with Anthropic API and description quality control.
"""

import logging
from typing import Dict, Set, Optional, Any

import anthropic

from ..config import config
from ..utils.text_utils import clean_description_response, refine_ai_description, normalize_description

logger = logging.getLogger(__name__)


class DescriptionGenerator:
    """Handles AI-powered description generation for schema elements."""

    def __init__(self, api_key: str, model: Optional[str] = None):
        """
        Initialize the description generator.

        Args:
            api_key: Anthropic API key
            model: Model to use (defaults to config value)
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model or config.model

    def generate_field_description(self, field_data: Dict, context: Dict) -> str:
        """
        Generate a description for a field.

        Args:
            field_data: Dictionary containing field information
            context: Context information about the field's parent

        Returns:
            Generated description or empty string if generation fails
        """
        field_name = field_data.get('name')
        if not field_name:
            return ""

        max_len = config.field_desc_max_length
        target_len = config.short_field_target
        parent_name = context.get('name', context.get('parent_name'))
        parent_kind = context.get('kind', context.get('parent_kind'))
        field_type_formatted = self._format_type(field_data.get('type', field_data.get('outputType')))

        prompt = (f"Concise description (max {max_len} chars) for field '{field_name}' "
                  f"(type: {field_type_formatted}) within '{parent_name}' ({parent_kind}). "
                  f"Purpose only. Complete sentence. No fluff.")

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=config.field_tokens,
                messages=[{"role": "user", "content": prompt}]
            )

            desc = response.content[0].text.strip() if response and response.content else ""
            desc = clean_description_response(desc)
            desc = refine_ai_description(desc)

            if (len(desc) <= max_len and
                    self._validate_description(desc, set(), "Field", field_name) and
                    len(desc.split()) >= 2):
                return normalize_description(desc, line_length=config.field_desc_max_length,
                                             make_token_efficient=True)

            # Try with shorter target if first attempt was too long
            logger.info(f"Field '{field_name}' in '{parent_name}' first desc too long "
                        f"({len(desc)} > {max_len}) or invalid. Retrying (target < {target_len} chars).")

            shorter_prompt = (f"Very concise description (strictly under {target_len} chars) "
                              f"for field '{field_name}'. Core meaning. Complete sentence.")

            shorter_tokens = max(30, int(target_len / 2.5))
            response_short = self.client.messages.create(
                model=self.model,
                max_tokens=shorter_tokens,
                messages=[{"role": "user", "content": shorter_prompt}]
            )

            desc_short = response_short.content[0].text.strip() if response_short and response_short.content else ""
            desc_short = clean_description_response(desc_short)
            desc_short = refine_ai_description(desc_short)

            if (self._validate_description(desc_short, set(), "Field", field_name) and
                    desc_short and len(desc_short.split()) >= 2):
                return normalize_description(desc_short, line_length=config.field_desc_max_length,
                                             make_token_efficient=True)
            else:
                logger.warning(f"Field '{field_name}' re-gen failed. Using original (len {len(desc)}) or empty.")
                return (normalize_description(desc, line_length=config.field_desc_max_length,
                                              make_token_efficient=True)
                        if desc and self._validate_description(desc, set(), "Field", field_name)
                           and len(desc.split()) >= 2 else "")

        except Exception as e:
            logger.error(f"API error for field '{field_name}' in '{parent_name}': {e}")
            return ""

    def generate_kind_description(self, data: Dict, context: Dict) -> str:
        """
        Generate a description for a schema kind (ObjectType, Model, etc.).

        Args:
            data: Dictionary containing kind information
            context: Context information about the kind

        Returns:
            Generated description or empty string if generation fails
        """
        kind = context.get('kind')
        element_name = context.get('name')

        if not kind or not element_name:
            return ""

        max_len = config.kind_desc_max_length
        target_len = config.short_kind_target

        prompt = (f"Generate a concise, business-focused description (max {max_len} chars) "
                  f"for the schema element '{element_name}' of kind '{kind}'. "
                  f"Focus on purpose and intent. No YAML details, no kind mention, "
                  f"no prefatory phrases. Complete sentences.")

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=config.kind_tokens,
                messages=[{"role": "user", "content": prompt}]
            )

            desc = response.content[0].text.strip() if response and response.content else ""
            desc = clean_description_response(desc)
            desc = refine_ai_description(desc)

            if (len(desc) <= max_len and
                    self._validate_description(desc, set(), kind, element_name)):
                return normalize_description(desc, line_length=config.line_length,
                                             make_token_efficient=True)

            # Try with shorter target if first attempt was too long
            logger.info(f"Kind '{element_name}' ({kind}) first desc too long "
                        f"({len(desc)} > {max_len}) or invalid. Retrying (target < {target_len} chars).")

            shorter_prompt = (f"Generate a very concise description (strictly under {target_len} chars, "
                              f"ideally around {int(target_len * 0.8)}-{target_len} chars) "
                              f"for '{element_name}' ({kind}). Core purpose only. Complete sentences. No fluff.")

            shorter_tokens = max(50, int(target_len / 2))
            response_short = self.client.messages.create(
                model=self.model,
                max_tokens=shorter_tokens,
                messages=[{"role": "user", "content": shorter_prompt}]
            )

            desc_short = response_short.content[0].text.strip() if response_short and response_short.content else ""
            desc_short = clean_description_response(desc_short)
            desc_short = refine_ai_description(desc_short)

            if self._validate_description(desc_short, set(), kind, element_name) and desc_short:
                return normalize_description(desc_short, line_length=config.line_length,
                                             make_token_efficient=True)
            else:
                logger.warning(f"Kind '{element_name}' ({kind}) re-gen failed. "
                               f"Using original (len {len(desc)}) or empty.")
                return (normalize_description(desc, line_length=config.line_length,
                                              make_token_efficient=True)
                        if desc and self._validate_description(desc, set(), kind, element_name) else "")

        except Exception as e:
            logger.error(f"API error for {kind} '{element_name}': {e}")
            return ""

    @staticmethod
    def _format_type(type_str: Any) -> str:
        """
        Format type information for display in prompts.

        Args:
            type_str: Type string to format

        Returns:
            Formatted type string
        """
        if not type_str or not isinstance(type_str, str):
            return "UnknownType"

        is_nullable = not type_str.endswith('!')
        base_type = type_str.rstrip('!')

        if base_type.startswith('[') and base_type.endswith(']'):
            inner = base_type[1:-1].rstrip('!').replace('[', '').replace(']', '')
            return (f"Array of {inner}{'s' if not inner.endswith('s') and len(inner) > 1 else ''} "
                    f"({'nullable' if is_nullable else 'non-nullable'})")

        return f"{base_type} ({'nullable' if is_nullable else 'non-nullable'})"

    @staticmethod
    def _validate_description(description: str, domain_keywords: Set[str],
                              kind: str, name: str) -> bool:
        """
        Validate that a description meets basic quality criteria.

        Args:
            description: Description to validate
            domain_keywords: Set of domain-specific keywords (unused in current implementation)
            kind: Type of schema element
            name: Name of schema element

        Returns:
            True if description is valid, False otherwise
        """
        return bool(description and description.strip())
