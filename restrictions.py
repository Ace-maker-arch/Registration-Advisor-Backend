def build_crn_rule_lookup(prereqs):# Your finding the crn to get the restriction for each class
    crn_rule_lookup = {}

    for _, data in prereqs.items():# loops through each course in prereqs. The course_number is ignored, data is infor about that course
        for sec in data.get("sections", []):#look at each section inside that course
            crn_rule_lookup[str(sec["courseReferenceNumber"])] = { # use the crn as the key
                "restriction": sec.get("restriction", "")#store the restriction to add it to the dictionary
            }

    return crn_rule_lookup