import os
import customtkinter as ctk


class AppWindow:
    def __init__(self, nam, ucchota, prostho, theme, color, icon):
        self.janala = ctk.CTk()
        self.janala.title(nam)

        # Calculate the center position of the window
        screen_prostho = self.janala.winfo_screenwidth()
        screen_ucchota = self.janala.winfo_screenheight()
        x = (screen_prostho // 2) - (prostho // 2)
        y = (screen_ucchota // 2) - (ucchota // 2)
        self.janala.geometry(f"{prostho}x{ucchota}+{x}+{y}")

        # Set theme and color locally
        self.theme = theme if theme else "system"
        self.color = color if color else "green"
        ctk.set_appearance_mode(self.theme)
        ctk.set_default_color_theme(self.color)

        # Set icon
        if icon:
            if not isinstance(icon, str):
                raise TypeError("Icon should be a string path to the icon file.")
            icon = icon.strip()
            if not icon.endswith('.ico'):
                raise ValueError("Icon file must be in .ico format.")
            if not os.path.isfile(icon):
                raise FileNotFoundError(f"Icon file not found: {icon}")
            try:
                self.janala.iconbitmap(icon)
            except Exception as e:
                raise RuntimeError(f"Failed to set icon: {e}")

    def notun_button_jukto_koro(self, button):
        """Add a button to the window."""
        if not isinstance(button, ctk.CTkButton):
            raise TypeError("Only CTkButton instances can be added.")
        button.pack(pady=10)

    def run(self):
        """Start the main event loop."""
        self.janala.mainloop()


def window_banao(nam, ucchota, prostho, theme, color, icon):
    """Create and return an AppWindow instance."""
    return AppWindow(nam, ucchota, prostho, theme, color, icon)


def button_banao(master, text, command=None):
    """Create and return a CTkButton."""
    if not isinstance(text, str):
        raise TypeError("Text should be a string.")
    if command and not callable(command):
        raise TypeError("Command should be a callable function.")
    return ctk.CTkButton(master=master, text=text, command=command)
