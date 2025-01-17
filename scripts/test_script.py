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

import src.revisit.revisit as rvt

if __name__ == "__main__":
    comp_one = rvt.component(
        component_name__='my-component',
        type='questionnaire',
    )

    print(comp_one)

    response_one = rvt.response(
        id='r-1',
        type='shortText',
        required=False,
        location='belowStimulus',
        prompt=''
    )

    response_one.set(prompt='New Prompt')
    print(response_one)

    response_one.set(options=['Option 1', 'Option 2', 'Option 3'])
