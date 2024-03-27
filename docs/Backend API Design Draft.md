# allvibes API
This draft outlines the design of the allvibes backend and its subsequent REST API. In brief, the server maintains no concept of "sessions"; sessions must be maintained entirely on the client side. Each piece of functionality making up the entire app is exposed as REST API endpoints, most of which are called via HTTP GET requests with several exceptions using HTTP POST. No function in this list depends on state or any previous functions. State is maintained entirely on the client side.

The main point of this concept, aside from complying with REST design principles, is to reduce the number of redirects within the backend to as little as possible, being zero for nearly all the functions, enabling smoother frontend development and higher responsiveness with ultimately a lower number of pages.

For the HTTP GET requests, parameters are specified as GET parameters, that is in the URL itself. As for HTTP POST requests, the expected `Content-Type` is `application/x-www-form-urlencoded`, meaning that the parameters are sent the same text-based manner as a submitted form, unless explicitly stated otherwise in the function's description.

Responses from the server to the client are always in JSON format, with the `Content-Type` being set to `application/json`. There are no exceptions to this.

The full behavior of each endpoint is outlined in this document.

# 1. List of API endpoints

## 1.1. Log in
We depend on Spotify authentication to log in.

To cope with CORS restrictions, there are two login endpoints: `/login` and `/weblogin`. The difference is that `/login` is REST-compliant while `/weblogin` performs redirects and does not directly return JSON. Both these functions are called via HTTP GET and take no parameters.

In the case of `/login`, the returned JSON object is:

| Field | Description |
| ----- | ----------- |
| status | Should always be "ok" |
| auth_url | Spotify's API URL to redirect to for authentication |

**Example response:**
```json
{
    "status": "ok",
    "auth_url": "https://accounts.spotify.com/authorize"
}
```

## 1.2. Post-authentication

After both successful and unsuccessful authentication, Spotify will redirect to `/callback` on either the API server or the frontend server, depending on whether `/login` or `/weblogin` was used respectively. In the case of an API call to `/callback`, the expected parameter is `code` passed via HTTP GET. Spotify provides this code and requires no additional action from the frontend developers.

| Parameter | Description |
| --------- | ----------- |
| code | Temporary code from Spotify's authentication; used to generate a token |

`/callback` with the appropriate parameter will return the following JSON object.

| Field | Description |
| ----- | ----------- |
| status | Should always be "ok" |
| token | Unique token from Spotify's API |
| email | User's email |
| exists | Boolean if this account already exists |
| id | UUID of this user; only valid if `exists==true` |

The client can then depend on the `exists` field to decide whether to take the user to home screen or the signup screen.

**Example response:**
```json
{
    "status": "ok",
    "token": "123456789ABCDEF",
    "email": "someone@something.com",
    "exists": true,
    "id": "c28a0a56-fe90-4341-a6f0-fd7e5da84444"
}
```

## 1.3. Account creation
Accounts are created via HTTP POST request to `/create` or `/websignup` for mobile and web clients, respectively, again to cope with CORS restrictions much like authentication.

The minimum information required to create an account are email, name, gender, and date of birth. Gender is stored as an integer, where 0 is male, 1 is female, and any other value is other. This is all sent via HTTP POST along with the request.

| Parameter | Description |
| --------- | ----------- |
| email | Email of the user |
| name | User's given name |
| gender | 0 = male, 1 = female, anything else = other |
| dob | Date of birth in `YYYY-MM-DD` format |

Upon successful account creation, the web-oriented `/websignup` will redirect to `/home` on the client server via HTTP GET with two parameters: `id` and `token`. The client can then store these in cookies to maintain sessions later and to allow access to the remaining functions.

As for the REST-compliant `/create`, the same information is simply returned in a JSON object.

| Field | Description |
| ----- | ----------- |
| status | Should be "ok" |
| id | User ID for the new user |
| token | Spotify token |

**Example response:**
```json
{
    "status": "ok",
    "id": "c28a0a56-fe90-4341-a6f0-fd7e5da84444",
    "token": "123456789ABCDEF"
}
```

