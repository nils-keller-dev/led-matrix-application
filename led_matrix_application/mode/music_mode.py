import os
import time
from urllib.request import urlopen

import spotipy
from mode.abstract_mode import AbstractMode
from PIL import Image
from RGBMatrixEmulator import graphics
from spotipy.oauth2 import SpotifyOAuth

IMAGE_SIZE = 50, 50
COLOR_WHITE = graphics.Color(255, 255, 255)
TEXT_SPEED = 20


class MusicMode(AbstractMode):
    def __init__(self, matrix):
        super().__init__(matrix)
        self.logo = Image.open("icons/spotify.png")
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
        self.last_frame_time = time.time()
        self.frame = 0
        self.one_char_width = self.font.CharacterWidth(0x0020)

    def start(self):
        self.matrix.Clear()
        self.update_song_data()

    def update_settings(self, _):
        pass

    def update_display(self):
        if self.song_data is None:
            self.matrix.SetImage(self.logo, 20, 20, False)
            return

        self.offscreen_canvas.Clear()

        current_time = time.time()
        time_delta = current_time - self.last_frame_time
        self.last_frame_time = current_time

        text_width = self.one_char_width * len(self.text)
        space_width = self.one_char_width * 4
        total_width = text_width + space_width

        if text_width > self.offscreen_canvas.width:
            self.frame = (self.frame + TEXT_SPEED * time_delta) % total_width

        offset_left = round(
            max((self.offscreen_canvas.width - text_width) // 2, 0) - self.frame
        )

        graphics.DrawText(
            self.offscreen_canvas,
            self.font,
            offset_left,
            61,
            COLOR_WHITE,
            self.text,
        )

        if total_width > self.offscreen_canvas.width and text_width > 64:
            graphics.DrawText(
                self.offscreen_canvas,
                self.font,
                offset_left + total_width,
                61,
                COLOR_WHITE,
                self.text,
            )

        self.offscreen_canvas.SetImage(self.image, 7, 2)

        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

    def update_song_data(self):
        new_song_data = self.spotipy.currently_playing()

        if new_song_data != self.song_data:
            self.song_data = new_song_data
            artist = self.song_data["item"]["artists"][0]["name"]
            song = self.song_data["item"]["name"]
            self.text = f"{artist} - {song}"
            image_url = self.song_data["item"]["album"]["images"][2]["url"]
            self.image = Image.open(urlopen(image_url)).resize(IMAGE_SIZE)
