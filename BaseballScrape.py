#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:33:01 2021

@author: nikmiklyukh
"""

import requests
import json

page = requests.get('http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/teams')
jsonText = page.json()
for i in 
print(jsonText['sports'][0]['leagues'][0]['teams'][0]['team']['name'])
