from setuptools import setup, find_packages # type: ignore


VERSION = '1.0.1'
DESCRIPTION = 'Simpler Python Package for Bangladeshi Beginners'
LONG_DESCRIPTION = 'This package was made with a thought of making python more easier for the new learners from ' \
                   'Bangladesh. Gradually this package will have all the fundamental functions that a programmer needs '
setup(
    name="PytBangla",
    version=VERSION,
    author="Mohammad Mahfuz Rahman",
    author_email="mahfuzrahman0712@gmail.com",
    author_phone="01540148390",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['speechrecognition', 'pyttsx3', 'pyaudio', 'pyautogui', 'pywhatkit', 'wikipedia', 'pyjokes', 'secure-smtplib',],
    keywords=['speech recognition', 'text to speech', 'take command',
              'A.I system', 'A.i Assistant', 'personal assistant',
              'mahfuz rahman', 'how to make personal assistant using python',
              'python personal assistant', 'CommandTaker',
              'Command Taker', 'command taker', 'python in bangla', 'programming', 'Computer Science & Engineering', 'Python Organization', 'Django', 'Flask', 'tkinter', 'java',
              'python',
              'kotlin', 'web development', 'app development', 'django developer', 'python bangladesh community', "what is Python", 'What is coding', 'What is programming', 'what is computer',
              'what is computer science','Mango', 'grape','PytBangla','python in bangla'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ],

)
