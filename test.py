import revisit as rvt


introduction = {
    "type": "markdown",
    "path": "ScatterJND-study/assets/introduction.md",
    "response": [
        {"type": "hello", "id": "one"}
    ]
}

introduction_two = {
    "type": "markdown",
    "path": "ScatterJND-study/assets/introduction.md",
}


component = rvt.component(
    component_name__='test',
    **introduction
)

component_two = rvt.component(
    component_name__='test_two',
    response=[rvt.response(type='test', id='test1')],
    **introduction_two
)

component_three = rvt.component(
    base__=component_two,
    component_name__='test_four',
    description='Here is a description'
)

print(component)
print(component_two)
print(component_three)
