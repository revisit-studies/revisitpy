import revisit as rvt

if __name__ == "__main__":
    newResponse = rvt.response(
        id='hello',
        type='matrix-radio',
        required=False,
        prompt='Test Prompt',
        test='hello',
        answerOptions='satisfaction5',
        questionOptions=['Test1', 'Test2']
    )

    newResponse.set(id='test5')

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

    # Works
    print(comp_one.get_response('test5'))
    # Works
    # print(comp_one.edit_response('test5', required=True))
    # Works -- throws error when trying to change type
    # print(comp_one.edit_response('test5', type='shortText'))
    # Works -- throws error because options is not in matrixResponse
    # print(comp_one.edit_response('test5', questionOptions='fdfd'))
    # Works -- none items are overwritten
    print(comp_one.response_context(all={'location': 'aboveStimulus'}))
    comps = [comp_one, comp_two]
    print(comp_one)
    print(comp_two)
    print(comp_two.component_name__)

    metadata = rvt.studyMetadata(
        authors=[],
        date='',
        title='',
        version='',
        description='',
        organizations=[]
    )

    uiConfig = rvt.uiConfig(
        contactEmail='test',
        logoPath='.../fdfd',
        sidebar=True,
        withProgressBar=False
    )

    sequence = rvt.sequence(
        components=[],
        order='fixed'
    )

    studyConfig = rvt.studyConfig(
        schema="testschema",
        uiConfig=uiConfig,
        studyMetadata=metadata,
        sequence=sequence,
        components=comps,
        test='hello'
    )
    print(studyConfig)
