# CherryPy server for IUT Cafegap event

This project have no confidentiality but there is authentication to data that server receives.

To use it, you need `staff.json` and `participants.json` files.

In `staff.json` insert users that is going to use the like this example:

```
{
    "USERNAME": "PASSWORD"
    "amir": "khazaie",
    ...
}
```

In `participants.json` insert data about participants like this example:

```
{
    "ID": {
        "ATTRIBUTE_1": "VALUE_1",
        "ATTRIBUTE_2": "VALUE_2",
        "ATTRIBUTE_3": "VALUE_3",
        ...
    },
    ...
}
```

To use this server and the android application in your own event probably you need to change android and server codes.
