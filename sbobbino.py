import os
import subprocess
import sys
from model.transcriptor_model import TranscriptorModel
from view.transcriptor_view import TranscriptorView
from controller.transcriptor_controller import TranscriptorController
import customtkinter as ctk
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


if __name__ == "__main__":

    # Modes: "System" (default), "Dark", "Light"
    ctk.set_appearance_mode("System")
    # Themes: "blue" (default), "green", "dark-blue"
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    model = TranscriptorModel()
    view = TranscriptorView(root)
    controller = TranscriptorController(model, view)
    view.set_controller(controller)
    root.mainloop()
