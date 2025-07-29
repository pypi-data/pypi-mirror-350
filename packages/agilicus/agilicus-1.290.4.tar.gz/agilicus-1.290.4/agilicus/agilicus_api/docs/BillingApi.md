# agilicus_api.BillingApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_billing_usage_record**](BillingApi.md#add_billing_usage_record) | **POST** /v1/billing_accounts/{billing_account_id}/usage_records | Add usage records for a billing account
[**add_customer_balance_transaction**](BillingApi.md#add_customer_balance_transaction) | **POST** /v1/billing_accounts/{billing_account_id}/balance_transactions | Add a customer balance transaction
[**add_org_to_billing_account**](BillingApi.md#add_org_to_billing_account) | **POST** /v1/billing_accounts/{billing_account_id}/orgs | Add an org to a billing account
[**add_org_to_billing_subscription**](BillingApi.md#add_org_to_billing_subscription) | **POST** /v1/billing_subscriptions/{billing_subscription_id}/orgs | Add an org to a billing subscription
[**add_subscription_balance_transaction**](BillingApi.md#add_subscription_balance_transaction) | **POST** /v1/billing_subscriptions/{billing_subscription_id}/balance_transactions | Add a subscription balance transaction
[**create_billing_account**](BillingApi.md#create_billing_account) | **POST** /v1/billing_accounts | Create a billing account
[**create_feature**](BillingApi.md#create_feature) | **POST** /v1/features | create a feature
[**create_product**](BillingApi.md#create_product) | **POST** /v1/products | Create a product
[**create_subscription**](BillingApi.md#create_subscription) | **POST** /v1/billing_subscriptions | Create a billing subscription
[**delete_billing_account**](BillingApi.md#delete_billing_account) | **DELETE** /v1/billing_accounts/{billing_account_id} | Delete a billing account
[**delete_feature**](BillingApi.md#delete_feature) | **DELETE** /v1/features/{feature_id} | Delete a feature
[**delete_product**](BillingApi.md#delete_product) | **DELETE** /v1/products/{product_id} | Delete a product
[**delete_subscription**](BillingApi.md#delete_subscription) | **DELETE** /v1/billing_subscriptions/{billing_subscription_id} | Delete a billing subscription
[**get_billing_account**](BillingApi.md#get_billing_account) | **GET** /v1/billing_accounts/{billing_account_id} | Get a single billing account
[**get_billing_account_orgs**](BillingApi.md#get_billing_account_orgs) | **GET** /v1/billing_accounts/{billing_account_id}/orgs | Get all orgs in a billing account
[**get_billing_subscription_orgs**](BillingApi.md#get_billing_subscription_orgs) | **GET** /v1/billing_subscriptions/{billing_subscription_id}/orgs | Get all orgs in a billing subscription
[**get_customer_balance_transactions**](BillingApi.md#get_customer_balance_transactions) | **GET** /v1/billing_accounts/{billing_account_id}/balance_transactions | Get the customers balance transactions
[**get_feature**](BillingApi.md#get_feature) | **GET** /v1/features/{feature_id} | Get a feature by id
[**get_product**](BillingApi.md#get_product) | **GET** /v1/products/{product_id} | Get a single product
[**get_subscription**](BillingApi.md#get_subscription) | **GET** /v1/billing_subscriptions/{billing_subscription_id} | Get a single billing subscription
[**get_subscription_balance_transactions**](BillingApi.md#get_subscription_balance_transactions) | **GET** /v1/billing_subscriptions/{billing_subscription_id}/balance_transactions | Get the subscription balance transactions
[**get_usage_records**](BillingApi.md#get_usage_records) | **GET** /v1/billing_accounts/{billing_account_id}/usage_records | Get all subscription usage records
[**list_billing_accounts**](BillingApi.md#list_billing_accounts) | **GET** /v1/billing_accounts | Get all billing accounts
[**list_checkout_sessions**](BillingApi.md#list_checkout_sessions) | **GET** /v1/billing_accounts/{billing_account_id}/checkout | list checkout sessions
[**list_features**](BillingApi.md#list_features) | **GET** /v1/features | Get all features
[**list_products**](BillingApi.md#list_products) | **GET** /v1/products | Get all products
[**list_subscription_features**](BillingApi.md#list_subscription_features) | **GET** /v1/billing_subscriptions/{billing_subscription_id}/features | Get all subscription features
[**list_subscriptions**](BillingApi.md#list_subscriptions) | **GET** /v1/billing_subscriptions | Get all billing subscriptions for a billing account
[**list_subscriptions_with_feature**](BillingApi.md#list_subscriptions_with_feature) | **GET** /v1/features/{feature_id}/subscriptions | Get all subscriptions using feature_id
[**new_subscription**](BillingApi.md#new_subscription) | **POST** /v1/billing_subscriptions/{billing_subscription_id}/new_subscription | Create a new upstream subscription
[**remove_org_from_billing_account**](BillingApi.md#remove_org_from_billing_account) | **DELETE** /v1/billing_accounts/{billing_account_id}/orgs/{org_id} | Remove an org from a billing account
[**remove_org_from_billing_subscription**](BillingApi.md#remove_org_from_billing_subscription) | **DELETE** /v1/billing_subscriptions/{billing_subscription_id}/orgs/{org_id} | Remove an org from a billing subscription
[**replace_billing_account**](BillingApi.md#replace_billing_account) | **PUT** /v1/billing_accounts/{billing_account_id} | Create or update a billing account
[**replace_feature**](BillingApi.md#replace_feature) | **PUT** /v1/features/{feature_id} | update a Feature
[**replace_product**](BillingApi.md#replace_product) | **PUT** /v1/products/{product_id} | Create or update a product
[**replace_subscription**](BillingApi.md#replace_subscription) | **PUT** /v1/billing_subscriptions/{billing_subscription_id} | Create or update a billing subscription
[**update_subscription_cancellation**](BillingApi.md#update_subscription_cancellation) | **POST** /v1/billing_subscriptions/{billing_subscription_id}/cancel | Update the subscription cancellation detail


# **add_billing_usage_record**
> CreateBillingUsageRecords add_billing_usage_record(billing_account_id)

Add usage records for a billing account

Add usage records for a billing account

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.create_billing_usage_records import CreateBillingUsageRecords
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_account_id = "1234" # str | Billing account Unique identifier
    create_billing_usage_records = CreateBillingUsageRecords(
        dry_run=False,
        usage_records=[
            BillingUsageRecord(
                dry_run=False,
            ),
        ],
    ) # CreateBillingUsageRecords |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Add usage records for a billing account
        api_response = api_instance.add_billing_usage_record(billing_account_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->add_billing_usage_record: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Add usage records for a billing account
        api_response = api_instance.add_billing_usage_record(billing_account_id, create_billing_usage_records=create_billing_usage_records)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->add_billing_usage_record: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account_id** | **str**| Billing account Unique identifier |
 **create_billing_usage_records** | [**CreateBillingUsageRecords**](CreateBillingUsageRecords.md)|  | [optional]

### Return type

[**CreateBillingUsageRecords**](CreateBillingUsageRecords.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Usage records created. |  -  |
**204** | No usage records created. This is due to either no subscriptions found for the customer or no active resources found.  |  -  |
**400** | Error creating usage records |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_customer_balance_transaction**
> BillingBalanceTransaction add_customer_balance_transaction(billing_account_id)

Add a customer balance transaction

Add a customer balance transaction

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.billing_balance_transaction import BillingBalanceTransaction
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_account_id = "1234" # str | Billing account Unique identifier
    billing_balance_transaction = BillingBalanceTransaction(
        amount=1,
        description="description_example",
        currency="currency_example",
    ) # BillingBalanceTransaction |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Add a customer balance transaction
        api_response = api_instance.add_customer_balance_transaction(billing_account_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->add_customer_balance_transaction: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Add a customer balance transaction
        api_response = api_instance.add_customer_balance_transaction(billing_account_id, billing_balance_transaction=billing_balance_transaction)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->add_customer_balance_transaction: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account_id** | **str**| Billing account Unique identifier |
 **billing_balance_transaction** | [**BillingBalanceTransaction**](BillingBalanceTransaction.md)|  | [optional]

### Return type

[**BillingBalanceTransaction**](BillingBalanceTransaction.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | BillingBalanceTransaction added |  -  |
**404** | BillingAccount |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_org_to_billing_account**
> Organisation add_org_to_billing_account(billing_account_id)

Add an org to a billing account

Add an org to a billing account

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.organisation import Organisation
from agilicus_api.model.billing_org import BillingOrg
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_account_id = "1234" # str | Billing account Unique identifier
    billing_org = BillingOrg(
        cascade=False,
    ) # BillingOrg |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Add an org to a billing account
        api_response = api_instance.add_org_to_billing_account(billing_account_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->add_org_to_billing_account: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Add an org to a billing account
        api_response = api_instance.add_org_to_billing_account(billing_account_id, billing_org=billing_org)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->add_org_to_billing_account: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account_id** | **str**| Billing account Unique identifier |
 **billing_org** | [**BillingOrg**](BillingOrg.md)|  | [optional]

### Return type

[**Organisation**](Organisation.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Org added to billing account |  -  |
**404** | BillingAccount or Organisation does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_org_to_billing_subscription**
> Organisation add_org_to_billing_subscription(billing_subscription_id)

Add an org to a billing subscription

Add an org to a billing subscription

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.organisation import Organisation
from agilicus_api.model.billing_org import BillingOrg
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_subscription_id = "1234" # str | Billing subscription Unique identifier
    billing_org = BillingOrg(
        cascade=False,
    ) # BillingOrg |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Add an org to a billing subscription
        api_response = api_instance.add_org_to_billing_subscription(billing_subscription_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->add_org_to_billing_subscription: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Add an org to a billing subscription
        api_response = api_instance.add_org_to_billing_subscription(billing_subscription_id, billing_org=billing_org)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->add_org_to_billing_subscription: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_subscription_id** | **str**| Billing subscription Unique identifier |
 **billing_org** | [**BillingOrg**](BillingOrg.md)|  | [optional]

### Return type

[**Organisation**](Organisation.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Org added to billing subscription |  -  |
**404** | BillingAccount, Organisation and or subscription does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_subscription_balance_transaction**
> BillingBalanceTransaction add_subscription_balance_transaction(billing_subscription_id)

Add a subscription balance transaction

Add a subscription balance transaction

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.billing_balance_transaction import BillingBalanceTransaction
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_subscription_id = "1234" # str | Billing subscription Unique identifier
    billing_balance_transaction = BillingBalanceTransaction(
        amount=1,
        description="description_example",
        currency="currency_example",
    ) # BillingBalanceTransaction |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Add a subscription balance transaction
        api_response = api_instance.add_subscription_balance_transaction(billing_subscription_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->add_subscription_balance_transaction: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Add a subscription balance transaction
        api_response = api_instance.add_subscription_balance_transaction(billing_subscription_id, billing_balance_transaction=billing_balance_transaction)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->add_subscription_balance_transaction: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_subscription_id** | **str**| Billing subscription Unique identifier |
 **billing_balance_transaction** | [**BillingBalanceTransaction**](BillingBalanceTransaction.md)|  | [optional]

### Return type

[**BillingBalanceTransaction**](BillingBalanceTransaction.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | BillingBalanceTransaction added |  -  |
**404** | BillingAccount |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_billing_account**
> BillingAccount create_billing_account(billing_account)

Create a billing account

Create a billing account

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.billing_account import BillingAccount
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_account = BillingAccount(
        metadata=MetadataWithId(),
        spec=BillingAccountSpec(
            customer_id="123",
            product_id="123",
            dev_mode=True,
        ),
        status=BillingAccountStatus(
            orgs=[
                Organisation(
                    all_users_group_id="123",
                    all_users_all_suborgs_group_id="123",
                    all_users_direct_suborgs_group_id="123",
                    auto_created_users_group_id="123",
                    external_id="123",
                    organisation="some name",
                    issuer="app1",
                    issuer_id="123",
                    subdomain="app1.example.com",
                    name_slug=K8sSlug("81c2v7s6djuy1zmetozkhdomha1bae37b8ocvx8o53ow2eg7p6qw9qklp6l4y010fogx"),
                    contact_id="123",
                    parent_id="123",
                    root_org_id="aB29sdkD3jlaAbl7",
                    auto_create=False,
                    trust_on_first_use_duration=86400,
                    feature_flags=[
                        FeatureFlag(
                            feature="saml_auth",
                            enabled=True,
                            setting="stable",
                        ),
                    ],
                    admin_state=OrganisationStateSelector("active"),
                    status=OrganisationStatus(
                        all_up=True,
                        admin_up=True,
                        issuer_up=True,
                        current_state=OrganisationStateStatus("active"),
                        capabilities=OrganisationCapabilities(
                            features=[
                                FeatureTagName("north-america"),
                            ],
                        ),
                    ),
                    billing_account_id="123",
                    billing_subscription_id="123",
                    shard="A",
                    cluster="ca-1",
                    configured_capabilities=OrganisationCapabilities(
                        features=[
                            FeatureTagName("north-america"),
                        ],
                    ),
                    owner_config=OrganisationOwnerConfig(
                        disable_user_requests=False,
                    ),
                    product_label_override="123",
                    system_options=OrganisationSystemOptions(
                        new_subscription_feature_overrides=[
                            "123",
                        ],
                        allowed_domains=[
                            "app1.subdomain.com",
                        ],
                    ),
                    ruleset_bundle_id="123",
                    point_of_presence_id="123",
                    point_of_presence_name=FeatureTagName("north-america"),
                    region_id="123",
                ),
            ],
            subscriptions=[
                BillingSubscription(
                    id="id_example",
                ),
            ],
            customer=BillingCustomer(
                id="id_example",
                name="John Smith",
                email="john@example.com",
                balance=1,
                created=1,
                currency="currency_example",
                description="description_example",
                invoice_prefix="invoice_prefix_example",
                livemode=True,
                metadata={
                    "key": "key_example",
                },
                phone="phone_example",
            ),
            products=[
                BillingProduct(
                    id="id_example",
                    name="name_example",
                ),
            ],
            product=Product(
                metadata=MetadataWithId(),
                spec=ProductSpec(
                    name="name_example",
                    description="description_example",
                    dev_mode=True,
                    label="123",
                    billing_product_prices=[
                        BillingProductPrice(
                            id="id_example",
                        ),
                    ],
                    trial_period=25,
                    features=[
                        "123",
                    ],
                ),
                status=ProductStatus(
                    billing_product_prices=[
                        BillingProductPrice(
                            id="id_example",
                        ),
                    ],
                    features=[
                        Feature(
                            metadata=MetadataWithId(),
                            spec=FeatureSpec(
                                name="name_example",
                                description="description_example",
                                priority=1,
                                key="e",
                                value=FeatureValue(
                                    enabled=True,
                                    min=1,
                                    max=1,
                                ),
                            ),
                            status=FeatureStatus(
                                products=[
                                    Product(),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
            org_subscriptions=[
                BillingOrgSubscription(
                    metadata=MetadataWithId(),
                    spec=BillingOrgSubscriptionSpec(
                        billing_account_id="123",
                        dev_mode=True,
                        subscription_id="subscription_id_example",
                        usage_override=[
                            BillingSubscriptionUsageOverrideItem(
                                metric="metric_example",
                                min_quantity=1,
                                max_quantity=1,
                                step_size=1,
                                group_by_org=True,
                            ),
                        ],
                        feature_overrides=[
                            "123",
                        ],
                        product_id="123",
                        cancel_detail=BillingSubscriptionCancelDetail(
                            cancel_at_period_end=True,
                            cancel_at=dateutil_parser('2025-07-07T15:49:51.23+02:00'),
                            immediately=True,
                            comment="comment_example",
                            feedback="feedback_example",
                            subscription=BillingSubscription(
                                id="id_example",
                            ),
                        ),
                    ),
                    status=BillingOrgSubscriptionStatus(
                        orgs=[
                            Organisation(
                                all_users_group_id="123",
                                all_users_all_suborgs_group_id="123",
                                all_users_direct_suborgs_group_id="123",
                                auto_created_users_group_id="123",
                                external_id="123",
                                organisation="some name",
                                issuer="app1",
                                issuer_id="123",
                                subdomain="app1.example.com",
                                name_slug=K8sSlug("81c2v7s6djuy1zmetozkhdomha1bae37b8ocvx8o53ow2eg7p6qw9qklp6l4y010fogx"),
                                contact_id="123",
                                parent_id="123",
                                root_org_id="aB29sdkD3jlaAbl7",
                                auto_create=False,
                                trust_on_first_use_duration=86400,
                                feature_flags=[
                                    FeatureFlag(
                                        feature="saml_auth",
                                        enabled=True,
                                        setting="stable",
                                    ),
                                ],
                                admin_state=OrganisationStateSelector("active"),
                                status=OrganisationStatus(
                                    all_up=True,
                                    admin_up=True,
                                    issuer_up=True,
                                    current_state=OrganisationStateStatus("active"),
                                    capabilities=OrganisationCapabilities(
                                        features=[
                                            FeatureTagName("north-america"),
                                        ],
                                    ),
                                ),
                                billing_account_id="123",
                                billing_subscription_id="123",
                                shard="A",
                                cluster="ca-1",
                                configured_capabilities=OrganisationCapabilities(
                                    features=[
                                        FeatureTagName("north-america"),
                                    ],
                                ),
                                owner_config=OrganisationOwnerConfig(
                                    disable_user_requests=False,
                                ),
                                product_label_override="123",
                                system_options=OrganisationSystemOptions(
                                    new_subscription_feature_overrides=[
                                        "123",
                                    ],
                                    allowed_domains=[
                                        "app1.subdomain.com",
                                    ],
                                ),
                                ruleset_bundle_id="123",
                                point_of_presence_id="123",
                                point_of_presence_name=FeatureTagName("north-america"),
                                region_id="123",
                            ),
                        ],
                        subscription=BillingSubscription(
                            id="id_example",
                        ),
                        balance=BillingOrgSubscriptionBalance(
                            upcoming_invoice={},
                            subscription_balance=1,
                            estimate_balance_end_date=dateutil_parser('1970-01-01T00:00:00.00Z'),
                        ),
                        feature_overrides=[
                            Feature(
                                metadata=MetadataWithId(),
                                spec=FeatureSpec(
                                    name="name_example",
                                    description="description_example",
                                    priority=1,
                                    key="e",
                                    value=FeatureValue(
                                        enabled=True,
                                        min=1,
                                        max=1,
                                    ),
                                ),
                                status=FeatureStatus(
                                    products=[
                                        Product(
                                            metadata=MetadataWithId(),
                                            spec=ProductSpec(
                                                name="name_example",
                                                description="description_example",
                                                dev_mode=True,
                                                label="123",
                                                billing_product_prices=[
                                                    BillingProductPrice(
                                                        id="id_example",
                                                    ),
                                                ],
                                                trial_period=25,
                                                features=[
                                                    "123",
                                                ],
                                            ),
                                            status=ProductStatus(
                                                billing_product_prices=[
                                                    BillingProductPrice(
                                                        id="id_example",
                                                    ),
                                                ],
                                                features=[
                                                    Feature(),
                                                ],
                                            ),
                                        ),
                                    ],
                                ),
                            ),
                        ],
                        usage_metrics=UsageMetrics(
                            metrics=[
                                UsageMetric(
                                    type="application",
                                    org_id="IAsl3dl40aSsfLKiU76",
                                    org_ids=[
                                        "123",
                                    ],
                                    provisioned=UsageMeasurement(
                                        peak=0,
                                        current=0,
                                    ),
                                    active=UsageMeasurement(
                                        peak=0,
                                        current=0,
                                    ),
                                ),
                            ],
                        ),
                        products=[
                            BillingProduct(
                                id="id_example",
                                name="name_example",
                            ),
                        ],
                        product=Product(
                            metadata=MetadataWithId(),
                            spec=ProductSpec(
                                name="name_example",
                                description="description_example",
                                dev_mode=True,
                                label="123",
                                billing_product_prices=[
                                    BillingProductPrice(
                                        id="id_example",
                                    ),
                                ],
                                trial_period=25,
                                features=[
                                    "123",
                                ],
                            ),
                            status=ProductStatus(
                                billing_product_prices=[
                                    BillingProductPrice(
                                        id="id_example",
                                    ),
                                ],
                                features=[
                                    Feature(
                                        metadata=MetadataWithId(),
                                        spec=FeatureSpec(
                                            name="name_example",
                                            description="description_example",
                                            priority=1,
                                            key="e",
                                            value=FeatureValue(
                                                enabled=True,
                                                min=1,
                                                max=1,
                                            ),
                                        ),
                                        status=FeatureStatus(
                                            products=[
                                                Product(),
                                            ],
                                        ),
                                    ),
                                ],
                            ),
                        ),
                        provider_status=BillingProviderSubscriptionStatus(
                            product_subscription_match=True,
                            subscription_missing_prices=[
                                BillingProductPrice(
                                    id="id_example",
                                ),
                            ],
                            subscription_additional_prices=[
                                BillingProductPrice(
                                    id="id_example",
                                ),
                            ],
                        ),
                    ),
                ),
            ],
            publishable_key="publishable_key_example",
        ),
    ) # BillingAccount | 

    # example passing only required values which don't have defaults set
    try:
        # Create a billing account
        api_response = api_instance.create_billing_account(billing_account)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->create_billing_account: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account** | [**BillingAccount**](BillingAccount.md)|  |

### Return type

[**BillingAccount**](BillingAccount.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New billing account created |  -  |
**400** | Error creating billing account |  -  |
**409** | Billing account already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_feature**
> Feature create_feature(feature)

create a feature

create a feature

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.feature import Feature
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    feature = Feature(
        metadata=MetadataWithId(),
        spec=FeatureSpec(
            name="name_example",
            description="description_example",
            priority=1,
            key="e",
            value=FeatureValue(
                enabled=True,
                min=1,
                max=1,
            ),
        ),
        status=FeatureStatus(
            products=[
                Product(
                    metadata=MetadataWithId(),
                    spec=ProductSpec(
                        name="name_example",
                        description="description_example",
                        dev_mode=True,
                        label="123",
                        billing_product_prices=[
                            BillingProductPrice(
                                id="id_example",
                            ),
                        ],
                        trial_period=25,
                        features=[
                            "123",
                        ],
                    ),
                    status=ProductStatus(
                        billing_product_prices=[
                            BillingProductPrice(
                                id="id_example",
                            ),
                        ],
                        features=[
                            Feature(),
                        ],
                    ),
                ),
            ],
        ),
    ) # Feature | 

    # example passing only required values which don't have defaults set
    try:
        # create a feature
        api_response = api_instance.create_feature(feature)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->create_feature: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature** | [**Feature**](Feature.md)|  |

### Return type

[**Feature**](Feature.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Feature created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_product**
> Product create_product(product)

Create a product

Create a product

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.product import Product
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    product = Product(
        metadata=MetadataWithId(),
        spec=ProductSpec(
            name="name_example",
            description="description_example",
            dev_mode=True,
            label="123",
            billing_product_prices=[
                BillingProductPrice(
                    id="id_example",
                ),
            ],
            trial_period=25,
            features=[
                "123",
            ],
        ),
        status=ProductStatus(
            billing_product_prices=[
                BillingProductPrice(
                    id="id_example",
                ),
            ],
            features=[
                Feature(
                    metadata=MetadataWithId(),
                    spec=FeatureSpec(
                        name="name_example",
                        description="description_example",
                        priority=1,
                        key="e",
                        value=FeatureValue(
                            enabled=True,
                            min=1,
                            max=1,
                        ),
                    ),
                    status=FeatureStatus(
                        products=[
                            Product(),
                        ],
                    ),
                ),
            ],
        ),
    ) # Product | 

    # example passing only required values which don't have defaults set
    try:
        # Create a product
        api_response = api_instance.create_product(product)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->create_product: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **product** | [**Product**](Product.md)|  |

### Return type

[**Product**](Product.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New product created |  -  |
**400** | Error creating product |  -  |
**409** | Product already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_subscription**
> BillingOrgSubscription create_subscription(billing_org_subscription)

Create a billing subscription

Create a billing subscription

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.billing_org_subscription import BillingOrgSubscription
from agilicus_api.model.error_message import ErrorMessage
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_org_subscription = BillingOrgSubscription(
        metadata=MetadataWithId(),
        spec=BillingOrgSubscriptionSpec(
            billing_account_id="123",
            dev_mode=True,
            subscription_id="subscription_id_example",
            usage_override=[
                BillingSubscriptionUsageOverrideItem(
                    metric="metric_example",
                    min_quantity=1,
                    max_quantity=1,
                    step_size=1,
                    group_by_org=True,
                ),
            ],
            feature_overrides=[
                "123",
            ],
            product_id="123",
            cancel_detail=BillingSubscriptionCancelDetail(
                cancel_at_period_end=True,
                cancel_at=dateutil_parser('2025-07-07T15:49:51.23+02:00'),
                immediately=True,
                comment="comment_example",
                feedback="feedback_example",
                subscription=BillingSubscription(
                    id="id_example",
                ),
            ),
        ),
        status=BillingOrgSubscriptionStatus(
            orgs=[
                Organisation(
                    all_users_group_id="123",
                    all_users_all_suborgs_group_id="123",
                    all_users_direct_suborgs_group_id="123",
                    auto_created_users_group_id="123",
                    external_id="123",
                    organisation="some name",
                    issuer="app1",
                    issuer_id="123",
                    subdomain="app1.example.com",
                    name_slug=K8sSlug("81c2v7s6djuy1zmetozkhdomha1bae37b8ocvx8o53ow2eg7p6qw9qklp6l4y010fogx"),
                    contact_id="123",
                    parent_id="123",
                    root_org_id="aB29sdkD3jlaAbl7",
                    auto_create=False,
                    trust_on_first_use_duration=86400,
                    feature_flags=[
                        FeatureFlag(
                            feature="saml_auth",
                            enabled=True,
                            setting="stable",
                        ),
                    ],
                    admin_state=OrganisationStateSelector("active"),
                    status=OrganisationStatus(
                        all_up=True,
                        admin_up=True,
                        issuer_up=True,
                        current_state=OrganisationStateStatus("active"),
                        capabilities=OrganisationCapabilities(
                            features=[
                                FeatureTagName("north-america"),
                            ],
                        ),
                    ),
                    billing_account_id="123",
                    billing_subscription_id="123",
                    shard="A",
                    cluster="ca-1",
                    configured_capabilities=OrganisationCapabilities(
                        features=[
                            FeatureTagName("north-america"),
                        ],
                    ),
                    owner_config=OrganisationOwnerConfig(
                        disable_user_requests=False,
                    ),
                    product_label_override="123",
                    system_options=OrganisationSystemOptions(
                        new_subscription_feature_overrides=[
                            "123",
                        ],
                        allowed_domains=[
                            "app1.subdomain.com",
                        ],
                    ),
                    ruleset_bundle_id="123",
                    point_of_presence_id="123",
                    point_of_presence_name=FeatureTagName("north-america"),
                    region_id="123",
                ),
            ],
            subscription=BillingSubscription(
                id="id_example",
            ),
            balance=BillingOrgSubscriptionBalance(
                upcoming_invoice={},
                subscription_balance=1,
                estimate_balance_end_date=dateutil_parser('1970-01-01T00:00:00.00Z'),
            ),
            feature_overrides=[
                Feature(
                    metadata=MetadataWithId(),
                    spec=FeatureSpec(
                        name="name_example",
                        description="description_example",
                        priority=1,
                        key="e",
                        value=FeatureValue(
                            enabled=True,
                            min=1,
                            max=1,
                        ),
                    ),
                    status=FeatureStatus(
                        products=[
                            Product(
                                metadata=MetadataWithId(),
                                spec=ProductSpec(
                                    name="name_example",
                                    description="description_example",
                                    dev_mode=True,
                                    label="123",
                                    billing_product_prices=[
                                        BillingProductPrice(
                                            id="id_example",
                                        ),
                                    ],
                                    trial_period=25,
                                    features=[
                                        "123",
                                    ],
                                ),
                                status=ProductStatus(
                                    billing_product_prices=[
                                        BillingProductPrice(
                                            id="id_example",
                                        ),
                                    ],
                                    features=[
                                        Feature(),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ),
            ],
            usage_metrics=UsageMetrics(
                metrics=[
                    UsageMetric(
                        type="application",
                        org_id="IAsl3dl40aSsfLKiU76",
                        org_ids=[
                            "123",
                        ],
                        provisioned=UsageMeasurement(
                            peak=0,
                            current=0,
                        ),
                        active=UsageMeasurement(
                            peak=0,
                            current=0,
                        ),
                    ),
                ],
            ),
            products=[
                BillingProduct(
                    id="id_example",
                    name="name_example",
                ),
            ],
            product=Product(
                metadata=MetadataWithId(),
                spec=ProductSpec(
                    name="name_example",
                    description="description_example",
                    dev_mode=True,
                    label="123",
                    billing_product_prices=[
                        BillingProductPrice(
                            id="id_example",
                        ),
                    ],
                    trial_period=25,
                    features=[
                        "123",
                    ],
                ),
                status=ProductStatus(
                    billing_product_prices=[
                        BillingProductPrice(
                            id="id_example",
                        ),
                    ],
                    features=[
                        Feature(
                            metadata=MetadataWithId(),
                            spec=FeatureSpec(
                                name="name_example",
                                description="description_example",
                                priority=1,
                                key="e",
                                value=FeatureValue(
                                    enabled=True,
                                    min=1,
                                    max=1,
                                ),
                            ),
                            status=FeatureStatus(
                                products=[
                                    Product(),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
            provider_status=BillingProviderSubscriptionStatus(
                product_subscription_match=True,
                subscription_missing_prices=[
                    BillingProductPrice(
                        id="id_example",
                    ),
                ],
                subscription_additional_prices=[
                    BillingProductPrice(
                        id="id_example",
                    ),
                ],
            ),
        ),
    ) # BillingOrgSubscription | 

    # example passing only required values which don't have defaults set
    try:
        # Create a billing subscription
        api_response = api_instance.create_subscription(billing_org_subscription)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->create_subscription: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_org_subscription** | [**BillingOrgSubscription**](BillingOrgSubscription.md)|  |

### Return type

[**BillingOrgSubscription**](BillingOrgSubscription.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New billing subscription created |  -  |
**400** | Error creating billing subscription |  -  |
**409** | Billing subscription already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_billing_account**
> delete_billing_account(billing_account_id)

Delete a billing account

Delete a billing account

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_account_id = "1234" # str | Billing account Unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Delete a billing account
        api_instance.delete_billing_account(billing_account_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->delete_billing_account: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account_id** | **str**| Billing account Unique identifier |

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Billing account has been deleted |  -  |
**404** | Billing account does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_feature**
> delete_feature(feature_id)

Delete a feature

Delete a feature

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    feature_id = "1234" # str | Feature ID Unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Delete a feature
        api_instance.delete_feature(feature_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->delete_feature: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_id** | **str**| Feature ID Unique identifier |

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Feature has been deleted |  -  |
**404** | feature_id does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_product**
> delete_product(product_id)

Delete a product

Delete a product

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    product_id = "1234" # str | Product Unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Delete a product
        api_instance.delete_product(product_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->delete_product: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **product_id** | **str**| Product Unique identifier |

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Product has been deleted |  -  |
**404** | Product does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_subscription**
> delete_subscription(billing_subscription_id)

Delete a billing subscription

Delete a billing subscription

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_subscription_id = "1234" # str | Billing subscription Unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Delete a billing subscription
        api_instance.delete_subscription(billing_subscription_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->delete_subscription: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_subscription_id** | **str**| Billing subscription Unique identifier |

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Billing subscription has been deleted |  -  |
**404** | Billing subscription does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_billing_account**
> BillingAccount get_billing_account(billing_account_id)

Get a single billing account

Get a single billing account

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.billing_account import BillingAccount
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_account_id = "1234" # str | Billing account Unique identifier
    org_id = "1234" # str | Organisation Unique identifier (optional)
    get_subscription_data = False # bool | In billing response, return subscription data (optional) if omitted the server will use the default value of False
    get_customer_data = False # bool | In billing response, return customer data (optional) if omitted the server will use the default value of False
    get_usage_metrics = False # bool | In billing response, return all associated usage metrics (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # Get a single billing account
        api_response = api_instance.get_billing_account(billing_account_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_billing_account: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a single billing account
        api_response = api_instance.get_billing_account(billing_account_id, org_id=org_id, get_subscription_data=get_subscription_data, get_customer_data=get_customer_data, get_usage_metrics=get_usage_metrics)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_billing_account: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account_id** | **str**| Billing account Unique identifier |
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **get_subscription_data** | **bool**| In billing response, return subscription data | [optional] if omitted the server will use the default value of False
 **get_customer_data** | **bool**| In billing response, return customer data | [optional] if omitted the server will use the default value of False
 **get_usage_metrics** | **bool**| In billing response, return all associated usage metrics | [optional] if omitted the server will use the default value of False

### Return type

[**BillingAccount**](BillingAccount.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return billing account |  -  |
**404** | billing account does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_billing_account_orgs**
> ListOrgsResponse get_billing_account_orgs(billing_account_id)

Get all orgs in a billing account

Get all orgs in a billing account

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.list_orgs_response import ListOrgsResponse
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_account_id = "1234" # str | Billing account Unique identifier
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500

    # example passing only required values which don't have defaults set
    try:
        # Get all orgs in a billing account
        api_response = api_instance.get_billing_account_orgs(billing_account_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_billing_account_orgs: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all orgs in a billing account
        api_response = api_instance.get_billing_account_orgs(billing_account_id, limit=limit)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_billing_account_orgs: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account_id** | **str**| Billing account Unique identifier |
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500

### Return type

[**ListOrgsResponse**](ListOrgsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return billing account |  -  |
**404** | billing account does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_billing_subscription_orgs**
> ListOrgsResponse get_billing_subscription_orgs(billing_subscription_id)

Get all orgs in a billing subscription

Get all orgs in a billing subscription

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.list_orgs_response import ListOrgsResponse
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_subscription_id = "1234" # str | Billing subscription Unique identifier
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500

    # example passing only required values which don't have defaults set
    try:
        # Get all orgs in a billing subscription
        api_response = api_instance.get_billing_subscription_orgs(billing_subscription_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_billing_subscription_orgs: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all orgs in a billing subscription
        api_response = api_instance.get_billing_subscription_orgs(billing_subscription_id, limit=limit)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_billing_subscription_orgs: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_subscription_id** | **str**| Billing subscription Unique identifier |
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500

### Return type

[**ListOrgsResponse**](ListOrgsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return orgs in a billing subscription |  -  |
**404** | billing account and or subscription does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_customer_balance_transactions**
> ListBillingBalanceTransactions get_customer_balance_transactions(billing_account_id)

Get the customers balance transactions

Get the customers balance transactions

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.list_billing_balance_transactions import ListBillingBalanceTransactions
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_account_id = "1234" # str | Billing account Unique identifier
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    starting_after = "starting_after_example" # str | A cursor for use in pagination. starting_after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include starting_after=obj_foo in order to fetch the next page of the list.  (optional)
    ending_before = "ending_before_example" # str | A cursor for use in pagination. ending_before is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with obj_bar, your subsequent call can include ending_before=obj_bar in order to fetch the previous page of the list.  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get the customers balance transactions
        api_response = api_instance.get_customer_balance_transactions(billing_account_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_customer_balance_transactions: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get the customers balance transactions
        api_response = api_instance.get_customer_balance_transactions(billing_account_id, limit=limit, starting_after=starting_after, ending_before=ending_before)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_customer_balance_transactions: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account_id** | **str**| Billing account Unique identifier |
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **starting_after** | **str**| A cursor for use in pagination. starting_after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include starting_after&#x3D;obj_foo in order to fetch the next page of the list.  | [optional]
 **ending_before** | **str**| A cursor for use in pagination. ending_before is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with obj_bar, your subsequent call can include ending_before&#x3D;obj_bar in order to fetch the previous page of the list.  | [optional]

### Return type

[**ListBillingBalanceTransactions**](ListBillingBalanceTransactions.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return ListBillingBalanceTransactions |  -  |
**404** | billing account does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_feature**
> Feature get_feature(feature_id)

Get a feature by id

Get a feature by id

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.feature import Feature
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    feature_id = "1234" # str | Feature ID Unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Get a feature by id
        api_response = api_instance.get_feature(feature_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_feature: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_id** | **str**| Feature ID Unique identifier |

### Return type

[**Feature**](Feature.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Feature |  -  |
**404** | feature_id does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_product**
> Product get_product(product_id)

Get a single product

Get a single product

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.product import Product
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    product_id = "1234" # str | Product Unique identifier
    get_subscription_data = False # bool | In billing response, return subscription data (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # Get a single product
        api_response = api_instance.get_product(product_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_product: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a single product
        api_response = api_instance.get_product(product_id, get_subscription_data=get_subscription_data)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_product: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **product_id** | **str**| Product Unique identifier |
 **get_subscription_data** | **bool**| In billing response, return subscription data | [optional] if omitted the server will use the default value of False

### Return type

[**Product**](Product.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a product |  -  |
**404** | product does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_subscription**
> BillingOrgSubscription get_subscription(billing_subscription_id)

Get a single billing subscription

Get a single billing subscription

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.billing_org_subscription import BillingOrgSubscription
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_subscription_id = "1234" # str | Billing subscription Unique identifier
    get_subscription_data = False # bool | In billing response, return subscription data (optional) if omitted the server will use the default value of False
    get_customer_data = False # bool | In billing response, return customer data (optional) if omitted the server will use the default value of False
    expand_feature_overrides_query = "aba23" # str | expand all feature overrides (optional)
    get_usage_metrics = False # bool | In billing response, return all associated usage metrics (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # Get a single billing subscription
        api_response = api_instance.get_subscription(billing_subscription_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_subscription: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a single billing subscription
        api_response = api_instance.get_subscription(billing_subscription_id, get_subscription_data=get_subscription_data, get_customer_data=get_customer_data, expand_feature_overrides_query=expand_feature_overrides_query, get_usage_metrics=get_usage_metrics)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_subscription: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_subscription_id** | **str**| Billing subscription Unique identifier |
 **get_subscription_data** | **bool**| In billing response, return subscription data | [optional] if omitted the server will use the default value of False
 **get_customer_data** | **bool**| In billing response, return customer data | [optional] if omitted the server will use the default value of False
 **expand_feature_overrides_query** | **str**| expand all feature overrides | [optional]
 **get_usage_metrics** | **bool**| In billing response, return all associated usage metrics | [optional] if omitted the server will use the default value of False

### Return type

[**BillingOrgSubscription**](BillingOrgSubscription.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return billing subscription |  -  |
**404** | billing subscription does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_subscription_balance_transactions**
> ListBillingBalanceTransactions get_subscription_balance_transactions(billing_subscription_id)

Get the subscription balance transactions

Get the subscription balance transactions

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.list_billing_balance_transactions import ListBillingBalanceTransactions
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_subscription_id = "1234" # str | Billing subscription Unique identifier
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    starting_after = "starting_after_example" # str | A cursor for use in pagination. starting_after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include starting_after=obj_foo in order to fetch the next page of the list.  (optional)
    ending_before = "ending_before_example" # str | A cursor for use in pagination. ending_before is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with obj_bar, your subsequent call can include ending_before=obj_bar in order to fetch the previous page of the list.  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get the subscription balance transactions
        api_response = api_instance.get_subscription_balance_transactions(billing_subscription_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_subscription_balance_transactions: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get the subscription balance transactions
        api_response = api_instance.get_subscription_balance_transactions(billing_subscription_id, limit=limit, starting_after=starting_after, ending_before=ending_before)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_subscription_balance_transactions: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_subscription_id** | **str**| Billing subscription Unique identifier |
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **starting_after** | **str**| A cursor for use in pagination. starting_after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include starting_after&#x3D;obj_foo in order to fetch the next page of the list.  | [optional]
 **ending_before** | **str**| A cursor for use in pagination. ending_before is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with obj_bar, your subsequent call can include ending_before&#x3D;obj_bar in order to fetch the previous page of the list.  | [optional]

### Return type

[**ListBillingBalanceTransactions**](ListBillingBalanceTransactions.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return ListBillingBalanceTransactions |  -  |
**404** | billing subscription does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_usage_records**
> ListBillingUsageRecordsResponse get_usage_records(billing_account_id)

Get all subscription usage records

Get all subscription usage records

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.list_billing_usage_records_response import ListBillingUsageRecordsResponse
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_account_id = "1234" # str | Billing account Unique identifier
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500

    # example passing only required values which don't have defaults set
    try:
        # Get all subscription usage records
        api_response = api_instance.get_usage_records(billing_account_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_usage_records: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all subscription usage records
        api_response = api_instance.get_usage_records(billing_account_id, limit=limit)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_usage_records: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account_id** | **str**| Billing account Unique identifier |
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500

### Return type

[**ListBillingUsageRecordsResponse**](ListBillingUsageRecordsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return all Usage records for the associated billing account |  -  |
**404** | billing account does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_billing_accounts**
> ListBillingAccountsResponse list_billing_accounts()

Get all billing accounts

Get all billing accounts

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.list_billing_accounts_response import ListBillingAccountsResponse
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    org_id = "1234" # str | Organisation Unique identifier (optional)
    customer_id = "1234" # str | query by billing customer id (optional)
    get_subscription_data = False # bool | In billing response, return subscription data (optional) if omitted the server will use the default value of False
    get_customer_data = False # bool | In billing response, return customer data (optional) if omitted the server will use the default value of False
    get_usage_metrics = False # bool | In billing response, return all associated usage metrics (optional) if omitted the server will use the default value of False
    page_at_id = "foo@example.com" # str | Pagination based query with the id as the key. To get the initial entries supply an empty string. On subsequent requests, supply the `page_at_id` field from the list response.  (optional)
    active_orgs_since = dateutil_parser('2015-07-07T15:49:51.230+02:00') # datetime | For billing accounts query, return only billing accounts that are associated with organisations that are active since the specific datetime (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all billing accounts
        api_response = api_instance.list_billing_accounts(limit=limit, org_id=org_id, customer_id=customer_id, get_subscription_data=get_subscription_data, get_customer_data=get_customer_data, get_usage_metrics=get_usage_metrics, page_at_id=page_at_id, active_orgs_since=active_orgs_since)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->list_billing_accounts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **customer_id** | **str**| query by billing customer id | [optional]
 **get_subscription_data** | **bool**| In billing response, return subscription data | [optional] if omitted the server will use the default value of False
 **get_customer_data** | **bool**| In billing response, return customer data | [optional] if omitted the server will use the default value of False
 **get_usage_metrics** | **bool**| In billing response, return all associated usage metrics | [optional] if omitted the server will use the default value of False
 **page_at_id** | **str**| Pagination based query with the id as the key. To get the initial entries supply an empty string. On subsequent requests, supply the &#x60;page_at_id&#x60; field from the list response.  | [optional]
 **active_orgs_since** | **datetime**| For billing accounts query, return only billing accounts that are associated with organisations that are active since the specific datetime | [optional]

### Return type

[**ListBillingAccountsResponse**](ListBillingAccountsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return billing accounts |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_checkout_sessions**
> ListBillingCheckoutSessions list_checkout_sessions(billing_account_id)

list checkout sessions

list checkout sessions

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.list_billing_checkout_sessions import ListBillingCheckoutSessions
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_account_id = "1234" # str | Billing account Unique identifier
    org_id = "1234" # str | Organisation Unique identifier (optional)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    checkout_session_status = "checkout_session_status_example" # str | retreive checkout sessions with specified status  (optional)

    # example passing only required values which don't have defaults set
    try:
        # list checkout sessions
        api_response = api_instance.list_checkout_sessions(billing_account_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->list_checkout_sessions: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # list checkout sessions
        api_response = api_instance.list_checkout_sessions(billing_account_id, org_id=org_id, limit=limit, checkout_session_status=checkout_session_status)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->list_checkout_sessions: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account_id** | **str**| Billing account Unique identifier |
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **checkout_session_status** | **str**| retreive checkout sessions with specified status  | [optional]

### Return type

[**ListBillingCheckoutSessions**](ListBillingCheckoutSessions.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return ListBillingCheckoutSessions |  -  |
**404** | billing account does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_features**
> ListFeaturesResponse list_features()

Get all features

Get all features

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.feature_key import FeatureKey
from agilicus_api.model.list_features_response import ListFeaturesResponse
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    key = FeatureKey("num_connectors") # FeatureKey | Query features by key name (optional)
    name = "aba23" # str | Query features by name (optional)
    prioritize_key = True # bool | When performing a feature query, rows with identical keys will return the highest priority row.  (optional)
    product_id = "aba23" # str | Query by product_id (optional)
    subscription_id = "aba23" # str | Query by subscription_id (optional)
    billing_account_id = "1234" # str | Billing account Unique identifier (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all features
        api_response = api_instance.list_features(limit=limit, key=key, name=name, prioritize_key=prioritize_key, product_id=product_id, subscription_id=subscription_id, billing_account_id=billing_account_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->list_features: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **key** | **FeatureKey**| Query features by key name | [optional]
 **name** | **str**| Query features by name | [optional]
 **prioritize_key** | **bool**| When performing a feature query, rows with identical keys will return the highest priority row.  | [optional]
 **product_id** | **str**| Query by product_id | [optional]
 **subscription_id** | **str**| Query by subscription_id | [optional]
 **billing_account_id** | **str**| Billing account Unique identifier | [optional]

### Return type

[**ListFeaturesResponse**](ListFeaturesResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a list of features |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_products**
> ListProductsResponse list_products()

Get all products

Get all products

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.list_products_response import ListProductsResponse
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    get_subscription_data = False # bool | In billing response, return subscription data (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all products
        api_response = api_instance.list_products(limit=limit, get_subscription_data=get_subscription_data)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->list_products: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **get_subscription_data** | **bool**| In billing response, return subscription data | [optional] if omitted the server will use the default value of False

### Return type

[**ListProductsResponse**](ListProductsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return billing accounts |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_subscription_features**
> ListFeaturesResponse list_subscription_features(billing_subscription_id)

Get all subscription features

Get all subscription features

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.list_features_response import ListFeaturesResponse
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_subscription_id = "1234" # str | Billing subscription Unique identifier
    prioritize_key = True # bool | When performing a feature query, rows with identical keys will return the highest priority row.  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all subscription features
        api_response = api_instance.list_subscription_features(billing_subscription_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->list_subscription_features: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all subscription features
        api_response = api_instance.list_subscription_features(billing_subscription_id, prioritize_key=prioritize_key)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->list_subscription_features: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_subscription_id** | **str**| Billing subscription Unique identifier |
 **prioritize_key** | **bool**| When performing a feature query, rows with identical keys will return the highest priority row.  | [optional]

### Return type

[**ListFeaturesResponse**](ListFeaturesResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return features associated with subscription |  -  |
**404** | billing subscription does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_subscriptions**
> ListBillingOrgSubscriptionsResponse list_subscriptions()

Get all billing subscriptions for a billing account

Get all billing subscriptions for a billing account

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.list_billing_org_subscriptions_response import ListBillingOrgSubscriptionsResponse
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    get_subscription_data = False # bool | In billing response, return subscription data (optional) if omitted the server will use the default value of False
    get_customer_data = False # bool | In billing response, return customer data (optional) if omitted the server will use the default value of False
    billing_account_id = "1234" # str | Billing account Unique identifier (optional)
    org_id = "1234" # str | Organisation Unique identifier (optional)
    customer_id = "1234" # str | query by billing customer id (optional)
    expand_feature_overrides_query = "aba23" # str | expand all feature overrides (optional)
    get_usage_metrics = False # bool | In billing response, return all associated usage metrics (optional) if omitted the server will use the default value of False
    page_at_id = "foo@example.com" # str | Pagination based query with the id as the key. To get the initial entries supply an empty string. On subsequent requests, supply the `page_at_id` field from the list response.  (optional)
    active_orgs_since = dateutil_parser('2015-07-07T15:49:51.230+02:00') # datetime | For billing accounts query, return only billing accounts that are associated with organisations that are active since the specific datetime (optional)
    has_cancel_detail = True # bool | For query of billing subscriptions, query if cancel_detail exists  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all billing subscriptions for a billing account
        api_response = api_instance.list_subscriptions(limit=limit, get_subscription_data=get_subscription_data, get_customer_data=get_customer_data, billing_account_id=billing_account_id, org_id=org_id, customer_id=customer_id, expand_feature_overrides_query=expand_feature_overrides_query, get_usage_metrics=get_usage_metrics, page_at_id=page_at_id, active_orgs_since=active_orgs_since, has_cancel_detail=has_cancel_detail)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->list_subscriptions: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **get_subscription_data** | **bool**| In billing response, return subscription data | [optional] if omitted the server will use the default value of False
 **get_customer_data** | **bool**| In billing response, return customer data | [optional] if omitted the server will use the default value of False
 **billing_account_id** | **str**| Billing account Unique identifier | [optional]
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **customer_id** | **str**| query by billing customer id | [optional]
 **expand_feature_overrides_query** | **str**| expand all feature overrides | [optional]
 **get_usage_metrics** | **bool**| In billing response, return all associated usage metrics | [optional] if omitted the server will use the default value of False
 **page_at_id** | **str**| Pagination based query with the id as the key. To get the initial entries supply an empty string. On subsequent requests, supply the &#x60;page_at_id&#x60; field from the list response.  | [optional]
 **active_orgs_since** | **datetime**| For billing accounts query, return only billing accounts that are associated with organisations that are active since the specific datetime | [optional]
 **has_cancel_detail** | **bool**| For query of billing subscriptions, query if cancel_detail exists  | [optional]

### Return type

[**ListBillingOrgSubscriptionsResponse**](ListBillingOrgSubscriptionsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return billing subscriptions |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_subscriptions_with_feature**
> ListBillingOrgSubscriptionsResponse list_subscriptions_with_feature(feature_id)

Get all subscriptions using feature_id

Get all subscriptions using feature_id

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.list_billing_org_subscriptions_response import ListBillingOrgSubscriptionsResponse
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    feature_id = "1234" # str | Feature ID Unique identifier
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    page_at_id = "foo@example.com" # str | Pagination based query with the id as the key. To get the initial entries supply an empty string. On subsequent requests, supply the `page_at_id` field from the list response.  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all subscriptions using feature_id
        api_response = api_instance.list_subscriptions_with_feature(feature_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->list_subscriptions_with_feature: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all subscriptions using feature_id
        api_response = api_instance.list_subscriptions_with_feature(feature_id, limit=limit, page_at_id=page_at_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->list_subscriptions_with_feature: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_id** | **str**| Feature ID Unique identifier |
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **page_at_id** | **str**| Pagination based query with the id as the key. To get the initial entries supply an empty string. On subsequent requests, supply the &#x60;page_at_id&#x60; field from the list response.  | [optional]

### Return type

[**ListBillingOrgSubscriptionsResponse**](ListBillingOrgSubscriptionsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | ListBillingOrgSubscriptionsResponse |  -  |
**404** | feature_id does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **new_subscription**
> BillingSubscriptionNewSubscription new_subscription(billing_subscription_id)

Create a new upstream subscription

Create a new upstream subscription

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.billing_subscription_new_subscription import BillingSubscriptionNewSubscription
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_subscription_id = "1234" # str | Billing subscription Unique identifier
    billing_subscription_new_subscription = BillingSubscriptionNewSubscription(
        description="description_example",
        trial_period=25,
        updated_subscription=BillingOrgSubscription(
            metadata=MetadataWithId(),
            spec=BillingOrgSubscriptionSpec(
                billing_account_id="123",
                dev_mode=True,
                subscription_id="subscription_id_example",
                usage_override=[
                    BillingSubscriptionUsageOverrideItem(
                        metric="metric_example",
                        min_quantity=1,
                        max_quantity=1,
                        step_size=1,
                        group_by_org=True,
                    ),
                ],
                feature_overrides=[
                    "123",
                ],
                product_id="123",
                cancel_detail=BillingSubscriptionCancelDetail(
                    cancel_at_period_end=True,
                    cancel_at=dateutil_parser('2025-07-07T15:49:51.23+02:00'),
                    immediately=True,
                    comment="comment_example",
                    feedback="feedback_example",
                    subscription=BillingSubscription(
                        id="id_example",
                    ),
                ),
            ),
            status=BillingOrgSubscriptionStatus(
                orgs=[
                    Organisation(
                        all_users_group_id="123",
                        all_users_all_suborgs_group_id="123",
                        all_users_direct_suborgs_group_id="123",
                        auto_created_users_group_id="123",
                        external_id="123",
                        organisation="some name",
                        issuer="app1",
                        issuer_id="123",
                        subdomain="app1.example.com",
                        name_slug=K8sSlug("81c2v7s6djuy1zmetozkhdomha1bae37b8ocvx8o53ow2eg7p6qw9qklp6l4y010fogx"),
                        contact_id="123",
                        parent_id="123",
                        root_org_id="aB29sdkD3jlaAbl7",
                        auto_create=False,
                        trust_on_first_use_duration=86400,
                        feature_flags=[
                            FeatureFlag(
                                feature="saml_auth",
                                enabled=True,
                                setting="stable",
                            ),
                        ],
                        admin_state=OrganisationStateSelector("active"),
                        status=OrganisationStatus(
                            all_up=True,
                            admin_up=True,
                            issuer_up=True,
                            current_state=OrganisationStateStatus("active"),
                            capabilities=OrganisationCapabilities(
                                features=[
                                    FeatureTagName("north-america"),
                                ],
                            ),
                        ),
                        billing_account_id="123",
                        billing_subscription_id="123",
                        shard="A",
                        cluster="ca-1",
                        configured_capabilities=OrganisationCapabilities(
                            features=[
                                FeatureTagName("north-america"),
                            ],
                        ),
                        owner_config=OrganisationOwnerConfig(
                            disable_user_requests=False,
                        ),
                        product_label_override="123",
                        system_options=OrganisationSystemOptions(
                            new_subscription_feature_overrides=[
                                "123",
                            ],
                            allowed_domains=[
                                "app1.subdomain.com",
                            ],
                        ),
                        ruleset_bundle_id="123",
                        point_of_presence_id="123",
                        point_of_presence_name=FeatureTagName("north-america"),
                        region_id="123",
                    ),
                ],
                subscription=BillingSubscription(
                    id="id_example",
                ),
                balance=BillingOrgSubscriptionBalance(
                    upcoming_invoice={},
                    subscription_balance=1,
                    estimate_balance_end_date=dateutil_parser('1970-01-01T00:00:00.00Z'),
                ),
                feature_overrides=[
                    Feature(
                        metadata=MetadataWithId(),
                        spec=FeatureSpec(
                            name="name_example",
                            description="description_example",
                            priority=1,
                            key="e",
                            value=FeatureValue(
                                enabled=True,
                                min=1,
                                max=1,
                            ),
                        ),
                        status=FeatureStatus(
                            products=[
                                Product(
                                    metadata=MetadataWithId(),
                                    spec=ProductSpec(
                                        name="name_example",
                                        description="description_example",
                                        dev_mode=True,
                                        label="123",
                                        billing_product_prices=[
                                            BillingProductPrice(
                                                id="id_example",
                                            ),
                                        ],
                                        trial_period=25,
                                        features=[
                                            "123",
                                        ],
                                    ),
                                    status=ProductStatus(
                                        billing_product_prices=[
                                            BillingProductPrice(
                                                id="id_example",
                                            ),
                                        ],
                                        features=[
                                            Feature(),
                                        ],
                                    ),
                                ),
                            ],
                        ),
                    ),
                ],
                usage_metrics=UsageMetrics(
                    metrics=[
                        UsageMetric(
                            type="application",
                            org_id="IAsl3dl40aSsfLKiU76",
                            org_ids=[
                                "123",
                            ],
                            provisioned=UsageMeasurement(
                                peak=0,
                                current=0,
                            ),
                            active=UsageMeasurement(
                                peak=0,
                                current=0,
                            ),
                        ),
                    ],
                ),
                products=[
                    BillingProduct(
                        id="id_example",
                        name="name_example",
                    ),
                ],
                product=Product(
                    metadata=MetadataWithId(),
                    spec=ProductSpec(
                        name="name_example",
                        description="description_example",
                        dev_mode=True,
                        label="123",
                        billing_product_prices=[
                            BillingProductPrice(
                                id="id_example",
                            ),
                        ],
                        trial_period=25,
                        features=[
                            "123",
                        ],
                    ),
                    status=ProductStatus(
                        billing_product_prices=[
                            BillingProductPrice(
                                id="id_example",
                            ),
                        ],
                        features=[
                            Feature(
                                metadata=MetadataWithId(),
                                spec=FeatureSpec(
                                    name="name_example",
                                    description="description_example",
                                    priority=1,
                                    key="e",
                                    value=FeatureValue(
                                        enabled=True,
                                        min=1,
                                        max=1,
                                    ),
                                ),
                                status=FeatureStatus(
                                    products=[
                                        Product(),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ),
                provider_status=BillingProviderSubscriptionStatus(
                    product_subscription_match=True,
                    subscription_missing_prices=[
                        BillingProductPrice(
                            id="id_example",
                        ),
                    ],
                    subscription_additional_prices=[
                        BillingProductPrice(
                            id="id_example",
                        ),
                    ],
                ),
            ),
        ),
    ) # BillingSubscriptionNewSubscription |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create a new upstream subscription
        api_response = api_instance.new_subscription(billing_subscription_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->new_subscription: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create a new upstream subscription
        api_response = api_instance.new_subscription(billing_subscription_id, billing_subscription_new_subscription=billing_subscription_new_subscription)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->new_subscription: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_subscription_id** | **str**| Billing subscription Unique identifier |
 **billing_subscription_new_subscription** | [**BillingSubscriptionNewSubscription**](BillingSubscriptionNewSubscription.md)|  | [optional]

### Return type

[**BillingSubscriptionNewSubscription**](BillingSubscriptionNewSubscription.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New upstream subscription created |  -  |
**404** | subscription does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_org_from_billing_account**
> remove_org_from_billing_account(billing_account_id, org_id)

Remove an org from a billing account

From an org from a billing account

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_account_id = "1234" # str | Billing account Unique identifier
    org_id = "1234" # str | Organisation Unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Remove an org from a billing account
        api_instance.remove_org_from_billing_account(billing_account_id, org_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->remove_org_from_billing_account: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account_id** | **str**| Billing account Unique identifier |
 **org_id** | **str**| Organisation Unique identifier |

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Organisation removed from billing account |  -  |
**404** | Billing account does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_org_from_billing_subscription**
> remove_org_from_billing_subscription(org_id, billing_subscription_id)

Remove an org from a billing subscription

From an org from a billing subscription

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier
    billing_subscription_id = "1234" # str | Billing subscription Unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Remove an org from a billing subscription
        api_instance.remove_org_from_billing_subscription(org_id, billing_subscription_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->remove_org_from_billing_subscription: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier |
 **billing_subscription_id** | **str**| Billing subscription Unique identifier |

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Organisation removed from billing subscription |  -  |
**404** | Billing subscription does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_billing_account**
> BillingAccount replace_billing_account(billing_account_id)

Create or update a billing account

Create or update a billing account

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.billing_account import BillingAccount
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_account_id = "1234" # str | Billing account Unique identifier
    billing_account = BillingAccount(
        metadata=MetadataWithId(),
        spec=BillingAccountSpec(
            customer_id="123",
            product_id="123",
            dev_mode=True,
        ),
        status=BillingAccountStatus(
            orgs=[
                Organisation(
                    all_users_group_id="123",
                    all_users_all_suborgs_group_id="123",
                    all_users_direct_suborgs_group_id="123",
                    auto_created_users_group_id="123",
                    external_id="123",
                    organisation="some name",
                    issuer="app1",
                    issuer_id="123",
                    subdomain="app1.example.com",
                    name_slug=K8sSlug("81c2v7s6djuy1zmetozkhdomha1bae37b8ocvx8o53ow2eg7p6qw9qklp6l4y010fogx"),
                    contact_id="123",
                    parent_id="123",
                    root_org_id="aB29sdkD3jlaAbl7",
                    auto_create=False,
                    trust_on_first_use_duration=86400,
                    feature_flags=[
                        FeatureFlag(
                            feature="saml_auth",
                            enabled=True,
                            setting="stable",
                        ),
                    ],
                    admin_state=OrganisationStateSelector("active"),
                    status=OrganisationStatus(
                        all_up=True,
                        admin_up=True,
                        issuer_up=True,
                        current_state=OrganisationStateStatus("active"),
                        capabilities=OrganisationCapabilities(
                            features=[
                                FeatureTagName("north-america"),
                            ],
                        ),
                    ),
                    billing_account_id="123",
                    billing_subscription_id="123",
                    shard="A",
                    cluster="ca-1",
                    configured_capabilities=OrganisationCapabilities(
                        features=[
                            FeatureTagName("north-america"),
                        ],
                    ),
                    owner_config=OrganisationOwnerConfig(
                        disable_user_requests=False,
                    ),
                    product_label_override="123",
                    system_options=OrganisationSystemOptions(
                        new_subscription_feature_overrides=[
                            "123",
                        ],
                        allowed_domains=[
                            "app1.subdomain.com",
                        ],
                    ),
                    ruleset_bundle_id="123",
                    point_of_presence_id="123",
                    point_of_presence_name=FeatureTagName("north-america"),
                    region_id="123",
                ),
            ],
            subscriptions=[
                BillingSubscription(
                    id="id_example",
                ),
            ],
            customer=BillingCustomer(
                id="id_example",
                name="John Smith",
                email="john@example.com",
                balance=1,
                created=1,
                currency="currency_example",
                description="description_example",
                invoice_prefix="invoice_prefix_example",
                livemode=True,
                metadata={
                    "key": "key_example",
                },
                phone="phone_example",
            ),
            products=[
                BillingProduct(
                    id="id_example",
                    name="name_example",
                ),
            ],
            product=Product(
                metadata=MetadataWithId(),
                spec=ProductSpec(
                    name="name_example",
                    description="description_example",
                    dev_mode=True,
                    label="123",
                    billing_product_prices=[
                        BillingProductPrice(
                            id="id_example",
                        ),
                    ],
                    trial_period=25,
                    features=[
                        "123",
                    ],
                ),
                status=ProductStatus(
                    billing_product_prices=[
                        BillingProductPrice(
                            id="id_example",
                        ),
                    ],
                    features=[
                        Feature(
                            metadata=MetadataWithId(),
                            spec=FeatureSpec(
                                name="name_example",
                                description="description_example",
                                priority=1,
                                key="e",
                                value=FeatureValue(
                                    enabled=True,
                                    min=1,
                                    max=1,
                                ),
                            ),
                            status=FeatureStatus(
                                products=[
                                    Product(),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
            org_subscriptions=[
                BillingOrgSubscription(
                    metadata=MetadataWithId(),
                    spec=BillingOrgSubscriptionSpec(
                        billing_account_id="123",
                        dev_mode=True,
                        subscription_id="subscription_id_example",
                        usage_override=[
                            BillingSubscriptionUsageOverrideItem(
                                metric="metric_example",
                                min_quantity=1,
                                max_quantity=1,
                                step_size=1,
                                group_by_org=True,
                            ),
                        ],
                        feature_overrides=[
                            "123",
                        ],
                        product_id="123",
                        cancel_detail=BillingSubscriptionCancelDetail(
                            cancel_at_period_end=True,
                            cancel_at=dateutil_parser('2025-07-07T15:49:51.23+02:00'),
                            immediately=True,
                            comment="comment_example",
                            feedback="feedback_example",
                            subscription=BillingSubscription(
                                id="id_example",
                            ),
                        ),
                    ),
                    status=BillingOrgSubscriptionStatus(
                        orgs=[
                            Organisation(
                                all_users_group_id="123",
                                all_users_all_suborgs_group_id="123",
                                all_users_direct_suborgs_group_id="123",
                                auto_created_users_group_id="123",
                                external_id="123",
                                organisation="some name",
                                issuer="app1",
                                issuer_id="123",
                                subdomain="app1.example.com",
                                name_slug=K8sSlug("81c2v7s6djuy1zmetozkhdomha1bae37b8ocvx8o53ow2eg7p6qw9qklp6l4y010fogx"),
                                contact_id="123",
                                parent_id="123",
                                root_org_id="aB29sdkD3jlaAbl7",
                                auto_create=False,
                                trust_on_first_use_duration=86400,
                                feature_flags=[
                                    FeatureFlag(
                                        feature="saml_auth",
                                        enabled=True,
                                        setting="stable",
                                    ),
                                ],
                                admin_state=OrganisationStateSelector("active"),
                                status=OrganisationStatus(
                                    all_up=True,
                                    admin_up=True,
                                    issuer_up=True,
                                    current_state=OrganisationStateStatus("active"),
                                    capabilities=OrganisationCapabilities(
                                        features=[
                                            FeatureTagName("north-america"),
                                        ],
                                    ),
                                ),
                                billing_account_id="123",
                                billing_subscription_id="123",
                                shard="A",
                                cluster="ca-1",
                                configured_capabilities=OrganisationCapabilities(
                                    features=[
                                        FeatureTagName("north-america"),
                                    ],
                                ),
                                owner_config=OrganisationOwnerConfig(
                                    disable_user_requests=False,
                                ),
                                product_label_override="123",
                                system_options=OrganisationSystemOptions(
                                    new_subscription_feature_overrides=[
                                        "123",
                                    ],
                                    allowed_domains=[
                                        "app1.subdomain.com",
                                    ],
                                ),
                                ruleset_bundle_id="123",
                                point_of_presence_id="123",
                                point_of_presence_name=FeatureTagName("north-america"),
                                region_id="123",
                            ),
                        ],
                        subscription=BillingSubscription(
                            id="id_example",
                        ),
                        balance=BillingOrgSubscriptionBalance(
                            upcoming_invoice={},
                            subscription_balance=1,
                            estimate_balance_end_date=dateutil_parser('1970-01-01T00:00:00.00Z'),
                        ),
                        feature_overrides=[
                            Feature(
                                metadata=MetadataWithId(),
                                spec=FeatureSpec(
                                    name="name_example",
                                    description="description_example",
                                    priority=1,
                                    key="e",
                                    value=FeatureValue(
                                        enabled=True,
                                        min=1,
                                        max=1,
                                    ),
                                ),
                                status=FeatureStatus(
                                    products=[
                                        Product(
                                            metadata=MetadataWithId(),
                                            spec=ProductSpec(
                                                name="name_example",
                                                description="description_example",
                                                dev_mode=True,
                                                label="123",
                                                billing_product_prices=[
                                                    BillingProductPrice(
                                                        id="id_example",
                                                    ),
                                                ],
                                                trial_period=25,
                                                features=[
                                                    "123",
                                                ],
                                            ),
                                            status=ProductStatus(
                                                billing_product_prices=[
                                                    BillingProductPrice(
                                                        id="id_example",
                                                    ),
                                                ],
                                                features=[
                                                    Feature(),
                                                ],
                                            ),
                                        ),
                                    ],
                                ),
                            ),
                        ],
                        usage_metrics=UsageMetrics(
                            metrics=[
                                UsageMetric(
                                    type="application",
                                    org_id="IAsl3dl40aSsfLKiU76",
                                    org_ids=[
                                        "123",
                                    ],
                                    provisioned=UsageMeasurement(
                                        peak=0,
                                        current=0,
                                    ),
                                    active=UsageMeasurement(
                                        peak=0,
                                        current=0,
                                    ),
                                ),
                            ],
                        ),
                        products=[
                            BillingProduct(
                                id="id_example",
                                name="name_example",
                            ),
                        ],
                        product=Product(
                            metadata=MetadataWithId(),
                            spec=ProductSpec(
                                name="name_example",
                                description="description_example",
                                dev_mode=True,
                                label="123",
                                billing_product_prices=[
                                    BillingProductPrice(
                                        id="id_example",
                                    ),
                                ],
                                trial_period=25,
                                features=[
                                    "123",
                                ],
                            ),
                            status=ProductStatus(
                                billing_product_prices=[
                                    BillingProductPrice(
                                        id="id_example",
                                    ),
                                ],
                                features=[
                                    Feature(
                                        metadata=MetadataWithId(),
                                        spec=FeatureSpec(
                                            name="name_example",
                                            description="description_example",
                                            priority=1,
                                            key="e",
                                            value=FeatureValue(
                                                enabled=True,
                                                min=1,
                                                max=1,
                                            ),
                                        ),
                                        status=FeatureStatus(
                                            products=[
                                                Product(),
                                            ],
                                        ),
                                    ),
                                ],
                            ),
                        ),
                        provider_status=BillingProviderSubscriptionStatus(
                            product_subscription_match=True,
                            subscription_missing_prices=[
                                BillingProductPrice(
                                    id="id_example",
                                ),
                            ],
                            subscription_additional_prices=[
                                BillingProductPrice(
                                    id="id_example",
                                ),
                            ],
                        ),
                    ),
                ),
            ],
            publishable_key="publishable_key_example",
        ),
    ) # BillingAccount |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create or update a billing account
        api_response = api_instance.replace_billing_account(billing_account_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->replace_billing_account: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create or update a billing account
        api_response = api_instance.replace_billing_account(billing_account_id, billing_account=billing_account)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->replace_billing_account: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account_id** | **str**| Billing account Unique identifier |
 **billing_account** | [**BillingAccount**](BillingAccount.md)|  | [optional]

### Return type

[**BillingAccount**](BillingAccount.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return updated billing account |  -  |
**404** | BillingAccount does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_feature**
> Feature replace_feature(feature_id)

update a Feature

update a Feature

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.feature import Feature
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    feature_id = "1234" # str | Feature ID Unique identifier
    feature = Feature(
        metadata=MetadataWithId(),
        spec=FeatureSpec(
            name="name_example",
            description="description_example",
            priority=1,
            key="e",
            value=FeatureValue(
                enabled=True,
                min=1,
                max=1,
            ),
        ),
        status=FeatureStatus(
            products=[
                Product(
                    metadata=MetadataWithId(),
                    spec=ProductSpec(
                        name="name_example",
                        description="description_example",
                        dev_mode=True,
                        label="123",
                        billing_product_prices=[
                            BillingProductPrice(
                                id="id_example",
                            ),
                        ],
                        trial_period=25,
                        features=[
                            "123",
                        ],
                    ),
                    status=ProductStatus(
                        billing_product_prices=[
                            BillingProductPrice(
                                id="id_example",
                            ),
                        ],
                        features=[
                            Feature(),
                        ],
                    ),
                ),
            ],
        ),
    ) # Feature |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # update a Feature
        api_response = api_instance.replace_feature(feature_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->replace_feature: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # update a Feature
        api_response = api_instance.replace_feature(feature_id, feature=feature)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->replace_feature: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_id** | **str**| Feature ID Unique identifier |
 **feature** | [**Feature**](Feature.md)|  | [optional]

### Return type

[**Feature**](Feature.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return updated Feature |  -  |
**404** | Feature does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_product**
> Product replace_product(product_id)

Create or update a product

Create or update a product

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.product import Product
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    product_id = "1234" # str | Product Unique identifier
    product = Product(
        metadata=MetadataWithId(),
        spec=ProductSpec(
            name="name_example",
            description="description_example",
            dev_mode=True,
            label="123",
            billing_product_prices=[
                BillingProductPrice(
                    id="id_example",
                ),
            ],
            trial_period=25,
            features=[
                "123",
            ],
        ),
        status=ProductStatus(
            billing_product_prices=[
                BillingProductPrice(
                    id="id_example",
                ),
            ],
            features=[
                Feature(
                    metadata=MetadataWithId(),
                    spec=FeatureSpec(
                        name="name_example",
                        description="description_example",
                        priority=1,
                        key="e",
                        value=FeatureValue(
                            enabled=True,
                            min=1,
                            max=1,
                        ),
                    ),
                    status=FeatureStatus(
                        products=[
                            Product(),
                        ],
                    ),
                ),
            ],
        ),
    ) # Product |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create or update a product
        api_response = api_instance.replace_product(product_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->replace_product: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create or update a product
        api_response = api_instance.replace_product(product_id, product=product)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->replace_product: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **product_id** | **str**| Product Unique identifier |
 **product** | [**Product**](Product.md)|  | [optional]

### Return type

[**Product**](Product.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return updated product |  -  |
**404** | BillingAccount does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_subscription**
> BillingOrgSubscription replace_subscription(billing_subscription_id)

Create or update a billing subscription

Create or update a billing subscription

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.billing_org_subscription import BillingOrgSubscription
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_subscription_id = "1234" # str | Billing subscription Unique identifier
    subscription_reconcile = True # bool | Allows control when communicating with backend provider, specifically with regard to subscriptions, and reconcile the subscription with the product  (optional)
    billing_org_subscription = BillingOrgSubscription(
        metadata=MetadataWithId(),
        spec=BillingOrgSubscriptionSpec(
            billing_account_id="123",
            dev_mode=True,
            subscription_id="subscription_id_example",
            usage_override=[
                BillingSubscriptionUsageOverrideItem(
                    metric="metric_example",
                    min_quantity=1,
                    max_quantity=1,
                    step_size=1,
                    group_by_org=True,
                ),
            ],
            feature_overrides=[
                "123",
            ],
            product_id="123",
            cancel_detail=BillingSubscriptionCancelDetail(
                cancel_at_period_end=True,
                cancel_at=dateutil_parser('2025-07-07T15:49:51.23+02:00'),
                immediately=True,
                comment="comment_example",
                feedback="feedback_example",
                subscription=BillingSubscription(
                    id="id_example",
                ),
            ),
        ),
        status=BillingOrgSubscriptionStatus(
            orgs=[
                Organisation(
                    all_users_group_id="123",
                    all_users_all_suborgs_group_id="123",
                    all_users_direct_suborgs_group_id="123",
                    auto_created_users_group_id="123",
                    external_id="123",
                    organisation="some name",
                    issuer="app1",
                    issuer_id="123",
                    subdomain="app1.example.com",
                    name_slug=K8sSlug("81c2v7s6djuy1zmetozkhdomha1bae37b8ocvx8o53ow2eg7p6qw9qklp6l4y010fogx"),
                    contact_id="123",
                    parent_id="123",
                    root_org_id="aB29sdkD3jlaAbl7",
                    auto_create=False,
                    trust_on_first_use_duration=86400,
                    feature_flags=[
                        FeatureFlag(
                            feature="saml_auth",
                            enabled=True,
                            setting="stable",
                        ),
                    ],
                    admin_state=OrganisationStateSelector("active"),
                    status=OrganisationStatus(
                        all_up=True,
                        admin_up=True,
                        issuer_up=True,
                        current_state=OrganisationStateStatus("active"),
                        capabilities=OrganisationCapabilities(
                            features=[
                                FeatureTagName("north-america"),
                            ],
                        ),
                    ),
                    billing_account_id="123",
                    billing_subscription_id="123",
                    shard="A",
                    cluster="ca-1",
                    configured_capabilities=OrganisationCapabilities(
                        features=[
                            FeatureTagName("north-america"),
                        ],
                    ),
                    owner_config=OrganisationOwnerConfig(
                        disable_user_requests=False,
                    ),
                    product_label_override="123",
                    system_options=OrganisationSystemOptions(
                        new_subscription_feature_overrides=[
                            "123",
                        ],
                        allowed_domains=[
                            "app1.subdomain.com",
                        ],
                    ),
                    ruleset_bundle_id="123",
                    point_of_presence_id="123",
                    point_of_presence_name=FeatureTagName("north-america"),
                    region_id="123",
                ),
            ],
            subscription=BillingSubscription(
                id="id_example",
            ),
            balance=BillingOrgSubscriptionBalance(
                upcoming_invoice={},
                subscription_balance=1,
                estimate_balance_end_date=dateutil_parser('1970-01-01T00:00:00.00Z'),
            ),
            feature_overrides=[
                Feature(
                    metadata=MetadataWithId(),
                    spec=FeatureSpec(
                        name="name_example",
                        description="description_example",
                        priority=1,
                        key="e",
                        value=FeatureValue(
                            enabled=True,
                            min=1,
                            max=1,
                        ),
                    ),
                    status=FeatureStatus(
                        products=[
                            Product(
                                metadata=MetadataWithId(),
                                spec=ProductSpec(
                                    name="name_example",
                                    description="description_example",
                                    dev_mode=True,
                                    label="123",
                                    billing_product_prices=[
                                        BillingProductPrice(
                                            id="id_example",
                                        ),
                                    ],
                                    trial_period=25,
                                    features=[
                                        "123",
                                    ],
                                ),
                                status=ProductStatus(
                                    billing_product_prices=[
                                        BillingProductPrice(
                                            id="id_example",
                                        ),
                                    ],
                                    features=[
                                        Feature(),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ),
            ],
            usage_metrics=UsageMetrics(
                metrics=[
                    UsageMetric(
                        type="application",
                        org_id="IAsl3dl40aSsfLKiU76",
                        org_ids=[
                            "123",
                        ],
                        provisioned=UsageMeasurement(
                            peak=0,
                            current=0,
                        ),
                        active=UsageMeasurement(
                            peak=0,
                            current=0,
                        ),
                    ),
                ],
            ),
            products=[
                BillingProduct(
                    id="id_example",
                    name="name_example",
                ),
            ],
            product=Product(
                metadata=MetadataWithId(),
                spec=ProductSpec(
                    name="name_example",
                    description="description_example",
                    dev_mode=True,
                    label="123",
                    billing_product_prices=[
                        BillingProductPrice(
                            id="id_example",
                        ),
                    ],
                    trial_period=25,
                    features=[
                        "123",
                    ],
                ),
                status=ProductStatus(
                    billing_product_prices=[
                        BillingProductPrice(
                            id="id_example",
                        ),
                    ],
                    features=[
                        Feature(
                            metadata=MetadataWithId(),
                            spec=FeatureSpec(
                                name="name_example",
                                description="description_example",
                                priority=1,
                                key="e",
                                value=FeatureValue(
                                    enabled=True,
                                    min=1,
                                    max=1,
                                ),
                            ),
                            status=FeatureStatus(
                                products=[
                                    Product(),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
            provider_status=BillingProviderSubscriptionStatus(
                product_subscription_match=True,
                subscription_missing_prices=[
                    BillingProductPrice(
                        id="id_example",
                    ),
                ],
                subscription_additional_prices=[
                    BillingProductPrice(
                        id="id_example",
                    ),
                ],
            ),
        ),
    ) # BillingOrgSubscription |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create or update a billing subscription
        api_response = api_instance.replace_subscription(billing_subscription_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->replace_subscription: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create or update a billing subscription
        api_response = api_instance.replace_subscription(billing_subscription_id, subscription_reconcile=subscription_reconcile, billing_org_subscription=billing_org_subscription)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->replace_subscription: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_subscription_id** | **str**| Billing subscription Unique identifier |
 **subscription_reconcile** | **bool**| Allows control when communicating with backend provider, specifically with regard to subscriptions, and reconcile the subscription with the product  | [optional]
 **billing_org_subscription** | [**BillingOrgSubscription**](BillingOrgSubscription.md)|  | [optional]

### Return type

[**BillingOrgSubscription**](BillingOrgSubscription.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return updated billing subscription |  -  |
**404** | BillingSubscription does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_subscription_cancellation**
> BillingOrgSubscription update_subscription_cancellation(billing_subscription_id)

Update the subscription cancellation detail

Update the subscription cancellation detail

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.billing_org_subscription import BillingOrgSubscription
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = billing_api.BillingApi(api_client)
    billing_subscription_id = "1234" # str | Billing subscription Unique identifier
    billing_org_subscription = BillingOrgSubscription(
        metadata=MetadataWithId(),
        spec=BillingOrgSubscriptionSpec(
            billing_account_id="123",
            dev_mode=True,
            subscription_id="subscription_id_example",
            usage_override=[
                BillingSubscriptionUsageOverrideItem(
                    metric="metric_example",
                    min_quantity=1,
                    max_quantity=1,
                    step_size=1,
                    group_by_org=True,
                ),
            ],
            feature_overrides=[
                "123",
            ],
            product_id="123",
            cancel_detail=BillingSubscriptionCancelDetail(
                cancel_at_period_end=True,
                cancel_at=dateutil_parser('2025-07-07T15:49:51.23+02:00'),
                immediately=True,
                comment="comment_example",
                feedback="feedback_example",
                subscription=BillingSubscription(
                    id="id_example",
                ),
            ),
        ),
        status=BillingOrgSubscriptionStatus(
            orgs=[
                Organisation(
                    all_users_group_id="123",
                    all_users_all_suborgs_group_id="123",
                    all_users_direct_suborgs_group_id="123",
                    auto_created_users_group_id="123",
                    external_id="123",
                    organisation="some name",
                    issuer="app1",
                    issuer_id="123",
                    subdomain="app1.example.com",
                    name_slug=K8sSlug("81c2v7s6djuy1zmetozkhdomha1bae37b8ocvx8o53ow2eg7p6qw9qklp6l4y010fogx"),
                    contact_id="123",
                    parent_id="123",
                    root_org_id="aB29sdkD3jlaAbl7",
                    auto_create=False,
                    trust_on_first_use_duration=86400,
                    feature_flags=[
                        FeatureFlag(
                            feature="saml_auth",
                            enabled=True,
                            setting="stable",
                        ),
                    ],
                    admin_state=OrganisationStateSelector("active"),
                    status=OrganisationStatus(
                        all_up=True,
                        admin_up=True,
                        issuer_up=True,
                        current_state=OrganisationStateStatus("active"),
                        capabilities=OrganisationCapabilities(
                            features=[
                                FeatureTagName("north-america"),
                            ],
                        ),
                    ),
                    billing_account_id="123",
                    billing_subscription_id="123",
                    shard="A",
                    cluster="ca-1",
                    configured_capabilities=OrganisationCapabilities(
                        features=[
                            FeatureTagName("north-america"),
                        ],
                    ),
                    owner_config=OrganisationOwnerConfig(
                        disable_user_requests=False,
                    ),
                    product_label_override="123",
                    system_options=OrganisationSystemOptions(
                        new_subscription_feature_overrides=[
                            "123",
                        ],
                        allowed_domains=[
                            "app1.subdomain.com",
                        ],
                    ),
                    ruleset_bundle_id="123",
                    point_of_presence_id="123",
                    point_of_presence_name=FeatureTagName("north-america"),
                    region_id="123",
                ),
            ],
            subscription=BillingSubscription(
                id="id_example",
            ),
            balance=BillingOrgSubscriptionBalance(
                upcoming_invoice={},
                subscription_balance=1,
                estimate_balance_end_date=dateutil_parser('1970-01-01T00:00:00.00Z'),
            ),
            feature_overrides=[
                Feature(
                    metadata=MetadataWithId(),
                    spec=FeatureSpec(
                        name="name_example",
                        description="description_example",
                        priority=1,
                        key="e",
                        value=FeatureValue(
                            enabled=True,
                            min=1,
                            max=1,
                        ),
                    ),
                    status=FeatureStatus(
                        products=[
                            Product(
                                metadata=MetadataWithId(),
                                spec=ProductSpec(
                                    name="name_example",
                                    description="description_example",
                                    dev_mode=True,
                                    label="123",
                                    billing_product_prices=[
                                        BillingProductPrice(
                                            id="id_example",
                                        ),
                                    ],
                                    trial_period=25,
                                    features=[
                                        "123",
                                    ],
                                ),
                                status=ProductStatus(
                                    billing_product_prices=[
                                        BillingProductPrice(
                                            id="id_example",
                                        ),
                                    ],
                                    features=[
                                        Feature(),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ),
            ],
            usage_metrics=UsageMetrics(
                metrics=[
                    UsageMetric(
                        type="application",
                        org_id="IAsl3dl40aSsfLKiU76",
                        org_ids=[
                            "123",
                        ],
                        provisioned=UsageMeasurement(
                            peak=0,
                            current=0,
                        ),
                        active=UsageMeasurement(
                            peak=0,
                            current=0,
                        ),
                    ),
                ],
            ),
            products=[
                BillingProduct(
                    id="id_example",
                    name="name_example",
                ),
            ],
            product=Product(
                metadata=MetadataWithId(),
                spec=ProductSpec(
                    name="name_example",
                    description="description_example",
                    dev_mode=True,
                    label="123",
                    billing_product_prices=[
                        BillingProductPrice(
                            id="id_example",
                        ),
                    ],
                    trial_period=25,
                    features=[
                        "123",
                    ],
                ),
                status=ProductStatus(
                    billing_product_prices=[
                        BillingProductPrice(
                            id="id_example",
                        ),
                    ],
                    features=[
                        Feature(
                            metadata=MetadataWithId(),
                            spec=FeatureSpec(
                                name="name_example",
                                description="description_example",
                                priority=1,
                                key="e",
                                value=FeatureValue(
                                    enabled=True,
                                    min=1,
                                    max=1,
                                ),
                            ),
                            status=FeatureStatus(
                                products=[
                                    Product(),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
            provider_status=BillingProviderSubscriptionStatus(
                product_subscription_match=True,
                subscription_missing_prices=[
                    BillingProductPrice(
                        id="id_example",
                    ),
                ],
                subscription_additional_prices=[
                    BillingProductPrice(
                        id="id_example",
                    ),
                ],
            ),
        ),
    ) # BillingOrgSubscription |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update the subscription cancellation detail
        api_response = api_instance.update_subscription_cancellation(billing_subscription_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->update_subscription_cancellation: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update the subscription cancellation detail
        api_response = api_instance.update_subscription_cancellation(billing_subscription_id, billing_org_subscription=billing_org_subscription)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->update_subscription_cancellation: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_subscription_id** | **str**| Billing subscription Unique identifier |
 **billing_org_subscription** | [**BillingOrgSubscription**](BillingOrgSubscription.md)|  | [optional]

### Return type

[**BillingOrgSubscription**](BillingOrgSubscription.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | subscription cancel_detail updated |  -  |
**404** | subscription does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

