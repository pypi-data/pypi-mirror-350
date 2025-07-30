import importlib.resources
import logging
import os
import os.path
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

from fastpluggy.core.tools.system import trigger_reload


def install_pip(force: bool = False, upgrade: bool = True) -> bool:
    """
    Ensure pip is installed for this Python interpreter.

    :param force: if True, re-install pip even if already present
    :param upgrade: if True, upgrade pip to the latest version after installation
    :return: True on success, False otherwise
    :raises CalledProcessError: if any subprocess call fails
    """
    logging.info("Checking for pip...")
    pip_installed = False
    try:
        import pip  # noqa: F401
        pip_installed = True
        logging.info(f"Found pip {pip.__version__}")
    except ImportError:
        logging.info("pip not found.")

    if pip_installed and not force:
        logging.info("Skipping pip installation.")
    else:
        # Try using ensurepip first
        try:
            import ensurepip
            logging.info("Bootstrapping pip via ensurepip...")
            ensurepip.bootstrap(upgrade=upgrade)
            logging.info("pip installed via ensurepip.")
        except (ImportError, Exception) as e:
            logging.warning(f"ensurepip failed: {e}. Falling back to get-pip.py")
            # Fallback: download get-pip.py
            url = "https://bootstrap.pypa.io/get-pip.py"
            fd, path = tempfile.mkstemp(suffix=".py")
            os.close(fd)
            try:
                logging.info(f"Downloading get-pip.py from {url}...")
                urllib.request.urlretrieve(url, path)
                cmd = [sys.executable, path]
                if upgrade:
                    cmd += ["--upgrade"]
                logging.info("Running get-pip.py...")
                subprocess.check_call(cmd)
                logging.info("pip installed via get-pip.py.")
            finally:
                try:
                    os.remove(path)
                except OSError:
                    pass

    # Optionally upgrade pip to latest
    if upgrade:
        cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
        logging.info("Upgrading pip to the latest version...")
        subprocess.check_call(cmd)
        logging.info("pip upgrade complete.")

    # Final sanity check
    try:
        import pip  # noqa: F401
        logging.info(f"pip is ready: version {pip.__version__}")
        return True
    except ImportError:
        logging.error("pip is still not available after installation!")
        return False


def init_plugins_if_needed(plugins_dir: str, enabled_plugins: list, install_requirements=True, trigger_dir=None):
    install_pip()

    plugins_dir = Path(plugins_dir)

    from fastpluggy_official_plugins import plugins as official_plugins
    plugins_embedded = importlib.resources.files(official_plugins)
    logging.debug(f"Plugins embedded: {plugins_embedded}")

    for plugin_name in enabled_plugins:
        src = plugins_embedded / plugin_name
        dest = Path(os.path.join(plugins_dir, plugin_name))

        if not dest.exists() and src.is_dir():
            shutil.copytree(src, dest)
            logging.debug(f"Copied {src} -> {dest}")

        # Try installing requirements
        if install_requirements:
            from fastpluggy.core.tools.install import install_requirements
            req_file = dest / "requirements.txt"
            logging.debug(f"Installing requirements from {req_file}")
            install_requirements(str(req_file))

        logging.debug(f"Copying {src} -> {dest}")
        logging.debug(f"src: {src.exists()}, dest: {dest.exists()}")

    if trigger_dir:
        trigger_reload(trigger_dir, create_file=True)