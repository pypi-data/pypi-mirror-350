# imports start
from setuptools import setup, find_packages  # type: ignore
import os
# imports end

# Metadata about the package
VERSION = '1.0.5'
DESCRIPTION = 'Simple python library to write programs in bangla language'

# Read the content of README.md
with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as readme_file:
    LONG_DESCRIPTION = readme_file.read()

setup(
    name="PytBangla",
    version=VERSION,
    author="Mohammad Mahfuz Rahman",
    author_email="mahfuzrahman0712@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'speechrecognition', 'pyttsx3', 'pyaudio', 'pyautogui', 'pywhatkit',
        'wikipedia', 'pyjokes', 'secure-smtplib', 'customtkinter', 'pandas',
        'requests', 'beautifulsoup4', 'opencv-python', 'numpy', 'pillow',
    ],
    keywords=[
        'speech recognition', 'text to speech', 'take command','command taker', 'python in bangla', 'programming','Python Organization',
        'Django','Flask', 'tkinter',  'python', 'web development','app development', 'django developer', 'python bangladesh community',
        "what is Python", 'What is coding', 'What is programming','PytBangla',
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ],
)
