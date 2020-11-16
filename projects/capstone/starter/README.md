# Final FullStack Project

## Heroku Link

https://infinite-basin-08333.herokuapp.com/

## For local usage

1. Install virtual environment with libraries from requirements.txt file

    pip install -r requirements.txt

2. For generating token we can use following link

    https://dev-mh.us.auth0.com/authorize?audience=https://localhost:5001&response_type=token&client_id=jBWCdl3oN49mA8UX1jV4rvNQZ0IyiN6o&redirect_uri=http://localhost:5000

3. App has two roles: assistant and director. Use personal tokens for queries.

    Assistant token (only read functional): eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBNaFZqTzk3NTVRbERiN1hseXBLWSJ9.eyJpc3MiOiJodHRwczovL2Rldi1taC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYzNTI5NzQzOGQxYTIwMDZkMjExMDYxIiwiYXVkIjoiaHR0cHM6Ly9sb2NhbGhvc3Q6NTAwMSIsImlhdCI6MTYwNTUxMjE5MiwiZXhwIjoxNjA1NTk4NTkyLCJhenAiOiJqQldDZGwzb040OW1BOFVYMWpWNHJ2TlFaMEl5aU42byIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.PKb2R4VfXVTG4jGQ46ttdTd7WrLQdtuR1WSC8hwP1lX06_GuSmS08U0SuBMjXZ83ijw0oLXpWLoJOs2vJ4XoIzr5Z2MOB9jg3UIzN2KOUHJjNr2RqRmUJoWy1jjN9s_oltC6qCwakxGHLzQ839ZQJkCB8DM0UxHtJnVN4oBOrwTwT__y4ZR-DNOErGb72jMN9_tvBmQrGIfCdXsY4jU5Pq-9ee_JlqK1X27PehrDVGd__frEUDjF_rz12VzTqQ9WNtZJ24qGxcmsn3PtfKME7uwWjQ05HpH4ZsWK2NKWAfVpsWpKh8jCAjjDr8ME7zAgZfXY8-4MVSSX6chF5SPr2w

    Director token (full functional): eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBNaFZqTzk3NTVRbERiN1hseXBLWSJ9.eyJpc3MiOiJodHRwczovL2Rldi1taC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTc4MDE0MzMzOTQ2NjEyMzYzNjAiLCJhdWQiOlsiaHR0cHM6Ly9sb2NhbGhvc3Q6NTAwMSIsImh0dHBzOi8vZGV2LW1oLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MDU1MTIxNDEsImV4cCI6MTYwNTU5ODU0MSwiYXpwIjoiakJXQ2RsM29ONDltQThVWDFqVjRydk5RWjBJeWlONm8iLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.BOQV5BA6IoZOSbJUlOwB0PJTMoGQDiWGDqv70i3xjCnXd5v2Uz8g-EIjBYjtROhX6kMT3LRHZP-pCBPi75GzEP2IMCurf73hk_x4siFn5M22hbMkkEllipr_-w1nz3G8YOI6B0yg7DzNyxYAYvvOCpiaJnDFXYpLWoKkupUetj0hSjHK0-JXSSKCdEchqtG7mhBfwYvcFWHRZpYei4gFUPYP28F0jVLZd9Cf2aU7QHJvMJenlzyFFvtXJZUeodVkpRvVp_D9MN4_DyBvpPhBeJIH1uRKQM4hBvGpZVpOWA4kkf5HXYlPzxjP4ylxaw2cp78gY3LXN0a3HRlYhvzoxg

4. Run flask app inside virtual environment
    ```
    export FLASK_APP=app.py
    flask run reload
    ```

5. Generate query with token. For example:
    ```
    curl --request GET 'http://127.0.0.1:5000/movies' --header 'authorization: Bearer <assistant/director token>'
    ```
6. For testing
    ```
    python test_app.py
    ```
