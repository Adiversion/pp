import json
import os

INPUT_FILE = "channels.json"
OUTPUT_FILE = "channels.m3u"

BASE_URL = "http://233d3515.kazmazpaz.ru/iptv"
TOKEN = os.environ.get("IPTV_TOKEN")

if not TOKEN:
    raise RuntimeError("IPTV_TOKEN environment variable is not set.")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    channels = json.load(f)

# Remove duplicates and sort numerically
channels = sorted(set(int(channel_id) for channel_id in channels))

with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
    f.write("#EXTM3U\n\n")

    for channel_id in channels:
        channel_id = str(channel_id)

        stream_url = (
            f"{BASE_URL}/{TOKEN}/{channel_id}/manifest.m3u8"
        )

        f.write(
            f'#EXTINF:-1 tvg-id="{channel_id}" '
            f'group-title="Live", {channel_id}\n'
        )
        f.write(f"{stream_url}\n\n")

print("=" * 50)
print("M3U CREATED")
print("=" * 50)
print(f"Channels : {len(channels)}")
print(f"Output   : {OUTPUT_FILE}")
print("=" * 50)
