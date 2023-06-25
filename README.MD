Fin Myth Busters
========
This project focuses on validating common myths in the financial market. 

While R is generally considered a better choice for this type of analysis, I have chosen to implement it in Python to compare the results with a similar approach in R.

Configuration
--------
Create a .env file in the same path with the following entries
```dotenv
ALPHAV_API=YOUR_ALPHA_VANTAGE_API_KEY
```
If omitted, alpha vantage cannot be used as the provider.

Yahoo finance is used by default.
