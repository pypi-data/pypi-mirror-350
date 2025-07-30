
import subprocess
from pathlib import Path
from typing import Dict, Optional, Any
import os
import sys

#
# async def pip_install_requirements(
#     directory: Optional[str] = None,
#     requirements_file: str = "requirements.txt",
#     stream_output: bool = True,
# ) -> dict[str, Any]:
#     """
#     Installs dependencies from a requirements.txt file.
#
#     Args:
#         requirements_file: The requirements.txt to use for installation.
#         directory: The directory the requirements.txt file is in. Defaults to
#             the current working directory.
#         stream_output: Whether to stream the output from pip install should be
#             streamed to the console
#
#     Returns:
#         A dictionary with the keys `stdout` and `stderr` containing the output
#             the `pip install` command
#
#     Raises:
#         subprocess.CalledProcessError: if the pip install command fails for any reason
#
#     Example:
#         ```yaml
#         pull:
#             - prefect.deployments.steps.git_clone:
#                 id: clone-step
#                 repository: https://github.com/org/repo.git
#             - prefect.deployments.steps.pip_install_requirements:
#                 directory: {{ clone-step.directory }}
#                 requirements_file: requirements.txt
#                 stream_output: False
#         ```
#     """
#     stdout_sink = io.StringIO()
#     stderr_sink = io.StringIO()
#
#     async with open_process(
#         [get_sys_executable(), "-m", "pip", "install", "-r", requirements_file],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         cwd=directory,
#     ) as process:
#         await _stream_capture_process_output(
#             process,
#             stdout_sink=stdout_sink,
#             stderr_sink=stderr_sink,
#             stream_output=stream_output,
#         )
#         await process.wait()
#
#         if process.returncode != 0:
#             raise RuntimeError(
#                 f"pip_install_requirements failed with error code {process.returncode}:"
#                 f" {stderr_sink.getvalue()}"
#             )
#
#     return {
#         "stdout": stdout_sink.getvalue().strip(),
#         "stderr": stderr_sink.getvalue().strip(),
#     }

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

def _clean_cache( stream_output: bool = True):
    try:
        subprocess.run(
            ["uv", "cache", "clean"],
            check=True,
            capture_output=not stream_output,
        )
    except subprocess.CalledProcessError as e:
        print(f"Failed to clean uv cache: {e.stderr.decode().strip()}")

async def uv_install(
    directory: Optional[str] = None,
    sub_directory: Optional[str] = None,
    venv_name: str = ".venv",
    min_python_version: str = "3.12",
    uv_base_command: str = "uv pip install ./",
    uv_extra_args: Optional[str] = None,  # e.g. "--strict"
    stream_output: bool = True,
    uv_clean_cache: bool = False,
) -> Dict[str, str]:
    """
    Install dependencies using uv in a virtual environment
    """
    # assert VENV_NAME is  venv_dir
    current_venv_name = os.environ.get("VENV_NAME", "")
    if current_venv_name != venv_name:
        raise ValueError(
            f"Current VENV_NAME is {current_venv_name}, but expected {venv_name}. "
        )
    major = int(min_python_version.split(".")[0])
    minor = int(min_python_version.split(".")[1])
    current_version = sys.version_info.major, sys.version_info.minor
    # check if the python version is at least major.minor
    if current_version < (major, minor):
        raise ValueError(
            f"Current Python version {sys.version} is lower than the required "
            f"version {min_python_version}."
        )

    # print python path and version
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    # print all args and kwargs
    print("locals: ", locals())

    # print environment variables
    print("Environment variables:")
    for key, value in sorted(os.environ.items()):
        print(f"{key}: {value}")

    if directory is None:
        directory = Path.cwd()
    if not isinstance(directory, Path):
        directory = Path(directory)

    if sub_directory:
        directory = directory / sub_directory

    print(f"directory: {directory}")
    if not directory.exists():
        raise FileNotFoundError(f"Directory {directory} does not exist.")
    # venv_path = directory / venv_dir

    # Create virtual environment
    # subprocess.run(
    #     ["uv", "venv", "--python", python_version, str(venv_path)],
    #     check=True,
    #     cwd=directory,
    #     capture_output=not stream_output
    # )
    if uv_clean_cache:
        _clean_cache(stream_output=stream_output)
    # Install dependencies
    install_cmd: list[str] = uv_base_command.split()
    # install_cmd += [ "--python",  str(venv_path / "bin" / "python") ]
    
    if uv_extra_args:
        install_cmd.extend(uv_extra_args.split())

    print("install_cmd: ", install_cmd)
    subprocess.run(
        install_cmd,
        check=True,
        cwd=directory,
        capture_output=not stream_output,
    )

    # return_dict = dict(virtual_env=str(venv_path), path=f"{venv_path / 'bin'}:{Path.cwd() / venv_path / 'bin'}:{os.environ.get('PATH', '')}")
    # print(f"return_dict: {return_dict}")
    return {}
