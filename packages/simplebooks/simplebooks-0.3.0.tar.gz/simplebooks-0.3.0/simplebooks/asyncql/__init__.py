from .Account import Account
from .AccountCategory import AccountCategory
from .AccountType import AccountType
from .ArchivedEntry import ArchivedEntry
from .ArchivedTransaction import ArchivedTransaction
from .Currency import Currency
from .Customer import Customer
from .Entry import Entry
from .EntryType import EntryType
from .Identity import Identity
from .Ledger import Ledger
from .LedgerType import LedgerType
from .Statement import Statement
from .Transaction import Transaction
from .Vendor import Vendor
from sqloquent.asyncql import (
    async_contains, async_within, async_has_many, async_belongs_to,
)


Identity.ledgers = async_has_many(Identity, Ledger, 'identity_id')
Ledger.owner = async_belongs_to(Ledger, Identity, 'identity_id')

Ledger.currency = async_belongs_to(Ledger, Currency, 'currency_id')
Currency.ledgers = async_has_many(Currency, Ledger, 'currency_id')

Ledger.accounts = async_has_many(Ledger, Account, 'ledger_id')
Account.ledger = async_belongs_to(Account, Ledger, 'ledger_id')

Account.children = async_has_many(Account, Account, 'parent_id')
Account.parent = async_belongs_to(Account, Account, 'parent_id')

Account.category = async_belongs_to(Account, AccountCategory, 'category_id')
AccountCategory.accounts = async_has_many(AccountCategory, Account, 'category_id')

Account.entries = async_has_many(Account, Entry, 'account_id')
Entry.account = async_belongs_to(Entry, Account, 'account_id')

Entry.transactions = async_within(Entry, Transaction, 'entry_ids')
Transaction.entries = async_contains(Transaction, Entry, 'entry_ids')

Transaction.ledgers = async_contains(Transaction, Ledger, 'ledger_ids')
Ledger.transactions = async_within(Ledger, Transaction, 'ledger_ids')

Statement.ledger = async_belongs_to(Statement, Ledger, 'ledger_id')
Ledger.statements = async_has_many(Ledger, Statement, 'ledger_id')

Statement.transactions = async_contains(Statement, Transaction, 'tx_ids')
Transaction.statements = async_within(Transaction, Statement, 'tx_ids')

Statement.archived_transactions = async_contains(Statement, ArchivedTransaction, 'tx_ids')
ArchivedTransaction.statements = async_within(ArchivedTransaction, Statement, 'tx_ids')

ArchivedEntry.transactions = async_within(ArchivedEntry, ArchivedTransaction, 'entry_ids')
ArchivedTransaction.entries = async_contains(ArchivedTransaction, ArchivedEntry, 'entry_ids')

ArchivedEntry.account = async_belongs_to(ArchivedEntry, Account, 'account_id')
Account.archived_entries = async_has_many(Account, ArchivedEntry, 'account_id')

ArchivedTransaction.ledgers = async_contains(ArchivedTransaction, Ledger, 'ledger_ids')
Ledger.archived_transactions = async_within(Ledger, ArchivedTransaction, 'ledger_ids')


def set_connection_info(db_file_path: str):
    """Set the connection info for all models to use the specified
        sqlite3 database file path.
    """
    Account.connection_info = db_file_path
    AccountCategory.connection_info = db_file_path
    ArchivedEntry.connection_info = db_file_path
    ArchivedTransaction.connection_info = db_file_path
    Currency.connection_info = db_file_path
    Customer.connection_info = db_file_path
    Entry.connection_info = db_file_path
    Identity.connection_info = db_file_path
    Ledger.connection_info = db_file_path
    Statement.connection_info = db_file_path
    Transaction.connection_info = db_file_path
    Vendor.connection_info = db_file_path


# no longer needed
del async_contains
del async_belongs_to
del async_within
del async_has_many

