# Develop Requirement System API Document

## Outline

- [Develop Requirement System API Document](#develop-requirement-system-api-document)
  - [Outline](#outline)
  - [API Development Progress](#api-development-progress)
  - [Orders Operation](#orders-operation)
    - [`GET` Fetch Orders Collection](#get-fetch-orders-collection)
    - [`GET` Fetch a Specific Orders](#get-fetch-a-specific-orders)
    - [`POST` Create an Orders](#post-create-an-orders)
    - [`PATCH` Update Partially Specific Orders Detail](#patch-update-partially-specific-orders-detail)
    - [`GET` Fetch Order's Ancestor Collection by Order Id](#get-fetch-orders-ancestor-collection-by-order-id)
    - [`GET` Fetch Order's Signature Collection by Order Id](#get-fetch-orders-signature-collection-by-order-id)
    - [`PUT` Update Order's Signature Deatail by Order Id and Signature Id](#put-update-orders-signature-deatail-by-order-id-and-signature-id)
  - [Histories Operation](#histories-operation)
    - [`GET` Filter Histories Collection by Order Id](#get-filter-histories-collection-by-order-id)
    - [`POST` Create User's Comment Histories](#post-create-users-comment-histories)
  - [Documents Operation](#documents-operation)
    - [`GET` Filter Documents Collection by Order Id](#get-filter-documents-collection-by-order-id)
    - [`GET` Fetch a Specific Documents](#get-fetch-a-specific-documents)
    - [`POST` Create a Documents](#post-create-a-documents)
    - [`PATCH` Update Partially Specific Documents Detail](#patch-update-partially-specific-documents-detail)
    - [`DEL` Delete Documents Detail](#del-delete-documents-detail)
  - [Schedules Operation](#schedules-operation)
    - [`GET` Filter Schedules Collection by Order Id](#get-filter-schedules-collection-by-order-id)
    - [`GET` Filter Schedules History by Order Id](#get-filter-schedules-history-by-order-id)
    - [`POST` Create a Schedules](#post-create-a-schedules)
    - [`PATCH` Update Partially Schedules Detail](#patch-update-partially-schedules-detail)
    - [`DEL` Delete Schedules Detail](#del-delete-schedules-detail)
  - [Development Progress Operation](#development-progress-operation)
    - [`GET` Filter Development Progress Collection by Order Id](#get-filter-development-progress-collection-by-order-id)
    - [`GET` Fetch a Specific Development Progress](#get-fetch-a-specific-development-progress)
    - [`POST` Create Development Progress](#post-create-development-progress)
    - [`PUT` Update Development Progress Deatail by Progress Id](#put-update-development-progress-deatail-by-progress-id)
    - [`PATCH` Update Partially Development Progress Detail](#patch-update-partially-development-progress-detail)
    - [`DEL` Delete Development Progress Detail](#del-delete-development-progress-detail)
  - [Notifications Operation](#notifications-operation)
    - [`GET` Fetch Notifications Collection by Current User](#get-fetch-notifications-collection-by-current-user)
    - [`PUT` Update Notifications Detail](#put-update-notifications-detail)
  - [Employees Operation](#employees-operation)
    - [`GET` Search Employees with Site / Employee Id / English Name / Extension / Department ID](#get-search-employees-with-site--employee-id--english-name--extension--department-id)
    - [`GET` Fetch Current Employee](#get-fetch-current-employee)
  - [Assigners Operation](#assigners-operation)
    - [`GET` Filter Assigner by Develop Team Sub Funciton & Project Id](#get-filter-assigner-by-develop-team-sub-funciton--project-id)
  - [Accounts Operation](#accounts-operation)
    - [`GET` Fiter Accounts Collection by Develop Team Sub Function](#get-fiter-accounts-collection-by-develop-team-sub-function)
  - [Projects Operation](#projects-operation)
    - [`GET` Filter Projects Collection by Account Id](#get-filter-projects-collection-by-account-id)
  - [Options Operation](#options-operation)
    - [`GET` Fetch Options Value](#get-fetch-options-value)

## API Development Progress

- [Develop Requirement System API Document](#develop-requirement-system-api-document)

  - [Orders Operation](#orders-operation)
    - [ ] [`GET` Fetch Orders Collection](#get-fetch-orders-collection)
    - [ ] [`GET` Fetch a Specific Orders](#get-fetch-a-specific-orders)
    - [ ] [`POST` Create an Orders](#post-create-an-orders)
    - [ ] [`PATCH` Update Partially Specific Orders Detail](#patch-update-partially-specific-orders-detail)
    - [ ] [`GET` Fetch Order's Ancestor Collection by Order Id](#get-fetch-orders-ancestor-collection-by-order-id)
    - [ ] [`GET` Fetch Order's Signature Collection by Order Id](#get-fetch-orders-signature-collection-by-order-id)
    - [ ] [`PUT` Update Order's Signature Deatail by Order Id and Signature Id](#put-update-orders-signature-deatail-by-order-id-and-signature-id)
  - [Histories Operation](#histories-operation)
    - [x] [`GET` Filter Histories Collection by Order Id](#get-filter-histories-collection-by-order-id)
    - [x] [`POST` Create User's Comment Histories](#post-create-users-comment-histories)
  - [Documents Operation](#documents-operation)
    - [x] [`GET` Filter Documents Collection by Order Id](#get-filter-documents-collection-by-order-id)
    - [x] [`GET` Fetch a Specific Documents](#get-fetch-a-specific-documents)
    - [x] [`POST` Create a Documents](#post-create-a-documents)
    - [x] [`PATCH` Update Partially Specific Documents Detail](#patch-update-partially-specific-documents-detail)
    - [x] [`DEL` Delete Documents Detail](#del-delete-documents-detail)
  - [Schedules Operation](#schedules-operation)
    - [x] [`GET` Filter Schedules Collection by Order Id](#get-filter-schedules-collection-by-order-id)
    - [x] [`GET` Filter Schedules Group Tracker by Order Id](#get-filter-schedules-group-tracker-by-order-id)
    - [x] [`POST` Create a Schedules](#post-create-a-schedules)
    - [x] [`PATCH` Update Partially Schedules Detail](#patch-update-partially-schedules-detail)
    - [x] [`DEL` Delete Schedules Detail](#del-delete-schedules-detail)
  - [Development Progress Operation](#development-progress-operation)
    - [ ] [`GET` Filter Development Progress Collection by Order Id](#get-filter-development-progress-collection-by-order-id)
    - [ ] [`POST` Create Development Progress](#post-create-development-progress)
    - [ ] [`PUT` Update Development Progress Deatail by Progress Id](#put-update-development-progress-deatail-by-progress-id)
    - [ ] [`PATCH` Update Partially Development Progress Detail](#patch-update-partially-development-progress-detail)
    - [ ] [`DEL` Delete Development Progress Detail](#del-delete-development-progress-detail)
  - [Notifications Operation](#notifications-operation)
    - [x] [`GET` Fetch Notifications Collection by Current User](#get-fetch-notifications-collection-by-current-user)
    - [x] [`PUT` Update Notifications Detail](#put-update-notifications-detail)
  - [Employees Operation](#employees-operation)
    - [x] [`GET` Search Employees with Site / Employee Id / English Name / Extension / Department ID](#get-search-employees-with-site--employee-id--english-name--extension--department-id)
    - [x] [`GET` Fetch Current Employee](#get-fetch-current-employee)
  - [Assigners Operation](#assigners-operation)
    - [x] [`GET` Filter Assigner by Develop Team Sub Funciton & Project Id](#get-filter-assigner-by-develop-team-sub-funciton--project-id)
  - [Accounts Operation](#accounts-operation)
    - [x] [`GET` Fiter Accounts Collection by Develop Team Sub Function](#get-fiter-accounts-collection-by-develop-team-sub-function)
  - [Projects Operation](#projects-operation)
    - [x] [`GET` Filter Projects Collection by Account Id](#get-filter-projects-collection-by-account-id)
  - [Options Operation](#options-operation)
    - [x] [`GET` Fetch Options Value](#get-fetch-options-value)

## Orders Operation

### `GET` Fetch Orders Collection

```url
{{service_url}}/api/orders/?page=value1&page_size=value2&filter={"param1":"value1", "param2":"value"}
```

Fetch all orders resource

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    filter (option) | {'id': 1}  | order id (exact search)
    " | {"account": 1} | account id (exact search)
    " | {"project": 3} | project id (exact search)
    " | {"initiator": "Jeff SH Wang"} | initator name (fuzzy search and case insensitive)
    " | {"assigner ": "Leo Tu"} | assigner name (fuzzy search and case insensitive)
    " | {"title": "There is title"} | title (fuzzy search and case insensitive)
    " | {"form_begin_time__before": "2020-03-10T08:26:38.093183Z"} | the begin time of form_begin_time (range search)
    " | {"form_begin_time__after": "2020-03-10T08:26:38.093183Z"}| the end time of form_begin_time (range search)
    " | {"parent": 20} | parent order id (exact search)
    page (option) | 5 | page (it indicate what page number is )
    page_size (option) | 10 | page size

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json

- BODY (raw)

    Example request

    ```json
    {}
    ```

    Example response

    ```json
    {
        "total": 100,
        "totalNotFilter": 20,
        "rows":[
            {
                "id": 2,
                "account": {
                    "id": 1,
                    "code": "Lily",
                },
                "project": {
                    "id": 2,
                    "name": "Stark"
                },
                "develop_team_function": "QT",
                "develop_team_sub_function": "DQMS",
                "status": {
                    "p3": {
                        "initiator": "Approve"
                    },
                },
                "initiator": {
                    "employee_id": "10612704",
                    "display_name": "Jeff SH Wang/WHQ/Wistron",
                    "extension": "85014815",
                    "job_title": "工程師",
                },
                "assigner": {
                    "employee_id": "10612704",
                    "display_name": "Jeff SH Wang/WHQ/Wistron",
                    "extension": "85014815",
                    "job_title": "工程師",
                },
                "developers": {
                    "mebmer":[
                        {
                            "employee_id": "10612704",
                            "display_name": "Jeff SH Wang/WHQ/Wistron",
                            "extension": "85014815",
                            "job_title": "工程師",
                        },
                        {
                            "employee_id": "10712714",
                            "display_name": "Leo Tu/WHQ/Wistron",
                            "extension": "85014817",
                            "job_title": "工程師",
                        },
                    ],
                    "contactor":{
                            "employee_id": "9505005",
                            "display_name": "Luis Liao/WHQ/Wistron",
                            "extension": "85014833",
                            "job_title": "功能經理",
                    }
                },
                "title": "DQMS develope requirement system",
                "description": "<br> Three is description </br>",
                "form_begin_time": "2020-03-10T08:26:38.093183Z",
                "form_end_time": "2020-04-10T08:26:38.093183Z",
                "expected_develop_duration_day": 10.5,
                "actual_develop_duration_day": 20.0,
                "repository_url": "www.gitlab.com",
                "parent": 10,
            },
            {
                "id": 3,
                "account": {
                    "id": 1,
                    "code": "Lily",
                },
                "project": {
                    "id": 2,
                    "name": "Stark"
                },
                "develop_team_function": "QT",
                "develop_team_sub_function": "DQMS",
                "status": {
                    "p3": {
                        "initiator": "Approve"
                    },
                },
                "initiator": {
                    "employee_id": "10612704",
                    "display_name": "Jeff SH Wang/WHQ/Wistron",
                    "extension": "85014815",
                    "job_title": "工程師",
                },
                "assigner": {
                    "employee_id": "10612704",
                    "display_name": "Jeff SH Wang/WHQ/Wistron",
                    "extension": "85014815",
                    "job_title": "工程師",
                },
                "developers": {
                    "mebmer":[
                        {
                            "employee_id": "10612704",
                            "display_name": "Jeff SH Wang/WHQ/Wistron",
                            "extension": "85014815",
                            "job_title": "工程師",
                        },
                        {
                            "employee_id": "10712714",
                            "display_name": "Leo Tu/WHQ/Wistron",
                            "extension": "85014817",
                            "job_title": "工程師",
                        },
                    ],
                    "contactor":{
                            "employee_id": "9505005",
                            "display_name": "Luis Liao/WHQ/Wistron",
                            "extension": "85014833",
                            "job_title": "功能經理",
                    }
                },
                "title": "DQMS develope requirement system",
                "description": "<br> Three is description </br>",
                "form_begin_time": "2020-03-10T08:26:38.093183Z",
                "form_end_time": "2020-04-10T08:26:38.093183Z",
                "expected_develop_duration_day": 10.5,
                "actual_develop_duration_day": 20.0,
                "repository_url": "www.gitlab.com",
                "parent": 10,
            }
        ]
    }

    ```

### `GET` Fetch a Specific Orders

```url
{{service_url}}/api/orders/:id/
```

Fetch a specific orders resource by `id`

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    `id` | Order id

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json

- BODY (raw)

    Example request

    ```json
    {}
    ```

    Example response

    ```json
    {
        "id": 2,
        "account": {
            "id": 1,
            "code": "Lily",
        },
        "project": {
            "id": 2,
            "name": "Stark"
        },
        "develop_team_function": "QT",
        "develop_team_sub_function": "DQMS",
        "status": {
            "p3": {
                "initiator": "Approve"
            },
        },
        "initiator": {
            "employee_id": "10612704",
            "display_name": "Jeff SH Wang/WHQ/Wistron",
            "extension": "85014815",
            "job_title": "工程師",
        },
        "assigner": {
            "employee_id": "10612704",
            "display_name": "Jeff SH Wang/WHQ/Wistron",
            "extension": "85014815",
            "job_title": "工程師",
        },
        "developers": {
            "mebmer":[
                {
                    "employee_id": "10612704",
                    "display_name": "Jeff SH Wang/WHQ/Wistron",
                    "extension": "85014815",
                    "job_title": "工程師",
                },
                {
                    "employee_id": "10712714",
                    "display_name": "Leo Tu/WHQ/Wistron",
                    "extension": "85014817",
                    "job_title": "工程師",
                },
            ],
            "contactor":{
                    "employee_id": "9505005",
                    "display_name": "Luis Liao/WHQ/Wistron",
                    "extension": "85014833",
                    "job_title": "功能經理",
            }
        },
        "title": "DQMS develope requirement system",
        "description": "<br> Three is description </br>",
        "form_begin_time": "2020-03-10T08:26:38.093183Z",
        "form_end_time": "2020-04-10T08:26:38.093183Z",
        "expected_develop_duration_day": 10.5,
        "actual_develop_duration_day": 20.0,
        "repository_url": "www.gitlab.com",
        "parent": 10,
    }
    ```

### `POST` Create an Orders

 - [ ] TODO Need to automatically add initiator

```url
{{service_url}}/api/orders/
```

Create a new orders

- PERMISSSION

    Everyone can use

- PARAMS

    Key|Value|Descriptions
    :---:|:---:|:---:
    account | 3 | account id
    project | 1 | project id
    developers | {"memeber": ["10612704", "10712714", "5825225"], "contactor": "D12345685"} | developers group
    develop_team_function | QT | the function of develop team
    develop_team_sub_function | PQT | the sub function of develop team
    status |{ "p1": {"initiator": "Accept"} }| current order status
    initiator| Z10612704 | employee_id of initiator
    assigner | Z10752135 | employee_id of assigner
    title | this is a good title | order's title
    description | this is a good description | order's description
    parent | 12 | the parent id of order

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json
    X-CSRFToken | {{ CSRF_COOKIE_NAME }}

- BODY (raw)

    Example request

    ```json
    {
        "account": 1,
        "project": 2,
        "develop_team_function": "QT",
        "develop_team_sub_function": "DQMS",
        "status": {"p3_initiator": "Approve"},
        "initiator": "10612704",
        "assigner": "10712714",
        "developers": {
            "member":[
                "10612704",
                "10712717"
            ],
            "contactor": "9505005"
        },
        "title": "DQMS develope requirement system",
        "description": "<br> Three is description </br>",
        "parent": 10,
    }
    ```

    Example response

    ```json
    {
        "id": 2,
        "account": {
            "id": 1,
            "code": "Lily",
        },
        "project": {
            "id": 2,
            "name": "Stark"
        },
        "develop_team_function": "QT",
        "develop_team_sub_function": "DQMS",
        "status": {
            "p3": {
                "initiator": "Approve"
            },
        },
        "initiator": {
            "employee_id": "10612704",
            "display_name": "Jeff SH Wang/WHQ/Wistron",
            "extension": "85014815",
            "job_title": "工程師",
        },
        "assigner": {
            "employee_id": "10612704",
            "display_name": "Jeff SH Wang/WHQ/Wistron",
            "extension": "85014815",
            "job_title": "工程師",
        },
        "developers": {
            "mebmer":[
                {
                    "employee_id": "10612704",
                    "display_name": "Jeff SH Wang/WHQ/Wistron",
                    "extension": "85014815",
                    "job_title": "工程師",
                },
                {
                    "employee_id": "10712714",
                    "display_name": "Leo Tu/WHQ/Wistron",
                    "extension": "85014817",
                    "job_title": "工程師",
                },
            ],
            "contactor": {
                    "employee_id": "9505005",
                    "display_name": "Luis Liao/WHQ/Wistron",
                    "extension": "85014833",
                    "job_title": "功能經理",
            }
        },
        "title": "DQMS develope requirement system",
        "description": "<br> Three is description </br>",
        "parent": 10,
    }
    ```

### `PATCH` Update Partially Specific Orders Detail

```url
{{service_url}}/api/orders/:id/
```

Update partial details of specific orders by order `id`

- PERMISSSION

    Only the assigner, developers and initiator.
    If the fields is only developers, only the assigner can use.

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    `id` | Order id

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    account | 3 | account id
    project | 1 | project id
    developers | {"memeber": ["10612704", "10712714", "5825225"], "contactor": "D12345685"} | developers group
    develop_team_function | QT | the function of develop team
    develop_team_sub_function | PQT | the sub function of develop team
    status |{ "p1": {"initiator": "Accept"} }| current order status
    initiator| Z10612704 | employee_id of initiator
    assigner | Z10752135 | employee_id of assigner
    title | this is a good title | order's title
    description | this is a good description | order's description
    expected_develop_duration_day | 20.5 | the expected develope duration
    actual_develop_duration_day | 10.5 | the actual develope duration
    repository_url | www.abc.com | the result repository url
    parent | 12 | the parent id of order

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json
    X-CSRFToken | {{ CSRF_COOKIE_NAME }}

- BODY (raw)

    Example request

    ```json
    {
        "id": 2,
        "account": 3,
        "project": 5,
        "develop_team_function": "QT",
        "develop_team_sub_function": "DQMS",
        "status": {
            "p3": {
                "initiator": "Approve"
            },
        },
        "initiator": "10612704",
        "assigner": "10712714",
        "developers": {
            "member":[
                "10612704",
                "10712717"
            ],
            "contactor": "9505005"
        },
        "title": "DQMS develope requirement system",
        "description": "<br> Three is description </br>",
    }
    ```

    Example response

    ```json
    {
        "id": 2,
        "account": {
            "id": 3,
            "code": "Lily",
        },
        "project": {
            "id": 5,
            "name": "Stark"
        },
        "develop_team_function": "QT",
        "develop_team_sub_function": "DQMS",
        "status": {
            "p3": {
                "initiator": "Approve"
            },
        },
        "initiator": {
            "employee_id": "10612704",
            "display_name": "Jeff SH Wang/WHQ/Wistron",
            "extension": "85014815",
            "job_title": "工程師",
        },
        "assigner": {
            "employee_id": "10612704",
            "display_name": "Jeff SH Wang/WHQ/Wistron",
            "extension": "85014815",
            "job_title": "工程師",
        },
        "developers": {
            "mebmer":[
                {
                    "employee_id": "10612704",
                    "display_name": "Jeff SH Wang/WHQ/Wistron",
                    "extension": "85014815",
                    "job_title": "工程師",
                },
                {
                    "employee_id": "10712714",
                    "display_name": "Leo Tu/WHQ/Wistron",
                    "extension": "85014817",
                    "job_title": "工程師",
                },
            ],
            "contactor":{
                    "employee_id": "9505005",
                    "display_name": "Luis Liao/WHQ/Wistron",
                    "extension": "85014833",
                    "job_title": "功能經理",
            }
        },
        "title": "DQMS develope requirement system",
        "description": "<br> Three is description </br>"
    }
    ```

### `GET` Fetch Order's Ancestor Collection by Order Id

```url
{{service_url}}/api/orders/:id/ancestors/
```

Fetch order's ancestor collection by orders `id`

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    `id` | Order id

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json

- BODY (raw)

    Example request

    ```json
    {}
    ```

    Example response

    ```json
    [
        {
            "id": 2,
            "account": {
                "id": 1,
                "code": "Lily",
            },
            "project": {
                "id": 2,
                "name": "Stark"
            },
            "develop_team_function": "QT",
            "develop_team_sub_function": "DQMS",
            "status": {
                "p3": {
                    "initiator": "Approve"
                },
            },
            "initiator": {
                "employee_id": "10612704",
                "display_name": "Jeff SH Wang/WHQ/Wistron",
                "extension": "85014815",
                "job_title": "工程師",
            },
            "assigner": {
                "employee_id": "10612704",
                "display_name": "Jeff SH Wang/WHQ/Wistron",
                "extension": "85014815",
                "job_title": "工程師",
            },
            "developers": {
                "mebmer":[
                    {
                        "employee_id": "10612704",
                        "display_name": "Jeff SH Wang/WHQ/Wistron",
                        "extension": "85014815",
                        "job_title": "工程師",
                    },
                    {
                        "employee_id": "10712714",
                        "display_name": "Leo Tu/WHQ/Wistron",
                        "extension": "85014817",
                        "job_title": "工程師",
                    },
                ],
                "contactor":{
                        "employee_id": "9505005",
                        "display_name": "Luis Liao/WHQ/Wistron",
                        "extension": "85014833",
                        "job_title": "功能經理",
                }
            },
            "title": "DQMS develope requirement system",
            "description": "<br> Three is description </br>",
            "form_begin_time": "2020-03-10T08:26:38.093183Z",
            "form_end_time": "2020-04-10T08:26:38.093183Z",
            "expected_develop_duration_day": 10.5,
            "actual_develop_duration_day": 20.0,
            "repository_url": "www.gitlab.com",
            "parent": null,
        },
        {
            "id": 3,
            "account": {
                "id": 1,
                "code": "Lily",
            },
            "project": {
                "id": 2,
                "name": "Stark"
            },
            "develop_team_function": "QT",
            "develop_team_sub_function": "DQMS",
            "status": {
                "p3": {
                    "initiator": "Approve"
                },
            },
            "initiator": {
                "employee_id": "10612704",
                "display_name": "Jeff SH Wang/WHQ/Wistron",
                "extension": "85014815",
                "job_title": "工程師",
            },
            "assigner": {
                "employee_id": "10612704",
                "display_name": "Jeff SH Wang/WHQ/Wistron",
                "extension": "85014815",
                "job_title": "工程師",
            },
            "developers": {
                "mebmer":[
                    {
                        "employee_id": "10612704",
                        "display_name": "Jeff SH Wang/WHQ/Wistron",
                        "extension": "85014815",
                        "job_title": "工程師",
                    },
                    {
                        "employee_id": "10712714",
                        "display_name": "Leo Tu/WHQ/Wistron",
                        "extension": "85014817",
                        "job_title": "工程師",
                    },
                ],
                "contactor":{
                        "employee_id": "9505005",
                        "display_name": "Luis Liao/WHQ/Wistron",
                        "extension": "85014833",
                        "job_title": "功能經理",
                }
            },
            "title": "DQMS develope requirement system",
            "description": "<br> Three is description </br>",
            "form_begin_time": "2020-03-10T08:26:38.093183Z",
            "form_end_time": "2020-04-10T08:26:38.093183Z",
            "expected_develop_duration_day": 10.5,
            "actual_develop_duration_day": 20.0,
            "repository_url": "www.gitlab.com",
            "parent": 2,
        }
    ]
    ```

### `GET` Fetch Order's Signature Collection by Order Id

```url
{{service_url}}/api/orders/:order_id/signatures/
```

Fetch order's signature collection by order's `id`

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    `order_id` | Order id

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json

- BODY (raw)

    Example request

    ```json
    {}
    ```

    Example response

    ```json
    [
        {
            "id": 1,
            "sequence": 1,
            "signer": {
                "employee_id": "10612704",
                "display_name": "Jeff SH Wang/WNH/Wistron",
                "extension": "85014602",
                "job_title": "工程師",
            },
            "status": "Accept",
            "comment": "OK",
            "timestamp": "2020-03-10T08:26:38.093183Z",
            "role_group": "initiator",
            "order": 1,
        },
        {
            "id": 2,
            "sequence": 2,
            "signer": {
                "employee_id": "Z10712718",
                "display_name": "David Wang/WNH/Wistron",
                "extension": "85015752",
                "job_title": "部門主管",
            },
            "status": "",
            "comment": "",
            "timestamp": null,
            "role_group": "initiator",
            "order": 1,
        },
        {
            "id": 3,
            "sequence": 3,
            "signer": {
                "employee_id": "9505005",
                "display_name": "Luis Liao/WNH/Wistron",
                "extension": "85014686",
                "job_title": "處長",
            },
            "status": "",
            "comment": "",
            "timestamp": null,
            "role_group": "developers",
            "order": 1,
        },
    ]
    ```

### `PUT` Update Order's Signature Deatail by Order Id and Signature Id

```url
{{service_url}}/api/orders/:order_id/signatures/:signature_id/
```

Update order's signature detail by order's `id` and signature's `id`

- PERMISSSION

    Only current signaturer can use

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    `order_id` | Order id
    `signature_id` | Signature id

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json

- BODY (raw)

    Example request

    ```json
    {
        "id": 1,
        "status": "Accept",
        "comment": "It's a good proposal",
    }
    ```

    Example response

    ```json
    {
        "id": 1,
        "status": "Accept",
        "comment": "It's a good proposal",
    }
    ```

---

## Histories Operation

### `GET` Filter Histories Collection by Order Id

```url
{{service_url}}/api/histories/?param1=value1
```

Filter histories resource by order

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    order| 10 | order id

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json

- BODY (raw)

    Example request

    ```json
    {}
    ```

    Example response

    ```json
    [
        {
            "id": 2,
            "comment": "<br>There is a comment</br>",
            "editor": {
                "employee_id": "9505005",
                "display_name": "Luis Liao/WNH/Wistron",
                "extension": "85014686",
                "job_title": "處長",
            },
            "timestamp": "2020-03-20T08:26:38.093183Z",
            "order": 10,
        },
        {
            "id": 3,
            "comment": "<br>There is a comment</br>",
            "editor": {
                "employee_id": "9505005",
                "display_name": "Luis Liao/WNH/Wistron",
                "extension": "85014686",
                "job_title": "處長",
            },
            "timestamp": "2020-03-21T08:26:38.093183Z",
            "order": 10,
        },
    ]
    ```

### `POST` Create User's Comment Histories

```url
{{service_url}}/api/histories/
```

Create a new user's comment histories

- PERMISSSION

    Everyone can use

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json
    X-CSRFToken | {{ CSRF_COOKIE_NAME }}

- BODY (raw)

    Example request

    ```json
    {
        "comment": "<br>There is a user comment</br>",
        "order": 10
    }
    ```

    Example response

    ```json
    {
        "id": 2,
        "comment": "<br>There is a user comment</br>",
        "editor": {
                "employee_id": "9505005",
                "display_name": "Luis Liao/WNH/Wistron",
                "extension": "85014686",
                "job_title": "處長",
        },
        "timestamp": "2020-03-20T08:26:38.093183Z",
        "order": 10
    }
    ```

---

## Documents Operation

### `GET` Filter Documents Collection by Order Id

```url
{{service_url}}/api/documents/?param1=value1
```

Filter documents resource by order

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    order | 1 | order id

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json

- BODY (raw)

    Example request

    ```json
    {}
    ```

    Example response

    ```json
    [
        {
            "id": 1,
            "name": "filename1.txt",
            "path": "http://dqms.wistron.com/document_1.pdf",
            "order": 1,
            "description": "There is document1 description",
            "size": "1024000",
            "uploader": "10612704",
            "created_time": "2020-03-21T08:26:38.093183Z",
        },
        {
            "id": 2,
            "name": "filename2.txt",
            "path": "http://dqms.wistron.com/document_2.pdf",
            "order": 1,
            "description": "There is document2 description",
            "size": "2048000",
            "uploder": "10612704",
            "created_time": "2020-03-21T08:26:38.093183Z",
        },
    ]
    ```

### `GET` Fetch a Specific Documents

```url
{{service_url}}/api/documents/:id/
```

Fetch a specific documents resource by documents `id`

- PATH VARIABLES
    Variable|Description
    :---: | :---:
    `id` | documents id

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json

- BODY (raw)

    Example request

    ```json
    {}
    ```

    Example response

    ```json
    {
        "id": 1,
        "name": "filename.txt",
        "description": "There is document description",
        "order": 1,
        "path": "http://dqms.wistron.com/document_1.pdf",
        "size": "1024000",
        "uploder": "10612704",
        "created_time": "2020-03-21T08:26:38.093183Z",
    }
    ```

### `POST` Create a Documents

```url
{{service_url}}/api/documents/
```

Create a new documents

- PERMISSSION

    Only initiator can use

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json
    X-CSRFToken | {{ CSRF_COOKIE_NAME }}

- BODY (raw)

    Example request

    ```json
    {
        "path": (binary),
        "name": "filename.txt",
        "description": "There is document description",
        "order": 1,
    }
    ```

    Example response

    ```json
    {
        "id": 1,
        "name": "filename.txt",
        "description": "There is document description",
        "order": 1,
        "path": "http://dqms.wistron.com/document_1.pdf",
        "size": "1024000",
        "uploder": "10612704",
        "created_time": "2020-03-21T08:26:38.093183Z",
    }
    ```

### `PATCH` Update Partially Specific Documents Detail

```url
{{service_url}}/api/documents/:id/
```

Update partial details of specific documents by document `id`

- PERMISSSION

    Only initiator can use

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    id | document id

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    name | 123.txt | the filename of documents
    description | This is a good description | the filedescriptionname of documents

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json
    X-CSRFToken | {{ CSRF_COOKIE_NAME }}

- BODY (raw)

    Example request

    ```json
    {
        "id": 1,
        "name": "filename.txt",
        "description": "There is document description",
    }
    ```

    Example response

    ```json
    {
        "id": 1,
        "name": "filename.txt",
        "description": "There is document description",
    }
    ```

### `DEL` Delete Documents Detail

```url
{{service_url}}/api/documents/:id/
```

Delete a documents detail by `id`

- PERMISSSION

    Only initiator can use

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    id | documents id

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json
    X-CSRFToken | {{ CSRF_COOKIE_NAME }}

- BODY (raw)

    Example request

    ```json
    {}
    ```

    Example response

    ```json
    {}
    ```

---

## Schedules Operation

### `GET` Filter Schedules Collection by Order Id

- [ ] TODO Add filter schedule by version is null

```url
{{service_url}}/api/schedules/?param1=value1
```

Filter schedules resource by order id

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    order (option) | 1 | order id

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json

- BODY (raw)

    Example request

    ```json
    {}
    ```

    Example response

    ```json
    [
        {
            "id": 1,
            "event_name": "Project Begin Time",
            "description": "This is a milestone.",
            "actual_time": null,
            "expected_time": "2020-03-21T08:59:38.093183Z",
            "complete_rate": 15,
            "version": 1,
            "update_time": "2020-01-20T08:59:38.093183Z",
            "created_time": "2020-01-20T08:59:38.093183Z",
            "order": 1,
        },
        {
            "id": 2,
            "event_name": "Project End Time",
            "description": "This is a milestone.",
            "actual_time": null,
            "expected_time": "2020-03-21T08:59:38.093183Z",
            "complete_rate": 15,
            "version": 1,
            "update_time": "2020-01-20T08:59:38.093183Z",
            "created_time": "2020-01-20T08:59:38.093183Z",
            "order": 1,
        },
        {
            "id": 3,
            "event_name": "MVP Time",
            "description": "This is a milestone.",
            "actual_time": null,
            "expected_time": "2020-03-21T08:59:38.093183Z",
            "complete_rate": 15,
            "version": null,
            "update_time": "2020-01-20T08:59:38.093183Z",
            "created_time": "2020-01-20T08:59:38.093183Z",
            "order": 1,
        },
    ]
    ```

- Default

    event_name : `Project Begin Time`, `Project End Time`, `MVP Time`

### `GET` Filter Schedules History by Order Id

```url
{{service_url}}/api/schedules/group_tracker/?param1=value1
```

Filter schedules history resource by order id

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    order (required) | 1 | order id

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json

- BODY (raw)

    Example request

    ```json
    {}
    ```

    Example resonse

    ```json
    {
        "1":[
            {
                "id": 1,
                "event_name": "Project Begin Time",
                "description": "This is a milestone.",
                "actual_time": "2020-03-21T08:59:38.093183Z",
                "expected_time": null,
                "complete_rate": 15,
                "version": 1,
                "update_time": "2020-01-20T08:59:38.093183Z",
                "created_time": "2020-01-20T08:59:38.093183Z",
                "order": 1,
            },
            {
                "id": 2,
                "event_name": "Project End Time",
                "description": "This is a milestone.",
                "actaul_time": "2020-03-21T08:59:38.093183Z",
                "expected_time": null,
                "complete_rate": 15,
                "version": 1,
                "update_time": "2020-01-20T08:59:38.093183Z",
                "created_time": "2020-01-20T08:59:38.093183Z",
                "order": 1,
            },
        ],
        "2":[
            {
                "id": 1,
                "event_name": "Project Begin Time",
                "description": "This is a milestone.",
                "actaul_time": "2020-03-21T08:59:38.093183Z",
                "expected_time": null,
                "complete_rate": 15,
                "version": 2,
                "update_time": "2020-01-20T08:59:38.093183Z",
                "created_time": "2020-01-20T08:59:38.093183Z",
                "order": 1,
            },
            {
                "id": 2,
                "event_name": "Project End Time",
                "actaul_time": "2020-03-21T08:59:38.093183Z",
                "expected_time": null,
                "description": "This is a milestone.",
                "complete_rate": 15,
                "version": 2,
                "update_time": "2020-01-20T08:59:38.093183Z",
                "created_time": "2020-01-20T08:59:38.093183Z",
                "order": 1,
            },
        ]
    }
    ```

### `POST` Create a Schedules

```url
{{service_url}}/api/schedules/
```

Create a new schedules

- PERMISSSION

    Only assigner can use

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json
    X-CSRFToken | {{ CSRF_COOKIE_NAME }}

- BODY (raw)

    Example request

    ```json
    {
        "event_name": "Project End Time",
        "description": "This is a milestone.",
        "expected_time": "2020-03-21T08:59:38.093183Z",
        "complete_rate": 15,
        "order": 1,
    }
    ```

    Example response

    ```json
    {
        "id": 2,
        "event_name": "Project End Time",
        "description": "This is a milestone.",
        "actual_time": null,
        "expected_time": "2020-03-21T08:59:38.093183Z",
        "version": null,
        "complete_rate": 15,
        "order": 1,
    }
    ```

### `PATCH` Update Partially Schedules Detail

```url
{{service_url}}/api/schedules/:id/
```

Update partial details of schedules by schedule `id`

- PERMISSSION

    Only assigner can use

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    id | schedules id

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    event_name| Project Begin Time | the name of schedules
    description | This is a description | the description of schedules
    expected_time | 2020-03-21T08:59:38.093183Z | the expected_time of schedules
    complete_rate | 15 | the complete_rate of schedules
    order | 2 | it indicate this record belong to which order

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json
    X-CSRFToken | {{ CSRF_COOKIE_NAME }}

- BODY (raw)

    Example request

    ```json
    {
        "id": 1,
        "event_name": "MVP Time",
        "expected_time": "2020-03-21T08:59:38.093183Z",
    }
    ```

    Example response

    ```json
    {
        "id": 1,
        "event_name": "MVP Time",
        "expected_time": "2020-03-21T08:59:38.093183Z",
    }
    ```

### `DEL` Delete Schedules Detail

```url
{{service_url}}/api/schedules/:id/
```

Delete a schedules detail by `id`

- PERMISSSION

    Only assigner can use

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    id | schedules id

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json
    X-CSRFToken | {{ CSRF_COOKIE_NAME }}

- BODY (raw)

    Example request

    ```json
    {}
    ```

    Example response

    ```json
    {}
    ```

---

## Development Progress Operation

### `GET` Filter Development Progress Collection by Order Id

```url
{{service_url}}/api/progress/?param1=value1
```

Filter progress resource by order id

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    order| 10 | order id

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json

- BODY (raw)

    Example request

    ```json
    {}
    ```

    Example response

    ```json
    [
        {
            "id": 2,
            "name": "Spirit 01",
            "description": "This is a description.",
            "start_time": "2020-03-20T08:26:38.093183Z",
            "end_time": "2020-03-20T08:26:38.093183Z",
            "complete_rate": 10,
            "editor": {
                "employee_id": "10612704",
                "display_name": "Jeff SH Wang/WHQ/Wistron",
                "extension": "85014815",
                "job_title": "工程師",
            },
            "update_time": "2020-03-20T08:26:38.093183Z",
            "order": 10,
        },
        {
            "id": 3,
            "name": "Spirit 02",
            "description": "This is a description.",
            "start_time": "2020-03-20T08:26:38.093183Z",
            "end_time": "2020-03-20T08:26:38.093183Z",
            "complete_rate": 100,
            "editor": {
                "employee_id": "10612704",
                "display_name": "Jeff SH Wang/WHQ/Wistron",
                "extension": "85014815",
                "job_title": "工程師",
            },
            "update_time": "2020-03-20T08:26:38.093183Z",
            "order": 10,
        },
    ]
    ```

### `GET` Fetch a Specific Development Progress

```url
{{service_url}}/api/progress/:id/
```

Fetch a specific progress resource by progress `id`

- PATH VARIABLES
    Variable|Description
    :---: | :---:
    `id` | progress id

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json

- BODY (raw)

    Example request

    ```json
    {}
    ```

    Example response

    ```json
    {
        "id": 2,
        "name": "Spirit 01",
        "description": "This is a description.",
        "start_time": "2020-03-20T08:26:38.093183Z",
        "end_time": "2020-03-20T08:26:38.093183Z",
        "complete_rate": 10,
        "editor": {
            "employee_id": "10612704",
            "display_name": "Jeff SH Wang/WHQ/Wistron",
            "extension": "85014815",
            "job_title": "工程師",
        },
        "update_time": "2020-03-20T08:26:38.093183Z",
        "order": 10,
    }
    ``

### `POST` Create Development Progress

```url
{{service_url}}/api/progress/
```

Create a new development progress on specific order

- PERMISSSION

    Only developers can use

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json
    X-CSRFToken | {{ CSRF_COOKIE_NAME }}

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    name | Progress Name | the name of the progress
    description | This is a description | the description of progress
    start_time| Project Begin Time | the start time of progress
    end_time | 2020-03-21T08:59:38.093183Z | the end time of progress
    complete_rate | 15 | the complete_rate of progress
    order | 2 | it indicate this progress belong to which order

- BODY (raw)

    Example request

    ```json
    {
        "name": "MVP Time",
        "start_time": "2020-03-20T08:26:38.093183Z",
        "end_time": "2020-03-20T08:26:38.093183Z",
        "description": "This is a description.",
        "complete_rate": 100,
        "order": 10
    }
    ```

    Example response

    ```json
    {
        "id": 2,
        "name": "MVP Time",
        "description": "This is a description.",
        "start_time": "2020-03-20T08:26:38.093183Z",
        "end_time": "2020-03-20T08:26:38.093183Z",
        "complete_rate": 100,
        "editor": {
            "employee_id": "10612704",
            "display_name": "Jeff SH Wang/WHQ/Wistron",
            "extension": "85014815",
            "job_title": "工程師",
        },
        "update_time": "2020-03-20T08:26:38.093183Z",
        "order": 10
    }
    ```

### `PUT` Update Development Progress Deatail by Progress Id

```url
{{service_url}}/api/progress/:id/
```

Update order's progress detail by progress `id`

- PERMISSSION

    Only developers can use

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    id | progress id

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    name | Progress Name | the name of the progress
    description | This is a description | the description of progress
    start_time| Project Begin Time | the start time of progress
    end_time | 2020-03-21T08:59:38.093183Z | the end time of progress
    complete_rate | 15 | the complete_rate of progress
    order | 2 | it indicate this progress belong to which order

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json
    X-CSRFToken | {{ CSRF_COOKIE_NAME }}

- BODY (raw)

    Example request

    ```json
    {
        "id": 1,
        "name": "MVP Time",
        "description": "This is a description.",
        "start_time": "2020-03-20T08:26:38.093183Z",
        "end_time": "2020-03-20T08:26:38.093183Z",
        "complete_rate": 100,
        "order": 10
    }
    ```

    Example response

    ```json
    {
        "id": 1,
        "name": "MVP Time",
        "description": "This is a description.",
        "start_time": "2020-03-20T08:26:38.093183Z",
        "end_time": "2020-03-20T08:26:38.093183Z",
        "complete_rate": 100,
        "editor": {
            "employee_id": "10612704",
            "display_name": "Jeff SH Wang/WHQ/Wistron",
            "extension": "85014815",
            "job_title": "工程師",
        },
        "update_time": "2020-03-20T08:26:38.093183Z",
        "order": 10
    }
    ```

### `PATCH` Update Partially Development Progress Detail

```url
{{service_url}}/api/progress/:id/
```

Update partial details of progress by progress `id`

- PERMISSSION

    Only developers can use

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    id | progress id

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    name | Progress Name | the name of the progress
    description | This is a description | the description of progress
    start_time| Project Begin Time | the start time of progress
    end_time | 2020-03-21T08:59:38.093183Z | the end time of progress
    complete_rate | 15 | the complete_rate of progress
    order | 2 | it indicate this progress belong to which order

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json
    X-CSRFToken | {{ CSRF_COOKIE_NAME }}

- BODY (raw)

    Example request

    ```json
    {
        "id": 1,
        "name": "MVP Time",
        "start_time": "2020-03-21T08:59:38.093183Z",
    }
    ```

    Example response

    ```json
    {
        "id": 1,
        "name": "MVP Time",
        "start_time": "2020-03-21T08:59:38.093183Z",
    }
    ```

### `DEL` Delete Development Progress Detail

```url
{{service_url}}/api/progress/:id/
```

Delete a progress detail by progress `id`

- PERMISSSION

    Only developers can use

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    id | progress id

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json
    X-CSRFToken | {{ CSRF_COOKIE_NAME }}

- BODY (raw)

    Example request

    ```json
    {}
    ```

    Example response

    ```json
    {}
    ```

---

## Notifications Operation

### `GET` Fetch Notifications Collection by Current User

```url
{{service_url}}/api/notifications/
```

Fetch notifications collection resource by current user

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    read | true/false | notifications read status  (exact search)

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json

- BODY (raw)

    Example request

    ```json
    {}
    ```

    Example response

    ```json
    [
        {
            "id": 1,
            "link": "http://xxx.xxx.xxx.xxx/?abc=123",
            "read": false,
            "category": "signature",
            "initiator": "10612704",
            "created_time": "2020-03-10T08:26:38.093183Z",
            "owner": "10612704",
        },
        {
            "id": 2,
            "link": "http://xxx.xxx.xxx.xxx/?def=123",
            "read": false,
            "category": "signature",
            "initiator": "10612704",
            "created_time": "2020-03-10T08:26:38.093183Z",
            "owner": "10612704",
        },
        {
            "id": 3,
            "link": "http://xxx.xxx.xxx.xxx/?def=123",
            "read": true,
            "category": "signature",
            "initiator": "10612704",
            "created_time": "2020-03-10T08:26:38.093183Z",
            "owner": "10612704",
        },
    ]
    ```

### `PUT` Update Notifications Detail

```url
{{service_url}}/api/notifications/:id/
```

Update detail of notifications by `id`

- PERMISSSION

    Only owner can use

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    id | notification id

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json
    X-CSRFToken | {{ CSRF_COOKIE_NAME }}

- BODY (raw)

    Example request 1

    ```json
    {
        "id": 1,
        "read": true,
    }
    ```

    Example response 1

    ```json
    {
        "id": 1,
        "link": "http://xxx.xxx.xxx.xxx/?order=123",
        "read": true,
        "category": "signature",
        "initiator": "10612704",
        "created_time": "2020-03-10T08:26:38.093183Z",
        "owner": "10612704",
    }
    ```

---

## Employees Operation

### `GET` Search Employees with Site / Employee Id / English Name / Extension / Department ID

```url
{{service_url}}/api/employees/?param1=value1&param2=value2...
```

Search employees resource with site / employee_id / english_name / extension / department_id

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    site (option)| WNH | employee location (exact search)
    employee_id (option)| 10612704 | employee id (fuzzy search and case insensitive)
    english_name (option)| Jeff SH Wang | employee english_name (fuzzy search and case insensitive)
    extension (option)| 4815556 | employee extension (fuzzy search and case insensitive)
    department_id (option)| ESQ | department id (fuzzy search and case insensitive)

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json

- BODY (raw)

    Example request

    ```json
    {}
    ```

    Example response

    ```json
    {
        "total": 2,
        "totalNotFilter": 3336,
        "rows":[
            {
                "employee_id": "10612704",
                "display_name": "Jeff SH Wang/WHQ/Wistron",
                "extension": "85014815",
                "job_title": "工程師",
            },
            {
                "employee_id": "10712714",
                "display_name": "Leo Tu/WHQ/Wistron",
                "extension": "85014817",
                "job_title": "工程師",
            },
        ]
    }
    ```

### `GET` Fetch Current Employee

```url
{{service_url}}/api/employees/me/
```

Fetch current employees detail

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json

- BODY (raw)

    Example request

    ```json
    {}
    ```

    Example response 1

    ```json
    {
        "employee_id": "10612704",
        "display_name": "Jeff SH Wang/WHQ/Wistron",
        "extension": "85014815",
        "job_title": "工程師",
    }
    ```

---

## Assigners Operation

### `GET` Filter Assigner by Develop Team Sub Funciton & Project Id

```url
{{service_url}}/api/assigners/?param1=value1&param2=value2
```

Filter a specific assigner resource via develop_team_sub_function and project_id

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    sub_function (require) | BIOS/TSC/PQT/DQMS | develop_team_sub_function
    project_id (require) | 1 | project id

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json

- BODY (raw)

    Example request

    ```json
    {}
    ```

    Example response

    ```json
    [
        {
            "employee_id": "10612704",
            "display_name": "Jeff SH Wang/WHQ/Wistron",
            "extension": "85014815",
            "job_title": "工程師",
        },
        {
            "employee_id": "10712714",
            "display_name": "Leo Tu/WHQ/Wistron",
            "extension": "85014817",
            "job_title": "工程師",
        },
    ]
    ```

---

## Accounts Operation

### `GET` Fiter Accounts Collection by Develop Team Sub Function

```url
{{service_url}}/api/accounts/?param1=value1
```

Filter accounts collection resource by develop_team_sub_function

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    sub_function (require) | BIOS/TSC/PQT/DQMS | develop_team_sub_function

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json

- BODY (raw)

    Example request

    ```json
    {}
    ```

    Example response

    ```json
    [
        {
            "id": 1,
            "name": "HPI",
            "code": "Astro",
            "business_unit": 2,
            "project_count": 0
        },
        {
            "id": 2,
            "name": "HPE",
            "code": "Apollo",
            "business_unit": 2,
            "project_count": 1
        },
        {
            "id": 3,
            "name": "Inspur",
            "code": "Irma",
            "business_unit": 3,
            "project_count": 0
        },
        {
            "id": 4,
            "name": "Cisco",
            "code": "Cindy",
            "business_unit": 1,
            "project_count": 1
        },
    ]
    ```

---

## Projects Operation

### `GET` Filter Projects Collection by Account Id

```url
{{service_url}}/api/projects/?param1=value1
```

Fetch projects collection resource by account id

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    acct_id (option) | 4 | account id (exact search)

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json

- BODY (raw)

    Example request

    ```json
    {}
    ```

    Example response

    ```json
    [
        {
            "id": 1,
            "wistron_name": null,
            "customer_name": "Trinity 1U",
            "wistron_code": "C182TR2",
            "plm_code_1": "QRQY00000137",
            "plm_code_2": "6PD02A010001",
            "deleted_at": null,
            "name": "Trinity 1U",
            "plm_code": "QRQY00000137",
            "type": "NPI",
            "status": "On-going",
            "product_line": "Server",
            "business_model": "ODM",
            "account": {
                "id": 4,
                "name": "Cisco",
                "code": "Cindy",
                "business_unit": 1
            }
        },
        {
            "id": 2,
            "wistron_name": null,
            "customer_name": "Trinity 2U",
            "wistron_code": "C182TR3",
            "plm_code_1": "QRQY00000154",
            "plm_code_2": "6PD022010001",
            "deleted_at": null,
            "name": "Trinity 2U",
            "plm_code": "QRQY00000154",
            "type": "NPI",
            "status": "On-going",
            "product_line": "Server",
            "business_model": "ODM",
            "account": {
                "id": 4,
                "name": "Cisco",
                "code": "Cindy",
                "business_unit": 1
            }
        }
    ]
    ```

---

## Options Operation

### `GET` Fetch Options Value

```url
{{service_url}}/api/options/?field=value1
```

Fetch option value resource via field value

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    field (option)| dept_category / dept_role / business_unit / project_type / project_status / product_line / business_model | field value

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json

- BODY (raw)

    Example request

    ```json
    {}
    ```

    Example response

    ```json
    {
        "EBG": {
            "BU": [
                "AM",
                "PCC",
                "PM"
            ],
            "EE": [
                "CE",
                "CPLD",
                "EA",
                "EE",
                "Power",
                "SI"
            ],
            "ME": [
                "ME",
                "Packing",
                "Structure",
                "Thermal"
            ],
            "QT": [
                "DQMS",
                "MQT",
                "PQT"
            ],
            "SW": [
                "BIOS",
                "BMC",
                "PM",
                "TSC"
            ]
        }
    }
    ```

---

`Order Table`

id: IntegerField (primary_key=True)

account: IntegerField

project: IntegerField

develop_team_function: CharField i.e. EE/SW/QT/BU

develop_team_sub_function: CharField i.e. TSC/BIOS/BMC/MQT/PQT/DQMS...

status: JSONField

initator: JSONField

assigner: JSONField

developers: JSONField

title: CharField

description: TextField

form_begin_time: DateTimeField

form_end_time: DateTimeField

expected_develop_duration_day: FloatField

actual_develop_duration_day: FloatField

repository_url: URLField

parent: TreeForeignKey

---

`History Table`

id: IntegerField (primary_key=True)

editor: CharField

comment: TextField

created_time: DateTimeField

order: ForeignKey

---

`Document Table`

id: IntegerField (primary_key=True)

path: FileField

name: CharFiled

description: CharField

uploader: CharField

size: IntegerField

created_time: DateTimeField

order: ForeignKey

---

`Schedule Table`

id: IntegerField (primary_key=True)

event_name: CharField

description: CharField

expected_time: DateTimeField

complete_rate: PositiveIntegerField

update_time: DateTimeField

created_time: DateTimeField

version: CharField

order: ForeignKey

---

`ScheduleTracker Table`

id: IntegerField (primary_key=True)

event_name: CharField

description: CharField

expected_time: DateTimeField

complete_rate: PositiveIntegerField

update_time: DateTimeField

created_time: DateTimeField

version: CharField

order: ForeignKey

---

`Progress Table`

id: IntegerField (primary_key=True)

name: CharField

description: TextField

complete_rate: PositiveIntegerField

start_time: DateTimeField

end_time: DateTimeField

editor: CharField

update_time: DateTimeField

order: ForeignKey

---

`Employee Table` (managed=False)

employee_id: CharField (primary_key=True)

english_name: CharField

chinese_name: CharField

department_id: CharField

department_name: CharField

mail: EmailField

job_title: CharField

extension: CharField

supervisor_id: CharField

site: CharField

---

`Signature Table`

id: IntegerField (primary_key=True)

sequence: PositiveIntegerField

signer: CharField

status: CharField

comment: TextField

signed_time: DateTimeField

role_group: CharField

order: ForeignKey

---

`Notification Table`

id: IntegerField (primary_key=True)

link: URLField

read: BoolField (true, false)

category: CharField (Ex/signature, develop, return, close)

initiator: CharField

created_time: DateTimeField

owner: CharField

---

`OrderTracker Table`

id: IntegerField (primary_key=True)

account: IntegerField

project: IntegerField

develop_team_function: CharField i.e. EE/SW/QT/BU

develop_team_sub_function: CharField i.e. TSC/BIOS/BMC/MQT/PQT/DQMS...

status: JSONField

initator: JSONField

assigner: JSONField

developers: JSONField

title: CharField

description: TextField

form_begin_time: DateTimeField

form_end_time: DateTimeField

expected_develop_duration_day: FloatField

actual_develop_duration_day: FloatField

repository_url: URLField

created_time: DateTimeField

order: ForeignKey
