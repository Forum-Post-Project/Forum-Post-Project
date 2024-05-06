from data.database import read_query, insert_query, update_query
from data.models import Category, Topic, CategoryWithTopics


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
                       page_size: int = 10) -> CategoryWithTopics or None:
    category_query = """select * from categories where category_id = ?"""
    topic_query = """select * from topics where category_id = ?"""
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

    if not category_data:
        return None

    category = Category.from_query_result(*category_data[0])
    topics_list = [Topic.from_query_result(*row) for row in topics_data]

    category_with_topics = CategoryWithTopics(
        category_id=category.category_id,
        name=category.name,
        is_locked=category.is_locked,
        is_private=category.is_private,
        topics=topics_list
    )

    return category_with_topics


def create_category(name: str) -> Category or None:
    query = """insert into categories (name) values(?)"""
    params = (name,)

    category_id = insert_query(query, params)

    if category_id:
        return Category(category_id=category_id,
                        name=name,
                        is_locked=False,
                        is_private=False
                        )
    else:
        return None


def lock_category(category_id: int):
    query = """update categories set is_locked = 1 where category_id = ?"""
    params = (category_id,)
    update_query(query, params)


def get_category(category_id: int) -> Category or None:
    query = """select * from categories where category_id = ?"""
    category = read_query(query, (category_id,))

    if category:
        return category[0]
    else:
        return None


def make_category_private(category_id: int):
    category_query = "update categories set is_private = 1 where category_id = ?"
    params = (category_id,)
    update_query(category_query, params)

    topic_query = "update topics set is_locked = 1 where category_id = ?"
    update_query(topic_query, params)


def make_category_non_private(category_id: int):
    category_query = "update categories set is_private = 0 where category_id = ?"
    params = (category_id,)
    update_query(category_query, params)

    topic_query = "update topics set is_locked = 0 where category_id = ?"
    update_query(topic_query, params)


def give_user_category_read_access(category_id: int, user_id: int, access_level: str = "Read"):
    query = """insert into users_category_access (user_id, category_id, access_level) values (?, ?, ?)"""
    params = (user_id, category_id, access_level)

    insert_query(query, params)