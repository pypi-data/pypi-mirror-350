from setuptools import setup, find_packages  # type: ignore
import os

VERSION = '1.0.3'
DESCRIPTION = 'Simple python library to write programms in bangla language'

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
        'wikipedia', 'pyjokes', 'secure-smtplib',
    ],
    keywords=[
        'speech recognition', 'text to speech', 'take command',
        'A.I system', 'A.i Assistant', 'personal assistant',
        'mahfuz rahman', 'how to make personal assistant using python',
        'python personal assistant', 'CommandTaker',
        'Command Taker', 'command taker', 'python in bangla', 'programming',
        'Computer Science & Engineering', 'Python Organization', 'Django',
        'Flask', 'tkinter', 'java', 'python', 'kotlin', 'web development',
        'app development', 'django developer', 'python bangladesh community',
        "what is Python", 'What is coding', 'What is programming',
        'what is computer', 'what is computer science', 'Mango', 'grape',
        'PytBangla', 'python in bangla'
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ],
)
