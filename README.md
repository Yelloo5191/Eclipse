To run:

Clone and run the following command
`virtualenv .env && source .env/bin/activate && pip install -r requirements.txt`

Create a .env file in the main directory with the following values
`TOKEN={your token here}`
`PREFIX={your prefix here}`

Run the file with either

`python main.py`

or if you have NPM installed and are developing the bot

```
npm i -g nodemon // first time only

nodemon --exec python main.py
```
