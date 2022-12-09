1. In terminal 1 (from chatbot): 
    ````shell
    rasa run --enable-api --cors "*"
    ````
2. In terminal 2 start server (from chatbot): 
    ````shell
    python -m http.server 8000
    ````
3. From chatroom, first delete yarn.lock file then build and launch:
   ````shell
    yarn install
    ````
   ````shell
    yarn serve
    ````
4. Bot enable on : 
    ````shell
     http://172.20.10.3:8081
    ````


Api documentation: 
- https://developers.themoviedb.org/3/getting-started/introduction
- https://pypi.org/project/tmdbv3api/