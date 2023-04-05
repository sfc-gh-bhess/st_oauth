# OAuth component for Streamlit

This Python package implements a "gate" for the Streamlit app
that will only allow the app to proceed once the user authenticates
via OAuth to a configured OAuth provider.

Simply include the component at the top of the Streamlit app, such as
```
import streamlit as st
from st_oauth import st_oauth

st.markdown("## This (and above) is always seen")
id = st_oauth()
st.markdown("## This (and below) is only seen after authentication")
```

The token is stored in Streamlit session state and is validated
on each re-run of the Streamlit. If the token is expired, it is cleared
from the session state and the user is prompted to reauthenticate. There
is also an option to logout (a logout button is placed in the sidebar).

## Installation 

You can install directly from github with this command:
```
pip install git+https://github.com/sfc-gh-bhess/st_oauth.git
```
Note that python 3.8 is the only supported python version currently.

To install directly from github via pipenv, use:
```
pipenv install git+https://github.com/sfc-gh-bhess/st_oauth.git#egg=st_oauth
```

## Description

This package adds an OAuth component that will not allow the app to 
continue until the user authenticates via OAuth. The call to `st_oauth()`
will return the value in the OAuth token that contains the identity
(`sub` or `upn`, as configured).

The `st_oauth()` function takes 2 optional parameters: `config` and `label`.
The `label` is the text to use in the link presented to log in. By default, 
the label is `Login via OAuth`.

The `st_oauth()` function also needs a configuration dictionary to function.
The necessary fields of the function are:
* `authorization_endpoint` - the URL to use to get an authorization code
* `token_endpoint` - the URL to use to trade an authorization code for a token
* `jwks_uri` - the URL to use to retrieve the JWKS signing key for the tokens
* `redirect_uri` - the URL that is configured in the OAuth provider as the redirect URL (it should be the URL of the Streamlit app itself)
* `client_id` - the client ID, as configured in the OAuth provider
* `client_secret` - the client secret for the client ID, as configured in the OAuth provider
* `scope` - the OAuth scope to use, as configured in the OAuth provider
* `audience` - the audience as configured in the OAuth provider
* `identity_field_in_token` - which field in the returned token that contains the identity (usually it is `sub` or `upn`). This is the field that will be returned from the `st_oauth()` call.

If `st_oauth()` is called without a `config` parameter, it will look for the 
configuration parameters in the secrets file (`st.secrets`) using the default
name `oauth`.
```
id = st_oauth()
```

The `.streamlit/secrets.toml` file would look something like this:
```
[oauth]
authorization_endpoint = "<OAUTH AUTH ENDPOINT usually ending in /v1/authorize>"
token_endpoint = "<OAUTH TOKEN ENDPOINT usually ending in /v1/token>"
jwks_uri = "<OAUTH JWKS ENDPOINT>"
redirect_uri = "<REDIRECT URI - this Streamlit's location>"
client_id = "<OAUTH CLIENT ID>"
client_secret = "<OAUTH CLIENT SECRET>"
scope = "<OAUTH SCOPE>"
audience = "<OAUTH AUDIENCE>"
identity_field_in_token = "<OAUTH TOKEN ID FIELD - sub or upn>"
```

If `st_oauth()` is called with a string valued `config` parameter, it will look for the
configuration parameters in the secrets file (`st.secrets`) using the supplied name.
```
id = st_oauth('my_oauth')
```

The `.streamlit/secrets.toml` file would look something like this:
```
[my_oauth]
authorization_endpoint = "<OAUTH AUTH ENDPOINT usually ending in /v1/authorize>"
...
```

If `st_oauth()` is called with a dictionary for the `config` parameter,
it will use those as the parameter values.
```
oauth_params = {'authorization_enddpoint': ...} # Or any way to create the dictionary
id = st_oauth(oauth_params)
```

### Multipage Streamlit Apps
This component supports multipage Streamlit apps. Just include
the call to `snowauth_session()` at the top of every page. If 
the user is not logged in, they will be presented with the login
link. Once authenticated, they will return to the main page of the
Streamlit app.

## Configuring your OAuth provider
Consult the documentation for your OAuth provider on how to create a new
application integration for `st_oauth`.

### Lower-level notes
If you do need to test to see if the session is already cached,
you can test it yourself directly:
```
if st_oauth._STKEY in st.session_state:
    do_something()
```