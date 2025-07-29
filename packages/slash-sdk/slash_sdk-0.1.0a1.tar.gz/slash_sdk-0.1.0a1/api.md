# LegalEntity

Types:

```python
from slash_sdk.types import PaginationResponse, LegalEntityListResponse
```

Methods:

- <code title="get /legal-entity">client.legal_entity.<a href="./src/slash_sdk/resources/legal_entity.py">list</a>() -> <a href="./src/slash_sdk/types/legal_entity_list_response.py">LegalEntityListResponse</a></code>

# Account

Types:

```python
from slash_sdk.types import Account, AccountListResponse, AccountRetrieveBalanceResponse
```

Methods:

- <code title="get /account/{accountId}">client.account.<a href="./src/slash_sdk/resources/account.py">retrieve</a>(account_id) -> <a href="./src/slash_sdk/types/account.py">Account</a></code>
- <code title="get /account">client.account.<a href="./src/slash_sdk/resources/account.py">list</a>(\*\*<a href="src/slash_sdk/types/account_list_params.py">params</a>) -> <a href="./src/slash_sdk/types/account_list_response.py">AccountListResponse</a></code>
- <code title="get /account/{accountId}/balance">client.account.<a href="./src/slash_sdk/resources/account.py">retrieve_balance</a>(account_id) -> <a href="./src/slash_sdk/types/account_retrieve_balance_response.py">AccountRetrieveBalanceResponse</a></code>

# VirtualAccount

Types:

```python
from slash_sdk.types import (
    CommissionDetails,
    CommissionRule,
    Money,
    VirtualAccount,
    VirtualAccountModel,
    VirtualAccountCreateResponse,
    VirtualAccountUpdateResponse,
    VirtualAccountListResponse,
)
```

Methods:

- <code title="post /virtual-account">client.virtual_account.<a href="./src/slash_sdk/resources/virtual_account.py">create</a>(\*\*<a href="src/slash_sdk/types/virtual_account_create_params.py">params</a>) -> <a href="./src/slash_sdk/types/virtual_account_create_response.py">VirtualAccountCreateResponse</a></code>
- <code title="get /virtual-account/{virtualAccountId}">client.virtual_account.<a href="./src/slash_sdk/resources/virtual_account.py">retrieve</a>(virtual_account_id) -> <a href="./src/slash_sdk/types/virtual_account.py">VirtualAccount</a></code>
- <code title="patch /virtual-account/{virtualAccountId}">client.virtual_account.<a href="./src/slash_sdk/resources/virtual_account.py">update</a>(virtual_account_id, \*\*<a href="src/slash_sdk/types/virtual_account_update_params.py">params</a>) -> <a href="./src/slash_sdk/types/virtual_account_update_response.py">VirtualAccountUpdateResponse</a></code>
- <code title="get /virtual-account">client.virtual_account.<a href="./src/slash_sdk/resources/virtual_account.py">list</a>(\*\*<a href="src/slash_sdk/types/virtual_account_list_params.py">params</a>) -> <a href="./src/slash_sdk/types/virtual_account_list_response.py">VirtualAccountListResponse</a></code>

# Transaction

Types:

```python
from slash_sdk.types import (
    Transaction,
    TransactionListResponse,
    TransactionAggregateResponse,
    TransactionRetrieveFeeDetailsResponse,
    TransactionUpdateNoteResponse,
)
```

Methods:

- <code title="get /transaction/{transactionId}">client.transaction.<a href="./src/slash_sdk/resources/transaction.py">retrieve</a>(transaction_id) -> <a href="./src/slash_sdk/types/transaction.py">Transaction</a></code>
- <code title="get /transaction">client.transaction.<a href="./src/slash_sdk/resources/transaction.py">list</a>(\*\*<a href="src/slash_sdk/types/transaction_list_params.py">params</a>) -> <a href="./src/slash_sdk/types/transaction_list_response.py">TransactionListResponse</a></code>
- <code title="get /transaction/aggregation">client.transaction.<a href="./src/slash_sdk/resources/transaction.py">aggregate</a>(\*\*<a href="src/slash_sdk/types/transaction_aggregate_params.py">params</a>) -> <a href="./src/slash_sdk/types/transaction_aggregate_response.py">TransactionAggregateResponse</a></code>
- <code title="get /transaction/{transactionId}/fee-details">client.transaction.<a href="./src/slash_sdk/resources/transaction.py">retrieve_fee_details</a>(transaction_id) -> <a href="./src/slash_sdk/types/transaction_retrieve_fee_details_response.py">TransactionRetrieveFeeDetailsResponse</a></code>
- <code title="patch /transaction/{transactionId}/note">client.transaction.<a href="./src/slash_sdk/resources/transaction.py">update_note</a>(transaction_id, \*\*<a href="src/slash_sdk/types/transaction_update_note_params.py">params</a>) -> <a href="./src/slash_sdk/types/transaction_update_note_response.py">TransactionUpdateNoteResponse</a></code>

