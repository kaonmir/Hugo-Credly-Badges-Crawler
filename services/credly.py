from bs4 import BeautifulSoup
import requests
import re

from settings import (
    CREDLY_SORT,
    CREDLY_USER,
    CREDLY_BASE_URL,
    BADGE_SIZE,
    NUMBER_LAST_BADGES,
)


uuid_to_url = {
    # CKS
    "9945dfcb-1cca-4529-85e6-db1be3782210": "https://www.cncf.io/wp-content/uploads/2020/11/kubernetes-security-specialist-logo.svg",
    # Add more UUID to URL mappings as needed
}


def convert_image_fancier(img):
    regex = r"https:\/\/images\.credly\.com\/size\/\d+x\d+\/images\/(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})\/.+"
    match = re.search(regex, img)
    if not match:
        raise Exception("Image not found")

    uuid = match.group(1)
    return uuid_to_url.get(uuid, img)


class Credly:
    def __init__(self, f=None):
        self.FILE = f
        self.BASE_URL = CREDLY_BASE_URL
        self.USER = CREDLY_USER
        self.SORT = CREDLY_SORT

    def data_from_html(self):
        if self.FILE:
            with open(self.FILE, "r") as f:
                return f.read()

        url = f"{self.BASE_URL}/users/{self.USER}/badges?sort={self.sort_by()}"
        response = requests.get(url)
        return response.text

    def sort_by(self):
        return "most_popular" if self.SORT == "POPULAR" else "-state_updated_at"

    def convert_to_dict(self, htmlBadge):
        soupBadge = BeautifulSoup(str(htmlBadge), "lxml")
        img = soupBadge.findAll(
            "img", {"class": "cr-standard-grid-item-content__image"}
        )[0]
        return {
            "title": htmlBadge["title"],
            "href": self.BASE_URL + htmlBadge["href"],
            "img": convert_image_fancier(
                img["src"].replace("110x110", f"{BADGE_SIZE}x{BADGE_SIZE}")
            ),
        }

    def return_badges_html(self):
        data = self.data_from_html()
        soup = BeautifulSoup(data, "lxml")
        return soup.findAll("a", {"class": "cr-public-earned-badge-grid-item"})

    def get_json(self):
        badges_html = (
            self.return_badges_html()[0:NUMBER_LAST_BADGES]
            if NUMBER_LAST_BADGES > 0
            else self.return_badges_html()
        )
        return {"badges": [self.convert_to_dict(badge) for badge in badges_html]}
