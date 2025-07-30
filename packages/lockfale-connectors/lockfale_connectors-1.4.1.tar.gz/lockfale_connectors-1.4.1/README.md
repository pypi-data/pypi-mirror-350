# Cyberpartner Connectors

## Connectors Package

This repository contains a collection of connectors for Kafka, MQTT, and PostgreSQL that can be used across any microservice
in relation to Cyberpartner applications.

There is specific enrichment and schema validation for Cyberpartner routing with Kafka.

The MQTT and PGSQL connectors are fairly generic and can be used in any project, but the kafka wrapper is not.

### Connectors Included

- **Kafka**: Kafka producer and consumer connectors
- **MQTT**: MQTT client, publisher, and subscriber connectors
- **PostgreSQL**: PostgreSQL database connector

### Installation from AWS CodeArtifact

```bash
# Configure poetry to use AWS CodeArtifact
export CODEARTIFACT_AUTH_TOKEN=$(aws codeartifact get-authorization-token \
  --domain YOUR_DOMAIN \
  --domain-owner YOUR_ACCOUNT_ID \
  --query authorizationToken \
  --output text)

export CODEARTIFACT_REPO_URL=$(aws codeartifact get-repository-endpoint \
  --domain YOUR_DOMAIN \
  --domain-owner YOUR_ACCOUNT_ID \
  --repository YOUR_REPO \
  --format pypi \
  --query repositoryEndpoint \
  --output text)

# Configure Poetry
poetry config repositories.codeartifact $CODEARTIFACT_REPO_URL
poetry config http-basic.codeartifact aws $CODEARTIFACT_AUTH_TOKEN

# Add the package to your project
poetry add lockfaleconnectors
```

# Publish to PyPi
```bash
poetry build
poetry config pypi-token.pypi <your-token-here>
poetry publish --build


```

# TODO
 - Update required / expected environment variables
 - Use confluent-kafka
 - Update Psycopg to v3.3