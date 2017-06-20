# a00_command
python package for receiving json rpc commands via Firebase


## Usage

```python

    from a00_command import Commander

    CREDS_PATH = "/path/to/credentials.json"
    GOOGLE_API_KEY = "google_api_key"
    CUSTOM_TOKEN_URL = "http://augment00.org/api/firebase-token/1234567890"
    AUTH_DOMAIN = "project-name.firebaseapp.com"
    DB_URL = "https://project-name.firebaseio.com"


    # read in the credentials from file
    with open(CREDS_PATH) as f:
        creds = json.loads(f.read())

    # make one
    commander = Commander(creds,
                          GOOGLE_API_KEY,
                          CUSTOM_TOKEN_URL,
                          AUTH_DOMAIN,
                          DB_URL)


    # add a function to be called by the commander
    commander.add_function(name, func)

    # start it
    commander.start()
    time.sleep(2)

    # ask it to process any waiting messages
    commander.tick()

    # stop it
    commander.stop()

```