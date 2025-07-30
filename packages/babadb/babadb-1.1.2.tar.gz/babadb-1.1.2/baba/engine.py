import os
from datetime import datetime

class BabaEngine:
    def __init__(self, filepath: str, logging: str = "console") -> None:
        self.filepath = filepath
        self.logging = logging
        if logging == "file":
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.log_folder = f"baba_logs/{now}"
            os.makedirs(self.log_folder, exist_ok=True)
            self.log_file = open(f"{self.log_folder}.log", "a", encoding="utf-8")
        else:
            self.log_file = None

    def log(self, msg: str, level: str = "INFO") -> None:
        colors = {
            "INFO": "\033[92m",
            "ERROR": "\033[91m",
            "WARNING": "\033[93m",
            "ENDC": "\033[0m"
        }
        text = f"[{level}] {msg}"
        if self.logging == "false":
            return
        if self.logging == "file" and self.log_file:
            self.log_file.write(text + "\n")
            self.log_file.flush()
        else:
            color = colors.get(level, "")
            endc = colors["ENDC"]
            print(f"{color}{text}{endc}")

    def close(self):
        if self.log_file:
            self.log_file.close()
