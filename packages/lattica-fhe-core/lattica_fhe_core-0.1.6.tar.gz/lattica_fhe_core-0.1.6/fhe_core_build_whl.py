import platform
import os
from pathlib import Path
from setuptools import Extension
from setuptools.command.build_ext import build_ext as _build_ext

PACKAGE_NAME = "lattica_fhe_core"
MODULE_FILENAME_BASE = "cpp_sdk" 

class NoOpBuildExt(_build_ext):
    def run(self):
        print(f"DEBUG NoOpBuildExt: run() called on OS: {platform.system()}. Skipping compilation.")
        for ext in self.extensions:
            # Ensure output directory for extension exists
            # For editable installs, the .so is in the source tree.
            # For wheel builds, this helps setuptools.
            os.makedirs(os.path.dirname(self.get_ext_fullpath(ext.name)), exist_ok=True)
            
            package_source_dir = Path(PACKAGE_NAME)
            found_so_files = list(package_source_dir.glob(f"{MODULE_FILENAME_BASE}.cpython*-*.so"))
            if not found_so_files:
                print(f"WARNING NoOpBuildExt: Precompiled .so for {ext.name} not found in {package_source_dir} matching {MODULE_FILENAME_BASE}.cpython*-*.so")
            else:
                print(f"DEBUG NoOpBuildExt: Found precompiled .so for {ext.name}: {found_so_files[0]}")
        print(f"DEBUG NoOpBuildExt: run() finished for {len(self.extensions)} extensions.")

def build(setup_kwargs): # Function name 'build' is expected by Poetry's 'script' key
    current_os = platform.system()
    print(f"DEBUG lattice_fhe_core_build_hook.py: OS: {current_os}, Arch: {platform.machine()}")
    print(f"DEBUG lattice_fhe_core_build_hook.py: Initial setup_kwargs: {setup_kwargs}")

    extension_name = f"{PACKAGE_NAME}.{MODULE_FILENAME_BASE}"
    ext_modules = [ Extension(extension_name, sources=[]) ]

    setup_kwargs.update({
        "ext_modules": ext_modules,
        "cmdclass": {"build_ext": NoOpBuildExt},
        "zip_safe": False,
    })
    print(f"DEBUG lattice_fhe_core_build_hook.py: Updated setup_kwargs with ext_modules and cmdclass: {setup_kwargs}")