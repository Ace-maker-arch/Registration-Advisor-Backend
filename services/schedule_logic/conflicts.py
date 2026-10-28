def has_time_conflict(sec1, sec2):#checks if two classes have a tinme conflcit or nt
    m1 = sec1.get("meeting")
    m2 = sec2.get("meeting")

    if not m1 or not m2:
        return False

    for day in ["monday", "tuesday", "wednesday", "thursday", "friday"]:
        if m1["days"].get(day) and m2["days"].get(day):
            start1 = int(m1["start"] or 0)
            end1 = int(m1["end"] or 0)

            start2 = int(m2["start"] or 0)
            end2 = int(m2["end"] or 0)

            if start1 < end2 and start2 < end1:
                return True

    return False