from dipdup import fields
from dipdup.models import Model


class Token(Model):
    """ERC20 token information"""

    address = fields.TextField(primary_key=True)
    name = fields.TextField(null=True)


class Transfer(Model):
    """ERC20 token transfer record"""

    id = fields.TextField(primary_key=True)

    token: fields.ForeignKeyRelation[Token] = fields.ForeignKeyField('models.Token', related_name='transfers')

    # Transfer details
    from_address = fields.TextField(db_index=True)
    to_address = fields.TextField(db_index=True)
    value = fields.DecimalField(decimal_places=0, max_digits=78)

    # Transaction info
    transaction_hash = fields.TextField(db_index=True)

    # Block info
    level = fields.BigIntField(db_index=True)
    timestamp = fields.DatetimeField(db_index=True)
