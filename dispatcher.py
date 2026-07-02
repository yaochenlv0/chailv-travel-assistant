from planner import plan_trip
from preference import save_preference
from expense import handle_expense

def query_info(user_query):
    """
    信息查询功能占位
    :param user_query:
    :return:
    """

    return f"""
【信息查询】

你想查询的信息是：
{user_query}

当前mvp3版本暂时不接入真实查询接口。
后续版本可以接入天气API、地图API，或者用RAG查询本地差旅制度文档。
"""

def chat(user_query):
    """
    普通聊天功能
    :param user_query:
    :return:
    """

    return f"""
【普通聊天】

你说的是：
{user_query}

我会继续理解你的需求。
如果你需要差旅规划，可以告诉我出发地、目的地、时间、预算和偏好。
"""

def dispatch_task(intent, user_query, trip_info):
    """
    根据意图分发任务
    :param intent:
    :param user_query:
    :param trip_info:
    :return:
    """

    if intent == "trip_planning":
        return plan_trip(trip_info)

    elif intent == "info_query":
        return query_info(user_query)

    elif intent == "preference":
        return save_preference(user_query)

    elif intent == "expense":
        return handle_expense(user_query)

    else:
        return chat(user_query)