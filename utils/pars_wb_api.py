import requests
from pydantic import ValidationError

from utils.schema import Item
from utils.utils import get_basket


def parse_wb_card(article):
    response = requests.get(
        f"https://card.wb.ru/cards/v2/detail?curr=rub&dest=-3626404&nm={article}",
    )
    if not bool(response.json().get("data").get("products")[0].get("totalQuantity")):
        return None

    basket = get_basket(article)
    image_url = f"https://basket-{basket}.wbbasket.ru/vol{int(article)//100000}/part{int(article)//1000}/{int(article)}/images/big/1.webp"
    item_url = f"https://www.wildberries.ru/catalog/{article}/detail.aspx"

    try:
        result = Item.model_validate(response.json().get("data").get("products")[0])
        result.image_url, result.item_url = image_url, item_url
    except ValidationError as e:
        print(e, "\nчто-то не так с данными!")
    else:
        return result


if __name__ == "__main__":
    import argparse
    import sys

    def createParser():
        parser = argparse.ArgumentParser()
        parser.add_argument("name", nargs="+")
        return parser

    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    i = 1
    for art in namespace.name:
        print(i, "*" * 60)
        print(parse_wb_card(art))
        # print(parse(art).sizes[0].price.total)
        i += 1
    # print(parse(namespace.name))
