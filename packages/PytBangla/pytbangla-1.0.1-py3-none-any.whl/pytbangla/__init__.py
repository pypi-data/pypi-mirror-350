# import starts here
import speech_recognition as sr
import pyttsx3
import os
import pyautogui
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import re
# import ends here

class Computer:
    def input_nao(self, input_variable, data_type=None):
        if data_type is None:
            if input_variable == '':
                raise ValueError("input_nao function er parameter e empty string pass kora jabe na")
            if isinstance(input_variable, str):
                return input(f'{input_variable}')
            elif isinstance(input_variable, int):
                return int(input(f'{input_variable}'))
            elif isinstance(input_variable, float):
                return float(input(f'{input_variable}'))
        else:
            if data_type == 'str':
                return str(input(f'{input_variable}'))
            elif data_type == 'int':
                return int(input(f'{input_variable}'))
            elif data_type == 'float':
                return float(input(f'{input_variable}'))
        return input(f'{input_variable}')

    def lekho(self, variable):
        print(f'{variable}')

    def bolo(self, audio):
        if isinstance(audio, (int, float)):
            audio = str(audio)
        elif not isinstance(audio, str):
            raise TypeError("bolo function e sudhu string data pass kora jabe")
        if audio == '':
            raise ValueError("bolo function er parameter e empty string pass kora jabe na")
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voices', voices[0].id)
        engine.say(audio)
        engine.runAndWait()

    def shuno(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening....")
            r.pause_threshold = 1
            audio = r.listen(source, timeout=2, phrase_time_limit=5)
        try:
            print("Recognising....")
            query = r.recognize_google(audio, language='en-in')
            print(f"Apni bolechen:\n {query}")
        except Exception:
            return 'none'
        return query

    def suru_koro(self, app):
        os.startfile(app)

    def bondho_koro(self, app):
        os.system("taskkill /f /im " + app + ".exe")

    def screenshot_nao(self, path):
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        
    def is_equal(self, a, b):
        if type(a) is type(b):
            return "yes" if a == b else "no"
        return False
class Calculator:
    def rectangular_area(self, l, w):
        return l * w

    def square_area(self, a):
        return a * a

    def triangle_area(self, l, h):
        return 0.5 * l * h

    def circular_area_diameter(self, d):
        r = 0.5 * d
        return 3.1416 * r * r

    def circular_area_radius(self, r):
        return 3.1416 * r * r

    def jog_koro(self, x, y):
        return x + y

    def biyog_koro(self, x, y):
        return x - y

    def gun_koro(self, x, y):
        return x * y

    def vag_koro(self, x, y):
        if y == 0:
            raise ValueError("Division by zero is not allowed")
        return x / y

    def vagsesh_ber_koro(self, x, y):
        if y == 0:
            raise ValueError("Division by zero is not allowed")
        return x % y

    def ghat_ber_koro(self, x, y):
        return x ** y

    def borgo_mul_koro(self, x):
        if x < 0:
            raise ValueError("Square root of negative number is not allowed")
        return x ** 0.5

    def factorial(self, x):
        if x < 0:
            raise ValueError("Factorial of negative number is not allowed")
        if x == 0 or x == 1:
            return 1
        result = 1
        for i in range(2, x + 1):
            result *= i
        return result

    def prime(self, n):
        if n <= 1:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    def palindrome(self, string):
        string = string.lower()
        string = re.sub(r'[^a-z0-9]', '', string)
        return string == string[::-1]

    def fibonacci(self, n):
        if n <= 0:
            return []
        elif n == 1:
            return [0]
        elif n == 2:
            return [0, 1]
        fib = [0, 1]
        for i in range(2, n):
            fib.append(fib[i - 1] + fib[i - 2])
        return fib
class Mailer:
    def __init__(self, UserName, Password, Host, Port):
        self.From = UserName
        self.Password = Password
        self.Host = Host
        self.Port = Port
    def email_pathao(self, To, Subject, Compose):
        msg = MIMEMultipart()
        msg['From'] = self.From
        msg['To'] = To
        msg['Subject'] = Subject
        body = MIMEText(Compose)
        msg.attach(body)
        s = smtplib.SMTP(self.Host, self.Port)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(self.From, self.Password)
        s.sendmail(self.From, To, msg.as_string())
        s.quit()
class FileManager:
    def file_create(self, file_name, content):
        with open(file_name, 'w') as file:
            file.write(content)
    def file_read(self, file_name):
        with open(file_name, 'r') as file:
            content = file.read()
        return content
    def file_delete(self, file_name):
        if os.path.exists(file_name):
            os.remove(file_name)
        else:
            raise FileNotFoundError(f"{file_name} does not exist")
    def file_rename(self, old_name, new_name):
        if os.path.exists(old_name):
            os.rename(old_name, new_name)
        else:
            raise FileNotFoundError(f"{old_name} does not exist")
    def file_copy(self, source, destination):
        if os.path.exists(source):
            with open(source, 'rb') as src_file:
                with open(destination, 'wb') as dest_file:
                    dest_file.write(src_file.read())
        else:
            raise FileNotFoundError(f"{source} does not exist")
    def file_move(self, source, destination):
        if os.path.exists(source):
            os.rename(source, destination)
        else:
            raise FileNotFoundError(f"{source} does not exist")
    def file_exists(self, file_name):
        return os.path.exists(file_name)
    def file_size(self, file_name):
        if os.path.exists(file_name):
            return os.path.getsize(file_name)
        else:
            raise FileNotFoundError(f"{file_name} does not exist")
    def file_extension(self, file_name):
        if os.path.exists(file_name):
            return os.path.splitext(file_name)[1]
        else:
            raise FileNotFoundError(f"{file_name} does not exist")
    def file_lines(self, file_name):
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                lines = file.readlines()
            return len(lines)
        else:
            raise FileNotFoundError(f"{file_name} does not exist")
    def file_word_count(self, file_name):
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                content = file.read()
            words = content.split()
            return len(words)
        else:
            raise FileNotFoundError(f"{file_name} does not exist")
    def file_character_count(self, file_name):
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                content = file.read()
            return len(content)
        else:
            raise FileNotFoundError(f"{file_name} does not exist")
    def file_search(self, file_name, search_term):
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                content = file.read()
            return search_term in content
        else:
            raise FileNotFoundError(f"{file_name} does not exist")
    def file_replace(self, file_name, old_string, new_string):
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                content = file.read()
            content = content.replace(old_string, new_string)
            with open(file_name, 'w') as file:
                file.write(content)
        else:
            raise FileNotFoundError(f"{file_name} does not exist")
    def file_append(self, file_name, content):
        if os.path.exists(file_name):
            with open(file_name, 'a') as file:
                file.write(content)
        else:
            raise FileNotFoundError(f"{file_name} does not exist")
    def file_create_directory(self, directory_name):
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
        else:
            raise FileExistsError(f"{directory_name} already exists")
    def file_delete_directory(self, directory_name):
        if os.path.exists(directory_name):
            os.rmdir(directory_name)
        else:
            raise FileNotFoundError(f"{directory_name} does not exist")
    def file_list_directory(self, directory_name):
        if os.path.exists(directory_name):
            return os.listdir(directory_name)
        else:
            raise FileNotFoundError(f"{directory_name} does not exist")
    def file_change_directory(self, directory_name):
        if os.path.exists(directory_name):
            os.chdir(directory_name)
        else:
            raise FileNotFoundError(f"{directory_name} does not exist")
    def file_current_directory(self):
        return os.getcwd()
    def file_copy_directory(self, source, destination):
        if os.path.exists(source):
            if not os.path.exists(destination):
                os.makedirs(destination)
            for item in os.listdir(source):
                s = os.path.join(source, item)
                d = os.path.join(destination, item)
                if os.path.isdir(s):
                    self.file_copy_directory(s, d)
                else:
                    self.file_copy(s, d)
        else:
            raise FileNotFoundError(f"{source} does not exist")
    def file_move_directory(self, source, destination):
        if os.path.exists(source):
            if not os.path.exists(destination):
                os.makedirs(destination)
            for item in os.listdir(source):
                s = os.path.join(source, item)
                d = os.path.join(destination, item)
                if os.path.isdir(s):
                    self.file_move_directory(s, d)
                else:
                    self.file_move(s, d)
            os.rmdir(source)
        else:
            raise FileNotFoundError(f"{source} does not exist")
    def file_rename_directory(self, old_name, new_name):
        if os.path.exists(old_name):
            os.rename(old_name, new_name)
        else:
            raise FileNotFoundError(f"{old_name} does not exist")
    def file_exists_directory(self, directory_name):
        return os.path.exists(directory_name)
    def file_size_directory(self, directory_name):
        if os.path.exists(directory_name):
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(directory_name):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
            return total_size
        else:
            raise FileNotFoundError(f"{directory_name} does not exist")
