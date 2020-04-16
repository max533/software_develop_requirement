# Develop Requirement System API Document

## Outline

- [Develop Requirement System API Document](#develop-requirement-system-api-document)
  - [Outline](#outline)
  - [Orders Operation](#orders-operation)
    - [`GET` Fetch Orders Collection](#get-fetch-orders-collection)
    - [`GET` Fetch a Specific Orders](#get-fetch-a-specific-orders)
    - [`POST` Create an Orders](#post-create-an-orders)
    - [`PATCH` Update Partially Specific Orders](#patch-update-partially-specific-orders)
  - [Histories Operation](#histories-operation)
    - [`GET` Filter Histories Collection by Order Id](#get-filter-histories-collection-by-order-id)
    - [`POST` Create User's Comment Histories](#post-create-users-comment-histories)
    - [`POST` Create User's Activity Histories](#post-create-users-activity-histories)
  - [Documents Operation](#documents-operation)
    - [`GET` Filter Documents Collection by Order Id](#get-filter-documents-collection-by-order-id)
    - [`GET` Fetch a Specific Documents](#get-fetch-a-specific-documents)
    - [`POST` Create a Documents](#post-create-a-documents)
    - [`PUT` Update Documents Detail](#put-update-documents-detail)
    - [`DEL` Delete Documents Detail](#del-delete-documents-detail)
  - [Schedulers Operation](#schedulers-operation)
    - [`GET` Filter Schedulers Collection by Order Id](#get-filter-schedulers-collection-by-order-id)
    - [`POST` Create a Schedulers](#post-create-a-schedulers)
    - [`PUT` Update Schedulers Detail](#put-update-schedulers-detail)
    - [`DEL` Delete Schedulers Detail](#del-delete-schedulers-detail)
  - [Assigners Operation](#assigners-operation)
    - [`GET` Filter Assigner by Sub Funciton & Project Id](#get-filter-assigner-by-sub-funciton--project-id)
  - [Developer Groups Operation](#developer-groups-operation)
    - [`GET` Fetch Developer Groups by Order Id](#get-fetch-developer-groups-by-order-id)
    - [`PUT` Update Developer Group Detail](#put-update-developer-group-detail)
  - [Employees Operation](#employees-operation)
    - [`GET` Search Employees with Site / Employee Id / English Name / Extension](#get-search-employees-with-site--employee-id--english-name--extension)
    - [`GET` Fetch Current My Employee's information](#get-fetch-current-my-employees-information)
  - [Accounts Operation](#accounts-operation)
    - [`GET` Fetch Accounts Collection](#get-fetch-accounts-collection)
  - [Projects Operation](#projects-operation)
    - [`GET` Filter Projects Collection by Account Id](#get-filter-projects-collection-by-account-id)
  - [Department Categorys Operation](#department-categorys-operation)
    - [`GET` Fetch Department Categorys Collection](#get-fetch-department-categorys-collection)

## Orders Operation

### `GET` Fetch Orders Collection

```text
{{service_url}}/orders/?param1=value1&param2=value2...
```

Fetch all orders resource

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    filter (option) | {'id':1}  | order id
    " | {"initiator": "Jeff SH Wang"} | initator name
    " | {"title": "There is title"} | title
    " | {"expected_develop_end_time__before":"2020-03-10T08:26:38.093183Z"}| the begin time of expected_develop_end_time
    " |{"expected_develop_end_time__after": "2020-03-10T08:26:38.093183Z"} | the end time of expected_develop_end_time
    " | { "form_begin_time__before":"2020-03-10T08:26:38.093183Z"} | the begin time of expected_develop_begin_time(option) | {"form_begin_time__after": "2020-03-10T08:26:38.093183Z"}| the end time of expected_develop_begin_time
    " | {"developer":"Leo Tu/WHQ/Wistron"} | developer name
    " | {"parent":20} | parent order id
    page (option) | 10 | page (which it indicate what is page number)
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
        "rows":{
            [
                {
                    "id": 2,
                    "account_name": "R360",
                    "project_name": "R360xxxxx",
                    "develop_team_function": "QT",
                    "develop_team_sub_function": "DQMS",
                    "status": {"p3_initiator_": "Approve"},
                    "initiator": {
                        "emplotee_id": 10612704,
                        "display_name": "Jeff SH Wang/WHQ/Wistron"
                    },
                    "assigner": {
                        "employee_id": 10612704,
                        "display_name": "Jeff SH Wang/WHQ/Wistron"
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
                    "account_name": "R360",
                    "project_name": "R360xxxxx",
                    "develop_team_function": "QT",
                    "develop_team_sub_function": "DQMS",
                    "status": {"p3_initiator_": "Approve"},
                    "initiator": {
                        "emplotee_id": 10612704,
                        "display_name": "Jeff SH Wang/WHQ/Wistron"
                    },
                    "assigner": {
                        "employee_id": 10612704,
                        "display_name": "Jeff SH Wang/WHQ/Wistron"
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
    }

    ```

### `GET` Fetch a Specific Orders

```text
{{service_url}}/orders/:id/
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
        "account_name": "R360",
        "project_name": "R360xxxxx",
        "develop_team_function": "QT",
        "develop_team_sub_function": "DQMS",
        "status": {"p3_initiator_": "Approve"},
        "initiator": {
            "emplotee_id": 10612704,
            "emplyee_name": "Jeff SH Wang"
        },
        "assigner": {
            "employee_id": 10612704,
            "employee_name": "Jeff SH Wang"
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

```text
{{service_url}}/orders/?fields=develop_team,label,status,initiator,assigner,title,description,form_begin_time,form_end_time,expected_develop_duration_day,repository_url,parent
```

Create a new orders

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    fields (require)| account_name/project_name/develop_team_function/develop_team_sub_function/status/initiator/assigner/title/description/expected_develop_duration_day/actual_develop_duration_day/repository_url/parent| which fields need to be validate

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json
    X-CSRFToken | {{ CSRF_COOKIE_NAME }}

- BODY (raw)

    Example request

    ```json
    {
        "account_name": "R360",
        "project_name": "R360xxxxx",
        "develop_team_function": "QT",
        "develop_team_sub_function": "DQMS",
        "status": {"p3_initiator": "Approve"},
        "initiator": {
            "emplotee_id": 10612704,
            "emplyee_name": "Jeff SH Wang"
        },
        "assigner": {
            "employee_id": 10612704,
            "employee_name": "Jeff SH Wang"
        },
        "title": "DQMS develope requirement system",
        "description": "<br> Three is description </br>",
        "expected_develop_duration_day": 10.5,
        "actual_develop_duration_day": 20.0,
        "repository_url": "www.gitlab.com",
        "parent": 10,
    }
    ```

    Example response

    ```json
    {
        "id": 2,
        "account_name": "R360",
        "project_name": "R360xxxxx",
        "develop_team_function": "QT",
        "develop_team_sub_function": "DQMS",
        "status": {"p3_initiator_": "Approve"},
        "initiator": {
            "emplotee_id": 10612704,
            "emplyee_name": "Jeff SH Wang"
        },
        "assigner": {
            "employee_id": 10612704,
            "employee_name": "Jeff SH Wang"
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

### `PATCH` Update Partially Specific Orders

```text
{{service_url}}/orders/:id/?fields=account_name/project_name/develop_team_function/develop_team_sub_function/status/initiator/assigner/title/description/expected_develop_duration_day/actual_develop_duration_day/repository_url/parent
```

Update partial details of specific orders by `id`

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    `id` | Order id

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    fields (require)| account_name/project_name/develop_team_function/develop_team_sub_function/status/initiator/assigner/title/description/expected_develop_duration_day/actual_develop_duration_day/repository_url/parent| which fields need to be validate

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
        "account_name": "R360",
        "project_name": "R360xxxxx",
        "develop_team_function": "QT",
        "develop_team_sub_function": "DQMS",
        "status": {"p3_initiator_": "Approve"},
        "initiator": {
            "emplotee_id": 10612704,
            "emplyee_name": "Jeff SH Wang"
        },
        "assigner": {
            "employee_id": 10612704,
            "employee_name": "Jeff SH Wang"
        },
        "title": "DQMS develope requirement system",
        "description": "<br> Three is description </br>",
    }
    ```

    Example response

    ```json
    {
        "id": 2,
        "account_name": "R360",
        "project_name": "R360xxxxx",
        "develop_team_function": "QT",
        "develop_team_sub_function": "DQMS",
        "status": {"p3_initiator_": "Approve"},
        "initiator": {
            "emplotee_id": 10612704,
            "emplyee_name": "Jeff SH Wang"
        },
        "assigner": {
            "employee_id": 10612704,
            "employee_name": "Jeff SH Wang"
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

---

## Histories Operation

### `GET` Filter Histories Collection by Order Id

```text
{{service_url}}/histories/?orders_id=10
```

Filter histories resource by order_id

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    orders_id| 10 | orders id

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
        [
            {
                "id": 2,
                "comment": "<br>There is a comment</br>",
                "editor": {
                    "employee_id": 10612704,
                    "display_name": "Jeff SH Wang/WHQ/Wistron",
                    "avatar": "http://www.abc.com/123.jpg"
                },
                "timestamp": "2020-03-20T08:26:38.093183Z",
                "orders_id": 10,
            },
            {
                "id": 3,
                "comment": "<br>There is a comment</br>",
                "editor": {
                    "employee_id": 10612704,
                    "display_name": "Jeff SH Wang/WHQ/Wistron",
                    "avatar": "http://www.abc.com/123.jpg"
                },
                "timestamp": "2020-03-21T08:26:38.093183Z",
                "orders_id": 10,
            },
        ]
    }
    ```

### `POST` Create User's Comment Histories

```text
{{service_url}}/histories/
```

Create a new user's comment histories

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
        "orders_id": 10
    }
    ```

    Example response

    ```json
    {
        "id": 2,
        "comment": "<br>There is a user comment</br>",
        "editor": {
            "employee_id": 10612704,
            "display_name": "Jeff Sh Wang/WHQ/Wistron"
        },
        "timestamp": "2020-03-20T08:26:38.093183Z",
        "orders_id": 10
    }
    ```

### `POST` Create User's Activity Histories

```text
{{service_url}}/histories/system/
```

Create a new user's activity histories

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json
    X-CSRFToken | {{ CSRF_COOKIE_NAME }}

- BODY (raw)

    Example request

    ```json
    {
        "comment": "<br>There is a system history</br>",
        "orders_id": 10
    }
    ```

    Example response

    ```json
    {
        "id": 2,
        "comment": "<br>There is a system history</br>",
        "editor": {
            "employee_id": 10612704,
            "display_name": "Jeff Sh Wang/WHQ/Wistron"
        },
        "timestamp": "2020-03-20T08:26:38.093183Z",
        "orders_id": 10
    }
    ```

---

## Documents Operation

### `GET` Filter Documents Collection by Order Id

```text
{{service_url}}/documents/?param1=value1
```

Filter documents resource by order_id

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    order_id | 1 | order id

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
        [
            {
                "id": 1,
                "name": "filename1.txt",
                "path": "http://dqms.wistron.com/document_1.pdf",
                "order_id": 1,
                "description": "There is document1 description",
                "size": "1024000",
                "created_time": "2020-03-21T08:26:38.093183Z",
            },
            {
                "id": 2,
                "name": "filename2.txt",
                "path": "http://dqms.wistron.com/document_2.pdf",
                "order_id": 1,
                "description": "There is document2 description",
                "size": "2048000",
                "created_time": "2020-03-21T08:26:38.093183Z",
            },
        ]
    }
    ```

### `GET` Fetch a Specific Documents

```text
{{service_url}}/documents/:id/
```

Fetch a specific documents resource by `id`

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
        "order_id": 1,
        "path": "http://dqms.wistron.com/document_1.pdf",
        "size": "1024000",
        "created_time": "2020-03-21T08:26:38.093183Z",
    }
    ```

### `POST` Create a Documents

```text
{{service_url}}/documents/
```

Create a new documents

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
        "order_id": 1,
    }
    ```

    Example response

    ```json
    {
        "id": 1,
        "name": "filename.txt",
        "description": "There is document description",
        "order_id": 1,
        "path": "http://dqms.wistron.com/document_1.pdf",
        "size": "1024000",
        "created_time": "2020-03-21T08:26:38.093183Z",
    }
    ```

### `PUT` Update Documents Detail

```text
{{service_url}}/documents/:id/
```

Update details of a documents by `id`

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    id | document id

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
        "path": (binary),
        "name": "filename.txt",
        "description": "There is document description",
        "order_id": 1,
    }
    ```

    Example response

    ```json
    {
        "id": 1,
        "name": "filename.txt",
        "description": "There is document description",
        "order_id": 1,
        "path": "http://dqms.wistron.com/document_1.pdf",
        "size": "1024000",
        "created_time": "2020-03-21T08:26:38.093183Z",
    }
    ```

### `DEL` Delete Documents Detail

```text
{{service_url}}/documents/:id/
```

Delete a documents detail by `id`

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

## Schedulers Operation

### `GET` Filter Schedulers Collection by Order Id

```text
{{service_url}}/schedulers/?param1=value1
```

Filter schedulers resource by order_id

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    order_id | 1 | order id

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
        [
            {
                "id": 1,
                "event_name": "MVP Time",
                "current_time": "2020-03-21T08:49:38.093183Z",
                "expected_time": "2020-03-21T08:59:38.093183Z",
                "complete_rate": "15",
                "time_tracker": [
                    "2020-03-21T08:26:38.093183Z",
                    "2020-03-21T08:37:38.093183Z",
                    "2020-03-21T08:49:38.093183Z",
                ],
                "order_id": 1,
            },
            {
                "id": 2,
                "event_name": "MVP Time2",
                "current_time": "2020-03-21T08:49:38.093183Z",
                "expected_time": "2020-03-21T08:59:38.093183Z",
                "complete_rate": "15",
                "time_tracker": [
                    "2020-03-21T08:26:38.093183Z",
                    "2020-03-21T08:37:38.093183Z",
                    "2020-03-21T08:49:38.093183Z",
                ],
                "order_id": 1,
            },
        ]
    }
    ```

- Default

    event_name : mvp_time, expected_develop_begin_time, expected_develop_end_time

### `POST` Create a Schedulers

```text
{{service_url}}/schedulers/
```

Create a new schedulers

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json
    X-CSRFToken | {{ CSRF_COOKIE_NAME }}

- BODY (raw)

    Example request

    ```json
    {
        "event_name": "MVP Time",
        "current_time": "2020-03-21T08:49:38.093183Z",
        "expected_time": "",
        "complete_rate": "15",
        "order_id": 1,
    }
    ```

    Example response

    ```json
    {
        "id": 1,
        "event_name": "MVP Time",
        "current_time": "2020-03-21T08:49:38.093183Z",
        "expected_time": "",
        "complete_rate": "15",
        "time_tracker": [],
        "order_id": 1
    }
    ```

### `PUT` Update Schedulers Detail

```text
{{service_url}}/schedulers/:id/
```

Update details of schedulers by `id`

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    id | schedulers id

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
        "event_name": "MVP Time",
        "current_time": "2020-03-21T08:49:38.093183Z",
        "expected_time": "2020-03-21T08:59:38.093183Z",
        "complete_rate": "15",
        "order_id": 1
    }
    ```

    Example response 1

    ```json
    {
        "id": 1,
        "event_name": "MVP Time",
        "current_time": "2020-03-21T08:49:38.093183Z",
        "expected_time": "2020-03-21T08:59:38.093183Z",
        "complete_rate": "15",
        "time_tracker": [],
        "order_id": 1
    }
    ```

    Example request 2

    ```json
    {
        "id": 1,
        "event_name": "MVP Time",
        "current_time": "2020-03-21T08:59:38.093183Z",
        "expected_time": "",
        "complete_rate": "15",
        "order_id": 1
    }
    ```

    Example response 2

    ```json
    {
        "id": 1,
        "event_name": "MVP Time",
        "current_time": "2020-03-21T08:59:38.093183Z",
        "expected_time": "",
        "complete_rate": "15",
        "time_tracker": ["2020-03-21T08:49:38.093183Z"],
        "order_id": 1
    }
    ```

### `DEL` Delete Schedulers Detail

```text
{{service_url}}/schedulers/:id/
```

Delete a schedulers detail by `id`

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    id | schedulers id

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

## Assigners Operation

### `GET` Filter Assigner by Sub Funciton & Project Id

```text
{{service_url}}/assigners/?param1=value1&param2=value2
```

Filter a specific assigner resource via develop_team_sub_function amd project_id

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
    {
        [
            {
                "employee_id": 10612704,
                "display_name": "Jeff SH Wang/WHQ/Wistron",
                "extension": "85014815",
                "job_title": "工程師",
                "avatar": "http://www.abc.com/123.jpg"
            },
            {
                "employee_id": 10712714,
                "display_name": "Leo Tu/WHQ/Wistron",
                "extension": "85014817",
                "job_title": "工程師",
                "avatar": "http://www.abc.com/123.jpg"
            },
        ]
    }
    ```

---

## Developer Groups Operation

### `GET` Fetch Developer Groups by Order Id

```text
{{service_url}}/developer_groups/:id/
```

Fetch a developer_groups resource by order_id

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    id | order id

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
        "developer":[
            {
                "employee_id": 10612704,
                "display_name": "Jeff SH Wang/WHQ/Wistron",
                "extension": "85014815",
                "job_title": "工程師",
                "avatar": "http://www.abc.com/123.jpg"
            },
            {
                "employee_id": 10712714,
                "display_name": "Leo Tu/WHQ/Wistron",
                "extension": "85014817",
                "job_title": "工程師",
                "avatar": "http://www.abc.com/123.jpg"
            },
        ],
        "developer_contacter":{
                "employee_id": 9505005,
                "display_name": "Luis Liao/WHQ/Wistron",
                "extension": "85014833",
                "job_title": "功能經理",
                "avatar": "http://www.abc.com/123.jpg"
        }
    }
    ```

    Example response 2

    ```json
    {
        "developer":[
            {
                "employee_id": 10612704,
                "display_name": "Jeff SH Wang/WHQ/Wistron",
                "extension": null,
                "job_title": null,
                "avatar": null
            },
            {
                "employee_id": 10712714,
                "display_name": "Leo Tu/WHQ/Wistron",
                "extension": null,
                "job_title": null,
                "avatar": null
            },
        ],
        "developer_contacter":{
                "employee_id": 9505005,
                "display_name": "Luis Liao/WHQ/Wistron",
                "extension": null,
                "job_title": null,
                "avatar": null
        }
    }
    ```

### `PUT` Update Developer Group Detail

```text
{{service_url}}/developer_groups/:id/
```

Update partial details of a specific documents by `id`

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    id | developer_groups id (which is same as orders id)

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json
    X-CSRFToken | {{ CSRF_COOKIE_NAME }}

- BODY (raw)

    Example request

    ```json
    {
        "developer":[
            {
                "employee_id": 10612704,
                "display_name": "Jeff SH Wang/WHQ/Wistron",
            },
            {
                "employee_id": 10712714,
                "display_name": "Leo Tu/WHQ/Wistron",
            },
        ],
        "developer_contacter":{
                "employee_id": 9505005,
                "display_name": "Luis Liao/WHQ/Wistron",
        }
    }
    ```

    Example response 1

    ```json
    {
        "developer":[
            {
                "employee_id": 10612704,
                "display_name": "Jeff SH Wang/WHQ/Wistron",
                "extension": "85014815",
                "job_title": "工程師",
                "avatar": "http://www.abc.com/123.jpg"
            },
            {
                "employee_id": 10712714,
                "display_name": "Leo Tu/WHQ/Wistron",
                "extension": "85014817",
                "job_title": "工程師",
                "avatar": "http://www.abc.com/123.jpg"
            },
        ],
        "developer_contacter":{
                "employee_id": 9505005,
                "display_name": "Luis Liao/WHQ/Wistron",
                "extension": "85014833",
                "job_title": "功能經理",
                "avatar": "http://www.abc.com/123.jpg"
        }
    }
    ```

    Example response 2

    ```json
    {
        "developer":[
            {
                "employee_id": 10612704,
                "display_name": "Jeff SH Wang/WHQ/Wistron",
                "extension": null,
                "job_title": null,
                "avatar": null
            },
            {
                "employee_id": 10712714,
                "display_name": "Leo Tu/WHQ/Wistron",
                "extension": null,
                "job_title": null,
                "avatar": null
            },
        ],
        "developer_contacter":{
                "employee_id": 9505005,
                "display_name": "Luis Liao/WHQ/Wistron",
                "extension": null,
                "job_title": null,
                "avatar": null
        }
    }
    ```

---

## Employees Operation

### `GET` Search Employees with Site / Employee Id / English Name / Extension

```text
{{service_url}}/employees/?param1=value1&param2=value2...
```

Search employees resource with site/employee_id/english_name/extension

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    site__exact (option)| WNH\WZS..... | employee location
    employee_id__icontains (option)| 10612704 | employee id
    english_name__icontains (option)| Jeff SH Wang | employee english_name
    extension__icontains (option)| 4815556 | employee extension

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
        "rows":{
            [
                {
                    "employee_id": 10612704,
                    "display_name": "Jeff SH Wang/WHQ/Wistron",
                    "extension": "85014815",
                    "job_title": "工程師",
                    "avatar": "http://www.abc.com/123.jpg"
                },
                {
                    "employee_id": 10712714,
                    "display_name": "Leo Tu/WHQ/Wistron",
                    "extension": "85014817",
                    "job_title": "工程師",
                    "avatar": "http://www.abc.com/123.jpg"
                },
            ]
        }
    }
    ```

### `GET` Fetch Current My Employee's information

```text
{{service_url}}/employees/me/
```

Fetch current user detail

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
            "employee_id": 10612704,
            "display_name": "Jeff SH Wang/WHQ/Wistron",
            "extension": "85014815",
            "job_title": "工程師",
            "avatar": "http://www.abc.com/123.jpg"
        }
    ```

---

## Accounts Operation

### `GET` Fetch Accounts Collection

```text
{{service_url}}/accounts/
```

Fetch accounts collection resource

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
            {
                "id": 5,
                "name": "Sugon",
                "code": "Sami",
                "business_unit": 3,
                "project_count": 0
            },
            {
                "id": 6,
                "name": "Intel",
                "code": "Iris",
                "business_unit": 3,
                "project_count": 0
            },
        ]
    }
    ```

---

## Projects Operation

### `GET` Filter Projects Collection by Account Id

```text
{{service_url}}/projects/?param1=value1
```

Fetch projects collection resource by account id

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    acct_id (required)| 1 | account id

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
        [
            {
                "id": 1,
                "wistron_name": null,
                "customer_name": "Trinity 1U",
                "wistron_code": "C182TR2",
                "plm_code_1": "QRQY00000137",
                "plm_code_2": "6PD02A010001",
                "deleted_at": null,
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
                "id": 3,
                "wistron_name": null,
                "customer_name": "Anders4",
                "wistron_code": "A191TB1",
                "plm_code_1": "QRQY00000718",
                "plm_code_2": "5PD05L010001",
                "deleted_at": null,
                "type": "NPI",
                "status": "On-going",
                "product_line": "Server",
                "business_model": "JDM",
                "account": {
                    "id": 2,
                    "name": "HPE",
                    "code": "Apollo",
                    "business_unit": 2
                }
            },
            {
                "id": 4,
                "wistron_name": "CX 2U4N",
                "customer_name": "CX400 M6",
                "wistron_code": "G182TR3",
                "plm_code_1": "5RDZ54010001",
                "plm_code_2": "5PD05H010001",
                "deleted_at": null,
                "type": "NPI",
                "status": "On-going",
                "product_line": "Server",
                "business_model": "ODM",
                "account": {
                    "id": 14,
                    "name": "Fujitsu",
                    "code": "Yama",
                    "business_unit": 2
                }
            },
        ]
    }
    ```

---

## Department Categorys Operation

### `GET` Fetch Department Categorys Collection

```text
{{service_url}}/dept_categorys/
```

Fetch dept_categorys collection resource

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

`Orders Table`

id: IntegerField

account: CharField i.e.

project: CharField

develop_team_function: CharField i.e. EE/SW/QT/BU

develop_team_sub_function: CharField i.e. TSC/BIOS/BMC/MQT/PQT/DQMS...

status: JSONField

initator: JSONField

assigner: JSONField

develop_group: JSONField

title: CharField

description: TextField

form_begin_time: DateTimeField

form_end_time: DateTimeField

expected_develop_duration_day: FloatField

actual_develop_duration_day: FloatField

repository_url: URLField

parent: ForeignKey

---

`Histories Table`

id: IntegerField

editor: JSONField

comment: TextField

created_time: DateTimeField

orders_id: ForeignKey

---

`Document Table`

id: IntegerField

path: FileField

name: CharFiled

description: CharField

size: IntegerField

created_time: DateTimeField

order_id: ForeignKey

---

`Schedule Table`

id: IntegerField

event_name: CharField

current_time: DateTimeField

expected_time: DateTimeField

complete_rate: PositiveIntegerField

time_tracker: ArrayField

order_id: ForeignKey

---

`Employee Table` (managed=False)

employee_id: CharField

english_name: CharField

chinese_name: CharField

department_id: CharField

department_name: CharField

mail: EmailField

job_title: CharField

extension: CharField

supervisor_id: CharField

site: CharField
