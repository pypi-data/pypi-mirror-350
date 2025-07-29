# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
__path__ = __import__('pkgutil').extend_path(__path__, __name__)

import os
import pkg_resources
import subprocess

MLFLOW_MODEL_PATH_REQUIREMENTS = os.path.join(
    os.getenv("AZUREML_MODEL_DIR", ""), "mlflow_model_folder/requirements.txt"
)


def get_installed_packages():
    """Return a set of installed package names with versions."""
    return {pkg.key: pkg.version for pkg in pkg_resources.working_set}


def install_missing_dependencies(requirements_file):
    """Install dependencies only if they are missing in the environment."""
    if not os.path.exists(requirements_file):
        print(f"Requirements file not found: {requirements_file}")
        return

    installed_packages = get_installed_packages()

    with open(requirements_file, "r") as f:
        for line in f:
            req = line.strip()
            if not req or req.startswith("#"):
                continue

            pkg_name = req.split("==")[0] if "==" in req else req

            if pkg_name in installed_packages:
                print(
                    f"{pkg_name} is already installed (Version: {installed_packages[pkg_name]})"
                )
            else:
                print(f"Installing missing package: {req}")
                try:
                    result = subprocess.run(
                        ["pip", "install", req],
                        check=False,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    if result.returncode == 0:
                        print(f"Successfully installed {req}")
                    else:
                        print(f"Failed to install {req}: {result.stderr}")
                except Exception as e:
                    print(f"Error installing {req}: {e}")


try:
    install_missing_dependencies(MLFLOW_MODEL_PATH_REQUIREMENTS)
except Exception as e:
    print(f"Dependency installation encountered an issue: {e}. Continuing execution...")
