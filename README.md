# Colour of Your Voice

Figure out the colour of your voice (or whatever inhuman sound you can muster up)!

![Screenshot 2025-06-15 114544](https://github.com/user-attachments/assets/ddb6826d-daf3-4536-ada9-79abba0910d8)

## Setup

Create a conda environment with `requirements.txt`  
```
conda create --name VoiceColour
conda activate VoiceColour
conda install --file requirements.txt
```

Run the Python file
```
python main.py
```

Sing to your heart desires!

## Features
### Raw Audio Signal
The raw audio signal is obtained from a sounddevice input stream, using the default input microphone. You can change the audio input device by adding a `device` input argument to `sd.InputStream` on Line 83 (https://python-sounddevice.readthedocs.io/en/0.3.15/api/streams.html#sounddevice.InputStream).

### FFT Spectrum
A **Fast Fourier Transform** is applied to the raw audio signal to obtain the frequency signals. The dominant frequency is extracted from the FFT, and mapped to an RGB colour via linear interpolation. This is done in the 0 Hz to 2000 Hz range; if you belive you can muster ungodly sounds that are outside this range, this can be changed via `MAX_FREQ` on line 15.

### Spectrogram
A time-frequency spectrogram is shown to visualise the breadth of frequencies present, over the past 5 seconds.

### Perlin Visual
A Perlin noise visualisation is also presented, unique to the extracted dominant frequency - the dominant frequency is used as the seed in the Perlin generator function.

## User Parameters
**Parameters**: The sampling rate and block size (for FFT) can be changed on Lines 12 and 13. (Note: Nyquist Theorem for Sampling Rate). Additionally, the spectogram time limit and the maximum frequency used for analysis can be changed on Lines 14 and 15.


