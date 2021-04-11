""" Quickstart script for InstaPy usage """
# -*- coding: UTF-8 -*-
# imports
from instapy import InstaPy
from instapy import smart_run
from instapy import set_workspace


# set workspace folder at desired location (default is at your home folder)
set_workspace(path=None)

# get an InstaPy session!
session = InstaPy(username="jules.dubois45",
                password="vache1s2")

with smart_run(session):
    # general settings
    session.set_dont_include(["friend1", "friend2", "friend3"])

    # activity
    #session.like_by_tags(["natgeo"], amount=10)

    session.get_all_tags_captions(["jeuconcours"], amount = 20)
    #session.like_by_tags(["jeuconcours"], amount = 20)
