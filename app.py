from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from exchangelib import Account, Credentials, Message, Mailbox, CalendarItem, EWSTimeZone, Attendee
from bs4 import BeautifulSoup
from dateutil import parser
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()


# Einloggen in den Account
creds = Credentials(os.environ.get("EMAIL"), os.environ.get("PASSWORD"))
account = Account(os.environ.get("EMAIL"), credentials=creds, autodiscover=True)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Email(BaseModel):
    subject: str
    body: str
    email_address: EmailStr


class EmailData(BaseModel):
    subject: str
    body: str
    author: EmailStr
    name: str


class CalendarItemModel(BaseModel):
    subject: str
    body: str
    location: Optional[str] = None
    start_time: str
    end_time: str
    attendees: Optional[List[str]] = None


@app.post("/email/")
async def create_email(email: Email):
    m = Message(
        account=account,
        folder=account.sent,
        subject=email.subject,
        body=email.body,
        to_recipients=[
            Mailbox(email_address=email.email_address),
        ],
    )
    m.send()
    return {"email": email}


@app.post("/calendar/")
async def create_calendar_item(item: CalendarItemModel):
    start_time = parser.parse(item.start_time)
    end_time = parser.parse(item.end_time)

    tz = EWSTimeZone("Europe/Berlin")
    start_time = start_time.replace(tzinfo=tz)
    end_time = end_time.replace(tzinfo=tz)

    attendees = None
    if item.attendees:
        attendees = [Attendee(mailbox=att) for att in item.attendees]

    cal_item = CalendarItem(
        folder=account.calendar,
        subject=item.subject,
        start=start_time,
        end=end_time,
        body=item.body,
        location=item.location,
        required_attendees=attendees,
    )
    cal_item.save()
    return {"calendar_item": item}


@app.get("/latest_email/", response_model=List[EmailData])
async def read_latest_emails():
    latest_emails = account.inbox.all().order_by("-datetime_received")[:10]
    email_list = []
    for email in latest_emails:
        soup = BeautifulSoup(email.body, "html.parser")
        body = soup.get_text()
        email_data = EmailData(
            subject=email.subject,
            body=body,
            author=email.author.email_address,
            name=email.author.name,
        )
        email_list.append(email_data)
    return email_list



@app.get("/logo.png")
async def plugin_logo():
    filename = "logo.png"
    return FileResponse(filename, media_type="image/png")


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return Response(text, media_type="application/json")


@app.get("/openapi.yaml")
async def openapi_spec():
    with open("openapi.yaml") as f:
        text = f.read()
        return Response(text, media_type="text/yaml")
