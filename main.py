import time
import datetime
import threading
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

# Engineering Design Notes:
# - The system is modular with Alarm and AlarmClock classes.
# - Alarm encapsulates the state and logic for individual alarms.
# - AlarmClock manages the collection of alarms and user interactions.
# - All input/output interactions are handled via a command-line interface.
# - Improved type safety by using a Time dataclass and DayOfWeek enum.

@dataclass(frozen=True)
class Time:
    hour: int
    minute: int

    def to_str(self) -> str:
        return f"{self.hour:02d}:{self.minute:02d}"

    @staticmethod
    def from_str(time_str: str) -> "Time":
        time_parts = time_str.split(":")
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        return Time(hour, minute)

class DayOfWeek(Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

    @staticmethod
    def from_str(day_str: str) -> "DayOfWeek":
        try:
            return DayOfWeek[day_str.upper()]
        except KeyError:
            raise ValueError(f"Invalid day: {day_str}")

class Alarm:
    def __init__(self, original_time: Time, day: DayOfWeek):
        self.id: str = str(uuid.uuid4())
        self.original_time: Time = original_time
        self.day: DayOfWeek = day
        self.snooze_count: int = 0
        self.active: bool = True
        self.snoozed_time: Optional[Time] = None

    def current_time(self) -> Time:
        return self.snoozed_time if self.snoozed_time else self.original_time

    def snooze(self) -> None:
        if self.snooze_count < 3:
            now = datetime.datetime.now().replace(second=0, microsecond=0)
            alarm_time = now.replace(hour=self.current_time().hour, minute=self.current_time().minute)
            snoozed_dt = alarm_time + datetime.timedelta(minutes=5)
            snoozed_hour = snoozed_dt.hour
            snoozed_minute = snoozed_dt.minute
            self.snoozed_time = Time(snoozed_hour, snoozed_minute)
            self.snooze_count += 1
            print(f"Alarm {self.id} snoozed to {self.snoozed_time.to_str()}")
        else:
            print(f"Alarm {self.id} has already been snoozed 3 times.")

    def reset_snooze(self) -> None:
        self.snooze_count = 0
        self.snoozed_time = None

class AlarmClock:
    def __init__(self):
        self.alarms: list[Alarm] = []
        self.running: bool = True

    def add_alarm(self, time_str: str, day_str: str) -> None:
        time_obj = Time.from_str(time_str)
        day_enum = DayOfWeek.from_str(day_str)
        alarm = Alarm(time_obj, day_enum)
        self.alarms.append(alarm)
        print(f"Alarm set for {time_obj.to_str()} on {day_enum.value} (ID: {alarm.id})")

    def delete_alarm(self, alarm_id: str) -> None:
        self.alarms = [alarm for alarm in self.alarms if alarm.id != alarm_id]
        print(f"Deleted alarm {alarm_id}")

    def snooze_alarm(self, alarm_id: str) -> None:
        for alarm in self.alarms:
            if alarm.id == alarm_id:
                alarm.snooze()
                break

    def snooze_alarm_by_time_day(self, time_str: str, day_str: str) -> None:
        alarm = self.find_alarm_by_time_day(time_str, day_str)
        if alarm:
            self.snooze_alarm(alarm.id)
        else:
            print(f"No alarm found for {time_str} on {day_str}.")

    def find_alarm_by_time_day(self, time_str: str, day_str: str) -> Alarm | None:
        try:
            target_time = Time.from_str(time_str)
            target_day = DayOfWeek.from_str(day_str)
        except ValueError as e:
            print(e)
            return None

        for alarm in self.alarms:
            if alarm.original_time == target_time and alarm.day == target_day:
                return alarm
        return None

    def check_alarms(self) -> None:
        while self.running:
            now = datetime.datetime.now()
            current_time = Time(now.hour, now.minute)
            current_day = DayOfWeek[now.strftime('%A').upper()]
            for alarm in self.alarms:
                if alarm.active and alarm.current_time() == current_time and alarm.day == current_day:
                    print(f"\n*** ALARM! It's {alarm.current_time().to_str()} on {alarm.day.value} ***")
                    alarm.active = False
            time.sleep(60)

    def start(self) -> None:
        print("Alarm Clock started.")
        threading.Thread(target=self.check_alarms, daemon=True).start()

    def list_alarms(self) -> None:
        for alarm in self.alarms:
            status = "Active" if alarm.active else "Inactive"
            print(f"ID: {alarm.id} | Time: {alarm.current_time().to_str()} | Day: {alarm.day.value} | Snoozes: {alarm.snooze_count}/3 | {status}")

    def show_current_time(self) -> None:
        now = datetime.datetime.now()
        print("Current Time:", now.strftime("%H:%M:%S on %A, %d %B %Y"))

if __name__ == '__main__':
    clock = AlarmClock()
    clock.start()

    # Automatically create a 5 AM alarm on Monday with 3 snoozes (for demonstration)
    base_time = "05:00"
    day_of_week = "Monday"
    clock.add_alarm(base_time, day_of_week)
    clock.snooze_alarm_by_time_day(base_time, day_of_week)
    clock.snooze_alarm_by_time_day(base_time, day_of_week)
    clock.snooze_alarm_by_time_day(base_time, day_of_week)

    while True:
        print("\nMenu:")
        print("1. Add Alarm")
        print("2. Delete Alarm")
        print("3. Snooze Alarm")
        print("4. List Alarms")
        print("5. Show Current Time")
        print("6. Exit")

        choice: str = input("Choose an option: ")

        if choice == '1':
            time_str: str = input("Enter alarm time (HH:MM): ")
            day: str = input("Enter day of the week: ")
            clock.add_alarm(time_str, day)
        elif choice == '2':
            time_str: str = input("Enter alarm time (HH:MM): ")
            day: str = input("Enter day of the week: ")
            alarm = clock.find_alarm_by_time_day(time_str, day)
            if alarm:
                clock.delete_alarm(alarm.id)
            else:
                print("Alarm not found.")
        elif choice == '3':
            time_str: str = input("Enter alarm time (HH:MM): ")
            day: str = input("Enter day of the week: ")
            clock.snooze_alarm_by_time_day(time_str, day)
        elif choice == '4':
            clock.list_alarms()
        elif choice == '5':
            clock.show_current_time()
        elif choice == '6':
            clock.running = False
            print("Exiting Alarm Clock.")
            break
        else:
            print("Invalid option. Please try again.")
