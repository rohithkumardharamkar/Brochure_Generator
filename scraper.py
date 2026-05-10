import requests

from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}


def fetch_website_content(url):

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        soup = BeautifulSoup(
            response.text,
            "lxml"
        )

        for script in soup([
            "script",
            "style",
            "noscript"
        ]):
            script.extract()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        return text[:1500]

    except Exception as e:

        print(
            f"Error fetching content from {url}: {e}"
        )

        return "Unable to fetch website content."