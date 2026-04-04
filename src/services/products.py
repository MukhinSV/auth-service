from src.exceptions import NoDataForUpdateException, ProductNotFoundException
from src.fake_db.products import products_db
from src.schemas.products import Product, ProductCreate, ProductUpdate, \
    ProductUpdatePartly


class ProductService:
    @staticmethod
    def _next_id() -> int:
        if not products_db:
            return 1
        return max(products_db) + 1

    @staticmethod
    def get_products() -> list[Product]:
        return [Product(**product_data) for product_data in
                products_db.values()]

    @staticmethod
    def get_product(product_id: int) -> Product:
        product = products_db.get(product_id)
        if product is None:
            raise ProductNotFoundException
        return Product(**product)

    @classmethod
    def create_product(cls, product_data: ProductCreate) -> Product:
        product_id = cls._next_id()
        product = Product(id=product_id, **product_data.model_dump())
        products_db[product_id] = product.model_dump()
        return product

    @staticmethod
    def update_product(product_id: int,
                       product_data: ProductUpdate) -> Product:
        if product_id not in products_db:
            raise ProductNotFoundException
        product = Product(id=product_id, **product_data.model_dump())
        products_db[product_id] = product.model_dump()
        return product

    @staticmethod
    def update_product_partly(
            product_id: int,
            product_data: ProductUpdatePartly
    ) -> Product:
        if product_id not in products_db:
            raise ProductNotFoundException
        update_data = product_data.model_dump(exclude_unset=True)
        if not update_data:
            raise NoDataForUpdateException
        products_db[product_id].update(update_data)
        return Product(**products_db[product_id])

    @staticmethod
    def delete_product(product_id: int) -> None:
        if product_id not in products_db:
            raise ProductNotFoundException
        del products_db[product_id]
