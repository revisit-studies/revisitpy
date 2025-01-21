'''
This is a blank script for testing purposes. Only this script will
currently be tracked in git. Any other scripts in this directory will
not be tracked by git.

This file is specifically useful for sharing code between
contributors of this package for testing purposes only.

This file is also ignored by the package builder.

Run this file using the module syntax:

uv run -m scripts.test_script
'''

import revisitpy.revisitpy as rvt
import random

if __name__ == "__main__":
    study_data = rvt.data('./scripts/data.csv')

    def component_function(id, r1, r2, position, component__):
        if component__.type == 'questionnaire':
            print('hello')
        return rvt.component(
            type='website',
            path='',
            parameters={
                'id': id,
                'r1': r1,
                'r2': r2,
                'position': position
            },
            component_name__=f'new__id:{id}_r1:{r1}_r2:{r2}_position:{position}'
        )

    comp_one = rvt.component(
        component_name__='my-component',
        type='questionnaire',
        metadata__={
            "id": random.randint(1, 10),
            'r1': random.randint(1, 10),
            'r2': random.randint(1, 10),
            'position': True
        }
    )

    comp_two = rvt.component(
        component_name__='my-component',
        type='questionnaire',
        metadata__={
            'id': 3
        }
    )

    first_seq = rvt.sequence(order='fixed', components=[comp_one])
    second_seq = rvt.sequence(order='fixed', components=[comp_one])
    sequence_one = first_seq + second_seq

    # print(sequence_one)
    sequence_one = sequence_one.component(component_function)

    # sequence = rvt.sequence(order='fixed', components=[comp_one]).from_data(study_data).component(component_function)

    # print(sequence_one)

    sequence_two = rvt.sequence(order='fixed', components=[comp_one]).from_data(study_data).component(component_function)

    # print(sequence_two)

    sequence_three = rvt.sequence(order='fixed', components=[comp_two]).permute(
        factors=[{'r1': 1}, {'r1': 2}],
        order='fixed'
    ).permute(
        factors=[{'r2': 3}, {'r2': 4}],
        order='fixed'
    ).permute(
        factors=[{'position': True}, {'position': False}],
        order='random'
    )

    # print(sequence_three)
    '''
    Output:

    {
        "components": [
            {
                "components": [
                    {
                        "components": [
                            "my-component__r1:1__r2:4__position:True",
                            "my-component__r1:1__r2:4__position:False"
                        ],
                        "order": "random"
                    },
                    {
                        "components": [
                            "my-component__r1:1__r2:3__position:True",
                            "my-component__r1:1__r2:3__position:False"
                        ],
                        "order": "random"
                    }
                ],
                "order": "fixed"
            },
            {
                "components": [
                    {
                        "components": [
                            "my-component__r1:2__r2:4__position:True",
                            "my-component__r1:2__r2:4__position:False"
                        ],
                        "order": "random"
                    },
                    {
                        "components": [
                            "my-component__r1:2__r2:3__position:True",
                            "my-component__r1:2__r2:3__position:False"
                        ],
                        "order": "random"
                    }
                ],
                "order": "fixed"
            }
        ],
        "order": "fixed"
    }

    '''

    sequence_three = rvt.sequence(order='fixed', components=[comp_two]).permute(
        factors=[{'r1': 1}, {'r1': 2}],
        order='fixed'
    ).permute(
        factors=[{'r2': 3}, {'r2': 4}],
        order='fixed'
    ).permute(
        factors=[{'position': True}, {'position': False}],
        order='random'
    ).component(component_function)

    print(sequence_three)

    '''
    {
        "components": [
            {
                "components": [
                    {
                        "components": [
                            "new__id:3_r1:2_r2:3_position:False",
                            "new__id:3_r1:2_r2:3_position:True"
                        ],
                        "order": "random"
                    },
                    {
                        "components": [
                            "new__id:3_r1:2_r2:4_position:False",
                            "new__id:3_r1:2_r2:4_position:True"
                        ],
                        "order": "random"
                    }
                ],
                "order": "fixed"
            },
            {
                "components": [
                    {
                        "components": [
                            "new__id:3_r1:1_r2:3_position:False",
                            "new__id:3_r1:1_r2:3_position:True"
                        ],
                        "order": "random"
                    },
                    {
                        "components": [
                            "new__id:3_r1:1_r2:4_position:False",
                            "new__id:3_r1:1_r2:4_position:True"
                        ],
                        "order": "random"
                    }
                ],
                "order": "fixed"
            }
        ],
        "order": "fixed"
    }
    '''

    print(comp_one.get('type'))

    # response_one = rvt.response(
    #     id='r-1',
    #     type='shortText',
    #     required=False,
    #     location='belowStimulus',
    #     prompt=''
    # )

    # response_one.set(prompt='New Prompt')
    # print(response_one)

    # response_one.set(options=['Option 1', 'Option 2', 'Option 3'])
