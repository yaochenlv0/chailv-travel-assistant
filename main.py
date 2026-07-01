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

def generate_transport_advice(trip_info):
    """
    根据用户偏好生成交通建议
    :param trip_info:
    :return:
    """

    preferences = trip_info["偏好"]

    if "高铁" in preferences:
        return "根据你的偏好，建议优先选择高铁出行。高铁适合中短途差旅，时间稳定，市中心到达也比较方便。"

    elif "飞机" in preferences:
        return "根据你的偏好，建议优先选择航班出行。飞机适合长距离差旅，但需要提前考虑值机，安检和机场通勤时间。"

    elif "低成本" in preferences:
        return "根据你的低成本偏好，建议优先比较高铁二等座、经济型航班和公共交通方案，选择总成本更低的出行方式。"

    else:
        return "当前没有明确交通偏好。建议优先考虑高铁或公共交通，并结合时间、价格和目的地位置进行选择。"

def generate_hotel_advice(trip_info):
    """
    根据目的地和预算生成住宿建议
    :param trip_info:
    :return:
    """

    destination = trip_info["目的地"] or "目的地"
    budget = trip_info["预算"]

    if budget is None:
        return f"建议选择{destination}交通便利、靠近办事地点或会议地点的酒店。当前未提供预算，建议后续补充预算范围。"

    budget_number = int(budget.replace("元", ""))

    if budget_number <= 800:
        return f"当前预算为{budget}，建议在{destination}选择经济型酒店或连锁酒店，并优先考虑交通便利位置。"

    elif budget_number <= 2000:
        return f"当前预算为{budget}，可以在{destination}选择商务型酒店，优先考虑距离办事地点较近的位置。"

    else:
        return f"当前预算为{budget}，住宿选择空间较大。建议优先选择交通便利、服务稳定、适合商务出行的酒店。"

def generate_schedule_advice(trip_info):
    """
    根据出行时间生成日程建议
    :param trip_info:
    :return:
    """

    travel_time = trip_info["出行时间"]

    if travel_time is None:
        return "当前未提供明确出行时间。建议补充出行日期，以便进一步安排交通和住宿。"

    if travel_time in ["今天", "明天"]:
        return f"出行时间是{travel_time}，时间较近，建议尽快确认交通票务和住宿，并预留充足换乘时间。"

    elif travel_time in ["后天", "下周"]:
        return f"出行时间是{travel_time}，仍有一定准备时间，建议先确定交通方式，再安排住宿和日程。"

    else:
        return f"出行时间是{travel_time}，建议提前规划交通、住宿和办事时间。"

def generate_budget_advice(trip_info):
    """
    根据预算生成费用提醒
    :param trip_info:
    :return:
    """

    budget = trip_info["预算"]

    if budget is None:
        return "当前未提供预算。建议补充预算信息，后续可以用于控制交通、住宿和餐饮费用。"

    budget_number = int(budget.replace("元", ""))

    if budget_number <= 800:
        return f"当前预算为{budget}，预算较紧，建议优先控制住宿和交通成本。"

    elif budget_number <= 2000:
        return f"当前预算为{budget}，适合普通商务差旅，建议合理分配交通、住宿和餐饮费用。"

    else:
        return f"当前预算为{budget}，预算相对充足，可以优先考虑时间效率和出行舒适度。"

def generate_constraint_advice(trip_info):
    """
    根据约束条件生成注意事项
    :param trip_info:
    :return:
    """

    constraints = trip_info["约束"]

    if not constraints:
        return "当前没有识别到特殊约束条件。"

    advice_list = []

    for constraint in constraints:
        if constraint == "上午到达":
            advice_list.append("你提到需要上午到达，建议选择前一晚出发或当天较早班次。")
        elif constraint == "存在否定约束":
            advice_list.append("你提到了否定约束，后续规划时需要避免你不希望出现的方案。")
        elif constraint == "存在强约束":
            advice_list.append("你提到了强约束，后续规划时应优先满足该条件。")
        else:
            advice_list.append(f"需要注意约束条件：{constraint}")

    return "\n".join(advice_list)

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

    transport_advice = generate_transport_advice(trip_info)
    hotel_advice = generate_hotel_advice(trip_info)
    schedule_advice = generate_schedule_advice(trip_info)
    budget_advice = generate_budget_advice(trip_info)
    constraint_advice = generate_constraint_advice(trip_info)

    result = f"""
【基础差旅行程方案】

一、行程信息
出发地：{departure}
目的地：{destination}
出行时间：{travel_time}
预算：{budget}
偏好：{preferences}
约束：{constraints}

二、交通建议
{transport_advice}

三、住宿建议
{hotel_advice}

四、日程建议
{schedule_advice}

五、预算提醒
{budget_advice}

六、约束提醒
{constraint_advice}
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
