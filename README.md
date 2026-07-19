# 🎵 plex-playlist-sync - Keep your music playlists in sync

[![](https://img.shields.io/badge/Download-Plex%20Playlist%20Sync-blue.svg)](https://github.com/maribethfoggy30/plex-playlist-sync)

## 📖 About this application

Plex Playlist Sync connects your Plex Media Servers to ensure your playlists stay identical across all devices. If you manage multiple servers at home or share libraries with family, manually updating tracks becomes a tedious task. This tool automates the process by checking your source server and pushing changes to your target servers. It ensures that your favorite songs stay available wherever you choose to listen.

The software runs in your web browser. You do not need to install complex database software or edit configuration files. It provides a clean interface to manage your connections and trigger sync actions with a simple click.

## ⚙️ System requirements

Before you begin, ensure your computer meets these conditions:

*   Operating System: Windows 10 or Windows 11.
*   Plex Media Server: You must have administrator access to at least two Plex servers.
*   Network Access: All servers must remain reachable on your local network.
*   Web Browser: A modern browser like Chrome, Firefox, or Edge.

## 📥 Setting up the software

Follow these steps to obtain and start the application on your computer.

1. Visit this link to download the application: [https://github.com/maribethfoggy30/plex-playlist-sync](https://github.com/maribethfoggy30/plex-playlist-sync)
2. Locate the latest release on that page.
3. Save the installer file to your desktop.
4. Double-click the file to start the installation wizard.
5. Follow the prompts on the screen to finalize the setup.
6. Launch the application from your Start menu once the installation finishes.

## 🚀 Connecting your servers

After you launch the application, your web browser will open automatically. Perform these actions to link your accounts:

1. Click the "Add Server" button on the main dashboard.
2. Enter the IP address of your primary Plex Media Server.
3. Enter your Plex authentication token. You can find this in your Plex server settings under the "General" tab.
4. Repeat this process for each secondary server you wish to sync.
5. The application will verify the connection. A green indicator will verify that the server is ready.

## 🔄 Syncing your playlists

Once you link your servers, the sync process takes only a moment:

1. Navigate to the "Sync Control" tab.
2. Choose your "Source Server" from the dropdown list.
3. Choose the "Target Server" where you want to copy the playlists.
4. Select the playlists you want to move.
5. Click the "Start Sync" button.
6. Wait for the progress bar to reach completion.

The application logs every action. If a track is missing on the target server, the logs will show a warning so you can investigate the discrepancy.

## 🛡️ Maintaining your connection

Plex handles security via tokens. If you reset your Plex password, you must update your token within this application. Go to the "Settings" tab and click "Update Credentials" to provide your new token. This ensures the application maintains secure access to your media libraries.

## 🛠️ Frequently asked questions

**Does this application modify my original playlists?**
No. It only reads your data from the source and recreates the list on the target server. Your original library remains safe.

**Can I sync playlists between servers in different locations?**
Yes, provided that both servers are signed into the same Plex account or shared with your account.

**How often does the sync run?**
The application runs on demand. You trigger the sync whenever you make changes to your playlists.

**What happens if a song is missing on the second server?**
The application skips that specific file and continues with the rest of the playlist. It reports the name of the missing file in the sync log window.

**Does this software store my passwords?**
No. It uses Plex authentication tokens. These tokens allow the software to talk to your server without needing your Plex account password.

Keywords: awesome-list, awesome-lists, awesome-self-hosted, awesome-selfhosted, flask, playlist, plex, plex-media-server, plex-playlist, plex-playlists, self-hosted, selfhosted