import json
import time
import schedule
import random
from tkinter import Tk, Label, Button, Toplevel, messagebox
import screeninfo  # 用於獲取螢幕資訊


# 讀取 JSON 配置
def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


# 顯示自訂通知視窗
def show_notification(message):
    # 獲取螢幕的解析度資訊
    screen = screeninfo.get_monitors()[0]
    screen_width = screen.width
    screen_height = screen.height

    # 建立一個新的彈出視窗
    popup = Toplevel()
    popup.title("提醒")

    # 設定視窗大小
    window_width = 300
    window_height = 150

    # 計算彈出視窗的位置 (貼近右下角的工作列)
    x_position = screen_width - window_width - 20  # 貼近右側
    y_position = screen_height - window_height - 80  # 貼近下側，並考慮工作列高度

    # 設定視窗大小和位置
    popup.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # 設置訊息標籤
    label = Label(popup, text=message, wraplength=280)
    label.pack(pady=10)

    # 建立按鈕以關閉視窗
    button = Button(popup, text="好的，没問題", command=popup.destroy)
    button.pack(pady=5)

    # 保持彈出視窗在頂層
    popup.attributes('-topmost', True)

    # 確保主視窗不阻擋
    popup.mainloop()


# 隨機選擇提醒訊息
def select_random_message(messages):
    if isinstance(messages, list):
        return random.choice(messages)
    return messages  # 如果不是列表，直接返回訊息


# 設置間隔提醒
def set_interval_reminder(messages, minutes):
    message = select_random_message(messages)
    schedule.every(minutes).minutes.do(lambda: show_notification(message))


# 設置定時提醒
def set_time_reminder(messages, times):
    for time in times:
        message = select_random_message(messages)
        schedule.every().day.at(time).do(lambda: show_notification(message))


# 顯示初始確認視窗
def show_initial_confirmation(config):
    root = Tk()
    root.withdraw()  # 隱藏主視窗

    # 取得提醒訊息和時間設定，組成確認訊息
    reminders_info = '\n'.join(
        [f"Message: {reminder['message']}, "
         f"Interval: {reminder.get('interval_minutes', 'N/A')} minutes, "
         f"Time: {', '.join(reminder.get('time', [])) or 'N/A'}"
         for reminder in config['reminders']]
    )

    confirm_message = f"Please confirm your config:\n\n{reminders_info}\n\nIs this correct?"

    # 顯示確認對話框
    user_response = messagebox.askyesno("Config Confirmation", confirm_message)
    if not user_response:
        messagebox.showinfo("Reminder Notifier", "Please update your config and restart the program.")
        root.destroy()
        exit()  # 結束程式

    root.destroy()  # 關閉對話框


# 主程式
def main():
    config = load_config('config.json')
    show_initial_confirmation(config)  # 確認設定
    reminders = config.get('reminders', [])

    # 根據 JSON 配置設置提醒
    for reminder in reminders:
        messages = reminder.get('message')
        interval_minutes = reminder.get('interval_minutes')
        times = reminder.get('time', [])

        if interval_minutes:
            set_interval_reminder(messages, interval_minutes)
        if times:
            set_time_reminder(messages, times)

    # 執行排程
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
