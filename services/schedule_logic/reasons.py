from collections import defaultdict

from utils.normalize import normalize

# Adds reasons to cards

def build_reason(course):
    reasons = [] # this list sotres each reason one by one
    # If the course is a major requirement, explain that.
    if course.get("type") == "MAJOR":
        reasons.append("Needed for major")

    # If the course is a UCC/general education requirement, explain that.
    elif course.get("type") == "UCC":
        reasons.append("Fulfills UCC requirement")

    reasons.append("No time conflicts")
    reasons.append("Prerequisites satisfied")
    return " + ".join(reasons)

def attach_reasons(selected): #Adds a reason field to ever selected course. This runs after the final shcuedle has already been chosen
    for course in selected:
        # Adds a new key called reason into each course dictionary
        course["reason"] = build_reason(course)

    return selected # Return the same slected schedule, but now every course has a reason