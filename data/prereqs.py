# Course prerequisite and restriction rules.
# You can keep adding courses here instead of making main.py huge.

PREREQS = {
    "DATABASE DRIVEN WEB APPLICATIONS": {
        "sections": [
            {"courseReferenceNumber": "42635", "restriction": None},
            {"courseReferenceNumber": "42636", "restriction": "WP Online"},
        ],
        "prerequisites": {
            "Subject": "Computer Science",
            "course_number": "CS (2400 or 2420 or 2421) with a C-",
        },
    },
    "Defensive Security": {
        "sections": [
            {"courseReferenceNumber": "42856", "restriction": None},
        ],
        "prerequisites": {
            "Subject": "Computer Science",
            "course_number": "CS 3800 with a C-",
        },
    },
    "Computer Science 1": {
        "sections": [
            {"courseReferenceNumber": "41144", "restriction": "WP Online"},
            {"courseReferenceNumber": "40551", "restriction": None},
            {"courseReferenceNumber": "40550", "restriction": None},
        ],
        "prerequisites": {
            "Subject": "Mathematics",
            "course_number": "1150 or 1350 or 1160 or 1600 with a C-",
        },
    },
    "Computer Science Seminar": {
        "sections": [
            {
                "courseReferenceNumber": "40553",
                "restriction": "Must be a senior and must be enrolled in Computer Science",
            }
        ],
        "prerequisites": {
            "Subject": "Computer Science",
            "course_number": "3420 with a C-",
        },
    },
    "COMPUTER AND INFORMATION TECHNOLOGY": {
        "sections": [
            {"courseReferenceNumber": "41143", "restriction": "WP Online"},
            {"courseReferenceNumber": "40102", "restriction": None},
        ]
    },
    "Fundamental of Computer Hardware": {
        "sections": [
            {"courseReferenceNumber": "41181", "restriction": "WP Online"},
            {"courseReferenceNumber": "41180", "restriction": None},
        ],
        "prerequisites": {
            "Subject": "Mathematics or Computer Science",
            "course_number": "Computer 2300 and 1160 or 1350 with a C-",
        },
    },
    "Penetration Testing & Ethical": {
        "sections": [
            {"courseReferenceNumber": "42634", "restriction": "WP Online"},
            {"courseReferenceNumber": "40829", "restriction": None},
        ],
        "prerequisites": {
            "Subject": "Computer Science",
            "course_number": "Computer Science 3660 or 3380 with a C-",
        },
    },
    "Applied Operating Systems": {
        "sections": [
            {"courseReferenceNumber": "41182", "restriction": "WP Online"},
            {"courseReferenceNumber": "42440", "restriction": "Approval by Academic Dean"},
        ],
        "prerequisites": {
            "Subject": "Computer Science",
            "course_number": "2350 with a C-",
        },
    },
    "Object-Oriented Programming in Java": {
        "sections": [
            {"courseReferenceNumber": "42224", "restriction": "WP Online"},
            {"courseReferenceNumber": "41584", "restriction": None},
        ],
        "prerequisites": {
            "Subject": "Computer Science or Mathematics",
            "course_number": "CS 2300 and (MATH 1160 or 1350) with a C-",
        },
    },
    "Data Base Management": {
        "sections": [{"courseReferenceNumber": "42643", "restriction": None}],
        "prerequisites": {
            "Subject": "Computer Science",
            "course_number": "CS 2300 or 342 with a C-",
        },
    },
    "Discrete Structures": {
        "sections": [{"courseReferenceNumber": "40552", "restriction": "CS Major"}],
        "prerequisites": {
            "Subject": "Computer Science or Mathematics",
            "course_number": "CS 2300 and (MATH 1160 or 1350) with a C-",
        },
    },
    "Computer Architecture and Organization": {
        "sections": [{"courseReferenceNumber": "42071", "restriction": "None"}],
        "prerequisites": {
            "Subject": "Computer Science",
            "course_number": "CS (3410 or 341) and (CS 3450 or 345) with a C-",
        },
    },
    "Computer Networks 1": {
        "sections": [
            {"courseReferenceNumber": "42225", "restriction": "WP Online"},
            {"courseReferenceNumber": "40748", "restriction": None},
        ],
        "prerequisites": {
            "Subject": "Computer Science",
            "course_number": "CS 2350",
        },
    },
    "Cloud Computing": {
        "sections": [
            {"courseReferenceNumber": "42638", "restriction": None},
            {"courseReferenceNumber": "42639", "restriction": "WP Online"},
        ],
        "prerequisites": {
            "Subject": "Computer Science",
            "course_number": "CS (3380 or 3420 or 3401) with a C-",
        },
    },
    "Computer Networks 2": {
        "sections": [{"courseReferenceNumber": "42633", "restriction": None}],
        "prerequisites": {
            "Subject": "Computer Science",
            "course_number": "CS 2352 and (3350 or 3351)",
        },
    },
    "Software Engineering": {
        "sections": [{"courseReferenceNumber": "42068", "restriction": "CS/CIT/IT/WIT major"}],
        "prerequisites": {
            "Subject": "Computer Science",
            "course_number": "CS 3420 with a c-",
        },
    },
    "DATA MINING & MACHINE LEARNING": {
        "sections": [{"courseReferenceNumber": "41087", "restriction": "None"}],
        "prerequisites": {
            "Subject": "Computer Science",
            "course_number": "CS (2400 or 2420 or 2421) and 2300 with a C-",
        },
    },
    "CyberSecurity Essentials": {
        "sections": [{"courseReferenceNumber": "42069", "restriction": "WP Online"}],
        "prerequisites": {
            "Subject": "Computer Science",
            "course_number": "CS 3660 with a C-",
        },
    },
    "Computer Science 2": {
        "sections": [{"courseReferenceNumber": "40137", "restriction": None}],
        "prerequisites": {
            "Subject": "CS or Math",
            "course_number": "CS 2300 and (1160 or 1350)",
        },
    },
    "Operating systems": {
        "sections": [{"courseReferenceNumber": "14225", "restriction": None}],
        "prerequisites": {
            "Subject": "CS",
            "course_number": "(2800 or 280) and (3420 or 342)",
        },
    },
}
