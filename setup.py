import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "midea_inventor_lib",
    version="1.0.4",
    author="Andrea Barbaresi",
    author_email="barban.mobile@google.com",
    description="Client-side Python library for EVA II PRO WiFi Smart Dehumidifier appliance by Midea/Inventor.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/barban-dev/midea_inventor_dehumidifier",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    install_requires=[
        "requests>=2.16.0",
        "pycryptodome>=3.6.6"
    ]
)
