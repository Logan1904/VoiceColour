# Colour of Your Voice

Figure out the colour of your voice (or whatever inhuman sound you can muster up)!

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

## Method

**Parameters**: The sampling rate and block size (for FFT) can be changed on Lines 10 and 11. (Note: Nyquist Theorem for Sampling Rate!)  

We get the audio input from the default input device. You can change the audio input device by adding a `device` input argument to `sd.InputStream` on Line 48 (https://python-sounddevice.readthedocs.io/en/0.3.15/api/streams.html#sounddevice.InputStream)  

We then perform **Fast Fourier Transfrom** to obtain the frequency signal from the raw audio input  

Finally, the dominant frequency is extracted and is converted to an RGB colour using linear interpolation between 0 Hz and 2000 Hz (This can be changed in the `frequency_to_colour` function)  

![image](https://github.com/user-attachments/assets/840d36ba-1ad8-45e1-a00f-daca54c2552b)
