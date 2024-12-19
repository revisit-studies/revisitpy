import models
import new_revisit as rvt
import json
if __name__ == "__main__":
    comp = models.QuestionnaireComponent(
        type='questionnaire',
        response=[
            models.Response(
                id='hello',
                type='matrix-radio',
                required=False,
                prompt='Test Prompt',
                answerOptions='satisfaction5',
                questionOptions=['Test1', 'Test2']
            )
        ]
    )
    newResponse = rvt.response(
        id='hello',
        type='matrix-radio',
        required=False,
        prompt='Test Prompt',
        answerOptions='satisfaction5',
        questionOptions=['Test1', 'Test2']
    )
    print(newResponse)
    newResponse.data(id='test5')
    comp_one = rvt.component(
        type='questionnaire',
        response=[],
        component_name__='Base_Test'
    )
    print(comp_one)
    comp = rvt.component(
        base__=comp_one,
        component_name__='Test'
    ).responses([
        newResponse
    ])

    print(comp)
    # print(comp.get_response(id='hello'))

    # newResponse = rvt.Response(
    #     id='hello',
    #     type='matrix-radio',
    #     required=False,
    #     prompt='Test Prompt',
    #     answerOptions='satisfaction5',
    #     questionOptions=['Test1', 'Test2']
    # )
    # print(json.dumps(json.loads(newResponse.model_dump_json()), indent=4))
