import src.revisit.revisit as rvt
import unittest
import json


class TestComponentsAndResponses(unittest.TestCase):
    def test_markdown_component(self):
        comp_one = rvt.component(
                    type='markdown',
                    path='./assets/test-path',
                    response=[],
                    component_name__='Base_Test'
                )

        self.assertEqual(
            json.loads(comp_one.__str__()),
            {
                'path': './assets/test-path',
                'response': [],
                'type': 'markdown'
            }
        )

    def test_response_getter(self):
        comp_two = rvt.component(
            type='questionnaire',
            response=[],
            component_name__='Base_Test'
        ).responses([
            rvt.response(
                id='first-response',
                type='matrix-checkbox',
                answerOptions='likely-7',
                required=True,
                prompt='Fake Prompt',
                questionOptions=[
                    'Question One',
                    'Question Two',
                    'Question Three'
                ]
            )
        ])

        response_one = comp_two.get_response(id='first-response')

        self.assertEqual(
            json.loads(response_one.__str__()),
            {'answerOptions': 'likely-7', 'id': 'first-response', 'prompt': 'Fake Prompt', 'questionOptions': ['Question One', 'Question Two', 'Question Three'], 'required': True, 'type': 'matrix-checkbox'}
        )


if __name__ == "__main__":
    unittest.main()
