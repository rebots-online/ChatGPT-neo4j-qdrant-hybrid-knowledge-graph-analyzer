# Architecture Documentation

## System Overview

```mermaid
graph TB
    subgraph "Data Sources"
        ChatGPT[ChatGPT Exports] --> Parser[Export Parser]
        Parser --> Processor[Data Processor]
    end
    
    subgraph "Storage Layer"
        Processor --> VectorDB[Qdrant Vector DB]
        Processor --> GraphDB[Neo4j Graph DB]
    end
    
    subgraph "Analysis Layer"
        VectorDB --> Semantic[Semantic Search]
        GraphDB --> Knowledge[Knowledge Graph]
        Semantic --> Hybrid[Hybrid Analysis]
        Knowledge --> Hybrid
    end
    
    subgraph "Interface Layer"
        Hybrid --> MCP[MCP Server]
        MCP --> Client[Client Applications]
    end
```

## Component Architecture

```mermaid
classDiagram
    class ChatExport {
        +List~Conversation~ conversations
        +Dict metadata
        +parse()
        +validate()
    }
    
    class Conversation {
        +String id
        +String title
        +List~Message~ messages
        +DateTime createTime
        +Dict metadata
        +buildThreads()
        +extractConcepts()
    }
    
    class Message {
        +String id
        +String content
        +String role
        +DateTime timestamp
        +List~String~ vectorIds
        +List~String~ conceptIds
        +generateEmbeddings()
        +analyzeContent()
    }
    
    class KnowledgeGraph {
        +createNode()
        +createRelationship()
        +findPatterns()
        +analyzeStructure()
    }
    
    class VectorStore {
        +storeEmbedding()
        +searchSimilar()
        +batchProcess()
        +updateMetadata()
    }
    
    class HybridAnalyzer {
        +analyzeSemantics()
        +findRelationships()
        +generateMetrics()
        +extractInsights()
    }
    
    ChatExport --> Conversation
    Conversation --> Message
    Message --> VectorStore
    Message --> KnowledgeGraph
    VectorStore --> HybridAnalyzer
    KnowledgeGraph --> HybridAnalyzer
```

## Data Flow

```mermaid
sequenceDiagram
    participant User
    participant Parser
    participant Processor
    participant Qdrant
    participant Neo4j
    participant MCP
    
    User->>Parser: Import ChatGPT Export
    Parser->>Processor: Parsed Conversations
    
    par Vector Processing
        Processor->>Qdrant: Store Embeddings
    and Graph Processing
        Processor->>Neo4j: Create Graph Structure
    end
    
    Processor->>MCP: Analysis Ready
    
    loop Analysis Requests
        User->>MCP: Query/Analysis Request
        MCP->>Qdrant: Vector Search
        MCP->>Neo4j: Graph Query
        MCP->>User: Combined Results
    end
```

## Storage Schema

### Vector Storage (Qdrant)

```mermaid
erDiagram
    VECTOR_COLLECTION {
        string id PK
        vector embedding
        string message_id FK
        string conversation_id FK
        timestamp created_at
        json metadata
    }
    
    PAYLOAD {
        string message_id PK
        string content
        string role
        timestamp timestamp
        json context
    }
```

### Graph Storage (Neo4j)

```mermaid
erDiagram
    CONVERSATION ||--o{ MESSAGE : CONTAINS
    MESSAGE ||--o{ CONCEPT : MENTIONS
    CONCEPT ||--o{ CONCEPT : RELATED_TO
    MESSAGE ||--o{ MESSAGE : REPLIES_TO
    
    CONVERSATION {
        string id PK
        string title
        timestamp create_time
        timestamp update_time
        json metadata
    }
    
    MESSAGE {
        string id PK
        string content
        string role
        string vector_id FK
        timestamp timestamp
        json metadata
    }
    
    CONCEPT {
        string id PK
        string name
        float relevance
        int frequency
        timestamp first_seen
        timestamp last_seen
        json metadata
    }
```

## Processing Pipeline

```mermaid
graph LR
    subgraph "Import Phase"
        Import[Import File] --> Validate[Validate Format]
        Validate --> Parse[Parse Content]
        Parse --> Extract[Extract Messages]
    end
    
    subgraph "Processing Phase"
        Extract --> Embed[Generate Embeddings]
        Extract --> Graph[Create Graph]
        Embed --> Store[Store Vectors]
        Graph --> Analyze[Analyze Structure]
    end
    
    subgraph "Analysis Phase"
        Store --> Search[Semantic Search]
        Analyze --> Pattern[Pattern Recognition]
        Search --> Combine[Hybrid Analysis]
        Pattern --> Combine
    end
```

## Integration Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        Claude[Claude Desktop]
        Custom[Custom Apps]
    end
    
    subgraph "MCP Layer"
        Server[MCP Server]
        Tools[Analysis Tools]
    end
    
    subgraph "Storage Layer"
        Qdrant[Qdrant]
        Neo4j[Neo4j]
    end
    
    Claude --> Server
    Custom --> Server
    Server --> Tools
    Tools --> Qdrant
    Tools --> Neo4j
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Application Tier"
        MCP[MCP Server]
        API[Analysis API]
    end
    
    subgraph "Database Tier"
        Qdrant[Qdrant Vector DB]
        Neo4j[Neo4j Graph DB]
    end
    
    subgraph "Client Tier"
        Claude[Claude Desktop]
        Web[Web Interface]
        CLI[Command Line]
    end
    
    Claude --> MCP
    Web --> API
    CLI --> API
    MCP --> API
    API --> Qdrant
    API --> Neo4j