# Transfer

Types:

```python
from slash_sdk.types import TransferCreateVirtualAccountTransferResponse
```

Methods:

- <code title="post /transfer/virtual-account">client.transfer.<a href="./src/slash_sdk/resources/transfer.py">create_virtual_account_transfer</a>(\*\*<a href="src/slash_sdk/types/transfer_create_virtual_account_transfer_params.py">params</a>) -> <a href="./src/slash_sdk/types/transfer_create_virtual_account_transfer_response.py">TransferCreateVirtualAccountTransferResponse</a></code>

# Card

Types:

```python
from slash_sdk.types import Card, CardGroupUtilization, CardStatus, CardListResponse
```

Methods:

- <code title="post /card">client.card.<a href="./src/slash_sdk/resources/card/card.py">create</a>(\*\*<a href="src/slash_sdk/types/card_create_params.py">params</a>) -> <a href="./src/slash_sdk/types/card/card.py">Card</a></code>
- <code title="get /card/{cardId}">client.card.<a href="./src/slash_sdk/resources/card/card.py">retrieve</a>(card_id, \*\*<a href="src/slash_sdk/types/card_retrieve_params.py">params</a>) -> <a href="./src/slash_sdk/types/card/card.py">Card</a></code>
- <code title="patch /card/{cardId}">client.card.<a href="./src/slash_sdk/resources/card/card.py">update</a>(card_id, \*\*<a href="src/slash_sdk/types/card_update_params.py">params</a>) -> <a href="./src/slash_sdk/types/card/card.py">Card</a></code>
- <code title="get /card">client.card.<a href="./src/slash_sdk/resources/card/card.py">list</a>(\*\*<a href="src/slash_sdk/types/card_list_params.py">params</a>) -> <a href="./src/slash_sdk/types/card_list_response.py">CardListResponse</a></code>
- <code title="get /card/{cardId}/utilization">client.card.<a href="./src/slash_sdk/resources/card/card.py">get_utilization</a>(card_id) -> <a href="./src/slash_sdk/types/card_group_utilization.py">CardGroupUtilization</a></code>

## SpendingConstraint

Types:

```python
from slash_sdk.types.card import PartialSpendingConstraint, Restriction, SpendingConstraint
```

Methods:

- <code title="put /card/{cardId}/spending-constraint">client.card.spending_constraint.<a href="./src/slash_sdk/resources/card/spending_constraint.py">update_full</a>(card_id, \*\*<a href="src/slash_sdk/types/card/spending_constraint_update_full_params.py">params</a>) -> <a href="./src/slash_sdk/types/card/spending_constraint.py">SpendingConstraint</a></code>
- <code title="patch /card/{cardId}/spending-constraint">client.card.spending_constraint.<a href="./src/slash_sdk/resources/card/spending_constraint.py">update_partial</a>(card_id, \*\*<a href="src/slash_sdk/types/card/spending_constraint_update_partial_params.py">params</a>) -> <a href="./src/slash_sdk/types/card/spending_constraint.py">SpendingConstraint</a></code>

# CardGroup

Types:

```python
from slash_sdk.types import CardGroup, CardGroupListResponse
```

Methods:

