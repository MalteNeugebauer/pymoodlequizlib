#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 12:18:01 2025

@author: malte
"""
import stackassessxmllib
import json
import re
from lxml import etree
import pathlib

#%% Basic defintions
current_dir = pathlib.Path(__file__).parent
alquiz_instant_tutoring_script_tag = '<script src="https://marvin.hs-bochum.de/~mneugebauer/alquiz-qpool-instant-tutoring.js"></script>'

#%%------------------------------------INTELLIGENT TUTORING SYSTEM----------------------------------

def it_version_config_text(**kwargs):
    text = ""
    Exercises = kwargs.get("Exercises")
    if Exercises == None:
        print("no exercises found for config callback of instant tutoring version")
        return ""

    seed_limit = kwargs.get("seed_limit")
    if seed_limit == None:
        seed_limit = 0
        print("continue without seed limit in an instant tutoring version")

    info_dict = {}
    groups = {}
    groups["start"] = "Start"
    questions = {}
    questions["start"] = {"name":"Start", "group":"start"}
    #, "type":"instruction"

    SortedExercises = sorted(Exercises, key=lambda x:f"t{x.topic_number}_{x.topic_id}_{x.exercise_number}_{x.exercise_part}")


    for Exercise in SortedExercises:
        #Check amount of possible variants
        seed_amount = 0
        for seed in Exercise.root.iterchildren("deployedseed"):
            seed_amount+=1
        if seed_amount < 1:
            print(f"No seed given for t{Exercise.topic_number}-{Exercise.exercise_number}-{Exercise.exercise_part}.")
            seed_amount = 1

        variant_amount = seed_amount if (seed_limit == 0 or seed_amount < seed_limit) else seed_limit

        group_identifier = f"t{Exercise.topic_number}_{Exercise.topic_id}_{Exercise.exercise_number}"
        group_check = groups.get(group_identifier)
        if group_check == None:
            groups[group_identifier] = Exercise.topic_label
        question_identifier = f"{group_identifier}_{Exercise.exercise_part}"
        questions[question_identifier] = {"name":Exercise.exercise_description, "variants":variant_amount}
        text = f"{text}t{Exercise.topic_number}_{Exercise.exercise_number}_{Exercise.exercise_part}\n"
    #print(groups)
    info_dict["groups"] = groups
    info_dict["questions"] = questions
    #print(info_dict)

    go_back_text = "Sie sind in der Konfigurationsdatei vom Digitalen Mentor gelandet. Klicken sie bitte auf eine der anderen Fragen in der Test-Navigation, um zurück zum Übungsraum zu gelangen."
    lang = kwargs.get("lang")
    if(lang != None and lang != "de"):
        go_back_text = "You have landed in the configuration file of the Digital Mentor. Please click on one of the other questions in the test navigation to return to the training area."

    return f'<script>window.location.href = document.querySelector("[id*=quiznavbutton]").href;</script>\n<p>{go_back_text}</p>\n{json.dumps(info_dict)}'

def it_version_add_to_script_text(**kwargs):
    text = ""
    Question = kwargs.get("Question")
    if Question == None:
        print("no question found for callback of add to script text")
        return "start"
    text = f"<script>ALQuiz.setCurrentQuestionId('t{Question.topic_number}_{Question.topic_id}_{Question.exercise_number}_{Question.exercise_part}')</script>"
    return text

def it_version_change_text(**kwargs):
    #Change inputs
    Question = kwargs.get("Question")
    if Question == None:
        print("no question found for input change")
        return False
    #Turn algebraic input into equivalence reasoning if desired
    if Question.its_keep_orig_input != None and Question.its_keep_orig_input == 1:
        print(f"ITS version: `{Question.debugging_id}`'s input fields will not be changed due to user definition.")
        return False
    for input_element in Question.root.iterchildren("input"):
        handling = False
        for input_type_element in input_element.iterchildren("type"):
            if(input_type_element.text == "algebraic"):
                input_type_element.text = "equiv"
                handling = True
        if handling == False:
            continue

        for input_options_element in input_element.iterchildren("options"):
            if input_options_element.text == None or input_options_element.text.strip() == "":
                input_options_element.text = "hideequiv"
            elif not "hideequiv" in input_options_element.text:
                input_options_element.text = f"{input_options_element.text}, hideequiv"
        name = ""
        for input_name_element in input_element.iterchildren("name"):
            name = input_name_element.text
        if name == "":
            continue

        name_replacement = f"{name}_its_replaced"
        search_sans_name = re.compile(f'{name}')

        for input_tans_element in input_element.iterchildren("tans"):
            input_tans_element.text = f"[{input_tans_element.text}]"

        for prt in Question.root.iterchildren("prt"):
            for node in prt.iterchildren("node"):
                for sans in node.iterchildren("sans"):
                    if name in sans.text:
                        sans.text = search_sans_name.sub(name_replacement, sans.text)
                    #else:
                    #    print(f"{name} is not in {sans.text} ({Question.exercise_description})")
            if Question.its_keep_orig_input != 1:
                for feedbackvariables in prt.iterchildren("feedbackvariables"):
                    for feedbackvariablestext in feedbackvariables.iterchildren("text"):
                        if feedbackvariablestext != None and feedbackvariablestext.text != None:
                            replace_ans_fields_text = f"/*---Replacing student answer input values to let original code align with equivalence reasoning nature of Instant Tutoring Version---*/\n{name_replacement}:last({name});\n"
                            feedbackvariablestext.text = search_sans_name.sub(name_replacement, feedbackvariablestext.text)
                            feedbackvariablestext.text = f"{replace_ans_fields_text}\n{feedbackvariablestext.text}"
    return True


it_fixed_seed_amount = 4
InstantTutoringVersion = stackassessxmllib.QuestionVersion("instant-tutoring", True, alquiz_instant_tutoring_script_tag, current_dir / "start-instant-tutoring.xml", current_dir / "config-instant-tutoring.xml", it_fixed_seed_amount, True, callback_last_quiz_element_text=it_version_config_text, callback_add_to_script=it_version_add_to_script_text, callback_change_before_clone=it_version_change_text, needs_exercises_as_callback_arg=True, seed_limit=it_fixed_seed_amount)

#%%------------------------------------INTELLIGENT TUTORING WITH ABSOLUTE TED FEEDBACK SYSTEM----------------------------------
## Some functions are reused from previous cells. Please run that cells first.
def it_version_ted_feedback_abs_change_text(**kwargs):
    success = it_version_change_text(**kwargs)
    if success == False or success == None:
        return success
    
    Question = kwargs.get("Question")
    if Question == None:
        print("no question found for input change (it ted abs)")
        return False
    
    # Add necessary function to question variables.
    maxima_code_convert_to_tree = """
