import ctypes
from ctypes import wintypes
from pynput import mouse, keyboard
import threading
import voicemeeterlib
import logging
import time
import pythoncom
from py3nvml.py3nvml import *
from pycaw.pycaw import AudioUtilities, IAudioMeterInformation
from comtypes import CLSCTX_ALL

# Setup logging for debugging
logging.basicConfig(level=logging.INFO)

class SystemMonitor:

    def __init__(self, gui):
        self.gui = gui
        self.mouse_activity = False
        self.keyboard_activity = False
        self.audio_activity = False
        self.current_audio_level = 0
        self.current_gpu_usage = 0
        self.voicemeeter_available = False

        # Versuch, Voicemeeter Remote API einzurichten
        try:
            self.vmr = voicemeeterlib.api('banana', ldirty=True)
            self.vmr.login()
            self.voicemeeter_available = True
        except voicemeeterlib.error.CAPIError as e:
            logging.error(f"VoiceMeeter nicht verfügbar: {e}")
            self.voicemeeter_available = False

        try:
            # Initialize NVML for GPU usage
            nvmlInit()
            self.gpu_monitoring_enabled = True
        except Exception as e:
            logging.error(f"Error initializing NVML: {e}")
            self.gpu_monitoring_enabled = False

        # Setup listeners for mouse and keyboard
        self.mouse_listener = mouse.Listener(on_move=self.on_mouse_event, on_click=self.on_mouse_event, on_scroll=self.on_mouse_event)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_keyboard_event)
        self.mouse_listener.start()
        self.keyboard_listener.start()

        # Start GPU monitoring thread
        self.gpu_monitor_thread = threading.Thread(target=self.monitor_gpu_usage, daemon=True)
        self.gpu_monitor_thread.start()

        # Start audio monitoring thread if VoiceMeeter is not available
        if not self.voicemeeter_available:
            self.audio_monitor_thread = threading.Thread(target=self.monitor_audio_pycaw, daemon=True)
            self.audio_monitor_thread.start()

    def on_mouse_event(self, *args):
        self.mouse_activity = True

    def on_keyboard_event(self, *args):
        self.keyboard_activity = True

    def check_audio_activity(self):
        audio_threshold = self.gui.audio_volume_threshold.get()
        if self.voicemeeter_available:
            try:
                if self.vmr.ldirty:  # Check if level values are updated
                    for i in range(3):  # Check the first 3 outputs (A1, A2, A3)
                        level = self.vmr.bus[i].levels.all  # Get level for A1, A2, A3
                        logging.debug(f"Output A{i+1} Level: {level}")  # Debug output
                        if audio_threshold == 0:
                            # Use a very low threshold but not zero
                            sensitivity_threshold = -60 + 0.1
                            if level[0] > sensitivity_threshold:
                                self.current_audio_level = self.convert_level_to_percentage(level[0])
                                return True
                        elif level[0] > -40:  # Check only the first value of the tuple
                            self.current_audio_level = self.convert_level_to_percentage(level[0])
                            return self.current_audio_level >= audio_threshold
                return False
            except Exception as e:
                logging.error(f"Error checking audio activity: {e}")
                return False
        else:
            # Audio monitoring using pycaw is handled in the separate thread
            return self.audio_activity

    def convert_level_to_percentage(self, level):
        # Convert audio level to percentage for the progress bar
        min_level = -60
        max_level = 0
        return max(0, min(100, 100 * (level - min_level) / (max_level - min_level)))

    def monitor_audio_pycaw(self):
        pythoncom.CoInitialize()  # Ensure COM is initialized in this thread
        while self.gui.running:
            try:
                sessions = AudioUtilities.GetAllSessions()
                audio_active = False
                max_volume = 0
                for session in sessions:
                    volume = session._ctl.QueryInterface(IAudioMeterInformation).GetPeakValue()
                    if volume > 0.01:  # Consider audio active if volume is above a threshold
                        audio_active = True
                        max_volume = max(max_volume, volume)
                self.current_audio_level = int(max_volume * 100)  # Convert to percentage
                self.audio_activity = audio_active
            except Exception as e:
                logging.error(f"Error checking audio activity via pycaw: {e}")
                self.audio_activity = False
                self.current_audio_level = 0
            time.sleep(1)

    def monitor_gpu_usage(self):
        while self.gui.running:
            if not self.gpu_monitoring_enabled:
                break
            try:
                if self.gui.screen_activity.get() or self.gui.screen_inactivity.get():  # Check if GPU monitoring is enabled
                    pythoncom.CoInitialize()  # Ensure WMI is initialized in this thread
                    handle = nvmlDeviceGetHandleByIndex(0)  # Assuming only one GPU is present
                    utilization = nvmlDeviceGetUtilizationRates(handle)
                    self.current_gpu_usage = utilization.gpu
                else:
                    self.current_gpu_usage = 0  # Reset GPU usage if monitoring is disabled
            except Exception as e:
                logging.error(f"Error checking GPU activity: {e}")
                self.current_gpu_usage = 0
            time.sleep(1)  # Check every second

    def get_scaled_gpu_usage(self):
        # Scale GPU usage value
        return min(100, self.current_gpu_usage * 10)

    def check_screen_activity(self):
        if not self.gpu_monitoring_enabled:
            return False
        return self.get_scaled_gpu_usage() > self.gui.gpu_threshold.get()

    def get_status(self):
        audio_status = self.check_audio_activity()
        mouse_status = self.mouse_activity
        keyboard_status = self.keyboard_activity
        screen_status = self.check_screen_activity() if (self.gui.screen_activity.get() or self.gui.screen_inactivity.get()) else False
        # Reset activity status
        self.mouse_activity = False
        self.keyboard_activity = False
        return audio_status, mouse_status, keyboard_status, screen_status

    def run(self):
        # Necessary call to capture input events
        self.mouse_listener.join()
        self.keyboard_listener.join()

    def __del__(self):
        if self.gpu_monitoring_enabled:
            nvmlShutdown()  # Cleanup NVML
