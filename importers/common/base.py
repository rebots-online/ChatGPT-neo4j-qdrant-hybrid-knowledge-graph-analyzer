from abc import ABC, abstractmethod
from typing import List, Dict, Generator, Any
from pathlib import Path
import json
from zipfile import ZipFile
import tempfile

class ChatImporter(ABC):
    """Base class for chat data importers"""
    
    @abstractmethod
    def validate_source(self, source_path: Path) -> bool:
        """
        Validate if the source can be processed by this importer
        
        Args:
            source_path: Path to the source file/directory
            
        Returns:
            bool: True if the source is valid for this importer
        """
        pass
    
    @abstractmethod
    def extract_conversations(self, source_path: Path) -> Generator[Dict[str, Any], None, None]:
        """
        Extract conversation data from the source
        
        Args:
            source_path: Path to the source file/directory
            
        Yields:
            Dict: Raw conversation data in a format suitable for ConversationThread
        """
        pass
    
    @abstractmethod
    def extract_metadata(self, source_path: Path) -> Dict[str, Any]:
        """
        Extract global metadata from the source
        
        Args:
            source_path: Path to the source file/directory
            
        Returns:
            Dict: Global metadata about the export
        """
        pass

class OpenAIExportImporter(ChatImporter):
    """Importer for native OpenAI ChatGPT exports"""
    
    def validate_source(self, source_path: Path) -> bool:
        """Check if the file is a valid OpenAI export zip"""
        if not source_path.is_file() or source_path.suffix != '.zip':
            return False
            
        try:
            with ZipFile(source_path, 'r') as zip_ref:
                return 'conversations.json' in zip_ref.namelist()
        except:
            return False
    
    def extract_conversations(self, source_path: Path) -> Generator[Dict[str, Any], None, None]:
        """Extract conversations from OpenAI export zip"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Extract zip contents
            with ZipFile(source_path, 'r') as zip_ref:
                zip_ref.extractall(tmp_dir)
            
            # Read conversations.json
            conversations_path = Path(tmp_dir) / 'conversations.json'
            with open(conversations_path) as f:
                conversations = json.load(f)
            
            # Yield each conversation
            for conversation in conversations:
                if 'mapping' not in conversation:
                    continue
                    
                # Clean and validate conversation data
                cleaned = {
                    'mapping': conversation['mapping'],
                    'title': conversation.get('title', 'Untitled'),
                    'create_time': conversation.get('create_time'),
                    'update_time': conversation.get('update_time'),
                    'root': conversation.get('root'),
                    'moderation_results': conversation.get('moderation_results', [])
                }
                
                yield cleaned
    
    def extract_metadata(self, source_path: Path) -> Dict[str, Any]:
        """Extract global metadata from the export"""
        metadata = {
            'source_type': 'openai_export',
            'import_time': None,
            'conversation_count': 0,
            'date_range': {
                'start': None,
                'end': None
            }
        }
        
        # Process zip to gather metadata
        with tempfile.TemporaryDirectory() as tmp_dir:
            with ZipFile(source_path, 'r') as zip_ref:
                zip_ref.extractall(tmp_dir)
                
            conversations_path = Path(tmp_dir) / 'conversations.json'
            with open(conversations_path) as f:
                conversations = json.load(f)
            
            metadata['conversation_count'] = len(conversations)
            
            # Find date range
            create_times = []
            for conv in conversations:
                if conv.get('create_time'):
                    create_times.append(conv['create_time'])
                    
            if create_times:
                metadata['date_range']['start'] = min(create_times)
                metadata['date_range']['end'] = max(create_times)
        
        return metadata