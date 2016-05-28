# Emoto Backend

A backend for emoto.

# TODO
- add emoto.

## API

- `GET /api/v1/users/{user}/status`
  Returns user as 'self' and partner, if exists, as 'partner'

- `GET /api/v1/users/{user}/messages`
  Returns an array of all messages. 

- `POST /api/v1/users/{user}/messages/new`
  Adds a new message. Required JSON payload: {text: string, emoto: string (optional)}

- `POST /api/v1/users/{user}/location`
   Sets location + time zone (for time offset). Required JSON payload: {latitude: float, longitude: float}

- `POST /api/v1/users/{user}/pair/{pair_code}`
   Pairs your account with another account.
  
- `POST /api/v1/users/{user}/unpair`
  Unpairs your account

- `POST /api/v1/users/{user}/register_push_notifications`
  Registers a push notification device token. Required JSON payload: {token: string}

- `POST /api/v1/users/new`
  Creates a new user. Required JSON payload: {username: str, latitude: float, longitude: float}

- `GET /api/v1/emotos`
  Returns a list of emotos.

## Required libraries

- boto
- django-storages
- requests
- pillow
- pyaml
- django-push-notifications
