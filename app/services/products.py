from sqlalchemy.orm import Session
from app.models.models import Product, Category
from app.schemas.products import ProductCreate, ProductUpdate
from app.utils.responses import ResponseHandler


class ProductService:
    @staticmethod
    def get_all_products(db: Session, page: int, limit: int, search: str = ""):
        products = db.query(Product).order_by(Product.id.asc()).filter(
            Product.title.contains(search)).limit(limit).offset((page - 1) * limit).all()
        
        # Convert products to list of dictionaries with all needed fields
        products_data = []
        for product in products:
            products_data.append({
                "id": product.id,
                "title": product.title,
                "price": product.price,
                "old_price": product.old_price if hasattr(product, 'old_price') else None,
                "category": product.category.name if product.category else "Uncategorized",
                "image_url": f"/static/images/products/{product.image}" if product.image else "/static/images/products/default.jpg",
                "rating": product.rating if hasattr(product, 'rating') else 0,
                "description": product.description
            })
        
        return {"message": f"Page {page} with {limit} products", "data": products_data}

    @staticmethod
    def get_product(db: Session, product_id: int):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            ResponseHandler.not_found_error("Product", product_id)
        return ResponseHandler.get_single_success(product.title, product_id, product)

    @staticmethod
    def create_product(db: Session, product: ProductCreate):
        category_exists = db.query(Category).filter(Category.id == product.category_id).first()
        if not category_exists:
            ResponseHandler.not_found_error("Category", product.category_id)

        product_dict = product.model_dump()
        db_product = Product(**product_dict)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return ResponseHandler.create_success(db_product.title, db_product.id, db_product)

    @staticmethod
    def update_product(db: Session, product_id: int, updated_product: ProductUpdate):
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            ResponseHandler.not_found_error("Product", product_id)

        for key, value in updated_product.model_dump().items():
            setattr(db_product, key, value)

        db.commit()
        db.refresh(db_product)
        return ResponseHandler.update_success(db_product.title, db_product.id, db_product)

    @staticmethod
    def delete_product(db: Session, product_id: int):
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            ResponseHandler.not_found_error("Product", product_id)
        db.delete(db_product)
        db.commit()
        return ResponseHandler.delete_success(db_product.title, db_product.id, db_product)
