
import subprocess
from pathlib import Path
from typing import Dict, Optional
import os


# pull:
#   - prefect.deployments.steps.git_clone:
#       id: clone-step
#       repository: https://git.vito.be/scm/tes/cams-ncp_flow_process.git
#       branch: main
#
#   - vito.sas_prefect.uv_install:
#       directory: "{{ clone-step.directory }}"
#       python_version: "3.12"
#       uv_extra_args: "--strict"
#       stream_output: true

def uv_install(
    directory: str | Path,
    python_version: str = "3.12",
    venv_dir: str = ".venv",
    uv_extra_args: Optional[str] = None,  # e.g. "--strict"
    stream_output: bool = True,
) -> Dict[str, Dict[str, str]]:
    """
    Install dependencies using uv in a virtual environment
    """
    if not isinstance(directory, Path):
        directory = Path(directory)
    venv_path = directory / venv_dir
    
    # Create virtual environment
    subprocess.run(
        ["uv", "venv", "--python", python_version, str(venv_path)],
        check=True,
        cwd=directory,
        capture_output=not stream_output,
    )

    # Install dependencies
    install_cmd = [
        "uv", "pip", "install", "./", "--python",  str(venv_path / "bin" / "python")
    ]
    
    if uv_extra_args:
        install_cmd.extend(uv_extra_args.split())

    print("install_cmd: ", install_cmd)
    subprocess.run(
        install_cmd,
        check=True,
        cwd=directory,
        capture_output=not stream_output,
    )

    return {
        "env": {
            "VIRTUAL_ENV": str(venv_path),
            "PATH": f"{venv_path / 'bin'}:{Path.cwd() / venv_path / 'bin'}:{os.environ.get('PATH', '')}"
        }
    }