# Contacts API — Integration Reference

> Runtime owner: **`vkgeorgia/Jeeves`** (external backend repository).
> This file is integration-oriented for consumers of the API.

**Base URL (production):** тот же хост, что в **`backend_url`** в корневом `_config.yml` (сайт и виджет собираются с этим значением через Jekyll).

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
# Подставьте базовый URL (как в _config.yml → backend_url), например:
# export BACKEND_URL="https://your-service-xxxxx.us-central1.run.app"

# List all contacts
curl "${BACKEND_URL}/api/contacts" \
  -H "x-api-key: $CONTACTS_API_KEY"

# Search
curl "${BACKEND_URL}/api/contacts?q=anna" \
  -H "x-api-key: $CONTACTS_API_KEY"

# Get by ID
curl "${BACKEND_URL}/api/contacts/42" \
  -H "x-api-key: $CONTACTS_API_KEY"
```

---

## Notes

- `raw_data` — unstructured JSON blob, may be null or contain extra fields from the source system
- `tags` — array of strings, may be null
- The API is read-only; contacts are managed externally (Contactor app)
