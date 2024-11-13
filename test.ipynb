import revisit as rvt
import data.rvt_data as rvt_data

if __name__ == "__main__":

    study_metadata = rvt.studyMetadata(**rvt_data.metadata)
    ui_config = rvt.uiConfig(**rvt_data.ui_config)

    base_question_1 = rvt.component(name='base_component_1', **rvt_data.base_component_1_data)
    base_question_2 = rvt.component(name='base_component_2', **rvt_data.base_component_2_data)
    base_question_3 = rvt.component(name='base_component_3', **rvt_data.base_component_3_data)

    # Iterate Through Each Set of Options

    introduction = rvt.component(name='introduction', type='Markdown')

    final_sequence = rvt.sequence(order='fixed', components=[introduction])
    inner_sequence = rvt.sequence(order='latinSquare')
    sequences = {}
    for key, curr_options in rvt_data.options.items():
        # Iterate through vis, text, both
        for question_type in ['Vis', 'Text', 'TextAndVis']:
            # Question 1
            curr_question_1 = rvt.component(
                name=f'{key.lower()}-{question_type}-question-1',
                base=base_question_1,
                path=f"Upset-Alttext-User-Survey/assets/{key}{question_type}.md",
                correctAnswer=rvt_data.correct_answers[key],
            ).responses([
                *base_question_1.response,
                # Both the following do the same exact thing -- different ways to handle it
                rvt.from_response(base_question_1.get_response(id='voq2')).data(
                    options=curr_options,
                    prompt=rvt_data.question_type_data[question_type]['q1_prompt']
                ),
                rvt.response(
                    base=base_question_1.get_response(id='voq3'),
                    options=curr_options + ['Empty Intersection (no sets)']
                )
            ])

            # Question 2
            curr_question_2 = rvt.component(
                name=f'{key.lower()}-{question_type}-question-2',
                base=base_question_2,
                path=f"Upset-Alttext-User-Survey/assets/{key}{question_type}.md",
                description=rvt_data.question_type_data[question_type]['description']
            )

            # Question 3
            curr_question_3 = rvt.component(
                name=f'{key.lower()}-{question_type}-question-3',
                base=base_question_3,
                path=f"Upset-Alttext-User-Survey/assets/{key}{question_type}.md",
                description=rvt_data.question_type_data[question_type]['description']
            ).responses([
                # Only one response for this. Copy original response, change prompt.
                rvt.from_response(base_question_2.get_response(id='voq1')).data(
                    prompt=rvt_data.question_type_data[question_type]['q3_prompt']
                )
            ])

            curr_sequence = rvt.sequence(
                order='fixed',
                components=[
                    curr_question_1,
                    curr_question_2,
                    curr_question_3
                ]
            )
            sequences[f'{key.lower()}-{question_type}'] = curr_sequence

# Using perumte function in revisit.py file
for set in rvt.permute(rvt_data.options.keys()):
    temp_sequence = rvt.sequence(
        order='latinSquare',
        components=[
            sequences[f'{set[0]}-Vis'],
            sequences[f'{set[1]}-TextAndVis'],
            sequences[f'{set[2]}-Text']
        ]
    )
    # Append inner sequence with new sequence
    inner_sequence = inner_sequence + temp_sequence

# Add final sequence with inner sequence
final_sequence = final_sequence + inner_sequence


study = rvt.study(
    studyMetadata=study_metadata,
    uiConfig=ui_config,
    sequence=final_sequence
)

print(study)
