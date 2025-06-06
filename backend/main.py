import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Configure genai with your API key
API_KEY = os.getenv("GENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("Please set GENAI_API_KEY in your environment or .env file")
client = genai.Client(api_key=API_KEY)

app = FastAPI()

# Allow CORS from all origins (adjust in production to your frontend domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

class SpectrumRequest(BaseModel):
    idea: str
    count: int = 30

@app.post("/api/generateSpectrums")
async def generate_spectrums(req: SpectrumRequest):
    idea = req.idea.strip()
    count = req.count

    if not idea:
        raise HTTPException(status_code=400, detail="Missing 'idea'")
    if count < 1 or count > 100:
        raise HTTPException(status_code=400, detail="'count' must be between 1 and 100")

    prompt_text = f"""
        You are generating JSON data for a party game where players guess a hidden point on a spectrum between two opposing **subjective stances**.

        Generate exactly {count} **creative and opinion-based spectrum pairs** inspired by the theme: "{idea}".

        Each pair must:
        - Be **debatable, contextual, or socially subjective**
        - Spark **conversation, disagreement, or laughter**
        - Use **short, punchy phrases or descriptors** (not single adjectives)
        - Avoid boring or universal opposites (like "Good/Bad", "Hot/Cold")
        - Reflect **modern behavior, social norms, internet culture, or generational quirks**
        - Include a mix of **niche** and **broad** spectrums

        Examples of the *style* you should follow:
        - "Would make a good pirate" vs "Would make a bad pirate"
        - "Fboy" vs "Husband"
        - "Culturally significant" vs "Culturally insignificant"
        - "Definitely ironic" vs "Completely sincere"

        Format your output as **valid JSON only**:
        An array of {count} objects, each with a "left" and "right" key, like this:

        [
        {{"left": "Cringe fashion choice", "right": "Sick fashion statement"}},
        {{"left": "Underrated opinion", "right": "Overrated opinion"}},
        ...
        ]
        """
        
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt_text,
            config=types.GenerateContentConfig(
                temperature=1.3
            )
        )
        
        if response.candidates and len(response.candidates) > 0:
            if response.candidates[0].content and response.candidates[0].content.parts:
                generated = response.candidates[0].content.parts[0].text
                # Debug - print raw response
                print("Raw response from API:", repr(generated))
                
                # Remove any markdown code block syntax if present
                if generated.startswith("```json"):
                    generated = generated.split("```json", 1)[1]
                if generated.startswith("```"):
                    generated = generated.split("```", 1)[1]
                if generated.endswith("```"):
                    generated = generated.rsplit("```", 1)[0]
                    
                # Strip whitespace
                generated = generated.strip()
                
                print("Processed response:", repr(generated))
                
                if not generated:
                    raise ValueError("Empty response after processing")
            else:
                raise ValueError("No text content in response")
        else:
            raise ValueError("No candidates in response")

        spectrums = json.loads(generated)
        if (
            not isinstance(spectrums, list)
            or len(spectrums) < count
            or any(
                not isinstance(p, dict)
                or "left" not in p
                or "right" not in p
                or not isinstance(p["left"], str)
                or not isinstance(p["right"], str)
                for p in spectrums
            )
        ):
            raise ValueError("Parsed JSON invalid or too few pairs")
    except Exception as e:
        print("Error generating/parsing spectrums:", e)
        raise HTTPException(status_code=500, detail="Failed to generate spectrums")

    # Return exactly `count` pairs (truncate if Gemini returned extras)
    return {
        "spectrums": [
            [p["left"].strip(), p["right"].strip()] 
            for p in spectrums[:count]
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")