## 1.4. Retrieve user information
Requests to `/userinfo` with an HTTP GET parameter named `id` will return the following generic information about a user.

| Field | Description |
| ----- | ----------- |
| status | Should be "ok" if the user exists |
| id | The same ID specified in the parameters |
| name | User's name |
| dob | Date of birth |
| gender | 0 = male, 1 = female, anything else = other |
| bio | User's bio |
| image | URL to the user's avatar |
| top_tracks | Array of the user's top 10 tracks over the past few months |
| top_artists | Array of the user's top 10 artists over the past few months |
| last_online | Date/time the user was last online in `YYYY-MM-DD HH:MM:SS` format |

Elements of `top_tracks` are defined as follows.

| Field | Description |
| ----- | ----------- |
| name | Name of the track |
| artist | Name of the track's artist |

Elements of `top_artists` are defined as follows.

| Field | Description |
| ----- | ----------- |
| name | Name of the artist |
| genre | Array of strings containing the genres this artist plays; may not be available |
| image | URL to an avatar for this artist; may not be available |

**Example response:**
```json
{
    "status": "ok",
    "id": "c28a0a56-fe90-4341-a6f0-fd7e5da84444",
    "name": "John",
    "dob": "1999-08-24",
    "gender": 0,
    "bio": "I like jazz and psychedelic rock.",
    "image": "https://cdn.something.com/images/12345678.jpg",
    "top_tracks": [
        {
            "name": "Welcome to the Machine",
            "artist": "Pink Floyd"
        },
        {
            "name": "Plainsong",
            "artist": "The Cure"
        }
    ],
    "top_artists": [
        {
            "name": "Pink Floyd",
            "genre": [
                "rock", "psychedelic rock", "progressive rock"
            ],
            "image": "https://cdn.something.com/images/123.jpg"
        },
        {
            "name": "The Cure",
            "genre": [
                "rock", "alternative rock"
            ]
        }
    ],
    "last_online": "2024-03-16 12:34:56"
}
```

## 1.5. Request data update
To request updating the user's music information from Spotify, the client requests `/update` via HTTP POST request. The data passed in this request are `id` of the user and `token` containing the Spotify token. Ideally, the client calls this function upon every startup or on every interval.

| Parameter | Description |
| --------- | ----------- |
| id | User ID of the current user |
| token | Spotify token |

Note that this simply requests an update, and does not mean that the update *will* happen. The database maintains the time and date of the most recent update, and updates are not undertaken until a certain threshold (3 days at the time of writing this) has passed. This is to avoid spamming Spotify's API as well as the fact that the data averaged out over the past month or six months is unlikely to change in a timeframe lower than the set threshold, saving internet traffic as well.

The returned object informs the client whether the update happened.

| Field | Description |
| ----- | ----------- |
| status | Should be "ok" |
| updated | Boolean value if the update happened |

**Example response:**
```json
{
    "status": "ok",
    "updated": false
}
```

## 1.6. Retrieve suggested matches
To search for people that the user can "swipe" on, the frontend requests `/recs` for recommendations. Requests are sent via HTTP GET and the parameter `id` of the current user is passed.

The returned object includes a list of people that the user can swipe on, up to 10 top tracks and/or artists shared between the users if available, and a music taste similarity score for each person.

The similarity score ranges from 0 to 1, where 0 indicates nothing in common and 1 indicates virtually identical music taste. It is recommended to interpret values higher than 0.3 as chances for a "good" match for marketing purposes, encouraging the user to "like" this person.

| Field | Description |
| ----- | ----------- |
| status | Should be "ok" |
| people | Array of `person` objects, sorted in descending order according to similarity score |

Each `person` object is defined as follows.

| Field | Description |
| ----- | ----------- |
| id | User ID, for use with `/userinfo` |
| score | Music similarity score |
| artists | Array of up to 10 top artists shared between the two users; may not be available |
| tracks | Array of up to 10 top tracks shared between the two users; may not be available |

The elements of `artists` and `tracks` are defined in the same way as is defined under `/userinfo`.

