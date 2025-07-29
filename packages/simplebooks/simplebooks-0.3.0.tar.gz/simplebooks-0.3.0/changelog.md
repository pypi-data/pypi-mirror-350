## 0.3.0

- Added `Statement`, `ArchivedTransaction`, and `ArchivedEntry`
- Updated `Transaction`: added `archive` method
- Updated `Account`:
    - Added `archived_entries` relation
    - Updated `balance` method to accept `previous_balances` parameter
- Updated `Entry`:
    - Added `archive` method
- Updated `Ledger`:
    - Added `archived_transactions` relation
    - Added `statements` relation

## 0.2.3

- Patch: readme links pointed to outdated documentation

## 0.2.2

- Patch: updated sqloquent dependency
- Updated `Account`: added boolean `active` column
- Added `get_migrations` tool
- Updated `publish_migrations` to accept callback to modify migrations

## 0.2.1

- Patch: expose `LedgerType` at module level

## 0.2.0

- Adapted bookchain v0.2.0 update: new `AccountCategory` and `LedgerType`
- Added a few helpful methods


