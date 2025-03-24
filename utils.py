from googlenewsdecoder import gnewsdecoder # I have no idea how this works, but it works
import os
from dotenv import load_dotenv
load_dotenv()

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

def most_recent_dir():
    # List directories in assets and get most recent
    os.chdir(os.getenv("APPDIR"))
    asset_dirs = [d for d in os.listdir('assets') if os.path.isdir(os.path.join('assets', d))]
    RUN_DIR = os.path.join('assets', max(asset_dirs))
    return RUN_DIR

def get_main_dir():
    RUN_DIR = most_recent_dir()
    MAIN = [os.path.join(RUN_DIR, d) for d in os.listdir(RUN_DIR) if os.path.isdir(os.path.join(RUN_DIR, d))][0] # only one directory in the RUN_DIR
    return MAIN

def get_grok_dir():
    MAIN = get_main_dir()
    return os.path.join(MAIN, 'grok')

def get_keyword():
    MAIN = get_main_dir()
    return MAIN.split('\\')[-1].replace('_', ' ')

# return contents of files

def get_news_report():
    MAIN = get_main_dir()
    with open(os.path.join(MAIN, 'news_report.txt'), 'r') as f:
        return f.read()

def get_soraprompts():
    MAIN = get_main_dir()
    with open(os.path.join(MAIN, 'soraprompts.txt'), 'r') as f:
        return f.read()

def get_sora_script():
    MAIN = get_main_dir()
    with open(os.path.join(MAIN, 'script.txt'), 'r') as f:
        return f.read()

def get_grok_script():
    GROK_DIR = get_grok_dir()
    with open(os.path.join(GROK_DIR, 'grok_script.txt'), 'r') as f:
        return f.read()