**Example response:**
```json
{
    "status": "ok",
    "people": [
        {
            "id": "c28a0a56-fe90-4341-a6f0-fd7e5da84444",
            "score": 0.47,
            "artists": [
                {
                    "name": "Pink Floyd",
                    "genre": [
                        "rock", "psychedelic rock", "progressive rock"
                    ],
                    "image": "https://cdn.something.com/images/123.jpg"
                },
                {
                    "name": "The Cure",
                    "genre": [
                        "rock", "alternative rock"
                    ]
                }
            ],
            "tracks": [
                {
                    "name": "Welcome to the Machine",
                    "artist": "Pink Floyd"
                },
                {
                    "name": "Plainsong",
                    "artist": "The Cure"
                }
            ]
        }
    ]
}
```

## 1.7. Like/dislike someone
This function is valid for the IDs returned by `/recs` to like or dislike them. Requests are sent via HTTP POST and take 3 parameters.

| Parameter | Description |
| --------- | ----------- |
| me | ID of the current user |
| other | ID of the user being judged, as returned by `/recs` |
| like | 0 = dislike, 1 = like |

The returned object indicates whether or not this action resulted in an immediate match. If this action did not result in an immediate match, the client uses `/matches` instead to scan an entire list of matches.

| Field | Description |
| ----- | ----------- | 
| status | Should be "ok" |
| matched | Boolean value |

**Example response:**
```json
{
    "status": "ok",
    "matched": true
}
```

## 1.8. Retrieve match list
The client retrieves a list of matches by requesting `/matches` via HTTP GET. One GET parameter is passed, `id` which contains the ID of the current user. The returned object is defined as follows.

| Field | Description |
| ----- | ----------- |
| status | Should be "ok" |
| people | Array of `person` objects, in descending order of most recently matched |

Each `person` object is defined in the same format as is defined under `/recs`, and thus includes a music taste similarity score, as well as an array of up to 10 top tracks and artists shared between the matches.

**Example response:**
```json
{
    "status": "ok",
    "people": [
        {
            "id": "c28a0a56-fe90-4341-a6f0-fd7e5da84444",
            "score": 0.47,
            "artists": [
                {
                    "name": "Pink Floyd",
                    "genre": [
                        "rock", "psychedelic rock", "progressive rock"
                    ],
                    "image": "https://cdn.something.com/images/123.jpg"
                },
                {
                    "name": "The Cure",
                    "genre": [
                        "rock", "alternative rock"
                    ]
                }
            ],
            "tracks": [
                {
                    "name": "Welcome to the Machine",
                    "artist": "Pink Floyd"
                },
                {
                    "name": "Plainsong",
                    "artist": "The Cure"
                }
            ]
        }
    ]
}
```

## 1.9. Send message
To send a message to a match, the client requests `/send` via HTTP POST. The parameters are defined as follows.

| Parameter | Description |
| --------- | ----------- |
| from | User ID of the current user, i.e. the sender |
| to | User ID of the recipient |
| text | The text to be sent |
| attachment | URLs to any media attachment |

The `attachment` field may be empty. In the case of multiple attachments, each URL is separated from the next by a semicolon.

The response only informs the client whether or not the message was sent.

| Field | Description |
| ----- | ----------- |
| status | Should be "ok" |

## 1.10. Receive new messages
The endpoint `/receive` is used to receive unread messages from a match. The client requests it via HTTP GET and passes two parameters. Note that this function does **not** mark messages as seen, allowing this to be used in notification systems. Instead, messages are automatically marked as seen by requesting the `/history` endpoint instead.

| Parameter | Description |
| --------- | ----------- |
| id | User ID of the current user, i.e. the recipient |
| from | User ID of the sender |

Upon success, the following object is returned.

| Field | Description |
| ----- | ----------- |
| status | Should be "ok" |
| messages | An array of `message` objects; may be empty in the case of no unread messages from this user |

Each `message` object in the aforementioned array contains a single received message. The array is arranged from most recent to least recent.

| Field | Description |
| ----- | ----------- |
| from | User ID of the sender |
| to | User ID of the recipient |
| id | Unique ID of this message; will someday be used to report abusive behavior, etc. |
| timestamp | Date/time this message was sent in `YYYY-MM-DD HH:MM:SS` format |
| text | Text content of the message; may be empty in case of attachment-only messages |
| attachment | URLs to attachments in this message |

