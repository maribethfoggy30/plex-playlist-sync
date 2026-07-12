# 📖 Full Installation Guide — Plex Playlist Sync

This is the detailed, hold-your-hand version. It covers **Windows**, **macOS**, and **Linux**, both the easy double-click way and the manual way, plus a big troubleshooting section at the end.

If you just want the fast version, see the Quick Start in [README.md](README.md).

---

## Table of contents
- [Before you start: what you'll need](#before-you-start-what-youll-need)
- [Step 1 — Find your Plex token](#step-1--find-your-plex-token)
- [Step 2 — Find your server address](#step-2--find-your-server-address)
- [Install on Windows](#install-on-windows)
- [Install on macOS](#install-on-macos)
- [Install on Linux](#install-on-linux)
- [Step 3 — Fill in your configuration (.env)](#step-3--fill-in-your-configuration-env)
- [Step 4 — Run the app](#step-4--run-the-app)
- [Troubleshooting](#troubleshooting)

---

## Before you start: what you'll need

1. **Python 3.8 or newer.** We'll install this in the OS-specific steps if you don't have it.
2. **At least one Plex Media Server** you control, and **its token** (Step 1).
3. **The address of each server** (Step 2).
4. About **5 minutes.**

---

## Step 1 — Find your Plex token

Every Plex server needs a token so the app can log in. To find one:

1. Sign in to Plex in a web browser and open any movie or show.
2. Click the **⋯ (More)** button → **Get Info** → **View XML**.
3. A new browser tab opens with a long URL. At the very end of that URL you'll see `X-Plex-Token=................`.
4. Copy the value after `X-Plex-Token=`. **That's your token.**

Official guide with pictures: <https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/>

> If your servers are on the same Plex account, they often share the same token. If they're separate accounts, grab a token from each one.

---

## Step 2 — Find your server address

Each server's address looks like `http://<ip-address>:32400`.

- **Local server** (same house/network): use its **local IP**, e.g. `http://192.168.1.10:32400`. You can find this in Plex under **Settings → Remote Access**, or in your router's device list.
- **Remote server**: use its **public IP or hostname**, e.g. `http://your-remote-host:32400`. The server must be reachable from wherever you run this app.

`32400` is Plex's standard port — keep it unless you've changed it.

---

## Install on Windows

### Install Python (skip if you already have it)
1. Go to <https://www.python.org/downloads/> and click **Download Python**.
2. Run the installer. **⚠️ Very important:** on the first screen, tick **“Add python.exe to PATH”** before clicking **Install Now**. This one checkbox prevents the most common error.
3. When it finishes, open **Command Prompt** and type `python --version` — you should see a version number.

### Install the app (easy way)
1. On this project's GitHub page, click the green **Code** button → **Download ZIP**.
2. Unzip it somewhere handy (e.g. your Desktop).
3. Open the unzipped folder and **double-click `install-windows.bat`**. A black window will run through the setup and create your `.env` file.
4. Continue to [Step 3](#step-3--fill-in-your-configuration-env).

---

## Install on macOS

### Install Python (skip if you already have it)
- macOS may already have Python 3. Open the **Terminal** app (Applications → Utilities → Terminal) and type `python3 --version`.
- If you get a version number, you're set. If not, download it from <https://www.python.org/downloads/> and run the installer.

### Install the app (easy way)
1. On this project's GitHub page, click the green **Code** button → **Download ZIP**.
2. Unzip it (double-click the ZIP) and open the folder.
3. **Double-click `install-mac.command`.**
   - **The first time**, macOS will likely say *“cannot be opened because it is from an unidentified developer.”* This is normal for all indie scripts. To get past it: **right-click** the file → **Open** → **Open** in the dialog. You only have to do this once per file.
   - If double-clicking still doesn't run it, see [the chmod tip](#the-command-files-wont-run-on-mac) in Troubleshooting.
4. Continue to [Step 3](#step-3--fill-in-your-configuration-env).

---

## Install on Linux

Open a terminal in the project folder and run:

```bash
# 1. Make sure Python and venv are available
python3 --version
sudo apt install python3-venv python3-pip   # Debian/Ubuntu; adjust for your distro

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your config file
cp .env.example .env
```

Then edit `.env` (Step 3) and run with `python app.py` (Step 4).

---

## Step 3 — Fill in your configuration (.env)

The installer created a file named **`.env`** in the project folder (on Linux you copied it yourself). Open it in any text editor — Notepad on Windows, TextEdit on Mac, or `nano .env` on Linux.

Fill in a block for each server:

```env
WEB_PORT=8511

PLEX_SERVER_1_NAME=Server 1 (Local)
PLEX_SERVER_1_URL=http://192.168.1.10:32400
PLEX_SERVER_1_TOKEN=paste_your_token_here

PLEX_SERVER_2_NAME=Server 2 (Remote)
PLEX_SERVER_2_URL=http://your-remote-host:32400
PLEX_SERVER_2_TOKEN=paste_your_token_here
```

- Replace the URLs with **your** server addresses from Step 2.
- Replace `paste_your_token_here` with **your** token(s) from Step 1.
- Need a third server? Copy a block and change the number to `3`.
- **Save the file** and make sure it's named exactly `.env` (not `.env.txt` — see Troubleshooting if Windows added `.txt`).

---

## Step 4 — Run the app

- **Windows:** double-click **`start-windows.bat`**.
- **Mac:** double-click **`start-mac.command`**.
- **Linux / manual:** run `source venv/bin/activate` then `python app.py`.

A window will open and print a message. Then open your web browser to:

**http://localhost:8511**

(If you changed `WEB_PORT`, use that number instead.)

To use it from another device on your network, replace `localhost` with the IP address of the computer running the app, e.g. `http://192.168.1.50:8511`.

To **stop** the app, close that window (or press `Ctrl+C` in it).

---

## Troubleshooting

### "Python is not recognized" / "command not found"
Python isn't installed or isn't on your PATH.
- **Windows:** reinstall Python and make sure you tick **“Add python.exe to PATH”**, then restart Command Prompt.
- **Mac/Linux:** try `python3` instead of `python`.

### The `.command` files won't run on Mac
macOS strips the "executable" permission from downloaded scripts. Two fixes:
- **Easy:** right-click the file → **Open** → **Open**.
- **If that fails:** open Terminal in the project folder and run:
  ```bash
  chmod +x install-mac.command start-mac.command
  ```
  Then double-click again.

### Windows saved my file as `.env.txt`
Notepad sometimes adds `.txt`. Fix it: in File Explorer, turn on **View → File name extensions**, then rename `.env.txt` back to `.env`. (Or in Notepad's Save dialog, set "Save as type" to **All Files** and quote the name: `".env"`.)

### The page loads but says "No playlists found" or shows a connection error
This almost always means the app can't reach that server or the token is wrong. Check:
- Is the **URL** exactly right, including `http://` and `:32400`?
- Is the **token** correct and for that specific server?
- Can the computer running the app actually **reach** that server? (Try opening the server's URL in a browser.)
- Is the Plex server **turned on and online**?

### "Address already in use" when starting
Something else is using port 8511. Change `WEB_PORT` in your `.env` to another number (e.g. `8600`) and restart.

### A static playlist synced but some items are missing
That's expected and by design — the target server didn't have those specific movies/episodes in its library, so they were skipped. The app tells you how many were skipped. Add the missing media to the target server and sync again.

### A smart playlist won't sync
The target server needs a library of the **same type** (e.g. if the smart playlist is built from Movies, the target needs a Movies library). Make sure a matching library exists on the target.

### Still stuck?
Open an Issue on the GitHub repo describing your OS, what you did, and the exact error message — happy to help.
