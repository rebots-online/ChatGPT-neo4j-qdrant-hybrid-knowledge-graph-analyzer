#!/bin/bash
set -e

# Default values
NEO4J_VERSION="5.15.0"
NEO4J_HOME="/opt/neo4j"
DEFAULT_PASSWORD="changeme"  # Will prompt to change on first login

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --password)
            NEO4J_PASSWORD="$2"
            shift
            shift
            ;;
        --home)
            NEO4J_HOME="$2"
            shift
            shift
            ;;
        --version)
            NEO4J_VERSION="$2"
            shift
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --password PASSWORD    Set initial Neo4j password"
            echo "  --home PATH           Set Neo4j home directory"
            echo "  --version VERSION     Set Neo4j version"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root"
    exit 1
fi

echo "Installing Neo4j ${NEO4J_VERSION}..."

# Install Java
echo "Installing Java..."
apt-get update
apt-get install -y openjdk-17-jre-headless

# Install wget if not present
apt-get install -y wget

# Download and install Neo4j
echo "Downloading Neo4j..."
wget -O neo4j.deb "https://neo4j.com/artifact.php?name=neo4j-community_${NEO4J_VERSION}_all.deb"
dpkg -i neo4j.deb || true
apt-get install -f -y
rm neo4j.deb

# Configure Neo4j
echo "Configuring Neo4j..."
cat > /etc/neo4j/neo4j.conf << EOL
# Default values for the low-level graph engine
dbms.default_database=neo4j
dbms.security.auth_enabled=true
dbms.memory.heap.initial_size=1G
dbms.memory.heap.max_size=2G
dbms.memory.pagecache.size=512M

# Network connector configuration
dbms.connector.bolt.enabled=true
dbms.connector.bolt.listen_address=0.0.0.0:7687
dbms.connector.http.enabled=true
dbms.connector.http.listen_address=0.0.0.0:7474
dbms.connector.https.enabled=false

# Allow any client to connect (configure firewall rules separately)
dbms.default_listen_address=0.0.0.0
EOL

# Create data directories
mkdir -p "${NEO4J_HOME}/data"
mkdir -p "${NEO4J_HOME}/logs"
mkdir -p "${NEO4J_HOME}/import"
mkdir -p "${NEO4J_HOME}/plugins"

# Set correct permissions
chown -R neo4j:neo4j /etc/neo4j
chown -R neo4j:neo4j "${NEO4J_HOME}"

# Start Neo4j
systemctl enable neo4j
systemctl start neo4j

# Wait for Neo4j to start
echo "Waiting for Neo4j to start..."
sleep 30

# Set initial password
echo "Setting initial password..."
neo4j-admin dbms set-initial-password "${NEO4J_PASSWORD:-$DEFAULT_PASSWORD}"

echo "Neo4j installation complete!"
echo "You can now connect to Neo4j at:"
echo "Browser interface: http://localhost:7474"
echo "Bolt connection: bolt://localhost:7687"
echo "Username: neo4j"
if [ -z "${NEO4J_PASSWORD}" ]; then
    echo "Password: ${DEFAULT_PASSWORD} (please change this on first login)"
else
    echo "Password: [as specified]"
fi
echo ""
echo "Important security notes:"
echo "1. Configure your firewall to restrict access to Neo4j ports"
echo "2. Change the default password immediately"
echo "3. Consider enabling HTTPS for production use"
echo ""
echo "To check logs:"
echo "journalctl -u neo4j"
echo ""
echo "To stop Neo4j:"
echo "systemctl stop neo4j"
echo ""
echo "To uninstall Neo4j:"
echo "apt-get remove neo4j"
echo "rm -rf ${NEO4J_HOME}"