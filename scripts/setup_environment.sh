#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up Chat Knowledge Grapher environment...${NC}"

# Create necessary directories
echo "Creating directory structure..."
mkdir -p {data,logs,cache,exports}

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt
pip install -e .

# Copy and customize configuration
echo "Setting up configuration..."
if [ ! -f config.yml ]; then
    cp config.template.yml config.yml
    echo -e "${YELLOW}Please edit config.yml with your specific settings${NC}"
fi

# Check Docker availability
echo "Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker not found. Please install Docker and Docker Compose.${NC}"
    exit 1
fi

# Check if services are accessible
echo "Checking Neo4j connection..."
if nc -z 192.168.0.157 7687 2>/dev/null; then
    echo "Neo4j is accessible"
else
    echo -e "${YELLOW}Neo4j is not accessible at 192.168.0.157:7687${NC}"
    echo "You may need to:"
    echo "1. Deploy Neo4j using infrastructure/scripts/deploy_neo4j.sh"
    echo "2. Update config.yml with correct Neo4j settings"
fi

echo "Checking Qdrant connection..."
if nc -z 192.168.0.157 6333 2>/dev/null; then
    echo "Qdrant is accessible"
else
    echo -e "${YELLOW}Qdrant is not accessible at 192.168.0.157:6333${NC}"
    echo "Please ensure Qdrant is running and update config.yml if needed"
fi

# Download spaCy model for NLP tasks
echo "Downloading spaCy language model..."
python -m spacy download en_core_web_sm

# Set up pre-commit hooks
echo "Setting up git hooks..."
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
set -e

# Run tests
python -m pytest tests/

# Check code formatting
black --check .
flake8 .
EOF
chmod +x .git/hooks/pre-commit

echo -e "${GREEN}Environment setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Edit config.yml with your specific settings"
echo "2. Deploy Neo4j if not already running:"
echo "   cd infrastructure/scripts && ./deploy_neo4j.sh"
echo "3. Start the MCP server:"
echo "   python -m mcp_modules.analysis.chat_analysis_server"
echo ""
echo "For development:"
echo "- Run tests: python -m pytest tests/"
echo "- Format code: black ."
echo "- Check style: flake8"