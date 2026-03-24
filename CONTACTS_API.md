# Contacts API — Integration Reference

**Base URL:** `https://ai-avatar-103512681014.us-central1.run.app`

## Authentication

All `/api/contacts` endpoints require a header:
```
x-api-key: <CONTACTS_API_KEY>
```

The key is stored in the `CONTACTS_API_KEY` environment variable on Cloud Run.

---

## Endpoints

### List contacts
```
GET /api/contacts
GET /api/contacts?q=<search>
```
- `q` — optional substring search on `full_name` and `notes` (case-insensitive)
- Returns all contacts sorted by `full_name`

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "full_name": "Anna Schmidt",
      "email": "anna@example.com",
      "phone": "+49123456789",
      "company": "Acme GmbH",
      "position": "CTO",
      "tags": ["recruiter", "warm"],
      "notes": "Met at conference",
      "raw_data": {}
    }
  ]
}
```

### Get contact by ID
```
GET /api/contacts/{id}
```

**Response:** single contact object (same fields as above), or `404` if not found.

---

## Error responses

| Code | Meaning |
|------|---------|
| `401 Unauthorized` | Missing or invalid `x-api-key` |
| `404 Not Found` | Contact ID does not exist |

---

## Examples

```bash
# List all contacts
curl https://ai-avatar-103512681014.us-central1.run.app/api/contacts \
  -H "x-api-key: $CONTACTS_API_KEY"

# Search
curl "https://ai-avatar-103512681014.us-central1.run.app/api/contacts?q=anna" \
  -H "x-api-key: $CONTACTS_API_KEY"

# Get by ID
curl https://ai-avatar-103512681014.us-central1.run.app/api/contacts/42 \
  -H "x-api-key: $CONTACTS_API_KEY"
```

---

## Notes

- `raw_data` — unstructured JSON blob, may be null or contain extra fields from the source system
- `tags` — array of strings, may be null
- The API is read-only; contacts are managed externally (Contactor app)
