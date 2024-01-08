from datetime import datetime, timedelta

# 提示用戶輸入起始時間
start_time_str = input("請輸入起始時間 (YYYY-MM-DD): ")

# 將輸入的時間轉換為 datetime 對象
start_time = datetime.strptime(start_time_str, "%Y-%m-%d")

# 計算45天後的時間
end_time = start_time + timedelta(days=45)

# 輸出結果
print(f"起始時間: {start_time}")
print(f"45天後的時間: {end_time}")
