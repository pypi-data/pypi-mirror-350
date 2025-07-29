from tkinter import Tk, Label
from datetime import datetime
import pytz
import bangla

# দিনের নাম বাংলায় রূপান্তরের জন্য ম্যাপ
day_map = {
    "Monday": "সোমবার",
    "Tuesday": "মঙ্গলবার",
    "Wednesday": "বুধবার",
    "Thursday": "বৃহস্পতিবার",
    "Friday": "শুক্রবার",
    "Saturday": "শনিবার",
    "Sunday": "রবিবার"
}

def get_bangla_time():
    now = datetime.now(pytz.timezone('Asia/Dhaka'))
    date = bangla.convert_english_digit_to_bangla(str(now.date()))
    time = bangla.convert_english_digit_to_bangla(now.strftime('%I:%M:%S %p'))
    day = day_map.get(now.strftime('%A'), now.strftime('%A'))
    return date, time, day

def update_time():
    date, time_now, day = get_bangla_time()
    label_date.config(text=f"📅 তারিখ: {date}")
    label_time.config(text=f"🕰️ সময়: {time_now}")
    label_day.config(text=f"📖 দিন: {day}")
    root.after(1000, update_time)

def run():
    global root, label_date, label_time, label_day
    root = Tk()
    root.title("বাংলা সময়")
    root.geometry("300x150")

    label_date = Label(root, font=("Kalpurush", 14))
    label_time = Label(root, font=("Kalpurush", 14))
    label_day = Label(root, font=("Kalpurush", 14))

    label_date.pack(pady=5)
    label_time.pack(pady=5)
    label_day.pack(pady=5)

    update_time()
    root.mainloop()
