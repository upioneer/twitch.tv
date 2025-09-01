# Twitch Stream Auto-Switcher
This script automates the process of finding and playing random streams from a specific Twitch collection in a dedicated browser window
## Prerequisites
Install Python 3.x
```bash
sudo apt install python3
```
Install Playwright
```bash
pip install playwright
```
or on Debian, install npm and Playwright
```bash
sudo apt-get install npm
npm init playwright@latest
```
Install python3-venv package
```baseh
sudo apt install python3.11-venv
```
## Setup
### Install Playwright and Browser Binaries
It's recommended to use a virtual environment
```
python3 -m venv twitch_env
source twitch_env/bin/activate
pip install playwright
playwright install
```
### Save the Script
[twitch_stream_auto_switcher.py](twitch_stream_auto_switcher.py)

Save the Python code as `twitch_stream_auto_switcher.py` in your desired directory.
## Run
Navigate to the script directory and execute
```
cd /path/to/your/script/
source twitch_env/bin/activate # If you used a virtual environment
python twitch_stream_auto_switcher.py
```

> Optional steps
## Customization
You can modify the script's behavior by changing the configuration variables at the top of the `twitch_stream_auto_switcher.py` file:
* `INTERVAL_MINUTES`: Sets how often (in minutes) a new stream is selected. Default is `30`
* `HEADLESS_MODE`: Set to `True` to run the browser without a visible GUI (in the background). Set to `False` to see the browser window. Default is `False`
## Browser Choice
The script uses Chromium by default. You can switch to Firefox or WebKit (Safari's engine) by changing the `playwright.chromium.launch()` line to `playwright.firefox.launch()` or `playwright.webkit.launch()` respectively, provided you have installed their binaries using `playwright install`
## Stop the Script
To stop the script from running, simply press `Ctrl + C` in the terminal where the script is active
## Important Note
This script launches its *own* browser window/tab and cannot directly control or replace an already open tab in your existing browser session (e.g., your personal Firefox window). This is a security feature of browser automation tools.
# References
[Playwright Documentation](https://playwright.dev/python/docs/intro)
# Related
[[WSL2]]
