# WAV Randomiser

## About
    
Provided a folder with images and corresponding audio files, such as yo.gif and yo.wav, the program will randomise the audio and show the 'answer' image when requested.
This was created for learning Japanese characters, but could equally be used for other languages or even UK Road Signs.

## Commands

- To run: `python randomiser.py`
- To make an executeable: `pyinstaller --onefile --add-data="pi.gif;img" --icon=.\a.ico --windowed .\randomiser.py`

## How-To

1. Browse for a folder with audio files in it
2. Select some files to randomise
3. Update the selection
4. Click Play to open the Play Menu
5. Click Play Next Sound
6. Click Display to display associated image
7. Repeat 5 and 6

All audio must be .wav files
All images must be .gif files
Audio and Images can be converted online or with software
Images must have the same name as the audio file
e.g. random.wav and random.gif
