# Game Inspector
It's a tool to measure FPS, FlipRate and other metrics, take screenshots, record video and draw overlay

This applications is based on:
* [fps_inspector_sdk](https://github.com/Andrey1994/fps_inspector_sdk)
* [screen_recorder_sdk](https://github.com/Andrey1994/screen_recorder_sdk)
* [game_overlay_sdk](https://github.com/Andrey1994/game_overlay_sdk)

**These python libraries could be used for automation and to develop other applications**

fps_inspector_sdk and screen_recorder_sdk are API agnostic and dont hook inside game process and can be used without game_overlay_sdk which hooks inside game process, so without overlay **it works with all games on all hardware**. To use them without overlay you need to choose PID mode in configuration window.

Game overlay is an experimental feature, for now it should work with x32 and x64 games which are based on:
* DX11
* DX12
* Vulkan
To use Game Overlay you need to choose Process Path or Process Name option, also for Steam Games you need to enter Game Id, more information about these options can be found in [game_overlay_sdk readme](https://github.com/Andrey1994/game_overlay_sdk)

## Installation
First of all you need to install Python 3 x64

To install all dependencies please run:
```
git submodule update --init --recursive
python fps_inspector_sdk\python\setup.py install
python screen_recorder_sdk\python\setup.py install
python game_overlay_sdk\python\setup.py install
python -m pip install -r requirements.txt
garden.bat install filebrowser --kivy
garden.bat install matplotlib --kivy
```
fps_inspector_sdk, screen_recorder_sdk and game_overlay_sdk could be installed from PYPI but in this case pyintaller will fail to find DLLs which are required for these packages, so I've attached them as submodules.

After that you will be able to run it using:
```
python game_inspector.py
```
To create a standalone executable please run:
```
python -m pyinstaller game_inspector.spec
```
game_inspector.exe will be in dist folder

## Usage Sample
**You need to run it with administrator priviligies and I recommend to start it from cmd, in this case you will see logs**
### Welcome Screen
![welcome](https://live.staticflickr.com/65535/48117105993_fed148044b_b.jpg)
Just press *Configure Session*
### Configuration
Here you have to specify one of the following options:
* PID(no overlay) - Process Id from running process, you can set 0 here, the application will taks screenshot of entire screen and record all events for FPS calculation. 
* Process Path(Overlay, works with SteamApp Id) - Path to an executable, application will run it. You can use filebrowser and click *Ok*
* Process Name(Overlay, doesnt works with SteamApp Id) - process name with extension, you will need to run it manually

Optional Inputs:
* SteamApp Id -  required for Steam Games, can be found [here](https://steamdb.info/search)
* Hotkeys which you are able to override(default are shift+i, shift+o, shift+p)
![configuration](https://live.staticflickr.com/65535/48117073956_4074e6d06b_b.jpg)

### Run
If you choosed overlay capable mode you will see game overlay in the left bottom corner, to start messaging you need to trigger hotkeys or press buttons, in PID mode you will not see an overlay but everything else will be the same.
**UI:**
* left upper corner - buttons to control
* left bottom corner - video, you will need to press play after recording
* right upper corner - fps/fliprate plot(in stored csv files there are much more useful metrics!)
* right bottom corner - screenshot
![run](https://live.staticflickr.com/65535/48117073881_37c41695a9_b.jpg)
