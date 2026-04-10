import requests

SOURCE = "http://filex.homes/get.php?username=1month&password=1month&type=m3u_plus"
PROXY = "https://sdtv-proxy.onrender.com"

res = requests.get(SOURCE)
lines = res.text.splitlines()

clean = ["#EXTM3U"]

for i in range(len(lines)):
    if lines[i].startswith("#EXTINF"):
        name = lines[i].split(",")[-1]
        stream = lines[i+1]

        # 🔥 IMPORTANT CHANGE
        proxy_stream = f"{PROXY}/m3u8?url={stream}"

        clean.append(f'#EXTINF:-1,{name}')
        clean.append(proxy_stream)

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(clean))

print("✅ FINAL WORKING M3U READY")