- <code title="post /card-group">client.card_group.<a href="./src/slash_sdk/resources/card_group/card_group.py">create</a>(\*\*<a href="src/slash_sdk/types/card_group_create_params.py">params</a>) -> <a href="./src/slash_sdk/types/card_group/card_group.py">CardGroup</a></code>
- <code title="get /card-group/{cardGroupId}">client.card_group.<a href="./src/slash_sdk/resources/card_group/card_group.py">retrieve</a>(card_group_id) -> <a href="./src/slash_sdk/types/card_group/card_group.py">CardGroup</a></code>
- <code title="patch /card-group/{cardGroupId}">client.card_group.<a href="./src/slash_sdk/resources/card_group/card_group.py">update</a>(card_group_id, \*\*<a href="src/slash_sdk/types/card_group_update_params.py">params</a>) -> <a href="./src/slash_sdk/types/card_group/card_group.py">CardGroup</a></code>
- <code title="get /card-group">client.card_group.<a href="./src/slash_sdk/resources/card_group/card_group.py">list</a>(\*\*<a href="src/slash_sdk/types/card_group_list_params.py">params</a>) -> <a href="./src/slash_sdk/types/card_group_list_response.py">CardGroupListResponse</a></code>
- <code title="get /card-group/{cardGroupId}/utilization">client.card_group.<a href="./src/slash_sdk/resources/card_group/card_group.py">get_utilization</a>(card_group_id) -> <a href="./src/slash_sdk/types/card_group_utilization.py">CardGroupUtilization</a></code>

## SpendingConstraint

Methods:

- <code title="put /card-group/{cardGroupId}/spending-constraint">client.card_group.spending_constraint.<a href="./src/slash_sdk/resources/card_group/spending_constraint.py">update_full</a>(card_group_id, \*\*<a href="src/slash_sdk/types/card_group/spending_constraint_update_full_params.py">params</a>) -> <a href="./src/slash_sdk/types/card/spending_constraint.py">SpendingConstraint</a></code>
- <code title="patch /card-group/{cardGroupId}/spending-constraint">client.card_group.spending_constraint.<a href="./src/slash_sdk/resources/card_group/spending_constraint.py">update_partial</a>(card_group_id, \*\*<a href="src/slash_sdk/types/card_group/spending_constraint_update_partial_params.py">params</a>) -> <a href="./src/slash_sdk/types/card/spending_constraint.py">SpendingConstraint</a></code>

# CardProduct

Types:

```python
from slash_sdk.types import CardProductListResponse
```

Methods:

- <code title="get /card-product">client.card_product.<a href="./src/slash_sdk/resources/card_product.py">list</a>(\*\*<a href="src/slash_sdk/types/card_product_list_params.py">params</a>) -> <a href="./src/slash_sdk/types/card_product_list_response.py">CardProductListResponse</a></code>

# SlashHandle

Types:

```python
from slash_sdk.types import SlashHandleListResponse
```

Methods:

- <code title="get /slash-handle">client.slash_handle.<a href="./src/slash_sdk/resources/slash_handle.py">list</a>(\*\*<a href="src/slash_sdk/types/slash_handle_list_params.py">params</a>) -> <a href="./src/slash_sdk/types/slash_handle_list_response.py">SlashHandleListResponse</a></code>

# Pay

Types:

```python
from slash_sdk.types import SlashHandle, PaySendResponse
```

Methods:

- <code title="get /pay">client.pay.<a href="./src/slash_sdk/resources/pay.py">retrieve</a>() -> <a href="./src/slash_sdk/types/slash_handle.py">SlashHandle</a></code>
- <code title="post /pay">client.pay.<a href="./src/slash_sdk/resources/pay.py">send</a>(\*\*<a href="src/slash_sdk/types/pay_send_params.py">params</a>) -> <a href="./src/slash_sdk/types/pay_send_response.py">PaySendResponse</a></code>

# Webhook

Types:

```python
from slash_sdk.types import Webhook, WebhookListResponse
```

Methods:

- <code title="post /webhook">client.webhook.<a href="./src/slash_sdk/resources/webhook.py">create</a>(\*\*<a href="src/slash_sdk/types/webhook_create_params.py">params</a>) -> <a href="./src/slash_sdk/types/webhook.py">Webhook</a></code>
- <code title="patch /webhook/{webhookId}">client.webhook.<a href="./src/slash_sdk/resources/webhook.py">update</a>(webhook_id, \*\*<a href="src/slash_sdk/types/webhook_update_params.py">params</a>) -> <a href="./src/slash_sdk/types/webhook.py">Webhook</a></code>
- <code title="get /webhook">client.webhook.<a href="./src/slash_sdk/resources/webhook.py">list</a>(\*\*<a href="src/slash_sdk/types/webhook_list_params.py">params</a>) -> <a href="./src/slash_sdk/types/webhook_list_response.py">WebhookListResponse</a></code>

