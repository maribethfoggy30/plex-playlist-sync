import os
import sys

import requests
import plexapi
import urllib3
from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from plexapi.server import PlexServer
from dotenv import load_dotenv

# ---------------------------------------------------------
# 🔧 CONFIGURATION (loaded from your .env file)
# ---------------------------------------------------------
# All personal settings live in a local ".env" file that is NEVER
# uploaded to GitHub. Copy ".env.example" to ".env" and fill it in.
# ---------------------------------------------------------
load_dotenv()

WEB_PORT = int(os.getenv("WEB_PORT", "8511"))
HOST = os.getenv("HOST", "0.0.0.0")
DEBUG = os.getenv("FLASK_DEBUG", "false").strip().lower() in ("1", "true", "yes", "on")


def load_servers():
    """Build the server list from environment variables.

    Define each server in .env with numbered blocks, e.g.:
        PLEX_SERVER_1_NAME=Server 1 (Local)
        PLEX_SERVER_1_URL=http://192.168.1.10:32400
        PLEX_SERVER_1_TOKEN=your_plex_token_here
    Add as many as you like (SERVER_2, SERVER_3, ...).
    """
    servers = {}
    for i in range(1, 21):  # supports up to 20 servers
        name = os.getenv(f"PLEX_SERVER_{i}_NAME")
        url = os.getenv(f"PLEX_SERVER_{i}_URL")
        token = os.getenv(f"PLEX_SERVER_{i}_TOKEN")

        if not any([name, url, token]):
            continue  # empty slot, skip it

        if name and url and token:
            servers[name] = {"url": url, "token": token}
        else:
            print(f"⚠️  Skipping PLEX_SERVER_{i}: incomplete config "
                  f"(each server needs NAME, URL, and TOKEN).")
    return servers


SERVERS_CONFIG = load_servers()

if not SERVERS_CONFIG:
    print("❌ No Plex servers configured.")
    print("   Copy '.env.example' to '.env' and add at least one server "
          "(two if you want to sync between them).")
    sys.exit(1)

# Bypass SSL certificate verification issues for raw remote IP addresses
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------------------------------------------------------
# FLASK APPLICATION INITIALIZATION
# ---------------------------------------------------------
app = Flask(__name__)


def get_plex_client(name):
    """Safely connects to a Plex server using an insecure SSL context handling."""
    import requests
    cfg = SERVERS_CONFIG.get(name)
    if not cfg:
        return None, "Configuration missing"
    try:
        session = requests.Session()
        session.verify = False
        plex = PlexServer(cfg["url"], cfg["token"], session=session)
        return plex, None
    except Exception as e:
        return None, str(e)

