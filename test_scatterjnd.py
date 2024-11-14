import revisit as rvt
import data.scatterjnd.metadata as metadata


if __name__ == '__main__':
    study_metadata = rvt.studyMetadata(**metadata.study_metadata)
    ui_config = rvt.uiConfig(**metadata.ui_config)

    study_data = rvt.data('data/scatterjnd/data.csv')

    # Response context can be omitted here since there is only one response total.
    # Using here for example sake -- common to set all to required and all have same location.
    # Alternatively can set response context to also have 'iframe' key to specify all responses have other properties
    # (i.e. can specify that all iframe responses have the same prompt and hidden value)

    jnd_study = rvt.study(
        studyMetadata=study_metadata,
        uiConfig=ui_config
    ).response_context(
        all={
            'required': True,
            'location': 'aboveStimulus'
        }
    )

    introduction = rvt.component(
        __name__='introduction',
        **metadata.introduction
    )
    training = rvt.component(
        __name__='training',
        **metadata.training
    )
    practice = rvt.component(
        __name__='practice',
        **metadata.practice
    )
    begin = rvt.component(
        __name__='begin',
        **metadata.practice
    )

    base_component = rvt.component(
        __name__='base-component-1',
        type='react-component',
        path='emma-jnd/vistaJND/src/components/vis/JNDScatterRevised.tsx'
    ).responses([
        rvt.response(
            id='scatterSelections',
            prompt='Select an option',
            type='iframe',
            hidden=True
        )
    ])

    inner_sequence = rvt.sequence(
        order='random'
    ).from_data(study_data).component(
        base=base_component,
        __name__='datum:id',
        parameters={
            'r1': 'datum:r1',
            'r2': 'datum:r2',
            'above': 'datum:position'
        }
    )

    sequence = rvt.sequence(
        order='fixed',
        components=[
            introduction,
            training,
            practice,
            begin,
            inner_sequence
        ]
    )

    jnd_study.sequence = sequence

    jnd_study.save('data/scatterjnd/config.json')
