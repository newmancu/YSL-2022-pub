# encoding=utf8

import json
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import datetime

API_BASEURL = "https://maintaining-2085.usr.yandex-academy.ru/"

ROOT_ID = "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"

IMPORT_BATCHES = [
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "OFFER",
                "name": "jPhone 13",
                "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "price": 79999
            },
            {
                "type": "OFFER",
                "name": "Xomiа Readme 10",
                "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "price": 59999
            },
            {
                "type": "CATEGORY",
                "name": "Смартфоны",
                "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
        ],
        "updateDate": "2022-02-02T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Телевизоры",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "OFFER",
                "name": "Samson 70\" LED UHD Smart",
                "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 32999
            },
            {
                "type": "OFFER",
                "name": "Phyllis 50\" LED UHD Smarter",
                "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 49999
            }
        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "OFFER",
                "name": "Goldstar 65\" LED UHD LOL Very Smart",
                "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 69999
            }
        ],
        "updateDate": "2022-02-03T15:00:00.000Z"
    }
]

SAME_UUID = {
    "items": [
            {
                "type": "CATEGORY",
                "name": "Телевизоры",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "OFFER",
                "name": "Goldstar 65\" LED UHD LOL Very Smart",
                "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 32999
            },
            {
                "type": "OFFER",
                "name": "Samson 70\" LED UHD Smart",
                "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 100
            },
        ],
        "updateDate": "2022-02-05T12:00:00.000Z"
}

