import time
import datetime
import threading
import uuid

# Engineering Design Notes:
# - The system is modular with Alarm and AlarmClock classes.
# - Alarm encapsulates the state and logic for individual alarms.
# - AlarmClock manages the collection of alarms and user interactions.
# - All input/output interactions are handled via a command-line interface.

class Alarm:
    def __init__(self, alarm_id: str, time_str: str, day: str):
        self.id: str = alarm_id                    
        self.time: str = time_str                 
        self.day: str = day                       
        self.snooze_count: int = 0                 
        self.active: bool = True                  

    def snooze(self) -> None:
        if self.snooze_count < 3:
            hour, minute = map(int, self.time.split(':'))
            alarm_time = datetime.datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
            snoozed_time = alarm_time + datetime.timedelta(minutes=5)
            self.time = snoozed_time.strftime('%H:%M')
            self.snooze_count += 1
            print(f"Alarm {self.id} snoozed to {self.time}")

    def reset_snooze(self) -> None:
        self.snooze_count = 0

class AlarmClock:
    def __init__(self):
        self.alarms: list[Alarm] = []              
        self.running: bool = True                  

    def add_alarm(self, time_str: str, day: str) -> None:
        alarm_id = str(uuid.uuid4())
        alarm = Alarm(alarm_id, time_str, day)
        self.alarms.append(alarm)
        print(f"Alarm set for {time_str} on {day} (ID: {alarm.id})")

    def delete_alarm(self, alarm_id: str) -> None:
        self.alarms = [alarm for alarm in self.alarms if alarm.id != alarm_id]
        print(f"Deleted alarm {alarm_id}")

    def snooze_alarm(self, alarm_id: str) -> None:
        for alarm in self.alarms:
            if alarm.id == alarm_id:
                alarm.snooze()
                break

    def snooze_alarm_by_time_day(self, time_str: str, day: str) -> None:
        alarm = self.find_alarm_by_time_day(time_str, day)
        if alarm:
            self.snooze_alarm(alarm.id)
        else:
            print(f"No alarm found for {time_str} on {day}.")

    def find_alarm_by_time_day(self, time_str: str, day: str) -> Alarm | None:
        for alarm in self.alarms:
            if alarm.time == time_str and alarm.day.lower() == day.lower():
                return alarm
        return None

    def check_alarms(self) -> None:
        while self.running:
            now = datetime.datetime.now()
            current_time = now.strftime('%H:%M')
            current_day = now.strftime('%A')
            for alarm in self.alarms:
                if alarm.active and alarm.time == current_time and alarm.day == current_day:
                    print(f"\n*** ALARM! It's {alarm.time} on {alarm.day} ***")
                    alarm.active = False
            time.sleep(60)  # Check every minute

    def start(self) -> None:
        print("Alarm Clock started.")
        threading.Thread(target=self.check_alarms, daemon=True).start()

    def list_alarms(self) -> None:
        for alarm in self.alarms:
            status = "Active" if alarm.active else "Inactive"
            print(f"ID: {alarm.id} | Time: {alarm.time} | Day: {alarm.day} | Snoozes: {alarm.snooze_count}/3 | {status}")

    def show_current_time(self) -> None:
        now = datetime.datetime.now()
        print("Current Time:", now.strftime("%H:%M:%S on %A, %d %B %Y"))

if __name__ == '__main__':
    clock = AlarmClock()
    clock.start()

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
