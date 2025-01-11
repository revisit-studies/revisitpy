import src.revisit as rvt

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
        type='markdown',
        path='./assets/test-path',
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

    comp_three = rvt.component(
        component_name__='TestThree',
        response=[],
        type='react-component',
        path='../assets/fake-path'
    )

    comps = [comp_one, comp_two, comp_three]

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

    rvt.widget(studyConfig, '/Users/bbollen23/study')
