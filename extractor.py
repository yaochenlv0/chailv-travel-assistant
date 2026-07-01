import re

def extract_trip_info(user_query):
    """
    从用户输入中提取结构化差旅信息
    :param user_query:
    :return: trip_info = {}
    """

    trip_info = {
        "出发地": None,
        "目的地": None,
        "出行时间": None,
        "预算": None,
        "偏好": [],
        "约束": [],
        "原始输入": user_query
    }

    # 提取出发地和目的地
    route_pattern = r"从([\u4e00-\u9fa5A-Za-z]+?)(?:去|到|前往)([\u4e00-\u9fa5A-Za-z]+?)(?:出差|开会|办事|旅游|，|。|,|$)"
    route_match = re.search(route_pattern, user_query)

    if route_match:
        trip_info["出发地"] = route_match.group(1)
        trip_info["目的地"] = route_match.group(2)

    # 提取出行时间
    time_keywords = ["今天","明天","后天","下周","周一","周二","周三","周四","周五","周六","周日"]

    for keyword in time_keywords:
        if keyword in user_query:
            trip_info["出行时间"] = keyword
            break

    # 提取预算
    budget_pattern = r"预算\s*(\d+)\s*元"
    budget_match = re.search(budget_pattern, user_query)

    if budget_match:
        trip_info["预算"] = budget_match.group(1) + "元"

    # 提取偏好
    if "高铁" in user_query:
        trip_info["偏好"].append("高铁")

    if "飞机" in user_query or "航班" in user_query:
        trip_info["偏好"].append("飞机")

    if "二等座" in user_query:
        trip_info["偏好"].append("二等座")

    if "商务座" in user_query:
        trip_info["偏好"].append("商务座")

    if "便宜" in user_query or "省钱" in user_query:
        trip_info["偏好"].append("低成本")

    # 提取约束
    if "上午" in user_query and "到" in user_query:
        trip_info["约束"].append("上午到达")

    if "不要" in user_query:
        trip_info["约束"].append("存在否定约束")

    if "必须" in user_query:
        trip_info["约束"].append("存在强约束")

    return trip_info