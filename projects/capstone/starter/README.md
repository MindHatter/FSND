# Final FullStack Project

This Capstone is the final project of the Udacity Full Stack Nano Degree (FSND) program. I enrolled in the program to get an introduction and practical experience in working with databases, API's, cyber securtiy and automated deployment & testing of systems. This is the start to refresh my technical skills and is a great foundational program that has put me on the right course.

## Overview

The Casting Agency is a company that is responsible for creating movies and managing and assigning actors to those movies. 

## Heroku Link

https://infinite-basin-08333.herokuapp.com/

## For local usage

1. Install virtual environment with libraries from requirements.txt file

    pip install -r requirements.txt

2. For generating token we can use following link

    https://dev-mh.us.auth0.com/authorize?audience=https://localhost:5001&response_type=token&client_id=jBWCdl3oN49mA8UX1jV4rvNQZ0IyiN6o&redirect_uri=http://localhost:5000

3. App has two roles by default

    Assistant: 
    * "get:actors" to view all actors or one of them
    * "get:movies" to view all movies or one of them
    
    Director has assistant permissions and: 
    * "delete:actors" to remove actors
    * "delete:movies" to remove products
    * "patch:actors" to update actors
    * "patch:movies" to update movies
    * "post:actors" to create actors
    * "post:movies" to create movies
    
    For RBAC control generate tokens for each role, add it into setup.sh file and run it.
    ```
    ./setup.sh
    ```

4. Run flask app inside virtual environment
    ```
    export FLASK_APP=app.py
    flask run reload
    ```

5. API endpoints.
    ```
    GET /actors
    GET /actors/<int:actor_id>
    GET /movies
    GET /movies/<int:movie_id>
    POST /actors {name, age, gender}
    POST /movies {title, releasedate}
    PATCH /actors/<int:actor_id> [name, age, gender]
    PATCH /movies [title, releasedate]
    DELETE /actors/<int:actor_id>
    DELETE /movies/<int:movie_id>
    ```

    You can use following template with curl for checking API endpoints:
    ```
    curl --request GET 'http://127.0.0.1:5000/<api endpoint>' --header 'authorization: Bearer <assistant/director token>'
    ```
    
6. For testing
    ```
    python test_app.py
    ```

