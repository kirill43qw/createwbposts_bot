from typing import List, Optional

from pydantic import BaseModel, field_validator


class Price(BaseModel):
    total: int


class Sizes(BaseModel):
    price: Optional[Price] = None


class Item(BaseModel):
    id: int
    name: str
    sizes: List[Sizes]
    image_url: str = None
    item_url: str = None

    @field_validator("sizes", mode="before")
    def valid_price(cls, sizes):
        return [size for size in sizes if size.get("price")]

    @property
    def total(self) -> Optional[int]:
        for size in self.sizes:
            if size.price:
                return int(size.price.total) // 100
        return None

    def __str__(self):
        return f"id={self.id} name='{self.name}' price='{self.total}', image_url={self.image_url}, item_url={self.item_url}"
