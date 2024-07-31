import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog
from tkinter import ttk
import threading
import configparser
import subprocess
from tkinter.ttk import Progressbar
from monitor import SystemMonitor

class ActivitySentinelApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Activity Sentinel")
        self.geometry("400x800")  # Increased height to accommodate new slider

        # Notebook Widget erstellen
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # Monitoring-Einstellungen Frame
        self.monitoring_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.monitoring_frame, text='Monitoring-Einstellungen')

        self.state_label = tk.Label(self.monitoring_frame, text="Active", font=("Helvetica", 24, "bold"), fg="green")
        self.state_label.pack(pady=10)

        self.audio_label = tk.Label(self.monitoring_frame, text="Audio Aktivität: Nicht erkannt")
        self.audio_label.pack(pady=10)

        # Pegelmonitor hinzufügen
        self.audio_level = Progressbar(self.monitoring_frame, orient="horizontal", length=200, mode="determinate", maximum=100)
        self.audio_level.pack(pady=5)

        # Audio Schwellenwert Slider
        self.audio_threshold = tk.Scale(self.monitoring_frame, from_=1, to=10, orient="horizontal", length=200, label="Audioaktivitätsdauer (Sekunden)")
        self.audio_threshold.pack(pady=5)
        self.audio_threshold.set(1)  # Standardwert auf 1 Sekunde setzen

        # Audio Volume Threshold Slider
        self.audio_volume_threshold = tk.Scale(self.monitoring_frame, from_=0, to=100, orient="horizontal", length=200, label="Audiolautstärke Schwellenwert")
        self.audio_volume_threshold.pack(pady=5)
        self.audio_volume_threshold.set(20)  # Standardwert auf 20 setzen

        self.mouse_label = tk.Label(self.monitoring_frame, text="Maus Aktivität: Nicht erkannt")
        self.mouse_label.pack(pady=10)

        self.keyboard_label = tk.Label(self.monitoring_frame, text="Tastatur Aktivität: Nicht erkannt")
        self.keyboard_label.pack(pady=10)

        self.screen_label = tk.Label(self.monitoring_frame, text="Bildschirm Aktivität: Nicht erkannt")
        self.screen_label.pack(pady=10)

        # GPU Auslastung Monitor
        self.gpu_usage = Progressbar(self.monitoring_frame, orient="horizontal", length=200, mode="determinate", maximum=100)
        self.gpu_usage.pack(pady=5)

        # GPU Schwellenwert Slider
        self.gpu_threshold = tk.Scale(self.monitoring_frame, from_=0, to=100, orient="horizontal", length=200, label="GPU-Schwellenwert")
        self.gpu_threshold.pack(pady=5)

        # Inaktivitäts-Timer Label
        self.inactivity_timer_label = tk.Text(self.monitoring_frame, height=1, width=30, bg=self.cget("background"), bd=0, highlightthickness=0)
        self.inactivity_timer_label.pack(pady=10)

        # Eingabe für Inaktivitätszeit
        self.inactivity_time_entry = tk.Entry(self.monitoring_frame)
        self.inactivity_time_entry.pack(pady=5)
        self.inactivity_time_entry.insert(0, "Zeit in Sekunden bis Skript ausgeführt wird")

        # Konfigurationseinstellungen Frame
        self.config_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.config_frame, text='Konfigurationseinstellungen')

        # Checkboxen für Inaktivitätseinstellungen
        self.audio_inactivity = tk.BooleanVar()
        self.mouse_inactivity = tk.BooleanVar()
        self.keyboard_inactivity = tk.BooleanVar()
        self.screen_inactivity = tk.BooleanVar()

        self.audio_inactivity_check = tk.Checkbutton(self.config_frame, text="Audio bei Inaktivität berücksichtigen", variable=self.audio_inactivity)
        self.audio_inactivity_check.pack(pady=5)
        self.mouse_inactivity_check = tk.Checkbutton(self.config_frame, text="Maus bei Inaktivität berücksichtigen", variable=self.mouse_inactivity)
        self.mouse_inactivity_check.pack(pady=5)
        self.keyboard_inactivity_check = tk.Checkbutton(self.config_frame, text="Tastatur bei Inaktivität berücksichtigen", variable=self.keyboard_inactivity)
        self.keyboard_inactivity_check.pack(pady=5)
        self.screen_inactivity_check = tk.Checkbutton(self.config_frame, text="Bildschirm bei Inaktivität berücksichtigen", variable=self.screen_inactivity)
        self.screen_inactivity_check.pack(pady=5)

        # Button für Inaktivitäts-Skript-Auswahl
        self.inactivity_script_button = tk.Button(self.config_frame, text="Inaktivitäts-Skript wählen", command=self.select_inactivity_script)
        self.inactivity_script_button.pack(pady=5)

        # Label für Inaktivitäts-Skript
        self.inactivity_script_label = tk.Label(self.config_frame, text="Kein Inaktivitäts-Skript ausgewählt")
        self.inactivity_script_label.pack(pady=5)

        # Checkboxen für Aktivitätseinstellungen
        self.audio_activity = tk.BooleanVar()
        self.mouse_activity = tk.BooleanVar()
        self.keyboard_activity = tk.BooleanVar()
        self.screen_activity = tk.BooleanVar()

        self.audio_activity_check = tk.Checkbutton(self.config_frame, text="Audio bei Aktivität berücksichtigen", variable=self.audio_activity)
        self.audio_activity_check.pack(pady=5)
        self.mouse_activity_check = tk.Checkbutton(self.config_frame, text="Maus bei Aktivität berücksichtigen", variable=self.mouse_activity)
        self.mouse_activity_check.pack(pady=5)
        self.keyboard_activity_check = tk.Checkbutton(self.config_frame, text="Tastatur bei Aktivität berücksichtigen", variable=self.keyboard_activity)
        self.keyboard_activity_check.pack(pady=5)
        self.screen_activity_check = tk.Checkbutton(self.config_frame, text="Bildschirm bei Aktivität berücksichtigen", variable=self.screen_activity)
        self.screen_activity_check.pack(pady=5)

        # Button für Aktivitäts-Skript-Auswahl
        self.activity_script_button = tk.Button(self.config_frame, text="Aktivitäts-Skript wählen", command=self.select_activity_script)
        self.activity_script_button.pack(pady=5)

        # Label für Aktivitäts-Skript
        self.activity_script_label = tk.Label(self.config_frame, text="Kein Aktivitäts-Skript ausgewählt")
        self.activity_script_label.pack(pady=5)

        self.running = True  # Add the running flag
        self.monitor = SystemMonitor(self)
        self.inactivity_time = 0
        self.inactivity_script_path = None
        self.activity_script_path = None
        self.inactivity_script_executed = False

        self.audio_active_time = 0

        # Laden der Konfiguration
        self.config = configparser.ConfigParser()
        self.load_config()

        # Start monitoring in a separate thread to avoid blocking the GUI
        self.monitor_thread = threading.Thread(target=self.monitor.run, daemon=True)
        self.monitor_thread.start()

        self.update_status()

    def load_config(self):
        self.config.read('config.cfg')
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
        else:
            self.config['Settings'] = {'gpu_threshold': '50', 'audio_threshold': '1', 'audio_volume_threshold': '20', 'inactivity_time': '0'}

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
        if current_state == "Active":
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
        self.audio_label.config(text=f"Audio Aktivität: {'Erkannt' if audio_status else 'Nicht erkannt'}" if audio_monitored else "Audio Aktivität: deactivated")
        self.mouse_label.config(text=f"Maus Aktivität: {'Erkannt' if mouse_status else 'Nicht erkannt'}" if mouse_monitored else "Maus Aktivität: deactivated")
        self.keyboard_label.config(text=f"Tastatur Aktivität: {'Erkannt' if keyboard_status else 'Nicht erkannt'}" if keyboard_monitored else "Tastatur Aktivität: deactivated")
        self.screen_label.config(text=f"Bildschirm Aktivität: {'Erkannt' if screen_status else 'Nicht erkannt'}" if screen_monitored else "Bildschirm Aktivität: deactivated")

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

        if current_state == "Active":
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
                    self.state_label.config(text="Inactive", fg="red")
                    if self.inactivity_script_path:
                        self.execute_script(self.inactivity_script_path)
                        self.inactivity_script_executed = True
                        self.inactivity_time = 0  # Stop decrementing

        elif current_state == "Inactive":
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
                    self.state_label.config(text="Active", fg="green")
                    if self.activity_script_path:
                        self.execute_script(self.activity_script_path)
                        self.inactivity_script_executed = False

        # Update the inactivity timer label with larger font and dynamic color for the number only
        self.inactivity_timer_label.config(state=tk.NORMAL)
        self.inactivity_timer_label.delete(1.0, tk.END)
        self.inactivity_timer_label.tag_configure("bold_red", font=("Helvetica", 12, "bold"), foreground="red")
        self.inactivity_timer_label.tag_configure("bold_green", font=("Helvetica", 12, "bold"), foreground="green")
        self.inactivity_timer_label.tag_configure("normal", font=("Helvetica", 12), foreground="black")

        self.inactivity_timer_label.insert(tk.END, "Inaktivitätszeit: ", "normal")
        if self.inactivity_time <= 10:
            self.inactivity_timer_label.insert(tk.END, f"{self.inactivity_time}", "bold_red")
        else:
            self.inactivity_timer_label.insert(tk.END, f"{self.inactivity_time}", "bold_green")
        self.inactivity_timer_label.insert(tk.END, " Sekunden", "normal")
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
