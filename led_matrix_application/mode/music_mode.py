import os
import threading
import time
from urllib.request import urlopen

import spotipy
from mode.abstract_mode import AbstractMode
from PIL import Image
from spotipy.oauth2 import SpotifyOAuth
from utils import get_rgb_matrix

graphics = get_rgb_matrix().get("graphics")


IMAGE_SIZE = 50, 50
IMAGE_SIZE_FULLSCREEN = 64, 64
COLOR_WHITE = graphics.Color(255, 255, 255)
TEXT_SPEED = 20


class MusicMode(AbstractMode):
    def __init__(self, matrix):
        super().__init__(matrix)
        self.logo = Image.open("icons/spotify.png").convert("RGB")
        self.font = graphics.Font()
        self.font.LoadFont("fonts/tamzen/1.bdf")

        self.offscreen_canvas = matrix.CreateFrameCanvas()

        scope = "user-read-currently-playing"
        username = os.getenv("SPOTIFY_USER")
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
        auth_manager = SpotifyOAuth(
            scope=scope,
            username=username,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
        )
        self.spotipy = spotipy.Spotify(auth_manager=auth_manager)

        self.song_data = None
        self.text = None
        self.image = None
        self.image_fullscreen = None
        self.last_frame_time = time.time()
        self.frame = 0
        self.one_char_width = self.font.CharacterWidth(0x0020)
        self.text_width = 0
        self.space_width = self.one_char_width * 4
        self.total_width = 0
        self.offset_left = 0
        self.song_data_thread = None
        self.is_mode_active = False
        self.lock = threading.Lock()

    def start(self):
        self.offscreen_canvas.Clear()
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
        self.update_song_data()
        self.is_mode_active = True

        self.song_data_thread = threading.Thread(target=self.update_song_data_loop)
        self.song_data_thread.start()

    def stop(self):
        self.is_mode_active = False
        self.song_data_thread.join()

    def update_settings(self, settings):
        with self.lock:
            if self.song_data is None:
                self.settings = settings
                return

            if self.song_data["currently_playing_type"] == "track":
                image_url = self.song_data["item"]["album"]["images"][2]["url"]
            else:
                image_url = self.song_data["item"]["images"][2]["url"]
            if settings["fullscreen"]:
                self.settings = settings
                if self.image_fullscreen is None:
                    self.image_fullscreen = self.process_image(
                        image_url, IMAGE_SIZE_FULLSCREEN
                    )
                self.display_fullscreen_image()
            else:
                if self.image is None:
                    self.image = self.process_image(image_url, IMAGE_SIZE)
                self.last_frame_time = time.time()
                self.settings = settings

    def update_display(self):
        with self.lock:
            if self.song_data is None or (
                self.image is None and self.image_fullscreen is None
            ):
                self.offscreen_canvas.Clear()
                self.offscreen_canvas.SetImage(self.logo, 20, 20, False)
                self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
                return

            if self.settings["fullscreen"]:
                return

            self.offscreen_canvas.Clear()

            graphics.DrawText(
                self.offscreen_canvas,
                self.font,
                self.offset_left,
                61,
                COLOR_WHITE,
                self.text,
            )

            if self.text_width > self.offscreen_canvas.width:
                graphics.DrawText(
                    self.offscreen_canvas,
                    self.font,
                    self.offset_left + self.total_width,
                    61,
                    COLOR_WHITE,
                    self.text,
                )

            self.offscreen_canvas.SetImage(self.image, 7, 2, False)

            current_time = time.time()
            time_delta = current_time - self.last_frame_time
            self.last_frame_time = current_time

            if self.text_width > self.offscreen_canvas.width:
                self.frame = (self.frame + TEXT_SPEED * time_delta) % self.total_width
                self.offset_left = round(
                    max((self.offscreen_canvas.width - self.text_width) // 2, 0)
                    - self.frame
                )

            self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

    def update_song_data(self):
        try:
            new_song_data = self.spotipy.currently_playing(additional_types=["episode"])
        except Exception as e:
            print(f"Error in update_song_data: {e}")
            return

        if new_song_data is not None and (
            self.song_data is None
            or new_song_data["item"]["id"] != self.song_data["item"]["id"]
        ):
            self.song_data = new_song_data
            if self.song_data["currently_playing_type"] == "track":
                artist = self.song_data["item"]["artists"][0]["name"]
                song = self.song_data["item"]["name"]
                image_url = self.song_data["item"]["album"]["images"][2]["url"]
            else:
                artist = self.song_data["item"]["show"]["publisher"]
                song = f"{self.song_data['item']['show']['name']} - {self.song_data['item']['name']}"
                image_url = self.song_data["item"]["images"][2]["url"]

            self.text = f"{artist} - {song}"

            self.frame = 0
            self.text_width = self.one_char_width * len(self.text)
            self.total_width = self.text_width + self.space_width
            self.offset_left = round(max((self.matrix.width - self.text_width) // 2, 0))

            if self.settings and self.settings["fullscreen"]:
                self.image_fullscreen = self.process_image(
                    image_url, IMAGE_SIZE_FULLSCREEN
                )
                self.image = None
                self.display_fullscreen_image()
            else:
                self.image = self.process_image(image_url, IMAGE_SIZE)
                self.image_fullscreen = None

    def process_image(self, url, size):
        try:
            return Image.open(urlopen(url)).resize(size).convert("RGB")
        except Exception as e:
            print(f"Error in process_image: {e}")

    def display_fullscreen_image(self):
        self.offscreen_canvas.SetImage(self.image_fullscreen, 0, 0, False)
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

    def update_song_data_loop(self):
        while self.is_mode_active:
            self.update_song_data()
            time.sleep(1)
