import old.revisit_alpha as rvt
import data.scatterjnd.metadata as metadata


study_metadata = rvt.studyMetadata(**metadata.study_metadata)
ui_config = rvt.uiConfig(**metadata.ui_config)

# Get parameter data from CSV file
study_data = rvt.data('data/scatterjnd/data.csv')

# Response context can be omitted here since there is only one response total.
# Using here for example sake -- common to set all to required and all have same location.
# Alternatively can set response context to also have 'iframe' key to specify all responses have other properties
# (i.e. can specify that all iframe responses have the same prompt and hidden value)

jnd_study = rvt.study(
    studyMetadata=study_metadata,
    uiConfig=ui_config
).response_context(
    all={
        'required': True,
        'location': 'aboveStimulus'
    }
)

# Create basic components -- pulling in info from metadata file.
introduction = rvt.component(
    component_name__='introduction',
    **metadata.introduction
)

training = rvt.component(
    component_name__='training',
    **metadata.training
)
practice = rvt.component(
    component_name__='practice',
    **metadata.practice
)
begin = rvt.component(
    component_name__='begin',
    **metadata.practice
)

# Initialize base component with one response
base_component = rvt.component(
    component_name__='base-component-1',
    type='react-component',
    path='emma-jnd/vistaJND/src/components/vis/JNDScatterRevised.tsx'
).responses([
    rvt.response(
        id='scatterSelections',
        prompt='Select an option',
        type='iframe',
        hidden=True
    )
])

# Create a sequence of responses
# 'from_data' creates an iterator over the provided data. To use values from
# dataset, prefix with 'datum:' and then use header key
inner_sequence = rvt.sequence(
    order='random'
).from_data(study_data).component(
    base__=base_component,
    component_name__='datum:id',
    parameters={
        'r1': 'datum:r1',
        'r2': 'datum:r2',
        'above': 'datum:position'
    }
)


# Initialize sequence
sequence = rvt.sequence(
    order='fixed',
    components=[
        introduction,
        training,
        practice,
        begin,
        # Above are components.
        # Inner sequence is entire separate sequence
        # defined above.
        inner_sequence
    ]
)

# Set sequence
jnd_study.sequence = sequence

# Save file
jnd_study.save('data/scatterjnd/config.json')