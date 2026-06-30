import re

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

    # 行程规划
    if any(keyword in user_query for keyword in trip_keywords):
        return "trip_planning"

    # 信息查询
    elif any(keyword in user_query for keyword in info_keywords):
        return "info_query"

    # 偏好记录
    elif any(keyword in user_query for keyword in preference_keywords):
        return "preference"

    # 聊天
    else:
        return "chat"

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

def plan_trip(trip_info):
    """
    根据结构化差旅信息，生成基础行程规划
    :return: result
    """

    departure = trip_info["出发地"] or "未提供"
    destination = trip_info["目的地"] or "未提供"
    travel_time = trip_info["出行时间"] or "未提供"
    budget = trip_info["预算"] or "未提供"
    preferences = "、".join(trip_info["偏好"]) if trip_info["偏好"] else "暂无"
    constraints = "、".join(trip_info["约束"]) if trip_info["约束"] else "暂无"

    result = f"""
【基础差旅行程方案】

出发地：{departure}
目的地：{destination}
出行时间：{travel_time}
预算：{budget}
偏好：{preferences}
约束：{constraints}

交通建议：
- 当前版本先根据偏好生成基础建议。
- 如果偏好中包含高铁，优先推荐高铁出行。
- 如果偏好中包含飞机，优先推荐航班出行。
- 如果没有明确偏好，默认推荐高铁或者公共交通

住宿建议：
- 建议选择目的地附近、交通便利的酒店。
- 如果预算有限，优先选择经济型酒店。
- 如果商务出差，优先考虑距离会议地点较近的酒店。

日程安排：
- 建议提前预留交通换乘时间。
- 建议出发前确认车次、航班、酒店入住时间。
"""

    return result


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

def save_preference(user_query):
    """
    偏好记录功能占位
    :param user_query:
    :return:
    """

    return f"""
【偏好记录】

已识别到你有可能想记录偏好：
{user_query}

当前mvp3版本仅模拟记录，不会真正写入文件。
后续mvp会加入json文件保存能力，让系统真正记住你的偏好。
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

    else:
        return chat(user_query)
def main() -> None:
    print("欢迎使用差旅出行助手")

    user_query = input("请输入你的需求：")

    intent = detect_intent(user_query)

    trip_info = None
    if intent == "trip_planning":
        trip_info = extract_trip_info(user_query)

    response = dispatch_task(intent, user_query, trip_info)


    print()
    print("助手回复：")
    print(f"识别到的用户意图是：{intent}")
    print(response)

if __name__ == "__main__":
    main()
