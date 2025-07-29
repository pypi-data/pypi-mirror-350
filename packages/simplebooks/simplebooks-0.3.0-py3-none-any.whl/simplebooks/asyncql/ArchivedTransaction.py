from __future__ import annotations
from sqloquent.asyncql import AsyncSqlModel, AsyncRelatedCollection
from sqloquent.errors import vert
from .ArchivedEntry import ArchivedEntry, EntryType
import packify


_empty_dict = packify.pack({})


class ArchivedTransaction(AsyncSqlModel):
    connection_info: str = ''
    table: str = 'archived_transactions'
    id_column: str = 'id'
    columns: tuple[str] = ('id', 'entry_ids', 'ledger_ids', 'timestamp', 'details')
    id: str
    entry_ids: str
    ledger_ids: str
    timestamp: str
    details: bytes
    entries: AsyncRelatedCollection
    ledgers: AsyncRelatedCollection
    statements: AsyncRelatedCollection

    # override automatic properties
    @property
    def details(self) -> dict[str, bytes]:
        """A packify.SerializableType stored in the database as a blob."""
        return packify.unpack(self.data.get('details', _empty_dict))
    @details.setter
    def details(self, val: dict[str, bytes]):
        if type(val) is not dict:
            return
        if not all([type(k) is str and type(v) is bytes for k, v in val.items()]):
            return
        self.data['details'] = packify.pack(val)

    @classmethod
    def _encode(cls, data: dict|None) -> dict|None:
        """Encode values for saving."""
        if type(data) is not dict:
            return None
        if type(data.get('details', {})) is dict:
            data['details'] = packify.pack(data.get('details', {}))
        return data

    async def validate(self, reload: bool = False) -> bool:
        """Determines if a Transaction is valid using the rules of accounting.
            Raises TypeError for invalid arguments. Raises ValueError if the
            entries do not balance for each ledger; or if any of the entries is
            contained within an existing Transaction. If reload is set to True,
            entries and accounts will be reloaded from the database.
        """
        if reload:
            await self.entries().reload()

        # first check that all ledgers balance
        ledgers = {}
        entry: ArchivedEntry
        for entry in self.entries:
            if reload:
                await entry.account().reload()
            if entry.account.ledger_id not in ledgers:
                ledgers[entry.account.ledger_id] = {'Dr': 0, 'Cr': 0}
            if entry.type in (EntryType.CREDIT, EntryType.CREDIT.value):
                ledgers[entry.account.ledger_id]['Cr'] += entry.amount
            else:
                ledgers[entry.account.ledger_id]['Dr'] += entry.amount

        for ledger_id, balances in ledgers.items():
            vert(balances['Cr'] == balances['Dr'],
                f"ledger {ledger_id} unbalanced: {balances['Cr']} Cr != {balances['Dr']} Dr")

        return True

    async def save(self, reload: bool = False) -> ArchivedTransaction:
        """Validate the transaction, save the entries, then save the
            transaction.
        """
        assert await self.validate(reload), 'cannot save an invalid Transaction'
        for e in self.entries:
            await e.save()
        return await super().save()

