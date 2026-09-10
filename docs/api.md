# Jeevan Setu API

Base URL when running locally: `http://127.0.0.1:5000`

## Health
`GET /api/health`

## Read state
- `GET /api/workers`
- `GET /api/alerts`
- `GET /api/environment`
- `GET /api/rover`

## Worker update
`POST /api/worker/update`

Example:
```json
{
  "worker_id": "W03",
  "name": "Worker 03",
  "zone": "N4",
  "heart_rate": 84,
  "movement": false,
  "sos": true,
  "fall_detected": true,
  "environment": {
    "gas": 860,
    "temperature": 42,
    "humidity": 74,
    "zone": "N4"
  }
}
```

## Rover
`POST /api/rover/update`

`POST /api/rover/deploy` with `{ "target_zone": "N4" }`

`POST /api/rover/reset`

## Demo helpers
`POST /api/demo/reset`

`POST /api/demo/emergency`

The demo helper intentionally uses controlled/sample values so the complete emergency workflow can be shown without physical sensors connected.
