import os
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import json
import time
from typing import Dict, List
import datetime

def generate_script(client: OpenAI, trend_data: Dict) -> str:

    """Generate a video script using GPT-4 based on trend data"""
    
    prompt = f"""Create a short, engaging 30-second video script about this trending business/finance topic:
    Topic: {trend_data['keyword']}
    Search Volume: {trend_data['volume']}
    Growth: {trend_data['volume_growth_pct']}%
    Related Keywords: {', '.join(trend_data['keywords'])}
    
    The script should:
    1. Be informative and factual
    2. Include key statistics and growth metrics
    3. Be suitable for a business audience
    4. End with a clear takeaway or insight
    
    Format the response as a natural, conversational script."""

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

def generate_sora_prompts(client: OpenAI, script: str) -> List[str]:
    """Generate Sora-compatible video prompts based on the script"""
    
    prompt = f"""Break down this script into 6-7 detailed video scene descriptions suitable for AI video generation:
    
    Script: {script}
    
    For each scene:
    1. Describe the visual elements in detail
    2. Focus on business/professional settings
    3. Include camera movements and transitions
    4. Keep each scene description under 250 characters
    
    Format: Return only the numbered list of scene descriptions."""

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Split the response into individual prompts
    scenes = response.choices[0].message.content.split('\n')
    return [scene.strip() for scene in scenes if scene.strip()]

def generate_voice(text: str, voice_id: str, output_format: str = "mp3_44100_128") -> bytes:
    """Generate text-to-speech audio using Eleven Labs"""
    client = ElevenLabs()
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        output_format=output_format,
    )
    play(audio)
    return audio

def generate_assets(trend_data: Dict, openai_api_key: str, elevenlabs_api_key: str, voice_id: str, run_dir: str) -> Dict:
    """Main function to generate all assets for a trending topic"""

    
    output_dir = run_dir + f'/{trend_data['keyword']}'
    os.makedirs(output_dir, exist_ok=True)

    # Setup
    client = OpenAI(api_key=openai_api_key)
    topic_dir = os.path.join(output_dir, trend_data['keyword'].replace(" ", "_"))
    os.makedirs(topic_dir, exist_ok=True)
    
    script = generate_script(client, trend_data) # Generate script
    sora_prompts = generate_sora_prompts(client, script) # Generate Sora prompts
    audio = generate_voice(script, voice_id) # Generate voice over
    
    # Save assets
    script_path = os.path.join(topic_dir, "script.txt")
    prompts_path = os.path.join(topic_dir, "sora_prompts.json")
    audio_path = os.path.join(topic_dir, "voiceover.mp3")
    
    with open(script_path, "w") as f:
        f.write(script)
        
    with open(prompts_path, "w") as f:
        json.dump(sora_prompts, f, indent=2)
        
    save(audio, audio_path)
    
    return {
        "topic": trend_data['keyword'],
        "script_path": script_path,
        "prompts_path": prompts_path,
        "audio_path": audio_path,
        "script": script,
        "sora_prompts": sora_prompts
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