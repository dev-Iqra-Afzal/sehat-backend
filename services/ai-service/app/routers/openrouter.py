import requests
# from app.core.config import OPENROUTER_API_KEY

# def ask_openrouter(prompt: str) -> str:
#     url = "https://openrouter.ai/api/v1/chat/completions"
#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     data = {
#         "model": "openai/gpt-3.5-turbo",  # You can change model if needed
#         "messages": [
#             {"role": "user", "content": prompt}
#         ]
#     }

#     try:
#         response = requests.post(url, headers=headers, json=data)
#         response.raise_for_status()
#         return response.json()["choices"][0]["message"]["content"]
#     except Exception as e:
#         return f"Error from OpenRouter: {e}"

# import google.generativeai as genai

# # Your Gemini API Key
# from app.core.config import GEMINI_API_KEY

# # Configure the API
# genai.configure(api_key=GEMINI_API_KEY)

# def ask_gemini(prompt: str) -> str:
#     try:
#         # Choose the model: "gemini-1.5-flash" (fast) or "gemini-1.5-pro" (more capable)
#         model = genai.GenerativeModel("gemini-1.5-flash")
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         return f"Error from Gemini: {e}"

# if __name__ == "__main__":
#     print(ask_gemini("Explain quantum computing in simple terms"))

# from app.core.config import DEEPINFRA_API_KEY

# def ask_deepinfra(prompt):
#     url = "https://api.deepinfra.com/v1/openai/chat/completions"
#     headers = {"Authorization": f"Bearer {DEEPINFRA_API_KEY}"}
#     data = {
#         "model": "meta-llama/Meta-Llama-3-8B-Instruct",
#         "messages": [{"role": "user", "content": prompt}]
#     }
#     r = requests.post(url, headers=headers, json=data)
    
#     try:
#         result = r.json()
#     except Exception:
#         raise ValueError(f"Non-JSON response: {r.text}")
    
#     if "choices" not in result:
#         raise ValueError(f"DeepInfra API error: {result}")
    
#     return result["choices"][0]["message"]["content"]

from app.core.config import GROQ_API_KEY

def ask_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    data = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }
    r = requests.post(url, headers=headers, json=data)
    return r.json()["choices"][0]["message"]["content"]

