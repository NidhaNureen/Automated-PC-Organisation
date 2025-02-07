import threading
import time
import schedule
import CleanUpFeatures
import Logger


# Function to trigger clean-up (temp)
def start_cleanup(days):
    print(f"Running cleanup (Interval: {days} days)")  # Debugging message
    CleanUpFeatures.save_days(days)  # Save interval
    try:
        Logger.clean_up_log()  # Run cleanup and log it
    except Exception as e:
        print(f"Error in cleanup: {e}")
    print("Cleanup completed.")  # Debugging message


def background_cleanup(interval):
    schedule.clear()
    schedule.every(10).seconds.do(start_cleanup, interval)  # Pass argument directly

    while True:
        print("Checking schedule...")  # Debugging message
        schedule.run_pending()
        time.sleep(2)  # Check every 2 sec


test_interval = 30  # Normal interval in days

threading.Thread(target=background_cleanup, args=(test_interval,), daemon=True).start()
print("Scheduler started...")  # Debugging message

# Keep script running
while True:
    time.sleep(1)

