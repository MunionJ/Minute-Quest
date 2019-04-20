import pygame
import mutagen.mp3


class Audio:
    def __init__(self, song=None):
        self.music = pygame.mixer.music
        self.sample_rate = 44100
        self.song = ''
        self.volume = 0.25
        self.load_music(song)

    def play_music(self, loops=0):
        self.music.play(loops)

    def stop_music(self):
        self.music.stop()

    def load_music(self, song):
        if song is None:
            return
        mp3_file = mutagen.mp3.MP3(song)
        freq = mp3_file.info.sample_rate
        if self.sample_rate != freq:
            self.sample_rate = freq
            pygame.mixer.quit()
            pygame.mixer.init(self.sample_rate)
        self.music.load(song)
        self.music.set_volume(self.volume)
