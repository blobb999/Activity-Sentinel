import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog
from tkinter import ttk
import threading
import configparser
import subprocess
from tkinter.ttk import Progressbar
from monitor import SystemMonitor
from language import translations
import os

class ActivitySentinelApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.language = "en"  # Default language

        self.title(translations[self.language]["title"])
        self.geometry("400x800")  # Increased height to accommodate new slider

        # Create Notebook Widget
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # Monitoring Settings Frame
        self.monitoring_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.monitoring_frame, text=translations[self.language]["monitoring_settings"])

        self.state_label = tk.Label(self.monitoring_frame, text=translations[self.language]["active"], font=("Helvetica", 24, "bold"), fg="green")
        self.state_label.pack(pady=10)

        self.audio_label = tk.Label(self.monitoring_frame, text=translations[self.language]["audio_activity"] + ": " + translations[self.language]["not_detected"])
        self.audio_label.pack(pady=10)

        # Add audio level progress bar
        self.audio_level = Progressbar(self.monitoring_frame, orient="horizontal", length=200, mode="determinate", maximum=100)
        self.audio_level.pack(pady=5)

        # Audio threshold slider
        self.audio_threshold = tk.Scale(self.monitoring_frame, from_=1, to=10, orient="horizontal", length=200, label=translations[self.language]["audio_activity_duration"])
        self.audio_threshold.pack(pady=5)
        self.audio_threshold.set(1)  # Set default value to 1 second

        # Audio volume threshold slider
        self.audio_volume_threshold = tk.Scale(self.monitoring_frame, from_=0, to=100, orient="horizontal", length=200, label=translations[self.language]["audio_volume_threshold"])
        self.audio_volume_threshold.pack(pady=5)
        self.audio_volume_threshold.set(20)  # Set default value to 20

        self.mouse_label = tk.Label(self.monitoring_frame, text=translations[self.language]["mouse_activity"] + ": " + translations[self.language]["not_detected"])
        self.mouse_label.pack(pady=10)

        self.keyboard_label = tk.Label(self.monitoring_frame, text=translations[self.language]["keyboard_activity"] + ": " + translations[self.language]["not_detected"])
        self.keyboard_label.pack(pady=10)

        self.screen_label = tk.Label(self.monitoring_frame, text=translations[self.language]["screen_activity"] + ": " + translations[self.language]["not_detected"])
        self.screen_label.pack(pady=10)

        # GPU usage progress bar
        self.gpu_usage = Progressbar(self.monitoring_frame, orient="horizontal", length=200, mode="determinate", maximum=100)
        self.gpu_usage.pack(pady=5)

        # GPU threshold slider
        self.gpu_threshold = tk.Scale(self.monitoring_frame, from_=0, to=100, orient="horizontal", length=200, label=translations[self.language]["gpu_threshold"])
        self.gpu_threshold.pack(pady=5)

        # Inactivity timer label
        self.inactivity_timer_label = tk.Text(self.monitoring_frame, height=1, width=30, bg=self.cget("background"), bd=0, highlightthickness=0)
        self.inactivity_timer_label.pack(pady=10)

        # Inactivity time entry
        self.inactivity_time_entry = tk.Entry(self.monitoring_frame)
        self.inactivity_time_entry.pack(pady=5)
        self.inactivity_time_entry.insert(0, translations[self.language]["inactivity_time"])

        # Configuration settings Frame
        self.config_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.config_frame, text=translations[self.language]["configuration_settings"])

        # Labels for active and inactive states
        self.active_status_label = tk.Label(self.config_frame, text=translations[self.language]["active_status"], font=("Helvetica", 14, "bold"))
        self.active_status_label.pack(pady=5)

        # Checkboxes for activity settings
        self.audio_activity = tk.BooleanVar()
        self.mouse_activity = tk.BooleanVar()
        self.keyboard_activity = tk.BooleanVar()
        self.screen_activity = tk.BooleanVar()

        self.audio_activity_check = tk.Checkbutton(self.config_frame, text=translations[self.language]["audio_activity"], variable=self.audio_activity)
        self.audio_activity_check.pack(pady=5)
        self.mouse_activity_check = tk.Checkbutton(self.config_frame, text=translations[self.language]["mouse_activity"], variable=self.mouse_activity)
        self.mouse_activity_check.pack(pady=5)
        self.keyboard_activity_check = tk.Checkbutton(self.config_frame, text=translations[self.language]["keyboard_activity"], variable=self.keyboard_activity)
        self.keyboard_activity_check.pack(pady=5)
        self.screen_activity_check = tk.Checkbutton(self.config_frame, text=translations[self.language]["screen_activity"], variable=self.screen_activity)
        self.screen_activity_check.pack(pady=5)

        # Button for selecting activity script
        self.activity_script_button = tk.Button(self.config_frame, text=translations[self.language]["select_activity_script"], command=self.select_activity_script)
        self.activity_script_button.pack(pady=5)

        # Label for activity script
        self.activity_script_label = tk.Label(self.config_frame, text=translations[self.language]["no_activity_script"])
        self.activity_script_label.pack(pady=5)

        # Label for inactive status
        self.inactive_status_label = tk.Label(self.config_frame, text=translations[self.language]["inactive_status"], font=("Helvetica", 14, "bold"))
        self.inactive_status_label.pack(pady=5)

        # Checkboxes for inactivity settings
        self.audio_inactivity = tk.BooleanVar()
        self.mouse_inactivity = tk.BooleanVar()
        self.keyboard_inactivity = tk.BooleanVar()
        self.screen_inactivity = tk.BooleanVar()

        self.audio_inactivity_check = tk.Checkbutton(self.config_frame, text=translations[self.language]["audio_activity"], variable=self.audio_inactivity)
        self.audio_inactivity_check.pack(pady=5)
        self.mouse_inactivity_check = tk.Checkbutton(self.config_frame, text=translations[self.language]["mouse_activity"], variable=self.mouse_inactivity)
        self.mouse_inactivity_check.pack(pady=5)
        self.keyboard_inactivity_check = tk.Checkbutton(self.config_frame, text=translations[self.language]["keyboard_activity"], variable=self.keyboard_inactivity)
        self.keyboard_inactivity_check.pack(pady=5)
        self.screen_inactivity_check = tk.Checkbutton(self.config_frame, text=translations[self.language]["screen_activity"], variable=self.screen_inactivity)
        self.screen_inactivity_check.pack(pady=5)

        # Button for selecting inactivity script
        self.inactivity_script_button = tk.Button(self.config_frame, text=translations[self.language]["select_inactivity_script"], command=self.select_inactivity_script)
        self.inactivity_script_button.pack(pady=5)

        # Label for inactivity script
        self.inactivity_script_label = tk.Label(self.config_frame, text=translations[self.language]["no_inactivity_script"])
        self.inactivity_script_label.pack(pady=5)

        # Language Selection
        self.language_var = tk.StringVar(value=self.language)
        self.language_label = tk.Label(self.config_frame, text=translations[self.language]["language"])
        self.language_label.pack(pady=10)
        self.english_check = tk.Radiobutton(self.config_frame, text="English", variable=self.language_var, value="en", command=self.set_language)
        self.english_check.pack(pady=5)
        self.german_check = tk.Radiobutton(self.config_frame, text="Deutsch", variable=self.language_var, value="de", command=self.set_language)
        self.german_check.pack(pady=5)

        self.running = True  # Add the running flag
        self.monitor = SystemMonitor(self)
        self.inactivity_time = 0
        self.inactivity_script_path = None
        self.activity_script_path = None
        self.inactivity_script_executed = False

        self.audio_active_time = 0

        # Load configuration
        self.config = configparser.ConfigParser()
        self.load_config()

        # Start monitoring in a separate thread to avoid blocking the GUI
        self.monitor_thread = threading.Thread(target=self.monitor.run, daemon=True)
        self.monitor_thread.start()

        self.update_status()

    def set_language(self):
        self.language = self.language_var.get()
        self.update_translations()
        self.save_config()  # Save the language setting immediately

    def update_translations(self):
        self.title(translations[self.language]["title"])
        self.notebook.tab(0, text=translations[self.language]["monitoring_settings"])
        self.notebook.tab(1, text=translations[self.language]["configuration_settings"])
        self.state_label.config(text=translations[self.language]["active"] if self.state_label.cget("text") in ["Active", "Aktiv"] else translations[self.language]["inactive"])
        self.audio_label.config(text=translations[self.language]["audio_activity"] + ": " + (translations[self.language]["detected"] if translations[self.language]["detected"] in self.audio_label.cget("text") else translations[self.language]["not_detected"]))
        self.audio_threshold.config(label=translations[self.language]["audio_activity_duration"])
        self.audio_volume_threshold.config(label=translations[self.language]["audio_volume_threshold"])
        self.mouse_label.config(text=translations[self.language]["mouse_activity"] + ": " + (translations[self.language]["detected"] if translations[self.language]["detected"] in self.mouse_label.cget("text") else translations[self.language]["not_detected"]))
        self.keyboard_label.config(text=translations[self.language]["keyboard_activity"] + ": " + (translations[self.language]["detected"] if translations[self.language]["detected"] in self.keyboard_label.cget("text") else translations[self.language]["not_detected"]))
        self.screen_label.config(text=translations[self.language]["screen_activity"] + ": " + (translations[self.language]["detected"] if translations[self.language]["detected"] in self.screen_label.cget("text") else translations[self.language]["not_detected"]))
        self.gpu_threshold.config(label=translations[self.language]["gpu_threshold"])
        self.inactivity_script_button.config(text=translations[self.language]["select_inactivity_script"])
        self.inactivity_script_label.config(text=translations[self.language]["no_inactivity_script"] if not self.inactivity_script_path else self.inactivity_script_path)
        self.activity_script_button.config(text=translations[self.language]["select_activity_script"])
        self.activity_script_label.config(text=translations[self.language]["no_activity_script"] if not self.activity_script_path else self.activity_script_path)
        self.audio_inactivity_check.config(text=translations[self.language]["audio_activity"])
        self.mouse_inactivity_check.config(text=translations[self.language]["mouse_activity"])
        self.keyboard_inactivity_check.config(text=translations[self.language]["keyboard_activity"])
        self.screen_inactivity_check.config(text=translations[self.language]["screen_activity"])
        self.audio_activity_check.config(text=translations[self.language]["audio_activity"])
        self.mouse_activity_check.config(text=translations[self.language]["mouse_activity"])
        self.keyboard_activity_check.config(text=translations[self.language]["keyboard_activity"])
        self.screen_activity_check.config(text=translations[self.language]["screen_activity"])
        self.active_status_label.config(text=translations[self.language]["active_status"], font=("Helvetica", 14, "bold"))
        self.inactive_status_label.config(text=translations[self.language]["inactive_status"], font=("Helvetica", 14, "bold"))
        self.language_label.config(text=translations[self.language]["language"])

    def load_config(self):
        config_file = 'config.cfg'
        if not os.path.exists(config_file):
            # Set default values if the config file doesn't exist
            self.config['Settings'] = {
                'gpu_threshold': '50',
                'audio_threshold': '3',
                'audio_volume_threshold': '10',
                'inactivity_time': '60',
                'language': 'en',
                'inactivity_script_path': '',
                'activity_script_path': '',
                'audio_inactivity': 'True',
                'mouse_inactivity': 'True',
                'keyboard_inactivity': 'True',
                'screen_inactivity': 'False',
                'audio_activity': 'True',
                'mouse_activity': 'True',
                'keyboard_activity': 'True',
                'screen_activity': 'False'
            }
            with open(config_file, 'w') as configfile:
                self.config.write(configfile)

        self.config.read(config_file)
        if 'Settings' in self.config:
            self.gpu_threshold.set(self.config.getint('Settings', 'gpu_threshold', fallback=50))
            self.audio_threshold.set(self.config.getint('Settings', 'audio_threshold', fallback=1))
            self.audio_volume_threshold.set(self.config.getint('Settings', 'audio_volume_threshold', fallback=20))
            inactivity_time = self.config.get('Settings', 'inactivity_time', fallback='0')
            self.inactivity_time_entry.delete(0, tk.END)
            self.inactivity_time_entry.insert(0, inactivity_time)
            self.inactivity_script_path = self.config.get('Settings', 'inactivity_script_path', fallback=None)
            self.activity_script_path = self.config.get('Settings', 'activity_script_path', fallback=None)
            if self.inactivity_script_path:
                self.inactivity_script_label.config(text=self.inactivity_script_path)
            if self.activity_script_path:
                self.activity_script_label.config(text=self.activity_script_path)
            self.audio_inactivity.set(self.config.getboolean('Settings', 'audio_inactivity', fallback=False))
            self.mouse_inactivity.set(self.config.getboolean('Settings', 'mouse_inactivity', fallback=False))
            self.keyboard_inactivity.set(self.config.getboolean('Settings', 'keyboard_inactivity', fallback=False))
            self.screen_inactivity.set(self.config.getboolean('Settings', 'screen_inactivity', fallback=False))
            self.audio_activity.set(self.config.getboolean('Settings', 'audio_activity', fallback=False))
            self.mouse_activity.set(self.config.getboolean('Settings', 'mouse_activity', fallback=False))
            self.keyboard_activity.set(self.config.getboolean('Settings', 'keyboard_activity', fallback=False))
            self.screen_activity.set(self.config.getboolean('Settings', 'screen_activity', fallback=False))
            self.language_var.set(self.config.get('Settings', 'language', fallback='en'))
            self.set_language()
        else:
            self.config['Settings'] = {
                'gpu_threshold': '50',
                'audio_threshold': '1',
                'audio_volume_threshold': '20',
                'inactivity_time': '0',
                'language': 'en'
            }

    def save_config(self):
        self.config['Settings']['gpu_threshold'] = str(self.gpu_threshold.get())
        self.config['Settings']['audio_threshold'] = str(self.audio_threshold.get())
        self.config['Settings']['audio_volume_threshold'] = str(self.audio_volume_threshold.get())
        self.config['Settings']['inactivity_time'] = self.inactivity_time_entry.get()
        self.config['Settings']['inactivity_script_path'] = str(self.inactivity_script_path)
        self.config['Settings']['activity_script_path'] = str(self.activity_script_path)
        self.config['Settings']['audio_inactivity'] = str(self.audio_inactivity.get())
        self.config['Settings']['mouse_inactivity'] = str(self.mouse_inactivity.get())
        self.config['Settings']['keyboard_inactivity'] = str(self.keyboard_inactivity.get())
        self.config['Settings']['screen_inactivity'] = str(self.screen_inactivity.get())
        self.config['Settings']['audio_activity'] = str(self.audio_activity.get())
        self.config['Settings']['mouse_activity'] = str(self.mouse_activity.get())
        self.config['Settings']['keyboard_activity'] = str(self.keyboard_activity.get())
        self.config['Settings']['screen_activity'] = str(self.screen_activity.get())
        self.config['Settings']['language'] = self.language
        with open('config.cfg', 'w') as configfile:
            self.config.write(configfile)

    def select_inactivity_script(self):
        self.inactivity_script_path = filedialog.askopenfilename()
        if self.inactivity_script_path:
            self.inactivity_script_label.config(text=self.inactivity_script_path)

    def select_activity_script(self):
        self.activity_script_path = filedialog.askopenfilename()
        if self.activity_script_path:
            self.activity_script_label.config(text=self.activity_script_path)

    def execute_script(self, script_path):
        try:
            subprocess.run(script_path, check=True)
        except Exception as e:
            print(f"Error executing script {script_path}: {e}")

    def update_status(self):
        audio_status, mouse_status, keyboard_status, screen_status = self.monitor.get_status()

        # Determine if each activity type is monitored based on the current state and checkbox settings
        current_state = self.state_label.cget("text")
        if current_state == translations[self.language]["active"]:
            audio_monitored = self.audio_activity.get()
            mouse_monitored = self.mouse_activity.get()
            keyboard_monitored = self.keyboard_activity.get()
            screen_monitored = self.screen_activity.get()
        else:
            audio_monitored = self.audio_inactivity.get()
            mouse_monitored = self.mouse_inactivity.get()
            keyboard_monitored = self.keyboard_inactivity.get()
            screen_monitored = self.screen_inactivity.get()

        # Update the labels to show the monitoring status and activity detection
        self.audio_label.config(text=translations[self.language]["audio_activity"] + ": " + (translations[self.language]["detected"] if audio_status else translations[self.language]["not_detected"]) if audio_monitored else translations[self.language]["audio_activity"] + ": " + translations[self.language]["not_detected"])
        self.mouse_label.config(text=translations[self.language]["mouse_activity"] + ": " + (translations[self.language]["detected"] if mouse_status else translations[self.language]["not_detected"]) if mouse_monitored else translations[self.language]["mouse_activity"] + ": " + translations[self.language]["not_detected"])
        self.keyboard_label.config(text=translations[self.language]["keyboard_activity"] + ": " + (translations[self.language]["detected"] if keyboard_status else translations[self.language]["not_detected"]) if keyboard_monitored else translations[self.language]["keyboard_activity"] + ": " + translations[self.language]["not_detected"])
        self.screen_label.config(text=translations[self.language]["screen_activity"] + ": " + (translations[self.language]["detected"] if screen_status else translations[self.language]["not_detected"]) if screen_monitored else translations[self.language]["screen_activity"] + ": " + translations[self.language]["not_detected"])

        # Update audio level progress bar
        if audio_status:
            self.audio_level['value'] = self.monitor.current_audio_level
            self.audio_active_time += 1
        else:
            self.audio_level['value'] = 0
            self.audio_active_time = 0

        if self.screen_activity.get() or self.screen_inactivity.get():
            self.gpu_usage['value'] = self.monitor.get_scaled_gpu_usage()
        else:
            self.gpu_usage['value'] = 0

        try:
            inactivity_duration = int(self.inactivity_time_entry.get())
        except ValueError:
            inactivity_duration = 0

        if self.inactivity_time == 0:
            self.inactivity_time = inactivity_duration

        if current_state == translations[self.language]["active"]:
            # Check activity conditions
            activity_conditions = [
                self.audio_activity.get() and self.audio_active_time >= self.audio_threshold.get(),
                self.mouse_activity.get() and mouse_status,
                self.keyboard_activity.get() and keyboard_status,
                self.screen_activity.get() and screen_status
            ]

            if any(activity_conditions):
                self.inactivity_time = inactivity_duration
            else:
                self.inactivity_time -= 1
                if self.inactivity_time <= 0:
                    self.state_label.config(text=translations[self.language]["inactive"], fg="red")
                    if self.inactivity_script_path:
                        self.execute_script(self.inactivity_script_path)
                        self.inactivity_script_executed = True
                        self.inactivity_time = 0  # Stop decrementing

        elif current_state == translations[self.language]["inactive"]:
            # Check inactivity conditions
            inactivity_conditions = [
                not self.audio_inactivity.get() or not audio_status,
                not self.mouse_inactivity.get() or not mouse_status,
                not self.keyboard_inactivity.get() or not keyboard_status,
                not self.screen_inactivity.get() or not screen_status
            ]

            if all(inactivity_conditions):
                if self.inactivity_time < inactivity_duration:
                    self.inactivity_time = inactivity_duration
                else:
                    if self.inactivity_script_path and not self.inactivity_script_executed:
                        self.execute_script(self.inactivity_script_path)
                        self.inactivity_script_executed = True
                    self.inactivity_time = 0  # Stop decrementing
            else:
                self.inactivity_time = inactivity_duration
                if self.inactivity_script_executed:
                    self.state_label.config(text=translations[self.language]["active"], fg="green")
                    if self.activity_script_path:
                        self.execute_script(self.activity_script_path)
                    self.inactivity_script_executed = False

        # Update the inactivity timer label with larger font and dynamic color for the number only
        self.inactivity_timer_label.config(state=tk.NORMAL)
        self.inactivity_timer_label.delete(1.0, tk.END)
        self.inactivity_timer_label.tag_configure("bold_red", font=("Helvetica", 12, "bold"), foreground="red")
        self.inactivity_timer_label.tag_configure("bold_green", font=("Helvetica", 12, "bold"), foreground="green")
        self.inactivity_timer_label.tag_configure("normal", font=("Helvetica", 12), foreground="black")

        self.inactivity_timer_label.insert(tk.END, translations[self.language]["inactivity_time_label"], "normal")
        if self.inactivity_time <= 10:
            self.inactivity_timer_label.insert(tk.END, f"{self.inactivity_time}", "bold_red")
        else:
            self.inactivity_timer_label.insert(tk.END, f"{self.inactivity_time}", "bold_green")
        self.inactivity_timer_label.insert(tk.END, translations[self.language]["seconds"], "normal")
        self.inactivity_timer_label.config(state=tk.DISABLED)

        self.after(1000, self.update_status)

    def on_closing(self):
        self.running = False  # Stop the monitoring threads
        self.save_config()
        self.destroy()

if __name__ == "__main__":
    app = ActivitySentinelApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
