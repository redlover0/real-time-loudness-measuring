# Safe Sound - Real-time Audio Analysis

> [!IMPORTANT]
> Safe Sound is a project by Create Co-Creator, dedicated to making sound environments safer for everyone. Our mission is to provide tools and solutions that help monitor, analyze, and improve audio safety across various environments. 
> Please be aware of this.

## About Create Co-Creator
Create Co-Creator is committed to developing innovative solutions for audio safety and analysis. This project represents one of our initiatives to make sound environments safer and more manageable for everyone.

## Development Status
This project serves as a proof of competency and is under active development by Create Co-Creator. As of December 13th, 2024, we are working on:
- JavaScript frontend implementation
- Second edition with enhanced features
- Additional improvements and optimizations

A simple package for real-time audio analysis in native Python, leveraging PyAudio and Numpy to extract and visualize FFT features from a live audio stream. The project offers capabilities for recording, analyzing, and visualizing audio data in real-time.

## Features

### Live Audio Analysis Pipeline
* Stream reader that captures live audio data from any source using PyAudio (soundcard, microphone, etc.)
* High-frequency data sampling (up to 1000 updates per second) with FIFO buffer storage
* Real-time FFT (Fast-Fourier-Transform) analysis via `.get_audio_features()`
* Interactive visualization through PyGame GUI with both 2D and 3D display modes

### Menu Options
1. Record New Data - Measure loudness in real-time
2. Analyze Existing Data - Process recorded audio data
3. Visualize Audio - Real-time audio environment visualization
4. Exit

## Installation

### Requirements
```bash
pip install -r requirements.txt
```

### System Dependencies

#### Ubuntu/Debian
```bash
sudo apt install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
```

#### macOS
```bash
brew install portaudio
```

### Alternative Audio Interface
If PyAudio isn't compatible with your system (common on Windows/Mac), you can use sounddevice:
```bash
pip install sounddevice
```

To switch between audio interfaces, modify the `__init__` function in the Stream_Analyzer class.

## Platform Compatibility
* Works across platforms where PyGame can access display and Python can detect audio card
* May require additional configuration in WSL environments
* Alternative sounddevice interface available for better Windows/Mac compatibility

## Usage
Run the program and select from the menu options (1-4) to access different features:
```
__________________________________________________

 Safe Sound - Real time audio analysis
__________________________________________________

 1. Record New Data - Measure Loudness in real time 

 2. Analyze Existing Data - here you can analyze data you've recorded

 3. Visualize Audio - visualize the audio environment around you
    Credit: https://github.com/aiXander

 4. Exit

Enter your choice (1-4): 
```

## Contributing
Feel free to contribute by submitting pull requests or opening issues. Please note the usage restrictions mentioned at the top of this README.