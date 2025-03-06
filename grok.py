import requests

class Grok:
    def __init__(self, api_key, url, model, stream=False, temperature=0):
        self.api_key = api_key
        self.url = url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        self.model = model
        self.stream = stream
        self.temperature = temperature
        self.data = lambda prompt, temperature: {
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a creative genius, designed to assist the user with whatever they ask."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": self.model,
            "stream": self.stream,
            "temperature": self.temperature if temperature is None else temperature
        }

    def generate_text(self, prompt, temperature=None, return_json=False):
        response = requests.post(self.url, headers=self.headers, json=self.data(prompt, temperature))
        if return_json:
            return response.json()
        else:
            return response.json()['choices'][0]['message']['content']

