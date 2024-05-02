from data.database import read_query, insert_query
from data.models import Category, Topic
from common.responses import CreatedSuccessfully, BadRequest


def get_all_categories() -> list[Category] or None:
    query = """select category_id, name, is_locked, is_private from categories"""
    params = ()

    data = read_query(query, params)

    categories = [Category.from_query_result(*row) for row in data]

    return categories


def get_category_by_id(category_id: int, search: str = None, sort: str = None) -> Category or None:  # todo
    category_query = """select category_id, name, is_locked, is_private from categories where category_id = ?"""
    topic_query = """select topic_id, title, category_id, user_id, creation_date, best_reply, is_locked from topics 
    where category_id = ?"""
    params = (category_id,)

    if search:
        category_query += " and name like ?"
        params += (f'%{search}%',)

    if sort:
        if sort.lower() in ["asc", "desc"]:
            category_query += f" order by category_id {sort.lower()}"
        else:
            raise ValueError("Sorting categories only using 'asc' or 'desc'!")

    category_data = read_query(category_query, params)
    topics_data = read_query(topic_query, params)

    category = Category.from_query_result(*category_data[0])
    topics_list = [Topic.from_query_result(*row) for row in topics_data]

    if not topics_list:
        category.topics_list = []

    category.topics_list = topics_list

    return category


def create_category(name: str):
    if not name:
        return BadRequest(content="Category name is required in order to create a category!")

    query = """insert into categories (name) values (?)"""
    params = (name,)

    category_id = insert_query(query, params)

    return CreatedSuccessfully(content=f"Category with id:{category_id} created successfully!")
