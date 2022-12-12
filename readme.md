1. In terminal 1 (from chatbot): 
    ````yml
    rasa run --enable-api --cors "*"
    ````
2. In terminal 2 start server (from chatbot): 
    ````yml
    rasa run actions
    ````
3. For network connexion follow instructions from next link:
   ````yml
   https://ngrok.com/download
   ````
4. I'm using Telegram, so I added this to credentials.yml: 
    ````yml
   telegram:
      access_token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      verify: rasa_bot
      webhook_url: https://52b1-37.eu.ngrok.io/webhooks/telegram/webhook
    ````

5. For API configuration you need to generate token and add to .env file.

   Useful documentation:

   - https://developers.themoviedb.org/3/getting-started/introduction
   - https://pypi.org/project/tmdbv3api/
   - https://github.com/AnthonyBloomer/tmdbv3api