import os
import sys
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
import subprocess
import platform

import argparse
import json
import os
import shutil

from jupyter_client.kernelspec import KernelSpecManager
from tempfile import TemporaryDirectory

kernel_json = {
    "argv": [sys.executable, "-m", "wollok_kernel", "-f", "{connection_file}"],
    "display_name": "Wollok",
    "language": "wollok",
}

class CustomHook(BuildHookInterface):
    def initialize(self, version, build_data):
        here = os.path.abspath(os.path.dirname(__file__))
        sys.path.insert(0, here)
        prefix = os.path.join(here, 'data_kernelspec')

        if platform.system() != "Windows":
            self.find_and_install_npm_dependencies(start_dir=here)
        else:
            print("Skipping node dependencies installation on Windows")

        self.copy_polyfills()

        with TemporaryDirectory() as td:
            os.chmod(td, 0o755) # Starts off as 700, not user readable
            with open(os.path.join(td, 'kernel.json'), 'w') as f:
                json.dump(kernel_json, f, sort_keys=True)
            print('Installing Jupyter kernel spec')

            # Requires logo files in kernel root directory
            cur_path = os.path.dirname(os.path.realpath(__file__))
            for logo in ["logo-32x32.png", "logo-64x64.png"]:
                try:
                    shutil.copy(os.path.join(cur_path, logo), td)
                except FileNotFoundError:
                    print("Custom logo files not found. Default logos will be used.")

            KernelSpecManager().install_kernel_spec(td, 'wollok', user=False, prefix=prefix)


    def find_and_install_npm_dependencies(self, start_dir="."):
        """Find and install npm dependencies for every package.json files in subfolders"""
        print("Installing node dependencies")
        exclude_folders = {"node_modules", ".git", ".venv", "__pycache__"}
        subprocess.run(["pwd"])
        for root, folders, files in os.walk(start_dir):
            folders[:] = [folder for folder in folders if folder not in exclude_folders]
            if "package.json" in files:
                print(f"package.json found in: {root}")
                try:
                    subprocess.run(["npm", "install", "--verbose"], cwd=root, check=True)
                    print(f"✅ npm install completed in {root}\n")
                except subprocess.CalledProcessError as e:
                    print(f"❌ Error executing npm install in {root}: {e}\n")

    def copy_polyfills(self):
        """Copy polyfills to the node_modules directory"""
        here = os.path.join("wollok_kernel", "wollok_bridge")
        polyfills_dir = os.path.join(here, "polyfills")
        target_dir = os.path.join(here, "node_modules")

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        for subdir in os.listdir(polyfills_dir):
            dir_source_path = os.path.join(polyfills_dir, subdir)
            dir_target_path = os.path.join(target_dir, subdir)
            if os.path.exists(dir_target_path):
                shutil.rmtree(dir_target_path)
            shutil.copytree(dir_source_path, dir_target_path)
            print(f"Copied {subdir} to {target_dir}")