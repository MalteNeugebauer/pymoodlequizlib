#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  4 11:14:26 2025

@author: malte
"""

#%% Import modules.
import stackassessxmllib
import importlib # For reloading modules in development state.
importlib.reload(stackassessxmllib)

#%% Main routine

table = stackassessxmllib.moodlexml_to_csv(filepath="import_example/test_exercsises.xml", output="output/output.csv", index=False, header=True)