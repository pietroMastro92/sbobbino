import os
import subprocess
import sys
from model.config_manager import ConfigManager
from model.transcriptor_model import TranscriptorModel
from view.transcriptor_view import TranscriptorView
from controller.transcriptor_controller import TranscriptorController
from model.sbobbino_settings import SbobbinoSettings
import customtkinter as ctk
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_setup():
    setup_script = ConfigManager.get_resource_path("build_whisper.sh")
    whisper_dir = sbobbino_settings.get_property('Paths', 'whisper_dir')
    logger.info(f"Folder of whisper is {whisper_dir}!")
    try:
        subprocess.check_call(["sh", setup_script, whisper_dir])
    except subprocess.CalledProcessError as e:
        logger.error(f"Setup failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    config_file = ConfigManager.get_resource_path("config.json")
    sbobbino_settings = SbobbinoSettings()
    if not os.path.exists(config_file):
        run_setup()

    # Modes: "System" (default), "Dark", "Light"
    ctk.set_appearance_mode("System")
    # Themes: "blue" (default), "green", "dark-blue"
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    config_manager = ConfigManager()
    model = TranscriptorModel(config_manager)
    view = TranscriptorView(root, config_manager)
    controller = TranscriptorController(model, view)
    view.set_controller(controller)
    root.mainloop()
