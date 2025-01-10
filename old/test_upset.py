import old.revisit_alpha as rvt
import data.upset.metadata as metadata

'''
To Note:

1. The use of 'response_context' here is not creating a 'responseContext' key in any component
or in the study. It is automatically doing the job of what responseContext is designed to do --
setting defaults for responses based on type (or for all responses when using 'all')
that don't already have a value assigned.

2. Base components are not generated -- components are created individually.
'''

# Create study metadata and ui config from JSON object in rvt_data
study_metadata = rvt.studyMetadata(**metadata.metadata)
ui_config = rvt.uiConfig(**metadata.ui_config)

# Initialize study with studyMetadata
# Use method chaining to assign a default response context
my_study = rvt.study(
    studyMetadata=study_metadata,
    uiConfig=ui_config
).response_context(
    all={'required': True, "location": "sidebar"}
)

# Initialize base components to copy from.
base_question_1 = rvt.component(component_name__='base_component_1', **metadata.base_component_1_data)
base_question_2 = rvt.component(component_name__='base_component_2', **metadata.base_component_2_data)
base_question_3 = rvt.component(component_name__='base_component_3', **metadata.base_component_3_data)

# Create blank introduction component.
introduction = rvt.component(component_name__='introduction', type='Markdown')

# Initialize an outer sequence with the introduction component
final_sequence = rvt.sequence(order='fixed', components=[introduction])

# Initialize an inner sequence with no components added.
inner_sequence = rvt.sequence(order='latinSquare')

# Dictionary to store various sequence blocks as we generate components
sequences = {}

# Iterate through data options (i.e. 'covid', 'tennis', 'organization')
for key, curr_options in metadata.options.items():

    # Iterate through vis, text, both
    for question_type in ['Vis', 'Text', 'TextAndVis']:

        # 'edit_response' and 'response_context' all rely on method chaining.
        curr_question_1 = rvt.component(
            # Set a name -- this will be used as a key
            component_name__=f'{key.lower()}-{question_type}-question-1',
            # Inherit base
            base__=base_question_1,
            # Overload path and correctAnswer
            path=f"Upset-Alttext-User-Survey/assets/{key}{question_type}.md",
            correctAnswer=metadata.correct_answers[key],
        ).edit_response(
            # Edit response with id='voq2'
            id='voq2',
            options=curr_options,
            prompt=metadata.question_type_data[question_type]['q1_prompt']
        ).edit_response(
            # Edit response with id='voq3'
            id='voq3',
            options=curr_options + ['Empty Intersection (no sets)']
        ).response_context(
            # Set response context for this component.
            numerical={"placeholder": "Please enter your answer here", "min": 0},
            radio={"options": ["Yes", "No"]}
        )

        # Question 2
        curr_question_2 = rvt.component(
            component_name__=f'{key.lower()}-{question_type}-question-2',
            base__=base_question_2,
            path=f"Upset-Alttext-User-Survey/assets/{key}{question_type}.md",
            description=metadata.question_type_data[question_type]['description']
        ).response_context(
            likert={"numItems": 5, "leftLabel": "Not"}
        )

        # Question 3
        curr_question_3 = rvt.component(
            component_name__=f'{key.lower()}-{question_type}-question-3',
            base__=base_question_3,
            path=f"Upset-Alttext-User-Survey/assets/{key}{question_type}.md",
            description=metadata.question_type_data[question_type]['description']
        ).responses([
            # Only one response. Instead of using edit_response, we can redefine responses.
            # 'from_response' makes a deep copy of the response. 'get_response' can search
            # for a response based on id from a component.
            # 'data' is a way to assign the values of a response without reinitializing it
            rvt.from_response(base_question_2.get_response(id='voq1')).data(
                prompt=metadata.question_type_data[question_type]['q3_prompt']
            )
            # Alternatively, we can use similar methods to components inheriting bases::
            # rvt.response(base_question_2.get_response(id='voq1'),
            # prompt=prompt=rvt_data.question_type_data[question_type]['q3_prompt'])
        ])

        # Create a sequence with the components above
        curr_sequence = rvt.sequence(
            order='fixed',
            components=[
                curr_question_1,
                curr_question_2,
                curr_question_3
            ]
        )
        # Track the sequence in a dictionary
        sequences[f'{key.lower()}-{question_type}'] = curr_sequence

# Permuting over all possible combinations
for set in rvt.permute(metadata.options.keys()):
    # Create a sequence with the sub sequences
    temp_sequence = rvt.sequence(
        order='latinSquare',
        components=[
            sequences[f'{set[0]}-Vis'],
            sequences[f'{set[1]}-TextAndVis'],
            sequences[f'{set[2]}-Text']
        ]
    )
    # Append inner sequence with new sequence
    # This is shorthand for inner_sequence.components.append(temp_sequence)
    inner_sequence = inner_sequence + temp_sequence

# Add final sequence with inner sequence
final_sequence = final_sequence + inner_sequence

# Assign sequence to study
my_study.sequence = final_sequence

my_study.save('data/upset/config.json')
