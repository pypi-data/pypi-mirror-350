# google-contact-local-python-package

## Enable People API

https://support.google.com/googleapi/answer/6158841?hl=en<br>

## How to run google-contact-local

```bash
# Clone the repository
git clone https://github.com/yourusername/google-contact-local-python-package.git
cd google-contact-local-python-package

# Create and activate a virtual environment
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

cd google-contact-local-python-package
cd google_contact_local

```

**You need to authinticate for the first time using the one_time_auth.py file in google-contact-local-python-package/google_contact_local**

**Before using the script you need to check if your username/email is added to the test user list in the google claud platform(check/ask Tal to add you)**


after regestiring as a test user run, update the email variable in one_time_auth.py to your test user 

then run:

```bash
python one_time_auth.py
```

click on the link printed the terminal, it will open "Choose Account Page" choose @circ.zone email
allow all the premissions asked bby the app(contact access for this repo)

Click "continue"
and you should be redirected to a url that end with: "execute-api.us-east-1.amazonaws.com/play1/api/v1/googleAccount/getCode?"

and the message shown need to start with: "Successfully authenticated - access_token saved in the database for the given state access_token, access_token: ******"

## Running the tests

You need to have at least one contact in https://contacts.google.com/, **make sure most of the fields are full**


## Running the tests in the GitHub action common error
Auth code not found in the database

check if the access token expired using:

```sql
    SELECT  user_external_id, access_token, refresh_token, expiry, is_refresh_token_valid, oauth_state 
    FROM `user_external`.`user_external_latest_token_general_view` 
    WHERE username = "play1@circ.zone"
    ORDER BY eu.start_timestamp DESC
```

ask for access to the play1 email and re-auth it with one_time_auth.py script 


### Pull contacts from Google Contacts

Run google_contacts.pull_contacts_with_stored_token("example@example.com")
This will pull the contacts details from your Google Contacts
and store them in the database in https://console.cloud.google on the app OAuth consent screen

## Google People API documentation

https://developers.google.com/people/api/rest<br>

To create local package and remote package layers (not to create GraphQL and REST-API layers)

# Google Contacts

Register in `https://developers.google.com/people/v1/getting-started`<br>

In the credentials section in google cloud application, create a new Create OAuth client ID credential of type "Web
application".
The Authorised redirect URIs must have an URL exactly identical to the GOOGLE_REDIRECT_URIS environment variable and if
it has a port number it must also be passed to the method "run_local_server"
