# Helper prepare candidates for openAI

from utils.normalize import normalize
from collections import defaultdict

def meeting_sort_key(section):#return a number the meeting start time so classes can be sorted
    meeting = section.get("meeting") or {}#gets the meeting dictionary
    start = meeting.get("start")#gets start from the meeting dictionary

    try:
        return int(start) if start else 9999#if start exist convert it to integer otherwise return 9999
    except:#if try crashes run the code below
        return 9999


def shrink_candidates_for_ai(candidates, max_per_course=2, max_total=16):#reduce the number of candidates before sending them to openAI
    grouped = defaultdict(list)#Creates a dictionary where each key automatically starts with an empty list

    for candidate in candidates:
        code = normalize(candidate.get("course_code", ""))
        grouped[code].append(candidate)#Adds the candidate into the correct course grade based on course number so all section of the saem course get grouped otgehter

    major_trimmed = []#stored major trimmer candidates
    ucc_trimmed = []

    for code, items in grouped.items():
        items = sorted(items, key=lambda c: meeting_sort_key(c.get("section", {})))#Store sections by meeting time
        candidate_type = items[0].get("type", "UCC")#gets the type for the candidate

        if candidate_type == "MAJOR":
            major_trimmed.extend(items[:2])# This makes sure you add only the first two sections
        else:
            ucc_trimmed.extend(items[:1])#only keep one section for each UCC course

    result = major_trimmed[:8] + ucc_trimmed[:8]
    return result[:max_total]


def compact_candidate(candidate):#removes unnessary data ebfore sening to ai, which saves tokem
    section = candidate.get("section", {})
    meeting = section.get("meeting") or {}

    return {#return only what you need
        "course_code": candidate.get("course_code"),
        "crn": candidate.get("crn"),
        "type": candidate.get("type"),
        "ucc_area": candidate.get("ucc_area"),
        "section": {
            "course_code": section.get("course_code"),
            "title": section.get("title"),
            "term": section.get("term"),
            "credits": section.get("credits"),
            "modality": section.get("modality"),
            "meeting": {
                "start": meeting.get("start"),
                "end": meeting.get("end"),
                "days": meeting.get("days"),
                "location": meeting.get("location"),
                "room": meeting.get("room"),
            },
        },
    }