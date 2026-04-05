from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int


class ProductUpdate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int


class ProductUpdatePartly(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    quantity: int | None = None


class CartItem(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int


class AddProductToCartRequest(BaseModel):
    quantity: int = Field(default=1, gt=0)


class Cart(BaseModel):
    user_id: int
    items: list[CartItem]
    total_price: float
