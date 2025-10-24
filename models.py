from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class TimeRange(BaseModel):
    start_at: Optional[str] = None
    end_at: Optional[str] = None
    timezone: Optional[str] = None


class GeoLocation(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None


class Participant(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    response: Optional[str] = None


class Entities(BaseModel):
    persons: Optional[List[str]] = None
    orgs: Optional[List[str]] = None
    places: Optional[List[str]] = None
    emails: Optional[List[str]] = None
    phones: Optional[List[str]] = None
    ids: Optional[List[str]] = None


class Message(BaseModel):
    speaker: str
    sent_at: Optional[str] = None
    text: str


class MessageThreadData(BaseModel):
    platform: Optional[str] = None
    messages: List[Message]


class ContactData(BaseModel):
    full_name: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    emails: Optional[List[str]] = None
    phones: Optional[List[str]] = None
    company: Optional[str] = None
    role: Optional[str] = None
    birthday: Optional[str] = None
    notes: Optional[str] = None
    categories: Optional[List[str]] = None


class DocumentSection(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None


class DocumentData(BaseModel):
    doc_type: Optional[str] = None
    sections: Optional[List[DocumentSection]] = None
    key_points: Optional[List[str]] = None
    action_items: Optional[List[str]] = None
    decisions: Optional[List[str]] = None
    references: Optional[List[str]] = None
    signatories: Optional[List[str]] = None


class CalendarAttendee(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    response: Optional[str] = None
    role: Optional[str] = None


class CalendarEventData(BaseModel):
    uid: Optional[str] = None
    organizer: Optional[str] = None
    attendees: Optional[List[CalendarAttendee]] = None
    description: Optional[str] = None
    sequence: Optional[int] = None
    status: Optional[str] = None


class ImageData(BaseModel):
    format: Optional[str] = None
    caption: Optional[str] = None


class Relationship(BaseModel):
    type: str
    target: str
    context: Optional[str] = None


class UniversalRecord(BaseModel):
    # Required retrieval-critical fields (work for ALL content types)
    summary: str
    questions: List[str] = []
    concepts: List[str] = []
    key_phrases: List[str] = []

    # Optional core metadata (high value when present)
    title: Optional[str] = None
    text: Optional[str] = None
    source: Optional[str] = None
    keywords: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    entities: Optional[Entities] = None
    sentiment: Optional[str] = None

    # Optional retrieval-enhancing fields (populate when relevant)
    relationships: Optional[List[Relationship]] = None
    temporal_context: Optional[Dict[str, Any]] = None
    claims: Optional[List[str]] = None

    # Optional time/place/people (only when relevant)
    time: Optional[TimeRange] = None
    location: Optional[GeoLocation] = None
    participants: Optional[List[Participant]] = None
    links: Optional[List[str]] = None
    status: Optional[str] = None
    dedupe_key: Optional[str] = None

    # Optional type-specific actions (only when truly present)
    action_items: Optional[List[str]] = None
    decisions: Optional[List[str]] = None

    # Type-specific sections (optional, populate as needed)
    message_thread: Optional[MessageThreadData] = None
    contact: Optional[ContactData] = None
    document: Optional[DocumentData] = None
    calendar_event: Optional[CalendarEventData] = None
    image: Optional[ImageData] = None

