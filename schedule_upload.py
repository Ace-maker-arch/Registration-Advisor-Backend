import re

from fastapi import APIRouter, Request

from config import SPRING_FILES
from utils.normalize import normalize
from utils.pdf_utils import extract_pdf_text
from services.JSON_class_section_formatter import load_json_files, detect_modality


router = APIRouter()


@router.post("/upload-schedule")
async def upload_schedule(request: Request):#gives you access to the raw request data
    contents = await request.body()#gets the raw bytes of the uploaded pdf
    extracted_text = extract_pdf_text(contents)#makes the pdf bytes readable

    student_name = None

    name_match = re.search(
        r"([A-Za-z]+-?[A-Za-z]*,\s+[A-Za-z]+-?[A-Za-z]*)\s+(?:Fall|Spring|Summer|Winter)\s+\d{4}\s+Schedule",
        extracted_text,
        re.IGNORECASE,
    )# It trying to find the user name

    professors = list(dict.fromkeys(
        re.findall(r"\n([A-Z][a-zA-Z'-]+,\s+[A-Z][a-zA-Z'-]+)\n", extracted_text)
    ))#find all professor names

    bad_words = {
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
        "Saturday", "Sunday",
        "Main", "Spring", "Fall", "Summer", "Winter"
    }#these word smight accendiantlly match the professor regex so you filter them out

    professors = [#start rebuilding the professors list
        p for p in professors#loop through each professor name
        if p.split(",")[0] not in bad_words#checks the lst name slides to make sure everyhting is fine
           and p.split(",")[1].strip() not in bad_words
    ]

    if name_match:#checks if regex found student name
        student_name = name_match.group(1).strip()

    crn_matches = re.findall(r"(\d{5})\s*\d{2}/\d{2}/\d{4}", extracted_text)#match crn
    crns = list(dict.fromkeys(crn_matches))#make sure to remove duplicates

    all_files = load_json_files(SPRING_FILES)#your combing all the spring files into one list

    raw_sections = []#this will hold every section form every spring JSON file
    for file in all_files:
        raw_sections.extend(file["data"])#adds all section from all files into raw_sections

    current_courses = []#store students current classes
    seen_crns = set()#Track CRNs already handled

    course_index = 0#track which professor to assign to which course

    for crn in crns:#loop thorugh each crn
        if crn in seen_crns:#if this crn was already processed skip it
            continue

        for section in raw_sections:#loop through ever section in your Spring JSON database
            if str(section.get("courseReferenceNumber")) == str(crn):#checks if the JSON section crn match the PDF CRN
                seen_crns.add(crn)#Marks this CRN as processed

                meetings = []#Creeates a list to store all meeting times

                if section.get("meetingsFaculty"):#Checks if this section has meeting date
                    for mt_entry in section["meetingsFaculty"]:#loops through each meeting
                        mt = mt_entry.get("meetingTime", {})#gets the meetimg time dcitioanry
                        meetings.append({
                            "start": mt.get("beginTime"),
                            "end": mt.get("endTime"),
                            "days": {
                                "monday": mt.get("monday"),
                                "tuesday": mt.get("tuesday"),
                                "wednesday": mt.get("wednesday"),
                                "thursday": mt.get("thursday"),
                                "friday": mt.get("friday"),
                            },
                            "location": mt.get("building"),
                            "room": mt.get("room"),
                        })

                meeting_time = meetings[0] if meetings else None#Use the first meeting as the main meeting

                subject = section.get("subject")
                course_number = section.get("courseNumber")
                course_code = normalize(f"{subject} {course_number}")#Creates full course code
                modality = detect_modality(section)#Detecs if the class is online async or in person

                professor = professors[course_index] if course_index < len(professors) else None

                current_courses.append({
                    "course_code": course_code,
                    "crn": crn,
                    "professor": professor,
                    "type": "CURRENT",
                    "section": {
                        "crn": str(crn),
                        "course_code": course_code,
                        "title": section.get("courseTitle"),
                        "term": section.get("termDesc"),
                        "credits": section.get("creditHours"),
                        "modality": modality,
                        "meeting": meeting_time,
                        "all_meetings": meetings,
                    },
                })

                course_index += 1
                break
    return {
        "student_name": student_name,
        "current_courses": current_courses,
    }


