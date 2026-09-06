import json
import os
import urllib.request
from datetime import datetime, timezone

repo_name = os.environ["REPO_NAME"]
repo_url = os.environ["REPO_URL"]
branch = os.environ["BRANCH"]
actor = os.environ["ACTOR"]
commit_url = os.environ["COMMIT_URL"]
webhook = os.environ["WEBHOOK_URL"]

commit_lines = []
with open("commits.txt", encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line:
            continue
        parts = line.split("|", 2)
        if len(parts) != 3:
            continue
        short_sha, subject, author = parts
        commit_lines.append(f"[`{short_sha}`]({repo_url}/commit/{short_sha}) {subject} — *{author}*")
commits_text = "\n".join(commit_lines) or "(sin commits nuevos)"

with open("diffstat.txt", encoding="utf-8") as f:
    diffstat_text = f.read().strip() or "(sin diff disponible)"

embed = {
    "author": {
        "name": actor,
        "url": f"https://github.com/{actor}",
        "icon_url": f"https://github.com/{actor}.png"
    },
    "title": f"📦 {repo_name} · {branch}",
    "url": commit_url,
    "color": 0xFF5F1F,
    "fields": [
        {"name": "Commits", "value": commits_text[:1024], "inline": False},
        {"name": "Archivos", "value": f"```\n{diffstat_text[:900]}\n```", "inline": False}
    ],
    "footer": {"text": repo_name, "icon_url": "https://github.githubassets.com/favicons/favicon.png"},
    "timestamp": datetime.now(timezone.utc).isoformat()
}
payload = json.dumps({"embeds": [embed]}).encode("utf-8")

req = urllib.request.Request(
    webhook,
    data=payload,
    headers={
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (compatible; DiscordChangelogBot/1.0)"
    }
)
urllib.request.urlopen(req)
