import json
import time
import schedule
import random
from tkinter import Tk, Label, Button, Toplevel, messagebox
import screeninfo  # Used to get screen information

# Load JSON configuration
def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Display custom notification window
def show_notification(message):
    # Get screen resolution information
    screen = screeninfo.get_monitors()[0]
    screen_width = screen.width
    screen_height = screen.height

    # Create a new popup window
    popup = Toplevel()
    popup.title("Reminder")

    # Set window size
    window_width = 300
    window_height = 150

    # Calculate the position of the popup (close to the bottom right taskbar)
    x_position = screen_width - window_width - 20  # Near the right side
    y_position = screen_height - window_height - 80  # Near the bottom, considering the taskbar height

    # Set the size and position of the window
    popup.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Set message label
    label = Label(popup, text=message, wraplength=280)
    label.pack(pady=10)

    # List of energetic phrases
    button_texts = ["Got it! ", "Great", "Let's go!!", "Ready","Let's do this!","Ok","Sound good"]

    # Create a button to close the window with random text
    button = Button(popup, text=random.choice(button_texts), command=popup.destroy)
    button.pack(pady=5)

    # Keep the popup window on top
    popup.attributes('-topmost', True)

    # Ensure the main window does not block
    popup.mainloop()

# Randomly select a reminder message
def select_random_message(messages):
    if isinstance(messages, list):
        return random.choice(messages)
    return messages  # If not a list, return the message directly

# Set interval reminders
def set_interval_reminder(messages, minutes):
    message = select_random_message(messages)
    schedule.every(minutes).minutes.do(lambda: show_notification(message))

# Set time-based reminders
def set_time_reminder(messages, times):
    for time in times:
        message = select_random_message(messages)
        schedule.every().day.at(time).do(lambda: show_notification(message))

# Display initial confirmation window
def show_initial_confirmation(config):
    root = Tk()
    root.withdraw()  # Hide the main window

    # Retrieve reminder messages and timing settings, and form the confirmation message
    reminders_info = '\n'.join(
        [f"Message: {reminder['message']}, "
         f"Interval: {reminder.get('interval_minutes', 'N/A')} minutes, "
         f"Time: {', '.join(reminder.get('time', [])) or 'N/A'}"
         for reminder in config['reminders']]
    )

    confirm_message = f"Please confirm your config:\n\n{reminders_info}\n\nIs this correct?"

    # Display the confirmation dialog box
    user_response = messagebox.askyesno("Config Confirmation", confirm_message)
    if not user_response:
        messagebox.showinfo("Reminder Notifier", "Please update your config and restart the program.")
        root.destroy()
        exit()  # Exit the program

    root.destroy()  # Close the dialog box

# Main program
def main():
    config = load_config('config.json')
    show_initial_confirmation(config)  # Confirm settings
    reminders = config.get('reminders', [])

    # Set reminders according to JSON configuration
    for reminder in reminders:
        messages = reminder.get('message')
        interval_minutes = reminder.get('interval_minutes')
        times = reminder.get('time', [])

        if interval_minutes:
            set_interval_reminder(messages, interval_minutes)
        if times:
            set_time_reminder(messages, times)

    # Run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
