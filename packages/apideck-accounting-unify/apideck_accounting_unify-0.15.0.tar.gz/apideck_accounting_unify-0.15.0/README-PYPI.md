# apideck-accounting-unify

Developer-friendly & type-safe Python SDK specifically catered to leverage *apideck-accounting-unify* API.

<div align="left">
    <a href="https://www.speakeasy.com/?utm_source=apideck-accounting-unify&utm_campaign=python"><img src="https://custom-icon-badges.demolab.com/badge/-Built%20By%20Speakeasy-212015?style=for-the-badge&logoColor=FBE331&logo=speakeasy&labelColor=545454" /></a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg" style="width: 100px; height: 28px;" />
    </a>
</div>

<!-- Start Summary [summary] -->
## Summary

Apideck: The Apideck OpenAPI Spec: SDK Optimized

For more information about the API: [Apideck Developer Docs](https://developers.apideck.com)
<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents
<!-- $toc-max-depth=2 -->
* [apideck-accounting-unify](https://github.com/apideck-libraries/sdk-python-pack/blob/master/#apideck-accounting-unify)
  * [SDK Installation](https://github.com/apideck-libraries/sdk-python-pack/blob/master/#sdk-installation)
  * [IDE Support](https://github.com/apideck-libraries/sdk-python-pack/blob/master/#ide-support)
  * [SDK Example Usage](https://github.com/apideck-libraries/sdk-python-pack/blob/master/#sdk-example-usage)
  * [Authentication](https://github.com/apideck-libraries/sdk-python-pack/blob/master/#authentication)
  * [Available Resources and Operations](https://github.com/apideck-libraries/sdk-python-pack/blob/master/#available-resources-and-operations)
  * [Pagination](https://github.com/apideck-libraries/sdk-python-pack/blob/master/#pagination)
  * [File uploads](https://github.com/apideck-libraries/sdk-python-pack/blob/master/#file-uploads)
  * [Retries](https://github.com/apideck-libraries/sdk-python-pack/blob/master/#retries)
  * [Error Handling](https://github.com/apideck-libraries/sdk-python-pack/blob/master/#error-handling)
  * [Server Selection](https://github.com/apideck-libraries/sdk-python-pack/blob/master/#server-selection)
  * [Custom HTTP Client](https://github.com/apideck-libraries/sdk-python-pack/blob/master/#custom-http-client)
  * [Resource Management](https://github.com/apideck-libraries/sdk-python-pack/blob/master/#resource-management)
  * [Debugging](https://github.com/apideck-libraries/sdk-python-pack/blob/master/#debugging)
* [Development](https://github.com/apideck-libraries/sdk-python-pack/blob/master/#development)
  * [Maturity](https://github.com/apideck-libraries/sdk-python-pack/blob/master/#maturity)
  * [Contributions](https://github.com/apideck-libraries/sdk-python-pack/blob/master/#contributions)

<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

> [!NOTE]
> **Python version upgrade policy**
>
> Once a Python version reaches its [official end of life date](https://devguide.python.org/versions/), a 3-month grace period is provided for users to upgrade. Following this grace period, the minimum python version supported in the SDK will be updated.

The SDK can be installed with either *pip* or *poetry* package managers.

### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install apideck-accounting-unify
```

### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add apideck-accounting-unify
```

### Shell and script usage with `uv`

You can use this SDK in a Python shell with [uv](https://docs.astral.sh/uv/) and the `uvx` command that comes with it like so:

```shell
uvx --from apideck-accounting-unify python
```

It's also possible to write a standalone Python script without needing to set up a whole project like so:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "apideck-accounting-unify",
# ]
# ///

from apideck_accounting_unify import Apideck

sdk = Apideck(
  # SDK arguments
)

# Rest of script here...
```

Once that is saved to a file, you can run it with `uv run script.py` where
`script.py` can be replaced with the actual file name.
<!-- End SDK Installation [installation] -->

<!-- Start IDE Support [idesupport] -->
## IDE Support

### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)
<!-- End IDE Support [idesupport] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```python
# Synchronous Example
from apideck_accounting_unify import Apideck
import os


with Apideck(
    api_key=os.getenv("APIDECK_API_KEY", ""),
    consumer_id="test-consumer",
    app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
) as apideck:

    res = apideck.accounting.tax_rates.list(consumer_id="test-consumer", app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX", service_id="salesforce", filter_={
        "assets": True,
        "equity": True,
        "expenses": True,
        "liabilities": True,
        "revenue": True,
    }, pass_through={
        "search": "San Francisco",
    }, fields="id,updated_at")

    while res is not None:
        # Handle items

        res = res.next()
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
from apideck_accounting_unify import Apideck
import asyncio
import os

async def main():

    async with Apideck(
        api_key=os.getenv("APIDECK_API_KEY", ""),
        consumer_id="test-consumer",
        app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
    ) as apideck:

        res = await apideck.accounting.tax_rates.list_async(consumer_id="test-consumer", app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX", service_id="salesforce", filter_={
            "assets": True,
            "equity": True,
            "expenses": True,
            "liabilities": True,
            "revenue": True,
        }, pass_through={
            "search": "San Francisco",
        }, fields="id,updated_at")

        while res is not None:
            # Handle items

            res = res.next()

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name      | Type | Scheme      | Environment Variable |
| --------- | ---- | ----------- | -------------------- |
| `api_key` | http | HTTP Bearer | `APIDECK_API_KEY`    |

To authenticate with the API the `api_key` parameter must be set when initializing the SDK client instance. For example:
```python
from apideck_accounting_unify import Apideck
import os


with Apideck(
    api_key=os.getenv("APIDECK_API_KEY", ""),
    consumer_id="test-consumer",
    app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
) as apideck:

    res = apideck.accounting.tax_rates.list(consumer_id="test-consumer", app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX", service_id="salesforce", filter_={
        "assets": True,
        "equity": True,
        "expenses": True,
        "liabilities": True,
        "revenue": True,
    }, pass_through={
        "search": "San Francisco",
    }, fields="id,updated_at")

    while res is not None:
        # Handle items

        res = res.next()

```
<!-- End Authentication [security] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [accounting](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/accounting/README.md)


#### [accounting.aged_creditors](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/agedcreditorssdk/README.md)

* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/agedcreditorssdk/README.md#get) - Get Aged Creditors

#### [accounting.aged_debtors](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/ageddebtorssdk/README.md)

* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/ageddebtorssdk/README.md#get) - Get Aged Debtors

#### [accounting.attachments](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/attachments/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/attachments/README.md#list) - List Attachments
* [upload](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/attachments/README.md#upload) - Upload attachment
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/attachments/README.md#get) - Get Attachment
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/attachments/README.md#delete) - Delete Attachment
* [download](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/attachments/README.md#download) - Download Attachment

#### [accounting.balance_sheet](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/balancesheetsdk/README.md)

* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/balancesheetsdk/README.md#get) - Get BalanceSheet

#### [accounting.bank_feed_accounts](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/bankfeedaccounts/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/bankfeedaccounts/README.md#list) - List Bank Feed Accounts
* [create](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/bankfeedaccounts/README.md#create) - Create Bank Feed Account
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/bankfeedaccounts/README.md#get) - Get Bank Feed Account
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/bankfeedaccounts/README.md#update) - Update Bank Feed Account
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/bankfeedaccounts/README.md#delete) - Delete Bank Feed Account

#### [accounting.bank_feed_statements](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/bankfeedstatements/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/bankfeedstatements/README.md#list) - List Bank Feed Statements
* [create](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/bankfeedstatements/README.md#create) - Create Bank Feed Statement
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/bankfeedstatements/README.md#get) - Get Bank Feed Statement
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/bankfeedstatements/README.md#update) - Update Bank Feed Statement
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/bankfeedstatements/README.md#delete) - Delete Bank Feed Statement

#### [accounting.bill_payments](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/billpayments/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/billpayments/README.md#list) - List Bill Payments
* [create](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/billpayments/README.md#create) - Create Bill Payment
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/billpayments/README.md#get) - Get Bill Payment
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/billpayments/README.md#update) - Update Bill Payment
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/billpayments/README.md#delete) - Delete Bill Payment

#### [accounting.bills](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/bills/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/bills/README.md#list) - List Bills
* [create](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/bills/README.md#create) - Create Bill
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/bills/README.md#get) - Get Bill
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/bills/README.md#update) - Update Bill
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/bills/README.md#delete) - Delete Bill

#### [accounting.company_info](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/companyinfosdk/README.md)

* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/companyinfosdk/README.md#get) - Get company info

#### [accounting.credit_notes](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/creditnotes/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/creditnotes/README.md#list) - List Credit Notes
* [create](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/creditnotes/README.md#create) - Create Credit Note
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/creditnotes/README.md#get) - Get Credit Note
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/creditnotes/README.md#update) - Update Credit Note
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/creditnotes/README.md#delete) - Delete Credit Note

#### [accounting.customers](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/customers/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/customers/README.md#list) - List Customers
* [create](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/customers/README.md#create) - Create Customer
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/customers/README.md#get) - Get Customer
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/customers/README.md#update) - Update Customer
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/customers/README.md#delete) - Delete Customer

#### [accounting.departments](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/departments/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/departments/README.md#list) - List Departments
* [create](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/departments/README.md#create) - Create Department
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/departments/README.md#get) - Get Department
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/departments/README.md#update) - Update Department
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/departments/README.md#delete) - Delete Department

#### [accounting.expenses](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/expenses/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/expenses/README.md#list) - List Expenses
* [create](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/expenses/README.md#create) - Create Expense
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/expenses/README.md#get) - Get Expense
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/expenses/README.md#update) - Update Expense
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/expenses/README.md#delete) - Delete Expense

#### [accounting.invoice_items](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/invoiceitems/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/invoiceitems/README.md#list) - List Invoice Items
* [create](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/invoiceitems/README.md#create) - Create Invoice Item
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/invoiceitems/README.md#get) - Get Invoice Item
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/invoiceitems/README.md#update) - Update Invoice Item
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/invoiceitems/README.md#delete) - Delete Invoice Item

#### [accounting.invoices](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/invoices/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/invoices/README.md#list) - List Invoices
* [create](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/invoices/README.md#create) - Create Invoice
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/invoices/README.md#get) - Get Invoice
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/invoices/README.md#update) - Update Invoice
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/invoices/README.md#delete) - Delete Invoice

#### [accounting.journal_entries](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/journalentries/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/journalentries/README.md#list) - List Journal Entries
* [create](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/journalentries/README.md#create) - Create Journal Entry
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/journalentries/README.md#get) - Get Journal Entry
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/journalentries/README.md#update) - Update Journal Entry
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/journalentries/README.md#delete) - Delete Journal Entry

#### [accounting.ledger_accounts](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/ledgeraccounts/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/ledgeraccounts/README.md#list) - List Ledger Accounts
* [create](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/ledgeraccounts/README.md#create) - Create Ledger Account
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/ledgeraccounts/README.md#get) - Get Ledger Account
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/ledgeraccounts/README.md#update) - Update Ledger Account
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/ledgeraccounts/README.md#delete) - Delete Ledger Account

#### [accounting.locations](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/locations/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/locations/README.md#list) - List Locations
* [create](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/locations/README.md#create) - Create Location
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/locations/README.md#get) - Get Location
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/locations/README.md#update) - Update Location
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/locations/README.md#delete) - Delete Location

#### [accounting.payments](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/payments/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/payments/README.md#list) - List Payments
* [create](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/payments/README.md#create) - Create Payment
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/payments/README.md#get) - Get Payment
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/payments/README.md#update) - Update Payment
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/payments/README.md#delete) - Delete Payment

#### [accounting.profit_and_loss](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/profitandlosssdk/README.md)

* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/profitandlosssdk/README.md#get) - Get Profit and Loss

#### [accounting.purchase_orders](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/purchaseorders/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/purchaseorders/README.md#list) - List Purchase Orders
* [create](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/purchaseorders/README.md#create) - Create Purchase Order
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/purchaseorders/README.md#get) - Get Purchase Order
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/purchaseorders/README.md#update) - Update Purchase Order
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/purchaseorders/README.md#delete) - Delete Purchase Order

#### [accounting.subsidiaries](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/subsidiaries/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/subsidiaries/README.md#list) - List Subsidiaries
* [create](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/subsidiaries/README.md#create) - Create Subsidiary
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/subsidiaries/README.md#get) - Get Subsidiary
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/subsidiaries/README.md#update) - Update Subsidiary
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/subsidiaries/README.md#delete) - Delete Subsidiary

#### [accounting.suppliers](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/suppliers/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/suppliers/README.md#list) - List Suppliers
* [create](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/suppliers/README.md#create) - Create Supplier
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/suppliers/README.md#get) - Get Supplier
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/suppliers/README.md#update) - Update Supplier
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/suppliers/README.md#delete) - Delete Supplier

#### [accounting.tax_rates](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/taxrates/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/taxrates/README.md#list) - List Tax Rates
* [create](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/taxrates/README.md#create) - Create Tax Rate
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/taxrates/README.md#get) - Get Tax Rate
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/taxrates/README.md#update) - Update Tax Rate
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/taxrates/README.md#delete) - Delete Tax Rate

#### [accounting.tracking_categories](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/trackingcategories/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/trackingcategories/README.md#list) - List Tracking Categories
* [create](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/trackingcategories/README.md#create) - Create Tracking Category
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/trackingcategories/README.md#get) - Get Tracking Category
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/trackingcategories/README.md#update) - Update Tracking Category
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/trackingcategories/README.md#delete) - Delete Tracking Category


### [vault](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/vault/README.md)


#### [vault.connection_custom_mappings](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/connectioncustommappings/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/connectioncustommappings/README.md#list) - List connection custom mappings

#### [vault.connection_settings](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/connectionsettings/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/connectionsettings/README.md#list) - Get resource settings
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/connectionsettings/README.md#update) - Update settings

#### [vault.connections](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/connections/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/connections/README.md#list) - Get all connections
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/connections/README.md#get) - Get connection
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/connections/README.md#update) - Update connection
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/connections/README.md#delete) - Deletes a connection
* [imports](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/connections/README.md#imports) - Import connection
* [token](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/connections/README.md#token) - Authorize Access Token

#### [vault.consumer_request_counts](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/consumerrequestcounts/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/consumerrequestcounts/README.md#list) - Consumer request counts

#### [vault.consumers](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/consumers/README.md)

* [create](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/consumers/README.md#create) - Create consumer
* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/consumers/README.md#list) - Get all consumers
* [get](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/consumers/README.md#get) - Get consumer
* [update](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/consumers/README.md#update) - Update consumer
* [delete](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/consumers/README.md#delete) - Delete consumer

#### [vault.create_callback](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/createcallback/README.md)

* [state](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/createcallback/README.md#state) - Create Callback State

#### [vault.custom_fields](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/customfields/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/customfields/README.md#list) - Get resource custom fields

#### [vault.custom_mappings](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/custommappings/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/custommappings/README.md#list) - List custom mappings

#### [vault.logs](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/logs/README.md)

* [list](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/logs/README.md#list) - Get all consumer request logs

#### [vault.sessions](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/sessions/README.md)

* [create](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/sessions/README.md#create) - Create Session

#### [vault.validate_connection](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/validateconnection/README.md)

* [state](https://github.com/apideck-libraries/sdk-python-pack/blob/master/docs/sdks/validateconnection/README.md#state) - Validate Connection State

</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start Pagination [pagination] -->
## Pagination

Some of the endpoints in this SDK support pagination. To use pagination, you make your SDK calls as usual, but the
returned response object will have a `Next` method that can be called to pull down the next group of results. If the
return value of `Next` is `None`, then there are no more pages to be fetched.

Here's an example of one such pagination call:
```python
from apideck_accounting_unify import Apideck
import os


with Apideck(
    api_key=os.getenv("APIDECK_API_KEY", ""),
    consumer_id="test-consumer",
    app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
) as apideck:

    res = apideck.accounting.tax_rates.list(consumer_id="test-consumer", app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX", service_id="salesforce", filter_={
        "assets": True,
        "equity": True,
        "expenses": True,
        "liabilities": True,
        "revenue": True,
    }, pass_through={
        "search": "San Francisco",
    }, fields="id,updated_at")

    while res is not None:
        # Handle items

        res = res.next()

```
<!-- End Pagination [pagination] -->

<!-- Start File uploads [file-upload] -->
## File uploads

Certain SDK methods accept file objects as part of a request body or multi-part request. It is possible and typically recommended to upload files as a stream rather than reading the entire contents into memory. This avoids excessive memory consumption and potentially crashing with out-of-memory errors when working with very large files. The following example demonstrates how to attach a file stream to a request.

> [!TIP]
>
> For endpoints that handle file uploads bytes arrays can also be used. However, using streams is recommended for large files.
>

```python
import apideck_accounting_unify
from apideck_accounting_unify import Apideck
import os


with Apideck(
    api_key=os.getenv("APIDECK_API_KEY", ""),
    consumer_id="test-consumer",
    app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
) as apideck:

    res = apideck.accounting.attachments.upload(reference_type=apideck_accounting_unify.AttachmentReferenceType.INVOICE, reference_id="123456", request_body=open("example.file", "rb"), x_apideck_metadata="{\"name\":\"document.pdf\",\"description\":\"Invoice attachment\"}", consumer_id="test-consumer", app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX", service_id="salesforce")

    assert res.create_attachment_response is not None

    # Handle response
    print(res.create_attachment_response)

```
<!-- End File uploads [file-upload] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
from apideck_accounting_unify import Apideck
from apideck_accounting_unify.utils import BackoffStrategy, RetryConfig
import os


with Apideck(
    api_key=os.getenv("APIDECK_API_KEY", ""),
    consumer_id="test-consumer",
    app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
) as apideck:

    res = apideck.accounting.tax_rates.list(consumer_id="test-consumer", app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX", service_id="salesforce", filter_={
        "assets": True,
        "equity": True,
        "expenses": True,
        "liabilities": True,
        "revenue": True,
    }, pass_through={
        "search": "San Francisco",
    }, fields="id,updated_at",
        RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

    while res is not None:
        # Handle items

        res = res.next()

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
from apideck_accounting_unify import Apideck
from apideck_accounting_unify.utils import BackoffStrategy, RetryConfig
import os


with Apideck(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    api_key=os.getenv("APIDECK_API_KEY", ""),
    consumer_id="test-consumer",
    app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
) as apideck:

    res = apideck.accounting.tax_rates.list(consumer_id="test-consumer", app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX", service_id="salesforce", filter_={
        "assets": True,
        "equity": True,
        "expenses": True,
        "liabilities": True,
        "revenue": True,
    }, pass_through={
        "search": "San Francisco",
    }, fields="id,updated_at")

    while res is not None:
        # Handle items

        res = res.next()

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

Handling errors in this SDK should largely match your expectations. All operations return a response object or raise an exception.

By default, an API error will raise a models.APIError exception, which has the following properties:

| Property        | Type             | Description           |
|-----------------|------------------|-----------------------|
| `.status_code`  | *int*            | The HTTP status code  |
| `.message`      | *str*            | The error message     |
| `.raw_response` | *httpx.Response* | The raw HTTP response |
| `.body`         | *str*            | The response content  |

When custom error responses are specified for an operation, the SDK may also raise their associated exceptions. You can refer to respective *Errors* tables in SDK docs for more details on possible exception types for each operation. For example, the `list_async` method may raise the following exceptions:

| Error Type                     | Status Code | Content Type     |
| ------------------------------ | ----------- | ---------------- |
| models.BadRequestResponse      | 400         | application/json |
| models.UnauthorizedResponse    | 401         | application/json |
| models.PaymentRequiredResponse | 402         | application/json |
| models.NotFoundResponse        | 404         | application/json |
| models.UnprocessableResponse   | 422         | application/json |
| models.APIError                | 4XX, 5XX    | \*/\*            |

### Example

```python
from apideck_accounting_unify import Apideck, models
import os


with Apideck(
    api_key=os.getenv("APIDECK_API_KEY", ""),
    consumer_id="test-consumer",
    app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
) as apideck:
    res = None
    try:

        res = apideck.accounting.tax_rates.list(consumer_id="test-consumer", app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX", service_id="salesforce", filter_={
            "assets": True,
            "equity": True,
            "expenses": True,
            "liabilities": True,
            "revenue": True,
        }, pass_through={
            "search": "San Francisco",
        }, fields="id,updated_at")

        while res is not None:
            # Handle items

            res = res.next()

    except models.BadRequestResponse as e:
        # handle e.data: models.BadRequestResponseData
        raise(e)
    except models.UnauthorizedResponse as e:
        # handle e.data: models.UnauthorizedResponseData
        raise(e)
    except models.PaymentRequiredResponse as e:
        # handle e.data: models.PaymentRequiredResponseData
        raise(e)
    except models.NotFoundResponse as e:
        # handle e.data: models.NotFoundResponseData
        raise(e)
    except models.UnprocessableResponse as e:
        # handle e.data: models.UnprocessableResponseData
        raise(e)
    except models.APIError as e:
        # handle exception
        raise(e)
```
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Override Server URL Per-Client

The default server can be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
from apideck_accounting_unify import Apideck
import os


with Apideck(
    server_url="https://unify.apideck.com",
    api_key=os.getenv("APIDECK_API_KEY", ""),
    consumer_id="test-consumer",
    app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
) as apideck:

    res = apideck.accounting.tax_rates.list(consumer_id="test-consumer", app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX", service_id="salesforce", filter_={
        "assets": True,
        "equity": True,
        "expenses": True,
        "liabilities": True,
        "revenue": True,
    }, pass_through={
        "search": "San Francisco",
    }, fields="id,updated_at")

    while res is not None:
        # Handle items

        res = res.next()

```

### Override Server URL Per-Operation

The server URL can also be overridden on a per-operation basis, provided a server list was specified for the operation. For example:
```python
import apideck_accounting_unify
from apideck_accounting_unify import Apideck
import os


with Apideck(
    api_key=os.getenv("APIDECK_API_KEY", ""),
    consumer_id="test-consumer",
    app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
) as apideck:

    res = apideck.accounting.attachments.upload(reference_type=apideck_accounting_unify.AttachmentReferenceType.INVOICE, reference_id="123456", request_body=open("example.file", "rb"), x_apideck_metadata="{\"name\":\"document.pdf\",\"description\":\"Invoice attachment\"}", consumer_id="test-consumer", app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX", service_id="salesforce", server_url="https://upload.apideck.com")

    assert res.create_attachment_response is not None

    # Handle response
    print(res.create_attachment_response)

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from apideck_accounting_unify import Apideck
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Apideck(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from apideck_accounting_unify import Apideck
from apideck_accounting_unify.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = Apideck(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Resource Management [resource-management] -->
## Resource Management

The `Apideck` class implements the context manager protocol and registers a finalizer function to close the underlying sync and async HTTPX clients it uses under the hood. This will close HTTP connections, release memory and free up other resources held by the SDK. In short-lived Python programs and notebooks that make a few SDK method calls, resource management may not be a concern. However, in longer-lived programs, it is beneficial to create a single SDK instance via a [context manager][context-manager] and reuse it across the application.

[context-manager]: https://docs.python.org/3/reference/datamodel.html#context-managers

```python
from apideck_accounting_unify import Apideck
import os
def main():

    with Apideck(
        api_key=os.getenv("APIDECK_API_KEY", ""),
        consumer_id="test-consumer",
        app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
    ) as apideck:
        # Rest of application here...


# Or when using async:
async def amain():

    async with Apideck(
        api_key=os.getenv("APIDECK_API_KEY", ""),
        consumer_id="test-consumer",
        app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
    ) as apideck:
        # Rest of application here...
```
<!-- End Resource Management [resource-management] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
```python
from apideck_accounting_unify import Apideck
import logging

logging.basicConfig(level=logging.DEBUG)
s = Apideck(debug_logger=logging.getLogger("apideck_accounting_unify"))
```

You can also enable a default debug logger by setting an environment variable `APIDECK_DEBUG` to true.
<!-- End Debugging [debug] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically. Any manual changes added to internal files will be overwritten on the next generation. 
We look forward to hearing your feedback. Feel free to open a PR or an issue with a proof of concept and we'll do our best to include it in a future release. 

### SDK Created by [Speakeasy](https://www.speakeasy.com/?utm_source=apideck-accounting-unify&utm_campaign=python)
