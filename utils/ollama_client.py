from groq import Groq

# Replace with your actual API key
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)


def ask_ollama(prompt, model="llama-3.3-70b-versatile"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Error: {str(e)}"