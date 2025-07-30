# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lattica_fhe_core']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lattica-fhe-core',
    'version': '0.1.6',
    'description': 'Lattica FHE Core Python Bindings',
    'long_description': '# Lattica FHE Core\n\nThis repository contains the source code for the **Lattica Client FHE SDK**, which powers encrypted inference for AI workloads using Fully Homomorphic Encryption (FHE). The SDK provides a portable FHE implementation that compiles into a shared library used both by the Lattica Python and JS clients.\n\n---\n\n## 🛠️ Build Instructions\n\n### Requirements\n\n#### Linux x86_64 or macOS ARM-64\n\n- C++17-compatible compiler (e.g. `g++ ≥ 9`)\n- CMake ≥ 3.14\n- Python ≥ 3.8\n- `pybind11`\n- `torch == 2.5.1`\n- `setuptools`, `wheel` (for Python packaging)\n\n##### macOS only:\n\n- autoconf, automake\n\n### Build Steps\n\n```bash\ngit clone https://github.com/Lattica-ai/lattica_fhe_core.git\ncd lattica_fhe_core\n\n# Create and activate a virtual environment (recommended)\npython -m venv .venv\nsource .venv/bin/activate\n\n# Install required Python packages\npip install pybind11 torch==2.5.1 setuptools wheel\n\n# Build the project\ncmake . -B build -DPYTHON_ENABLED=ON\ncmake --build build --parallel 32\n```\n\nThis will generate a Python extension shared library named like:\n\n```\n# On Linux:\ncpp_sdk.cpython-312-x86_64-linux-gnu.so\n\n# On macOS:\ncpp_sdk.cpython-312-darwin.so\n```\n\n---\n\n## ▶️ Using This Build in the Lattica Client\n\nTo replace the binary distributed by `lattica-query`:\n\n1. Install the query client as described here:  \n   👉 https://platformdocs.lattica.ai/how-to-guides/client-installation/how-to-install-query-client\n\n2. Locate the installed `.so` file by running:\n\n```bash\npip show -f lattica-fhe-core\n```\n\n3. Replace the installed `cpp_sdk.*.so` file with the one you built.\n\n---\n\n## 📁 Project Structure\n\nA detailed breakdown of the major components in this repository:\n\n---\n\n### `src/encryption_schemes/`\n\nImplements the supported encryption schemes used by the Lattica client.\n\n- Includes `ckks`, `rbgv`, and two GSW-like variants (`*_g`, `*_g_crt`) based on gadget matrix decompositions.\n- Each scheme provides:\n  - Encoding and decoding of plaintext data\n  - Encryption and decryption procedures\n  - Key generation, including auxiliary key-switching keys\n- All cryptographic randomness is generated via **Libsodium**\n\n---\n\n### `src/context_utils/`\n\nProvides utilities for interpreting and validating encryption context parameters.\n\n- Parameters are received from the backend per model — they are not generated locally.\n- Includes logic for:\n  - Representing data in **double-CRT form**\n  - Managing modulus chains and per-prime decompositions\n  - Ensuring structural compatibility of runtime contexts\n\n---\n\n### `src/homomorphic_operations/`\n\nImplements **apply-clear** versions of homomorphic operations.\n\n- These simulate encrypted computation by applying the logic directly to plaintext inputs.\n- Used only for client-side validation and debugging — no encrypted computation is performed here.\n- Actual homomorphic execution is handled remotely by the Lattica backend.\n\n---\n\n### `src/binding/python/`\n\nDefines the Python interface via `pybind11`.\n\n- These four functions are exposed:\n  1. `py_generate_key(...)`\n  2. `py_enc(...)`\n  3. `py_dec(...)`\n  4. `py_apply_client_block(...)`\n\n---\n\n### `src/encryption_scheme_utils/`\n\nImplements abstractions for representing and manipulating the structure of plaintext data.\n\n- Defines the `pt_shape` object, which describes logical dimensions, padding, and layout\n\n---\n\n### `src/tensor_engine/`\n\nImplements the core arithmetic and layout handling logic for encrypted and plaintext data.\n\n- All data — including ciphertexts, plaintexts, and context elements — is represented as **tensors**\n- Built on **PyTorch tensor operations**, with select extensions for FHE-specific requirements\n- Includes custom kernels for modular arithmetic routines: addition, multiplication, NTT, inverse NTT\n\n---\n\n### `src/serialization/`\n\nHandles serialization and deserialization of all major objects.\n\n- Implemented using **Protocol Buffers (protobuf)**\n- Supports efficient encoding of ciphertexts, plaintexts, keys, and context objects\n\n---\n\n### `src/slot_permutation/`\n\nImplements **coefficient permutations**, supports both:\n\n- Permutations in the **coefficient basis**\n- Permutations in the **CRT basis**\n\n---\n\n### `src/` (top-level)\n\n- `num.cpp`: Implements **multi-precision integer arithmetic**\n- `toolkit_python.cpp`: Entry point for the Python integration layer\n\n---\n\n## 🔐 License\n\nSee [LICENSE.txt](./LICENSE.txt) for license details.\n\nFor support, please contact the Lattica team or consult internal documentation.\n',
    'author': 'LatticaAI',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}
from fhe_core_build_whl import *
build(setup_kwargs)

setup(**setup_kwargs)
