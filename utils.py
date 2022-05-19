import json


def load_json(path: str) -> list:
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def response_user(user):
    """Выводит json с данными пользователя"""
    return {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'age': user.age,
        'email': user.email,
        'phone': user.phone,
        'role': user.role
    }


def response_order(order):
    """Выводит json с данными товара"""
    return {
        'id': order.id,
        'name': order.name,
        'description': order.description,
        'start_date': order.start_date,
        'end_date': order.end_date,
        'address': order.address,
        'price': order.price,
        'customer_id': order.customer_id,
        'executor_id': order.executor_id
    }


def response_offer(user):
    """Выводит json с данными заказа"""
    return {
        'id': user.id,
        'order_id': user.order_id,
        'executor_id': user.executor_id,

    }
