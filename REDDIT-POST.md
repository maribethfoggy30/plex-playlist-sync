# Reddit Post (ready to paste)

> **How to use this file:** the actual post is in the grey box below — copy the title and body straight into Reddit. Everything outside the box is just notes for you. When you post, upload the screenshot (`assets/screenshot.png`) as an image, or drop the GitHub link and Reddit will usually preview it.

---

## 📍 Good subreddits to post in
- **r/selfhosted** — probably your best audience; loves free self-hosted tools like this.
- **r/PleX** — the obvious home for it. Check their rules first (see note below).
- **r/homelab** and **r/DataHoarder** — secondary, if the framing fits.
- **r/Python** or **r/flask** — if you want to share it as a coding project rather than a Plex tool.

> ⚠️ **Etiquette heads-up:** some subs (especially r/PleX) have rules about self-promotion — often a "Self-Promo Saturday" thread, or a requirement that it's free/open-source (yours is, so you're fine). Skim the sidebar/rules before posting, and it never hurts to reply to comments and take feedback graciously. Reddit rewards "I built this to scratch my own itch" energy and is allergic to anything that reads like an ad — which is exactly why the post below is low-key.

---

## ✍️ The post

**Title:**
```
I got annoyed that Plex won't let you copy playlists between servers, so I built a little tool that does
```

**Body:**
```
I run a couple of Plex servers — one local, one remote for family — and it's always bugged me that there's no built-in way to move a playlist from one to the other. If you've ever tried, you know smart playlists in particular are a real pain to recreate by hand.

So I put together a small web app to scratch my own itch, and figured a few of you might find it useful too.

You pick two of your servers and their playlists show up side by side. Hit a sync button and it copies a playlist from one to the other. For smart playlists it actually rebuilds the filter rules on the target server (not just a frozen snapshot of the current items), so they stay dynamic. For regular playlists it matches everything by title and tells you if anything couldn't be found on the other server. You can also rename playlists right in the browser, which was another thing that always bugged me.

It's just Python/Flask, runs locally on your own machine, nothing cloud, no accounts. Free and MIT licensed. Setup is basically: download, run the installer, paste in your Plex server addresses + tokens, done. There are double-click install/start scripts for Windows and Mac.

Screenshot below. Link's in the comments / here: [GitHub link]

I'm not a professional dev so go easy on me — but bug reports and ideas are very welcome.
```

---

## 💡 Tips
- Posting the **screenshot** directly (as the image in an image post) tends to get more engagement than a bare link.
- Put the GitHub link **in the post or the first comment** — some subs auto-filter link posts, so a text post + link-in-comment is often safer.
- Skip mentioning the "buy me a coffee" thing in the Reddit post itself — it can rub some communities the wrong way. It's already on the GitHub page, which is the right place for it.
