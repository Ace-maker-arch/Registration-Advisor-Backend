from fastapi import APIRouter, Body

import state
from services.schedule_logic.swaps import get_swap_options,replace_course


router = APIRouter()


@router.post("/swap-options")
async def swap_options(data: dict = Body(...)):# take json body from the frontend request and store it inside a variable called data this happens because of the loadSwapOptions function whhich reutrns schedule and crn
    schedule = data.get("schedule")
    crn = data.get("crn")# get crn of the class the student wants to replace

    if not state.candidates_store:# checks if candidate data exist. candidate_store is where are stored after the user uplaod degree works pdf
        return {"error": "No candidate data found. Upload PDF first."}

    options = get_swap_options(schedule, state.candidates_store, crn)#looks at the current schedule, remove the selected class mentally, then find valid candidates that do not conflict
    return {"options": options}# This sends the result back to swift


@router.post("/swap")
async def swap_course(data: dict = Body(...)):
    schedule = data.get("schedule")#gets the current schedule from request
    crn = data.get("crn")#gets the crn being removed
    replacement_crn = data.get("replacement_crn")#gets the crn being added

    if not state.candidates_store:
        return {"error": "No candidate data found. Upload PDF first."}

    if not replacement_crn:
        return {"error": "No replacement CRN provided."}

    updated = replace_course(schedule, state.candidates_store, crn, replacement_crn)# inside this function removes old crn, finds replacement crn, return updated schedule
    return {"new_schedule": updated}