# ---------------------------------------------------------
# DARK MODE FRONTEND TEMPLATE (WITH SAFARI ALIGNMENT FIX)
# ---------------------------------------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>🎬 Plex Playlist Sync</title>
    <style>
        body { background-color: #121212; color: #E0E0E0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #e5a93b; text-align: center; margin-bottom: 5px; }
        .caption { text-align: center; color: #888; margin-bottom: 30px; }
        .alert { background-color: #cf6679; color: #000; padding: 12px; border-radius: 4px; margin-bottom: 20px; font-weight: bold; text-align: center; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
        .panel { background-color: #1e1e1e; border: 1px solid #333; border-radius: 8px; padding: 20px; }
        select { width: 100%; padding: 10px; background-color: #2c2c2c; color: #fff; border: 1px solid #444; border-radius: 4px; margin-bottom: 20px; font-size: 16px; }

        /* Playlist Item Layout and Safari Alignment Fixes */
        .playlist-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #252525;
            padding: 10px 15px;
            margin-bottom: 8px;
            border-radius: 4px;
            border-left: 4px solid #e5a93b;
            min-height: 38px; /* Standardizes column container heights perfectly across Safari/Webkit */
            box-sizing: border-box;
        }

        /* Rename Input Styling */
        .playlist-name-container {
            display: flex;
            align-items: center;
            flex-grow: 1;
            margin-right: 15px;
            overflow: hidden;
        }
        .playlist-input {
            background: transparent;
            color: #fff;
            border: 1px solid transparent;
            padding: 4px 8px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 4px;
            width: 100%;
            transition: all 0.2s;
            box-sizing: border-box;
            height: 30px; /* Explicit height constraints bypass Safari form agent padding variations */
        }
        .playlist-input:hover { background-color: #2c2c2c; border-color: #555; cursor: pointer; }
        .playlist-input:focus { background-color: #1a1a1a; border-color: #e5a93b; color: #e5a93b; outline: none; cursor: text; }

        .smart-badge { background-color: #29b6f6; color: #000; font-size: 11px; padding: 2px 6px; border-radius: 3px; font-weight: bold; margin-left: 6px; white-space: nowrap; }
        .sync-btn { background-color: #e5a93b; color: #121212; border: none; padding: 8px 16px; border-radius: 4px; font-weight: bold; cursor: pointer; text-decoration: none; font-size: 14px; transition: background 0.2s; white-space: nowrap; display: inline-flex; align-items: center; height: 30px; }
        .sync-btn:hover { background-color: #ffca66; }
        .no-playlists { color: #666; font-style: italic; text-align: center; margin-top: 20px; }
    </style>
    <script>
        function renamePlaylist(inputElement, serverName, oldName) {
            const newName = inputElement.value.trim();

            if (!newName || newName === oldName) {
                inputElement.value = oldName;
                return;
            }

            fetch('/rename', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams({
                    'server': serverName,
                    'old_name': oldName,
                    'new_name': newName
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    inputElement.style.color = '#4caf50';
                    setTimeout(() => { inputElement.style.color = ''; }, 1000);

                    inputElement.setAttribute('onblur', `renamePlaylist(this, '${serverName}', '${newName.replace(/'/g, "\\'")}')`);
                    inputElement.onkeypress = function(e) {
                        if (e.which == 13) { this.blur(); }
                    };

                    const itemPanel = inputElement.closest('.playlist-item');
                    const syncBtn = itemPanel.querySelector('.sync-btn');
                    if (syncBtn) {
                        const url = new URL(syncBtn.href, window.location.origin);
                        url.searchParams.set('playlist', newName);
                        syncBtn.href = url.pathname + url.search;
                    }
                } else {
                    alert('⚠️ Error renaming playlist: ' + data.error);
                    inputElement.value = oldName;
                }
            })
            .catch(err => {
                alert('💥 Network error encountered during rename handling.');
                inputElement.value = oldName;
            });
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>🎬 Plex Playlist Synchronizer</h1>
        <div class="caption">Accessible via Port {{ port }} | Click on any playlist text name to edit it live</div>

        {% if error_msg %}
            <div class="alert">⚠️ {{ error_msg }}</div>
        {% endif %}

        <div class="grid">
            <div class="panel">
                <h3>👈 Left Server Selection</h3>
                <form method="GET" action="/">
                    <input type="hidden" name="right" value="{{ right_name }}">
                    <select name="left" onchange="this.form.submit()">
                        {% for name in server_options %}
                            <option value="{{ name }}" {% if name == left_name %}selected{% endif %}>{{ name }}</option>
                        {% endfor %}
                    </select>
                </form>

                {% if left_error %}
                    <div style="color: #cf6679; font-weight: bold;">⚠️ Error: {{ left_error }}</div>
                {% elif not left_playlists %}
                    <div class="no-playlists">No playlists found on this server.</div>
                {% else %}
                    {% for pl in left_playlists %}
                        <div class="playlist-item">
                            <div class="playlist-name-container">
                                🎵 <input type="text" class="playlist-input" value="{{ pl.title }}"
                                           onblur="renamePlaylist(this, '{{ left_name }}', '{{ pl.title|replace("'", "\\'") }}')"
                                           onkeypress="if(event.which == 13) this.blur();">
                                {% if pl.smart %}<span class="smart-badge">SMART</span>{% endif %}
                            </div>
                            <a href="/sync?source={{ left_name }}&target={{ right_name }}&playlist={{ pl.title }}&left={{ left_name }}&right={{ right_name }}" class="sync-btn">Sync ➡️</a>
                        </div>
                    {% endfor %}
                {% endif %}
            </div>

            <div class="panel">
                <h3>👉 Right Server Selection</h3>
                <form method="GET" action="/">
                    <input type="hidden" name="left" value="{{ left_name }}">
                    <select name="right" onchange="this.form.submit()">
                        {% for name in server_options %}
                            <option value="{{ name }}" {% if name == right_name %}selected{% endif %}>{{ name }}</option>
                        {% endfor %}
                    </select>
                </form>

                {% if right_error %}
                    <div style="color: #cf6679; font-weight: bold;">⚠️ Error: {{ right_error }}</div>
                {% elif not right_playlists %}
                    <div class="no-playlists">No playlists found on this server.</div>
                {% else %}
                    {% for pl in right_playlists %}
                        <div class="playlist-item">
                            <a href="/sync?source={{ right_name }}&target={{ left_name }}&playlist={{ pl.title }}&left={{ left_name }}&right={{ right_name }}" class="sync-btn">⬅️ Sync</a>
                            <div class="playlist-name-container" style="margin-right: 0; margin-left: 15px;">
                                {% if pl.smart %}<span class="smart-badge" style="margin-left: 0; margin-right: 6px;">SMART</span>{% endif %}
                                <input type="text" class="playlist-input" value="{{ pl.title }}"
                                       onblur="renamePlaylist(this, '{{ right_name }}', '{{ pl.title|replace("'", "\\'") }}')"
                                       onkeypress="if(event.which == 13) this.blur();" style="text-align: right;"> 🎵
                            </div>
                        </div>
                    {% endfor %}
                {% endif %}
            </div>
        </div>
    </div>
</body>
</html>
"""

# ---------------------------------------------------------
# APPLICATION ROUTING & BUSINESS LOGIC
# ---------------------------------------------------------
@app.route("/")
def index():
    server_options = list(SERVERS_CONFIG.keys())

    left_name = request.args.get("left", server_options[0])
    right_name = request.args.get("right", server_options[1] if len(server_options) > 1 else server_options[0])
    global_error = request.args.get("error")

    left_playlists, left_error = [], None
    right_playlists, right_error = [], None

    left_plex, err_a = get_plex_client(left_name)
    if err_a: left_error = err_a
    else:
        try:
            left_playlists = [{"title": pl.title, "smart": pl.smart} for pl in left_plex.playlists()]
        except Exception as e: left_error = str(e)

    right_plex, err_b = get_plex_client(right_name)
    if err_b: right_error = err_b
    else:
        try:
            right_playlists = [{"title": pl.title, "smart": pl.smart} for pl in right_plex.playlists()]
        except Exception as e: right_error = str(e)

    return render_template_string(
        HTML_TEMPLATE,
        port=WEB_PORT,
        server_options=server_options,
        left_name=left_name,
        right_name=right_name,
        left_playlists=left_playlists,
        right_playlists=right_playlists,
        left_error=left_error,
        right_error=right_error,
        error_msg=global_error
    )


@app.route("/rename", methods=["POST"])
def rename():
    server_name = request.form.get("server")
    old_name = request.form.get("old_name")
    new_name = request.form.get("new_name")

    plex, err = get_plex_client(server_name)
    if err:
        return jsonify({"success": False, "error": f"Connection lost: {err}"})

    try:
        print(f"✏️ RENAME REQUEST: Modifying '{old_name}' ➡️ '{new_name}' on {server_name}")
        playlist = plex.playlist(old_name)
        playlist.edit(title=new_name)
        print("   Success!")
        return jsonify({"success": True})
    except Exception as e:
        print(f"💥 Rename action failed: {str(e)}")
        return jsonify({"success": False, "error": str(e)})


@app.route("/sync")
def sync():
    source_name = request.args.get("source")
    target_name = request.args.get("target")
    playlist_name = request.args.get("playlist")

    orig_left = request.args.get("left")
    orig_right = request.args.get("right")

    source_plex, _ = get_plex_client(source_name)
    target_plex, _ = get_plex_client(target_name)

    if not source_plex or not target_plex:
        return redirect(url_for("index", left=orig_left, right=orig_right, error="One of the chosen target servers is unreachable."))

    try:
        print(f"\n===== STARTING SYNC: '{playlist_name}' [{source_name} ➡️ {target_name}] =====")

        source_pl = source_plex.playlist(playlist_name)

        try:
            print(f"🗑️ Cleaning up any pre-existing playlist named '{playlist_name}' on target...")
            target_plex.playlist(playlist_name).delete()
            print("   Old version wiped.")
        except plexapi.exceptions.NotFound:
            print("   No pre-existing playlist found on target. Proceeding.")

        # --- SMART PLAYLIST HANDLER ---
        if source_pl.smart:
            print("🧠 Smart playlist detected. Extracting filter configuration rules...")

            source_section = source_pl.section()
            if not source_section:
                raise Exception("Could not find the original library section driving this smart playlist ruleset.")

            target_section = None
            for section in target_plex.library.sections():
                if section.type == source_section.type:
                    target_section = section
                    break

            if not target_section:
                raise Exception(f"Destination server is missing a matching library section type: '{source_section.type}'")

            raw_payload = source_pl.filters()
            actual_filters = raw_payload.get('filters', {})
            raw_sort = raw_payload.get('sort')
            smart_sort = raw_sort[0] if isinstance(raw_sort, list) and len(raw_sort) > 0 else raw_sort

            smart_type = raw_payload.get('libtype')
            if not smart_type or smart_type == 'video':
                smart_type = 'show' if target_section.type == 'show' else 'movie'

            print(f"📁 Processing Rule Segments:")
            print(f"   -> Pure Filters: {actual_filters}")
            print(f"   -> Extracted Sort: {smart_sort}")
            print(f"   -> Validated Type: {smart_type}")
            print(f"🏗️ Deploying smart definition to target library block: '{target_section.title}'")

            target_section.createPlaylist(
                title=playlist_name,
                smart=True,
                libtype=smart_type,
                sort=smart_sort,
                filters=actual_filters
            )
            print("🎉 SUCCESS: Smart playlist rules generated perfectly on target server!")
            return redirect(url_for("index", left=orig_left, right=orig_right))

        # --- STATIC PLAYLIST HANDLER ---
        else:
            print("📋 Static playlist detected. Synchronizing individual tracked titles...")
            source_items = source_pl.items()
            target_items = []
            missing_titles = []

            for item in source_items:
                libtype = item.type if hasattr(item, 'type') else None
                search_results = target_plex.library.search(title=item.title, libtype=libtype)

                if search_results:
                    matched_item = search_results[0]
                    target_items.append(matched_item)
                else:
                    missing_titles.append(item.title)

            if not target_items:
                error_msg = f"Sync aborted: 0 out of {len(source_items)} items could be located on {target_name}."
                return redirect(url_for("index", left=orig_left, right=orig_right, error=error_msg))

            target_plex.createPlaylist(playlist_name, items=target_items)
            print("🎉 SUCCESS: Static playlist built perfectly on target!")

            if missing_titles:
                warn_msg = f"Synced {len(target_items)} items. Missing items skipped: {', '.join(missing_titles[:3])}..."
                return redirect(url_for("index", left=orig_left, right=orig_right, error=warn_msg))

            return redirect(url_for("index", left=orig_left, right=orig_right))

    except Exception as e:
        print(f"💥 CRITICAL SYNC EXCEPTION: {str(e)}")
        return redirect(url_for("index", left=orig_left, right=orig_right, error=f"Sync Execution Failure: {str(e)}"))


if __name__ == "__main__":
    print(f"🎬 Plex Playlist Sync starting on http://localhost:{WEB_PORT}")
    print(f"   Loaded {len(SERVERS_CONFIG)} server(s): {', '.join(SERVERS_CONFIG.keys())}")
    app.run(host=HOST, port=WEB_PORT, debug=DEBUG)
