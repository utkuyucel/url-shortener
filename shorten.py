import os
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("HOST", "127.0.0.1")
port = os.getenv("PORT", "8000")
base_url = f"http://{host}:{port}"

URL_TO_SHORTEN = "https://paulgraham.com/articles.html"  # Example URL to shorten

def main():
    payload = json.dumps({"original_url": URL_TO_SHORTEN}).encode("utf-8")
    req = Request(f"{base_url}/urls", data=payload, headers={"Content-Type": "application/json"})
    try:
        with urlopen(req) as resp:
            result = json.load(resp)
            print("Short URL:", f"{base_url}/u/{result['short_path']}")
    except HTTPError as e:
        error = e.read().decode()
        print(f"Error ({e.code}): {error}")

if __name__ == "__main__":
    main()
