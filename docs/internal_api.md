# DRS API Document

## Outline

- [DRS API Document](#drs-api-document)
  - [Outline](#outline)
  - [Orders Operation](#orders-operation)
    - [`GET` Fetch Orders Collection](#get-fetch-orders-collection)
    - [`GET` Fetch a Specific Orders](#get-fetch-a-specific-orders)
    - [`POST` Create an Orders](#post-create-an-orders)
    - [`PATCH` Update a Partially Specific Orders](#patch-update-a-partially-specific-orders)
  - [Histories Operation](#histories-operation)
    - [`GET` Fetch Histories Collection by Order Id](#get-fetch-histories-collection-by-order-id)
    - [`POST` Create a Histories](#post-create-a-histories)
  - [Documents Operation](#documents-operation)
    - [`GET` Fetch a Specific Documents](#get-fetch-a-specific-documents)
    - [`PATCH` Update a Partially Specific Documents](#patch-update-a-partially-specific-documents)
  - [Assigner Operation](#assigner-operation)
    - [`GET` Fetch a Specific Assigner by department](#get-fetch-a-specific-assigner-by-department)
  - [Developer Group Operation](#developer-group-operation)
    - [`GET` Fetch a Specific Developer Group](#get-fetch-a-specific-developer-group)
    - [`PUT` Update a Specific Developer Group](#put-update-a-specific-developer-group)
  - [Person Operation](#person-operation)
    - [`GET` Search a Specific Person](#get-search-a-specific-person)
  - [Label Operation](#label-operation)
    - [`GET`  Fetch Label Collections](#get-fetch-label-collections)

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
    page_number (option) | 10 | page number
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
        "row":{
            [
                {
                    "id": 2,
                    "develop_team": "DQMS",
                    "label": "R360xxxxx",
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
                    "mvp_time": "2020-03-20T08:26:38.093183Z",
                    "expected_develop_begin_time": "2020-03-150T08:26:38.093183Z",
                    "expected_develop_end_time": "2020-04-05T08:26:38.093183Z",
                    "expected_develop_duration_day": 10.5,
                    "actual_develop_duration_day": 20.0,
                    "repository_url": "www.gitlab.com",
                    "document_1": "document_1.pdf",
                    "document_2": "document_2.pdf",
                    "document_3": "document_3.pdf",
                    "document_4": "document_4.pdf",
                    "document_5": "document_5.pdf",
                    "parent": 10,
                },
                {
                    "id": 3,
                    "develop_team": "DQMS",
                    "label": "R360xxxxx",
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
                    "mvp_time": "2020-03-20T08:26:38.093183Z",
                    "expected_develop_begin_time": "2020-03-150T08:26:38.093183Z",
                    "expected_develop_end_time": "2020-04-05T08:26:38.093183Z",
                    "expected_develop_duration_day": 10.5,
                    "actual_develop_duration_day": 20.0,
                    "repository_url": "www.gitlab.com",
                    "document_1": "document_1.pdf",
                    "document_2": "document_2.pdf",
                    "document_3": "document_3.pdf",
                    "document_4": "document_4.pdf",
                    "document_5": "document_5.pdf",
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
        "develop_team": "DQMS",
        "label": "R360xxxxx",
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
        "mvp_time": "2020-03-20T08:26:38.093183Z",
        "expected_develop_begin_time": "2020-03-150T08:26:38.093183Z",
        "expected_develop_end_time": "2020-04-05T08:26:38.093183Z",
        "expected_develop_duration_day": 10.5,
        "actual_develop_duration_day": 20.0,
        "repository_url": "www.gitlab.com",
        "parent": 10,
    }
    ```

### `POST` Create an Orders

```text
{{service_url}}/orders/?fields=develop,label,status,initiator,assigner,title,description,form_begin_time,form_end_time,mvp_time,expected_develop_begin_time,expected_develop_duration_day,repository_url,parent
```

Create a new orders

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    fields (require)| develop_team/label/status/initiator/assigner/title/description/form_begin_time/form_end_time/mvp_time/expected_develop_begin_time/expected_develop_duration_day/actual_develop_duration_day/repository_url/repository_url/parent| which fields need to be validate

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
        "develop_team": "DQMS",
        "label": "R360xxxxx",
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
        "form_begin_time": "2020-03-10T08:26:38.093183Z",
        "form_end_time": "2020-04-10T08:26:38.093183Z",
        "mvp_time": "2020-03-20T08:26:38.093183Z",
        "expected_develop_begin_time": "2020-03-150T08:26:38.093183Z",
        "expected_develop_end_time": "2020-04-05T08:26:38.093183Z",
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
        "develop_team": "DQMS",
        "label": "R360xxxxx",
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
        "mvp_time": "2020-03-20T08:26:38.093183Z",
        "expected_develop_begin_time": "2020-03-150T08:26:38.093183Z",
        "expected_develop_end_time": "2020-04-05T08:26:38.093183Z",
        "expected_develop_duration_day": 10.5,
        "actual_develop_duration_day": 20.0,
        "repository_url": "www.gitlab.com",
        "parent": 10,
    }
    ```

### `PATCH` Update a Partially Specific Orders

```text
{{service_url}}/orders/:id/?fields=develop_team,label,status,initiator,assigner,title,description
```

Update partial details of a specific orders by `id`

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    `id` | Order id

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    fields (require)| develop_team/label/status/initiator/assigner/title/description/form_begin_time/form_end_time/mvp_time/expected_develop_begin_time/expected_develop_duration_day/actual_develop_duration_day/repository_url/repository_url/parent| which fields need to be validate

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
        "develop_team": "DQMS",
        "label": "R360xxxxx",
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
        "develop_team": "DQMS",
        "label": "R360xxxxx",
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
        "mvp_time": "2020-03-20T08:26:38.093183Z",
        "expected_develop_begin_time": "2020-03-150T08:26:38.093183Z",
        "expected_develop_end_time": "2020-04-05T08:26:38.093183Z",
        "expected_develop_duration_day": 10.5,
        "actual_develop_duration_day": 20.0,
        "repository_url": "www.gitlab.com",
        "parent": 10,
    }
    ```

---

## Histories Operation

### `GET` Fetch Histories Collection by Order Id

```text
{{service_url}}/histories/?orders_id=10
```

Fetch all histories resource

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

### `POST` Create a Histories

```text
{{service_url}}/histories/
```

Create a new histories

- HEADERS

    Key|Value
    :---: | :---:
    Content-Type | application/json
    X-CSRFToken | {{ CSRF_COOKIE_NAME }}

- BODY (raw)

    Example request

    ```json
    {
        "comment": "<br>There is a comment</br>",
        "editor": {
            "employee_id": 10612704,
            "display_name": "Jeff Sh Wang/WHQ/Wistron"
        },
        "timestamp": "2020-03-20T08:26:38.093183Z",
        "orders_id": 10
    }
    ```

    Example response

    ```json
    {
        "id": 2,
        "comment": "<br>There is a comment</br>",
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

### `GET` Fetch a Specific Documents

```text
{{service_url}}/documents/:id/
```

Fetch a specific documents resource by `id`

- PATH VARIABLES
    Variable|Description
    :---: | :---:
    `id` | documents id (which is same as orders id)

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
        "document_1": "http://dqms.wistron.com/document_1.pdf",
        "document_2": "http://dqms.wistron.com/document_2.pdf",
        "document_3": "http://dqms.wistron.com/document_3.pdf",
        "document_4": "http://dqms.wistron.com/document_4.pdf",
        "document_5": "http://dqms.wistron.com/document_5.pdf",
        "document_summary": "<br>There is document summary</br>"
    }
    ```

### `PATCH` Update a Partially Specific Documents

```text
{{service_url}}/documents/:id/?fields=document_1,document_2,document_4,document_summary
```

Update partial details of a specific documents by `id`

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    id | document id (which is same as orders id)

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    fields| document_1/document_2/document_3/document_4/document_5/document_summary | field which want ot be validate

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
        "document_1": "http://dqms.wistron.com/document_1.pdf",
        "document_2": "http://dqms.wistron.com/document_2.pdf",
        "document_4": "http://dqms.wistron.com/document_4.pdf",
        "document_summary": "<br>There is document summary</br>"
    }
    ```

    Example response

    ```json
    {
        "id": 1,
        "document_1": "http://dqms.wistron.com/document_1.pdf",
        "document_2": "http://dqms.wistron.com/document_2.pdf",
        "document_3": "http://dqms.wistron.com/document_3.pdf",
        "document_4": "http://dqms.wistron.com/document_4.pdf",
        "document_5": "http://dqms.wistron.com/document_5.pdf",
        "document_summary": "<br>There is document summary</br>"
    }
    ```

---

## Assigner Operation

### `GET` Fetch a Specific Assigner by department

```text
{{service_url}}/assigner/?param1=value1
```

Fetch a specific assigner resource via query string

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    dept_name (require) | SW/TSC/DQMS/QT | department abbreviation

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
                "avatar": "http://www.abc.com/123.jpg"
            },
            {
                "employee_id": 10712714,
                "display_name": "Leo Tu/WHQ/Wistron",
                "avatar": "http://www.abc.com/123.jpg"
            },
        ]
    }
    ```

---

## Developer Group Operation

### `GET` Fetch a Specific Developer Group

```text
{{service_url}}/developer_groups/:id/
```

Fetch a specific developer_groups resource

- PATH VARIABLES

    Variable|Description
    :---: | :---:
    id | developer_groups id (which is same as orders id)

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
        "developer":[
            {
                "employee_id": 10612704,
                "display_name": "Jeff SH Wang/WHQ/Wistron",
                "avatar": "http://www.abc.com/123.jpg"
            },
            {
                "employee_id": 10712714,
                "display_name": "Leo Tu/WHQ/Wistron",
                "avatar": "http://www.abc.com/123.jpg"
            },
        ],
        "developer_contacter":{
                "employee_id": 9505005,
                "display_name": "Luis Liao/WHQ/Wistron",
                "avatar": "http://www.abc.com/123.jpg"
        }
    }
    ```

### `PUT` Update a Specific Developer Group

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
                "display_name": "Jeff SH Wang/WHQ/Wistron"
            },
            {
                "employee_id": 10712714,
                "display_name": "Leo Tu/WHQ/Wistron"
            },
        ],
        "developer_contacter":{
                "employee_id": 9505005,
                "display_name": "Luis Liao/WHQ/Wistron"
        }
    }
    ```

    Example response

    ```json
    {
        "developer":[
            {
                "employee_id": 10612704,
                "display_name": "Jeff SH Wang/WHQ/Wistron",
                "avatar": "http://www.abc.com/123.jpg"
            },
            {
                "employee_id": 10712714,
                "display_name": "Leo Tu/WHQ/Wistron",
                "avatar": "http://www.abc.com/123.jpg"
            },
        ],
        "developer_contacter":{
                "employee_id": 9505005,
                "display_name": "Luis Liao/WHQ/Wistron",
                "avatar": "http://www.abc.com/123.jpg"
        }
    }
    ```

---

## Person Operation

### `GET` Search a Specific Person

```text
{{service_url}}/person/?param1=value1&param2=value2...
```

Fetch a specific developer resource

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:
    site (require)| WHQ\WZS | developer location
    employee_id (option)| 10612704 | developer id
    employee_name (option)| Jeff SH Wang | developer name

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
                "avatar": "http://www.abc.com/123.jpg"
            },
            {
                "employee_id": 10712714,
                "display_name": "Leo Tu/WHQ/Wistron",
                "avatar": "http://www.abc.com/123.jpg"
            },
        ]
    }
    ```

---

TODO wait for customer & project list 2.0

## Label Operation

### `GET`  Fetch Label Collections

```text
{{service_url}}/label/?param1=value1&param2=value2...
```

Fetch a specific developer resource

- PARAMS

    Key|Value|Description
    :---:|:---:|:---:

---

`Orders Table`

id: IntegerField

develop_team: CharField /TSC/SQ/QT/DQMS+MMS

label: CharField /Customer

status: JSONField

initator: JSONField

assigner: JSONField

title: CharField

description: TextField

form_begin_time: DateTimeField

form_end_time: DateTimeField

mvp_time: DateTimeField

expected_develop_begin_time: DateTimeField

expected_develop_end_time: DateTimeField

expected_develop_duration_day: FloatField

actual_develop_duration_day: FloatField

document_1: FileField

document_2: FileField

document_3: FileField

document_4: FileField

document_5: FileField

document_summary: TextField

repository_url: URLField

parent: ForeignKey

owner_group: JSONField

---

`Histories Table`

id: IntegerField

editor: JSONField

comment: TextField

timestamp: DateTimeField

orders_id: ForeignKey
