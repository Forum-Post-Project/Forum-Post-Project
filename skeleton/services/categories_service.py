from data.database import read_query, insert_query, update_query
from data.models import Category, Topic
from common.responses import CreatedSuccessfully, BadRequest


def get_all_categories() -> list[Category] or None:
    query = """select category_id, name, is_locked, is_private from categories"""
    params = ()

    data = read_query(query, params)

    categories = [Category.from_query_result(*row) for row in data]

    return categories


def get_category_by_id(category_id: int,
                       search: str = None,
                       sort: str = None,
                       page: int = None,
                       page_size: int = 10) -> Category or None:
    category_query = """select category_id, name, is_locked, is_private from categories where category_id = ?"""
    topic_query = """select topic_id, title, category_id, user_id, creation_date, best_reply, is_locked from topics 
    where category_id = ?"""
    params = (category_id,)

    if search:
        topic_query += " and title like ?"
        params += (f'%{search}%',)

    if sort:
        if sort.lower() in ["asc", "desc"]:
            topic_query += f" order by creation_date {sort.lower()}"
        else:
            raise ValueError("Sorting topics only using 'asc' or 'desc'!")

    if page and page_size:
        if page < 1:
            page = 1
        offset = (page - 1) * page_size
        topic_query += " limit ? offset ?"
        params += (page_size, offset)

    category_data = read_query(category_query, params)
    topics_data = read_query(topic_query, params)

    category = Category.from_query_result(*category_data[0])
    topics_list = [Topic.from_query_result(*row) for row in topics_data]

    if not topics_list:
        category.topics_list = []

    category.topics_list = topics_list

    return category


def create_category(category: Category):
    query = """insert into categories (name) values (?)"""
    params = (category.name,)

    category_id = insert_query(query, params)
    category.category_id = category_id
    return category #, CreatedSuccessfully(content=f"Category with id:{category_id} created successfully!")


def lock_category(category_id: int):
    query = """update categories set is_locked = 1 where category_id = ?"""
    params = (category_id,)
    update_query(query, params)
