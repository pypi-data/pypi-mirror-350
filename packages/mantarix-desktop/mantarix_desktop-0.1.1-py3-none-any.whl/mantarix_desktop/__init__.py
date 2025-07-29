import asyncio
import os
import signal
import subprocess
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path

from mantarix.utils import (
    get_arch,
    is_linux,
    is_macos,
    is_windows,
    random_string,
    safe_tar_extractall,
)

from rich.console import Console
from rich.theme import Theme

console = Console(log_path=False, theme=Theme({"log.message": "green bold"}))

import mantarix_desktop
import mantarix_desktop.version

def get_package_bin_dir():
    return str(Path(__file__).parent.joinpath("app"))


def open_mantarix_view(page_url, assets_dir, hidden):
    args, mantarix_env, pid_file = __locate_and_unpack_mantarix_view(
        page_url, assets_dir, hidden
    )
    return subprocess.Popen(args, env=mantarix_env), pid_file


async def open_mantarix_view_async(page_url, assets_dir, hidden):
    args, mantarix_env, pid_file = __locate_and_unpack_mantarix_view(
        page_url, assets_dir, hidden
    )
    return (
        await asyncio.create_subprocess_exec(args[0], *args[1:], env=mantarix_env),
        pid_file,
    )


def close_mantarix_view(pid_file):
    if pid_file is not None and os.path.exists(pid_file):
        try:
            with open(pid_file) as f:
                fvp_pid = int(f.read())
            console.log(f"Mantarix View process {fvp_pid}")
            os.kill(fvp_pid, signal.SIGKILL)
        except Exception:
            pass
        finally:
            os.remove(pid_file)


