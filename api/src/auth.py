import requests
from urllib.parse import parse_qs, urlparse

def get_authentication_token(npsso):
    authorize_url = "https://ca.account.sony.com/api/authz/v3/oauth/authorize"
    params = {
        "access_type": "offline",
        "client_id": "09515159-7237-4370-9b40-3806e67c0891",
        "response_type": "code",
        "scope": "psn:mobile.v2.core psn:clientapp",
        "redirect_uri": "com.scee.psxandroid.scecompcall://redirect"
    }

    try:
        response = requests.get(authorize_url, params=params, cookies={"npsso": npsso}, allow_redirects=False)
    except requests.HTTPError:
        print("Error: Check npsso")
        return None

    if "Location" in response.headers:
        redirect_url = response.headers["Location"]
        parsed_url = urlparse(redirect_url)
        query_params = parse_qs(parsed_url.query)
        if "code" in query_params:
            code = query_params["code"][0]
        else:
            print("Error: Unable to extract authorization code")
            return None
    else:
        print("Error: Unable to find the redirect URL")
        return None

    token_url = "https://ca.account.sony.com/api/authz/v3/oauth/token"
    body = {
        "code": code,
        "redirect_uri": "com.scee.psxandroid.scecompcall://redirect",
        "grant_type": "authorization_code",
        "token_format": "jwt"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic MDk1MTUxNTktNzIzNy00MzcwLTliNDAtMzgwNmU2N2MwODkxOnVjUGprYTV0bnRCMktxc1A="
    }

    try:
        response = requests.post(token_url, data=body, headers=headers)
        response.raise_for_status()
        token = response.json().get("access_token")
        if token:
            return token
        else:
            return None
    except requests.HTTPError:
        return None
