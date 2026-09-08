import json
import os


# ============================================================
# CONFIG
# ============================================================

BASE_URL = "http://233d3515.kazmazpaz.ru/iptv"

INPUT_FILE = "channels.json"
OUTPUT_FILE = "channels.m3u"

GROUP = "Live"


# ============================================================
# LOAD TOKEN
# ============================================================

TOKEN = os.environ.get("IPTV_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "IPTV_TOKEN environment variable is missing."
    )


# ============================================================
# LOAD CHANNEL IDS
# ============================================================

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    channel_ids = json.load(f)


# Remove duplicates and sort
channel_ids = sorted(
    set(int(channel_id) for channel_id in channel_ids)
)


# ============================================================
# GENERATE M3U
# ============================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8",
    newline="\n"
) as f:

    f.write("#EXTM3U\n\n")

    for index, channel_id in enumerate(
        channel_ids,
        start=1
    ):

        channel_name = f"Channel {index}"

        stream_url = (
            f"{BASE_URL}/"
            f"{TOKEN}/"
            f"{channel_id}/"
            f"manifest.m3u8"
        )

        f.write(
            f'#EXTINF:-1 '
            f'tvg-id="Channel{index}" '
            f'group-title="{GROUP}", '
            f'{channel_name}\n'
        )

        f.write(
            f'{stream_url}\n\n'
        )


print(
    f"Generated {len(channel_ids)} channels "
    f"into {OUTPUT_FILE}"
)
