import os
import subprocess
import ffmpeg
from docx import Document
from docx.shared import Pt
from threading import Event
import logging
import pty

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TranscriptorModel:
    def __init__(self):
        self.event = Event()
        self.process = None

    def transcript(self, file_path, language, model, update_result_text):
        file_name, file_extension = os.path.splitext(file_path)
        if file_extension.lower() == ".wav":
            update_result_text(
                "The file  is already in WAV format. Conversion is not needed\n")
        else:
            file_name_without_extension = file_name
            output_file = f'{file_name_without_extension}.wav'
            try:
                update_result_text(
                    f"FFMPEG-->CONVERSION OF {file_path} in WAV\n")
                (
                    ffmpeg
                    .input(file_path)
                    .output(f'{file_name_without_extension}.wav', ar=16000, ac=1, codec='pcm_s16le')
                    .overwrite_output()
                    .run()
                )
                update_result_text(
                    f"File converted successfully to {output_file}")
                file_path = f'{file_name_without_extension}.wav'
            except ffmpeg.Error as e:
                update_result_text(f"Error occurred: {e.stderr.decode()}")

        file_name_without_extension = os.path.splitext(file_path)[0]
        dirName = os.path.dirname(file_path)
        if language == "auto":
            command = f"whisper '{file_name_without_extension}.wav' --model {model} -f txt -o {dirName} --threads 4"
        else:
            command = f"whisper '{file_name_without_extension}.wav' --language {language} --model {model} -f txt -o {dirName} --threads 4"

        update_result_text(f"Execution of: {command}\n")

        master_fd, slave_fd = pty.openpty()
        self.process = subprocess.Popen(
            command,
            shell=True,
            stdout=master_fd,
            stderr=slave_fd,
            stdin=subprocess.DEVNULL,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        os.close(slave_fd)

        try:
            with os.fdopen(master_fd) as stdout:
                for line in iter(stdout.readline, ''):
                    if self.event.is_set():
                        self.process.kill()
                        break
                    if line:
                        update_result_text(line)
        except Exception as e:
            update_result_text(f"An error occurred: {str(e)}")
        finally:
            self.process.wait()
            self.process = None

    def terminate_process(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()

    def reformat_text(self, input_file, output_file, words_per_line):
        try:
            with open(input_file, 'r') as f:
                content = f.read().split()

            formatted_text = []
            line = ""
            for word in content:
                line += word + " "
                if len(line.split()) >= words_per_line:
                    formatted_text.append(line.strip())
                    line = ""

            if line:
                formatted_text.append(line.strip())

            doc = Document()
            for line in formatted_text:
                p = doc.add_paragraph(line)
                paragraph_format = p.paragraph_format
                paragraph_format.space_after = Pt(0)

            doc.save(output_file)
            # logger.info(f"Reformatted and justified text saved as {output_file}")
        except FileNotFoundError:
            logger.error(f"Error: File '{input_file}' not found.")
