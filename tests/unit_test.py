# encoding=utf8

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

from expected_and_import_trees import *

API_BASEURL = "http://127.0.0.1:8000"

ROOT_ID = "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"


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
    with open("../expected.json", "w") as f:
        json.dump(expected, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    with open("../response.json", "w") as f:
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

    assert status == 200, f"Expected HTTP status code 200, got {status}"

    deep_sort_children(response)
    deep_sort_children(EXPECTED_ROOT_AFTER_ALL_IMPORT_TREE)
    if response != EXPECTED_ROOT_AFTER_ALL_IMPORT_TREE:
        print_diff(EXPECTED_ROOT_AFTER_ALL_IMPORT_TREE, response)
        print("Response tree doesn't match expected tree.")
        sys.exit(1)

    print("Test nodes passed.")


def test_updates():
    params = urllib.parse.urlencode({
        "date": "2022-02-04T00:00:00Z"
    })
    status, response = request(f"/updates?{params}", json_response=True)
    assert status == 200, f"Expected HTTP status code 200, got {status}"
    print("Test updates passed.")


def test_updates_after_import_batches_for_update():
    for index, batch in enumerate(IMPORT_BATCHES_FOR_UPDATE):
        print(f"Importing batch for update test {index}")
        status, _ = request("/imports", method="POST", data=batch)

        assert status == 200, f"Expected HTTP status code 200, got {status}"

    print("Test import for update test passed.")

    params = urllib.parse.urlencode({
        "date": "2022-03-03T13:00:00Z"
    })

    status, response = request(f"/updates?{params}", method="GET", json_response=True)
    assert status == 200, f"Expected HTTP status code 200, got {status}"

    response["items"].sort(key=lambda x: x["id"])
    EXPECTED_TREE_AFTER_IMPORT_BATCHES_FOR_UPDATE['items'].sort(key=lambda x: x["id"])
    if response != EXPECTED_TREE_AFTER_IMPORT_BATCHES_FOR_UPDATE:
        print_diff(EXPECTED_TREE_AFTER_IMPORT_BATCHES_FOR_UPDATE, response)
        print("Response tree doesn't match expected tree.")
        sys.exit(1)

    print("Test updates after import batches for update passed.")


def test_history():
    params = urllib.parse.urlencode({
        "dateStart": "2022-02-01T00:00:00Z",
        "dateEnd": "2022-02-03T00:00:00Z"
    })
    status, response = request(
        f"/node/{ROOT_ID}/history?{params}", json_response=True)
    assert status == 200, f"Expected HTTP status code 200, got {status}"
    print("Test stats passed.")


def test_file_delete():
    params = urllib.parse.urlencode({
        "date": "2022-02-04T00:00:00Z"
    })
    ENTITY_ID = '863e1a7a-1304-42ae-943b-179184c077e3'
    status, _ = request(f"/delete/863e1a7a-1304-42ae-943b-179184c077e3?{params}", method="DELETE")
    assert status == 200, f"Expected HTTP status code 200, got {status}"

    status, response = request(f"/nodes/{ROOT_ID}", json_response=True)
    assert status == 200, f"Expected HTTP status code 200, got {status}"

    deep_sort_children(response)
    deep_sort_children(EXPECTED_FILE_DELETE_TREE)
    if response != EXPECTED_FILE_DELETE_TREE:
        print_diff(EXPECTED_FILE_DELETE_TREE, response)
        print("Response tree doesn't match expected tree.")
        sys.exit(1)

    status, _ = request(f"/nodes/{ENTITY_ID}", json_response=True)
    assert status == 404, f"Expected HTTP status code 404, got {status}"

    print("Test file delete passed.")


def test_folder_delete():
    params = urllib.parse.urlencode({
        "date": "2022-02-04T00:00:00Z"
    })

    ENTITY_ID = 'd515e43f-f3f6-4471-bb77-6b455017a2d2'
    status, _ = request(f"/delete/{ENTITY_ID}?{params}", method="DELETE")
    assert status == 200, f"Expected HTTP status code 200, got {status}"

    status, response = request(f"/nodes/{ROOT_ID}", json_response=True)
    assert status == 200, f"Expected HTTP status code 200, got {status}"

    deep_sort_children(response)
    deep_sort_children(EXPECTED_FOLDER_DELETE_TREE)
    if response != EXPECTED_FOLDER_DELETE_TREE:
        print_diff(EXPECTED_FOLDER_DELETE_TREE, response)
        print("Response tree doesn't match expected tree.")
        sys.exit(1)

    status, _ = request(f"/nodes/{ENTITY_ID}", json_response=True)
    assert status == 404, f"Expected HTTP status code 404, got {status}"

    print("Test folder delete passed.")


def test_root_delete():
    params = urllib.parse.urlencode({
        "date": "2022-02-04T00:00:00Z"
    })
    status, _ = request(f"/delete/{ROOT_ID}?{params}", method="DELETE")
    assert status == 200, f"Expected HTTP status code 200, got {status}"

    status, _ = request(f"/nodes/{ROOT_ID}", json_response=True)
    assert status == 404, f"Expected HTTP status code 404, got {status}"

    print("Test root delete passed.")


def test_all():
    test_import()  # заполнение
    test_nodes()
    test_updates()
    test_history()
    test_file_delete()
    test_root_delete()  # очистка
    test_import()  # заполнение
    test_folder_delete()
    test_root_delete()  # очистка
    test_import()  # заполнение
    test_updates_after_import_batches_for_update()
    test_root_delete()  # очистка


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

    print(f"Testing API on {API_BASEURL}")

    if test_name is None:
        test_all()
    else:
        test_func = globals().get(f"test_{test_name}")
        if not test_func:
            print(f"Unknown test: {test_name}")
            sys.exit(1)
        test_func()


if __name__ == "__main__":
    main()
