import json
import os

INPUT_FILE = "channels.json"
OUTPUT_FILE = "channels.m3u"

BASE_URL = "http://233d3515.kazmazpaz.ru/iptv"
TOKEN = os.environ.get("IPTV_TOKEN")

if not TOKEN:
    raise RuntimeError("IPTV_TOKEN environment variable is not set.")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Normalize input: supports both dict {"101": "HBO"} and list ["101", 102]
channel_map = {}

if isinstance(raw_data, dict):
    for ch_id, ch_name in raw_data.items():
        channel_map[int(ch_id)] = str(ch_name).strip()
elif isinstance(raw_data, list):
    for ch_id in raw_data:
        channel_map[int(ch_id)] = ""
else:
    raise ValueError("channels.json must contain either a JSON list or dictionary.")

# Sort numerically by Channel ID
sorted_channel_ids = sorted(channel_map.keys())

with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
    f.write("#EXTM3U\n\n")

    for ch_id in sorted_channel_ids:
        ch_id_str = str(ch_id)
        raw_name = channel_map[ch_id]

        # Use the custom name if present, otherwise fallback to "Channel <ID>"
        display_name = raw_name if raw_name else f"Channel {ch_id_str}"

        stream_url = f"{BASE_URL}/{TOKEN}/{ch_id_str}/manifest.m3u8"

        # The display name appears after the comma in the #EXTINF line
        f.write(
            f'#EXTINF:-1 tvg-id="{ch_id_str}" tvg-name="{display_name}" '
            f'group-title="Live",{display_name}\n'
        )
        f.write(f"{stream_url}\n\n")

print("=" * 50)
print("M3U CREATED")
print("=" * 50)
print(f"Channels : {len(sorted_channel_ids)}")
print(f"Output   : {OUTPUT_FILE}")
print("=" * 50)
