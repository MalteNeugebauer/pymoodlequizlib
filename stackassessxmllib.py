#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 09:30:11 2025

@author: malte
"""

from lxml import etree
import copy
import pandas as pd
import json
import re
import pathlib # For checking if a directory exists.
import distutils # For copying files and folders.
import time # For adding time information into questions.
import subprocess # For running terminal commands.
import math # For floor function.

parser = etree.XMLParser(strip_cdata=False)

default_question_xml = """<quiz>
<!-- question: 0  -->
  <question type="category">
    <category>
      <text>$course$/top/Default for Test-Kurs 4 (EAK)</text>
    </category>
    <info format="moodle_auto_format">
      <text>The default category for questions shared in context 'Test-Kurs 4 (EAK)'.</text>
    </info>
    <idnumber></idnumber>
  </question>

<!-- question: 0  -->
  <question type="category">
    <category>
      <text>$course$/top/Default for Test-Kurs 4 (EAK)/Export</text>
    </category>
    <info format="html">
      <text></text>
    </info>
    <idnumber></idnumber>
  </question>

<!-- question: 17885  -->
  <question type="stack">
    <name>
      <text>Default Question 1.1</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[<p></p><p>[[input:ans1]] [[validation:ans1]][[feedback:prt1]]</p>]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text></text>
    </generalfeedback>
    <defaultgrade>1.0000000</defaultgrade>
    <penalty>0.1000000</penalty>
    <hidden>0</hidden>
    <idnumber></idnumber>
    <stackversion>
      <text>2023010400</text>
    </stackversion>
    <questionvariables>
      <text>ta1:1;</text>
    </questionvariables>
    <specificfeedback format="html">
      <text></text>
    </specificfeedback>
    <questionnote>
      <text></text>
    </questionnote>
    <questionsimplify>1</questionsimplify>
    <assumepositive>0</assumepositive>
    <assumereal>0</assumereal>
    <prtcorrect format="html">
      <text><![CDATA[<span style="font-size: 1.5em; color:green;"><i class="fa fa-check"></i></span> Richtige Antwort, gut gemacht!]]></text>
    </prtcorrect>
    <prtpartiallycorrect format="html">
      <text><![CDATA[<span style="font-size: 1.5em; color:orange;"><i class="fa fa-adjust"></i></span> Die Antwort ist teilweise korrekt.]]></text>
    </prtpartiallycorrect>
    <prtincorrect format="html">
      <text><![CDATA[<span style="font-size: 1.5em; color:red;"><i class="fa fa-times"></i></span> Falsche Antwort.]]></text>
    </prtincorrect>
    <multiplicationsign>dot</multiplicationsign>
    <sqrtsign>1</sqrtsign>
    <complexno>i</complexno>
    <inversetrig>cos-1</inversetrig>
    <logicsymbol>lang</logicsymbol>
    <matrixparens>[</matrixparens>
    <variantsselectionseed></variantsselectionseed>
    <input>
      <name>ans1</name>
      <type>algebraic</type>
      <tans>ta1</tans>
      <boxsize>15</boxsize>
      <strictsyntax>1</strictsyntax>
      <insertstars>5</insertstars>
      <syntaxhint></syntaxhint>
      <syntaxattribute>0</syntaxattribute>
      <forbidwords></forbidwords>
      <allowwords></allowwords>
      <forbidfloat>1</forbidfloat>
      <requirelowestterms>0</requirelowestterms>
      <checkanswertype>0</checkanswertype>
      <mustverify>1</mustverify>
      <showvalidation>3</showvalidation>
      <options></options>
    </input>
    <prt>
      <name>prt1</name>
      <value>1.0000000</value>
      <autosimplify>1</autosimplify>
      <feedbackstyle>1</feedbackstyle>
      <feedbackvariables>
        <text></text>
      </feedbackvariables>
      <node>
        <name>0</name>
        <answertest>EqualComAss</answertest>
        <sans>ans1</sans>
        <tans>ta1</tans>
        <testoptions></testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1</truescore>
        <truepenalty></truepenalty>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt1-1-T</trueanswernote>
        <truefeedback format="html">
          <text></text>
        </truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0</falsescore>
        <falsepenalty></falsepenalty>
        <falsenextnode>1</falsenextnode>
        <falseanswernote>prt1-1-F</falseanswernote>
        <falsefeedback format="html">
          <text></text>
        </falsefeedback>
      </node>
      <node>
        <name>1</name>
        <answertest>AlgEquiv</answertest>
        <sans>ans1</sans>
        <tans>ta1</tans>
        <testoptions></testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>0.1</truescore>
        <truepenalty></truepenalty>
        <truenextnode>-1</truenextnode>
        <trueanswernote>prt1-2-T</trueanswernote>
        <truefeedback format="html">
          <text><![CDATA[<p dir="ltr" style="text-align: left;">Du kannst noch weiter vereinfachen.<br></p>]]></text>
        </truefeedback>
        <falsescoremode>-</falsescoremode>
        <falsescore>0</falsescore>
        <falsepenalty></falsepenalty>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>prt1-2-F</falseanswernote>
        <falsefeedback format="html">
          <text></text>
        </falsefeedback>
      </node>
    </prt>
  </question>

</quiz>
"""

default_prt_node_xml = """<node>
<name>999</name>
<answertest>AlgEquiv</answertest>
<sans>1</sans>
<tans>1</tans>
<testoptions></testoptions>
<quiet>0</quiet>
<truescoremode>+</truescoremode>
<truescore>0</truescore>
<truepenalty></truepenalty>
<truenextnode>-1</truenextnode>
<trueanswernote>prt-999-T</trueanswernote>
<truefeedback format="html">
  <text></text>
</truefeedback>
<falsescoremode>-</falsescoremode>
<falsescore>0</falsescore>
<falsepenalty></falsepenalty>
<falsenextnode>-1</falsenextnode>
<falseanswernote>prt-999-F</falseanswernote>
<falsefeedback format="html">
  <text></text>
</falsefeedback>
</node>
"""

# Functions for smoother work with lxml
def extract_child_info_from_xml(root, child_tag, stop_on_first=True, error_if_none=True):
    elem = None
    for candidate in root.iterchildren(child_tag):
        elem = candidate
        if stop_on_first == True:
            break
    if elem == None:
        raise ValueError(f"No information found for child tag {child_tag}.")
    
    return elem
    
def add_child_infos_to_xml(root, name_value_dict):
    list_of_subelements = {}
    for tag, value in name_value_dict.items():        
        element = etree.SubElement(root, tag)
        if value != None:
            element.text = f"{value}"
        list_of_subelements[tag] = element
        
    return list_of_subelements

class QuestionPool:
    def __init__(self, Question_Ver, Raw_Questions):
        self.Question_Ver = Question_Ver
        self.Questions = []

        self.root = etree.Element("quiz")
        self.tree = etree.ElementTree(self.root)

        self.first_elements = []
        self.last_elements = []
        
        self.stamp_iter = 0

        for Question in Raw_Questions:
            CopiedQuestion = copy.deepcopy(Question)

            add_to_script_text = ""
            if self.Question_Ver.callback_add_to_script != None:
                add_to_script_text = self.Question_Ver.callback_add_to_script(Question=CopiedQuestion)

            #Add script and hint (if desired) to exercise text.
            exercise_hint_string = ""
            if self.Question_Ver.show_hint == True:
                exercise_hint_string = "" if pd.isna(Question.exercise_hint) else f'<p class="hint">{Question.exercise_hint}</p>'
            for questiontext_element in CopiedQuestion.root.iterchildren("questiontext"):
                for questiontext_text_element in questiontext_element.iterchildren("text"):
                    questiontext_text_element.text = etree.CDATA(f"{Question_Ver.script_on_init}{add_to_script_text}{questiontext_text_element.text}{exercise_hint_string}")


            if self.Question_Ver.callback_change_before_clone != None:
                self.Question_Ver.callback_change_before_clone(Question=CopiedQuestion)

            if self.Question_Ver.variants_as_single == True:
                print("special handling for variants as single")

                seeds = []
                for seed in CopiedQuestion.root.iterchildren("deployedseed"):
                    seeds.append(copy.deepcopy(seed))
                    CopiedQuestion.root.remove(seed)

                if len(seeds) < 1:
                    print(f"No seed given for t{CopiedQuestion.topic_number}-{CopiedQuestion.exercise_number:02d}-{CopiedQuestion.exercise_part}.")
                    self.Questions.append(CopiedQuestion)
                    continue

                question_clones = []

                seed_amount = len(seeds) if (self.Question_Ver.fixed_seed_amount == 0 or len(seeds) < self.Question_Ver.fixed_seed_amount) else self.Question_Ver.fixed_seed_amount

                for j in range(seed_amount):
                    question_clones.append(copy.deepcopy(CopiedQuestion))
                    question_clones[j].root.append(seeds[j])
                    j+=1

                variant_count = 1
                for question_variant in question_clones:
                    for name_element in question_variant.root.iterchildren("name"):
                        for nametext_element in name_element.iterchildren("text"):
                            nametext_element.text = f"{nametext_element.text} (Auto-Generation Variant {variant_count})"
                    self.Questions.append(question_variant)
                    variant_count+=1

            else:
                self.Questions.append(CopiedQuestion)

        if self.Question_Ver.custom_first_elements_filepath != "":
            custom_first_element_tree = etree.parse(self.Question_Ver.custom_first_elements_filepath, parser)
            custom_first_element_root = custom_first_element_tree.getroot()
            for question_element in custom_first_element_root.iterchildren("question"):
                if question_element.attrib["type"] != "category":
                    self.first_elements.append(question_element)

        if self.Question_Ver.custom_last_elements_filepath != "":
            custom_last_element_tree = etree.parse(self.Question_Ver.custom_last_elements_filepath, parser)
            custom_last_element_root = custom_last_element_tree.getroot()
            for question_element in custom_last_element_root.iterchildren("question"):
                if question_element.attrib["type"] != "category":
                    self.last_elements.append(question_element)

        self.update_xml_tree();

    def get_category_as_xml_element(self, category_name):
        category_question = etree.Element("question", type="category")
        category = etree.SubElement(category_question, "category")
        category_text = etree.SubElement(category, "text")
        info = etree.SubElement(category, "info")
        info.append(etree.Element("text"))
        category_question.append(etree.Element("idnumber"))
        category_text.text = f"$course$/top/Question Pool Digital Mentoring/{self.Question_Ver.name}/{category_name}"
        return category_question

    def update_xml_tree(self):
        self.root = etree.Element("quiz")
        self.tree = etree.ElementTree(self.root)

        if self.first_elements != []:

            if self.Question_Ver.callback_first_quiz_element_text != None:
                text = self.Question_Ver.callback_first_quiz_element_text(**self.Question_Ver.callback_kwargs)
                for questiontext_element in self.first_elements[0].iterchildren("questiontext"):
                    for questiontext_textelement in questiontext_element.iterchildren("text"):
                        questiontext_textelement.text = etree.CDATA(text)

            self.root.append(self.get_category_as_xml_element("000 Start Elements"))
            for starting_element in self.first_elements:
                self.root.append(starting_element)



        for Question in self.Questions:
            last_category = ""
            category_string = f"t{Question.topic_number}_{Question.topic_id}_{Question.exercise_number} {Question.topic_label}"
            if category_string != last_category:
                self.root.append(self.get_category_as_xml_element(category_string))
                last_category = category_string

            self.root.append(Question.root)

        if self.last_elements != []:
            self.root.append(self.get_category_as_xml_element("zzz Config Elements"))
            for finishing_element in self.last_elements:
                self.root.append(finishing_element)

            #change text in finishing element which shall contain the configuration
            if self.Question_Ver.callback_last_quiz_element_text != None:
                text = self.Question_Ver.callback_last_quiz_element_text(**self.Question_Ver.callback_kwargs)
                questions = []
                for question in self.root.iterchildren("question"):
                    questions.append(question)

                last_question = questions[-1]
                for questiontext_element in last_question.iterchildren("questiontext"):
                    for questiontext_text_element in questiontext_element.iterchildren("text"):
                        questiontext_text_element.text = etree.CDATA(text)

    def write_to_xml_file(self, filepath=""):
        if filepath == "":
            filepath = f"output-{self.Question_Ver.name}.xml"
        self.tree.write(filepath, pretty_print=True)
        
    def write_to_mbz_file(self, output_folder="", template_path="./template"):
        # Check if template folder exists.
        template_path_object = pathlib.Path(template_path)
        if not template_path_object.is_dir():
            raise FileNotFoundError("Template path  for Moodle backup file is not a directory.")
            
        path_to_template_folder = template_path_object
        #path_to_template_folder = "./backup-moodle2-empty-quiz-with-interactive-mode/"

        output_path = pathlib.Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
        
        distutils.dir_util.copy_tree(path_to_template_folder, str(output_path))
        
        # Manually create a question bank and insert the questions' references to a manually created quiz file.
        ## Prepare variables for question bank.
        user_id = 34131
        question_category_start_id = 65134
        plugin_entry_iter = 4332
        plugin_input_iter = 1678
        plugin_prt_iter = 4424
        plugin_node_iter = 4327
        plugin_seed_iter = 11667
        
        ## Prepare variables for quiz file.
        question_instance_iter = 1
        question_reference_iter = 1
        ### Get the template quiz file.
        #### Get the correct folder.
        activities_path = output_path / "activities"
        quiz_candidates_path_names = [x.name for x in activities_path.iterdir() if x.is_dir() and x.name.startswith("quiz")]
        ##### Expect the first one to be the desired folder containing the quiz template.
        quiz_template_folder = activities_path / quiz_candidates_path_names[0]
        quiz_tree = etree.parse(quiz_template_folder / "quiz.xml")
        quiz_root = quiz_tree.getroot()
        quiz = None
        for quiz_elem in quiz_root.iterchildren("quiz"):
            quiz = quiz_elem
        #### If the template quiz's sumgrades is set to zero, set to 1. Zero is the default for empty quizzes, which is expected as template. Thus, it has to be set here to an active quiz's value.
        for sumgrades_elem in quiz.iterchildren("sumgrades"):
            sumgrades_value = sumgrades_elem.text
            if float(sumgrades_value) == 0:
                sumgrades_elem.text = "1.00000"
        
        
        question_instances = None
        for question_instances_elem in quiz.iterchildren("question_instances"):
            question_instances = question_instances_elem
            
        etree.strip_elements(question_instances, "question_instance")
        
        #### Get some information from template.
        quiz_id = quiz_root.get("id")
        context_id = quiz_root.get("contextid")
        context_instance_id = quiz_root.get("moduleid")
        
        ## Prepare variables for the reference information file.
        inforef_tree = etree.parse(quiz_template_folder / "inforef.xml")
        inforef_root = inforef_tree.getroot()
        question_categoryref = None
        for question_categoryref_elem in inforef_root.iterchildren("question_categoryref"):
            question_categoryref = question_categoryref_elem
        if question_categoryref == None:
            question_categoryref = etree.SubElement(inforef_root, "question_categoryref")
        
        
        ## Start building question bank and quiz file
        question_bank_root = etree.Element("question_categories")
        
        top_question_category = etree.SubElement(question_bank_root, "question_category")
        top_question_category.set("id", f"{question_category_start_id}")
        for tag, value in {
               "name":"top",
               	"contextid":context_id,
               	"contextlevel":50,
               	"contextinstanceid":context_instance_id,
               	"stamp":self.get_moodle_stamp(),
                "info":None,
                "infoformat":0,
                "parent":0,
                "sortorder":0,
                "idnumber":"$@NULL@$",
                "question_bank_entries":None
            }.items():        
            element = etree.SubElement(top_question_category, tag)
            if value != None:
                element.text = f"{value}"
        
        question_category_default_values = {
            "name":"testcategory",
        	"contextid":context_id,
        	"contextlevel":50,
        	"contextinstanceid":context_instance_id,
        	"stamp":self.get_moodle_stamp(),
            "info":None,
            "infoformat":0,
            "parent":question_category_start_id,
            "sortorder":0,
            "idnumber":"$@NULL@$",
        }
        question_category = etree.SubElement(question_bank_root, "question_category")
        question_category.set("id", f"{question_category_start_id+1}")
        
        ## Add category information into reference information tree.
        for question_category_id in [question_category_start_id, question_category_start_id+1]:
            question_category_id_elem = etree.SubElement(etree.SubElement(question_categoryref, "question_category"), "id")
            question_category_id_elem.text = f"{question_category_id}"
        
        for tag, value in question_category_default_values.items():        
            element = etree.SubElement(question_category, tag)
            if value != None:
                element.text = f"{value}"
                
        question_bank_entries = etree.SubElement(question_category, "question_bank_entries")
        
        question_bank_entry_default_values = {
            "questioncategoryid":question_category_start_id+1,
            "idnumber":"$@NULL@$",
            "ownerid":user_id,
        }
        
        question_versions_default_values = {
            "version":1,
            "status":"ready",
        }
        
        question_bank_entry_id = 54334
        question_versions_id = 13454
        question_id = 8765
        
        slot_iter = 1
        page_iter = 1
        
        #questionRoots = [x.tree for x in self.Questions]      
        
        #for Question in self.Questions:
        for questionroot in self.root.iterchildren("question"):
            # Check for real question
            qtype = questionroot.get("type")
            
            if qtype == "category":
                continue
            question_bank_entry = etree.SubElement(question_bank_entries, "question_bank_entry")
            question_bank_entry.set("id", f"{question_bank_entry_id}")
            add_child_infos_to_xml(question_bank_entry, question_bank_entry_default_values)
                    
            question_version = etree.SubElement(question_bank_entry, "question_version")
            question_versions = etree.SubElement(question_version, "question_versions")
            question_versions.set("id", f"{question_versions_id}")
            add_child_infos_to_xml(question_versions, question_versions_default_values)
                    
            questions = etree.SubElement(question_versions, "questions")
            question = etree.SubElement(questions, "question")
            question.set("id", f"{question_id}")
            
            ## Extract relevant values from question's xml.                    
            question_name = extract_child_info_from_xml(extract_child_info_from_xml(questionroot, "name"), "text").text
            
            questiontext_elem = extract_child_info_from_xml(questionroot, "questiontext")
            ## You may want to check the questiontext_elems "format" attribute and derive the question bank entry's questiontextformat value from it.
            ##...
            questiontext = extract_child_info_from_xml(questiontext_elem, "text").text
            generalfeedback_elem = extract_child_info_from_xml(questionroot, "generalfeedback")
            ## You may want to check the generalfeedback_elem's "format" attribute (switch generalfeedback_elem.get("format"): ... ) and derive the question bank entry's qgeneralfeedbackformat value from it.
            ##...
            
            generalfeedback = extract_child_info_from_xml(generalfeedback_elem, "text").text
            defaultmark = extract_child_info_from_xml(questionroot, "defaultgrade").text
            penalty = extract_child_info_from_xml(questionroot, "penalty").text
            
            timestamp = int(time.time())
            
            question_values = {
                "parent":0,
                "name":question_name,
                "questiontext":questiontext,
                "questiontextformat":1, # see above for further information
                "generalfeedback":generalfeedback,
                "generalfeedbackformat":1, # see above for further information
                "defaultmark":defaultmark,
                "penalty":penalty,
                "qtype":qtype,
                "length":1,
                "stamp":self.get_moodle_stamp(),
                "timecreated":timestamp,
                "timemodified":timestamp,
                "createdby":user_id,
                "modifiedby":user_id,
            }
            add_child_infos_to_xml(question, question_values)
            
            if qtype == "stack":
                plugin_elem = etree.SubElement(question, "plugin_qtype_stack_question")
                options_elem = etree.SubElement(plugin_elem, "stackoptions")
                options_elem.set("id", f"{plugin_entry_iter}")
                
                self.convert_and_append_question_bank_xml_from_question_xml(questionroot, options_elem, simple_convert_names=["questionsimplify", "assumepositive", "assumereal", "multiplicationsign", "sqrtsign", "complexno", "inversetrig", "logicsymbol", "matrixparens", "variantsselectionseed"], flatten_convert_names=["stackversion", "questionvariables", "specificfeedback", "questionnote", "prtcorrect", "prtpartiallycorrect", "prtincorrect"])
                
                further_stackoption_values = {
                    "prtcorrectformat":1,
                    "prtpartiallycorrectformat":1,
                    "prtincorrectformat":1
                }
                add_child_infos_to_xml(options_elem, further_stackoption_values)
                
                
                stackinputs = etree.SubElement(plugin_elem, "stackinputs")
                
                for input_elem in questionroot.iterchildren("input"):
                    copied_node = copy.deepcopy(input_elem)
                    copied_node.tag = "stackinput"
                    copied_node.set("id", f"{plugin_input_iter}")
                    
                    stackinputs.append(copied_node)
                    
                    plugin_input_iter += 1
                
                stackprts = etree.SubElement(plugin_elem, "stackprts")
                
                for prt_elem in questionroot.iterchildren("prt"):
                    stackprt = etree.SubElement(stackprts, "stackprt")
                    stackprt.set("id", f"{plugin_prt_iter}")
                    self.convert_and_append_question_bank_xml_from_question_xml(prt_elem, stackprt, simple_convert_names=["name", "value", "autosimplify", "feedbackstyle"], flatten_convert_names=["feedbackvariables"])
                    
                    stackprtnodes = etree.SubElement(stackprt, "stackprtnodes")
                    for node_elem in prt_elem.iterchildren("node"):
                        stackprtnode = etree.SubElement(stackprtnodes, "stackprtnode")
                        stackprtnode.set("id", f"{plugin_node_iter}")
                        self.convert_and_append_question_bank_xml_from_question_xml(node_elem, stackprtnode, simple_convert_names=["name", "answertest", "sans", "tans", "testoptions", "quiet", "truescoremode", "truescore", "truepenalty", "truenextnode", "trueanswernote", "falsescoremode", "falsescore", "falsepenalty", "falsenextnode", "falseanswernote"], flatten_convert_names=["truefeedback", "falsefeedback"], rename_dict={"name":"nodename"})
                        
                        plugin_node_iter += 1
                    
                        
                    
                    plugin_prt_iter += 1
                
                stackdeployedseeds = etree.SubElement(plugin_elem, "stackdeployedseeds")
                for seed_elem in questionroot.iterchildren("deployedseed"):
                    stackdeployedseed = etree.SubElement(stackdeployedseeds, "stackdeployedseed")
                    stackdeployedseed.set("id", f"{plugin_seed_iter}")
                    copied_seed = copy.deepcopy(seed_elem)
                    copied_seed.tag = "seed"
                    stackdeployedseed.append(copied_seed)
                    
                    plugin_seed_iter += 1
                    
                
                plugin_entry_iter += 1
                
            else:
                print("Handle other kind of exercise")
                
            ## Insert reference into quiz file.
            question_instance = etree.SubElement(question_instances, "question_instance")
            question_instance.set("id", f"{question_instance_iter}")
            question_instance_values = {
                "quizid": quiz_id,
                "slot": slot_iter,
                "page": page_iter,
                "requireprevious": 0,
                "maxmark": 1.0000000,
            }
            add_child_infos_to_xml(question_instance, question_instance_values)
            
            question_reference = etree.SubElement(question_instance, "question_reference")
            question_reference.set("id", f"{question_reference_iter}")
            question_reference_values = {
                "usingcontextid": context_id,
                "component": "mod_quiz",
                "questionarea": "slot",
                "questionbankentryid": question_bank_entry_id,
                "version": "$@NULL@$",
            }
            add_child_infos_to_xml(question_reference, question_reference_values)
            
            question_bank_entry_id+=1
            question_versions_id+=1
            question_id+=1
            question_instance_iter += 1
            question_reference_iter += 1
            
            slot_iter+=1
            page_iter+=1
            
        # Overwrite the contents of the questions.xml file with the content of the generated question bank.
        question_bank_tree = etree.ElementTree(question_bank_root)
        question_bank_tree.write(output_path / "questions.xml")
        
        # Overwrite the contents of the quiz.xml file with the content of the manipulated quiz tree.
        quiz_tree.write(quiz_template_folder / "quiz.xml")
        
        # Overwrite the contents of the reference information file with the content of the manipulated info tree.
        inforef_tree.write(quiz_template_folder / "inforef.xml")
        
        # Compress whole folder with `tar -zcvf output.mbz output/`
        output_file_path = output_path.parent / f"{output_path.name}.mbz"
        command = f'tar -cv -I \'gzip -6\' -f {output_file_path} -C {output_path} .'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        
        
        #print(etree.tostring(question_bank_root))
        #print()
        
    def get_moodle_stamp(self, increment=True):
        self.stamp_iter += 1
        return f"non.existent.domain+automaticallygenerated{self.stamp_iter-1}"
    
    def get_question_bank_xml_dict_from_question_xml(self, root, simple_convert_names=[], flatten_convert_names=[]):
        flatten_convert = {}
        for elem_name in flatten_convert_names:
            flatten_convert[elem_name] =  extract_child_info_from_xml(extract_child_info_from_xml(root, elem_name), "text").text
            
        simple_convert = {}
        for elem_name in simple_convert_names:
            simple_convert[elem_name] = extract_child_info_from_xml(root, elem_name).text
        return flatten_convert | simple_convert
    
    def convert_and_append_question_bank_xml_from_question_xml(self, root_from, root_to, simple_convert_names=[], flatten_convert_names=[], rename_dict={}):
        values = self.get_question_bank_xml_dict_from_question_xml(root_from, simple_convert_names, flatten_convert_names)
        renamed_values = {i if i not in rename_dict else rename_dict[i]:j for i,j in values.items()}
        return add_child_infos_to_xml(root_to, renamed_values)
        

class QuestionVersion:
    def __init__(self, name, variants_as_single=False, script_on_init="", custom_first_elements_filepath="", custom_last_elements_filepath="", fixed_seed_amount=0, show_hint=True, callback_first_quiz_element_text=None, callback_last_quiz_element_text=None, callback_add_to_script=None, callback_change_before_clone=None, needs_exercises_as_callback_arg=False, **callback_kwargs):
        self.name = name
        self.variants_as_single = variants_as_single
        self.script_on_init = script_on_init
        self.custom_first_elements_filepath = custom_first_elements_filepath
        self.callback_first_quiz_element_text = callback_first_quiz_element_text
        self.custom_last_elements_filepath = custom_last_elements_filepath
        self.fixed_seed_amount = fixed_seed_amount
        self.show_hint = show_hint
        self.callback_last_quiz_element_text = callback_last_quiz_element_text
        self.callback_add_to_script = callback_add_to_script
        self.callback_kwargs = callback_kwargs
        self.callback_change_before_clone = callback_change_before_clone
        self.needs_exercises_as_callback_arg = needs_exercises_as_callback_arg


class MoodleQuestion:
    def __init__(self, topic_number, topic_id, exercise_number, exercise_part, topic_label, exercise_description, exercise_variables, exercise_text, exercise_content, exercise_hint, specificfeedback, custom_general_feedback, exercise_note, custom_prt, add_prt_node_on_not_correct, add_prt_node_wa, custom_input, custom_seed, its_keep_orig_input,  question_template_file_path=None):
        self.topic_number = topic_number
        self.topic_id = topic_id
        self.exercise_number = exercise_number
        self.exercise_part = exercise_part
        self.debugging_id = f"{self.topic_number} {self.topic_id} {self.exercise_number} {self.exercise_part}"
        # You may want to uncomment this line for debugging reasons. It serves to identify the currently parsed exercise.
        print(self.debugging_id)
        self.topic_label = topic_label
        self.exercise_description = exercise_description
        self.exercise_variables = exercise_variables
        self.exercise_text = exercise_text
        self.exercise_content = exercise_content
        self.exercise_hint = exercise_hint
        self.specificfeedback = specificfeedback
        self.custom_general_feedback = custom_general_feedback
        self.exercise_note = exercise_note
        self.custom_prt = None if pd.isna(custom_prt) else etree.fromstring(custom_prt, parser)
        self.its_keep_orig_input = its_keep_orig_input

        self.add_prt_node_on_not_correct = add_prt_node_on_not_correct
        self.add_prt_node_wa = None if type(add_prt_node_wa) is not list else [wa for wa in add_prt_node_wa if pd.isna(wa) == False]
        self.custom_input = None if pd.isna(custom_input) else etree.fromstring(custom_input, parser)
        self.custom_seed = None if pd.isna(custom_seed) else etree.fromstring(custom_seed, parser)
        if question_template_file_path == None:
            default_question_quiz_root = etree.fromstring(default_question_xml)
            default_question_quiz_tree = etree.ElementTree(default_question_quiz_root)
        else:
            default_question_quiz_tree = etree.parse(question_template_file_path, parser)
            default_question_quiz_root = default_question_quiz_tree.getroot()
            
        default_prt_node = etree.fromstring(default_prt_node_xml)

        for question_element in default_question_quiz_root.iterchildren("question"):
            if question_element.attrib["type"] == "stack":
                self.root = question_element
                break

        for questionname_element in self.root.iterchildren("name"):
            for questionname_text_element in questionname_element.iterchildren("text"):
                questionname_text_element.text = f"t{self.topic_number}-{self.exercise_number:02d}-{self.exercise_part} {self.exercise_description}"

        exercise_content_string = "" if pd.isna(self.exercise_content) else f"<p>{self.exercise_content}</p>"
        for questiontext_element in self.root.iterchildren("questiontext"):
            for questiontext_text_element in questiontext_element.iterchildren("text"):
                questiontext_text_element.text = etree.CDATA(f"<p>{self.exercise_text}</p>\n{exercise_content_string}")
                
        if not pd.isna(self.specificfeedback):
            for specificfeedback_element in self.root.iterchildren("specificfeedback"):
                for specificfeedback_text_element in specificfeedback_element.iterchildren("text"):
                    specificfeedback_text_element.text = etree.CDATA(self.specificfeedback)

        for questionvariables_element in self.root.iterchildren("questionvariables"):
            for questionvariables_text_element in questionvariables_element.iterchildren("text"):
                questionvariables_text_element.text = self.exercise_variables

        if self.custom_general_feedback is not None and not pd.isna(self.custom_general_feedback):
            for general_feedback_element in self.root.iterchildren("generalfeedback"):
                for general_feedback_text_element in general_feedback_element.iterchildren("text"):
                    general_feedback_text_element.text = etree.CDATA(self.custom_general_feedback)

        if self.exercise_note is not None and not pd.isna(self.exercise_note):
            for questionnote_element in self.root.iterchildren("questionnote"):
                for questionnote_text_element in questionnote_element.iterchildren("text"):
                    questionnote_text_element.text = self.exercise_note


        if self.custom_prt is not None:
            for prt_element in self.root.iterchildren("prt"):
                self.root.remove(prt_element)
            if self.custom_prt.tag == "prt":
                self.root.append(self.custom_prt)
            elif self.custom_prt.tag == "prt_fields":
                for prt_element in self.custom_prt.iterchildren("prt"):
                    self.root.append(prt_element)

        if self.custom_input is not None:
            for old_input_element in self.root.iterchildren("input"):
                self.root.remove(old_input_element)
            if self.custom_input.tag == "input":
                self.root.append(self.custom_input)
            elif self.custom_input.tag == "input_fields":
                for input_element in self.custom_input.iterchildren("input"):
                    self.root.append(input_element)

        if self.custom_seed is not None:
            for old_seed_element in self.root.iterchildren("deployedseed"):
                self.root.remove(old_seed_element)
            if self.custom_seed.tag == "deployedseed":
                self.root.append(self.custom_seed)
            elif self.custom_seed.tag == "seed_fields":
                for seed_element in self.custom_seed.iterchildren("deployedseed"):
                    self.root.append(seed_element)

        if self.add_prt_node_wa is not None:
            i=1
            for wa_text in self.add_prt_node_wa:
                #node_to_add_tree = etree.parse("default-prt-node.xml", parser)
                #node_to_add = node_to_add_tree.getroot()
                node_to_add = copy.deepcopy(default_prt_node)

                for sans_element in node_to_add.iterchildren("sans"):
                    sans_element.text = "ans1"

                for tans_element in node_to_add.iterchildren("tans"):
                    tans_element.text = f"wa{i}"

                for truefeedback_element in node_to_add.iterchildren("truefeedback"):
                    for truefeedback_text_element in truefeedback_element.iterchildren("text"):
                        truefeedback_text_element.text = etree.CDATA(wa_text)


                for prt in self.root.iterchildren("prt"):

                    all_nodes = []
                    node_amount = 0

                    prtname = ""
                    for prtname_element in prt.iterchildren("name"):
                        prtname = prtname_element.text

                    for node in prt.iterchildren("node"):
                        all_nodes.append(node)
                        node_amount+=1

                    if node_amount <= 0:
                        continue

                    #Assume that the last node in the tree is the last node in the flow chart. This code is problematic if e. g. the last node in the XML is one of the first nodes in the prt.
                    last_node = all_nodes[-1]
                    last_node_number = 0
                    for name_element in last_node.iterchildren("name"):
                        last_node_number = int(name_element.text)
                    new_node_name = f"{last_node_number+1}"
                    new_node_label = f"{last_node_number+2}"

                    for name_element in node_to_add.iterchildren("name"):
                        name_element.text = new_node_name

                    for trueanswernote_element in node_to_add.iterchildren("trueanswernote"):
                        trueanswernote_element.text = f"{prtname}-{new_node_label}-T"
                    for falseanswernote_element in node_to_add.iterchildren("falseanswernote"):
                        falseanswernote_element.text = f"{prtname}-{new_node_label}-F"

                    for falsenextnode_element in last_node.iterchildren("falsenextnode"):
                        if falsenextnode_element.text == "-1":
                            falsenextnode_element.text = new_node_name

                    #for truescore_element in last_node.iterchildren("truescore"):
                    #    if truescore_element.text != "1":
                    #        for truenextnode_element in node.iterchildren("truenextnode"):
                    #            if truenextnode_element.text == "-1":
                    #                truenextnode_element.text = new_node_name

                    prt.append(copy.deepcopy(node_to_add))

                i+=1

        if self.add_prt_node_on_not_correct is not None and not pd.isna(self.add_prt_node_on_not_correct):
            #node_to_add_tree = etree.parse("default-prt-node.xml", parser)
            # = node_to_add_tree.getroot()
            node_to_add = copy.deepcopy(default_prt_node)
            for truefeedback_element in node_to_add.iterchildren("truefeedback"):
                for truefeedback_text_element in truefeedback_element.iterchildren("text"):
                    truefeedback_text_element.text = etree.CDATA(f"<p>{self.add_prt_node_on_not_correct}</p>")



            for prt in self.root.iterchildren("prt"):
                #node_amount = 0
                #for node in prt.iterchildren("node"):
                #    node_amount+=1
                for node in prt.iterchildren("node"):
                    for falsenextnode_element in node.iterchildren("falsenextnode"):
                        if falsenextnode_element.text == "-1":
                            falsenextnode_element.text = "999"
                    for truescore_element in node.iterchildren("truescore"):
                        if truescore_element.text != "1":
                            for truenextnode_element in node.iterchildren("truenextnode"):
                                if truenextnode_element.text == "-1":
                                    truenextnode_element.text = "999"

                prtname = ""
                for prtname_element in prt.iterchildren("name"):
                    prtname = prtname_element.text

                for trueanswernote_element in node_to_add.iterchildren("trueanswernote"):
                    trueanswernote_element.text = f"{prtname}-1000-T"
                for falseanswernote_element in node_to_add.iterchildren("falseanswernote"):
                    falseanswernote_element.text = f"{prtname}-1000-F"

                prt.append(copy.deepcopy(node_to_add))

    def __str__(self):
        return f"{etree.tostring(self.root, pretty_print=True)}"
    
DefaultVersion = QuestionVersion("default")

def get_exercises_as_Moodle_Question_array(filepath, **kwargs):
    df = pd.read_csv(filepath, **kwargs)
    Exercises_To_Parse = []
    for data in df.itertuples():
        Exercise_To_Parse = MoodleQuestion(data.topic_number, data.topic_id, data.exercise_number, data.exercise_part, data.topic_label, data.exercise_description, data.exercise_variables, data.exercise_text, data.exercise_content, data.exercise_hint, data.specificfeedback, data.custom_general_feedback, data.exercise_note, data.custom_prt, data.add_prt_node_on_not_correct, [data.add_prt_node_wa1, data.add_prt_node_wa2, data.add_prt_node_wa3], data.custom_input, data.custom_seed, None if "its_keep_orig_input" not in dir(data) else data.its_keep_orig_input) #,  question_template_file_path="default_question_en.xml"
        Exercises_To_Parse.append(Exercise_To_Parse)
        
    return Exercises_To_Parse
    

def generate_questions_xml_from_file(filepath, output="output.xml", version=None, **kwargs):
    Pool = generate_Pool_from_file(filepath, version, **kwargs)
    Pool.write_to_xml_file(output)
    return Pool

def generate_quiz_mbz_from_file(filepath, template_path, output_folder="output", version=None, **kwargs):
    Pool = generate_Pool_from_file(filepath, version, **kwargs)
    Pool.write_to_mbz_file(output_folder, template_path)
    return Pool
    
def generate_Pool_from_file(filepath, version=None, **kwargs):
    if version == None:
        version = DefaultVersion
    Exercises_To_Parse = get_exercises_as_Moodle_Question_array(filepath, **kwargs)
    if version.needs_exercises_as_callback_arg == True:
        version.callback_kwargs["Exercises"] = Exercises_To_Parse
    
    Pool = QuestionPool(version, Exercises_To_Parse)
    return Pool


#%% Functions for Moodle_xml_to_csv
def get_last_child_element(element, child_tag):
    to_return = False
    for child in element.iterchildren(child_tag):
        to_return = child
    if to_return == False:
        print(f"didnt find {child_tag} in element")
    return to_return

def get_last_child_text_element(element, child_tag):
    to_return = ""
    for child in element.iterchildren(child_tag):
        for child_text_element in child.iterchildren("text"):
            to_return = child_text_element
    if to_return == False:
        print(f"didnt find {child_tag} text in element")
    return to_return

def strip_encoding_information(string):
    return string[2:-1]

def get_enumerated_alpha(i, lowercase=True):
    start_letters = 97 if lowercase == True else 65
    j = i
    letters = []
    letter_num = j % 26
    letters.append(chr(letter_num+start_letters))
    times_through_the_alphabet = math.floor((j-letter_num) / 26)
    
    while times_through_the_alphabet != 0:
        j = times_through_the_alphabet
        letter_num = j % 26
        letters.append(chr(letter_num+start_letters-1))
        times_through_the_alphabet = math.floor((j-letter_num) / 26)
        
    return ''.join(letters[::-1])

def moodlexml_to_csv(filepath, output="output.csv", **kwargs):
    parser = etree.XMLParser(strip_cdata=False)
    tree = etree.parse(filepath, parser=parser)
    root = tree.getroot()
    
    table = pd.DataFrame(columns=pd.Series(["topic_number", "topic_id", "parent_label", "exercise_number", "exercise_part", "topic_label", "exercise_description", "exercise_variables", "exercise_text", "exercise_content", "exercise_hint", "specificfeedback", "exercise_note", "already_parsed", "custom_prt", "add_prt_node_on_not_correct", "add_prt_node_wa1", "add_prt_node_wa2", "add_prt_node_wa3", "custom_input", "custom_seed", "custom_general_feedback", "personal_note"]))
    
    topic_number = 999
    topic_id = "gen" #for generated
    parent_label = "Generated"
    exercise_number = 999
    topic_label = "generated"
    already_parsed = 0
    add_prt_node_on_not_correct = ""
    add_prt_node_wa1 = ""
    add_prt_node_wa2 = ""
    add_prt_node_wa3 = ""
    custom_seed = ""
    custom_general_feedback = ""
    personal_note = ""
    
    question_skip = 0
    
    i = 0
    
    for question in root.iterchildren("question"):
        
        exercise_part = get_enumerated_alpha(i)
        
        if question.attrib["type"] != "stack":
            question_skip += 1
            print("skip non stack question")
            continue
        
        exercise_description = ""
        exercise_variables = ""
        exercise_text = ""
        exercise_content = ""
        exercise_hint = ""
        exercise_note = ""
        custom_prt = ""
        custom_input = ""
        
        exercise_description = get_last_child_text_element(question, "name").text
        exercise_variables = get_last_child_text_element(question, "questionvariables").text
        exercise_text = get_last_child_text_element(question, "questiontext").text
        
        #in this special case: remove img tag, remove speech bubble and save content as hint
        regex_digital_mentor_additionals = re.compile(r'<.*?class="bubble">([\d\D]*)<\/.*?>[\d\D]*<img.*?class="dm-icon.*?>')
        regex_scripts = re.compile(r'<script[\d\D]*?</script>')
        
        matches = []
        hint_matches_object = regex_digital_mentor_additionals.finditer(exercise_text)
        for match in hint_matches_object:
            matches.append(match)
            
        if len(matches) != 1:
            print(f"no digital mentoring hints found in {exercise_description}, continue")
        else:
            exercise_hint = matches[0].group(1)
            
        exercise_text = regex_digital_mentor_additionals.sub("", exercise_text)
        exercise_text = regex_scripts.sub("", exercise_text)
        
        
        exercise_text_max_len = 100000
        if len(exercise_text) > exercise_text_max_len:
            question_skip += 1
            print(f'skip question with too long exercise text (>{exercise_text_max_len}): {exercise_description})')
            continue
        
        specificfeedback = get_last_child_text_element(question, "specificfeedback").text        
        exercise_note = get_last_child_text_element(question, "questionnote").text
        
        inputs = []
        for input_element in question.iterchildren("input"):
            inputs.append(input_element)
        
        if len(inputs) == 1:
            custom_input = etree.tostring(inputs[0], encoding="unicode", method="xml")
        else:
            input_collector = etree.Element("input_fields")
            for input_element in inputs:
                input_collector.append(input_element)
            custom_input = etree.tostring(input_collector, encoding="unicode", method="xml")
        
        prts = []
        for prt in question.iterchildren("prt"):
            prts.append(prt)
        
        if len(prts) == 1:
            custom_prt = etree.tostring(prts[0], encoding="unicode", method="xml")
        else:
            prt_collector = etree.Element("prt_fields")
            for prt in prts:
                prt_collector.append(prt)
            custom_prt = etree.tostring(prt_collector, encoding="unicode", method="xml")
            
        seeds = []
        for seed in question.iterchildren("deployedseed"):
            seeds.append(seed)
        if len(seeds) > 0:
            seed_collector = etree.Element("seed_fields")
            for seed in seeds:
                seed_collector.append(seed)
            custom_seed = etree.tostring(seed_collector, encoding="unicode", method="xml")
        
        table.loc[-1] = [topic_number, topic_id, parent_label, exercise_number, exercise_part, topic_label, exercise_description, exercise_variables, exercise_text, exercise_content, exercise_hint, specificfeedback, exercise_note, already_parsed, custom_prt, add_prt_node_on_not_correct, add_prt_node_wa1, add_prt_node_wa2, add_prt_node_wa3, custom_input, custom_seed, custom_general_feedback, personal_note]
        table.index = table.index + 1
        
        i+=1
        
    table.sort_index()
    
    table.to_csv(output, **kwargs)
            
    print(f"skipped {question_skip} questions")
    return table
    