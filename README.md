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

## Prompt examples

> Hi Copilot, how's my indexer doing? Please, answer very briefly in this dialog.
> Track USDC transfers, ask Perplexity for correct contract address and block that was two years ago, add transfers index with these parameters.
> Index USDT from same block
> What is the volume of token transfers for address 0xbf51c5f00f4435536ed26e23073c6fd0990a32ed and for what time period?
> Give me a quick summary of token transactions for 0x8a4497f460afa320f372114981de0198e2166095