import requests

def internet_available(timeout=3) -> bool:
    try:
        requests.get("https://www.google.com/generate_204", timeout=timeout)
        return True
    except requests.RequestException:
        return False
