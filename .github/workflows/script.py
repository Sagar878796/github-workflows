import requests
import os

PORTAL = "https://jiotv.be/stalker_portal/c/"
MAC = "00:1A:79:C2:F0:E3"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": f"mac={MAC}; stb_lang=en; timezone=Asia/Kolkata;"
}

def get_token():
    url = PORTAL.replace("/c/", "/server/load.php?type=stb&action=handshake&JsHttpRequest=1-xml")
    res = requests.get(url, headers=HEADERS)
    return res.json()["js"]["token"]

def get_channels(token):
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {token}"

    url = PORTAL.replace("/c/", "/server/load.php?type=itv&action=get_all_channels&JsHttpRequest=1-xml")
    res = requests.get(url, headers=headers)
    return res.json()["js"]["data"]

def generate_m3u(channels):
    m3u = "#EXTM3U\n"
    for ch in channels:
        name = ch.get("name")
        cmd = ch.get("cmd")
        if "http" in cmd:
            stream = cmd.split(" ")[-1]
            m3u += f'#EXTINF:-1,{name}\n{stream}\n'
    return m3u

def def save_playlist(content):
    os.makedirs("Playlist", exist_ok=True)
    with open("Playlist/Star.m3u", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    token = get_token()
    channels = get_channels(token)
    playlist = generate_m3u(channels)
    save_playlist(playlist)
    print("Playlist Generated ✅")
