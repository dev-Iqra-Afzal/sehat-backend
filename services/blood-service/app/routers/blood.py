from fastapi import APIRouter, Request, HTTPException
import httpx
import json
import re

router = APIRouter(prefix="/blood", tags=["Blood"])

@router.get("/{location}")
async def get_blood_sources(
    request: Request,
    location: str,
):
    try:
        # Construct the AI prompt
        prompt = (
            f"Give me a list of all blood donation centers near {location}. (more than 10) "
            f"Include their name, address, contact information, and working hours. "
            f"Respond in JSON format as a list of dictionaries with keys: name, address, contact, hours."
        )

        # Send POST request to http://localhost:8008/chat
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://ai-service:8000/chat",
                json={"prompt": prompt},
                timeout=20
            )

        # Check if response is successful
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="AI server error")

        ai_response = response.json().get("response", "")

        # Try to parse JSON response
        try:
            data = json.loads(ai_response)
        except json.JSONDecodeError:
            json_str_match = re.search(r'\[.*\]', ai_response, re.DOTALL)
            if json_str_match:
                data = json.loads(json_str_match.group(0))
            else:
                raise ValueError("Invalid JSON returned by AI")

        # Optional: Validate data format
        for item in data:
            if not all(k in item for k in ("name", "address", "contact", "hours")):
                raise ValueError("Incomplete data format in AI response")

        return {"location": location, "sources": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching blood sources: {str(e)}")
