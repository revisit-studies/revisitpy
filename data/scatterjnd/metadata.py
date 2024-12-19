study_metadata = {
    "title": "Scatter Plot JND Study",
    "version": "pilot",
    "authors": ["The reVISit Team"],
    "date": "2024-06-26",
    "description": "This is a reVISit variation study of JND(Just Noticeable Difference) Scatter Plot experiment.",
    "organizations": ["University of Utah", "WPI", "University of Toronto"]
}

ui_config = {
    "contactEmail": "contact@revisit.dev",
    "helpTextPath": "ScatterJND-study/assets/help.md",
    "logoPath": "revisitAssets/revisitLogoSquare.svg",
    "withProgressBar": True,
    "autoDownloadStudy": False,
    "sidebar": False,
    "urlParticipantIdParam": "PROLIFIC_PID",
    "studyEndMsg": "**Thank you for completing the study."
    " You may click this link and return to Prolific**: [yourProlificLink](yourProlificLink)"
}

introduction = {
    "type": "markdown",
    "path": "ScatterJND-study/assets/introduction.md",
    "response": [
        {
            "id": "prolificId",
            "prompt": "Please enter your Prolific ID",
            "required": True,
            "location": "belowStimulus",
            "type": "shortText",
            "placeholder": "Prolific ID",
            "paramCapture": "PROLIFIC_PID"
        }
    ]
}

training = {
    "type": "markdown",
    "path": "ScatterJND-study/assets/training.md",
    "response": []
}

practice = {
    "type": "react-component",
    "path": "emma-jnd/vistaJND/src/components/vis/PracticeScatter.tsx",
    "response": [
        {
            "id": "completed",
            "prompt": "Did you complete the practice?",
            "type": "iframe",
            "hidden": True
        }
    ]
}
begin = {
    "type": "markdown",
    "path": "ParallelJND-study/assets/begin.md",
    "response": []
}
