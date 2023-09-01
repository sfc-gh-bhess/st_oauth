from urllib.parse import urlencode
import requests
import streamlit as st
import jwt

import string
import random

_STKEY = 'ST_OAUTH'
_DEFAULT_SECKEY = 'oauth'

@st.cache_resource(ttl=300)
def qparms_cache(key):
    return {}

@st.cache_resource(ttl=360000)
def jwks_client(jwks_uri):
    return jwt.PyJWKClient(jwks_uri)

def logout():
    if _STKEY in st.session_state:
        del st.session_state[_STKEY]

def string_num_generator(size):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

def validate_config(config):
    required_config_options = [ 'authorization_endpoint', 
                                'token_endpoint',
                                'jwks_uri',
                                'redirect_uri',
                                'client_id',
                                'client_secret',
                                'scope' ]
    return all([k in config for k in required_config_options])

def show_auth_link(config, label):
    state_parameter = string_num_generator(15)
    query_params = urlencode({'redirect_uri': config['redirect_uri'], 'client_id': config['client_id'], 'response_type': 'code', 'state': state_parameter, 'scope': config['scope']})
    request_url = f"{config['authorization_endpoint']}?{query_params}"
    if st.experimental_get_query_params():
        qpcache = qparms_cache(state_parameter)
        qpcache = st.experimental_get_query_params()
    st.markdown(f'<a href="{request_url}" target="_self">{label}</a>', unsafe_allow_html=True)
    st.stop()
    
def validate_token(token, config):
    signing_key = jwks_client(config['jwks_uri']).get_signing_key_from_jwt(token['access_token'])
    try:
        audience = config['audience'] if 'audience' in config else None
        leeway = config['leeway'] if 'leeway' in config else 0
        data = jwt.decode(token['access_token'], signing_key.key, algorithms=["RS256"], audience=audience, leeway=leeway)
    except (jwt.exceptions.ExpiredSignatureError):
        return False, 'Expired'
    except:
        return False, 'Invalid'
    return True, data[config['identity_field_in_token']] if 'identity_field_in_token' in config and config['identity_field_in_token'] in data else 'OK'

def st_oauth(config=None, label="Login via OAuth"):
    if not config:
        config = _DEFAULT_SECKEY
    if isinstance(config, str):
        config = st.secrets[config]
    if _STKEY in st.session_state:
        token = st.session_state[_STKEY]
        valid, msg = validate_token(token, config)
        if not valid:
            del st.session_state[_STKEY]
            st.warning(f"OAuth Token {msg}")
    if _STKEY not in st.session_state:
        if not validate_config(config):
            st.error("Invalid OAuth Configuration")
            st.stop()
        if 'code' not in st.experimental_get_query_params():
            show_auth_link(config, label)
        code = st.experimental_get_query_params()['code'][0]
        state = st.experimental_get_query_params()['state'][0]
        qpcache = qparms_cache(state)
        qparms = qpcache
        qpcache = {}
        st.experimental_set_query_params(**qparms)
        theaders = {
                        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
                    }
        tdata = {
                    'grant_type': 'authorization_code', 
                    'redirect_uri': config['redirect_uri'],
                    'client_id': config['client_id'],
                    'client_secret': config['client_secret'],
                    'scope': config['scope'],
                    'state': state,
                    'code': code,
                }
        try:
            ret = requests.post(config["token_endpoint"], headers=theaders, data=urlencode(tdata).encode("utf-8"))
            ret.raise_for_status()
        except requests.exceptions.RequestException as e:
            st.error(e)
            show_auth_link(config, label)
        token = ret.json()
        valid, msg = validate_token(token, config)
        if valid:
            st.session_state[_STKEY] = token
        else:
            st.error("Invalid OAuth Token")
            show_auth_link(config, label)

    if _STKEY in st.session_state:
        st.sidebar.button("Logout", on_click=logout)
    return msg
