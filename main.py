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

def main() -> None:
    print("欢迎使用差旅出行助手")

    user_query = input("请输入你的需求：")

    intent = detect_intent(user_query)

    print()
    print("助手回复：")
    print(f"收到，你的差旅需求是：{user_query}")
    print(f"识别的用户意图是：{intent}")

    if intent == "trip_planning":
        trip_info = extract_trip_info(user_query)

        print()
        print("已提取到的结构化差旅信息：")
        print(trip_info)

        print("接下来我可以为你生成差旅行程方案。")

    elif intent == "info_query":
        print("接下来我可以为你查询相关差旅信息。")

    elif intent == "preference":
        print("接下来我可以帮你记录个人偏好。")

    elif intent == "chat":
        print("我可以继续和你对话，并尝试理解你的需求。")

if __name__ == "__main__":
    main()
