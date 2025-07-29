

![Alt Text](images/logo.png)

**PytBangla** is a Python library that brings a touch of Bengali flavor to programming, offering tools for speech interaction, file management, calculations, and email automation using Bengali-named methods. It's designed to be friendly, intuitive, and culturally resonant for native Bangla speakers who love to code.

## Features 📌

### 🖥️ Computer Class
- `input_nao(prompt, data_type)`: Custom input method with data type support.
- `lekho(variable)`: Print to console.
- `bolo(text)`: Convert text to speech using `pyttsx3`.
- `shuno()`: Voice input using microphone.
- `suru_koro(app)`: Start an application.
- `bondho_koro(app)`: Force close an application.
- `screenshot_nao(path)`: Take a screenshot and save.
- `is_equal(a, b)`: Check if two values are equal and same type.

### 🧮 Calculator Class
- Area calculations: `rectangular_area`, `square_area`, `triangle_area`, `circular_area_diameter`, `circular_area_radius`
- Basic operations: `jog_koro`, `biyog_koro`, `gun_koro`, `vag_koro`, `vagsesh_ber_koro`, `ghat_ber_koro`
- Advanced math: `borgo_mul_koro`, `factorial`, `prime`, `palindrome`, `fibonacci`

### 📧 Mailer Class
- Initialize with credentials: `Mailer(username, password, host, port)`
- Send mail: `email_pathao(to, subject, compose)`

### 📂 FileManager Class
Full-featured file manager:
- Create, read, delete, rename, copy, move files
- Check file existence, size, extension, line/word/char count
- Search, replace, append content
- Manage directories

## Installation 📦

```bash
pip install pytbangla
```

> Note: `pyaudio` may need to be installed separately depending on your OS.

## Example Usage 🚀

```python
from pytbangla import Computer, Calculator, Mailer, FileManager

c = Computer()
c.lekho("Hello from PytBangla!")
c.bolo("Bhalo achi")

calc = Calculator()
print(calc.jog_koro(10, 20))  # 30

fm = FileManager()
fm.file_create("test.txt", "This is PytBangla")
```

## Contributing 🤝

Feel free to fork and contribute! Pull requests are warmly welcome.

## License 📝

MIT License - do what you want, just give credit.

---
Crafted with ❤️ for the Bangla coding community.
