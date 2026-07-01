from intent import detect_intent
from extractor import extract_trip_info
from dispatcher import dispatch_task

def main() -> None:
    """
    差旅出行助手程序入口
    :return:
    """
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
