#!/usr/bin/env python3

"""
Directory processing for metadata bootstrap operations.
Handles the processing of entire directories containing multiple HML/YAML files.
"""

import logging
import os
import shutil
from collections import defaultdict
from typing import Dict, List, Any, Optional, Tuple

from .document_enhancer import DocumentEnhancer
from .file_processor import FileProcessor
from ..config import config
from ..relationships.detector import RelationshipDetector
from ..relationships.generator import RelationshipGenerator
from ..relationships.mapper import RelationshipMapper
from ..schema.domain_analyzer import DomainAnalyzer
from ..schema.metadata_collector import MetadataCollector
from ..utils.path_utils import FileCollector, get_file_stats
from ..utils.yaml_utils import save_yaml_documents

logger = logging.getLogger(__name__)


class DirectoryProcessor:
    """
    Processes entire directories of HML/YAML files through the enhancement workflow.

    This class orchestrates the processing of multiple files in a directory structure,
    handling cross-file relationships, domain analysis across the entire schema,
    and coordinated output generation.
    """

    def __init__(self, metadata_collector: MetadataCollector,
                 domain_analyzer: DomainAnalyzer,
                 relationship_detector: RelationshipDetector,
                 relationship_mapper: RelationshipMapper,
                 relationship_generator: RelationshipGenerator,
                 document_enhancer: DocumentEnhancer):
        """
        Initialize the directory processor with required components.

        Args:
            metadata_collector: Schema metadata collector
            domain_analyzer: Domain analysis component
            relationship_detector: Relationship detection component
            relationship_mapper: Relationship mapping component
            relationship_generator: Relationship generation component
            document_enhancer: Document enhancement component
        """
        self.metadata_collector = metadata_collector
        self.domain_analyzer = domain_analyzer
        self.relationship_detector = relationship_detector
        self.relationship_mapper = relationship_mapper
        self.relationship_generator = relationship_generator
        self.document_enhancer = document_enhancer

        # Create file processor for individual file handling
        self.file_processor = FileProcessor(
            metadata_collector, domain_analyzer, relationship_detector,
            relationship_mapper, relationship_generator, document_enhancer
        )

        # Processing state
        self.schema_metadata: Dict[str, Dict] = {}
        self.enhanced_documents_by_file: Dict[str, List] = {}
        self.generated_relationships: List[Dict] = []
        self.processing_statistics: Dict[str, Any] = {}

    def process_directory(self, input_dir: str, output_dir: str) -> Dict[str, Any]:
        """
        Process an entire directory of HML files.

        Args:
            input_dir: Input directory path
            output_dir: Output directory path

        Returns:
            Dictionary with comprehensive processing results
        """
        logger.info(f"Starting directory processing: {input_dir} -> {output_dir}")

        try:
            # Initialize processing
            os.makedirs(output_dir, exist_ok=True)

            # Collect and filter files
            processed_files, excluded_files = self._collect_and_filter_files(input_dir)

            if not processed_files:
                logger.warning("No files to process")
                return self._create_empty_result(input_dir, output_dir)

            # Scan for existing relationships across all files
            self._scan_for_existing_relationships(processed_files)

            # Perform first pass: collect metadata and enhance structures
            self._perform_first_pass(processed_files, input_dir)

            # Build comprehensive relationship map
            relationship_map = self._build_comprehensive_relationship_map()

            # Perform second pass: add relationship information and save files
            self._perform_second_pass(relationship_map, input_dir, output_dir)

            # Generate and write relationship definitions
            self._write_relationship_definitions(output_dir)

            # Copy excluded files
            self._copy_excluded_files(excluded_files, input_dir, output_dir)

            # Calculate final statistics
            return self._calculate_final_statistics(
                input_dir, output_dir, processed_files, excluded_files
            )

        except Exception as e:
            logger.error(f"Error in directory processing: {e}")
            logger.debug("Full traceback:", exc_info=True)

            return {
                'success': False,
                'error': str(e),
                'input_dir': input_dir,
                'output_dir': output_dir
            }

    @staticmethod
    def _collect_and_filter_files(input_dir: str) -> Tuple[List[str], List[str]]:
        """Collect and filter HML files from input directory."""
        # Use FileCollector to find and filter files
        collector = FileCollector(input_dir, config.file_glob)

        # Add exclusions from configuration
        for excluded_file in config.excluded_files:
            if excluded_file:  # Skip empty strings
                collector.add_exclusion(excluded_file)

        # Collect all files
        all_files = collector.collect_files()

        # Separate processed and excluded files
        processed_files = []
        excluded_files = []

        for file_path in all_files:
            filename = os.path.basename(file_path)
            if filename in config.excluded_files:
                excluded_files.append(file_path)
            else:
                processed_files.append(file_path)

        logger.info(
            f"Found {len(all_files)} HML files: {len(processed_files)} to process, {len(excluded_files)} excluded")

        # Log subgraph summary
        subgraph_summary = collector.get_subgraph_summary(processed_files)
        logger.info(f"Files by subgraph: {subgraph_summary}")

        return processed_files, excluded_files

    def _scan_for_existing_relationships(self, file_paths: List[str]) -> None:
        """Scan all files for existing relationship definitions."""
        existing_signatures = self.relationship_detector.scan_for_existing_relationships(file_paths)
        logger.info(f"Found {len(existing_signatures)} existing relationship signatures across all files")

    def _perform_first_pass(self, file_paths: List[str], input_dir: str) -> None:
        """Perform first pass: metadata collection and structure enhancement."""
        logger.info("Starting first pass: metadata collection and structure enhancement")

        self.schema_metadata = {}
        self.enhanced_documents_by_file = {}

        for file_path in file_paths:
            try:
                logger.debug(f"First pass processing: {file_path}")

                # Process file using file processor's first pass logic
                results = self._process_file_first_pass(file_path, input_dir)

                if results:
                    rel_path, enhanced_docs, metadata = results
                    self.schema_metadata[rel_path] = metadata
                    self.enhanced_documents_by_file[rel_path] = enhanced_docs

                    logger.debug(f"First pass completed: {file_path}")

            except Exception as e:
                logger.error(f"Error in first pass for {file_path}: {e}")
                logger.debug("Full traceback:", exc_info=True)

        total_entities = sum(len(meta.get('entities', [])) for meta in self.schema_metadata.values())
        logger.info(f"First pass complete: {len(self.schema_metadata)} files, {total_entities} entities")

    def _process_file_first_pass(self, file_path: str, input_dir: str) -> Optional[Tuple[str, List, Dict]]:
        """Process a single file in the first pass."""
        from ..utils.yaml_utils import load_yaml_documents
        from ..utils.path_utils import extract_subgraph_from_path

        try:
            # Load documents
            documents = load_yaml_documents(file_path)
            if not documents or all(d is None for d in documents):
                logger.warning(f"Empty or invalid YAML: {file_path}")
                return None

            # Extract file metadata
            subgraph = extract_subgraph_from_path(file_path)
            rel_path = os.path.relpath(file_path, input_dir)

            # Initialize metadata
            metadata = {
                'entities': [],
                'subgraph': subgraph,
                'file_path': rel_path
            }

            enhanced_documents = []

            # Process each document
            for doc in documents:
                if doc is not None:
                    # Extract domain terms
                    self.domain_analyzer.extract_domain_terms(doc)

                    # Collect schema metadata
                    self.metadata_collector.collect_schema_metadata(doc, metadata, subgraph)

                    # Enhance document structure
                    enhanced_doc = self.document_enhancer.enhance_yaml_structure(doc)
                    enhanced_documents.append(enhanced_doc)

                    # Update metadata with descriptions
                    self.metadata_collector.update_metadata_with_descriptions(enhanced_doc, metadata)
                else:
                    enhanced_documents.append(None)

            return rel_path, enhanced_documents, metadata

        except Exception as e:
            logger.error(f"Error processing file in first pass {file_path}: {e}")
            return None

    def _build_comprehensive_relationship_map(self) -> Dict[str, Any]:
        """Build comprehensive relationship map from all collected metadata."""
        logger.info("Building comprehensive relationship map...")

        if not self.schema_metadata:
            logger.warning("No schema metadata available for relationship mapping")
            return {'entities': {}, 'relationships': [], 'generated_yaml': []}

        # Build relationship map using all collected metadata
        relationship_map = self.relationship_mapper.build_relationship_map(self.schema_metadata)

        # Store generated relationships for later writing
        self.generated_relationships = relationship_map.get('generated_yaml', [])

        stats = relationship_map.get('statistics', {})
        logger.info(f"Relationship map built: {stats.get('total_entities', 0)} entities, "
                    f"{stats.get('total_relationships', 0)} relationships, "
                    f"{len(self.generated_relationships)} YAML definitions generated")

        return relationship_map

    def _perform_second_pass(self, relationship_map: Dict[str, Any],
                             input_dir: str, output_dir: str) -> None:
        """Perform second pass: add relationships and save enhanced files."""
        logger.info("Starting second pass: adding relationships and saving files")

        for rel_path, enhanced_docs in self.enhanced_documents_by_file.items():
            try:
                # Extract subgraph from path
                from ..utils.path_utils import extract_subgraph_from_path
                full_path = os.path.join(input_dir, rel_path)
                subgraph = extract_subgraph_from_path(full_path)

                # Add relationship information to descriptions
                final_docs = self.document_enhancer.enhance_with_relationships(
                    enhanced_docs, relationship_map, subgraph
                )

                # Prepare output path
                output_path = os.path.join(output_dir, rel_path)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # Save enhanced documents
                save_yaml_documents(final_docs, output_path)

                logger.debug(f"Second pass completed and saved: {output_path}")

            except Exception as e:
                logger.error(f"Error in second pass for {rel_path}: {e}")
                logger.debug("Full traceback:", exc_info=True)

        logger.info("Second pass complete: all files enhanced with relationships")

    def _write_relationship_definitions(self, output_dir: str) -> None:
        """Write generated relationship definitions to appropriate files."""
        if not self.generated_relationships:
            logger.info("No relationship definitions to write")
            return

        logger.info(f"Writing {len(self.generated_relationships)} relationship definitions...")

        # Group relationships by target file
        relationships_by_file = defaultdict(list)
        for rel_info in self.generated_relationships:
            file_path = rel_info.get('target_file_path')
            if file_path:
                relationships_by_file[file_path].append(rel_info['relationship_definition'])

        # Write relationships to each file
        written_count = 0
        for file_rel_path, relationships in relationships_by_file.items():
            try:
                output_path = os.path.join(output_dir, file_rel_path)

                # Load existing documents
                existing_documents = []
                if os.path.exists(output_path):
                    from ..utils.yaml_utils import load_yaml_documents
                    try:
                        existing_documents = load_yaml_documents(output_path)
                    except Exception as e:
                        logger.error(f"Could not read existing file {output_path}: {e}")
                        existing_documents = []

                # Filter out None documents
                final_documents = [doc for doc in existing_documents if doc is not None]

                # Deduplicate and append new relationships
                unique_relationships = self._deduplicate_relationships_for_file(
                    relationships, final_documents
                )

                if unique_relationships:
                    final_documents.extend(unique_relationships)

                    # Save updated documents
                    save_yaml_documents(final_documents, output_path)
                    written_count += len(unique_relationships)

                    logger.debug(f"Appended {len(unique_relationships)} relationships to {output_path}")

            except Exception as e:
                logger.error(f"Error writing relationships to {file_rel_path}: {e}")

        logger.info(f"Successfully wrote {written_count} relationship definitions")

    def _deduplicate_relationships_for_file(self, new_relationships: List[Dict],
                                            existing_documents: List[Dict]) -> List[Dict]:
        """Deduplicate relationships against existing documents in the file."""
        unique_relationships = []

        # Extract existing relationship signatures from current file
        existing_signatures = set()
        for doc in existing_documents:
            if isinstance(doc, dict) and doc.get('kind') == 'Relationship':
                signature = self._extract_relationship_signature(doc)
                if signature:
                    existing_signatures.add(signature)

        # Check each new relationship for duplicates
        for rel_def in new_relationships:
            signature = self._extract_relationship_signature(rel_def)

            if signature and signature not in existing_signatures:
                unique_relationships.append(rel_def)
                existing_signatures.add(signature)
            elif not signature:
                # Include relationships we can't create signatures for
                logger.warning(f"Could not create signature for relationship, including anyway")
                unique_relationships.append(rel_def)
            else:
                logger.debug(f"Skipping duplicate relationship: {rel_def.get('definition', {}).get('name', 'unnamed')}")

        return unique_relationships

    @staticmethod
    def _extract_relationship_signature(rel_def: Dict) -> Optional[Tuple]:
        """Extract unique signature from relationship definition."""
        try:
            definition = rel_def.get('definition', {})
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
            logger.warning(f"Could not create relationship signature: {e}")
            return None

    @staticmethod
    def _copy_excluded_files(excluded_files: List[str],
                             input_dir: str, output_dir: str) -> None:
        """Copy excluded files to output directory without processing."""
        if not excluded_files:
            return

        logger.info(f"Copying {len(excluded_files)} excluded files...")

        for file_path in excluded_files:
            try:
                rel_path = os.path.relpath(file_path, input_dir)
                output_path = os.path.join(output_dir, rel_path)

                # Skip if input and output are the same
                if os.path.abspath(file_path) == os.path.abspath(output_path):
                    logger.debug(f"Skipping copy (same path): {file_path}")
                    continue

                # Create output directory and copy file
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                shutil.copy2(file_path, output_path)

                logger.debug(f"Copied excluded file: {output_path}")

            except Exception as e:
                logger.error(f"Error copying excluded file {file_path}: {e}")

    @staticmethod
    def _create_empty_result(input_dir: str, output_dir: str) -> Dict[str, Any]:
        """Create result dictionary for empty processing."""
        return {
            'success': True,
            'input_dir': input_dir,
            'output_dir': output_dir,
            'files_processed': 0,
            'files_excluded': 0,
            'entities_found': 0,
            'relationships_generated': 0,
            'warning': 'No files found to process'
        }

    def _calculate_final_statistics(self, input_dir: str, output_dir: str,
                                    processed_files: List[str],
                                    excluded_files: List[str]) -> Dict[str, Any]:
        """Calculate comprehensive final statistics."""
        # Basic file statistics
        stats = {
            'success': True,
            'input_dir': input_dir,
            'output_dir': output_dir,
            'files_processed': len(processed_files),
            'files_excluded': len(excluded_files),
            'total_files_found': len(processed_files) + len(excluded_files)
        }

        # Entity statistics
        total_entities = 0
        entities_by_kind = defaultdict(int)
        entities_by_subgraph = defaultdict(int)

        for metadata in self.schema_metadata.values():
            entities = metadata.get('entities', [])
            total_entities += len(entities)

            for entity in entities:
                kind = entity.get('kind', 'Unknown')
                subgraph = entity.get('subgraph', 'None')
                entities_by_kind[kind] += 1
                entities_by_subgraph[subgraph] += 1

        stats.update({
            'entities_found': total_entities,
            'entities_by_kind': dict(entities_by_kind),
            'entities_by_subgraph': dict(entities_by_subgraph)
        })

        # Relationship statistics
        stats.update({
            'relationships_generated': len(self.generated_relationships),
            'relationship_files_modified': len(set(
                rel.get('target_file_path') for rel in self.generated_relationships
                if rel.get('target_file_path')
            ))
        })

        # Domain analysis statistics
        if hasattr(self.domain_analyzer, 'get_domain_summary'):
            stats['domain_analysis'] = self.domain_analyzer.get_domain_summary()

        # File statistics
        if processed_files:
            file_stats = get_file_stats(processed_files)
            stats['file_statistics'] = file_stats

        # Processing performance
        stats['processing_summary'] = {
            'files_with_entities': len([m for m in self.schema_metadata.values() if m.get('entities')]),
            'files_with_relationships': len([
                rel.get('target_file_path') for rel in self.generated_relationships
            ]),
            'cross_subgraph_relationships': len([
                rel for rel in self.generated_relationships
                if 'subgraph' in rel.get('relationship_definition', {}).get('definition', {}).get('target', {}).get(
                    'model', {})
            ])
        }

        return stats

    def get_processing_state(self) -> Dict[str, Any]:
        """
        Get current processing state for monitoring/debugging.

        Returns:
            Dictionary with current processing state information
        """
        return {
            'schema_metadata_files': len(self.schema_metadata),
            'enhanced_documents_files': len(self.enhanced_documents_by_file),
            'generated_relationships': len(self.generated_relationships),
            'total_entities': sum(len(meta.get('entities', [])) for meta in self.schema_metadata.values()),
            'domain_terms_collected': len(self.domain_analyzer.domain_specific_terms) if hasattr(self.domain_analyzer,
                                                                                                 'domain_specific_terms') else 0
        }


def create_directory_processor(metadata_collector: MetadataCollector,
                               domain_analyzer: DomainAnalyzer,
                               relationship_detector: RelationshipDetector,
                               relationship_mapper: RelationshipMapper,
                               relationship_generator: RelationshipGenerator,
                               document_enhancer: DocumentEnhancer) -> DirectoryProcessor:
    """
    Create a DirectoryProcessor instance with all required components.

    Args:
        metadata_collector: Schema metadata collector
        domain_analyzer: Domain analysis component
        relationship_detector: Relationship detection component
        relationship_mapper: Relationship mapping component
        relationship_generator: Relationship generation component
        document_enhancer: Document enhancement component

    Returns:
        Configured DirectoryProcessor instance
    """
    return DirectoryProcessor(
        metadata_collector, domain_analyzer, relationship_detector,
        relationship_mapper, relationship_generator, document_enhancer
    )
