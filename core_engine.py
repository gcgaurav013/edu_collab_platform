import os
from openai import OpenAI
from groq import Groq
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class AIOrchestrator:
    def __init__(self, provider, api_key):
        self.provider = provider
        self.api_key = api_key

    def generate(self, prompt, context=""):
        # Research-oriented system prompt to reduce hallucination
        system_instruction = (
            "You are a PhD-level Educational Assistant. "
            "Use the provided context to fulfill the request. "
            "If the information is not in the context, state that it is not available. "
            "Context:\n"
        )
        full_prompt = f"{system_instruction}{context}\n\nTask: {prompt}"
        
        try:
            if self.provider == "Gemini":
                genai.configure(api_key=self.api_key)
                # Using the latest stable Gemini 1.5 Flash (faster) or Pro
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(full_prompt)
                return response.text

            elif self.provider == "Groq":
                client = Groq(api_key=self.api_key)
                # UPDATED: Using Llama 3.3 70B (Current stable flagship)
                # Alternative: "llama-3.1-8b-instant" for speed
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile", 
                    messages=[{"role": "user", "content": full_prompt}]
                )
                return completion.choices[0].message.content

            elif self.provider == "OpenAI":
                client = OpenAI(api_key=self.api_key)
                # UPDATED: Using GPT-4o (Omni)
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": full_prompt}]
                )
                return response.choices[0].message.content

            elif self.provider == "OpenRouter":
                client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=self.api_key,
                )
                # Using Claude 3.5 Sonnet via OpenRouter
                response = client.chat.completions.create(
                    model="anthropic/claude-3.5-sonnet",
                    messages=[{"role": "user", "content": full_prompt}]
                )
                return response.choices[0].message.content
                
        except Exception as e:
            return f"Error with {self.provider}: {str(e)}"