OFFER_PRICE = [
    {
    "items": [
            {
                "type": "CATEGORY",
                "name": "Телевизоры",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "OFFER",
                "name": "Goldstar 65\" LED UHD LOL Very Smart",
                "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": -100
            },
        ],
        "updateDate": "2022-02-06T12:00:00.000Z"
    },
    {
    "items": [
            {
                "type": "CATEGORY",
                "name": "Телевизоры",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "OFFER",
                "name": "Goldstar 65\" LED UHD LOL Very Smart",
                "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
        ],
        "updateDate": "2022-02-06T12:00:00.000Z"
    },
]

GOOD_OFFER_PRICE = [
    {
    "items": [
            {
                "type": "OFFER",
                "name": "Goldstar 65\" LED UHD LOL Very Smart",
                "id": "11883e11-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 0
            },
            {
                "type": "OFFER",
                "name": "Goldstar 65\" LED UHD LOL Very Smart",
                "id": "22883e22-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 123
            },
        ],
        "updateDate": "2022-02-06T12:00:00.000Z"
    },

]

CATEG_PRICE = [
    {
    "items": [
            {
                "type": "CATEGORY",
                "name": "Телевизоры",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "price": 100
            },
        ],
        "updateDate": "2022-02-07T12:00:00.000Z"
    },
    {
    "items": [
            {
                "type": "CATEGORY",
                "name": "Телевизоры",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "price": -100
            },
        ],
        "updateDate": "2022-02-08T12:00:00.000Z"
    },
]

NORM_CATEG_PRICE = {
    "items": [
            {
                "type": "CATEGORY",
                "name": "Телевизоры",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "price": None
            },
        ],
        "updateDate": "2022-02-09T12:00:00.000Z"
}

CHANGE_TYPE = {
    
    "items": [
            {
                "type": "OFFER",
                "name": "Телевизоры",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "price": 100
            },
        ],
        "updateDate": "2022-02-10T12:00:00.000Z"
}

OFFER_PARENT = [
    {
    "items": [
            {
                "type": "OFFER",
                "name": "NEW TV",
                "id": "1ca41b96-2bfe-474c-9116-d435bf5fc8f2",
                "parentId": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                "price": 100
            },
        ],
        "updateDate": "2022-02-11T12:00:00.000Z"
    },
    {
    "items": [
            {
                "type": "OFFER",
                "name": "NEW TV1",
                "id": "54a41b96-2bfe-474c-9116-d435bf5fc8f2",
                "parentId": None,
                "price": 100
            },
            {
                "type": "OFFER",
                "name": "NEW TV2",
                "id": "66666666-2bfe-474c-9116-d435bf5fc8f2",
                "parentId": "54a41b96-2bfe-474c-9116-d435bf5fc8f2",
                "price": 200
            },
        ],
        "updateDate": "2022-02-12T12:00:00.000Z"
    },
    
]

NULL_NAME = [
    {
    "items": [
            {
                "type": "OFFER",
                "name": None,
                "id": "1ca77b96-2bfe-474c-9116-d435bf5fc8f2",
                "parentId": None,
                "price": 100
            },
        ],
        "updateDate": "2022-02-13T12:00:00.000Z"
    },
    {
    "items": [
            {
                "type": "CATEGORY",
                "name": None,
                "id": "54a77b96-2bfe-474c-9116-d435bf5fc8f2",
                "parentId": None,
            },
        ],
        "updateDate": "2022-02-13T12:00:00.000Z"
    },
]

RANDOM_ORDER = {
    "items": [
            {
                "type": "OFFER",
                "name": "1 Item",
                "id": "b536444a-4f6f-4009-bfb9-37da4bea30b8",
                "parentId": "d0fb42fc-c9c2-43ad-9ca1-14ea46ce6f28",
                "price": 1233
            },
            {
                "type": "CATEGORY",
                "name": "1 Top category",
                "id": "b15be624-9913-4120-9b17-8d2251f6589a",
                "parentId": None,
            },
            {
                "type": "CATEGORY",
                "name": "1 sub category",
                "id": "d0fb42fc-c9c2-43ad-9ca1-14ea46ce6f28",
                "parentId": "b15be624-9913-4120-9b17-8d2251f6589a",
            },
            {
                "type": "CATEGORY",
                "name": "2 sub category",
                "id": "fd3215db-6e9e-4db9-b88e-ccf4c6b71630",
                "parentId": "0ed6e0c1-13cc-4849-971e-f04d8f6d64bd",
            },
            {
                "type": "CATEGORY",
                "name": "2 Top category",
                "id": "0ed6e0c1-13cc-4849-971e-f04d8f6d64bd",
                "parentId": None,
            },
            {
                "type": "CATEGORY",
                "name": "3 sub category",
                "id": "442ce7ee-6730-48ef-a982-d48d721e4a7b",
                "parentId": "0ed6e0c1-13cc-4849-971e-f04d8f6d64bd",
            },

        ],
        "updateDate": "2022-02-16T12:00:00.000Z"
}

RANDOM_TREE_ORDER = {
    "type": "CATEGORY",
    "name": "1 Top category",
    "id": "b15be624-9913-4120-9b17-8d2251f6589a",
    "price": 1233,
    "parentId": None,
    "date": "2022-02-16T12:00:00.000Z",
    "children": [
        {
        "type": "CATEGORY",
        "name": "1 sub category",
        "id": "d0fb42fc-c9c2-43ad-9ca1-14ea46ce6f28",
        "price": 1233,
        "parentId": "b15be624-9913-4120-9b17-8d2251f6589a",
        "date": "2022-02-16T12:00:00.000Z",
        "children": [
                {
                    "type": "OFFER",
                    "name": "1 Item",
                    "id": "b536444a-4f6f-4009-bfb9-37da4bea30b8",
                    "parentId": "d0fb42fc-c9c2-43ad-9ca1-14ea46ce6f28",
                    "price": 1233,
                    "date": "2022-02-16T12:00:00.000Z",
                    "children": None,
                },
            ]
        }
    ]
}

EXPECTED_TREE = {
    "type": "CATEGORY",
    "name": "Товары",
    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "price": 58599,
    "parentId": None,
    "date": "2022-02-03T15:00:00.000Z",
    "children": [
        {
            "type": "CATEGORY",
            "name": "Телевизоры",
            "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 50999,
            "date": "2022-02-03T15:00:00.000Z",
            "children": [
                {
                    "type": "OFFER",
                    "name": "Samson 70\" LED UHD Smart",
                    "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 32999,
                    "date": "2022-02-03T12:00:00.000Z",
                    "children": None,
                },
                {
                    "type": "OFFER",
                    "name": "Phyllis 50\" LED UHD Smarter",
                    "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 49999,
                    "date": "2022-02-03T12:00:00.000Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "name": "Goldstar 65\" LED UHD LOL Very Smart",
                    "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 69999,
                    "date": "2022-02-03T15:00:00.000Z",
                    "children": None
                }
            ]
        },
        {
            "type": "CATEGORY",
            "name": "Смартфоны",
            "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 69999,
            "date": "2022-02-02T12:00:00.000Z",
            "children": [
                {
                    "type": "OFFER",
                    "name": "jPhone 13",
                    "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 79999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "name": "Xomiа Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 59999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                }
            ]
        },
    ]
}


def request(path, method="GET", data=None, json_response=False):
    try:
        params = {
            "url": f"{API_BASEURL}{path}",
            "method": method,
            "headers": {},
        }

        if data:
            params["data"] = json.dumps(
                data, ensure_ascii=False).encode("utf-8")
            params["headers"]["Content-Length"] = len(params["data"])
            params["headers"]["Content-Type"] = "application/json"

        req = urllib.request.Request(**params)

        with urllib.request.urlopen(req) as res:
            res_data = res.read().decode("utf-8")
            if json_response:
                res_data = json.loads(res_data)
            return (res.getcode(), res_data)
    except urllib.error.HTTPError as e:
        return (e.getcode(), None)


def deep_sort_children(node):
    if node.get("children"):
        node["children"].sort(key=lambda x: x["id"])

        for child in node["children"]:
            deep_sort_children(child)


def print_diff(expected, response):
    with open("expected.json", "w") as f:
        json.dump(expected, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    with open("response.json", "w") as f:
        json.dump(response, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    subprocess.run(["git", "--no-pager", "diff", "--no-index",
                    "expected.json", "response.json"])


def test_import():
    for index, batch in enumerate(IMPORT_BATCHES):
        print(f"Importing batch {index}")
        status, _ = request("/imports", method="POST", data=batch)

        assert status == 200, f"Expected HTTP status code 200, got {status}"

    print("Test import passed.")


def test_nodes():
    status, response = request(f"/nodes/{ROOT_ID}", json_response=True)
    # print(json.dumps(response, indent=2, ensure_ascii=False))

    assert status == 200, f"Expected HTTP status code 200, got {status}"

    deep_sort_children(response)
    deep_sort_children(EXPECTED_TREE)
    if response != EXPECTED_TREE:
        print_diff(EXPECTED_TREE, response)
        print("Response tree doesn't match expected tree.")
        sys.exit(1)

    print("Test nodes passed.")


def test_sales():
    params = urllib.parse.urlencode({
        "date": "2022-02-04T00:00:00.000Z"
    })
    status, response = request(f"/sales?{params}", json_response=True)
    assert status == 200, f"Expected HTTP status code 200, got {status}"
    print("Test sales passed.")


def test_stats():
    params = urllib.parse.urlencode({
        "dateStart": "2022-02-01T00:00:00.000Z",
        "dateEnd": "2022-02-03T00:00:00.000Z"
    })
    status, response = request(
        f"/node/{ROOT_ID}/statistic?{params}", json_response=True)

    assert status == 200, f"Expected HTTP status code 200, got {status}"
    print("Test stats passed.")


def test_delete():
    status, _ = request(f"/delete/{ROOT_ID}", method="DELETE")
    assert status == 200, f"Expected HTTP status code 200, got {status}"

    status, _ = request(f"/nodes/{ROOT_ID}", json_response=True)
    assert status == 404, f"Expected HTTP status code 404, got {status}"

    print("Test delete passed.")


def test_import_same_uuid():
    status, _ = request("/imports", method="POST", data=SAME_UUID)

    assert status == 400, f"Expected HTTP status code 400, got {status}"

    print("Test import same uuid passed.")

def test_import_offer_price():
    for index, batch in enumerate(OFFER_PRICE):
        print((f'Offer price {index}'))
        status, _ = request("/imports", method="POST", data=batch)

        assert status == 400, f"Expected HTTP status code 400, got {status}"
    for index2, batch in enumerate(GOOD_OFFER_PRICE):
        print((f'Offer price {index+index2+1}'))
        status, _ = request("/imports", method="POST", data=batch)

        assert status == 200, f"Expected HTTP status code 200, got {status}"

    print("Test import offer price passed.")

def test_import_categ_price():
    for index, batch in enumerate(CATEG_PRICE):
        print((f'Categ price {index}'))
        status, _ = request("/imports", method="POST", data=batch)

        assert status == 400, f"Expected HTTP status code 400, got {status}"

    print((f'Categ price {index+1}'))
    status, _ = request("/imports", method="POST", data=NORM_CATEG_PRICE)

    assert status == 200, f"Expected HTTP status code 200, got {status}"

    print("Test import categ price passed.")

def test_import_change_type():
    status, _ = request("/imports", method="POST", data=CHANGE_TYPE)

    assert status == 400, f"Expected HTTP status code 400, got {status}"

    print("Test import change type passed.")

def test_import_offer_parent():
    for index, batch in enumerate(OFFER_PARENT):
        print((f'Offer parent {index}'))
        status, _ = request("/imports", method="POST", data=batch)

        assert status == 400, f"Expected HTTP status code 400, got {status}"

    print("Test import offer parent passed.")

def test_import_null_name():
    for index, batch in enumerate(NULL_NAME):
        print((f'Null name {index}'))
        status, _ = request("/imports", method="POST", data=batch)

        assert status == 400, f"Expected HTTP status code 400, got {status}"

    print("Test import null name passed.")

def test_random_order_insert():
    status, _ = request("/imports", method="POST", data=RANDOM_ORDER)

    assert status == 200, f"Expected HTTP status code 200, got {status}"

    status, response = request(f"/nodes/b15be624-9913-4120-9b17-8d2251f6589a", json_response=True)
    # print(json.dumps(response, indent=2, ensure_ascii=False))

    assert status == 200, f"Expected HTTP status code 200, got {status}"

    deep_sort_children(response)
    deep_sort_children(RANDOM_TREE_ORDER)
    if response != RANDOM_TREE_ORDER:
        print_diff(RANDOM_TREE_ORDER, response)
        print("Response tree doesn't match expected tree.")
        sys.exit(1)

    print("Test import random order passed.")

def test_cascade_delete():

    status, response = request(f"/nodes/11883e11-0507-482f-bce2-2fb306cf6483", json_response=True)
    # print(json.dumps(response, indent=2, ensure_ascii=False))

    assert status == 404, f"Expected HTTP status code 404, got {status}"
    print("Test cascade delete passed")

def test_many_inserts():
    N = 10000
    cur = datetime.datetime(2023,8,1,12,0,0,0)
    for index in range(N):
        cur2 = cur + datetime.timedelta(1)
        curf = cur2.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        print(f"Importing batch {index}")
        pdata = {
            "items": [
            {
                "type": "OFFER",
                "name": f"Item {index}",
                "id": "11773e77-0507-482f-dce2-" + str(index).zfill(12),
                "parentId": None,
                "price": index
            },
            ],
            "updateDate": curf
        }
        status, _ = request("/imports", method="POST", data=pdata)

        assert status == 200, f"Expected HTTP status code 200, got {status}"

    print("Test import passed.")

def test_all():
    # test_delete()
    test_import()
    test_nodes()
    test_sales()
    test_stats()

    test_import_same_uuid()
    test_import_offer_price()
    test_import_categ_price()
    test_import_change_type()
    test_import_offer_parent()
    test_import_null_name()
    test_random_order_insert()
    test_delete()
    test_cascade_delete()



def main():
    global API_BASEURL
    test_name = None

    for arg in sys.argv[1:]:
        if re.match(r"^https?://", arg):
            API_BASEURL = arg
        elif test_name is None:
            test_name = arg

    if API_BASEURL.endswith('/'):
        API_BASEURL = API_BASEURL[:-1]

    if test_name is None:
        for i in range(1000):
            print(i)
            test_all()
    else:
        test_func = globals().get(f"test_{test_name}")
        if not test_func:
            print(f"Unknown test: {test_name}")
            sys.exit(1)
        test_func()


if __name__ == "__main__":
    main()
