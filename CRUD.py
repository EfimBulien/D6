import sqlite3
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List


app = FastAPI()


class Product(BaseModel):
    id: int = None
    name: str
    description: str
    price: float
    category: str


@app.get("/products", response_model=List[Product])
def get_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM Products').fetchall()
    conn.close()

    return [Product(**product) for product in products]


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM Products WHERE id = ?', (product_id,)).fetchone()
    conn.close()

    if product is None:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    return Product(**product)


@app.post("/products", status_code=201)
def create_product(product: Product):
    conn = get_db_connection()
    conn.execute('INSERT INTO Products (name, description, price, category) VALUES (?, ?, ?, ?)',
                 (product.name, product.description, product.price, product.category))
    conn.commit()
    conn.close()

    return {"message": "Продукт успешно создан"}


@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    conn = get_db_connection()
    conn.execute('UPDATE Products SET name = ?, description = ?, price = ?, category = ? WHERE id = ?',
                 (product.name, product.description, product.price, product.category, product_id))
    conn.commit()
    conn.close()

    return {"message": "Продукт успешно обновлен"}


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    conn = get_db_connection()
    conn.execute('DELETE FROM Products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()

    return {"message": "Продукт успешно удален"}


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9090)