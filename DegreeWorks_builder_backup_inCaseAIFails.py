from collections import defaultdict
from services.schedule_logic.conflicts import has_time_conflict
from utils.normalize import normalize

# Both funcitons here are backups in case the ai fails completely or partially
def pick_schedule(candidates, ucc_area_remaining):#Builds a sechdule if ai fails
    # ucc_area_remaining tells you how man yucc classes are still needed per area
    selected = []# This will hold the final picked classes
    seen_codes = set()# This tracks course codes already selected
    seen_ucc_area_count = defaultdict(int)#Creates a counting dictionary for ucc's

    major_candidates = [c for c in candidates if c.get("type") == "MAJOR"]# creates a list of only major classes
    ucc_candidates = [c for c in candidates if c.get("type") == "UCC"]#creates a list of only UCC's

    for candidate in major_candidates:#loop thoruhg eahc major class
        code = candidate["section"]["course_code"]

        if code in seen_codes:#checks if the course was already picked
            continue

        if any(has_time_conflict(candidate["section"], picked["section"]) for picked in selected):#if it has a time conflict with another class skip
            continue

        seen_codes.add(code)
        selected.append(candidate)

        if len(selected) >= 3:#stop after 3 major classes
            break

    for candidate in ucc_candidates:#here you get UCC
        code = candidate["section"]["course_code"]
        area = candidate.get("ucc_area")#Get ucca area for that course

        if code in seen_codes:#  skips if the coruse was alrady picked
            continue

        if area:#chekcs if candidate has a UCC area
            allowed_for_area = ucc_area_remaining.get(area, 0)#gets how many classes are allowed or needed for that UCC area
            if seen_ucc_area_count[area] >= allowed_for_area:#this prevents picking too many ucc classes from the same area
                continue

        if any(has_time_conflict(candidate["section"], picked["section"]) for picked in selected):#checks if the UCC class conflicts with any selected class
            continue

        if area:#if the class has a UCC area increase the count for that area by one
            seen_ucc_area_count[area] += 1

        seen_codes.add(code)
        selected.append(candidate)

        if len(selected) >= 5:# if the schedule has 5 return immediately
            return selected

    for candidate in major_candidates:# you only do this loop if you didn't get enough UCC's
        code = candidate["section"]["course_code"]#gets the course code

        if code in seen_codes:#skips duplicates
            continue

        if any(has_time_conflict(candidate["section"], picked["section"]) for picked in selected):#checks time conflicts
            continue

        seen_codes.add(code)
        selected.append(candidate)

        if len(selected) >= 5:
            return selected

    return selected


def fill_remaining_schedule(selected, candidates, max_classes=5):#If AI picked some classes but fewer than 5, add more valid classes
    seen_codes = {normalize(item["section"]["course_code"]) for item in selected}

    for candidate in candidates:
        code = normalize(candidate["section"]["course_code"])

        if code in seen_codes:
            continue

        if any(has_time_conflict(candidate["section"], picked["section"]) for picked in selected):
            continue

        selected.append(candidate)
        seen_codes.add(code)

        if len(selected) >= max_classes:
            break

    return selected