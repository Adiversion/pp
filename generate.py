import json
import os

CHANNELS_FILE = "channels.json"
NAMES_FILE = "names.json"
OUTPUT_FILE = "channels.m3u"

BASE_URL = "http://233d3515.kazmazpaz.ru/iptv"
TOKEN = os.environ.get("IPTV_TOKEN")

if not TOKEN:
    raise RuntimeError("IPTV_TOKEN environment variable is not set.")

# 1. Load channel IDs from channels.json
if not os.path.exists(CHANNELS_FILE):
    raise FileNotFoundError(f"Missing {CHANNELS_FILE}. Please ensure it is present in the repository.")

with open(CHANNELS_FILE, "r", encoding="utf-8") as f:
    raw_channels = json.load(f)

# Deduplicate and sort numerically
channel_ids = sorted(set(int(ch_id) for ch_id in raw_channels))

# 2. Load names mapping from names.json (if available)
names_map = {}
if os.path.exists(NAMES_FILE):
    with open(NAMES_FILE, "r", encoding="utf-8") as f:
        raw_names = json.load(f)
        # Normalize keys as strings
        names_map = {str(k).strip(): str(v).strip() for k, v in raw_names.items()}

# 3. Generate M3U Playlist formatted for OTT Navigator
with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
    f.write('#EXTM3U\n\n')

    named_count = 0
    for ch_id in channel_ids:
        ch_str = str(ch_id)

        # Lookup scraped name, fallback to "Channel <ID>" if not mapped
        channel_name = names_map.get(ch_str)
        if channel_name:
            named_count += 1
        else:
            channel_name = f"Channel {ch_str}"

        stream_url = f"{BASE_URL}/{TOKEN}/{ch_str}/manifest.m3u8"

        # EXTINF attributes:
        # - tvg-id: channel ID for EPG guide matching
        # - tvg-name: explicit channel name for metadata search
        # - tvg-chno: remote channel keypad number
        # - group-title: default category grouping
        f.write(
            f'#EXTINF:-1 tvg-id="{ch_str}" tvg-name="{channel_name}" '
            f'tvg-chno="{ch_str}" group-title="Live",{channel_name}\n'
        )
        f.write(f"{stream_url}\n\n")

print("=" * 50)
print("PLAYLIST CREATED SUCCESSFULLY")
print("=" * 50)
print(f"Total Channels : {len(channel_ids)}")
print(f"Named Channels : {named_count}")
print(f"Unnamed (ID)   : {len(channel_ids) - named_count}")
print(f"Output File    : {OUTPUT_FILE}")
print("=" * 50)
