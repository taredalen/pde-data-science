<h1 align="center">
  <a href="docs/bot.svg"><img src="docs/bot.svg" alt="Markdownify" width="200"></a>
  <br>
  Open-source chatbot with Rasa and the NLP
  <br>
</h1>
<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#related">Related</a> •
  <a href="#license">License</a>
</p>


<table>
<tr>
<td>
  A webapp using Quandl API to display history of stock growth in a given period of time. It helps predict the growth of stocks from the  charts of stock performace in any period of time. It helps to judge stocks, with the principle of momentum investing, which returns 1% per month on average.
</td>
</tr>
</table>




## Key Features

kkk


## How to use

1. In terminal 1 (from chatbot):
    ````yml
    rasa run --enable-api --cors "*"
    ````
2. In terminal 2 start server (from chatbot): 
    ````yml
    rasa run actions
    ````
3. Finally, open server page:
    ````yml
    python widget/server.py
    ````
5. For API configuration you need to generate token and add to .env file.
 
## Related

- [TMDB for python](https://github.com/AnthonyBloomer/tmdbv3api): TMDB API for movie requests
- [TMDB API](https://developers.themoviedb.org/3): get started and generate a key

