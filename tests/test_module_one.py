import revisitpy.revisitpy as rvt
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

    
class TestConfigGeneration(unittest.TestCase):
    def test_generated_config_matches_json(self):
        # Load the reference config
        with open("tests/config.json", "r") as f:
            reference_config = json.load(f)

        # Generate the config using revisitpy
        study_metadata = rvt.studyMetadata(**reference_config["studyMetadata"])
        ui_config = rvt.uiConfig(**reference_config["uiConfig"])

        # Build components
        components = {}
        for name, comp in reference_config["components"].items():
            responses = [
                rvt.response(**resp) for resp in comp.get("response", [])
            ]
            component = rvt.component(
                **{k: v for k, v in comp.items() if k != "response"},
                response=responses,
                component_name__=name
            )
            components[name] = component

        # Build sequence, replacing names with actual component objects
        sequence_components = [
            components[name] if name in components else name
            for name in reference_config["sequence"]["components"]
        ]
        sequence = rvt.sequence(
            order=reference_config["sequence"]["order"],
            components=[
                components["introduction"],
                components["consent"],
                "$vlat.se.full",
                components["survey"],
            ]
        )

        # Build the study config
        study_config = rvt.studyConfig(
            schema=reference_config["$schema"],
            studyMetadata=study_metadata,
            uiConfig=ui_config,
            importedLibraries=reference_config["importedLibraries"],
            components=list(components.values()),
            sequence=sequence
        )

        # Compare the generated config to the reference
        generated_json = json.loads(study_config.__str__())
        self.assertEqual(generated_json["$schema"], reference_config["$schema"])
        self.assertEqual(generated_json["studyMetadata"], reference_config["studyMetadata"])
        self.assertEqual(generated_json["uiConfig"], reference_config["uiConfig"])
        self.assertEqual(generated_json["importedLibraries"], reference_config["importedLibraries"])
        self.assertEqual(generated_json["components"], reference_config["components"])
        self.assertEqual(generated_json["sequence"], reference_config["sequence"])

if __name__ == "__main__":
    unittest.main()
