# ERC20 Token Indexer with AI Integration

Index Ethereum ERC20 tokens and interact with the data using natural language.

## What It Does

- Tracks ERC20 token transfers on Ethereum
- Lets AI agents add new tokens to track
- Enables querying transfers by address
- Everything works through simple language commands

## Quick Start

### Requirements

- Python 3.12
- Ethereum node access (Alchemy API key)

### Install

```shell
curl -Lsf https://dipdup.io/install.py | python
export NODE_API_KEY=your_alchemy_api_key
```

### Run

```shell
dipdup -e .env -С sqlite run
dipdup -e .env -C sqlite mcp run
```

MCP server runs at http://localhost:9999

## Development

```shell
make install
source .venv/bin/activate

# For local dev with PostgreSQL
cp deploy/.env.default deploy/.env
make up
```

Built with [DipDup](https://dipdup.io) - Documentation: [dipdup.io/docs](https://dipdup.io/docs/)

## Scenaries

Track USDC transfers, ask perplexity for correct contract address and from which block to start indexer. Add transfers index. Answer very briefly.
