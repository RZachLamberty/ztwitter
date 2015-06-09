#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: auth.py
Author: zlamberty
Created: 2015-06-08

Description:
    Module for twitter utility functions

Usage:
    <usage>

"""

import logging
import requests
import yaml

import constants

from requests_oauthlib import OAuth1
from urlparse import parse_qs


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token={}"
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

logger = logging.getLogger(__name__)
logging.getLogger('requests').setLevel(logging.INFO)
logging.getLogger('oauthlib').setLevel(logging.INFO)
logging.getLogger('requests_oauthlib').setLevel(logging.INFO)


# ----------------------------- #
#   authentication helpers      #
# ----------------------------- #

class ZtwitterAuthError(Exception):
    pass


def load_auth_from_yaml(f):
    """ load a yaml file that should contain keys 'key' and 'secret'. """
    with open(f, 'rb') as fIn:
        auth = yaml.load(fIn)
    if not all(k in auth for k in ['key', 'secret']):
        raise ZtwitterAuthError(
            "yaml file improperly formatted; requires both 'key' and "
            "'secret'"
        )
    return auth


# ----------------------------- #
#   initial auth setup          #
# ----------------------------- #

def setup_oauth(key, secret, tokenUrl=REQUEST_TOKEN_URL, authUrl=AUTHORIZE_URL,
                accessUrl=ACCESS_TOKEN_URL):
    """ Authorize your app via identifier. """
    credentials = get_oauth_credentials(key, secret, tokenUrl)

    oauth = verify_oauth(key, secret, credentials, authUrl)

    # Finally, Obtain the Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]

    return token, secret


def get_oauth_credentials(key, secret, tokenUrl):
    oauth = OAuth1(client_key=key, client_secret=secret)
    r = requests.post(url=tokenUrl, auth=oauth)
    return parse_qs(r.content)


def verify_oauth(key, secret, credentials, authUrl=AUTHORIZE_URL):
    resourceOwnerKey = credentials.get('oauth_token')[0]
    resourceOwnerSecret = credentials.get('oauth_token_secret')[0]

    # Authorize
    authorize_url = authUrl.format(resourceOwnerKey)

    logger.warning('Please go here and authorize: {}'.format(authorize_url))

    verifier = raw_input('Please input the verifier: ')
    oauth = OAuth1(
        client_key=key,
        client_secret=secret,
        resource_owner_key=resourceOwnerKey,
        resource_owner_secret=resourceOwnerSecret,
        verifier=verifier
    )
    return oauth


# ----------------------------- #
#   loading auth                #
# ----------------------------- #

def get_oauth(key, secret, tokenUrl=REQUEST_TOKEN_URL, authUrl=AUTHORIZE_URL,
              accessUrl=ACCESS_TOKEN_URL):
    oauthToken, oathSecret = setup_oauth(
        key, secret, tokenUrl, authUrl, accessUrl
    )
    oauth = OAuth1(
        client_key=key,
        client_secret=secret,
        resource_owner_key=oauthToken,
        resource_owner_secret=oathSecret
    )
    return oauth
