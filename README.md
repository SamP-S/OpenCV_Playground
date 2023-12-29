# OpenCV Playground

A tkinter wrapper around core opencv functions. Good for experimenting with opencv through a simple GUI to see what different image operations do. Originally created for trying to extract data from scanned graphs but the project was cancelled so this is the expirmentation work leftover and cleaned up a bit.

## Installation

### Requirements
- Numpy
- MatPlotLib
- OpenCV-4
- TKinter
- Pillow

### Installation Steps
1. Install OpenCV & TKinter (Copy + Paste in Terminal)
```
# Debian Linux Systems (Ubuntu)
sudo apt update
sudo apt install python3-opencv
sudo apt install python3-tk
```
```
# Arch Linux Systems (Manjaro)
sudo pacman -Syu
sudo pacman -S opencv
sudo pacman -S python-opencv
sudo pacman -S tk
```

2. Install python package dependencies
```
pip install -r requirements.txt
```


## Usage
Run main driver python script:
```
python main.py
```

## Features
Current features:
- Linux Only
- Load image
- Operation timeline (undo/redo)
- Image operations

Current image operations supported:
- Grey Scale
- Blur/Sharpen
- Black/White Threshold
- Edge Detection
- Colour Range Mask
- RGB Filter
- Contrast

## License

This project is licensed under the [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0.html).
