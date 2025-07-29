#!/usr/bin/env python3

"""
Configuration management for Metadata Bootstrap.
Centralizes all environment variables, defaults, and configuration parsing.
"""

import os
import re
import logging
from typing import Dict, List, cast
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables from multiple possible locations
def load_env_files():
    """Load .env files from multiple possible locations."""
    possible_env_paths = [
        # Current working directory
        Path.cwd() / '.env',
        # Same directory as this config file
        Path(__file__).parent / '.env',
        # Parent directory of the package
        Path(__file__).parent.parent / '.env',
        # Common project root locations
        Path.cwd().parent / '.env',
    ]

    env_loaded = False
    for env_path in possible_env_paths:
        if env_path.exists():
            load_dotenv(env_path)
            print(f"✅ Loaded environment variables from: {env_path}")
            env_loaded = True
            break

    if not env_loaded:
        print("⚠️  No .env file found. Using system environment variables only.")
        print(f"   Searched in: {[str(p) for p in possible_env_paths]}")


# Load environment variables
load_env_files()

logger = logging.getLogger(__name__)


class BootstrapperConfig:
    """Configuration class for Metadata Bootstrapper."""

    def __init__(self):
        # API Configuration
        self.model = os.environ.get('METADATA_BOOTSTRAP_MODEL', 'claude-3-haiku-20240307')
        self.api_key = os.environ.get('ANTHROPIC_API_KEY')

        # Processing Configuration
        self.line_length = int(os.environ.get('METADATA_BOOTSTRAP_LINE_LENGTH', '65'))
        self.field_desc_max_length = int(os.environ.get('METADATA_BOOTSTRAP_FIELD_DESC_MAX_LENGTH', '120'))
        self.kind_desc_max_length = int(os.environ.get('METADATA_BOOTSTRAP_KIND_DESC_MAX_LENGTH', '250'))
        self.field_tokens = int(os.environ.get('METADATA_BOOTSTRAP_FIELD_TOKENS', '250'))
        self.kind_tokens = int(os.environ.get('METADATA_BOOTSTRAP_KIND_TOKENS', '400'))

        # Target lengths for concise descriptions
        self.short_field_target = int(os.environ.get('METADATA_BOOTSTRAP_SHORT_FIELD_TARGET', '100'))
        self.short_kind_target = int(os.environ.get('METADATA_BOOTSTRAP_SHORT_KIND_TARGET', '180'))

        # Processing limits
        self.max_examples = int(os.environ.get('METADATA_BOOTSTRAP_MAX_EXAMPLES', '5'))
        self.max_domain_keywords = int(os.environ.get('METADATA_BOOTSTRAP_MAX_DOMAIN_KEYWORDS', '10'))
        self.token_efficient = os.environ.get('METADATA_BOOTSTRAP_TOKEN_EFFICIENT', 'True').lower() in (
        'true', 'yes', '1')

        # File patterns
        self.file_glob = os.environ.get('FILE_GLOB', "**/metadata/*.hml")

        # Exclusions
        self.excluded_kinds = self._parse_list(
            os.environ.get('METADATA_BOOTSTRAP_EXCLUDED_KINDS',
                           "DataConnectorScalarRepresentation,DataConnectorLink,BooleanExpressionType,ScalarType,AggregateExpression")
        )

        self.excluded_files = self._parse_list(
            os.environ.get('METADATA_BOOTSTRAP_EXCLUDED_FILES', '')
        )

        # Field classifications
        self.generic_fields = self._parse_list(
            os.environ.get('METADATA_BOOTSTRAP_GENERIC_FIELDS',
                           "id,key,code,name,description,created_at,updated_at,updated,created,status,active,enabled,timestamp")
        )

        self.domain_identifiers = self._parse_list(
            os.environ.get('METADATA_BOOTSTRAP_DOMAIN_IDENTIFIERS',
                           "iata,icao,isbn,swift,duns,cusip,sedol,gtin,upc,ean,faa,ein,ssn,passport,license,registration")
        )

        # Domain mappings
        self.domain_mappings = self._parse_domain_mappings(
            os.environ.get('METADATA_BOOTSTRAP_DOMAIN_MAPPINGS', '')
        )

        # OpenDD schema types
        self.primitive_types = self._parse_list(
            os.environ.get('METADATA_BOOTSTRAP_PRIMITIVE_TYPES', "ID,Int,Float,Boolean,String")
        )

        self.opendd_kinds = self._parse_list(
            os.environ.get('METADATA_BOOTSTRAP_KINDS',
                           "Type,Command,Model,Relationship,ObjectType,ScalarType,EnumType,InputObjectType," +
                           "BooleanExpressionType,ObjectBooleanExpressionType,DataConnectorLink,Subgraph," +
                           "Supergraph,Role,AuthConfig,CompatibilityConfig,GraphqlConfig")
        )

        # FK Templates
        self.fk_templates_string = os.environ.get('METADATA_BOOTSTRAP_FK_TEMPLATES',
                                                  "id|{pt}_id,{gi}|{pt}_{gi},id|{ps}_{pt}_id,{gi}|{ps}_{pt}_{gi}")

        # Parse FK templates
        self.fk_templates = self._parse_fk_templates()

        # Special markers
        self.relationship_marker = "***ADD_RELATIONSHIPS***"

    def _parse_list(self, value: str) -> List[str]:
        """Parse comma-separated string into list, filtering empty values."""
        if not value:
            return []
        return [item.strip() for item in value.split(',') if item.strip()]

    def _parse_domain_mappings(self, value: str) -> Dict[str, List[str]]:
        """Parse domain mappings from environment variable."""
        mappings = {}
        if not value:
            return mappings

        try:
            for domain_group in value.split('|'):
                if ':' in domain_group:
                    domain, terms = domain_group.split(':', 1)
                    mappings[domain.strip()] = [t.strip() for t in terms.split(',')]
        except Exception as e:
            logger.warning(f"Failed to parse domain mappings: {e}")

        return mappings

    def _parse_fk_templates(self) -> List[Dict]:
        """Parse FK templates from configuration string."""
        parsed_templates = []

        if not self.fk_templates_string:
            logger.warning("No FK templates string provided.")
            return parsed_templates

        template_pairs = self.fk_templates_string.split(',')
        logger.info(f"Raw FK template pairs: {template_pairs}")

        # Build regex patterns
        pt_re = r"(?P<primary_table>\w+?)"
        ps_re = r"(?P<primary_subgraph>\w+?)"
        fs_re = r"(?P<foreign_subgraph>\w+?)"

        sorted_generic_fields = sorted(self.generic_fields, key=len, reverse=True)
        gi_re_options = "|".join(re.escape(gf) for gf in sorted_generic_fields)
        gi_re = f"(?P<generic_id>(?:{gi_re_options}))"

        for tpl_pair_str in template_pairs:
            tpl_pair_str = tpl_pair_str.strip()
            if not tpl_pair_str:
                continue

            if '|' not in tpl_pair_str:
                logger.warning(f"Invalid FK template pair (missing '|'): '{tpl_pair_str}'. Skipping.")
                continue

            pk_tpl_str, fk_tpl_str_orig = [part.strip() for part in tpl_pair_str.split('|', 1)]

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
                logger.info(f"Successfully parsed FK template: PK='{pk_tpl_str}', FK_Orig='{fk_tpl_str_orig}'")
            except re.error as e:
                logger.error(f"Failed to compile regex for FK template '{fk_tpl_str_orig}': {e}")

        if not parsed_templates:
            logger.warning("No FK templates were successfully parsed. FK detection might be limited.")

        return parsed_templates

    def validate(self) -> bool:
        """Validate configuration and return True if valid."""
        errors = []

        if not self.api_key:
            errors.append("ANTHROPIC_API_KEY is required")

        if self.line_length < 20:
            errors.append("Line length must be at least 20 characters")

        if self.field_desc_max_length < 50:
            errors.append("Field description max length must be at least 50 characters")

        if self.kind_desc_max_length < 100:
            errors.append("Kind description max length must be at least 100 characters")

        if errors:
            for error in errors:
                logger.error(f"Configuration error: {error}")
            return False

        return True

    def get_io_config(self) -> Dict[str, str]:
        """Get input/output configuration from environment."""
        return {
            'input_dir': os.environ.get('METADATA_BOOTSTRAP_INPUT_DIR'),
            'output_dir': os.environ.get('METADATA_BOOTSTRAP_OUTPUT_DIR'),
            'input_file': os.environ.get('METADATA_BOOTSTRAP_INPUT_FILE'),
            'output_file': os.environ.get('METADATA_BOOTSTRAP_OUTPUT_FILE'),
            'use_case': os.environ.get('METADATA_BOOTSTRAP_USE_CASE')
        }


# Global configuration instance
config = BootstrapperConfig()
