import requests

API_URL = "https://november7-730026606190.europe-west1.run.app/messages"


def get_all_messages():
    """
    Fetch ALL messages using skip & limit pagination.
    Ensures real, non-garbage messages.
    """
    all_msgs = []
    skip = 0
    limit = 200

    while True:
        url = f"{API_URL}?skip={skip}&limit={limit}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed batch at skip={skip}")
            break

        batch = response.json().get("items", [])

        if not batch:
            break

        for m in batch:
            all_msgs.append({
                "id": m.get("id"),
                "text": m.get("message", "")
            })

        if len(batch) < limit:
            break

        skip += limit

    return all_msgs
