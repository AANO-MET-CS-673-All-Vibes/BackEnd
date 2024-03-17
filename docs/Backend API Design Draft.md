# allvibes backend plan
This document is to assist with my own design of the backend portion for the project. I'm planning a backend that is fundamentally nothing more than an REST-compliant API that exposes the functionality we'll provide. This will allow for extra flexibility in the frontend, as well as (potentially in the future) making it easier to separate the web client from the mobile client.

The main point of this design concept is to reduce the number of redirects within the backend to as little as possible, making frontend development smoother and more responsive with ultimately a lower number of pages.

## Log in
We depend on Spotify authentication to log in.

To cope with CORS restrictions, there are two login functions: `/login` and `/weblogin`. The difference is that `/login` is REST-compliant while `/weblogin` performs redirects and does not directly return JSON.

In the case of `/login`, the returned JSON object is:

| Field | Description |
| ----- | ----------- |
| status | Should always be "ok" |
| auth_url | Spotify's API URL to redirect to for authentication |

## Post-authentication

After both successful and unsuccessful authentication, Spotify will redirect to `/callback` on either the API server or the frontend server, depending on whether `/login` or `/weblogin` was used respectively. In the case of an API call to `/callback`, the expected parameter is `code` passed via HTTP GET. Spotify provides this code and requires no additional action from the frontend developers. 

`/callback` with the appropriate parameter will return the following JSON object.

| Field | Description |
| ----- | ----------- |
| status | Should always be "ok" |
| token | Unique token from Spotify's API |
| email | User's email |
| exists | Boolean if this account already exists |
| id | UUID of this user; only valid if `exists==true` |

The frontend can then depend on the `exists` field to decide whether to take the user to home screen or the signup screen.

## Account creation
Accounts are created via HTTP POST request to `/create` or `/websignup` for mobile and web clients, respectively, again to cope with CORS restrictions much like authentication.

The minimum information required to create an account are email, name, gender, and date of birth. Gender is stored as an integer, where 0 is male, 1 is female, and any other value is other. This is all sent via HTTP POST along with the request.

Upon successful account creation, the web-oriented `/websignup` will redirect to `/home` on the client server via HTTP GET with two parameters: `id` and `token`. The client can then store these in cookies to maintain sessions later and to allow access to the remaining functions.

As for the REST-compliant `/create`, the same information is simply returned in a JSON object.

| Field | Description |
| ----- | ----------- |
| status | Should be "ok" |
| id | User ID for the new user |
| token | Spotify token |

## Retrieve user information
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
| last_online | Date/time the user was last online |

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

## Request data update
To request updating the user's music information from Spotify, the client requests `/update` via HTTP POST request. The data passed in this request are `id` of the user and `token` containing the Spotify token. Ideally, the client calls this function upon every startup or on every interval.

Note that this simply requests an update, and does not mean that the update *will* happen. The database maintains the time and date of the most recent update, and updates are not undertaken until a certain threshold (3 days at the time of writing this) has passed. This is to avoid spamming Spotify's API as well as the fact that the data averaged out over the past month or six months is unlikely to change in a timeframe lower than the set threshold, saving internet traffic as well.

The returned object informs the client whether the update happened.

| Field | Description |
| ----- | ----------- |
| status | Should be "ok" |
| updated | Boolean value if the update happened |

## Retrieve suggested matches
To search for people that the user can "swipe" on, the frontend requests `/recs` for recommendations. Requests are sent via HTTP GET and the parameter `id` of the current user is passed.

The returned object includes a list of people that the user can swipe on, up to 10 top tracks and/or artists shared between the users if available, and a music taste similarity score for each person. The similarity score ranges from 0 to 1, where 0 indicates nothing in common and 1 indicates virtually identical music taste. I recommend the frontend treat values higher than 0.3 as chances for a "good" match for marketing purposes.

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

## Like/dislike someone
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

## Match list retrieval
TODO

## Send/receive messages
TODO

## Retrieve message history
TODO

## Match profile retrieval
TODO: retrieve info about someone we alr matched with

## Unmatch
TODO

## Block/report match
TODO

## Profile updates
TODO: this should probably be very similar to account creation; it's nothing more than updating the user's info in the main table

## Event notifications
TODO
