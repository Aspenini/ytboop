import sys
import requests
import urllib.parse
import subprocess

def main():
    if len(sys.argv) < 2:
        print("No ytboop:// URL provided.")
        return

    # Launch backend if not already running
    try:
        requests.get("http://localhost:5000")
    except:
        subprocess.Popen(["python", "app.py"], cwd=".")

    parsed = urllib.parse.urlparse(sys.argv[1])
    query = urllib.parse.parse_qs(parsed.query)

    url = query.get("url", [""])[0]
    type_ = query.get("type", [""])[0]
    format_ = query.get("format", [""])[0]

    requests.post("http://localhost:5000/download", data={
        "url": url,
        "type": type_,
        "format": format_
    })

if __name__ == '__main__':
    main()
