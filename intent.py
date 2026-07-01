def detect_intent(user_query):
    """
    根据用户输入，判断用户意图
    :param user_query:
    :return: intent("trip_planning","info_query","preference","chat")
    """
    # 行程规划关键词
    trip_keywords = ["出差","行程","去","到","从","酒店","住宿","交通"]

    # 信息查询关键词
    info_keywords = ["查","查询","天气","几点","多少","信息","路线"]

    # 偏好记录关键词
    preference_keywords = ["喜欢","偏好","优先","以后","记住","不喜欢"]

    # 偏好记录(优先级最高)
    if any(keyword in user_query for keyword in preference_keywords):
        return "preference"

    # 信息查询
    elif any(keyword in user_query for keyword in info_keywords):
        return "info_query"

    # 行程规划
    elif any(keyword in user_query for keyword in trip_keywords):
        return "trip_planning"

    # 聊天
    else:
        return "chat"