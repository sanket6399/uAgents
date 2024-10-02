import os
import json
import aiohttp
from dotenv import load_dotenv
from twilio.rest import Client
# Load environment variables
load_dotenv()

SERP_API_KEY = os.getenv("SERP_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_WHATSAPP_NUMBER = os.getenv("FROM_WHATSAPP_NUMBER")
TO_WHATSAPP_NUMBER = os.getenv("TO_WHATSAPP_NUMBER")


async def get_job_summary(query: str, location: str):
    url = "https://serpapi.com/search.json"
    params = {
        "q": query + " careers",
        "location": location,
        "engine": "google_jobs",
        "api_key": SERP_API_KEY,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, ssl=False) as response:
            if response.status == 200:
                data = await response.json()
                jobs = data.get("jobs_results", [])
                if jobs:
                    job = jobs[0]
                    return json.dumps({
                        "Title": job.get("title", "N/A"),
                        "Company": job.get("company_name", "N/A"),
                        "Location": job.get("location", "N/A"),
                        "Link": job.get("link", "N/A"),
                        "Posted": job.get("detected_extensions", {}).get("posted_at", "N/A"),
                        "Type": job.get("detected_extensions", {}).get("schedule_type", "N/A"),
                        "Description": job.get("description", "N/A"),
                    }, indent=2)
                else:
                    return "No job results found."
            else:
                return f"Failed to fetch data: {response.status}"


async def send_whatsapp_message(body: str):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=body,
        from_=FROM_WHATSAPP_NUMBER,
        to=TO_WHATSAPP_NUMBER
    )
    return message.sid
