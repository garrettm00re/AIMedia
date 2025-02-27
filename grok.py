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
        self.data = {
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a creative genius, designed to assist the user with whatever they ask."
                },
                {
                    "role": "user",
                    "content": ""
                }
            ],
            "model": model,
            "stream": stream,
            "temperature": temperature
        } 
    def generate_text(self, prompt, return_json=False):
        self.data["messages"][1]["content"] = prompt
        response = requests.post(self.url, headers=self.headers, json=self.data)
        if return_json:
            return response.json()
        else:
            return response.json()['choices'][0]['message']['content']

