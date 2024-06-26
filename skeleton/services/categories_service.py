from data.database import read_query, insert_query, update_query
from data.models import Category, Topic, CategoryWithTopics, UserCategoryAccess
from common.responses import BadRequest


def get_all_categories() -> list[Category] or None:
    query = """select category_id, name, is_locked, is_private from categories"""
    params = ()

    data = read_query(query, params)

    categories = [Category.from_query_result(*row) for row in data]

    return categories


def get_category_by_id(category_id: int,
                       search: str = None,
                       sort_by: str = None,
                       page: int = None,
                       page_size: int = 10) -> CategoryWithTopics or None:
    category_query = """select * from categories where category_id = ?"""
    topic_query = """select * from topics where category_id = ?"""
    params = (category_id,)

    if search:
        topic_query += """ and title like ?"""
        params += (f'%{search}%',)

    if sort_by:
        if sort_by.lower() in ["oldest", "newest"]:
            if sort_by.lower() == "oldest":
                topic_query += """ order by creation_date asc"""
            else:
                topic_query += """ order by creation_date desc"""
        else:
            return BadRequest(content="Sorting topics only using 'oldest' or 'newest'!")

    if page and page_size:
        if page < 1:
            page = 1
        offset = (page - 1) * page_size
        topic_query += " limit ? offset ?"
        params += (page_size,)
        params += (offset,)

    category_data = read_query(category_query, (category_id,))
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


def give_user_category_write_access(category_id: int, user_id: int, access_level: str = "Write"):
    query = """insert into users_category_access (user_id, category_id, access_level) values (?, ?, ?)"""
    params = (user_id, category_id, access_level)

    insert_query(query, params)


def revoke_user_category_access(user_id: int, category_id: int):
    query = """"delete from users_category_access where user_id = ? and category_id = ?"""
    update_query(query, (user_id, category_id))


def access_exists(user_id, category_id):
    existing_access_query = """select access_level from users_category_access where user_id = ? and category_id = ?"""
    existing_access = read_query(existing_access_query, (user_id, category_id))
    return True if existing_access else False


def check_write_access(user_id, category_id):
    existing_access_query = """select access_level from users_category_access where user_id = ? and category_id = ?"""

    existing_access = read_query(existing_access_query, (user_id, category_id))
    if existing_access and existing_access[0][0] == "Write":
        return True
    else:
        return False


def get_privileged_users(category_id: int):

    query = """
        select uca.user_id, u.username, uca.access_level
        from users_category_access as uca
        join users as u on uca.user_id = u.user_id
        where uca.category_id = ?
    """
    params = (category_id,)
    result = read_query(query, params)

    privileged_users = [UserCategoryAccess.from_query_result(*row) for row in result]

    return privileged_users
