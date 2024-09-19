import tkinter as tk
from tkinter import filedialog
import threading
import os


class TranscriptorController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.controller = self

    def select_files(self):
        file_paths = filedialog.askopenfilenames(
            filetypes=[("Audio file", "*.m4a *.mp3 *.wav")])
        for file_path in file_paths:
            self.view.file_listbox.insert(tk.END, file_path)

    def delete_selected_files(self):
        selected_indices = self.view.file_listbox.curselection()
        for index in reversed(selected_indices):
            self.view.file_listbox.delete(index)

    def delete_all_files(self):
        self.view.file_listbox.delete(0, tk.END)

    def start_execution(self):
        self.execute_thread = threading.Thread(
            target=self.execute_commands, args=(self.model.event,))
        self.execute_thread.start()

    def execute_commands(self, event):
        try:
            self.view.stop_button.configure(state=tk.NORMAL)
            self.view.execute_button.configure(state=tk.DISABLED)
            self.view.result_text.delete('1.0', tk.END)
            self.view.result_text.update()
            file_paths = self.view.file_listbox.get(0, tk.END)
            language = self.view.language_combobox.get()
            model = self.view.models_combobox.get()
            for file_path in file_paths:
                self.model.transcript(
                    file_path, language, model, self.update_result_text)
                if event.is_set():
                    break
                file_name, _ = os.path.splitext(file_path)
                if os.path.exists(file_name + r".txt"):
                    self.model.reformat_text(
                        file_name + r".txt", file_name + '.docx', 50)
                    os.remove(file_name + r".txt")
        finally:
            event.clear()
            self.view.root.after(0, self.update_buttons_state)

    def update_buttons_state(self):
        self.view.stop_button.configure(state=tk.DISABLED)
        self.view.execute_button.configure(state=tk.NORMAL)

    def stop_transcription(self):
        if tk.messagebox.askyesno("Stop the transcription?", "Are you sure you want to stop the transcription?"):
            self.model.event.set()
            self.model.terminate_process()
            self.update_result_text("Interrupted transcript. Please wait.\n")

    def update_result_text(self, text):
        self.view.root.after(0, self.view.update_result_text, text)
