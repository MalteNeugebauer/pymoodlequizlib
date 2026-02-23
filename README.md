# pymoodlequizlib
A collection of python scripts and libraries to easily edit quizzes and questions in the learning management system [Moodle](https://moodle.org).

The main purpose of this repository is to share resources that allow for creating different versions of the same set of Moodle exercises. These versions add gamification or additional feedback to default exercises in Moodle. The focus is on exercises of the [STACK](https://stack-assessment.org) type.

## Concept
The information of versions and exercises are stored separately. This way, different versions of the same set of exercises can be created. The figure below illustrates that exemplarily for three different versions. The resulting learning data can be analyzed regarding differences in the effect on learners (see [paper section](#papers) below).

![maths training area example question](./img/learning-activity-generation.png)

## Usage
 - Install the [requirements](requirements.txt). E.g. with `mamba create -n pymoodlequizlib --file requirements.txt`.
 - Store the information of your STACK exercises in a single CSV file like those in [exercises](exercises) or choose one of the files there.
- You can include exercises from your Moodle system or from question pools by downloading them in Moodle XML format and use [xml_to_csv.py](xml_to_csv.py) to convert them into CSV.
 - If you only want a selection of the exercises to be included in the (modified) quiz, you can fill the `already_parsed` column in your CSV file with values:
   - 0 for including
   - 1 for excluding
 - Choose a [versions](#version) (see below).
 - Run the script [csv_to_mbz.py](csv_to_mbz.py). Make sure to import the chosen version and pass it as an argument to the file generation function. You can define a name for the output file. By default, an `mbz` file named according to the colum `topic_number` is stored in a folder named `output`.
 - Import the output file(s) in your Moodle course as described in the [Moodle documentation](https://docs.moodle.org/500/en/Course_restore).

## Versions
For more information on the different versions, see the [math-digital-mentoring repository](https://github.com/MalteNeugebauer/math-digital-mentoring) or [its website](https://malteneugebauer.github.io/math-digital-mentoring/).

Here is a brief overview.
| Name             | Module              | Flavors                                                                          | Description                                                                                                                                                                                                                                                | Icon |
|------------------|---------------------|----------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------|
| Default          | -                   | -                                                                                |   Exercises are converted to Moodle's default when leaving `version` empty.                                                                                                                                                                                |      |
| Preview          | qv_preview          | Normal                                                                           | Replaces Moodle's default enumeration of exercises in the exercise overview by user's choice. By default, alphabetical, which is more common in German textbooks.                                                                                          |      |
| Instant Tutoring | qv_instant_tutoring | InstantTutoringVersion InstantTutoringTEDABSVersion InstantTutoringTEDRELVersion InstantTutoringTEDRelSpotFeedbackVersion| Integrates a pedagogical agent that comments on learner's input according to the STACK feedback. The flavors `InstantTutoringTEDABSVersion` and `InstantTutoringTEDRELVersion` add automated absolute or similarity-based feedback on incorrect responses. The additional flavor `SpotFeedback` adds automated hints about positions in a term where changes are necessary (experimental). |      |
| Math Magician    | qv_math_magician    | MathMagicianVersion                                                              | Wraps the set of exercises into a medieval game environment. Learner fight their way through the dark forest, rescue fairies and earn points for solving exercises and their variants.                                                                     |      |

## Papers
 - Neugebauer, M.; Erlebach, R.; Kaufmann, C.; Mohr, J.; Frochte, J. (2024): *Efficient Learning Processes By Design: Analysis of Usage Patterns in Differently Designed Digital Self-Learning Environments.* Proceedings of the 16th International Conference on Computer Supported Education. https://doi.org/10.5220/0012558200003693