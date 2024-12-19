import revisit as rvt
import data.test.metadata as metadata


study_metadata = rvt.studyMetadata(**metadata.study_metadata)
ui_config = rvt.uiConfig(**metadata.ui_config)

# Get parameter data from CSV file

# Response context can be omitted here since there is only one response total.
# Using here for example sake -- common to set all to required and all have same location.
# Alternatively can set response context to also have 'iframe' key to specify all responses have other properties
# (i.e. can specify that all iframe responses have the same prompt and hidden value)

my_study = rvt.study(
    studyMetadata=study_metadata,
    uiConfig=ui_config
).response_context(
    all={
        'required': True,
        'location': 'aboveStimulus'
    }
)


# Initialize base component with one response
component = rvt.component(
    component_name__='likert-component',
    type='questionnaire',
).responses([
    rvt.response(
        id='my_likert',
        type='likert',
        prompt="How confident are you in your answers?",
        secondaryText="1 = Not at all confident, 5 = Very confident",
        rightLabel="Very",
        numItems=5
    ),
    rvt.response(
        id='my_slider',
        type='slider',
        prompt="How are you feeling?",
        options=[
            {
                "label": "Bad",
                "value": 0
            },
            {
                "label": "OK",
                "value": 50
            },
            {
                "label": "Good",
                "value": 100
            }
        ]
    ),
])

sequence = rvt.sequence(components=[component])

my_study.sequence = sequence

# Save file
my_study.save('data/test/config.json')
