"""Development Mode (a.k.a. “Editable Installs”)
$ cd your-python-project
$ python -m venv .venv
# Activate your environment with:
#      `source .venv/bin/activate` on Unix/macOS
# or   `.venv\\Scripts\\activate` on Windows

$ pip install --editable .

# Now you have access to your package
# as if it was installed in .venv
$ python -c "import your_python_project"
"""

import setuptools

with open("requirements.txt", "r", encoding="utf-8") as f:
    required = f.read().splitlines()


setuptools.setup(
    name="fabric-analytics-engine",
    packages=setuptools.find_packages(),
    install_requires=required,
)
