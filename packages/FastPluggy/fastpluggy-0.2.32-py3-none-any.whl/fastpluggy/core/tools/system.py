import logging
import os
import signal
from pathlib import Path


def restart_application():
    os.kill(os.getpid(), signal.SIGINT)

def restart_application_force():
    os.kill(os.getpid(), signal.SIGKILL)


def trigger_reload(plugins_dir: Path | str, create_file:bool = False):
    plugins_dir = Path(plugins_dir)

    logging.info(f"Touching/delete an file under plugins_dir is enough to trigger uvicorn reload: {plugins_dir}")

    marker = plugins_dir / ".reload-trigger"
    # toggle it so every call is a filesystem event
    if marker.exists():
        marker.unlink()
        logging.info("Removed reload marker")
    else:
        if create_file:
            marker.write_text("reload\n")
            logging.info("Created reload marker")