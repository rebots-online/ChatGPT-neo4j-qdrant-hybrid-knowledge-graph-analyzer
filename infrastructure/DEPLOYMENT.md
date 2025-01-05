# Deployment Guide

This guide covers different deployment options for setting up the Chat Knowledge Graph Analyzer infrastructure.

## Option 1: Docker Compose (Recommended)

The simplest way to deploy the required infrastructure is using Docker Compose.

### Prerequisites
- Docker Engine 20.10+
- Docker Compose V2
- 4GB RAM minimum
- 10GB disk space

### Steps

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Edit `.env` with your configuration:
```env
NEO4J_PASSWORD=your_secure_password
QDRANT_API_KEY=optional_api_key
```

3. Start the services:
```bash
cd infrastructure/docker
docker compose up -d
```

4. Verify the services:
```bash
docker compose ps
```

Services will be available at:
- Neo4j Browser: http://localhost:7474
- Neo4j Bolt: bolt://localhost:7687
- Qdrant API: http://localhost:6333

### Volume Management

Data is persisted in Docker volumes:
```bash
# List volumes
docker volume ls | grep chat_analyzer

# Backup volumes
docker run --rm -v chat-analyzer-neo4j_data:/data -v $(pwd):/backup alpine tar czf /backup/neo4j_data.tar.gz /data
docker run --rm -v chat-analyzer-qdrant_data:/data -v $(pwd):/backup alpine tar czf /backup/qdrant_data.tar.gz /data
```

## Option 2: Direct Installation

For production environments or when you need more control, you can install services directly.

### Neo4j Installation

1. Using the deployment script:
```bash
cd infrastructure/scripts
sudo ./deploy_neo4j.sh --password your_secure_password
```

Script options:
- `--password`: Set initial Neo4j password
- `--home`: Set Neo4j home directory
- `--version`: Set Neo4j version

2. Manual configuration:
- Edit `/etc/neo4j/neo4j.conf`
- Configure memory settings
- Set up authentication
- Configure backup strategy

### Qdrant Installation

1. Using official packages:
```bash
curl -L https://github.com/qdrant/qdrant/releases/latest/download/qdrant.tar.gz | tar -xz
cd qdrant
./qdrant
```

2. Configuration:
- Edit `config/production.yaml`
- Set up authentication if needed
- Configure storage paths
- Set resource limits

## Security Considerations

### Network Security
1. Configure firewalls to restrict access:
```bash
# UFW example
ufw allow from trusted_ip to any port 7474 proto tcp  # Neo4j HTTP
ufw allow from trusted_ip to any port 7687 proto tcp  # Neo4j Bolt
ufw allow from trusted_ip to any port 6333 proto tcp  # Qdrant API
```

2. Enable TLS:
- For Neo4j: Configure HTTPS in neo4j.conf
- For Qdrant: Set up reverse proxy with TLS

### Authentication
1. Change default passwords immediately
2. Use strong passwords
3. Set up API keys for Qdrant
4. Consider using client certificates

### Monitoring

1. Set up health checks:
```bash
# Neo4j
curl -u neo4j:password http://localhost:7474/browser/

# Qdrant
curl http://localhost:6333/healthz
```

2. Monitor resources:
```bash
# Check logs
docker compose logs -f

# Monitor resource usage
docker stats
```

## Backup Strategy

### Automated Backups

1. Create a backup script:
```bash
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d)

# Neo4j backup
neo4j-admin dump --database=neo4j \
  --to=$BACKUP_DIR/neo4j_$DATE.dump

# Qdrant backup
curl -X POST http://localhost:6333/snapshots
```

2. Schedule with cron:
```bash
0 2 * * * /path/to/backup_script.sh
```

### Restore Process

1. Neo4j restore:
```bash
neo4j-admin load --from=/path/to/backup.dump --database=neo4j
```

2. Qdrant restore:
```bash
curl -X PUT http://localhost:6333/snapshots/{snapshot_name}
```

## Scaling Considerations

### Vertical Scaling
- Adjust memory settings in configuration files
- Increase CPU allocation
- Expand disk space

### Horizontal Scaling
- Set up Neo4j clustering
- Configure Qdrant replicas
- Use load balancers

## Troubleshooting

### Common Issues

1. Memory problems:
```bash
# Check memory usage
free -h
docker stats
```

2. Connection issues:
```bash
# Test connectivity
nc -zv localhost 7687
nc -zv localhost 6333
```

3. Permission problems:
```bash
# Check volume permissions
ls -l /var/lib/docker/volumes/
```

### Logs

```bash
# Docker logs
docker compose logs -f neo4j
docker compose logs -f qdrant

# Direct installation logs
journalctl -u neo4j
tail -f /var/log/qdrant/qdrant.log
```

## Maintenance

### Regular Tasks

1. Update services:
```bash
# Docker
docker compose pull
docker compose up -d

# Direct installation
apt update
apt upgrade neo4j
```

2. Clean up:
```bash
# Remove old logs
find /var/log/neo4j -name "*.log" -mtime +30 -delete

# Clean Docker
docker system prune
```

3. Check for updates:
```bash
# Check versions
curl -s https://api.github.com/repos/neo4j/neo4j/releases/latest
curl -s https://api.github.com/repos/qdrant/qdrant/releases/latest
```

## Support

- [Neo4j Documentation](https://neo4j.com/docs/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Project Issues](https://github.com/rebots-online/ChatGPT-neo4j-qdrant-hybrid-knowledge-graph-analyzer/issues)