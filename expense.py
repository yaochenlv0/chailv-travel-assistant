import os
import json
import re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXPENSES_FILE = os.path.join(BASE_DIR, "data", "expenses.json")

def get_default_expense_data():
    """
    获取默认费用数据结构
    :return:
    """

    return {
        "expenses": []
    }

def load_expenses():
    """
    从本地JSON文件读取费用记录
    :return:
    """

    if not os.path.exists(EXPENSES_FILE):
        return get_default_expense_data()

    try:
        with open(EXPENSES_FILE, "r", encoding="utf-8") as file:
            expense_data = json.load(file)

            if "expenses" not in expense_data:
                expense_data["expenses"] = []

            return expense_data

    except json.JSONDecodeError:
        return get_default_expense_data()

def save_expenses(expense_data):
    """
    将用户记录保存到本地
    :param expense_data:
    :return:
    """

    os.makedirs(os.path.dirname(EXPENSES_FILE), exist_ok=True)

    with open(EXPENSES_FILE, "w", encoding="utf-8") as file:
        json.dump(expense_data, file, ensure_ascii=False,indent=4)

def detect_expense_category(user_query):
    """
    根据用户输入判断用户类型
    :param user_query:
    :return:
    """

    transport_keywords = ["交通","打车","车费","地铁","公交","高铁票","火车票","机票","出租车"]
    hotel_keywords = ["住宿", "酒店", "房费", "宾馆"]
    meal_keywords = ["餐饮", "吃饭", "饭", "早餐", "午餐", "晚餐", "咖啡", "奶茶"]

    if any(keyword in user_query for keyword in transport_keywords):
        return "交通"

    elif any(keyword in user_query for keyword in hotel_keywords):
        return "住宿"

    elif any(keyword in user_query for keyword in meal_keywords):
        return "餐饮"

    else:
        return "其他"

def extract_expense_amount(user_query):
    """
    从用户输入中提取金额
    :param user_query:
    :return:
    """

    amount_pattern = r"(\d+(?:\.\d+)?)\s*元"
    amount_match = re.search(amount_pattern, user_query)

    if amount_match:
        return float(amount_match.group(1))

    return None

def extract_expense_info(user_query):
    """
    从用户输入中提取费用信息
    :param user_query:
    :return:
    """

    category = detect_expense_category(user_query)
    amount = extract_expense_amount(user_query)

    expense_info = {
        "类型": category,
        "金额": amount,
        "说明": user_query,
        "记录时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "原始输入": user_query
    }

    return expense_info

def add_expense(user_query):
    """
    新增一笔费用记录
    :param user_query:
    :return:
    """

    expense_info = extract_expense_info(user_query)

    if expense_info["金额"] is None:
        return f"""
【费用记录】

我识别到你可能想记录费用：

{user_query}

但是没有识别到明确金额。
请使用类似下面的表达：

- 打车花了35元
- 就带你住宿300元
- 午餐花了50元
"""
    expense_data = load_expenses()
    expense_data["expenses"].append(expense_info)
    save_expenses(expense_data)

    return f"""
【费用记录】

已记录一笔费用记录

类型：{expense_info["类型"]}
金额：{expense_info["金额"]}
说明：{expense_info["说明"]}

你可以继续记录其他费用，或者输入”生成报销清单“查看汇总。
"""

def summarize_expenses():
    """
    汇总费用数据
    :return:
    """

    expense_data = load_expenses()
    expenses = expense_data["expenses"]

    summary = {
        "交通": 0,
        "住宿": 0,
        "餐饮": 0,
        "其他": 0
    }

    for expense in expenses:
        category = expense.get("类型", "其他")
        amount = expense.get("金额", 0) or 0

        if category not in summary:
            summary[category] = 0

        summary[category] += amount

    total = sum(summary.values())

    return summary,total,expenses

def generate_reimbursement_report():
    """
    生成简单报销清单
    :return:
    """

    summary, total, expenses = summarize_expenses()

    if not expenses:
        return f"""
【报销清单】

当前没有消费记录

你可以先记录费用，例如：
- 打车花了35元
- 酒店住宿300元
- 午餐花了50元
"""

    detail_lines = []

    for index, expense in enumerate(expenses, start=1):
        detail_lines.append(
            f"{index}.{expense['类型']} - {expense['金额']}元 - {expense['说明']}"
        )

    detail_text = "\n".join(detail_lines)

    return f"""
【报销清单】

一、费用明细
{detail_text}

二、分类汇总
交通：{summary.get("交通",0)}元
住宿：{summary.get("住宿",0)}元
餐饮：{summary.get("餐饮",0)}元
其他：{summary.get("其他",0)}元

三、总费用
总费用：{total}元
"""

def handle_expense(user_query):
    """
    处理费用相关需求
    :param user_query:
    :return:
    """

    amount = extract_expense_amount(user_query)

    if amount is not None:
        return add_expense(user_query)

    report_keywords = ["汇总","总费用","报销","清单","费用清单","报销清单"]

    if any(keyword in user_query for keyword in report_keywords):
        return generate_reimbursement_report()

    return """
    【费用管理】
    
    我认识到你可能象处理费用，但没有判断出是记录费用还是查看费用。
    
    你可以这样说：
    
    - 打车花了35元
    - 酒店住宿300元
    - 午餐花了50元
    - 生成报销清单
    """