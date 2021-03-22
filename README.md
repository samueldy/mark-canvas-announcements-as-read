# Mark all Canvas Announcements as Read

Easy way to automatically mark all course announcements on Canvas as read, instead of doing them manually one by one.

Users of Instructure's [Canvas LMS](https://www.instructure.com/canvas/) have [asked a lot](https://community.canvaslms.com/t5/Idea-Conversations/Marking-all-announcements-read/idi-p/351918) for the ability to quickly mark all course announcements as read. As of 24 Dec 2020, this capability still doesn't seem to be implemented in the web or mobile app GUIs, but is available through v1 of the Canvas REST API. This Python script facilitates this action.

## Configuration

You need a Canvas LMS token to run this script.

1. Log into the Canvas web app using your institution's domain (i.e., `https://umich.instructure.com`) and make a note of this `.instructure.com` URL.
2. Under **Account** > **Settings** > **Approved Integrations**, choose to generate a new access token. Take note of this token (a long string of letters, numbers, and symbols) because you can't see it again once you leave that screen.
3. Create a file `~/.instructure/.instructure.json`, where `~` is your home folder. (On Windows 7/8/10, this folder is generally located at `%USERPROFILE%`, `%HOMEPATH%`, or `C:\Users\<username>`. On  macOS and most \*NIX systems it is usually located at `$HOME` or `/home/<username>`.) In this file, enter your token in the form:
```
{"token": "YOUR_TOKEN_HERE"}
```
4. Clone this repo to your local computer.
5. Change the `MY_DOMAIN` variable in the script to match your institution's Canvas URL (e.g., `https://umich.instructure.com` for University of Michigan).

## Usage

Run the script using Python, 3.6 or higher. You'll need the `requests` library, which is available from PyPI or Anaconda Cloud:

```
# Install `requests` library from PyPI
pip install -U requests

# Or install `requests` library with conda
conda activate <your_environment>
conda install -c conda-forge requests
```

Then just run the script directly. No command-line arguments are needed.

```
# On Linux/macOS/BSD
cd <repo folder>
python3 ./mark-canvas-announcements-as-read.py

# Or on Windows
cd <repo folder>
python ./mark-canvas-announcements-as-read.py
```

Hope this helps!!
