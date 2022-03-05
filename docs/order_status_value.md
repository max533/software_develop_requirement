# Order Status Value in mutilple stage

## Outline

- [Order Status Value in mutilple stage](#order-status-value-in-mutilple-stage)
  - [Outline](#outline)
  - [P0 Stage](#p0-stage)
  - [P1 Stage](#p1-stage)
  - [P2 Stage](#p2-stage)
  - [P3 Stage](#p3-stage)
  - [P4 Stage](#p4-stage)
  - [P5 Stage](#p5-stage)

## P0 Stage

```json
// Signed : True
{
    "P0": {
        "initiator":"Approve"
    },
    "signed": true,
}

{
    "P0": {
        "initiator":"Close"
    },
    "signed": true,
}

// Signed : False

{
    "P0": {
        "initiator":"Approve"
    },
    "signed": false,
}

{
    "P0": {
        "initiator":"Close"
    },
    "signed": false,
}

```

## P1 Stage

```json
{
    "P1":{
        "10612704": ""
    }
}

{
    "P1":{
        "10612704": "Approve"
    }
}

{
    "P1":{
        "10612704": "Return"
    }
}

{
    "P1":{
        "10612704": "Close"
    }
}
```

## P2 Stage

```json
{
    "P2":{
        "assigner": ""
    }
}

{
    "P2":{
        "assigner": "Approve"
    }
}

{
    "P2":{
        "assigner": "Close"
    }
}

{
    "P2":{
        "assigner": "Return"
    }
}

```

## P3 Stage

```json
// Signed : True

{
    "P3":{
        "assigner": "",
        "initiator": "",
        "developer": ""
    },
    "signed": true,
}

{
    "P3":{
        "assigner": "Approve",
        "initiator": "",
        "developer": ""
    },
    "signed": true,
}

{
    "P3":{
        "assigner": "Approve",
        "initiator": "Approve",
        "developer": ""
    },
    "signed": true,
}

{
    "P3":{
        "assigner": "Approve",
        "initiator": "Approve",
        "developer": "Approve"
    },
    "signed": true,
}

{
    "P3":{
        "assigner": "Approve",
        "initiator": "Approve",
        "developer": "Return"
    },
    "signed": true,
}

{
    "P3":{
        "assigner": "Approve",
        "initiator": "Return",
        "developer": ""
    },
    "signed": true,
}

{
    "P3":{
        "assigner": "Approve",
        "initiator": "",
        "developer": "Return"
    },
    "signed": true,
}

{
    "P3":{
        "assigner": "Close"
    },
    "signed": true,
}

// Signed : False

{
    "P3":{
        "assigner": "",
        "initiator": "",
        "developer": ""
    },
    "signed": false,
}

{
    "P3":{
        "assigner": "Approve",
        "initiator": "",
        "developer": ""
    },
    "signed": false,
}

{
    "P3":{
        "assigner": "Approve",
        "initiator": "Approve",
        "developer": ""
    },
    "signed": false,
}

{
    "P3":{
        "assigner": "Approve",
        "initiator": "Approve",
        "developer": "Approve"
    },
    "signed": false,
}

{
    "P3":{
        "assigner": "Approve",
        "initiator": "Approve",
        "developer": "Return"
    },
    "signed": false,
}

{
    "P3":{
        "assigner": "Approve",
        "initiator": "Return",
        "developer": ""
    },
    "signed": false,
}

{
    "P3":{
        "assigner": "Approve",
        "initiator": "",
        "developer": "Return"
    },
    "signed": false,
}

{
    "P3":{
        "assigner": "Close"
    },
    "signed": false,
}

```

## P4 Stage

```json
{
    "P4": {
        "9505005": ""
    }
}

{
    "P4": {
        "9505005": "Approve"
    }
}

{
    "P4": {
        "9505005": "Return"
    }
}

{
    "P4": {
        "9505005": "Close"
    }
}
```

## P5 Stage

```json
{
    "P5": {
        "developer": ""
    }
}

{
    "P5": {
        "developer": "Approve"
    }
}

{
    "P5": {
        "initiator": "Approve"
    }
}

{
    "P5": {
        "initiator": "Return"
    }
}

{
    "P5": {
        "initiator": "Close"
    }
}
```
