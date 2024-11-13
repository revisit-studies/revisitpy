metadata = {
        "title": "Upset Alttext User Survey",
        "version": "pilot",
        "authors": [
            "The reVISit Team"
        ],
        "date": "2024-03-19",
        "description": "A sample questionnaire study",
        "organizations": [
            "University of Utah"
        ]
    }

ui_config = {
        "contactEmail": "test@test.com",
        "helpTextPath": "Upset-Alttext-User-Survey/assets/upset.md",
        "logoPath": "revisitAssets/revisitLogoSquare.svg",
        "urlParticipantIdParam": "PROLIFIC_PID",
        "studyEndMsg": ("**Thank you for participating. You may click this link and return to Prolific**:"
                        "[https://app.prolific.com/submissions/complete?cc=CVRK3FRJ]"
                        "(https://app.prolific.com/submissions/complete?cc=CVRK3FRJ)"),
        "withProgressBar": True,
        "autoDownloadStudy": False,
        "sidebar": True,
        "enumerateQuestions": True,
        "sidebarWidth": 440
    }

survey_choices = ["Just Visualization", "Just Text Description", "Text and Visualization Combined"]

training_options_one = ["Action", "Adventure", "Documentary", "Fantasy", "Romance", "Thriller"]

training_options_two = ["Adventure", "Documentary", "Fantasy", "Mystery", "War"]

training_options_three = [
    "Action", "Comedy", "Drama", "Horror", "Mystery", "Romance", "SciFi", "Thriller"
]

options = {
    'covid': ["Anosmia", "Cough", "Diarrhea", "Fatigue", "Fever", "Shortness of Breath"],
    'tennis': ["Australian", "French Open", "US Open", "Wimbledon"],
    'organization': ["CICA", "G-5", "Interpol", "SAARC", "SICA", "UN", "UNESCO", "UPU", "WHO"]
}

question_type_data = {
    "Vis": {
        "description": "Content: Visualization Only",
        "q1_prompt": "How many sets are shown in the upset plot?",
        "q3_prompt": "What are your insights and take-aways from this plot for this data?"
    },
    "Text": {
        "description": "Content: Text Only",
        "q1_prompt": "How many sets are shown in the description?",
        "q3_prompt": "What are your insights and take-aways from the description of this data?"
    },
    "TextAndVis": {
        "description": "Content: Text and Visual",
        "q1_prompt": "How many sets are there?",
        "q3_prompt": "What are your insights and take-aways from the plot and the description for this data?"
    },
}

correct_answers = {
    "covid": [
        {
            "id": "voq1",
            "answer": "6"
        },
        {
            "id": "voq2",
            "answer": "Fatigue"
        },
        {
            "id": "voq3",
            "answer": "Anosmia,Fatigue"
        },
        {
            "id": "voq4",
            "answer": "281"
        },
        {
            "id": "voq5",
            "answer": "It is the intersection of 2-3 sets"
        },
        {
            "id": "voq6",
            "answer": "Diverging a lot"
        },
        {
            "id": "voq7",
            "answer": "Yes"
        },
        {
            "id": "voq8",
            "answer": "Yes"
        }
    ],
    "tennis": [
        {
            "id": "voq1",
            "answer": "4"
        },
        {
            "id": "voq2",
            "answer": "Australian"
        },
        {
            "id": "voq3",
            "answer": "French Open"
        },
        {
            "id": "voq4",
            "answer": "23"
        },
        {
            "id": "voq5",
            "answer": "It is only of a single set"
        },
        {
            "id": "voq6",
            "answer": "Roughly equal"
        },
        {
            "id": "voq7",
            "answer": "No"
        },
        {
            "id": "voq8",
            "answer": "Yes"
        }
    ],
    "organization": [
        {
            "id": "voq1",
            "answer": "8"
        },
        {
            "id": "voq2",
            "answer": "UPU"
        },
        {
            "id": "voq3",
            "answer": "Interpol,UN,UNESCO,UPU,WHO"
        },
        {
            "id": "voq4",
            "answer": "117"
        },
        {
            "id": "voq5",
            "answer": "It is the intersection of many sets"
        },
        {
            "id": "voq6",
            "answer": "Diverging a lot"
        },
        {
            "id": "voq7",
            "answer": "Yes"
        },
        {
            "id": "voq8",
            "answer": "No"
        }
    ]
}

