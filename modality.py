def detect_modality(section):#figures our if a class is online or in person
    instr_desc = (section.get("instructionalMethodDescription") or "").lower()#gets soemthing like async or in person
    instr_code = (section.get("instructionalMethod") or "").upper()

    attributes = section.get("sectionAttributes", [])
    attr_desc = [a.get("description", "").lower() for a in attributes] # get every attribute description

    meeting_time = None
    if section.get("meetingsFaculty"):#checks if this exists
        meeting_time = section["meetingsFaculty"][0].get("meetingTime", {})

    building = (meeting_time.get("building") if meeting_time else "") or ""#get building online or async
    room = (meeting_time.get("room") if meeting_time else "") or ""#gets room like async

    building = building.upper()
    room = room.upper()

    if (
        "async" in instr_desc
        or any("asynchronous" in d for d in attr_desc)
        or "ASY" in instr_code
    ):
        return "ONLINE_ASYNC"

    if (
        ("online" in instr_desc or "ONL" in instr_code)
        and "async" not in instr_desc
    ):
        return "ONLINE_SYNC"

    if building == "ONLINE" or room in ["ASYNC", "SYN"]:
        if "async" in instr_desc:
            return "ONLINE_ASYNC"
        return "ONLINE_SYNC"

    return "IN_PERSON"

def modality_matches_preference(modality, preference):#checks if the class matches what the student selected in SwiftUI
    if not preference:# IF the student did not choice a prefernce allow everything
        return True

    if preference == "WP Online Only":
        return modality in ["ONLINE_ASYNC", "ONLINE_SYNC"]

    if preference == "In Person + Async":
        return modality in ["IN_PERSON", "ONLINE_ASYNC"]

    return True