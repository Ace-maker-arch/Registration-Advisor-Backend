import json
from datetime import datetime#used for dates and times
from pathlib import Path# used for fil/folder paths

from fastapi import APIRouter, Body#ApirROuter lets you creates router and body is to read data from the request body


router = APIRouter()#Creates a router object. This router stores your endpoints


@router.post("/confirm-schedule")#Frontend sends data to the backend
async def confirm_schedule(data: dict = Body(...)):
    student_id = data.get("student_id")#gets student id

    if not student_id:
        return {"error": "student_id is required"}

    save_dir = Path("saved_students")#does not create folder only the path
    save_dir.mkdir(exist_ok=True)# create the folder only if it does not arleady exist

    file_path = save_dir / f"{student_id}.json"#creates the full file path

    saved_data = {
        "student_id": student_id,
        "student_name": data.get("student_name"),
        "major": data.get("major"),
        "program": data.get("program"),
        "gpa": data.get("gpa"),
        "saved_at": datetime.utcnow().isoformat(),
        "current_classes": data.get("current_classes", []),
        "next_semester_classes": data.get("next_semester_classes", []),
    }

    with open(file_path, "w") as f:#opens the file for writing
        json.dump(saved_data, f, indent=2)#write the dicitonar yinto the json file but first convert python dicitonary into JSOn and save it in a file

    return {"message": "Schedule saved successfully"}


@router.get("/confirm-schedule/{student_id}")
async def get_confirmed_schedule(student_id: str):#FastAPi automatically extractsthe student ID from the URL
    file_path = Path("saved_students") / f"{student_id}.json"#builds the path to the student saved file

    if not file_path.exists():#checks if the file exists
        return {"error": "Student schedule not found"}

    with open(file_path, "r") as f:# open to read the ifle
        saved_data = json.load(f)#reads json form the file and converts it back to python dictioanry

    return saved_data
