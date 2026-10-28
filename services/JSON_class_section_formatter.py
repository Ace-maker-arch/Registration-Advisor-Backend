# This files is where all classes from json are converted into a different format

import json

from utils.normalize import normalize
from utils.modality import detect_modality

def load_json_files(file_paths):
    all_files = []

    for file_path in file_paths:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            all_files.append(data)

    return all_files#your combining all the files into one list


# This funciton is used so that you can take each class from the JSON files and convert it into section_record variable format
# This applies to all ten files
#here you access the json spring data
def build_section_database(all_files, crn_rule_lookup=None):#Convers original json files into clean section objects your app uses.
    crn_rule_lookup = crn_rule_lookup or {} # For this specific section version of the class what rules apply
    all_sections = []# Final list htat iwll hold all clean section

    for file in all_files: # loop throughe ach json file
        for section in file["data"]: # loop throughe ach data section
            # your geting all of this from the json dictionar
            subject = section.get("subject")
            course_number = section.get("courseNumber")
            course_code = normalize(f"{subject} {course_number}")

            meeting_time = None
            professor = None

            if section.get("meetingsFaculty"):#checks if section has meeting data
                mt = section["meetingsFaculty"][0].get("meetingTime", {})#Gets meetingtime dictionary

                meeting_time = {
                    "start": mt.get("beginTime"),
                    "end": mt.get("endTime"),
                    "days": { # true or false for each day
                        "monday": mt.get("monday"),
                        "tuesday": mt.get("tuesday"),
                        "wednesday": mt.get("wednesday"),
                        "thursday": mt.get("thursday"),
                        "friday": mt.get("friday"),
                    },
                    "location": mt.get("building"),
                    "room": mt.get("room"),
                }

                faculty_list = section.get("faculty", []) # get list of professor
                if faculty_list: # if list is not empty
                    first = faculty_list[0]# Takes first professor

                    if isinstance(first, dict):#If this variable is a dictioanry
                        professor = first.get("displayName")# get professor name
                    elif isinstance(first, str):
                        professor = first#If its already as tring use directly


            section_record = {# Creates clean ersion of section
                "crn": section.get("courseReferenceNumber"),
                "course_code": course_code,
                "title": section.get("courseTitle"),
                "subject": subject,
                "course_number": course_number,
                "term": section.get("termDesc"),
                "credits": section.get("creditHours"),
                "enrollment": section.get("enrollment"),
                "modality": detect_modality(section),
                "instructional_method": section.get("instructionalMethod"),
                "instructional_method_description": section.get("instructionalMethodDescription"),
                "section_attributes": section.get("sectionAttributes", []),
                "meeting": meeting_time,
                "professor": professor,
                "restriction": crn_rule_lookup.get(
                    str(section.get("courseReferenceNumber")), {}
                ).get("restriction", ""),
            }

            all_sections.append(section_record)

    return all_sections
