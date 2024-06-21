import customtkinter as ctk
import tkinter as tk
import os
import sys
import logging
from model.config_manager import ConfigManager

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TranscriptorView:
    def __init__(self, root, config_manager: ConfigManager):
        self.root = root
        self.controller = None
        self.config_manager = config_manager
        self.create_widgets()

    def get_resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def create_widgets(self):
        self.root.title("Sbobbino")
        self.root.geometry("1400x560")

        # Set a background color that will be used for the control frame
        background_color = self.root.cget("bg")

        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        self.control_frame = ctk.CTkFrame(
            self.main_frame)
        self.control_frame.grid(
            row=0, column=0, sticky=ctk.NW, padx=10, pady=10)

        self.select_button = ctk.CTkButton(
            self.control_frame, text="Select Audio File", command=self.select_files)
        self.select_button.grid(
            row=0, column=0, columnspan=2, pady=8, sticky=ctk.EW)

        self.file_listbox = tk.Listbox(
            self.control_frame, height=10, bg=background_color)
        self.file_listbox.grid(
            row=1, column=0, columnspan=2, pady=10, sticky=ctk.EW)

        self.delete_selected_button = ctk.CTkButton(
            self.control_frame, text="Remove Selected", command=self.delete_selected_files)
        self.delete_selected_button.grid(
            row=2, column=0, pady=5, sticky=ctk.EW)

        self.delete_all_button = ctk.CTkButton(
            self.control_frame, text="Delete All", command=self.delete_all_files)
        self.delete_all_button.grid(row=2, column=1, pady=5, sticky=ctk.EW)

        languages = ["auto", "it", "en"]
        self.language_label = ctk.CTkLabel(
            self.control_frame, text="Select Transcription Language")
        self.language_label.grid(row=3, column=0, columnspan=2, pady=5)
        self.language_combobox = ctk.CTkComboBox(
            self.control_frame, values=languages)
        self.language_combobox.set("auto")
        self.language_combobox.grid(
            row=4, column=0, columnspan=2, pady=5, sticky=ctk.EW)

        # Automatically list the models present in the models folder
        models_path = self.get_resource_path(self.config_manager.get('models_path'))
        model_files = [f for f in os.listdir(
            models_path) if f.startswith("ggml") and f.endswith(".bin")]
        self.models_combobox = ctk.CTkComboBox(
            self.control_frame, values=model_files)
        self.models_combobox.set(model_files[0])
        self.models_combobox.grid(
            row=6, column=0, columnspan=2, pady=5, sticky=ctk.EW)

        self.execute_button = ctk.CTkButton(
            self.control_frame, text="Start Transcription", command=self.start_execution)
        self.execute_button.grid(
            row=7, column=0, columnspan=2, pady=5, sticky=ctk.EW)

        self.stop_button = ctk.CTkButton(
            self.control_frame, text="Stop Transcription", command=self.stop_transcription)
        self.stop_button.grid(
            row=8, column=0, columnspan=2, pady=5, sticky=ctk.EW)
        self.stop_button.configure(state=ctk.DISABLED)

        self.result_frame = ctk.CTkFrame(self.main_frame)
        self.result_frame.grid(
            row=0, column=1, sticky=ctk.NSEW, rowspan=9, padx=10, pady=10)

        self.result_text = ctk.CTkTextbox(
            self.result_frame, wrap=ctk.WORD)
        self.result_text.pack(fill=ctk.BOTH, expand=True)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=3)

    def set_controller(self, controller):
        self.controller = controller

    def update_result_text(self, text):
        self.result_text.insert(ctk.END, text)
        self.result_text.see(ctk.END)

    def select_files(self):
        self.controller.select_files()

    def delete_selected_files(self):
        self.controller.delete_selected_files()

    def delete_all_files(self):
        self.controller.delete_all_files()

    def start_execution(self):
        self.controller.start_execution()

    def stop_transcription(self):
        self.controller.stop_transcription()
