import os
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import json
import time
from typing import Dict, List
import datetime
import os
print(os.getcwd())
from utils import save, saveAudio

def getNewsReport(client: OpenAI, trend_data: Dict, news_report_path: str) -> str:
    """Get a news report for a trending topic"""

    prompt = f"""Generate a news report for this trending business/finance topic by synthesizing the following news articles:
    Topic: {trend_data['keyword']}
    Related Keywords: {', '.join(trend_data['keywords'])}
    
    News Articles:
    """
    validArticles = 0
    for newsArticle in trend_data['news']:
        if newsArticle.mainText is not None:
            prompt += f"{newsArticle}\n\n"
            validArticles += 1

    if validArticles == 0:
        return "No valid news articles found"
    else:
        print(validArticles, 'validArticles')
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        newsReport = response.choices[0].message.content
        save(newsReport, news_report_path)
        return newsReport

def generate_script(client: OpenAI, trend_data: Dict, news_report: str, script_path: str) -> str:

    """Generate a video script using GPT-4 based on trend data"""
    
    prompt = f"""Create a short, engaging 30-second video script about this trending business/finance topic:
    Topic: {trend_data['keyword']}
    Related Keywords: {', '.join(trend_data['keywords'])}
    News Report: {news_report}
    
    The script should be:
    1. Informative and factual
    2. Suitable for a business audience
    3. Conversational script.
    4. At most 30 seconds in length."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    script = response.choices[0].message.content
    save(script, script_path)
    return script

def generate_narration(client: OpenAI, script: str, narration_path: str) -> str:
    """Generate a narration using GPT-4 based on the script"""

    prompt = f"""Extract the words to be spoken from this video script:
    Script: {script}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    narration = response.choices[0].message.content
    save(narration, narration_path)
    return narration

def generate_sora_prompts(client: OpenAI, script: str, prompts_path: str, num_prompts: int = 1) -> List[str]:
    """Generate Sora-compatible video prompts based on the script"""

    soraScripts = []
    prompt = f"""Break down this script into a detailed video scene descriptions suitable for AI video generation:
    
    Script: {script}
    
    For each scene:
    1. Describe the visual elements in detail
    2. Focus on business/professional settings
    3. Include camera movements and transitions
    4. Keep each scene description under 400 characters
    
    """
    
    for i in range(num_prompts):
        response = client.chat.completions.create(
            temperature=1.0,
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        filename = os.path.join(prompts_path, "sora_prompt_" + str(i) + ".txt")
        soraScript = response.choices[0].message.content
        save(soraScript, filename)
        soraScripts.append(soraScript)
    return soraScripts


def generate_voice(narration: str, voice_id: str, audio_path: str, output_format: str = "mp3_44100_128") -> bytes:
    """Generate text-to-speech audio using Eleven Labs"""
    client = ElevenLabs()
    print(voice_id, 'voice_id')
    audio = client.text_to_speech.convert(
        text=narration,
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        output_format=output_format,
    )
    saveAudio(audio, audio_path)
    play(audio)

def generate_video(prompt: str, video_path: str) -> None:
    """Generate a video using Sora"""
    client = Sora()
    client.generate_video(prompt, video_path)

def generate_assets(trend_data: Dict, openai_api_key: str, elevenlabs_api_key: str, voice_id: str, run_dir: str) -> Dict:
    """Main function to generate all assets for a trending topic"""

    # Setup
    topic_dir = os.path.join(run_dir, trend_data['keyword'].replace(" ", "_"))
    os.makedirs(topic_dir, exist_ok=True)

    sora_prompt_dir = os.path.join(topic_dir, "sora_prompts")
    os.makedirs(sora_prompt_dir, exist_ok=True)

    print(topic_dir, 'topic_dir')
    print(sora_prompt_dir, 'sora_prompt_dir')
    # Initialize clients
    client = OpenAI(api_key=openai_api_key)


    # Asset save paths
    news_report_path = os.path.join(topic_dir, "news_report.txt")
    script_path = os.path.join(topic_dir, "script.txt")
    audio_path = os.path.join(topic_dir, "voiceover.mp3")
    video_path = os.path.join(topic_dir, "video.mp4")
    narration_path = os.path.join(topic_dir, "narration.txt")
    # Generate assets
    news_report = getNewsReport(client, trend_data, news_report_path)
    script = generate_script(client, trend_data, news_report=news_report, script_path=script_path) # Generate script
    narration = generate_narration(client, script, narration_path) # Generate narration
    sora_prompts = generate_sora_prompts(client, script, sora_prompt_dir) # Generate Sora prompts
    generate_voice(narration = narration, voice_id = voice_id, audio_path = audio_path) # Generate voice over

    for prompt in sora_prompts:
            generate_video(prompt, video_path) # Generate video
    
    return {"paths" : {
        "script": script_path,
        "audio": audio_path,
        "video": video_path,
        "sora_prompts": sora_prompt_dir,
        "news_report": news_report_path
    }
    }

# Example usage:
if __name__ == "__main__":
    # Load environment variables for API keys
    openai_api_key = os.getenv("OPENAI_API_KEY")
    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = os.getenv("ELEVENLABS_VOICE_ID", "default_voice_id")
    
    # Example trend data
    trend_data = {
        "keyword": "Example Trend",
        "volume": 10000,
        "volume_growth_pct": 200,
        "keywords": ["keyword1", "keyword2"]
    }
    
    result = generate_assets(
        trend_data=trend_data,
        openai_api_key=openai_api_key,
        elevenlabs_api_key=elevenlabs_api_key,
        voice_id=voice_id
    ) 