# Merchant

Types:

```python
from slash_sdk.types import Merchant, MerchantListResponse
```

Methods:

- <code title="get /merchant/{merchantId}">client.merchant.<a href="./src/slash_sdk/resources/merchant.py">retrieve</a>(merchant_id) -> <a href="./src/slash_sdk/types/merchant.py">Merchant</a></code>
- <code title="get /merchant">client.merchant.<a href="./src/slash_sdk/resources/merchant.py">list</a>(\*\*<a href="src/slash_sdk/types/merchant_list_params.py">params</a>) -> <a href="./src/slash_sdk/types/merchant_list_response.py">MerchantListResponse</a></code>

# MerchantCategory

Types:

```python
from slash_sdk.types import MerchantCategoryListResponse
```

Methods:

- <code title="get /merchant-category">client.merchant_category.<a href="./src/slash_sdk/resources/merchant_category.py">list</a>(\*\*<a href="src/slash_sdk/types/merchant_category_list_params.py">params</a>) -> <a href="./src/slash_sdk/types/merchant_category_list_response.py">MerchantCategoryListResponse</a></code>

# DeveloperAccount

Types:

```python
from slash_sdk.types import (
    DeveloperApplicationData,
    DeveloperApplicationModel,
    DeveloperApplicationType,
)
```

Methods:

- <code title="post /developer-account/{developerAccountId}/application">client.developer_account.<a href="./src/slash_sdk/resources/developer_account.py">create_application</a>(developer_account_id, \*\*<a href="src/slash_sdk/types/developer_account_create_application_params.py">params</a>) -> <a href="./src/slash_sdk/types/developer_application_model.py">DeveloperApplicationModel</a></code>

# DeveloperApplication

Methods:

- <code title="get /developer-application/{developerApplicationId}">client.developer_application.<a href="./src/slash_sdk/resources/developer_application.py">retrieve</a>(developer_application_id) -> <a href="./src/slash_sdk/types/developer_application_model.py">DeveloperApplicationModel</a></code>
- <code title="patch /developer-application/{developerApplicationId}">client.developer_application.<a href="./src/slash_sdk/resources/developer_application.py">update</a>(developer_application_id, \*\*<a href="src/slash_sdk/types/developer_application_update_params.py">params</a>) -> <a href="./src/slash_sdk/types/developer_application_model.py">DeveloperApplicationModel</a></code>
- <code title="post /developer-application/{developerApplicationId}/secret">client.developer_application.<a href="./src/slash_sdk/resources/developer_application.py">create_or_regenerate_secret</a>(developer_application_id) -> <a href="./src/slash_sdk/types/developer_application_model.py">DeveloperApplicationModel</a></code>

# WellKnown

Types:

```python
from slash_sdk.types import WellKnownRetrieveOpenidConfigurationResponse
```

Methods:

- <code title="get /.well-known/openid-configuration">client.well_known.<a href="./src/slash_sdk/resources/well_known.py">retrieve_openid_configuration</a>() -> <a href="./src/slash_sdk/types/well_known_retrieve_openid_configuration_response.py">WellKnownRetrieveOpenidConfigurationResponse</a></code>

# Oauth2

Types:

```python
from slash_sdk.types import Oauth2GetTokenResponse
```

Methods:

- <code title="post /oauth2/token">client.oauth2.<a href="./src/slash_sdk/resources/oauth2/oauth2.py">get_token</a>(\*\*<a href="src/slash_sdk/types/oauth2_get_token_params.py">params</a>) -> <a href="./src/slash_sdk/types/oauth2_get_token_response.py">Oauth2GetTokenResponse</a></code>

## Userinfo

Types:

```python
from slash_sdk.types.oauth2 import UserInfo
```

Methods:

- <code title="get /oauth2/userinfo">client.oauth2.userinfo.<a href="./src/slash_sdk/resources/oauth2/userinfo.py">retrieve</a>() -> <a href="./src/slash_sdk/types/oauth2/user_info.py">UserInfo</a></code>
- <code title="post /oauth2/userinfo">client.oauth2.userinfo.<a href="./src/slash_sdk/resources/oauth2/userinfo.py">submit</a>() -> <a href="./src/slash_sdk/types/oauth2/user_info.py">UserInfo</a></code>

