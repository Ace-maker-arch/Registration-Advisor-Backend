from utils.normalize import normalize
from services.schedule_logic.conflicts import has_time_conflict

def replace_course(schedule, candidates, crn_to_replace, replacement_crn):#Replace one class int he schedule with another class
    # shceudle is the student current schuedle, candidates are all possible replacement classesm,crn_to_replace is the crn in the schedule that we want to remove and place the replacement_crn or class
    new_schedule = []#this will beocme the updated shcedule

    for item in schedule:#loops throughe ver course in the current schedule
        if str(item["section"]["crn"]) != str(crn_to_replace):#if this is not the class you want to replace then automatically add it to the new schedule
            new_schedule.append(item)

    selected_candidate = None#this will hold the replacement class

    for candidate in candidates:#loops thorughe every possible replacement option
        if str(candidate["section"]["crn"]) == str(replacement_crn):#is this candidate the one the student selected
            selected_candidate = candidate#store the replacement class
            break# no need to continue searhcing

    if not selected_candidate:#if we failed to find a replacement class then return orginal schedule unchanged
        return schedule

    if any(#does any course in the schedule alreayd match this course code, you do this to prevent taking duplicate courses
        c["section"]["course_code"] == selected_candidate["section"]["course_code"]
        for c in new_schedule
    ):
        return schedule#if true reject replacement, return original schedule

    for existing in new_schedule:#loops through all remaining course
        if has_time_conflict(selected_candidate["section"], existing["section"]):#does the new class conflict with any existing class
            return schedule# if does have a time conflict return old schedule so you reject the replacement

    new_schedule.append(selected_candidate)#if it passed all checks then add new class
    return new_schedule#return enw schedule


def get_swap_options(schedule, candidates, crn_to_replace):# Finds valid replacement options
    base_schedule = [] # this will hold the schedule without the class being replaced

    for item in schedule:#loops through current schedule
        if str(item["section"]["crn"]) != str(crn_to_replace):# skip the class being replaced
            base_schedule.append(item)#keep all other classes

    base_course_codes = {#Creates a set of exisitng course codes
        normalize(item["section"]["course_code"])#gets course code and stadnarizes it
        for item in base_schedule
    }

    options = []# This will store valid swap options
    seen_crns = set()#tracks CRn already added to rpevent duplicates

    for candidate in candidates:#loop thorugh ever possible candidate
        candidate_crn = str(candidate["section"]["crn"])#gets candidate crn
        candidate_code = normalize(candidate["section"]["course_code"])#gets candidate code

        if candidate_crn == str(crn_to_replace):#skip if same class for nio duplicates
            continue

        if candidate_crn in seen_crns:#checks if already added
            continue

        if candidate_code in base_course_codes:#checks if course already exist in schedule
            continue

        if any(has_time_conflict(candidate["section"], existing["section"]) for existing in base_schedule):
            continue#checks every existing course if any has time conflict exist

        seen_crns.add(candidate_crn)
        options.append(candidate)#add cnadidate to vlaid option list

    return options# return all valid replacement options