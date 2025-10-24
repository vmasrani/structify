Extract a structured record from the input using a universal schema optimized for retrieval and search.

## REQUIRED FIELDS (must always populate)
- `summary`: 1-2 sentence overview of the content. REQUIRED for all content types.
- `questions`: 3-5 hypothetical questions this content answers. Even for images/contacts, ask what someone might search for. Example: ["What is the project deadline?", "Who handles customer support?", "What does this diagram show?"]
- `concepts`: Broader themes/topics (more abstract than keywords). Example: ["project management", "customer service", "network architecture"]
- `key_phrases`: Important multi-word expressions. Keep together, don't split. Example: ["quarterly business review", "API rate limiting", "customer success team"]

## Optional Core Metadata (populate when evident)
- `title`: Concise identifying title
- `text`: Full text content or description
- `source`: Origin (file path, URL, platform)
- `keywords`: Specific important single terms (supplement to key_phrases)
- `tags`: Categorical labels for organization
- `entities`: Named entities - `persons[]`, `orgs[]`, `places[]`, `emails[]`, `phones[]`, `ids[]`
- `sentiment`: Overall tone - "positive", "negative", "neutral", "urgent", "formal", "casual"

## Optional Retrieval-Enhancing Fields (when relevant)
- `relationships`: Connections to people/things. Example: `[{type: "spouse", target: "Jane Doe", context: "likes gardening and mystery novels"}]`, `[{type: "references", target: "Q3 Budget Doc"}]`
- `temporal_context`: Dict with `urgency` (high/medium/low), `time_horizon` (past/present/future/ongoing), `expiry_date`, `recurrence`
- `claims`: Atomic, verifiable facts. Example: ["Budget is $50K", "Deadline is March 15, 2024", "John is the project lead"]

## Optional Context (only when relevant)
- `time`: Temporal range with `start_at`, `end_at`, `timezone` (ISO 8601)
- `location`: Geographic details with `name`, `address`, `lat`, `lon`
- `participants`: People involved with `name`, `email`, `role`, `response`
- `links`: URLs or references found in content
- `status`: Current state (e.g., "active", "completed", "pending")
- `dedupe_key`: Unique identifier for deduplication
- `action_items`: Specific tasks or next steps (when explicitly present)
- `decisions`: Key decisions made or documented (when explicitly present)

## Type-Specific Sections (populate only if applicable)
Populate the relevant section(s) based on content type:

### message_thread (for emails, chats, SMS, conversations)
- `platform`: Communication platform if identifiable
- `messages[]`: Array of `{speaker, sent_at, text}`

### contact (for people, organizations, contact info)
- `full_name`, `given_name`, `family_name`
- `emails[]`, `phones[]`
- `company`, `role`, `birthday`, `notes`, `categories[]`
- Mirror emails/phones into entities

### document (for documents, notes, reports, articles)
- `doc_type`: Type of document
- `sections[]`: Array of `{title, text}` for structured content
- `key_points[]`: Main takeaways
- `references[]`: Citations or sources
- `signatories[]`: People who signed/authored

### calendar_event (for meetings, appointments, scheduled events)
- `uid`: Unique event identifier
- `organizer`: Event organizer
- `attendees[]`: Array of `{name, email, response, role}`
- `description`: Event details
- `sequence`: Version number
- Map DTSTART/DTEND to `time.start_at`/`time.end_at`

### image (for images, media files)
- `format`: File format/extension
- `caption`: Brief description
- Put full description in `text`, derive concise `title`, include topical `keywords[]`

## Critical Guidelines
- ALWAYS generate summary, questions, concepts, and key_phrases - these are required for retrieval
- For questions: think about what a user might search for to find this content
- For concepts: extract broader themes that connect to related content
- For key_phrases: capture multi-word terms that should be matched together
- Use only evidence in the input; omit optional fields rather than guessing
- Multiple type-specific sections can be populated if content spans types

