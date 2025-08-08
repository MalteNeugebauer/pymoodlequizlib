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

version = qv_instant_tutoring.InstantTutoringTEDRelVersion

Pools = stackassessxmllib.generate_quizzes_mbz_from_file(filepath="exercises/test_exercises.csv", template_path="backup-moodle2-empty-quiz-with-interactive-mode", version=version, exclude_column="already_parsed", delimiter=";")

# Overview of versions
## version = None # Moodle Default version.
## version = qv_preview.NormalVersion # Simple manipulations, e.g., replacing numerical by alphabetical enumeration.
## version = qv_instant_tutoring.InstantTutoringVersion # Instant Tutoring with default feedback.
## version = qv_instant_tutoring.InstantTutoringTEDAbsVersion # Instant Tutoring with additional absolute distance feedback.
## version = qv_instant_tutoring.InstantTutoringTEDRelVersion # Instant Tutoring with additional similarity based feedback.
## version = qv_math_magician.MathMagicianVersion # Role Play Game Version