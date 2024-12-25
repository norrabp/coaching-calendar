import requests
import json
from client import FlaskAPIClient


def main():
    # Initialize client
    client = FlaskAPIClient()

    try:
        # Login as root
        client.login("root@root.com", "rootroot")

        print("Clearing database...")
        clear_db_response = client.clear_db()
        print(json.dumps(clear_db_response, indent=2))

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
