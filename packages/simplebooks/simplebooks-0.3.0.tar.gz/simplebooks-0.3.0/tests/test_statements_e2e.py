from context import models, simplebooks
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
        simplebooks.set_connection_info(DB_FILEPATH)
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

    def make_txn(self, credit_acct: models.Account, debit_acct: models.Account,
                 amount: int, details: dict|None = None) -> models.Transaction:
        txn_nonce = os.urandom(16)
        credit_entry = models.Entry({
            'type': models.EntryType.CREDIT,
            'account_id': credit_acct.id,
            'amount': amount,
            'nonce': txn_nonce,
        })
        debit_entry = models.Entry({
            'type': models.EntryType.DEBIT,
            'account_id': debit_acct.id,
            'amount': amount,
            'nonce': txn_nonce,
        })
        txn = models.Transaction.prepare(
            [credit_entry, debit_entry],
            str(time()),
            details=details
        )
        return txn

    def test_e2e(self):
        assert models.Account.query().count() == 0
        assert models.Entry.query().count() == 0

        # setup identity, currency, ledger, and some accounts
        identity = models.Identity.insert({'name': 'Test Man'})
        currency = models.Currency.insert({
            'name': 'US Dollar',
            'prefix_symbol': '$',
            'fx_symbol': 'USD',
            'base': 100,
            'unit_divisions': 1,
        })
        ledger = models.Ledger.insert({
            'name': 'General Ledger',
            'identity_id': identity.id,
            'currency_id': currency.id,
            'type': models.LedgerType.PRESENT,
        })
        asset_acct, liability_acct, equity_acct = ledger.setup_basic_accounts()
        asset_acct.save()
        liability_acct.save()
        equity_acct.save()

        # make sub account
        assert len(liability_acct.children) == 0
        liability_sub_acct = models.Account.insert({
            'name': 'Liability Sub Account',
            'type': models.AccountType.LIABILITY,
            'ledger_id': ledger.id,
            'parent_id': liability_acct.id,
        })

        # prepare and save some valid transactions
        txn1 = self.make_txn(equity_acct, asset_acct, 10_000_00)
        assert txn1.validate()
        txn1.save()
        txn2 = self.make_txn(liability_acct, equity_acct, 5_000_00)
        assert txn2.validate()
        txn2.save()
        txn3 = self.make_txn(liability_sub_acct, liability_acct, 2_000_00)
        assert txn3.validate()
        txn3.save()

        # check balances
        assert equity_acct.balance() == 5_000_00, equity_acct.balance()
        assert asset_acct.balance() == 10_000_00, asset_acct.balance()
        assert liability_acct.balance() == 3_000_00, liability_acct.balance()
        assert liability_sub_acct.balance() == 2_000_00, liability_sub_acct.balance()
        balances = ledger.balances(reload=True)
        assert len(balances.keys()) == 4, balances
        assert balances[equity_acct.id][0] == 5_000_00, balances[equity_acct.id][0]
        assert balances[asset_acct.id][0] == 10_000_00, balances[asset_acct.id][0]
        assert balances[liability_acct.id][0] == 3_000_00, balances[liability_acct.id][0]
        assert balances[liability_sub_acct.id][0] == 2_000_00, balances[liability_sub_acct.id][0]

        # make a Statement with the transactions
        stmt = models.Statement.prepare([txn1, txn2, txn3], ledger)
        assert stmt.validate()
        stmt.save()

        # trim
        trimmed = stmt.trim()
        assert trimmed == 3, trimmed

        # statement should not delete itself during a trim
        assert models.Statement.find(stmt.id) is not None, 'Statement trimmed itself'

        # check balances without the Statement balances
        assert equity_acct.balance() == 0, equity_acct.balance()
        assert asset_acct.balance() == 0, asset_acct.balance()
        assert liability_acct.balance() == 0, liability_acct.balance()
        assert liability_sub_acct.balance() == 0, liability_sub_acct.balance()

        # check balances with the Statement balances
        assert equity_acct.balance(previous_balances=stmt.balances) == 5_000_00, \
            equity_acct.balance(previous_balances=stmt.balances)
        assert asset_acct.balance(previous_balances=stmt.balances) == 10_000_00, \
            asset_acct.balance(previous_balances=stmt.balances)
        assert liability_acct.balance(previous_balances=stmt.balances) == 3_000_00, \
            liability_acct.balance(previous_balances=stmt.balances)
        assert liability_sub_acct.balance(previous_balances=stmt.balances) == 2_000_00, \
            liability_sub_acct.balance(previous_balances=stmt.balances)

        # check archived transactions
        stmt.archived_transactions().reload()
        assert len(stmt.archived_transactions) == 3, stmt.archived_transactions
        for txn in stmt.archived_transactions:
            txn: models.ArchivedTransaction
            assert txn.validate()


if __name__ == '__main__':
    unittest.main()
