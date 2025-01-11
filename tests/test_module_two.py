import src.revisit as rvt


study_metadata = rvt.studyMetadata(
    title='Test Title',
    date="",
    organizations=[],
    authors=[],
    version='1.0',
    description=""
)

newResponse = rvt.response(
    id='hello',
    type='matrix-radio',
    required=False,
    prompt='Test Prompt',
    test='hello',
    answerOptions='satisfaction5',
    questionOptions=['Test1', 'Test2']
)

base_comp = rvt.component(
    type='questionnaire',
    response=[],
    component_name__='Base_Test'
)

comp_one = rvt.component(
    base__=base_comp,
    component_name__='Test',
).responses([
    newResponse
])

comp_two = rvt.component(
    base__=base_comp,
    component_name__='TestTwo',
).responses([
    newResponse
])


ui_config = rvt.uiConfig(
    sidebar=True,
    contactEmail='',
    withProgressBar=True,
    logoPath='',
    helpTextPath=''
)


introduction = rvt.component(
    component_name__='introduction',
    type='markdown',
    path="ScatterJND-study/assets/introduction.md",
    response=[
        rvt.response(**{
            "id": "prolificId",
            "prompt": "Please enter your Prolific ID",
            "required": True,
            "location": "belowStimulus",
            "type": "shortText",
            "placeholder": "Prolific ID",
            "paramCapture": "PROLIFIC_PID"
        })
    ]
)

training = rvt.component(
    component_name__='training',
    type='markdown',
    path="ScatterJND-study/assets/training.md",
    response=[]
)

practice_response = rvt.response(
    id="completed",
    prompt="Did you complete the practice?",
    type="iframe",
    hidden=True,
    required=True
)
practice = rvt.component(
    component_name__='practice',
    type='react-component',
    path="emma-jnd/vistaJND/src/components/vis/PracticeScatter.tsx",
).responses([
    practice_response
])

begin = rvt.component(
    component_name__='begin',
    type='markdown',
    path="ParallelJND-study/assets/begin.md"
)

base_component = rvt.component(
    component_name__='base-component-1',
    type='react-component',
    path='emma-jnd/vistaJND/src/components/vis/JNDScatterRevised.tsx'
).responses([
    rvt.response(
        id='scatterSelections',
        prompt='Select an option',
        type='iframe',
        hidden=True,
        required=True
    )
])

study_data = rvt.data('data/data.csv')

sequence = rvt.sequence(order='random').from_data('study_data').component(
    base__=base_component,
    component_name__='datum:id',
    parameters={
        'r1': 'datum:r1',
        'r2': 'datum:r2',
        'above': 'datum:position'
    }
)

other_sequence = rvt.sequence(
    order='fixed',
    components=[
        introduction,
        training,
        practice,
        begin
    ]
)


study = rvt.studyConfig(
    schema='test',
    uiConfig=ui_config,
    studyMetadata=study_metadata,
    sequence=other_sequence + sequence,
    components=[rvt.component(component_name__='my-test-thing', type='questionnaire', response=[])]
)

print(study)
