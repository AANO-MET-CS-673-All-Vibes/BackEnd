# allvibes backend plan
This document is to assist with my own design of the backend portion for the project. I'm planning a backend that is fundamentally nothing more than an API that exposes the functionality we'll provide. This will allow for extra flexibility in the frontend, as well as (potentially in the future) making it easier to separate the web client from the mobile client.

The main point of this design concept is to reduce the number of redirects within the backend to as little as possible, making frontend development smoother and more responsive with ultimately a lower number of pages.

## Log in
We depend on Spotify authentication to log in. So a request may look like this:
1. `/login` - redirects to Spotify's authorization page
2. `/callback` - in both success or failure to authorize, we are redirected here
3. `/operations` - if successful, we are redirected to operations

Now I'm thinking of rewriting `/operations` to simply return a JSON object with the following fields:
| Field | Description |
| ----- | ----------- |
| status | Should always be "ok" |
| token | Unique token from Spotify's API |
| exists | Whether or not this account already exists: "true" or "false" as a string type |

The frontend can then depend on the `exists` field to decide whether to take the user to home screen or the signup screen.

## Account creation
In the case of `/operations` indicating the account does not exist, the frontend will offer a form asking the user for their name, date of birth, gender, sexuality, bio, profile picture, etc. This form will then be submitted to `/create` by an HTTP POST request. Note that the form will not ask for email or password; email will automatically be pulled from Spotify's API and we don't need a password if we already depend on Spotify for authentication.
Nevertheless, a successful POST request to `/create` will return the following JSON object:
| Field | Description |
| ----- | ----------- |
| status | Should be "ok" |

