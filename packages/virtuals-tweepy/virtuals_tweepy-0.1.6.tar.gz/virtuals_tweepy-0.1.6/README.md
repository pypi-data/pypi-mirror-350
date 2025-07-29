# Virtuals Protocol Tweepy: Twitter for Python!

## Installation

The easiest way to install the latest version from PyPI is by using
[pip](https://pip.pypa.io/):

```bash
pip install virtuals-tweepy
```

## Quickstart: Initialize Client with Virtuals Protocol's GAME Access Token

### How to Get a GAME API Key
1. Go to the Virtuals Protocol's [GAME Console](https://console.game.virtuals.io/)
2. Sign in with your wallet.
3. Click on "**Create a New Project**" to register a new project.
4. Once your project is created, click on "**Generate one now**" under "API Key" to generate your API key.

### How to Get GAME X Access Token (Virtuals Protocol's X Enterprise API)

- To get the access token for this option, run the following command:

  ```bash
  poetry run virtuals-tweepy auth -k <GAME_API_KEY>
  ```

  You will see the following output:

  ```bash
  Waiting for authentication...
  
  Visit the following URL to authenticate:
  https://x.com/i/oauth2/authorize?response_type=code&client_id=VVdyZ0t4WFFRMjBlMzVaczZyMzU6MTpjaQ&redirect_uri=http%3A%2F%2Flocalhost%3A8714%2Fcallback&state=866c82c0-e3f6-444e-a2de-e58bcc95f08b&code_challenge=K47t-0Mcl8B99ufyqmwJYZFB56fiXiZf7f3euQ4H2_0&code_challenge_method=s256&scope=tweet.read%20tweet.write%20users.read%20offline.access
  ```

  After authenticating, you will receive the following message:

  ```bash
  Authenticated! Here's your access token:
  apx-<xxx>
  ```

- With this access token, you can enjoy up to 35 calls per 5 minutes to the X API, which is significantly higher than the standard X API plan.

- If you've obtained a GAME Twitter Access Token via the GAME authentication flow, set it as environment variables (e.g. using a `.env` file with [python-dotenv](https://pypi.org/project/python-dotenv/)):
  ```dotenv
  GAME_TWITTER_ACCESS_TOKEN=apx-<game-twitter-access-token>
  ```

- You can now initialize the Tweepy client directly with it:

  ```python
  import os

  from virtuals_tweepy import Client
  from dotenv import load_dotenv
  
  load_dotenv()
  
  game_twitter_access_token = os.environ.get("GAME_TWITTER_ACCESS_TOKEN")
  
  client = Client(
      game_twitter_access_token=game_twitter_access_token
  )
  ```

### Using your own X API credentials

- If you don't already have one, create an X (Twitter) account and navigate to the [developer portal](https://developer.x.com/en/portal/dashboard).
- Create a project app, generate the following credentials and set them as environment variables(e.g. using a `.env` file with [python-dotenv](https://pypi.org/project/python-dotenv/)):
  ```dotenv
  TWITTER_BEARER_TOKEN=<twitter-bearer-token>
  TWITTER_API_KEY=<twitter-api-key>
  TWITTER_API_KEY_SECRET=<twitter-api-secret-key>
  TWITTER_ACCESS_TOKEN=<twitter-access-token>
  TWITTER_ACCESS_TOKEN_SECRET=<twitter-access-token-secret>
  ```

- If you decide to use your own X API credentials, you can initialize the Tweepy client with them as follows:

  ```python
  import os

  from virtuals_tweepy import Client
  from dotenv import load_dotenv
  
  load_dotenv()
  
  # 1. Twitter API OAuth 2.0
  bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
  
  client = Client(
    bearer_token=bearer_token
  )
  
  # 2. Twitter API OAuth 1.0a
  consumer_key = os.environ.get("TWITTER_API_KEY")
  consumer_secret = os.environ.get("TWITTER_API_KEY_SECRET")
  access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
  access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
  
  client = Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
  )
  ```

Latest version of Python and older versions not end of life (bugfix and security) are supported.

## Acknowledgments

This project is a modified version of [Tweepy](https://github.com/tweepy/tweepy) by [Virtuals Protocol](https://virtuals.io/), originally created by Joshua Roesslein.
Original work is Copyright (c) 2009-2023 Joshua Roesslein and is licensed under the MIT License.
