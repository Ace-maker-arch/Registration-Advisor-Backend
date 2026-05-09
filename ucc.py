import re

from utils.normalize import normalize


def find_ucc_area_from_section(section):#What category is this item
    attributes = section.get("section_attributes", []) or []

    for attr in attributes:
        code = (attr.get("code") or "").upper()
        desc = (attr.get("description") or "").upper()

        if code in {"PBW", "PWB"} or "PERSONAL WELL" in desc:
            return "One|Personal Well Being"
        if code in {"ACE", "CEX", "EXP"} or "UCC-2" in desc or "EXPRESSION" in desc:
            return "Two|Expression"
        if code in {"PPWK", "SPWK"} or "UCC-3" in desc or "WAYS KNOW" in desc:
            return "Three|Ways of Knowing"
        if code == "DJUS" or "UCC-4" in desc or "DIVERSITY" in desc or "JUSTICE" in desc:
            return "Four|Diversity and Justice"
        if code in {"CCE", "CCEG"} or "UCC-5" in desc or "COMMUNITY" in desc or "CIVIC" in desc:
            return "Five|Community and Civic Engagement"
        if code in {"GAWR", "GLBL"} or "UCC-6" in desc or "GLOBAL" in desc:
            return "Six|Global Awareness"

    return None


def make_find_ucc_area(all_sections):#lets you find ucc area only using course_code. Find the item then tell me its cateogry
    def find_ucc_area(course_code):
        norm_code = normalize(course_code)

        for section in all_sections:
            if normalize(section.get("course_code", "")) == norm_code:
                area = find_ucc_area_from_section(section)#you figure which area does the UCC belong to
                if area: #if a valid ucc is found return imediately to the outter function
                    return area

        return None

    return find_ucc_area# The outter funcitonr eturn the inner funciton itself


def extract_ucc_requirements(extracted_text):# Read Degree Works and what finds what UCC area the student needs
    ucc_blocks = re.findall(#your searching the degreework find things like Core Are three: Ways of Knowing
        r"(Core Area\s+(?:One|Two|Three|Four|Five|Six):.*?)(?=Core Area\s+(?:One|Two|Three|Four|Five|Six):|$)",
        extracted_text,# This is the text your are searching through
        re.DOTALL,#Allows . in the regex to match across multiple lines, without this it would stop at the linebreak
    )

    ucc_requirements = []# Creates an empty list where you will sotre clean UCC requirement dictioanries

    for block in ucc_blocks:#Each ucc_block is one UCC area section from Degreeworks
        area_match = re.search(# Search inside that one block for the area number and name
            r"Core Area\s+(One|Two|Three|Four|Five|Six):\s*([A-Za-z &-]+)",
            block,#only search inside the current ucc block
        )
