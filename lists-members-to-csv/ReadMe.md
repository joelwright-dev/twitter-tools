# Twitter Lists member extractor to CSV file

First you must create a file in this folder called constants.py and copy and paste the following:
```bash
TWITTER_API_KEY = "ABC123"
TWITTER_API_SECRET = "ABC123"
TWITTER_ACCESS_TOKEN = "ABC123"
TWITTER_ACCESS_SECRET = "ABC123"
TWITTER_BEARER_TOKEN = "ABC123"
```
And replace ABC123 with your respective twitter API keys. You will also need an elevated account. Star this repository if you wish for me to create an easy github app which allows you to do this without worrying about API keys.

Simply run:
```bash
python3 main.py [twitter list id]
```
And replace `[twitter list id]` with the id of the Twitter List you wish to extract members from.

The program currently only has a limit of 20 members which I will be solving soon.
