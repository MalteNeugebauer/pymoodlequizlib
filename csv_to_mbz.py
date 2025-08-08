#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 12:13:28 2025

@author: malte
"""

#%% Import modules.
import stackassessxmllib
import versions.qv_instant_tutoring as qv_instant_tutoring
import importlib # For reloading modules in development state.
importlib.reload(stackassessxmllib)
importlib.reload(qv_instant_tutoring)

#%% Main routine

Pools = stackassessxmllib.generate_quizzes_mbz_from_file(filepath="exercises/test_exercises.csv", template_path="backup-moodle2-empty-quiz-with-interactive-mode", version=qv_instant_tutoring.InstantTutoringTEDRelVersion, exclude_column="already_parsed", delimiter=";")