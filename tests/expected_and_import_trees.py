IMPORT_BATCHES = [
    {
        "items": [
            {
                "type": "FOLDER",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None
            }
        ],
        "updateDate": "2022-02-01T12:00:00Z"
    },
    {
        "items": [
            {
                "type": "FOLDER",
                "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "FILE",
                "url": "/file/url1",
                "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "size": 128
            },
            {
                "type": "FILE",
                "url": "/file/url2",
                "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "size": 256
            }
        ],
        "updateDate": "2022-02-02T12:00:00Z"
    },
    {
        "items": [
            {
                "type": "FOLDER",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "FILE",
                "url": "/file/url3",
                "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "size": 512
            },
            {
                "type": "FILE",
                "url": "/file/url4",
                "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "size": 1024
            }
        ],
        "updateDate": "2022-02-03T12:00:00Z"
    },
    {
        "items": [
            {
                "type": "FILE",
                "url": "/file/url5",
                "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "size": 64
            }
        ],
        "updateDate": "2022-02-03T15:00:00Z"
    }
]

EXPECTED_ROOT_AFTER_ALL_IMPORT_TREE = {
    "type": "FOLDER",
    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "size": 1984,
    "url": None,
    "parentId": None,
    "date": "2022-02-03T15:00:00Z",
    "children": [
        {
            "type": "FOLDER",
            "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "size": 1600,
            "url": None,
            "date": "2022-02-03T15:00:00Z",
            "children": [
                {
                    "type": "FILE",
                    "url": "/file/url3",
                    "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "size": 512,
                    "date": "2022-02-03T12:00:00Z",
                    "children": None,
                },
                {
                    "type": "FILE",
                    "url": "/file/url4",
                    "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "size": 1024,
                    "date": "2022-02-03T12:00:00Z",
                    "children": None
                },
                {
                    "type": "FILE",
                    "url": "/file/url5",
                    "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "size": 64,
                    "date": "2022-02-03T15:00:00Z",
                    "children": None
                }
            ]
        },
        {
            "type": "FOLDER",
            "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "size": 384,
            "url": None,
            "date": "2022-02-02T12:00:00Z",
            "children": [
                {
                    "type": "FILE",
                    "url": "/file/url1",
                    "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "size": 128,
                    "date": "2022-02-02T12:00:00Z",
                    "children": None
                },
                {
                    "type": "FILE",
                    "url": "/file/url2",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "size": 256,
                    "date": "2022-02-02T12:00:00Z",
                    "children": None
                }
            ]
        },
    ]
}

EXPECTED_FILE_DELETE_TREE = {
    "type": "FOLDER",
    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "size": 1856,
    "url": None,
    "parentId": None,
    "date": "2022-02-04T00:00:00Z",
    "children": [
        {
            "type": "FOLDER",
            "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "size": 1600,
            "url": None,
            "date": "2022-02-03T15:00:00Z",
            "children": [
                {
                    "type": "FILE",
                    "url": "/file/url3",
                    "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "size": 512,
                    "date": "2022-02-03T12:00:00Z",
                    "children": None,
                },
                {
                    "type": "FILE",
                    "url": "/file/url4",
                    "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "size": 1024,
                    "date": "2022-02-03T12:00:00Z",
                    "children": None
                },
                {
                    "type": "FILE",
                    "url": "/file/url5",
                    "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "size": 64,
                    "date": "2022-02-03T15:00:00Z",
                    "children": None
                }
            ]
        },
        {
            "type": "FOLDER",
            "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "size": 256,
            "url": None,
            "date": "2022-02-04T00:00:00Z",
            "children": [
                {
                    "type": "FILE",
                    "url": "/file/url2",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "size": 256,
                    "date": "2022-02-02T12:00:00Z",
                    "children": None
                }
            ]
        },
    ]
}

EXPECTED_FOLDER_DELETE_TREE = {
    "type": "FOLDER",
    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "size": 1600,
    "url": None,
    "parentId": None,
    "date": "2022-02-04T00:00:00Z",
    "children": [
        {
            "type": "FOLDER",
            "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "size": 1600,
            "url": None,
            "date": "2022-02-03T15:00:00Z",
            "children": [
                {
                    "type": "FILE",
                    "url": "/file/url3",
                    "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "size": 512,
                    "date": "2022-02-03T12:00:00Z",
                    "children": None,
                },
                {
                    "type": "FILE",
                    "url": "/file/url4",
                    "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "size": 1024,
                    "date": "2022-02-03T12:00:00Z",
                    "children": None
                },
                {
                    "type": "FILE",
                    "url": "/file/url5",
                    "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "size": 64,
                    "date": "2022-02-03T15:00:00Z",
                    "children": None
                }
            ]
        }
    ]
}

IMPORT_BATCHES_FOR_UPDATE = [
    {
        "items": [
            {
                "type": "FOLDER",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None
            }
        ],
        "updateDate": "2022-03-01T12:00:00Z"
    },
    {
        "items": [
            {
                "type": "FOLDER",
                "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "FILE",
                "url": "/file/url1",
                "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "size": 128
            },
            {
                "type": "FILE",
                "url": "/file/url2",
                "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "size": 256
            }
        ],
        "updateDate": "2022-03-02T12:00:00Z"
    },
    {
        "items": [
            {
                "type": "FOLDER",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "FILE",
                "url": "/file/url3",
                "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "size": 512
            },
            {
                "type": "FILE",
                "url": "/file/url4",
                "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "size": 1024
            }
        ],
        "updateDate": "2022-03-03T12:00:00Z"
    },
    {
        "items": [
            {
                "type": "FILE",
                "url": "/file/url1new",
                "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "size": 128
            },
        ],
        "updateDate": "2022-03-03T13:00:00Z"
    },
    {
        "items": [
            {
                "type": "FILE",
                "url": "/file/url3new",
                "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "size": 512
            },
        ],
        "updateDate": "2022-03-03T20:00:00Z"
    },
    {
        "items": [
            {
                "type": "FILE",
                "url": "/file/url5",
                "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "size": 64
            }
        ],
        "updateDate": "2022-03-04T15:00:00Z"
    }
]

EXPECTED_TREE_AFTER_IMPORT_BATCHES_FOR_UPDATE = {
    "items": [
        {
            "type": "FILE",
            "url": "/file/url1new",
            "id": "863e1a7a-1304-42ae-943b-179184c077e3",
            "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "size": 128,
            "date": "2022-03-03T13:00:00Z"
        },
        {
            "type": "FILE",
            "url": "/file/url4",
            "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
            "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
            "size": 1024,
            "date": "2022-03-03T12:00:00Z"
        }
    ]
}
