from src.utils.return_url_object import return_simple_url_object
from src.utils.file_operation import get_unique_short_uuid4, upload_file, delete_file
from src.core.database.database import Database
from src.core.models.models import User
from src.core.repository.common_tools import checkEntityAlreadyExists
from src.utils.hashing import Hasher


def get_all_users():
    db = Database()

    query = "SELECT * FROM user"
    users = db.fetch_all(query)
    
    if len(users):
        for user in users:
            if user['avatar']:
                user['avatar'] = return_simple_url_object(user['avatar'])
    
    return users


def get_user_by_id(user_id: int):
    db = Database()
    
    query = "SELECT * FROM user WHERE id = ?;"
    user = db.fetch_one(query, (user_id,))
    
    if user and user['avatar']:
        user = dict(user)
        user['avatar'] = return_simple_url_object(user['avatar'])

    return user


def get_simple_user_by_id(user_id: int):
    db = Database()

    query = "SELECT * FROM user WHERE id = ?;"
    user = db.fetch_one(query, (user_id,))
    
    if user and user['avatar']:
        user['avatar'] = return_simple_url_object(user['avatar'])
        
    return user


def get_user_by_email(email: str):
    db = Database()

    query = "SELECT * FROM user WHERE login = ?;"
    user = db.fetch_one(query, (email,))
    
    if user and user['avatar']:
        user = dict(user)
        user['avatar'] = return_simple_url_object(user['avatar'])
    
    return user


def create_user(user: User, file):
    db = Database()

    result_check = checkEntityAlreadyExists('user', user)

    if not result_check:
        return False
    
    if file:
        user.avatar = upload_file('users', file, get_unique_short_uuid4())
    
    user.password = Hasher.get_password_hash(user.password)

    query = ("INSERT INTO user (login, password, role, avatar) VALUES (?, ?, 'U', ?);")
    
    params = (user.login, user.password, user.avatar)
    
    cursor = db.execute_query(query, params)

    return get_user_by_email(user.login)


def update_user(id: int, user: User, file):
    db = Database()

    try:
        check_user_exist = get_user_by_id(id)

        if not check_user_exist:
            return False

        query = "UPDATE user SET "
        params = ()

        if user.login:
            query += "login = ?, "
            params = params + (user.login,)


        if user.password:
            query += "password = ?, "
            user.password = Hasher.get_password_hash(user.password)
            params = params + (user.password,)
            
        if file:
            query += "avatar = ?, "
            delete_file(user.avatar)
            user.avatar = upload_file('users', file, get_unique_short_uuid4())
            params = params + (user.avatar,)

        query = query[:-2]

        query += " WHERE id = ?;"
        params = params + (id,)
        
        db.execute_query(query, params)

        return get_user_by_id(id)
    except:
        return False


def delete_user_by_id(id: int):
    db = Database()

    check_user_exist = get_user_by_id(id)

    if not check_user_exist:
        return False

    query = "DELETE FROM user WHERE id = ?;"
    db.execute_query(query, (id,))

    return True
