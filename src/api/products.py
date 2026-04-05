from fastapi import APIRouter, Depends

from src.dependencies import require_permission, require_roles, UserIdDep
from src.exceptions import NoDataForUpdateException, \
    NoDataForUpdateHTTPException, ProductNotFoundHTTPException
from src.schemas.products import ProductCreate, ProductUpdate, \
    ProductUpdatePartly, AddProductToCartRequest
from src.services.products import ProductService, ProductNotFoundException

router = APIRouter(prefix="/products", tags=["Товары"])


@router.get(
    "",
    summary="Получить список товаров"
)
async def get_products():
    return ProductService.get_products()


@router.get(
    "/cart",
    summary="Посмотреть корзину",
    dependencies=[Depends(require_roles("USER", "MANAGER", "ADMIN"))]
)
async def get_cart(user_id: UserIdDep):
    return ProductService.get_cart(user_id)


@router.get(
    "/{product_id}",
    summary="Получить товар по id"
)
async def get_product(product_id: int):
    try:
        return ProductService.get_product(product_id)
    except ProductNotFoundException:
        raise ProductNotFoundHTTPException


@router.post(
    "/cart/{product_id}",
    summary="Добавить товар в корзину",
    dependencies=[Depends(require_roles("USER", "MANAGER", "ADMIN"))]
)
async def add_product_to_cart(
        product_id: int,
        cart_item_data: AddProductToCartRequest,
        user_id: UserIdDep
):
    try:
        return ProductService.add_product_to_cart(
            user_id,
            product_id,
            cart_item_data
        )
    except ProductNotFoundException:
        raise ProductNotFoundHTTPException


@router.post(
    "",
    summary="Добавить товар",
    dependencies=[Depends(require_permission("products.manage"))]
)
async def create_product(product_data: ProductCreate):
    return ProductService.create_product(product_data)


@router.put(
    "/{product_id}",
    summary="Полностью обновить товар",
    dependencies=[Depends(require_permission("products.manage"))]
)
async def update_product(product_id: int, product_data: ProductUpdate):
    try:
        return ProductService.update_product(product_id, product_data)
    except ProductNotFoundException:
        raise ProductNotFoundHTTPException


@router.patch(
    "/{product_id}",
    summary="Частично обновить товар",
    dependencies=[Depends(require_permission("products.manage"))]
)
async def update_product_partly(
        product_id: int,
        product_data: ProductUpdatePartly
):
    try:
        return ProductService.update_product_partly(product_id, product_data)
    except ProductNotFoundException:
        raise ProductNotFoundHTTPException
    except NoDataForUpdateException:
        raise NoDataForUpdateHTTPException


@router.delete(
    "/{product_id}",
    summary="Удалить товар",
    dependencies=[Depends(require_permission("products.manage"))]
)
async def delete_product(product_id: int):
    try:
        ProductService.delete_product(product_id)
    except ProductNotFoundException:
        raise ProductNotFoundHTTPException
    return {"detail": "Товар успешно удалён"}
