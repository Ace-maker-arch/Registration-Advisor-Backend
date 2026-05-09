import re

from utils.normalize import normalize


def is_senior(completed_courses):#This checks to see if your a senior
    total_credits = 0

    for course in completed_courses:
        try:
            total_credits += int(course.get("credits", 0))
        except:
            pass

    return total_credits >= 90


def is_cs_major(major):#this checks to see if you are a computer science major
    return "COMPUTER SCIENCE" in normalize(major or "")


def restriction_satisfied(section, completed_courses, major):#this checks to see if you have satisfied a restriciton
    restriction = normalize(section.get("restriction", ""))

    if not restriction:
        return True

    if "APPROVAL" in restriction:
        return False

    if "SENIOR" in restriction and not is_senior(completed_courses):
        return False

    if "CS MAJOR" in restriction and not is_cs_major(major):
        return False

    return True


def extract_requirement_tokens(text, default_subject="CS"):# Takes a prerequsiite and turn into a clean list of course codes
    text = normalize(text)

    full_codes = [normalize(m) for m in re.findall(r"[A-Z]{2,4}\s*\d{3,4}", text)]# Finds full course code
    bare_numbers = re.findall(r"\b\d{3,4}\b", text)#Finds numbers alone

    tokens = list(full_codes)#Starts list with full codes

    for number in bare_numbers:#loop through numbers
        if not any(code.endswith(number) for code in full_codes):# If number is not already part of a full code like CS 2300
            tokens.append(f"{default_subject} {number}")# Then converts 2300 to CS 2300

    return list(dict.fromkeys(tokens))# Removes duplicates

def prereqs_satisfied(crn, completed_courses, in_progress_courses, prereqs):#THis function cehck can this student take this crn(class) based on prerequisites
    taken = {# All taken courses or currently taking courses
        normalize(c["course_number"])
        for c in completed_courses + in_progress_courses
    }

    for _, data in prereqs.items():#loop through prereq rules.
        for sec in data.get("sections", []):#loops through each section attched to that prerequisite rule
            if str(sec["courseReferenceNumber"]) != str(crn):#skip if rule is not for this crn
                continue

            rule = normalize(data.get("prerequisites", {}).get("course_number", ""))

            if not rule:# If there is no prerequsiite rule just allow
                return True

            and_parts = re.split(r"\bAND\b", rule)# This splits the rule by and

            for part in and_parts:# loops through each end section
                part = part.strip()#removes spaces
                or_options = re.split(r"\bOR\b", part)#splits by or

                part_satisfied = False#tracks if the student satisfied a requirement

                for option in or_options:#loops throughe ver or option
                    option = option.strip()#removes spaces
                    tokens = extract_requirement_tokens(option, default_subject="CS")#extract course codes from the text

                    if any(token in taken for token in tokens):#Does the student have any of these required courses
                        part_satisfied = True
                        break

                if not part_satisfied:# If even one and section fails reject the class
                    return False

            return True

    return True


def major_subjects_for_major(major):
    major_normalized = normalize(major or "")

    if "COMPUTER SCIENCE" in major_normalized:
        return {"CS"}

    if "BIOLOGY" in major_normalized:
        return {"BIO"}

    if "CHEMISTRY" in major_normalized:
        return {"CHEM"}

    if "MATHEMATICS" in major_normalized:
        return {"MATH"}

    if "ACCOUNTING" in major_normalized:
        return {"ACCT"}

    if "FINANCE" in major_normalized:
        return {"FIN"}

    if "MARKETING" in major_normalized:
        return {"MKT"}

    if "PSYCHOLOGY" in major_normalized:
        return {"PSY"}

    if "SOCIOLOGY" in major_normalized:
        return {"SOC"}

    if "ANTHROPOLOGY" in major_normalized:
        return {"ANTH"}

    if "PHYSICS" in major_normalized:
        return {"PHYS"}

    return set()


def candidate_type_for_course(course_code, major, find_ucc_area):#decides whether the candidate is a UCC or major class
    normalized_course = normalize(course_code)
    subject = normalized_course.split()[0] if normalized_course else ""
    major_subjects = major_subjects_for_major(major)

    if subject in major_subjects:
        return "MAJOR"

    if find_ucc_area(normalized_course):
        return "UCC"

    return "SUPPORT"
