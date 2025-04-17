from dipdup import mcp
from tortoise.expressions import Q

from dipdup_mcp_tutorial import models

# Constants for indexer-specific settings
ERC20_TEMPLATE_NAME = 'erc20_events'  # The template to use for ERC20 event indexes
ERC20_INDEX_PREFIX = 'transfers_'  # Prefix for auto-generated index names
ERC20_TYPENAME = 'erc20'


@mcp.tool(
    'AddIndexForERC20Token', 'Add an ERC20 token contract and create an event index for tracking transfers'
)
async def add_erc20_token(
    token_name: str,
    token_address: str,
    first_level: int = 0,
    last_level: int = 0,
) -> str:
    """Add an ERC20 token contract and create a transfer event index from template.

    Args:
        token_name: Name identifier for the token contract (e.g. 'usdt', 'link')
        token_address: The ERC20 token contract address
        first_level: Optional starting block level for indexing
        last_level: Optional ending block level for indexing

    Returns:
        A message confirming the contract and index were added
    """
    # Get the indexer API URL
    ctx = mcp.get_ctx()

    # Add the contract to the indexer via API call
    add_c_resp = await ctx.call_api(
        method='post',
        path='/add_contract',
        params={
            'kind': 'evm',
            'name': token_name,
            'address': token_address,
            'typename': ERC20_TYPENAME,
        },
    )

    # Add the index from template via API call
    index_name = f'{ERC20_INDEX_PREFIX}{token_name}_events'
    add_i_resp = await ctx.call_api(
        method='post',
        path='/add_index',
        params={
            'name': index_name,
            'template': ERC20_TEMPLATE_NAME,
            'values': {'contract': token_name},
            'first_level': first_level,
            'last_level': last_level,
        },
    )

    # Save token info to the database
    token = models.Token(address=token_address, name=token_name)
    await token.save()

    return f'Calling add contract: {add_c_resp or 'Success'}\nCalling add index: {add_i_resp or 'Success'}'


@mcp.tool('GetTokenTransfers', 'Get token transfers to or from a specific address')
async def get_token_transfers(
    address: str,
    limit: int = 10,
    from_address: bool = True,
    to_address: bool = True,
) -> str:
    """Get token transfers to or from a specific address.

    Args:
        address: The address to search for transfers
        limit: Maximum number of transfers to return (default: 10)
        from_address: Include transfers from this address (default: True)
        to_address: Include transfers to this address (default: True)

    Returns:
        A formatted string with transfer details
    """
    if not from_address and not to_address:
        return "Error: At least one of 'from_address' or 'to_address' must be True"

    # Build query conditions - more elegant pythonic approach
    conditions = Q()
    if from_address:
        conditions |= Q(from_address=address)
    if to_address:
        conditions |= Q(to_address=address)

    # Execute single query with our conditions
    transfers = await models.Transfer.filter(conditions).order_by('-level').limit(limit).prefetch_related('token')

    if not transfers:
        return f'No transfers found for address {address}'

    # Format the results with cleaner presentation
    result = [f'Token transfers for address {address}:']

    for i, t in enumerate(transfers):
        token_name = t.token.name if t.token.name else t.token.address
        token_display = f'{token_name}' if t.token.name else f'Token at {t.token.address[:10]}...'

        result.append(
            f'{i}. {t.from_address} → {t.to_address}\n'
            f'{t.value} {token_display} raw units\n'
            f'Block: {t.level}, Tx: ...{t.transaction_hash[-4:]}'
        )

    return '\n'.join(result)
