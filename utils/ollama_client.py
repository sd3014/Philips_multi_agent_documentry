import requests


def ask_ollama(prompt, model="mistral"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()

        # Debug output (very helpful)
        print("OLLAMA RESPONSE:", data)

        # Safe return
        if "response" in data:
            return data["response"]

        elif "error" in data:
            return f"Ollama Error: {data['error']}"

        else:
            return f"Unexpected Response: {data}"

    except Exception as e:
        return f"Exception occurred: {str(e)}"