# allvibes backend plan
This document is to assist with my own design of the backend portion for the project. I'm planning a backend that is fundamentally nothing more than an API that exposes the functionality we'll provide. This will allow for extra flexibility in the frontend, as well as (potentially in the future) making it easier to separate the web client from the mobile client.

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
Accounts are created via HTTP POST request to `/create`. The minimum information required to create an account are email, name, gender, and date of birth. Gender is stored as an integer, where 0 is male, 1 is female, and any other value is other. Upon successful account creation, the following JSON object is returned.

| Field | Description |
| ----- | ----------- |
| status | Should be "ok" |
| id | UUID of this user |

## Suggested profile retrieval
TODO: scan for people nearby and recommend them in order of most similar music taste

## Match attempt
TODO: send a match attempt and then either match or not

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
