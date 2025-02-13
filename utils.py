from googlenewsdecoder import gnewsdecoder # I have no idea how this works, but it works

def get_final_url(url):
    print("URL", url)
    if "news.google.com" in url:
        interval_time = 1  # interval is optional, default is None
        try:
            decoded_url = gnewsdecoder(url, interval=interval_time)
            if decoded_url.get("status"):
                return decoded_url["decoded_url"]
            else:
                print("ERROR: COULD NOT DECODE URL")
                return 'ERROR: Could not decode URL'
        except Exception as e:
            print(f"Error occurred: {e}")
            return 'ERROR: Encountered exception and can not decode URL'
    else:
        return url

def saveAudio(audio, path):
    with open(path, "wb") as f:
        for chunk in audio:
            f.write(chunk)
            
def save(fileContents, path):
    if isinstance(fileContents, bytes):
        with open(path, "wb") as f:
            f.write(fileContents)
    else:
        with open(path, "w") as f:
            f.write(fileContents)