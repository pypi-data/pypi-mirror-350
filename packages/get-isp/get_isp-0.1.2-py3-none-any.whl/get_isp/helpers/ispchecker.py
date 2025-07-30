import requests
from bs4 import BeautifulSoup
import re


def get_isp_info(telephone_number):
    result = None

    telephone_number = (
        "+66" + telephone_number[1:]
        if telephone_number.startswith("0")
        else telephone_number
    )

    url = f"https://whocalld.com/{telephone_number}"
    headers = {"Host": "whocalld.com", "User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 404:
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            page_div = soup.find("div", {"class": "page"})
            if page_div:
                p_tag = page_div.find("p")
                if p_tag:
                    text = p_tag.text.strip()
                    match = re.search(
                        r"carrier for this number is ([A-Za-z0-9\s\-]+?)(?: in Thailand|\.|$)",
                        text,
                    )
                    if match:
                        result = match.group(1).strip()
    except Exception as e:
        result = None

    return result
