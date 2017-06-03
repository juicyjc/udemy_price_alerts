import requests
import re
import uuid
import models.items.constants as ItemConstants
from models.stores.store import Store
from common.database import Database
from bs4 import BeautifulSoup

__author__ = 'jc'


class Item(object):
    def __init__(self, name, url, price=None, _id=None):
        self.name = name
        self.url = url
        store = Store.find_by_url(url)
        self.tag_name = store.tag_name
        self.query = store.query
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self):
        # https://www.amazon.com/Canon-Frame-Full-HD-Digital-Camera/dp/B007FGYZFI/ref=sr_1_3
        # <span id="priceblock_ourprice" class="a-size-medium a-color-price">$2,499.00</span>

        # http://www.johnlewis.com/house-by-john-lewis-hinton-office-chair/p2083183?colour=Grey
        # "span", {"itemprop": "price", "class": "now-price"}

        url = self.url
        request = requests.get(url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()

        pattern = re.compile("(\d+.\d+)")
        match = pattern.search(string_price)
        self.price = float(match.group())
        return self.price

    def save_to_mongo(self):
        # Insert JSON representation
        Database.update(ItemConstants.COLLECTION, {'_id': self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url": self.url,
            "price": self.price
        }

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": item_id}))
