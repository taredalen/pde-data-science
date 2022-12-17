1. In terminal 1 (from chatbot): 
    ````yml
    rasa run --enable-api --cors "*"
    ````
2. In terminal 2 start server (from chatbot): 
    ````yml
    rasa run actions
    ````
3. Open index file for bot widget

5. For API configuration you need to generate token and add to .env file.

   Useful documentation:

   - https://developers.themoviedb.org/3/getting-started/introduction
   - https://pypi.org/project/tmdbv3api/
   - https://github.com/AnthonyBloomer/tmdbv3api