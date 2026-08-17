# AEON Status API

`GET /api/status` exposes only the safe operational snapshot.

`POST /api/status` requires `Authorization: Bearer $AEON_API_TOKEN` and strips unknown fields before writing. Deploy behind HTTPS; never commit the token.
