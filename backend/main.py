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
# genai.configure(api_key=API_KEY)
client = genai.Client(api_key=API_KEY)

app = FastAPI()

# Allow CORS from all origins (adjust in production to your frontend domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

# Instantiate a GenerativeModel from genai
# model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')

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
Given the concept: "{idea}"
Return exactly {count} opposite-end word pairs suitable for a Wavelength spectrum, be creative and fun/funny.
Each pair must be a JSON object with keys "left" and "right".
Output a JSON array of length {count}, for example:

[
  {{"left":"Hot","right":"Cold"}},
  {{"left":"Joy","right":"Sadness"}},
  ...
]

Do not include any extra text or commentary—only the JSON array.
""".strip()
    
    # generation_config = types.GenerateContentConfig(
    #     max_output_tokens=1024,
    #     temperature=1.25
    # )
        
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-05-20",
            contents=prompt_text,
            config=types.GenerateContentConfig(
                max_output_tokens=1024,
                temperature=1.25
            )
        )

        # response = client.models.generate_content(
        # model="gemini-2.5-flash-preview-05-20", contents=prompt_text,
        # generation_config=generation_config
        # )
        
        # response = model.generate_content(
        #     contents=prompt_text,
        #     generation_config=generation_config
        # )
        generated = response.text

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
