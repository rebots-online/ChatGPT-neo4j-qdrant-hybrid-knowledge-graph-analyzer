from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import uuid

@dataclass
class Message:
    id: str
    content: str
    role: str  # 'user' or 'assistant'
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=lambda: datetime.now())
    metadata: Dict = field(default_factory=dict)
    embedding_id: Optional[str] = None  # Reference to Qdrant vector
    
    def to_vector_payload(self) -> Dict:
        """Convert message to a format suitable for vector storage"""
        return {
            "id": self.id,
            "content": self.content,
            "role": self.role,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }

@dataclass
class ConversationThread:
    id: str
    title: Optional[str]
    messages: Dict[str, Message]  # message_id -> Message
    root_id: str
    metadata: Dict = field(default_factory=dict)
    
    @classmethod
    def from_export_mapping(cls, conversation_data: Dict) -> 'ConversationThread':
        """Create a ConversationThread from native ChatGPT export format"""
        messages = {}
        mapping = conversation_data['mapping']
        
        # First pass: Create Message objects
        for node_id, node in mapping.items():
            msg = node['message']
            if msg is None:
                continue
                
            content = ""
            for part in msg['content'].get('parts', []):
                if isinstance(part, str):
                    content += part
            
            messages[node_id] = Message(
                id=node_id,
                content=content,
                role=msg['author']['role'],
                children_ids=node.get('children', [])
            )
        
        # Second pass: Set parent IDs
        for node_id, msg in messages.items():
            for child_id in msg.children_ids:
                if child_id in messages:
                    messages[child_id].parent_id = node_id
        
        return cls(
            id=str(uuid.uuid4()),
            title=conversation_data.get('title'),
            messages=messages,
            root_id=conversation_data.get('root', next(iter(mapping))),
            metadata={
                "create_time": conversation_data.get('create_time'),
                "update_time": conversation_data.get('update_time'),
                "moderation_results": conversation_data.get('moderation_results', [])
            }
        )
    
    def traverse_messages(self) -> List[Message]:
        """Traverse messages in chronological order"""
        result = []
        queue = [self.root_id]
        
        while queue:
            msg_id = queue.pop(0)
            if msg_id in self.messages:
                msg = self.messages[msg_id]
                result.append(msg)
                queue.extend(msg.children_ids)
                
        return result

    def extract_semantic_units(self) -> List[Dict]:
        """Extract semantic units for vector embedding"""
        units = []
        for msg in self.traverse_messages():
            # Basic semantic unit: entire message
            units.append({
                "text": msg.content,
                "metadata": {
                    "message_id": msg.id,
                    "conversation_id": self.id,
                    "role": msg.role,
                    "type": "message",
                    "context": {
                        "title": self.title,
                        "parent_id": msg.parent_id
                    }
                }
            })
            
            # TODO: Add more granular semantic units:
            # - Sentence-level splits
            # - Paragraph-level splits
            # - Code blocks
            # - Question-answer pairs
            
        return units