def __locate_and_unpack_mantarix_view(page_url, assets_dir, hidden):
    console.status(
        "Starting Mantarix View app...",
        spinner="bouncingBall",
    )

    args = []

    # pid file - Mantarix client writes its process ID to this file
    pid_file = str(Path(tempfile.gettempdir()).joinpath(random_string(20)))

    if is_windows():
        mantarix_exe = "mantarix.exe"
        temp_mantarix_dir = Path.home().joinpath(
            ".mantarix", "bin", f"mantarix-{mantarix_desktop.version.version}"
        )

        # check if mantarix_view.exe exists in "bin" directory (user mode)
        mantarix_path = os.path.join(get_package_bin_dir(), "mantarix", mantarix_exe)
        if os.path.exists(mantarix_path):
            console.log(f"Mantarix View found in: {mantarix_path}")
        else:
            # check if mantarix.exe is in MANTARIX_VIEW_PATH (mantarix developer mode)
            mantarix_path = os.environ.get("MANTARIX_VIEW_PATH")
            if mantarix_path and os.path.exists(mantarix_path):
                console.log(f"Mantarix View found in PATH: {mantarix_path}")
                mantarix_path = os.path.join(mantarix_path, mantarix_exe)
            else:
                if not temp_mantarix_dir.exists():
                    console.log(f"Platform is Windows!")
                    zip_file = __download_mantarix_client("mantarix-windows.zip")

                    console.log(f"Extracting mantarix.exe from archive to {temp_mantarix_dir}")
                    temp_mantarix_dir.mkdir(parents=True, exist_ok=True)
                    with zipfile.ZipFile(zip_file, "r") as zip_arch:
                        zip_arch.extractall(str(temp_mantarix_dir))
                    os.remove(zip_file)
                mantarix_path = str(temp_mantarix_dir.joinpath("mantarix", mantarix_exe))
        args = [mantarix_path, page_url, pid_file]
    elif is_macos():
        # build version-specific path to Mantarix.app
        temp_mantarix_dir = Path.home().joinpath(
            ".mantarix", "bin", f"mantarix-{mantarix_desktop.version.version}"
        )

        # check if mantarix.exe is in MANTARIX_VIEW_PATH (mantarix developer mode)
        mantarix_path = os.environ.get("MANTARIX_VIEW_PATH")
        if mantarix_path:
            console.log(f"Mantarix.app is set via MANTARIX_VIEW_PATH: {mantarix_path}")
            temp_mantarix_dir = Path(mantarix_path)
        else:
            # check if mantarix_view.app exists in a temp directory
            if not temp_mantarix_dir.exists():
                # check if mantarix.tar.gz exists
                gz_filename = "mantarix-macos.tar.gz"
                tar_file = os.path.join(get_package_bin_dir(), gz_filename)
                if not os.path.exists(tar_file):
                    console.log(f"Platform is macOS!")
                    tar_file = __download_mantarix_client(gz_filename)

                console.log(f"Extracting Mantarix.app from archive to {temp_mantarix_dir}")
                temp_mantarix_dir.mkdir(parents=True, exist_ok=True)
                with tarfile.open(str(tar_file), "r:gz") as tar_arch:
                    safe_tar_extractall(tar_arch, str(temp_mantarix_dir))
                os.remove(tar_file)
            else:
                console.log(f"Mantarix View found in: {temp_mantarix_dir}")

        app_name = None
        for f in os.listdir(temp_mantarix_dir):
            if f.endswith(".app"):
                app_name = f
        assert app_name is not None, f"Application bundle not found in {temp_mantarix_dir}"
        app_path = temp_mantarix_dir.joinpath(app_name)
        args = ["open", str(app_path), "-n", "-W", "--args", page_url, pid_file]
    elif is_linux():
        # build version-specific path to mantarix folder
        temp_mantarix_dir = Path.home().joinpath(
            ".mantarix", "bin", f"mantarix-{mantarix_desktop.version.version}"
        )

        app_path = None
        # check if mantarix.exe is in MANTARIX_VIEW_PATH (mantarix developer mode)
        mantarix_path = os.environ.get("MANTARIX_VIEW_PATH")
        if mantarix_path:
            console.log(f"Mantarix View is set via MANTARIX_VIEW_PATH: {mantarix_path}")
            temp_mantarix_dir = Path(mantarix_path)
            app_path = temp_mantarix_dir.joinpath("mantarix")
        else:
            # check if mantarix_view.app exists in a temp directory
            if not temp_mantarix_dir.exists():
                # check if mantarix.tar.gz exists
                gz_filename = f"mantarix-linux-{get_arch()}.tar.gz"
                tar_file = os.path.join(get_package_bin_dir(), gz_filename)
                if not os.path.exists(tar_file):
                    console.log(f"Platform is Linux!")
                    tar_file = __download_mantarix_client(gz_filename)

                console.log(f"Extracting Mantarix from archive to {temp_mantarix_dir}")
                temp_mantarix_dir.mkdir(parents=True, exist_ok=True)
                with tarfile.open(str(tar_file), "r:gz") as tar_arch:
                    safe_tar_extractall(tar_arch, str(temp_mantarix_dir))
                os.remove(tar_file)
            else:
                console.log(f"Mantarix View found in: {temp_mantarix_dir}")

            app_path = temp_mantarix_dir.joinpath("mantarix", "mantarix")
        args = [str(app_path), page_url, pid_file]

    mantarix_env = {**os.environ}

    if assets_dir:
        args.append(assets_dir)

    if hidden:
        mantarix_env["MANTARIX_HIDE_WINDOW_ON_START"] = "true"
    
    console.log(f"Running View app:\n\tArgs: {args}\n\tEnv: {mantarix_env}\n\tPid File: {pid_file}")
    
    return args, mantarix_env, pid_file

def __download_mantarix_client(file_name):
    ver = mantarix_desktop.version.version
    temp_arch = Path(tempfile.gettempdir()).joinpath(file_name)
    console.log(f"Downloading Mantarix v{ver} to {temp_arch}")
    mantarix_url = f"https://github.com/mantarix-dev/mantarix-client/releases/download/v{ver}/{file_name}"
    urllib.request.urlretrieve(mantarix_url, temp_arch)
    return str(temp_arch)
