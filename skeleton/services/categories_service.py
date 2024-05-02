from data.database import read_query, insert_query
from data.models import Category
from common.responses import CreatedSuccessfully, BadRequest


def get_all_categories() -> list[Category] or None:
    query = """select category_id, name, is_locked, is_private from categories"""
    params = ()

    data = read_query(query, params)

    categories = [Category.from_query_result(*row) for row in data]

    return categories


def get_category_by_id(category_id: int) -> Category or None:  # todo
    query = """select category_id, name, is_locked, is_private from categories where category_id = ?"""
    params = (category_id,)

    data = read_query(query, params)

    category = Category.from_query_result(*data[0])

    return category


def create_category(name: str):
    if not name:
        return BadRequest(content="Category name is required in order to create a category!")

    query = """insert into categories (name) values (?)"""
    params = (name,)

    category_id = insert_query(query, params)

    return CreatedSuccessfully(content=f"Category with id:{category_id} created successfully!")
