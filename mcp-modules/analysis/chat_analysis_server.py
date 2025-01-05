#!/usr/bin/env python3
from typing import Dict, Any, List
import asyncio
import json
from pathlib import Path

from modelcontextprotocol import Server, StdioServerTransport
from modelcontextprotocol.types import (
    CallToolRequestSchema,
    ErrorCode,
    ListToolsRequestSchema,
    McpError,
)

from ...core.processors.conversation_processor import ConversationProcessor
from ...core.models.conversation import ConversationThread
from ...importers.common.base import OpenAIExportImporter

class ChatAnalysisServer:
    """MCP server for chat analysis operations"""
    
    def __init__(self):
        self.server = Server(
            {
                "name": "chat-analysis-server",
                "version": "0.1.0",
            },
            {
                "capabilities": {
                    "tools": {},
                }
            }
        )
        
        # Initialize processor with clients
        self.processor = ConversationProcessor(
            qdrant_client=None,  # TODO: Initialize from config
            neo4j_client=None    # TODO: Initialize from config
        )
        
        self._setup_tools()
    
    def _setup_tools(self):
        """Set up MCP tools"""
        self.server.set_request_handler(ListToolsRequestSchema, self._handle_list_tools)
        self.server.set_request_handler(CallToolRequestSchema, self._handle_call_tool)
    
    async def _handle_list_tools(self, _):
        """Handle tool listing request"""
        return {
            "tools": [
                {
                    "name": "import_conversations",
                    "description": "Import and analyze chat conversations",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "source_path": {
                                "type": "string",
                                "description": "Path to the chat export file"
                            },
                            "format": {
                                "type": "string",
                                "enum": ["openai_native", "html", "markdown", "json"],
                                "description": "Format of the chat export"
                            }
                        },
                        "required": ["source_path", "format"]
                    }
                },
                {
                    "name": "semantic_search",
                    "description": "Search conversations by semantic similarity",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query text"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of results",
                                "default": 10
                            },
                            "filters": {
                                "type": "object",
                                "description": "Optional filters for search results"
                            }
                        },
                        "required": ["query"]
                    }
                },
                {
                    "name": "analyze_metrics",
                    "description": "Analyze conversation metrics",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "conversation_id": {
                                "type": "string",
                                "description": "ID of the conversation to analyze"
                            },
                            "metrics": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "enum": [
                                        "message_frequency",
                                        "response_times",
                                        "topic_diversity",
                                        "conversation_depth",
                                        "interaction_patterns"
                                    ]
                                },
                                "description": "Metrics to analyze"
                            }
                        },
                        "required": ["conversation_id"]
                    }
                },
                {
                    "name": "extract_concepts",
                    "description": "Extract and analyze concepts from conversations",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "conversation_id": {
                                "type": "string",
                                "description": "ID of the conversation to analyze"
                            },
                            "min_relevance": {
                                "type": "number",
                                "description": "Minimum relevance score for concepts",
                                "minimum": 0,
                                "maximum": 1,
                                "default": 0.5
                            }
                        },
                        "required": ["conversation_id"]
                    }
                }
            ]
        }
    
    async def _handle_call_tool(self, request):
        """Handle tool execution request"""
        try:
            if request.params.name == "import_conversations":
                return await self._import_conversations(request.params.arguments)
            elif request.params.name == "semantic_search":
                return await self._semantic_search(request.params.arguments)
            elif request.params.name == "analyze_metrics":
                return await self._analyze_metrics(request.params.arguments)
            elif request.params.name == "extract_concepts":
                return await self._extract_concepts(request.params.arguments)
            else:
                raise McpError(ErrorCode.MethodNotFound, f"Unknown tool: {request.params.name}")
        except Exception as e:
            raise McpError(ErrorCode.InternalError, str(e))
    
    async def _import_conversations(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Import and process conversations"""
        source_path = Path(args["source_path"])
        format_type = args["format"]
        
        if format_type == "openai_native":
            importer = OpenAIExportImporter()
        else:
            raise McpError(ErrorCode.InvalidParams, f"Unsupported format: {format_type}")
        
        stats = await self.processor.process_import(importer, source_path)
        return {"content": [{"type": "text", "text": json.dumps(stats, indent=2)}]}
    
    async def _semantic_search(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Perform semantic search"""
        # TODO: Implement semantic search using Qdrant
        pass
    
    async def _analyze_metrics(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze conversation metrics"""
        # TODO: Implement metric analysis
        pass
    
    async def _extract_concepts(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and analyze concepts"""
        # TODO: Implement concept extraction
        pass
    
    async def run(self):
        """Run the MCP server"""
        transport = StdioServerTransport()
        await self.server.connect(transport)
        print("Chat Analysis MCP server running on stdio", file=sys.stderr)

if __name__ == "__main__":
    import sys
    
    server = ChatAnalysisServer()
    asyncio.run(server.run())