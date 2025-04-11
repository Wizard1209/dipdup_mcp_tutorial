from dipdup.context import HandlerContext
from dipdup.models.evm import EvmEvent

from advanced_mcp_tutorial import models
from advanced_mcp_tutorial.types.erc20.evm_events.transfer import TransferPayload


async def on_transfer(
    ctx: HandlerContext,
    event: EvmEvent[TransferPayload],
) -> None:
    """Handle ERC20 token transfers"""
    # Get or create token record
    token = await models.Token.get_or_none(address=event.data.address)
    if token is None:
        contract_name = (c.name for c in ctx.config.contracts.values() if c.address == event.data.address)
        token = models.Token(
            address=event.data.address,
            name=next(contract_name, 'Unknown'),
        )
        await token.save()

    transfer = models.Transfer(
        id=f'{event.data.transaction_hash}.{event.data.log_index}',
        token=token,
        from_address=event.payload.from_,
        to_address=event.payload.to,
        value=event.payload.value,
        transaction_hash=event.data.transaction_hash,
        level=event.data.level,
        timestamp=event.data.timestamp,
    )

    await transfer.save()
