import src.revisit.revisit as rvt

comp = rvt.component(
    component_name__='test-comp',
    type='website',
    path='fake-path'
)

study_metadata = rvt.studyMetadata(
    authors=["Brian Bollen"],
    organizations=["Visualization Design La"],
    title='Showcasing revisit-py',
    description='',
    date='2025-01-13',
    version='1.0'
)

ui_config = rvt.uiConfig(
  contactEmail="briancbollen@gmail.com",
  logoPath="./assets/revisitLogoSquare.svg",
  sidebar=True,
  withProgressBar=False
)

sequence = rvt.sequence(order='fixed', components=[comp])


# sequence.permute(
#         factors=['comp:A', 'comp:B', 'comp:C'],
#         order='fixed',
#         numSamples='1'
#     )

# sequence.permute(
#         factors=['comp:A', 'comp:B', 'comp:C'],
#         order='fixed',
#     ).permute(
#         factors=['data:1', 'data:2'],
#         order='random'
#     )

sequence.permute(
        factors=['comp:A', 'comp:B', 'comp:C'],
        order='fixed',
    ).permute(
        factors=['data:1', 'data:2'],
        order='fixed',
        numSamples=1
    ).permute(
        factors=['task:easy', 'task:med', 'task:hard'],
        order='random'
    )
    
# sequence.permute(
#         factors=['comp:A', 'comp:B', 'comp:C'],
#         order='fixed',
#         numSamples='1'
#     ).permute(
#         factors=['data:1', 'data:2'],
#         order='fixed'
#     ).permute(
#         factors=['task:easy', 'task:med', 'task:hard'],
#         order='random'
#     ).permute(
#         factors=['lastly:X', 'lastly:Y'],
#         order='random'
#     )

# print(sequence)
study = rvt.studyConfig(
    schema='fake-schema',
    uiConfig=ui_config,
    studyMetadata=study_metadata,
    sequence=sequence
)
print(study)