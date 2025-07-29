# DeskWebLib

**DeskWebLib** is a custom Robot Framework library that combines web automation using Selenium and desktop automation using image-based techniques with PyAutoGUI. It is designed for hybrid test scenarios involving both browser and desktop applications.

## Features

- Web automation using Selenium
  - Open browser, navigate, click, input text, verify elements, etc.
- Desktop automation using PyAutoGUI and image recognition
  - Launch applications, send text, image-based clicking, log checking

## Installation

```bash
pip install Deskweblib==0.1.4
```
## Folder Structure
```
DeskWebLib/
├── DesktopKeywords/
│   ├── __init__.py
│   └── keywords.py
├── WebKeywords/
│   ├── __init__.py
│   └── keywords.py
├── DeskWebLib/
│   └── DeskWebLib.py
├── setup.py
├── README.md
└── LICENSE
```

## How to Import in Robot Framework
```commandline
*** Settings ***
Library    DeskWebLib    browser=chrome    implicit_wait=5

```

## Available Keywords
### Web Keywords
```
Open Browser

Go To

Click Element

Input Text

Get Text

Maximize Browser Window

Close Browser
```
### Desktop (Image-Based) Keywords
```
Image Based MouseClick

Launch Application

Send Text

Check Log Entries

Clear Log File
```
##  To generate complete keyword documentation:

```bash
python -m robot.libdoc DeskWebLib.DeskWebLib output.html
```

