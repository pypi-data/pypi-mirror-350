from asyncio import run
from context import asyncql, simplebooks
from genericpath import isfile
from os import getcwd
from sqlite3 import OperationalError
from time import time
import os
import unittest


DB_FILEPATH = f'{getcwd()}/tests/test.db'
MIGRATIONS_PATH = 'tests/migrations'


class TestStatementsE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        asyncql.set_connection_info(DB_FILEPATH)
        super().setUpClass()

    def setUp(self):
        if isfile(DB_FILEPATH):
            os.remove(DB_FILEPATH)
        simplebooks.publish_migrations(MIGRATIONS_PATH)
        simplebooks.automigrate(MIGRATIONS_PATH, DB_FILEPATH)
        super().setUp()

    def tearDown(self):
        for file in os.listdir(MIGRATIONS_PATH):
            if isfile(f'{MIGRATIONS_PATH}/{file}'):
                os.remove(f'{MIGRATIONS_PATH}/{file}')
        if isfile(DB_FILEPATH):
            os.remove(DB_FILEPATH)
        super().tearDown()

    async def make_txn(self, credit_acct: asyncql.Account, debit_acct: asyncql.Account,
                 amount: int, details: dict|None = None) -> asyncql.Transaction:
        txn_nonce = os.urandom(16)
        credit_entry = asyncql.Entry({
            'type': asyncql.EntryType.CREDIT,
            'account_id': credit_acct.id,
            'amount': amount,
            'nonce': txn_nonce,
        })
        debit_entry = asyncql.Entry({
            'type': asyncql.EntryType.DEBIT,
            'account_id': debit_acct.id,
            'amount': amount,
            'nonce': txn_nonce,
        })
        txn = await asyncql.Transaction.prepare(
            [credit_entry, debit_entry],
            str(time()),
            details=details
        )
        return txn

    async def e2e(self):
        assert await asyncql.Account.query().count() == 0
        assert await asyncql.Entry.query().count() == 0

        # setup identity, currency, ledger, and some accounts
        identity = await asyncql.Identity.insert({'name': 'Test Man'})
        currency = await asyncql.Currency.insert({
            'name': 'US Dollar',
            'prefix_symbol': '$',
            'fx_symbol': 'USD',
            'base': 100,
            'unit_divisions': 1,
        })
        ledger = await asyncql.Ledger.insert({
            'name': 'General Ledger',
            'identity_id': identity.id,
            'currency_id': currency.id,
            'type': asyncql.LedgerType.PRESENT,
        })
        asset_acct, liability_acct, equity_acct = ledger.setup_basic_accounts()
        await asset_acct.save()
        await liability_acct.save()
        await equity_acct.save()

        # make sub account
        assert len(liability_acct.children) == 0
        liability_sub_acct = await asyncql.Account.insert({
            'name': 'Liability Sub Account',
            'type': asyncql.AccountType.LIABILITY,
            'ledger_id': ledger.id,
            'parent_id': liability_acct.id,
        })

        # prepare and save some valid transactions
        txn1 = await self.make_txn(equity_acct, asset_acct, 10_000_00)
        assert await txn1.validate()
        await txn1.save()
        txn2 = await self.make_txn(liability_acct, equity_acct, 5_000_00)
        assert await txn2.validate()
        await txn2.save()
        txn3 = await self.make_txn(liability_sub_acct, liability_acct, 2_000_00)
        assert await txn3.validate()
        await txn3.save()

        # check balances
        assert await equity_acct.balance() == 5_000_00, await equity_acct.balance()
        assert await asset_acct.balance() == 10_000_00, await asset_acct.balance()
        assert await liability_acct.balance() == 3_000_00, await liability_acct.balance()
        assert await liability_sub_acct.balance() == 2_000_00, await liability_sub_acct.balance()
        balances = await ledger.balances(reload=True)
        assert len(balances.keys()) == 4, balances
        assert balances[equity_acct.id][0] == 5_000_00, balances[equity_acct.id][0]
        assert balances[asset_acct.id][0] == 10_000_00, balances[asset_acct.id][0]
        assert balances[liability_acct.id][0] == 3_000_00, balances[liability_acct.id][0]
        assert balances[liability_sub_acct.id][0] == 2_000_00, balances[liability_sub_acct.id][0]

        # make a Statement with the transactions
        stmt = await asyncql.Statement.prepare([txn1, txn2, txn3], ledger)
        assert await stmt.validate()
        await stmt.save()

        # trim
        trimmed = await stmt.trim()
        assert trimmed == 3, trimmed

        # statement should not delete itself during a trim
        assert await asyncql.Statement.find(stmt.id) is not None, 'Statement trimmed itself'

        # check balances without the Statement balances
        assert await equity_acct.balance() == 0, await equity_acct.balance()
        assert await asset_acct.balance() == 0, await asset_acct.balance()
        assert await liability_acct.balance() == 0, await liability_acct.balance()
        assert await liability_sub_acct.balance() == 0, await liability_sub_acct.balance()

        # check balances with the Statement balances
        assert await equity_acct.balance(previous_balances=stmt.balances) == 5_000_00, \
            await equity_acct.balance(previous_balances=stmt.balances)
        assert await asset_acct.balance(previous_balances=stmt.balances) == 10_000_00, \
            await asset_acct.balance(previous_balances=stmt.balances)
        assert await liability_acct.balance(previous_balances=stmt.balances) == 3_000_00, \
            await liability_acct.balance(previous_balances=stmt.balances)
        assert await liability_sub_acct.balance(previous_balances=stmt.balances) == 2_000_00, \
            await liability_sub_acct.balance(previous_balances=stmt.balances)

        # check archived transactions
        await stmt.archived_transactions().reload()
        assert len(stmt.archived_transactions) == 3, stmt.archived_transactions
        for txn in stmt.archived_transactions:
            txn: asyncql.ArchivedTransaction
            assert await txn.validate()

    def test_e2e(self):
        run(self.e2e())


if __name__ == '__main__':
    unittest.main()