# Fdx

## Customers

Types:

```python
from slash_sdk.types.fdx import CustomerRetrieveCurrentResponse
```

Methods:

- <code title="get /fdx/customers/current">client.fdx.customers.<a href="./src/slash_sdk/resources/fdx/customers.py">retrieve_current</a>() -> <a href="./src/slash_sdk/types/fdx/customer_retrieve_current_response.py">CustomerRetrieveCurrentResponse</a></code>

## Accounts

Types:

```python
from slash_sdk.types.fdx import (
    DepositAccount,
    InvestmentAccount,
    LineOfCreditAccount,
    LoanAccount,
    AccountRetrieveResponse,
    AccountListResponse,
    AccountListTransactionsResponse,
    AccountRetrieveContactResponse,
    AccountRetrievePaymentNetworksResponse,
)
```

Methods:

- <code title="get /fdx/accounts/{accountId}">client.fdx.accounts.<a href="./src/slash_sdk/resources/fdx/accounts/accounts.py">retrieve</a>(account_id) -> <a href="./src/slash_sdk/types/fdx/account_retrieve_response.py">AccountRetrieveResponse</a></code>
- <code title="get /fdx/accounts">client.fdx.accounts.<a href="./src/slash_sdk/resources/fdx/accounts/accounts.py">list</a>(\*\*<a href="src/slash_sdk/types/fdx/account_list_params.py">params</a>) -> <a href="./src/slash_sdk/types/fdx/account_list_response.py">AccountListResponse</a></code>
- <code title="get /fdx/accounts/{accountId}/transactions">client.fdx.accounts.<a href="./src/slash_sdk/resources/fdx/accounts/accounts.py">list_transactions</a>(account_id, \*\*<a href="src/slash_sdk/types/fdx/account_list_transactions_params.py">params</a>) -> <a href="./src/slash_sdk/types/fdx/account_list_transactions_response.py">AccountListTransactionsResponse</a></code>
- <code title="get /fdx/accounts/{accountId}/contact">client.fdx.accounts.<a href="./src/slash_sdk/resources/fdx/accounts/accounts.py">retrieve_contact</a>(account_id) -> <a href="./src/slash_sdk/types/fdx/account_retrieve_contact_response.py">AccountRetrieveContactResponse</a></code>
- <code title="get /fdx/accounts/{accountId}/payment-networks">client.fdx.accounts.<a href="./src/slash_sdk/resources/fdx/accounts/accounts.py">retrieve_payment_networks</a>(account_id, \*\*<a href="src/slash_sdk/types/fdx/account_retrieve_payment_networks_params.py">params</a>) -> <a href="./src/slash_sdk/types/fdx/account_retrieve_payment_networks_response.py">AccountRetrievePaymentNetworksResponse</a></code>

### Statements

Types:

```python
from slash_sdk.types.fdx.accounts import StatementListResponse
```

Methods:

- <code title="get /fdx/accounts/{accountId}/statements">client.fdx.accounts.statements.<a href="./src/slash_sdk/resources/fdx/accounts/statements.py">list</a>(account_id, \*\*<a href="src/slash_sdk/types/fdx/accounts/statement_list_params.py">params</a>) -> <a href="./src/slash_sdk/types/fdx/accounts/statement_list_response.py">StatementListResponse</a></code>
- <code title="get /fdx/accounts/{accountId}/statements/{statementId}">client.fdx.accounts.statements.<a href="./src/slash_sdk/resources/fdx/accounts/statements.py">retrieve_pdf</a>(statement_id, \*, account_id) -> BinaryAPIResponse</code>

# Crypto

Types:

```python
from slash_sdk.types import CryptoCreateOfframpResponse
```

Methods:

- <code title="post /crypto/offramp">client.crypto.<a href="./src/slash_sdk/resources/crypto.py">create_offramp</a>(\*\*<a href="src/slash_sdk/types/crypto_create_offramp_params.py">params</a>) -> <a href="./src/slash_sdk/types/crypto_create_offramp_response.py">CryptoCreateOfframpResponse</a></code>
