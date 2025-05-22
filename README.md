# 🕰️ Python CLI Alarm Clock

A simple, user-friendly Alarm Clock application built with Python using Object-Oriented Programming principles.

## 🚀 Features

- 🕒 **Display Current Time**
- ⏰ **Add Alarms** for any time and day of the week
- 😴 **Snooze Alarms** up to 3 times with 5-minute intervals
- 🗑️ **Delete Alarms** by time and day
- 📋 **List All Alarms** with status and snooze count
- 🔁 **Concurrent Alarm Checking** in the background using threads

## 📦 Requirements

- Python 3.10+
- No external dependencies (uses built-in `datetime`, `uuid`, and `threading` modules)

## 💻 How to Use

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/python-cli-alarm-clock.git
   cd python-cli-alarm-clock

2. Run the application:
   ```bash
   python alarm_clock.py

3. Use the interactive menu:
   Menu:
        1. Add Alarm
        2. Delete Alarm
        3. Snooze Alarm
        4. List Alarms
        5. Show Current Time
        6. Exit


## 🧠 Engineering Notes
- Uses UUIDs internally for unique alarm IDs, but users only interact with friendly inputs (time + day).
- Maximum of 3 snoozes per alarm, each delaying the alarm by 5 minutes.







  
