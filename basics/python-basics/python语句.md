```
# 提取出发地和目的地
    route_pattern = r"从([\u4e00-\u9fa5A-Za-z]+?)(?:去|到|前往)([\u4e00-\u9fa5A-Za-z]+?)(?:出差|开会|办事|旅游|，|。|,|$)"
    route_match = re.search(route_pattern, user_query)
```

```
trip_info["出发地"] = route_match.group(1)
```

```
def main() -> None:
```

```
trip_info["预算"] = budget_match.group(1) + "元"
```

```
os.makedirs(os.path.dirname(PREFERENCE_FILE),exist_ok=True)
```

```
json.dump(preferences, file, ensure_ascii=False, indent=4)
```

```
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PREFERENCE_FILE = os.join(BASE_DIR,'data','preferences.json')
```

```
amount_pattern = r"(\d+(?:\.\d+)?)\s*元"
amount_match = re.search(amount_pattern, user_query)
```

```
datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```