converttotree(expr):= block(
   [op, args,expri],
   if atom(expr) then
     return([string(expr)])
   elseif ( is(op(expr)="-") and is(length(args(expr))=1)) and is(atom(first(args(expr)))) then
     return ["-",string(first(args(expr)))]
   elseif ( is(op(expr)="-") and is(length(args(expr))=1)) then (
     expri : first(args(expr)),
     if ( is(op(expri)="/") and is(length(args(expri))=2) and integerp(first(args(expri))) and integerp(second(args(expri))) ) then
     return([sconcat("-",string(first(args(expri))),"/",string(second(args(expri))))])
   )
   elseif ( is(op(expr)="/") and is(length(args(expr))=2) and integerp(first(args(expr))) and integerp(second(args(expr))) ) then
     return([sconcat(string(first(args(expr))),"/",string(second(args(expr))))])
   else 0,
   op : op(expr),
   args : args(expr),
   return(append([op],makelist(converttotree(a), a, args)))
);
"""

    for questionvariables_element in Question.root.iterchildren("questionvariables"):
        for questionvariables_text in questionvariables_element.iterchildren("text"):
            questionvariables_text.text = f"{questionvariables_text.text}{maxima_code_convert_to_tree}"
    
    ## First, get all the PRT nodes' teacher's answers, that give full points.
    fullscore_tans = []
    for prt in Question.root.iterchildren("prt"):
        for node in prt.iterchildren("node"):
            truescore_value = None
            for truescore_element in node.iterchildren("truescore"):
                truescore_value = truescore_element.text
            
            if truescore_value != "1":
                # Not found or it's not the node we are looking for.
                continue
            
            tans_value = None
            for tans_element in node.iterchildren("tans"):
                tans_value = tans_element.text
                
            if tans_value == None:
                # Not found.
                continue
            
            fullscore_tans.append(tans_value)
    
    text_to_add = ""
    for fullscore_answer in fullscore_tans:
        text_to_add = f'{text_to_add}\n<div class="maxima-code-output mco-teacher" style="display: none;">{{@sconcat(converttotree({fullscore_answer}))@}}</div>'

    # Assume `last(ans1)` always to be the student's input.
    text_to_add = f'{text_to_add}\n<div class="maxima-code-output mco-student" style="display: none;">{{@sconcat(converttotree(last(ans1)))@}}</div>'
    
    # Add Javascript code that calculates the TED on the fly and formulates something out of it.
    # As the fetched script is not executed, this doesn't work. It has to be initiated by the main script ...qpool-instant-tutoring.js.
    #text_to_add = f"{text_to_add}\n<script>{javascript_code_formulate_distance}</script>"
    # At least we can insert a field for the feedback
    text_to_add = f'{text_to_add}\n<div class="maxima-code-output mco-ted-feedback mco-ted-abs"></div>'
    
    # Add script to the PRT node, that has no following node on false, or that are true but give 0 points and have no following node. Assume that node(s) to be the one(s) that say only "False" and mean "False and I don't know why".
    for prt in Question.root.iterchildren("prt"):
        for node in prt.iterchildren("node"):
            falsenextnode_value = None
            for falsenextnode_element in node.iterchildren("falsenextnode"):
                falsenextnode_value = falsenextnode_element.text
            falsescore_value = None
            for falsescore_element in node.iterchildren("falsescore"):
                falsescore_value = falsescore_element.text
                
            truenextnode_value = None
            for truenextnode_element in node.iterchildren("truenextnode"):
                truenextnode_value = truenextnode_element.text
            truescore_value = None
            for truescore_element in node.iterchildren("truescore"):
                truescore_value = truescore_element.text
            
            #if (falsenextnode_value != "-1" or falsescore_value != "0") and (truenextnode_value != "-1" or truescore_value != "0"):   
            
            target_outcomes = []
            if (falsenextnode_value == "-1" and falsescore_value == "0"):
                target_outcomes.append("false")
            if (truenextnode_value == "-1" and truescore_value == "0"):
                target_outcomes.append("true")
            if(len(target_outcomes) == 0):
                # Not found or it's not the node we are looking for.
                continue
            
            for target_outcome in target_outcomes:
                for feedback_element in node.iterchildren(f"{target_outcome}feedback"):
                    for feedback_text_element in feedback_element.iterchildren("text"):
                        previous_text = ""
                        if feedback_text_element.text != None:
                            previous_text = feedback_text_element.text
                        if target_outcome == "true":
                            feedback_text_element.text = etree.CDATA(f"{text_to_add}{previous_text}")
                        else:
                            feedback_text_element.text = etree.CDATA(f"{previous_text}{text_to_add}")
    
    return True
            
InstantTutoringTEDAbsVersion = stackassessxmllib.QuestionVersion("instant-tutoring-ted-abs", True, alquiz_instant_tutoring_script_tag, current_dir / "start-instant-tutoring.xml", current_dir / "config-instant-tutoring.xml", it_fixed_seed_amount, True, callback_last_quiz_element_text=it_version_config_text, callback_add_to_script=it_version_add_to_script_text, callback_change_before_clone=it_version_ted_feedback_abs_change_text, needs_exercises_as_callback_arg=True, seed_limit=it_fixed_seed_amount)

#%%------------------------------------INTELLIGENT TUTORING WITH RELATIVE TED FEEDBACK SYSTEM----------------------------------
## Some functions are reused from previous cells. Please run that cells first.
def it_version_ted_feedback_rel_change_text(**kwargs):
    success = it_version_ted_feedback_abs_change_text(**kwargs)
    if success == False or success == None:
        return success
    
    Question = kwargs.get("Question")
    if Question == None:
        print("no question found for input change (it ted abs)")
        return False
    
    # Replace the beforehand defined feedback field for absolute feedback to a relative feedback field.
    search = '<div class="maxima-code-output mco-ted-feedback mco-ted-abs"></div>'
    replace = '<div class="maxima-code-output mco-ted-feedback mco-ted-rel"></div>'
    
    outcomes = ["true", "false"]
    for prt in Question.root.iterchildren("prt"):
        for node in prt.iterchildren("node"):
            for outcome in outcomes:
                for feedback_element in node.iterchildren(f"{outcome}feedback"):
                    for feedback_text_element in feedback_element.iterchildren("text"):
                        if feedback_text_element.text != None and search in feedback_text_element.text:
                            feedback_text_element.text = etree.CDATA(re.sub(search, replace, feedback_text_element.text))
    return True

InstantTutoringTEDRelVersion = stackassessxmllib.QuestionVersion("instant-tutoring-ted-rel", True, alquiz_instant_tutoring_script_tag, current_dir / "start-instant-tutoring.xml", current_dir / "config-instant-tutoring.xml", it_fixed_seed_amount, True, callback_last_quiz_element_text=it_version_config_text, callback_add_to_script=it_version_add_to_script_text, callback_change_before_clone=it_version_ted_feedback_rel_change_text, needs_exercises_as_callback_arg=True, seed_limit=it_fixed_seed_amount)