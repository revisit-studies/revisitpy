import new_revisit as rvt

if __name__ == "__main__":
    newResponse = rvt.response(
        id='hello',
        type='matrix-radio',
        required=False,
        prompt='Test Prompt',
        answerOptions='satisfaction5',
        questionOptions=['Test1', 'Test2']
    )

    # a = rvt.response(type='shortText')

    b = rvt.response(hidden=None, id='', location=None, options=[], paramCapture=None, placeholder=None, prompt='', required=False, requiredLabel=None, requiredValue=None, secondaryText=None, type='dropdown')

    c = rvt.response(id='', options=[], prompt='', required=False, type='dropdown')

    newResponse.data(id='test5')

    base_comp = rvt.component(
        type='questionnaire',
        response=[],
        component_name__='Base_Test'
    )
    

    # print(comp_one)
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
    print(comp_one.edit_response('test5', required=True))
    # Works -- throws error when trying to change type
    # print(comp_one.edit_response('test5', type='shortText'))
    # Works -- throws error because options is not in matrixResponse
    # print(comp_one.edit_response('test5', options=['12', '13']))
    # print(comp_one.response_context(required=True))
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
    # print(studyConfig)
