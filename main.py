from dataclasses import dataclass
import os
import random
import sys
import time
from typing import Literal

import requests


ENDPOINT = "https://7tv.io/v3/gql"


@dataclass
class UserCosmetic:
    id: str
    kind: Literal["PAINT", "BADGE"]
    selected: bool


def fetch_user_cosmetics() -> list[UserCosmetic]:
    query = """
        query GetUserCosmetics($id: ObjectID!) {
            user(id: $id) {
                cosmetics {
                    id
                    kind
                    selected
                }
            }
        }
    """
    variables = {"id": os.environ["USER_ID"]}
    payload = {"query": query, "variables": variables}
    try:
        response = requests.post(url=ENDPOINT, json=payload)
        response.raise_for_status()
    except requests.Timeout:
        print("Fetching paints timed out, trying again later")
    except Exception as e:
        print(f"Something went wrong fetching paints: {e}")
        sys.exit(1)
    data = response.json()
    if "errors" in data:
        print(f"An error occured while fetching paints: {data['errors'][0]['message']}")
        sys.exit(1)
    return [UserCosmetic(**cosmetic) for cosmetic in data["data"]["user"]["cosmetics"]]


def change_paint(paint_id: str) -> None:
    query = """
        mutation UpdateUserCosmetics($user_id: ObjectID!, $update: UserCosmeticUpdate!) {
            user(id: $user_id) {
                cosmetics(update: $update)
            }
        }
        """
    variables = {
        "user_id": os.environ["USER_ID"],
        "update": {"id": paint_id, "kind": "PAINT", "selected": True},
    }
    payload = {"query": query, "variables": variables}
    headers = {"Authorization": "Bearer " + os.environ["TOKEN"]}

    try:
        response = requests.post(url=ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
    except requests.Timeout:
        print("Changing paint timed out, trying again later")
    except Exception as e:
        print(f"Something went wrong updating paints: {e}")
        sys.exit(1)
    data = response.json()
    if "errors" in data:
        print(f"An error occured while updating paints: {data['errors'][0]['message']}")
        sys.exit(1)


def main() -> None:
    if "USER_ID" not in os.environ or os.environ["USER_ID"] == "":
        print("User id is missing from .env")
        return
    if "TOKEN" not in os.environ or os.environ["TOKEN"] == "":
        print("Token is missing from .env")
        return

    try:
        interval = max(10, int(sys.argv[1]))
    except (IndexError, ValueError):
        interval = 300

    while True:
        cosmetics = fetch_user_cosmetics()
        paints = [cosmetic for cosmetic in cosmetics if cosmetic.kind == "PAINT"]
        if len(paints) == 0:
            print("You don't own any paints")
            return
        random_paint = random.choice([paint for paint in paints if not paint.selected])
        change_paint(random_paint.id)
        time.sleep(interval)


if __name__ == "__main__":
    main()
