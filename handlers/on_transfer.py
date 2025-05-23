from dipdup.context import HandlerContext
from dipdup.models.evm import EvmEvent

from dipdup_mcp_tutorial import models
from dipdup_mcp_tutorial.types.erc20.evm_events.transfer import TransferPayload


async def on_transfer(
    ctx: HandlerContext,
    event: EvmEvent[TransferPayload],
) -> None:
    """Handle ERC20 token transfers"""
    # Get or create token record
    token = await models.Token.get_or_none(address=event.data.address)
    if token is None:
        token = models.Token(
            address=event.data.address,
            name='Unknown',
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