base_component_1_data = {
    "type": "markdown",
    "nextButtonLocation": "sidebar",
    "description": "Content: Visualization Only",
    "instruction": "Please answer the following question about the plot:",
    "response": [
        {
            "id": "voq1",
            "prompt": "How many sets are shown in the upset plot?",
            "type": "numerical",
            "max": 100
        },
        {
            "id": "voq2",
            "prompt": "What is the largest set?",
            "type": "dropdown",
            "placeholder": "Please select an answer",
            "options": []
        },
        {
            "id": "voq3",
            "prompt": "What is the largest intersection?",
            "secondaryText": "Select all Sets in the Intersection",
            "type": "checkbox",
            "options": [
                "Empty Intersection (no sets)"
            ]
        },
        {
            "id": "voq4",
            "prompt": "How large is the largest intersection?",
            "type": "numerical",
            "max": 1000000000
        },
        {
            "id": "voq5",
            "prompt": "How many sets make up the largest intersection?",
            "type": "dropdown",
            "placeholder": "Please choose your answer",
            "options": [
                "It is only of a single set",
                "It is the intersection of 2-3 sets",
                "It is the intersection of many sets",
                "It is the empty intersection (no sets)"
            ]
        },
        {
            "id": "voq6",
            "prompt": "How similar are the set sizes?",
            "type": "dropdown",
            "placeholder": "Please choose your answer",
            "options": [
                {
                    "label": "Roughly equal (all the set sizes look similar)",
                    "value": "Roughly equal"
                },
                {
                    "label": "Diverging a bit (the sizes of the largest set and"
                             " the smallest set don't differ largely)",
                    "value": "Diverging a bit"
                },
                {
                    "label": "Diverging a lot (the sizes of the largest set and"
                             " the smallest set differ largely)",
                    "value": "Diverging a lot"
                }
            ]
        },
        {
            "id": "voq7",
            "prompt": "Is the largest set present in the largest intersection?",
            "type": "radio"
        },
        {
            "id": "voq8",
            "prompt": "Is the all-set intersection (intersection having all the sets) present? ",
            "type": "radio"
        }
    ]
}

base_component_2_data = {
    "type": "markdown",
    "nextButtonLocation": "sidebar",
    "description": "Content: Visualization Only",
    "instruction": "Rate the content:",
    "response": [
        {
            "id": "voq1",
            "prompt": "How confident are you in your answers?",
            "secondaryText": "1 = Not at all confident, 5 = Very confident",
            "type": "likert",
            "rightLabel": "Very"
        },
        {
            "id": "voq2",
            "prompt": "How well did you understand the information presented?",
            "secondaryText": "1 = Not at all understood, 5 = Completely understood",
            "type": "likert",
            "rightLabel": "Completely"
        },
        {
            "id": "voq3",
            "prompt": "How effective was the plot at conveying information?",
            "secondaryText": "1 = Not at all effective, 5 = Extremely effective",
            "type": "likert",
            "rightLabel": "Extremely"
        }
    ]
}

base_component_3_data = {
    "type": "markdown",
    "nextButtonLocation": "sidebar",
    "description": "Content: Visualization Only",
    "instruction": "Please answer the following question about the chart:",
    "response": [
        {
            "id": "voq1",
            "prompt": "What are your insights and take-aways from this plot for this data?",
            "required": True,
            "location": "sidebar",
            "type": "longText",
            "placeholder": "Please enter your answer here"
        }
    ]
}