#Looks for the status of the ucc area like Complete, In_progress_or in complete
        status_match = re.search(r"\b(COMPLETE|IN-PROGRESS|INCOMPLETE)\b", block)

        area_number = area_match.group(1) if area_match else None# If the regex found an area get group 1 like "Three"
        area_name = area_match.group(2).strip() if area_match else None# If regex found an area get group two lie "Ways of knowing"
        status = status_match.group(1) if status_match else None#get group 3 if exist like "INCOMPLETE"

        course_code_matches = re.findall(r"\b[A-Z]{2,4}\s+\d{4}\b", block)#Finds all course codes in this block
        course_options = [normalize(c) for c in list(dict.fromkeys(course_code_matches))]
        # The code above does two things removes duplicate and normalizes the code

        required_count_match = re.search(#Searchs for how many courses the student must choose
            r"Select\s+(\d+)\s+Course|Choose\s+(\d+)\s+of",
            block,# Search inside this block
            re.IGNORECASE,
        )

        required_count = (#Start calculating the number of required courses
            int(required_count_match.group(1) or required_count_match.group(2))#gets number form either regex
            if required_count_match#if nothing is found default to one
            else 1
        )

        block_course_matches = re.findall(
            r"([A-Z]{2,4}\s+\d{4})\s+([A-Z0-9 &/\-'.]+?)\s+([A-Z][A-Z+-]*|REG|WD|P)\s+\(?(\d+)\)?\s+((?:Spring|Summer|Fall|Winter)\s*\d{4})",# THis regex capture five things course_number,course_name,grade,credit,and term
            block,
        )#searchs for courses liksted as compelted or in pregress in the UCC block

        completed_in_block = []#For completed UCC course
        in_progress_in_block = []#For in progress UCC courses

        for course_number, course_name, grade, credits, term in block_course_matches:
            course_info = {
                "course_number": normalize(course_number),
                "course_name": course_name.strip(),
                "grade": grade.strip().upper(),
                "credits": credits,
                "term": term,
            }

            if course_info["grade"] == "REG":
                in_progress_in_block.append(course_info)
            elif course_info["grade"] in ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "P"]:
                completed_in_block.append(course_info)

        satisfied_count = len(completed_in_block) + len(in_progress_in_block)# counts how many courses are compelted or in progress

        is_satisfied = (#Starts deciding whether the UCC area is satisfied or not
            status in {"COMPLETE", "IN-PROGRESS"}#If degreework says compelte or in progress treat it as satisfied
            or (satisfied_count >= required_count and status != "INCOMPLETE")
        )

        ucc_requirements.append({
            "area_number": area_number,
            "area_name": area_name,
            "status": status,
            "completed_courses": completed_in_block,
            "in_progress_courses": in_progress_in_block,
            "course_options": course_options,
            "required_count": required_count,
            "is_satisfied": is_satisfied,
        })

    return canonicalize_ucc_requirements(ucc_requirements) #before reutring it clean and get rid of duplicates


def canonicalize_ucc_requirements(ucc_requirements):#Clean and removes duplicates for UCC
    canonical_ucc_requirements = {}#Will store one clean version per UCC

    for ucc in ucc_requirements:
        area_number = ucc.get("area_number")
        area_name_clean = (
            (ucc.get("area_name") or "")
            # your jsut getting rid of the words like complete or sectino fron the string
            .replace(" COMPLETE", "")
            .replace(" IN-PROGRESS", "")
            .replace(" INCOMPLETE", "")
            .replace(" section", "")
            .strip()
        )

        if not area_number or not area_name_clean:# if iether is missing skip
            continue

        key = f"{area_number}|{area_name_clean}" # like "Thtre ways of knowing"
        status = (ucc.get("status") or "").strip().upper()

        existing = canonical_ucc_requirements.get(key)#looks up if this area is already in dictionary

        if existing is None: #means the area hasnt been stored
            canonical_ucc_requirements[key] = {**ucc, "area_name": area_name_clean}
            continue

        existing_status = (existing.get("status") or "").strip().upper()#get the status of the alread stored version

        priority = {
            "COMPLETE": 3,
            "IN-PROGRESS": 2,
            "INCOMPLETE": 1,
            "": 0,
        }

        if priority.get(status, 0) > priority.get(existing_status, 0):
            canonical_ucc_requirements[key] = {**ucc, "area_name": area_name_clean}#overwrites the old version with the better one

    return list(canonical_ucc_requirements.values())# return clean ucc list


def calculate_ucc_area_remaining(ucc_requirements):#Calculates how many UCCs are needed for that area.
    ucc_area_remaining = {}#Creates an empty dictionary that will store the final answer

    for ucc in ucc_requirements:#loop throughe ver UCC requirement
        area_key = f"{ucc.get('area_number')}|{ucc.get('area_name')}"#Creates a unique name for that UCC area

        if ucc.get("is_satisfied"):#checks of this UCC area is alrayd completed
            ucc_area_remaining[area_key] = 0#means if the area is done allow 0 classes
        else:
            ucc_area_remaining[area_key] = 1#Allowed to recommend 1 class for this ucc area if the area is not completed

    return ucc_area_remaining
