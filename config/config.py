from pathlib import Path


def get_project_dir():
    # Get the root directory of the FastAPI project
    return Path(__file__).resolve().parent.parent


def get_log_dir():
    projectDir = get_project_dir()
    logDir = projectDir / "log"
    if not logDir.exists:
        logDir.mkdir(parents=True, exist_ok=True)
    return logDir