import re

def detect_intent(user_query):
    """
    根据用户输入，判断用户意图
    :param user_query:
    :return: intent("trip_planning","info_query","preference","chat")
    """
    # 行程规划关键词
    trip_keywords = ["出差","行程","去","到","从","交通"]

    # 信息查询关键词
    info_keywords = ["查","查询","天气","几点","多少","信息","路线"]

    # 偏好记录关键词
    preference_keywords = ["喜欢","偏好","优先","以后","记住","不喜欢"]

    # 费用记录关键词
    expense_record_keywords = [
        "费用", "花了", "花费", "支出",
        "交通费", "住宿费", "餐饮费",
        "打车", "车费", "房费",
        "高铁票", "火车票", "机票", "酒店费",
        "酒店", "住宿", "午餐", "晚餐", "早餐", "吃饭", "餐饮"
    ]

    expense_report_keywords = ["报销", "清单", "总费用", "费用汇总", "报销清单", "费用清单", "生成报销清单"]

    # 费用记录判断
    amount_pattern = r"\d+(?:\.\d+)?\s*元"
    has_amount = re.search(amount_pattern,user_query) is not None
    has_expense_record_keyword = any(keyword in user_query for keyword in expense_record_keywords)
    has_expense_report_keyword = any(keyword in user_query for keyword in expense_report_keywords)

    # 偏好记录(优先级最高)
    if any(keyword in user_query for keyword in preference_keywords):
        return "preference"

    elif has_expense_report_keyword:
        return "expense"

    # 费用记录优先级也高于行程规划
    elif has_amount and has_expense_record_keyword:
        return "expense"

    # 信息查询
    elif any(keyword in user_query for keyword in info_keywords):
        return "info_query"

    # 行程规划
    elif any(keyword in user_query for keyword in trip_keywords):
        return "trip_planning"

    # 聊天
    else:
        return "chat"