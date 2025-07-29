from __future__ import annotations
from sqloquent import SqlModel, RelatedModel, RelatedCollection
from sqloquent.errors import tert, vert
from .ArchivedTransaction import ArchivedTransaction
from .Ledger import Ledger
from .Transaction import Transaction
from .Entry import Entry, EntryType
from time import time
import packify


_empty_dict = packify.pack({})


class Statement(SqlModel):
    connection_info: str = ''
    table: str = 'statements'
    id_column: str = 'id'
    columns: tuple[str] = (
        'id', 'height', 'tx_ids', 'ledger_id', 'balances', 'timestamp', 'details'
    )
    id: str
    height: int
    tx_ids: str
    ledger_id: str
    balances: bytes
    timestamp: str
    details: bytes
    ledger: RelatedModel
    transactions: RelatedCollection
    archived_transactions: RelatedCollection

    @property
    def tx_ids(self) -> list[str]:
        """A list of transaction IDs."""
        return self.data.get('tx_ids', '').split(',')
    @tx_ids.setter
    def tx_ids(self, val: list[str]):
        if type(val) is not list:
            return
        # sort the ids, join into a comma-separated string
        val.sort()
        self.data['tx_ids'] = ','.join(val)

    @property
    def balances(self) -> dict[str, tuple[EntryType, int]]:
        """A dict mapping account IDs to tuple[EntryType, int] balances."""
        balances: dict = packify.unpack(self.data.get('balances', _empty_dict))
        return {
            k: (EntryType(v[0]), v[1])
            for k, v in balances.items()
        }
    @balances.setter
    def balances(self, val: dict[str, tuple[EntryType, int]]):
        tert(type(val) is dict, 'balances must be a dict')
        tert(all([
                type(k) is str and
                type(v) is tuple and
                len(v) == 2 and
                type(v[0]) is EntryType and
                type(v[1]) is int
                for k, v in val.items()
            ]),
            'balances must be a dict of str: tuple[EntryType, int]')
        val = {
            k: (v[0].value, v[1])
            for k, v in val.items()
        }
        self.data['balances'] = packify.pack(val)

    @classmethod
    def calculate_balances(
        cls, txns: list[Transaction|ArchivedTransaction],
        parent_balances: dict[str, tuple[EntryType, int]]|None = None,
        reload: bool = False
    ) -> dict[str, tuple[EntryType, int]]:
        """Calculates the account balances for a list of rolled-up
            transactions. If parent_balances is provided, those are the
            starting balances to which the balances of the rolled-up
            transactions are added. If reload is True, the entries are
            reloaded from the database.
        """
        balances = parent_balances or {}
        for txn in txns:
            if reload:
                txn.entries().reload()
            for e in txn.entries:
                e: Entry
                bal = {EntryType.CREDIT: 0, EntryType.DEBIT: 0}
                if e.account_id in balances:
                    bal[balances[e.account_id][0]] = balances[e.account_id][1]
                bal[e.type] += e.amount
                net_credit = bal[EntryType.CREDIT] - bal[EntryType.DEBIT]
                if net_credit >= 0:
                    balances[e.account_id] = (EntryType.CREDIT, net_credit)
                else:
                    balances[e.account_id] = (EntryType.DEBIT, -net_credit)
        return balances

    @classmethod
    def prepare(
            cls, txns: list[Transaction|ArchivedTransaction],
            ledger: Ledger|None = None
        ) -> Statement:
        """Prepare a statement by checking that all txns are for the
            same ledger and summarizing the net account balance changes
            from the transactions and the previous Statement. Raises
            TypeError if there are no txns and no ledger, or if the
            transactions are not all Transaction or ArchivedTransaction
            instances. Raises ValueError if the transactions are not all
            for the same ledger.
        """
        tert(len(txns) > 0 or ledger is not None,
            'must provide either txns or ledger')
        tert(all([
                isinstance(txn, (Transaction, ArchivedTransaction))
                for txn in txns
            ]),
             'all txns must be Transaction or ArchivedTransaction instances'
        )
        if ledger is None:
            ledger = txns[0].ledger
        vert(all([ledger.id == txn.ledger_ids for txn in txns]),
             'all txns must be for the same ledger')

        balances = {}
        height = 0

        # check for parent
        parent: Statement|None = cls.query().equal(
            'ledger_id', ledger.id
        ).order_by('height', direction='desc').first()
        if parent is None:
            balances = cls.calculate_balances(txns)
        else:
            balances = cls.calculate_balances(txns, parent.balances)
            height = parent.height + 1

        # create statement
        stmt = cls({
            'ledger_id': ledger.id,
            'timestamp': str(int(time())),
            'height': height
        })
        stmt.balances = balances
        stmt.tx_ids = [txn.id for txn in txns]
        return stmt

    def validate(self, reload: bool = False) -> bool:
        """Validates that the balances are correct, and that the height
            is 1 + the height of the most recentStatement (if one
            exists).
        """
        if reload:
            self.reload()
            self.transactions().reload()
            self.archived_transactions().reload()

        # check that the balances are correct
        txns = {
            txn.id: txn
            for txn in self.transactions
            if txn.id is not None
        }
        txns.update({
            txn.id: txn
            for txn in self.archived_transactions
            if txn.id is not None
        })
        balances = self.calculate_balances(list(txns.values()))
        if balances != self.balances:
            return False

        # check that the height is correct
        parent: Statement|None = self.query().equal(
            'ledger_id', self.ledger_id
        ).order_by('height', direction='desc').not_equal('id', self.id).first()
        if parent is None:
            return self.height == 0
        return self.height == parent.height + 1

    def trim(self, archive: bool = True) -> None:
        """Trims the transactions and entries summarized in this
            Statement. Returns the number of transactions trimmed. If
            archive is True, the transactions and entries are archived
            before being deleted. Raises ValueError if the Statement is
            not valid.
        """
        vert(self.validate(), 'Statement is not valid')
        self.transactions().reload()
        txns = self.transactions
        for txn in txns:
            txn: Transaction
            txn.entries().reload()
            for e in txn.entries:
                e: Entry
                if archive:
                    e.archive()
                e.delete()
            if archive:
                txn.archive()
            txn.delete()
        return len(txns)

