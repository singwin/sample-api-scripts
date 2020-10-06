import random
import requests
import string
import urllib3


def check_response(r: requests.Response) -> None:
    assert (
        r.status_code == 200
    ), f"{r.url} returned HTTP {r.status_code} {r.text}"


def check_var(val: str) -> bool:
    return val is not None and val != "" and "example" not in val


def check_url(url: str) -> bool:
    return check_var(url) and url.startswith("https://")


def random_string(length: int = 20) -> str:
    choices = string.ascii_letters + string.digits
    return "".join(random.choice(choices) for i in range(length))


def check_wallet_url(url: str) -> str:
    if url is None:
        return str
    for suffix in ["/api/v1/", "/api/v1", "/"]:
        if url.endswith(suffix):
            print(
                f"There's no need to add \"{suffix}\" to WALLETSERVER_URL. "
                "Removing it.")
            url = url[:-len(suffix)]
    return url
