import pydantic
import requests

import models


def parse(article):
    short_id = int(article) // 100000
    match short_id:
        case _ if 0 <= short_id <= 143:
            basket = "01"
        case _ if 144 <= short_id <= 287:
            basket = "02"
        case _ if 288 <= short_id <= 431:
            basket = "03"
        case _ if 432 <= short_id <= 719:
            basket = "04"
        case _ if 720 <= short_id <= 1007:
            basket = "05"
        case _ if 1008 <= short_id <= 1061:
            basket = "06"
        case _ if 1062 <= short_id <= 1115:
            basket = "07"
        case _ if 1116 <= short_id <= 1169:
            basket = "08"
        case _ if 1170 <= short_id <= 1313:
            basket = "09"
        case _ if 1314 <= short_id <= 1601:
            basket = "10"
        case _ if 1602 <= short_id <= 1655:
            basket = "11"
        case _ if 1656 <= short_id <= 1919:
            basket = "12"
        case _ if 1920 <= short_id <= 2045:
            basket = "13"
        case _ if 2046 <= short_id <= 2189:
            basket = "14"
        case _ if 2190 <= short_id <= 2405:
            basket = "15"
        case _:
            basket = "16"

    response = requests.get(
        f"https://card.wb.ru/cards/v2/detail?curr=rub&dest=-3626404&nm={article}",
    )

    if not bool(response.json().get("data").get("products")[0].get("totalQuantity")):
        # if not response.json().get("data").get("products")[0].get("sizes")[0].get("price"):
        return None
    image_url = f"https://basket-{basket}.wbbasket.ru/vol{int(article)//100000}/part{int(article)//1000}/{int(article)}/images/big/1.webp"
    item_url = f"https://www.wildberries.ru/catalog/{article}/detail.aspx"

    try:
        result = models.Item.model_validate(
            response.json().get("data").get("products")[0]
        )
        result.image_url, result.item_url = image_url, item_url
    except pydantic.ValidationError as e:
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
        print(parse(art))
        # print(parse(art).sizes[0].price.total)
        i += 1
    # print(parse(namespace.name))
