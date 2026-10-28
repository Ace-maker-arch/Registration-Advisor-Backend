import re

from utils.normalize import normalize
from services.ucc import extract_ucc_requirements, calculate_ucc_area_remaining

# All the regex is happening here
def parse_degreeworks_text(extracted_text):#Takes all degree works text and extract the student's academci data
    normalized_text = re.sub(r"\s+", " ", extracted_text).strip()# replaces mutliple spaces or newlines with a single space

    major = None
    major_match = re.search(
        r"Major\s+([A-Za-z &/]+?)\s+(?:Minors?|Program|College)\b",# Finds the word major and keepin going until you hit the word minors,program, or college
        normalized_text,
        re.IGNORECASE,
    )#Tries to match to major

    if major_match:# if the major exist you extract it
        major = major_match.group(1).strip()

    still_needed_matches = re.findall(# Find all classes that are label still needed
        r"Still needed:\s*(.*?)(?=\n[A-Z]|\Z)",
        extracted_text,
        re.DOTALL,
    )

    not_started_courses = []
    unmet_requirements = []

    for requirement in still_needed_matches:
        if re.search(r"^\s*\d+\s+Class\s+in\s+", requirement, re.IGNORECASE):# checks if the requirements look something like 1 Class in CS 3500
            not_started_courses.append(requirement)
        else:
            unmet_requirements.append(requirement)# If it is not a simple 1 class in requirement save it unmet requirement

    # Removes duplicates
    not_started_courses = list(dict.fromkeys(not_started_courses))
    unmet_requirements = list(dict.fromkeys(unmet_requirements))

    #Your extracting major requirements now
    major_requirements = []

    for req in still_needed_matches:# loop through still needed matchs again
        matches = re.findall(r"\b[A-Z]{2,4}\s+\d{4}\b", req)# tries to find course like CS 3500
        for course in matches: # looops through ever course code found
            if course not in major_requirements:# Only add the course if it hasn't been added yet
                major_requirements.append(course)

    major_needed_courses = {normalize(course) for course in major_requirements}# Creates a cleaned set of requrie courses

    normalized_lines_text = re.sub(r"[ \t]+", " ", extracted_text)#Replaces repeating spaces and tabs one with space
    normalized_lines_text = re.sub(r"\n+", "\n", normalized_lines_text)# replace mutliple newlines with one newline

    course_matches = re.findall(# This capture 5 pieces course_number,course_name,grade,credits,term
        r"([A-Z]{2,4}\s+\d{4})\s+([A-Z0-9 &/\-'.]+?)\s+([A-Z][A-Z+-]*|REG|WD|P)\s+\(?(\d+)\)?\s+((?:Spring|Summer|Fall|Winter)\s*\d{4})",
        normalized_lines_text,
    )

    completed_courses = []
    in_progress_courses = []
    failed_courses = []
    seen_courses = set()

    for course_number, course_name, grade, credits, term in course_matches:
        grade = grade.strip().upper()#Cleans the grade

        course_info = {# builds a dictionary for one course
            "course_number": course_number,
            "course_name": course_name.strip(),
            "grade": grade,
            "credits": credits,
            "term": term,
        }

        course_key = (course_number, grade, term)#CCreates a unique ID for duplicating checking

        if course_key not in seen_courses:# Only adds if the course_key has not already been added
            seen_courses.add(course_key)

            if grade == "REG":
                in_progress_courses.append(course_info)
            elif grade in ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "P"]:
                completed_courses.append(course_info)
            elif grade in ["F", "D", "D+", "D-"]:
                failed_courses.append(course_info)

    exempt_courses = re.findall(# Checks if the PDF says the World Language requirement is exempt
        r"World\s+Language\s+Requirement\s+Exempt",
        extracted_text,
    )

    registration_data = None
    reg_match = re.search(# searchs for registration date
        r"Registration Date[:\s]+([A-Za-z]+\.?\s+\d+(?:st|nd|rd|th)?)",
        extracted_text,
        re.IGNORECASE,
    )

    if reg_match:# if found save only the date part
        registration_data = reg_match.group(1).strip()

    program_match = re.search(r"Program\s+(.*?)College", extracted_text)#Finds text between program and college
    gpa_match = re.search(r"GPA:\s*([0-9.]+)", extracted_text)# Finds gpa
    credits_required_match = re.search(r"Credits required:\s*(\d+)", extracted_text)#Find credits required
    credits_applied_match = re.search(r"Credits applied:\s*(\d+)", extracted_text)#Finds credits applied

    program = program_match.group(1).strip() if program_match else None#Stores program if found the same for the rest
    gpa = gpa_match.group(1).strip() if gpa_match else None
    credits_required = credits_required_match.group(1).strip() if credits_required_match else None
    credits_applied = credits_applied_match.group(1).strip() if credits_applied_match else None

    credits_remaining = int(credits_required or 0) - int(credits_applied or 0)

    ucc_requirements = extract_ucc_requirements(extracted_text)#Extract UCC area from degreeworks
    ucc_area_remaining = calculate_ucc_area_remaining(ucc_requirements)#Calculates how many UCC classes are still needed in each area

    return {
        "major": major,
        "program": program,
        "gpa": gpa,
        "credits_required": credits_required,
        "credits_applied": credits_applied,
        "credits_remaining": credits_remaining,
        "completed_courses": completed_courses,
        "in_progress_courses": in_progress_courses,
        "failed_courses": failed_courses,
        "exempt_courses": exempt_courses,
        "not_started_courses": not_started_courses,
        "unmet_requirements": unmet_requirements,
        "major_requirements": major_requirements,
        "major_needed_courses": major_needed_courses,
        "ucc_requirements": ucc_requirements,
        "ucc_area_remaining": ucc_area_remaining,
        "registration_date": registration_data,
    }
