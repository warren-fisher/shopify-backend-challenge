# Image hosting web app
This web application was created as part of the shopify backend challenge.
It is hosted at https://images.warrenfisher.net
## Features
- Can upload a file
    - Can view files at the 'image gallery' tab
- Uploading multiple files creates an album
    - Can view albums at the 'abums' tab
- Users can optionally create an account
    - User passwords are hashed and then sent to the backend for storage in a database
    - API returns a user authentication token, which the frontend will include with subsequent requests
- Files or albums can be made private (if you have an account)

## TODO
- React better display albums in groups
- Prevent user from uploading the same file multiple times by spam clicking button
    - Response from clicking button?