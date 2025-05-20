import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import colorsys


# Audio settings
SAMPLE_RATE = 44100  # Hz
BLOCK_SIZE = 4410    # 100 ms

# Frequency to colour 
def frequency_to_colour(freq, min_freq=0, max_freq=2000):
    freq = np.clip(freq, min_freq, max_freq)
    h = (freq - min_freq) / (max_freq - min_freq)
    r, g, b = colorsys.hls_to_rgb(h, 0.5, 1.0)

    return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'

class VoicecolourApp:
    def __init__(self, root):
        self.root = root
        self.root.title("colour of Your Voice")

        # Create plots
        self.fig, (self.ax_waveform, self.ax_fft) = plt.subplots(2, 1, figsize=(12, 8))
        self.fig.tight_layout(pad=3)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        # colour block
        self.colour_frame = tk.Frame(root, width=800, height=100, bg='black')
        self.colour_frame.pack(pady=10)

        # Frequency label
        self.freq_label = tk.Label(root, text="Listening...", font=("Helvetica", 14))
        self.freq_label.pack()

        # Audio buffer
        self.latest_audio = np.zeros(BLOCK_SIZE)
        self.new_data_available = False

        # Start updating plots
        self.root.after(30, self.update_plots)

        # Start audio stream
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            blocksize=BLOCK_SIZE,
            channels=1,
            callback=self.audio_callback
        )
        self.stream.start()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print("Audio Callback Status:", status)

        self.latest_audio = indata[:, 0].copy()
        self.new_data_available = True

    def update_plots(self):
        if self.new_data_available:
            audio = self.latest_audio
            self.new_data_available = False

            # Normalize audio to [-1, 1] because whistling can be very low amplitude
            max_val = np.max(np.abs(audio))
            if max_val != 0:
                audio = audio / max_val

            t = np.linspace(0, len(audio) / SAMPLE_RATE, num=len(audio)) * 1000  # ms

            # FFT
            fft_vals = np.abs(np.fft.rfft(audio))
            fft_freqs = np.fft.rfftfreq(len(audio), 1 / SAMPLE_RATE)

            # Normalize
            fft_vals /= np.max(fft_vals) if np.max(fft_vals) != 0 else 1
            
            # Find dominant frequency
            dominant_idx = np.argmax(fft_vals)
            dominant_freq = fft_freqs[dominant_idx]

            # Waveform plot
            self.ax_waveform.clear()
            self.ax_waveform.plot(t, audio)
            self.ax_waveform.set_title("Raw Audio Signal")
            self.ax_waveform.set_xlabel("Time (ms)")
            self.ax_waveform.set_ylim(-1, 1)
            self.ax_waveform.grid(True)

            # FFT plot
            self.ax_fft.clear()
            self.ax_fft.plot(fft_freqs, fft_vals)
            self.ax_fft.set_title("FFT Spectrum")
            self.ax_fft.set_xlabel("Frequency (Hz)")
            self.ax_fft.set_xlim(0, 2000)
            self.ax_fft.set_ylim(0, 1)
            self.ax_fft.grid(True)

            # Set colour block and label
            colour = frequency_to_colour(dominant_freq)
            self.colour_frame.config(bg=colour)
            self.freq_label.config(text=f"Dominant Frequency: {dominant_freq:.1f} Hz")

            self.canvas.draw()

        # Schedule next update
        self.root.after(30, self.update_plots)

if __name__ == "__main__":
    root = tk.Tk()
    app = VoicecolourApp(root)
    root.mainloop()