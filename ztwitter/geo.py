#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: geo.py
Author: zlamberty
Created: 2015-06-08

Description:
    helper functions for twitter geocode helps

Usage:
    <usage>

"""

import logging
import requests

import constants


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

LAT_LNG = (
    "https://api.twitter.com/1.1/geo/reverse_geocode.json"
    "?lat={lat:}&long={lng:}&granularity=city"
)
GET_TID = "https://api.twitter.com/1.1/geo/id/{tid:}.json"


logger = logging.getLogger(__name__)


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def bounding_box_from_tid(auth, tid, tidUrl=GET_TID):
    """ doc """
    return requests.get(
        url=tidUrl.format(tid=tid),
        auth=auth
    ).json()


def tid_from_rev_geocode_json(json):
    """ expecting a twitter json response from a reverse_geocode call, return
        the twitter id

    """
    return json['result']['places'][0]['id']


def tid_from_lat_lng(auth, lat, lng, latLngUrl=LAT_LNG):
    """ doc """
    return tid_from_rev_geocode_json(
        requests.get(
            url=latLngUrl.format(lat=lat, lng=lng),
            auth=auth
        ).json()
    )
