from preference import apply_saved_preferences

def generate_transport_advice(trip_info):
    """
    根据用户偏好生成交通建议
    :param trip_info:
    :return:
    """

    preferences = trip_info["偏好"]

    if "高铁" in preferences and "二等座" in preferences:
        return "根据你的历史偏好，建议优先选择高铁二等座。高铁适合中短途差旅，时间稳定，市中心到达也比较方便。"

    elif "高铁" in preferences:
        return "根据你的偏好，建议优先选择高铁出行。高铁适合中短途差旅，时间稳定，市中心到达也比较方便。"

    elif "飞机" in preferences or "航班" in preferences:
        return "根据你的偏好，建议优先选择航班出行。飞机适合长距离差旅，但需要提前考虑值机、安检和机场通勤时间。"

    elif "效率优先" in preferences:
        return "根据你的效率优先偏好，建议优先选择耗时更短、换乘更少的交通方案。"

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

    trip_info = apply_saved_preferences(trip_info)

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