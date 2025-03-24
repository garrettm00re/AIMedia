from grok import Grok

def generate_script_grok(client: Grok, trend_data: dict, news_report: str) -> str:

    """Generate a video script using Grok based on trend data"""
    
    prompt = f"""Create a short, video script about this trending topic:
    Topic: {trend_data['keyword']}
    Related Keywords: {', '.join(trend_data['keywords'])}
    News Report: {news_report}
    
    The script must be:
    1. Informative and accurate
    2. Focused on the most important and sensational aspects of the story
    3. Conversational and concise.
    4. Written with charged language and emotional appeals.
    5. Quick to the point, no fluff.
    6. Between 60 and 80 words in length.

    The script must NOT:
    1. Contain an outro of any kind, or mention subscribing to the channel
    2. Use acronyms or abbreviations without explanation
    3. Contain any headers, formatting, directions for the video, or other instructions.

    End the script with a uniqueand engaging question.
    """
    return client.generate_text(prompt)

def generate_sora_prompts_grok(client: Grok, script: str, num_prompts: int = 1) -> list[str]:
    """Generate Sora-compatible video prompts based on the script"""

    soraScripts = []
    prompt = f"""Break down this script into a series of four video scene descriptions suitable for AI video generation:
    
    Script: {script}
    
    There should be four scenes.

    For each scene:
    
    1. Describe the visual elements in detail
    2. Include camera movements and transitions
    3. Be concise -- under 25 words.
    4. Use loose, conversational language in your description.
    5. Format the scene description as follows:
        [Scene Title] <= 5 words
        [Scene Description] <= 25 words
        [Camera Movements/Transitions] <= 25 words
        newline

    Do NOT:
    1. Generate a scene for an outro
    2. Use acronyms or abbreviations without explanation
    3. Use the newline character, never the word "newline"
    """
    
    for i in range(num_prompts):
        soraScript = client.generate_text(prompt)
        soraScripts.append(soraScript)
    return soraScripts

def generate_sora_prompts_grokV2(client: Grok, script: str, num_prompts: int = 1) -> list[str]:
    """Generate Sora-compatible video prompts based on the script"""

    soraScripts = []
    prompt = f"""Break down this script into a series of four video scene descriptions suitable for AI video generation:
    
    Script: {script}
    
    There should be five scenes.

    For each scene:
    
    1. Describe the visual elements in detail
    2. Include camera movements and transitions
    3. Be concise -- under 25 words.
    4. Use loose, conversational language in your description.
    5. Scene descriptions should tell a story. Ensure that it can be told in ten seconds or less.
    6. Format the scene description as follows:
        [Scene Title] <= 5 words
        [Scene Description] <= 25 words
        [Camera Movements/Transitions] <= 25 words
        newline

    Do NOT:
    1. Generate a scene for an outro
    2. Use acronyms or abbreviations without explanation
    """
    
    for i in range(num_prompts):
        soraScript = client.generate_text(prompt)
        soraScripts.append(soraScript)
    return soraScripts

def generate_sora_prompts_grokV3(client: Grok, script: str, num_prompts: int = 1, temp = 1.6) -> list[str]:
    """Generate Sora-compatible video prompts based on the script"""

    soraPrompts = []
    prompt = f"""Break down this script into a series of five video scene descriptions suitable for AI video generation:
    
    Script: {script}
    
    There should be four scenes.

    For each scene:
    
    1. Determine the most sensational aspect of the corresponding portion of the script. Capture it with a creative idea described vividly.
    2. Include camera movements and transitions
    3. Be concise -- under 25 words.
    4. Use loose, conversational language in your description.
    5. Format the scene description as follows:
        [Scene Title] <= 5 words
        [Scene Description] <= 25 words
        [Camera Movements/Transitions] <= 25 words
        newline

    Do NOT:
    1. Generate a scene for an outro
    2. Use acronyms or abbreviations without explanation
    3. Use the word "newline". Always use the newline character.
    4. Use people's names. Instead, describe the person in detail.
    """
    
    for i in range(num_prompts):
        soraPrompt = client.generate_text(prompt, temperature=temp)
        print(soraPrompt)
        soraPrompts.append(soraPrompt)
    return soraPrompts

def makeHook(client: Grok, script, audience, temp = 1.6):
    prompt = f"""Generate a short (< 10 words) hook that introduces the following video script. 

    The hook must:
    1. Directly engage the audience, {audience}, with a statement.
    2. Be < 10 words.
    3. Use dramatic language
    4. Capture the most essential themes from the script

    Use a confident tone. DO NOT use a ? anywhere.

    script: {script}
    """
    return client.generate_text(prompt, temperature=temp)

def finalScript(client: Grok, script, hook, temp = 0):
    prompt = f"""Prepend the hook to the script, and make sure it melds well. Do not change the hook.
    
    script: {script}
    hook: {hook}
    """
    return client.generate_text(prompt, temperature=temp)

def generate_grok_image_prompts(client: Grok, script: str, num_prompts: int = 10) -> list[str]:
    """Generate Grok image prompts based on the script"""

    prompt = f"""Generate a series of (~{int}) image descriptions that capture the most sensational themes of the following script.

    For each image:
    1. Be assertive and highly creative in your description. 
    2. Be clear and concise. 
    3. Use familiar elements of popular culture where appropriate e.g. brands, celebrities, landmarks, products, etc.

    Each image prompt should have the following format:
    Generate an image of [description]

    Separate each image prompt with a newline.
    
    Script: {script}
    """
    return client.generate_text(prompt)

def generate_grok_narration(client: Grok, script: str) -> str:
    """Generate a narration using Grok based on the script"""

    prompt = f"""Extract only the words to be spoken from this video script:
    Script: {script}.

    The result should NOT include any mention of a narrator or scene descriptions.
    """
    return client.generate_text(prompt)

def generate_hashtags(client: Grok, script: str) -> list[str]:
    """Generate hashtags using Grok based on the script"""

    prompt = f"""Generate the best series of hashtags to make this video go viral on instagram reels, tik tok, and youtube shorts.
    Select the best 10 hashtags and brief reasoning for each.

    The result should be in the following format:
    for each hashtag:
        [Hashtag] [Reasoning]

    Include a one-line space separated list of all hashtags at the end.

    Script: {script}"""
    return client.generate_text(prompt)

def generate_grok_opinion_analysis(client: Grok, news_report: str) -> str:
    """Generate an opinion analysis using Grok based on the news report"""

    prompt = f"""Generate an opinion analysis using Grok based on the news report:
    News Report: {news_report}

    The opinion analysis should:
    1. Be highly engaging and bold.
    2. Provide evidence based reasoning for claims made. 
    3. Be less than 500 words in length.
    4. Be written in a professional tone.

    The opinion analysis should NOT:
    1. Cite sources.

    Format:
    [Title Highlighting the Central Claim] <= 10 words
    [Opinion Analysis] <= 500 words
    """

    return client.generate_text(prompt)