Much like in `/send`, `attachment` may be empty in the case of no attachments. In the case of multiple attachments, each two URLs are separated by a semicolon.

**Example response:**
```json
{
    "status": "ok",
    "messages": [
        {
            "from": "f870e60f-e574-4c6b-ba64-b50a0b19e2cc",
            "to": "23b4b38f-ec20-4762-891d-b05d9292645f",
            "id": "4ffe29a2-8f93-4aee-bfe4-c69b342abd6b",
            "timestamp": "2024-03-25 21:11:03",
            "text": "thank you!! i really like yours too! c:",
            "attachment": ""
        }
    ]
}
```

## 1.11. Retrieve message history
The endpoint `/history` is used to retrieve message history between matches. It includes messages sent by both the user (the one sending the request) and their match (the "context"). This function also marks all messages as having been seen at the exact time the function was called, if they hadn't already by that point in time.

This function divides messages up into "pages" for network efficiency, where each page contains up to 20 messages sent in either direction. The client requests additional pages as the user attempts to scroll earlier up in the conversation.

This endpoint uses HTTP GET and takes 3 parameters.

| Parameter | Description |
| --------- | ----------- |
| id | User ID of the user |
| context | User ID of the match |
| page | Page number to retrieve; this number is zero-based |

Upon success, the following object is returned.

| Field | Description |
| ----- | ----------- |
| status | Should be "ok" |
| count | The number of messages returned in this response |
| last_page | Boolean value indicating whether this page is the earliest message history |
| messages | Array of `message` objects |

The `message` object is defined in the same as is defined under the `/receive` endpoint, and in the same way they are arranged in order of most recent to least recent within the array.

The `last_page` field is set to `true` if this is the last valid page for this conversation, i.e. the client has scrolled up the very first message in the conversation, and subsequent calls to this API will return an array of size zero and `count` set to zero. Likewise, a `count` value of less than 20 should also be interpreted as `last_page` being set to `true`.

**Example response:**
```json
{
    "status": "ok",
    "count": 3,
    "last_page": true,
    "messages": [
        {
            "from": "23b4b38f-ec20-4762-891d-b05d9292645f",
            "to": "f870e60f-e574-4c6b-ba64-b50a0b19e2cc",
            "id": "87f2e412-1b81-49c6-a4f9-11509c91f620",
            "timestamp": "2024-03-25 21:12:28",
            "text": "thank you! so what do you do for a living?",
            "attachment": ""
        },
        {
            "from": "f870e60f-e574-4c6b-ba64-b50a0b19e2cc",
            "to": "23b4b38f-ec20-4762-891d-b05d9292645f",
            "id": "4ffe29a2-8f93-4aee-bfe4-c69b342abd6b",
            "timestamp": "2024-03-25 21:11:03",
            "text": "thank you!! i really like yours too! c:",
            "attachment": ""
        },
        {
            "from": "23b4b38f-ec20-4762-891d-b05d9292645f",
            "to": "f870e60f-e574-4c6b-ba64-b50a0b19e2cc",
            "id": "614f90ce-dc8d-4cbe-91c1-dca825c555ba",
            "timestamp": "2024-03-25 21:08:42",
            "text": "heyy, i really like your hair color",
            "attachment": ""
        }
    ]
}
```

## 1.12. Upload media attachment
TODO

## 1.13. Unmatch
The endpoint `/unmatch` is used to unmatch with a match. It is requested via HTTP POST and takes two parameters.

| Parameter | Description |
| --------- | ----------- |
| me | User ID of the current user |
| other | User ID of the match to be unmatched |

Upon success, the object returned indicates only whether or not the unmatch happened.

| Field | Description |
| ----- | ----------- |
| status | Should be "ok" |

## 1.14. Block/report match
TODO

## 1.15. Profile updates
TODO: this should probably be very similar to account creation; it's nothing more than updating the user's info in the main table

## 1.16. Event notifications
TODO
