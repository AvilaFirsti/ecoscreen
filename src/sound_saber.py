"""
Sound Saber - Cursor Sonoro do EcoScreen
Versão inicial simples (sem binaural)
"""

import time
import numpy as np
import sounddevice as sd
from pynput import mouse
import pyttsx3

class SoundSaber:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 180)      # Velocidade da voz
        self.is_active = False
        self.last_position = (0, 0)
        
        print("🔊 Sound Saber inicializado! Pressione Ctrl+C para parar.")

    def speak(self, text):
        """Fala algo usando voz sintetizada"""
        self.engine.say(text)
        self.engine.runAndWait()

    def play_cursor_sound(self, x, y, screen_width=1920, screen_height=1080):
        """Gera som conforme a posição do mouse (panning + pitch)"""
        # Normaliza posição (0.0 a 1.0)
        norm_x = x / screen_width
        norm_y = y / screen_height
        
        # Panning (esquerda/direita)
        pan = norm_x * 2 - 1  # de -1 (esquerda) até +1 (direita)
        
        # Pitch (grave embaixo, agudo em cima)
        pitch = 800 + (norm_y * 600)  # varia entre 800Hz e 1400Hz
        
        # Gera um tom curto
        duration = 0.08  # segundos
        frequency = pitch
        t = np.linspace(0, duration, int(44100 * duration), False)
        tone = 0.3 * np.sin(frequency * t * 2 * np.pi)
        
        # Aplica panning
        left = tone * (1 - max(0, pan))
        right = tone * (1 + min(0, pan))
        stereo = np.column_stack((left, right))
        
        sd.play(stereo, samplerate=44100)
        sd.wait()

    def on_move(self, x, y):
        """Chamado toda vez que o mouse se move"""
        if not self.is_active:
            return
            
        # Evita tocar som muito rápido (throttle)
        if abs(x - self.last_position[0]) > 15 or abs(y - self.last_position[1]) > 15:
            self.play_cursor_sound(x, y)
            self.last_position = (x, y)

    def start(self):
        """Inicia o Sound Saber"""
        self.is_active = True
        print("🚀 Sound Saber ATIVADO! Mova o mouse para ouvir.")
        self.speak("Sound Saber ativado")

        # Listener do mouse
        with mouse.Listener(on_move=self.on_move) as listener:
            listener.join()

    def stop(self):
        self.is_active = False
        print("⛔ Sound Saber parado.")


# ===================== EXECUÇÃO =====================
if __name__ == "__main__":
    saber = SoundSaber()
    try:
        saber.start()
    except KeyboardInterrupt:
        saber.stop()