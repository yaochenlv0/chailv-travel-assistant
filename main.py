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
    #

def main() -> None:
    print("欢迎使用差旅出行助手")

    user_query = input("请输入你的需求：")

    intent = detect_intent(user_query)

    print()
    print("助手回复：")
    print(f"收到，你的差旅需求是：{user_query}")
    print(f"识别的用户意图是：{intent}")

    if intent == "trip_planning":
        print("接下来我可以为你生成差旅行程方案。")

    elif intent == "info_query":
        print("接下来我可以为你查询相关差旅信息。")

    elif intent == "preference":
        print("接下来我可以帮你记录个人偏好。")

    elif intent == "chat":
        print("我可以继续和你对话，并尝试理解你的需求。")

if __name__ == "__main__":
    main()
