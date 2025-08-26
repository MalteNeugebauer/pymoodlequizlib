#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 13:06:05 2025

@author: malte
"""
import stackassessxmllib
import json
import pathlib

#%% Basic defintions
current_dir = pathlib.Path(__file__).parent

#%%------------------------------------PREVIEW---------------------------------
def normal_version_config_text(**kwargs):
    Exercises = kwargs.get("Exercises")
    if Exercises == None:
        print("no exercises found for config callback of preview version")
        return ""

    info_dict = {}
    groups = []
    groups.append({"id":"start", "name":"Start","questions":["i"]})

    SortedExercises = sorted(Exercises, key=lambda x:f"t{x.topic_number}_{x.topic_id}_{x.exercise_number}_{x.exercise_part}")

    previous_group = ""
    for Exercise in SortedExercises:
        group_identifier = f"t{Exercise.topic_number}_{Exercise.topic_id}_{Exercise.exercise_number}"
        if previous_group == group_identifier:
            groups[-1]["questions"].append(Exercise.exercise_part)
        else:
            groups.append({"id":group_identifier, "name":Exercise.topic_label , "questions":[Exercise.exercise_part]})
        previous_group = group_identifier

    info_dict["groups"] = groups
    return json.dumps(info_dict)


NormalVersion = stackassessxmllib.QuestionVersion("normal", False, '<script src="https://marvin.hs-bochum.de/~mneugebauer/alquiz-qpool-normal.js"></script>', current_dir / "start-normal.xml", current_dir / "config-normal.xml", callback_last_quiz_element_text=normal_version_config_text, needs_exercises_as_callback_arg=True)