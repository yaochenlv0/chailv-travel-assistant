import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PREFERENCE_FILE = os.path.join(BASE_DIR,'data','preferences.json')

def get_default_preferences():
    """
    获取默认偏好结构
    :return:
    """

    return {
        "交通偏好": [],
        "座位偏好": [],
        "住宿偏好": [],
        "预算偏好": [],
        "其他偏好": []
    }

def load_preferences():
    """
    从本地JSON文件中读取用户偏好
    :return: preferences
    """

    if not os.path.exists(PREFERENCE_FILE):
        return get_default_preferences()

    try:
        with open(PREFERENCE_FILE, "r", encoding="utf-8") as file:
            preferences = json.load(file)

            # 防止旧文件缺少某些字段
            default_preferences = get_default_preferences()
            for key, value in default_preferences.items():
                if key not in preferences:
                    preferences[key] = value

            return preferences

    except json.JSONDecodeError:
        return get_default_preferences()

def save_preferences(preferences):
    """
    将用户偏好保存到本地JSON文件
    :param preferences:
    :return:
    """

    os.makedirs(os.path.dirname(PREFERENCE_FILE),exist_ok=True)

    with open(PREFERENCE_FILE, "w", encoding="utf-8") as file:
        json.dump(preferences, file, ensure_ascii=False, indent=4)

def add_unique_value(target_list,value):
    """
    向列表中添加不重复的值
    :param target_list:
    :param value:
    :return:
    """

    if value not in target_list:
        target_list.append(value)
        return True

    return False

def extract_preference_from_text(user_query):
    """
    从用户输入中提取用户偏好
    :param user_query:
    :return: new_preferences
    """

    new_preferences = get_default_preferences()

    # 交通偏好
    if "高铁" in user_query:
        new_preferences["交通偏好"].append("高铁")

    if "飞机" in user_query or "航班" in user_query:
        new_preferences["交通偏好"].append("飞机")

    if "公共交通" in user_query or "地铁" in user_query:
        new_preferences["交通偏好"].append("公共交通")

    # 座位偏好
    if "二等座" in user_query:
        new_preferences["座位偏好"].append("二等座")

    if "商务座" in user_query:
        new_preferences["座位偏好"].append("商务座")

    if "经济舱" in user_query:
        new_preferences["座位偏好"].append("经济舱")

        # 住宿偏好
    if "靠近" in user_query or "近一点" in user_query:
        new_preferences["住宿偏好"].append("靠近办事地点")

    if "安静" in user_query:
        new_preferences["住宿偏好"].append("安静")

        # 预算偏好
    if "便宜" in user_query or "省钱" in user_query or "低成本" in user_query:
        new_preferences["预算偏好"].append("低成本")

    if "舒适" in user_query:
        new_preferences["预算偏好"].append("舒适优先")

    if "效率" in user_query or "节省时间" in user_query:
        new_preferences["预算偏好"].append("效率优先")

    return new_preferences

def format_preferences(preferences):
    """
    将偏好字典格式化为文本
    :param preferences:
    :return:
    """

    lines = []

    for category, values in preferences.items():
        if values:
            lines.append(f"{category}：{'、'.join(values)}")
        if not lines:
            return "暂无已保存偏好"

    return "\n".join(lines)

def save_preference(user_query):
    """
    保存用户偏好
    :param user_query:
    :return:
    """

    preferences = load_preferences()
    new_preferences = extract_preference_from_text(user_query)

    has_new_preference = False

    for category, values in new_preferences.items():
        for value in values:
            added = add_unique_value(preferences[category],value)
            if added:
                has_new_preferences = True

    save_preferences(preferences)

    if has_new_preference:
        return f"""
【偏好记录】

已保存你的偏好。

当前已保存偏好：
{format_preferences(preferences)}
"""
    else:
        return f"""
【偏好记录】

我没有识别到新的明确偏好，或者这些偏好之前已经保存过。

当前已保存偏好：
{format_preferences(preferences)}
"""

def apply_saved_preferences(trip_info):
    """
    将历史偏好保存到当前行程信息当中
    :param trip_info:
    :return: updated_trip_info
    """

    saved_preferences = load_preferences()

    updated_trip_info = trip_info.copy()
    updated_trip_info["偏好"] = list(trip_info["偏好"])

    for category in ["交通偏好","座位偏好","住宿偏好","预算偏好"]:
        for preference in saved_preferences.get(category,[]):
            if preference not in updated_trip_info["偏好"]:
                updated_trip_info["偏好"].append(preference)

    updated_trip_info["历史偏好"] = saved_preferences

    return updated_trip_info