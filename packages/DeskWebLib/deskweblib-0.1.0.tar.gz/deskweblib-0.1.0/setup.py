from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="DeskWebLib",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "robotframework",
        "selenium",
        "pyautogui",
        "pillow",
        "opencv-python",
        "numpy",
    ],
    long_description=long_description,
    url="https://github.com/Reshma1410/deskweblib/tree/master",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Robot Framework",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

    long_description_content_type="text/markdown",  # Important!
    description="Hybrid Robot Framework library for web and desktop automation",
    author="Reshma Banu",
    license="MIT",
)
