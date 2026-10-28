import requests# request lets you sent HTTP request, like GET, POST, ect.
# In the backend you use this to talk to WPUNJ's registration website/API
import time #


def reset_session(session: requests.Session):# A session is like a browser that remembers cookies and connection data. This does not create the session object yet but is a type hint
    url = "https://selfservice9.wpunj.edu/StudentRegistrationSsb/ssb/classSearch/resetDataForm"
    response = session.get(url)# This sends a get request into the home browser. It like opening this page first
    response.raise_for_status()#Make sure the reset request worked. If it did not work, throw an error

def make_unique_session():#Creates a unique session ID every time it is called
    return f"regi{int(time.time() * 1000)}"

def get_all_classes(term="202640", page_max_size=3000):#Retrieves all classes from the university API
    # Session is lets the server recoginize you and how cookies is where the id is stored and handled
    #This function connects to the WPUNJ Banner API and downloads all available classes for a specific semester

    session = requests.Session() #Creates an HTTP session. A session stores cookies, authentication information, connection setting. Think of it as opening a browser window that remembers what happened previously

    reset_session(session) #Visits the class search home page first. This initailizes the cookies required by Banner otherwise the search request may fail

    unique_id = make_unique_session()# You create a unique session id to distinguish one session from another

    url = f"https://selfservice9.wpunj.edu/StudentRegistrationSsb/ssb/searchResults/searchResults?txt_term=202640&startDatepicker=&endDatepicker=&uniqueSessionId=y95ag1778381973528&pageOffset=0&pageMaxSize=10&sortColumn=subjectDescription&sortDirection=asc"

    response = session.get(url)#here params are added to the url

    response.raise_for_status()# raises an exception if the HTTP status code indicate failure

    data = response.json()#Parses the JSON response into a Python dictionary

    reset_session(session)# visit the home page once more.
    # This clears and refresh the session so the same session can be safely used for furutre api calls, such as prereq request

    return data.get("data", [])#