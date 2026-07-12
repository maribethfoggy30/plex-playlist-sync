# Changelog

All notable changes to this project are documented here.

## [1.0.0] — 2026-07-12

Initial public release.

### Features
- Side-by-side view of playlists on two Plex servers at once.
- One-click sync of a playlist from one server to another.
- Full support for **smart playlists** — the filter rules are recreated on the
  target server, not just the current items.
- Support for **static playlists** — items are matched by title on the target
  library, with a clear report of any titles that couldn't be found.
- Inline playlist renaming — click a name, type, and it saves to Plex live.
- Configurable for any number of Plex servers.
- Dark-mode web interface with Safari/WebKit alignment fixes.

### Configuration
- All settings (servers, tokens, port) now load from a private `.env` file.
- Debug mode defaults to off for safer operation on a network.
