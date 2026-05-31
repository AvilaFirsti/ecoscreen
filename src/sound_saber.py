"""
Sound Saber - Versão 1.9
Borda Contínua com som DISTINTO
"""

import time
import subprocess
import numpy as np
import sounddevice as sd
from pynput import mouse
import pyttsx3

class SoundSaber:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)
        self.is_active = False
        
        self.volume = 0.18
        self.pitch_range = 220
        
        try:
            output = subprocess.check_output(["xrandr"]).decode()
            import re
            match = re.search(r'(\d+)x(\d+)', output)
            self.screen_width = int(match.group(1))
            self.screen_height = int(match.group(2))
        except:
            self.screen_width = 1920
            self.screen_height = 1080

        self.stream = None
        print(f"🔊 Sound Saber 1.9 - Borda com som distinto")

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def start_audio_stream(self):
        def callback(outdata, frames, time_info, status):
            if not self.is_active:
                outdata[:] = 0
                return
                
            try:
                x, y = mouse.Controller().position
                
                norm_x = max(0, min(1, x / self.screen_width))
                norm_y = max(0, min(1, y / self.screen_height))
                
                t = np.linspace(0, frames/44100, frames, False)
                
                # === SOM NORMAL DENTRO DA TELA ===
                base_freq = 280 - (norm_y * self.pitch_range)
                hum = self.volume * np.sin(base_freq * t * 2 * np.pi)
                subtle = (self.volume * 0.25) * np.sin(4.2 * t * 2 * np.pi)
                tone = hum + subtle
                
                # === DETECÇÃO DE BORDA ===
                at_border = (x <= 12 or x >= self.screen_width - 12 or 
                            y <= 12 or y >= self.screen_height - 12)
                
                if at_border:
                    # Som DISTINTO da borda (mais grave e "encorpado")
                    border_freq = 160 + (norm_y * 60)   
                    border_hum = 0.32 * np.sin(border_freq * t * 2 * np.pi)
                    border_vib = 0.12 * np.sin(9 * t * 2 * np.pi)
                    tone = border_hum + border_vib   
                    
                    # Aviso sutil de borda
                    tone += 0.08 * np.sin(1200 * t * 2 * np.pi)
                
                # Panning
                pan = norm_x * 2 - 1
                left = tone * (0.9 - pan * 0.45)
                right = tone * (0.9 + pan * 0.45)
                
                outdata[:, 0] = left
                outdata[:, 1] = right
                
            except:
                outdata[:] = 0

        self.stream = sd.OutputStream(samplerate=44100, channels=2, callback=callback, blocksize=1024)
        self.stream.start()

    def start(self):
        self.is_active = True
        print("🚀 Sound Saber 1.9 ATIVADO!")
        self.speak("Sound Saber versão 1.9 ativado")
        
        self.start_audio_stream()
        
        with mouse.Listener(on_move=lambda x, y: None) as listener:
            listener.join()

    def stop(self):
        self.is_active = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
        print("⛔ Sound Saber parado.")


if __name__ == "__main__":
    saber = SoundSaber()
    try:
        saber.start()
    except KeyboardInterrupt:
        saber.stop()
