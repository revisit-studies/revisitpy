# ReVISitPy

# Installation

```sh
pip install revisitpy
```

or with [uv](https://github.com/astral-sh/uv):

```sh
uv add revisitpy
```

# Usage

The reVISit python package wraps the standard items of the reVISit configuration file with readable, easy-to-use functions. We expose a factory function for each top-level item in the reVISit configuration: `studyMetadata`, `uiConfig`, `components`, and `sequence`. Currently, we do not expose a `baseComponents` function. Instead, base components are still well-defined components and can be passed during the creation of another component. The final configuration will not include base components but will have the expected inherited output. 

Each factory function takes in the same parameters as the reVISit configuration file. For example, the `studyMetadata` function requires the author, organizations, title, version, and description parameters. Robust error output will help you, the user, understand what is required in each function. For the sake of brevity, we do not list every possible parameter since these are already defined in the current study configuration. Instead, we will show additional required/optional parameters as well as additional methods and other exposed functions.

The individual classes (`Component`, `Response`, `Sequence`, `StudyMetadata`, `UIConfig`, and `StudyConfig`) should not be created directly. Instead, you should use the corresponding factory functions to insantiate them (`component()`, `response()`, `sequence()`, `studyMetadata()`, `uiConfig()`, and `studyConfig()`).

# Functions

### `component(component_name__, base__, **kwargs) -> Component`

Instantiates a Component class with the given input parameters.

### **Parameters**:
| Parameter | Type   | Description                     | Default Value |
|-----------|--------|---------------------------------|---------------|
| `component_name__`  | `str` | Names the component for use in the final configuration file.   | _None_     |
| `base__`  | `Optional[component]` | When a base component is passed, all properties of the base are inherited by the component. Any other specified property during input will override base properties. | _None_        |
| `**kwargs` | `dict` | The component function requires any property that the component already requires, such as "type". Refer to the configuration documentation for required properties. | _None_ |

### **Returns**:
- `Component`: Returns an instantiation of the Component class.

### **Raises**:
- `RevisitError`: If the required properties are not specified, and exception will be raised.

### **Example**:
```python
import revisit as rvt

# Initializing a markdown component with an empty response list.
my_component = rvt.component(
    component_name__='my-component',
    response=[],
    type='markdown',
    path='./assets/my-markdown-file.md'
)

# Instantiating a component with the base as "my_component".
my_other_component = rvt.component(
    component_name__='my-other-component',
    base__=my_component,
    path='./assets/my-other-markdown-file.md'
)
```


### `response(**kwargs) -> Response`


Instantiates a Response class with the given input parameters.

### **Parameters**:
| Parameter | Type   | Description                     | Default Value |
|-----------|--------|---------------------------------|---------------|
| `**kwargs` | `dict` | The component function requires any property that the component already requires, such as "type". Refer to the configuration documentation for required properties. | _None_ |

### **Returns**:
- `Response`: Returns an instantiation of the Response class.

### **Raises**:
- `RevisitError`: If the required properties are not specified, and exception will be raised.

### **Example**:
```python
import revisit as rvt

# Initializing a matrix radio response
my_response = rvt.response(
    type='matrix-radio',
    answerOptions='likely5',
    questionOptions=['Question 1', 'Question 2', 'Question 3'],
    required=True,
    location='sidebar'
)
```

### `studyMetadata(**kwargs) -> StudyMetadata`

Instantiates a StudyMetadata class with the given parameters.

### **Parameters**:
| Parameter | Type   | Description                     | Default Value |
|-----------|--------|---------------------------------|---------------|
| `**kwargs` | `dict` | Required properties for the StudyMetadata | _None_ |

### **Returns**:
- `Response`: Returns an instantiation of the Response class.

### **Raises**:
- `RevisitError`: If the required properties are not specified, and exception will be raised.

### **Example**:
```python
import revisit as rvt

# Initializing a matrix radio response
my_response = rvt.response(
    type='matrix-radio',
    answerOptions='likely5',
    questionOptions=['Question 1', 'Question 2', 'Question 3'],
    required=True,
    location='sidebar'
)
```

### `uiConfig(**kwargs) -> UIConfig`

Instantiates a UIConfig class with the given parameters.

### **Parameters**:
| Parameter | Type   | Description                     | Default Value |
|-----------|--------|---------------------------------|---------------|
| `**kwargs` | `dict` | The component function requires any property that the component already requires, such as "type". Refer to the configuration documentation for required properties. | _None_ |

### **Returns**:
- `Response`: Returns an instantiation of the Response class.

### **Raises**:
- `RevisitError`: If the required properties are not specified, and exception will be raised.

### **Example**:
```python
import revisit as rvt

# Initializing a matrix radio response
my_response = rvt.response(
    type='matrix-radio',
    answerOptions='likely5',
    questionOptions=['Question 1', 'Question 2', 'Question 3'],
    required=True,
    location='sidebar'
)
```

### `studyConfig(studyMetadata, uiConfig, sequence, schema, components) -> StudyConfig`

Instantiates a the final `StudyConfig` based on the `UIConfig`, `StudyMetadata`, `Sequence`, and `Components` input. Note that the components list is completely optional: using the `studyConfig` factory function automatically populates all components based on their presence in the sequence.

### **Parameters**:
| Parameter | Type   | Description                     | Default Value |
|-----------|--------|---------------------------------|---------------|
| `studyMetadata` | `StudyMetadata` | An instance of the `StudyMetadata` class | _None_ |
| `uiConfig` | `UIConfig` | An instance of the `UIConfig` class | _None_ |
| `sequence` | `ComponentBlock` | The top level member of your sequence. | _None_ |
| `components` | `Optional[List[Component]]` | The list of `Component`s to be added to the config. This is automatically populated based on the inputted sequence | `[]` |
| `schema` | `str` |The valid `$schema` value for the config. You can always find the most recent schema value in the public repository of our main study repository, such as [here](https://github.com/revisit-studies/study/blob/main/public/demo-html/config.json) | _None_ |

### **Returns**:
- `StudyConfig`: Returns an instantiation of the StudyConfig class.

### **Raises**:
- `RevisitError`: If the required properties are not specified, and exception will be raised.

### **Example**:

```python
ui_config = rvt.uiConfig(...)
study_metadata = rvt.studyMetadata(...)
comp_one = rvt.component(...)
comp_two = rvt.component(...)
sequence = rvt.sequence(order='fixed',components=[comp_one, comp_two])

study = rvt.studyConfig(
    schema='https://raw.githubusercontent.com/revisit-studies/study/v2.0.0-rc5/src/parser/StudyConfigSchema.json',
    studyMetadata=study_metadata,
    uiConfig=ui_config,
    sequence=sequence # <-- Do not need to add components list separately if they are already in the sequence.
)
```


### `data(file_path)`

Parses a CSV file with the given `file_path` and returns a list of DataRows. Output can be passed into the `from_data` method of the `sequence` class to generate components based on the CSV data.

### **Parameters**:
| Parameter | Type   | Description                     | Default Value |
|-----------|--------|---------------------------------|---------------|
| `file_path` | `str` | Path to the CSV file | _None_ |

### **Returns**:
- `List[DataRow]`: Returns a list of dataclasses called `DataRow`. 


### **Example**:

In the below example, we create the study data using the `data` method, then create a sequence from this data using the `from_data` method. Each component shown in the new sequence will have the respective data added to their `meta` attribute. From here, you can use the `component` method of the `Sequence` class to transform each component based on their respective `meta` attributes that you applied with `from_data` method.

```python

'''
'my_csv_file.csv' contents

id | value_1 | value_2
---|---------|--------
 1 | 0.3     | 3
 2 | 0.1     | 4
 3 | 1.2     | 1
'''

study_data = rvt.data('path/to/my_csv_file.csv')

sequence = rvt.sequence(order='fixed').from_data(study_data)

print(sequence)
'''
{
    "order": "fixed",
    "components": [
        'id:1__value_1:0.3__value_2:3',
        'id:2__value_1:0.1__value_2:4',
        'id:3__value_1:1.2__value_2:1',
    ]
}
'''
```

# Classes 

## `Component`

The class that is instantiated when calling the `component` factory function. Used to define the components in the study configuration file.

### **Attributes**:
| Attribute   | Type     | Description                         | Default Value |
|-------------|----------|-------------------------------------|---------------|
| `component_name__`     | `str`   | Name of the component to be used as the key in the study config.        | _None_     |
| `base__`     | `Optional[Component]`   | The base component which is inherited by this component.         | _None_        |
| `meta` | `Optional[dict]` | A dictionary specifying metadata of the object. These attributes _are_ a part of the underlying component and will be shown when printing the components or the final configuration. These are used to attach arbitrary attributes to the component as well as for use with the `Sequence` class's `component` function. This attribute can also be set through the `Sequence` class's `permute` and `from_data` methods. | _None_ |

### **Methods**:

#### `responses(responses: List[Response]) -> self`

Sets responses for the component

**Parameters**:  
| Parameter   | Type     | Description                         | Default Value |
|-------------|----------|-------------------------------------|---------------|
| `responses`    | `List[Response]`   | Valid list of responses.         | _None_     |

**Returns**:  
- `self`: Returns self for method chaining.

**Raises**:  
- `RevisitError`: If the list is not a valid list of responses, raises an exception.

**Example**:
```python
my_response=rvt.response(
    id='my_response',
    type='dropdown',
    options=['Option 1', 'Option 2']
)

my_component = rvt.component(
    component_name__='my_component',
    type='markdown',
    path='assets/my-markdown-file.md'
).responses([
    my_response
])
```

#### `get_response(id: str) -> Response | None`


Returns the response of the component with the given ID. If the Response does not exist, returns `None`.

**Parameters**:  
| Parameter   | Type     | Description                         | Default Value |
|-------------|----------|-------------------------------------|---------------|
| `id`    | `str`   | ID of Response         | _None_     |

**Returns**:
- `Response`: The response with the given ID.

**Example**:
```python
the_response = my_component.get_response(id='the_response')

if the_response is not None:
    print(the_response)
```

#### `edit_response(id: str, **kwargs: dict) -> self`

Edits the Response in the Component with the given ID. This is done by creating a new copy of the existing Response.

**Parameters**:  
| Parameter   | Type     | Description                         | Default Value |
|-------------|----------|-------------------------------------|---------------|
| `id`    | `str`   | ID of Response         | _None_     |

**Returns**:
- `self`: Returns self for method chaining.

**Example**:
```python
test_response = rvt.response(
    id='test_response',
    type='shortText',
    prompt='Original Prompt:',
    required=True
)

component_one = rvt.component(
    component_name__='component_one',
    type='questionnaire',
    response=[test_response]
)

component_two = rvt.component(
    component_name__='component_two',
    type='questionnaire',
    response=[test_response]
).edit_response(id='test_response', prompt='New Prompt', required=False)

print(component_one)
'''
Expected Output:
{
    "response": [
        {
            "id": "test_response",
            "prompt": "Original Prompt:",
            "required": true,
            "type": "shortText"
        }
    ],
    "type": "questionnaire"
}
'''
print(component_two)
'''
{
    "response": [
        {
            "id": "test_response",
            "prompt": "New Prompt",
            "required": false,
            "type": "shortText"
        }
    ],
    "type": "questionnaire"
}
'''
```

#### `get(param) -> Any`

Retrieves the given parameter from the component. The param `'name'` can be used as shorthand for `'component_name__'`.

**Parameters**:  
| Parameter   | Type     | Description                         | Default Value |
|-------------|----------|-------------------------------------|---------------|
| `param`    | `str`   | Parameter name to be retrieved      | _None_     |


#### `clone(component_name__) -> Component`


Clones the component with the given new component name.

**Parameters**:  
| Parameter   | Type     | Description                         | Default Value |
|-------------|----------|-------------------------------------|---------------|
| `component_name__`    | `str`   | New component name to assign to cloned component.        | _None_     |


**Returns**:
- `self`: Returns self for method chaining.

**Example**:
```python
test_response = rvt.response(
    id='test_response',
    type='shortText',
    prompt='Original Prompt:',
    required=True
)

component_one = rvt.component(
    component_name__='component_one',
    type='questionnaire',
    response=[test_response]
)

component_two = component_one.clone(component_name__='component_two').edit_response(id='test_response', prompt='New Prompt', required=False)

print(component_one)
'''
Expected Output:
{
    "response": [
        {
            "id": "test_response",
            "prompt": "Original Prompt:",
            "required": true,
            "type": "shortText"
        }
    ],
    "type": "questionnaire"
}
'''
print(component_two)
'''
{
    "response": [
        {
            "id": "test_response",
            "prompt": "New Prompt",
            "required": false,
            "type": "shortText"
        }
    ],
    "type": "questionnaire"
}
'''
```

## `Response`

This is the `Responsse` class. When calling the `response` factory function, an instantiation of this class is returned.

### **Attributes**:
_No attributes_


### **Methods**:

#### `get(param) -> Any`

Retrieves the given parameter from the response. The param `'name'` can be used as an alternative for `'id'`.

**Parameters**:  
| Parameter   | Type     | Description                         | Default Value |
|-------------|----------|-------------------------------------|---------------|
| `param`    | `str`   | Parameter name to be retrieved      | _None_     |


#### `set(**kwargs: dict) -> self`



Sets the values of the response to the input dictionary. The `type` cannot be changed and would require creating a new response

**Parameters**:  
| Parameter   | Type     | Description                         | Default Value |
|-------------|----------|-------------------------------------|---------------|
| `**kwargs`    | `dict`   | Dictionary containing valid values for the current response type.        | _None_     |

**Returns**:
- `self`: Returns self for method chaining.

**Raises**:
- `RevisitError`: If the user attempts to change the `type` attribute of the response, an exception will be raised. Any invalid inputs for the instantiated response type will also raise an exception.

**Examples**:
```python
response_one = rvt.response(
    id='r-1',
    type='shortText',
    required=False,
    location='belowStimulus',
    prompt=''
)

response_one.set(prompt='New Prompt')
print(response_one)
'''
Expected Output
{
    "id": "r-1",
    "location": "belowStimulus",
    "prompt": "New Prompt",
    "required": false,
    "type": "shortText"
}
'''

response_one.set(type='longText')
# Raises Exception: 'Cannot change type from shortText to longText'

response_one.set(options=[1,2,3])

```

#### `clone() -> Response`


Clones the response.

**Parameters**:  
_No parameters_

**Returns**:
- `self`: Returns self for method chaining.

**Examples**:
```python
import random
question_1 = rvt.response(
    id='q-1',
    type='shortText',
    prompt='What is 4 - 2?',
    required=True,
    location='belowStimulus'
)

# Initialize a list with first question
final_responses = [question_1]

# Randomly generate different arithmetic questions by cloning original question.
for i in range(2, 21):
    curr_response = question_1.clone().set(
        id=f'q-{i}',
        prompt=f'What is {random.randint(1, 10)} - {random.randint(1, 10)}'
    )
    final_responses.append(curr_response)

component_one = rvt.component(
    component_name__='component_one',
    type='questionnaire',
    response=final_responses
)

print(component_one)
'''
Expected Output:
{
    "response": [
        {
            "id": "q-1",
            "location": "belowStimulus",
            "prompt": "What is 4 - 2?",
            "required": true,
            "type": "shortText"
        },
        {
            "id": "q-2",
            "location": "belowStimulus",
            "prompt": "What is 10 - 4",
            "required": true,
            "type": "shortText"
        },

        ...

        {
            "id": "q-20",
            "location": "belowStimulus",
            "prompt": "What is 2 - 5",
            "required": true,
            "type": "shortText"
        }
    ],
    "type": "questionnaire"
}
'''
```


## `ComponentBlock`

  
The `ComponentBlock` class (also referred to as a "Sequence"). A well-defined sequence simply contains an order and a set of components, with other optional properties. Just as in the nested structure of component blocks in the reVISit study configuration, `ComponentBlock` classes can be added together.

A `ComponentBlock` automatically tracks all of its existing `Component` classes. When the `ComponentBlock` is added to the study configuration, all components will automatically be added to the high-level components element of the study config.

### **Attributes**:
_No attributes_


### **Methods**:

#### `__add__(other: Union[ComponentBlock, Component]) -> self:`



Adds two `ComponentBlock` or `Component` to the input sequence. When adding two sequences together, the right sequence gets added as a `ComponentBlock` to the list of components of the left sequence. When the right object is an instance of the `Component` class, the component is added to the `ComponentBlock`'s list of components.


**Parameters**:  
| Parameter   | Type     | Description                         | Default Value |
|-------------|----------|-------------------------------------|---------------|
| `other`   | `Union[ComponentBlock, Component]`   | Other item adding to left sequence.        | _None_     |

**Returns**:
- `self`: Returns self for method chaining.

**Raises**:
- `NotImplemented`: If the right item is not a `Component` or `ComponentBlock`, raises a `NotImplemented` exception.

**Examples**:
```python
first_sequence = rvt.sequence(
    order='fixed',
    components=[introduction]
)
second_sequence = rvt.sequence(
    order='random',
    components=[comp_one, comp_two]
)

first_sequence = first_sequence + second_sequence

print(first_sequence)
'''
Expected Output:
{
    "order": "fixed",
    "components" : [
        "introduction",
        {
            "order": "random"
            "components" : [
                "comp_one",
                "comp_two"
            ]
        }
    ]
}
'''
post_study = rvt.component(
    component_name__='post-study',
    type='markdown',
    path='./post-study.md'
)

first_sequence = first_sequence + post_study
print(first_sequence)
'''
Expected Output:
{
    "order": "fixed",
    "components" : [
        "introduction",
        {
            "order": "random"
            "components" : [
                "comp_one",
                "comp_two"
            ]
        },
        "post-study"
    ]
}
'''
```

#### `get_component(name: str) -> Component:`



Fetches the `Component` with the given component name from the sequence.


**Parameters**:  
| Parameter   | Type     | Description                         | Default Value |
|-------------|----------|-------------------------------------|---------------|
| `name`   | `str`   | string matching the `component_name__` attribute of the desired `Component`.       | _None_     |

**Returns**:
- `Component`: Returns desired `Component`. If no component with specified name is found, returns `None`.


**Examples**:
```python

sequence = rvt.sequence(
    order='random',
    components=[comp_one, comp_two]
)

print(sequence.get_component(name='comp_two'))
'''
{
    "type": "markdown",
    "path": "my_markdown_file.md",
    "response": []
}
'''
```

#### `get_components() -> List[Component]`

Fetches the list of all components in the sequence.

**Parameters**:  
_None_

**Returns**:
- `List[Component]`: Returns list of all components in the sequence.


**Examples**:
```python

sequence = rvt.sequence(
    order='random',
    components=[comp_one, comp_two]
)

# Fetches first component in component list.
print(sequence.get_components()[0])
'''
{
    "type": "markdown",
    "path": "my_markdown_file.md",
    "response": []
}
'''
```


#### `component(component_function: Optional[Callable]) -> self`

Maps each component in the current sequence to the result of the inputted `component_function`. This will maintain the entire structure of the sequence and will recursively call this function to replace every component.

The `met` attribute of the components are passed in as arguments to the `component_function`. This makes it especially useful after using the `permute` or `from_data` methods since both add `meta` attributes to the components. If an exception is raised when calling the `component_function`, the original input component will be used in its stead.  Additionally, the `component_function` can also take in the `component__` parameter which is the original component that is being transformed. 

#### **Examples**:

**Simple component function to change the name**
```python

# Basic component function
def my_component_function(id, value):
    return rvt.component(
        component_name__=f"{id}_{value}"
        type='website',
        path='path/to/html',
    )


first_boring_component = rvt.component(type='questionnaire',meta={'id': 1, 'value': 2}, component_name__='bor-comp-1')
second_boring_component = rvt.component(type='questionnaire',meta={'id': 2, 'value': 7}, component_name__='bor-comp-2')

sequence = rvt.sequence(order='fixed', components=[first_boring_component, second_boring_component])

print(sequence)
'''
{
    'order':'fixed',
    'components':[
        'bor-comp-1',
        'bor-comp-2'
    ]
}
'''

sequence.component(my_component_function)

print(sequence)
'''
{
    'order':'fixed',
    'components':[
        '1_2',
        '2_7'
    ]
}
'''
```

**Passing in Original Components**

In the example below, we'll use the original component to determine if we want to append the `meta` as parameters.

```python
def my_component_function(id, value, component__):
    if component__.get('type') === 'website':
        return rvt.component(
            component_name__=f"website_{id}_{value}"
            type='website',
            path='path/to/html',
            parameters={
                'id':id,
                'value':value
            }
        )
    
    return rvt.component(
        component_name__=f'questionnaire_{id}_{value}'
        type='questionnaire',
    )

first_boring_component = rvt.component(type='questionnaire',meta={'id': 1, 'value': 2}, component_name__='bor-comp-1')
second_boring_component = rvt.component(type='website',meta={'id': 2, 'value': 7}, component_name__='bor-comp-2')

sequence = rvt.sequence(
    order='fixed',
    components=[first_boring_component, second_boring_component]
).component(my_component_function)

print(sequence)

'''
{
    'order':'fixed',
    'components':[
        'questionnaire_1_2',
        'website_2_7'
    ]
}
'''
```

:::info
If you'd like to have your `component_function` always take in all `meta` entries and the original component, you can define your component function using the `kwargs` keyword like `def my_component_function(**kwargs)`. Then, to access each entry, you can use `kwargs.get('my_metadata_key')` and `kwargs.get('component__')`.
:::

You can find more examples of using the `component` method in the [Scatter JND Example](../../revisitpy/examples/example_jnd_study) where we first construct a sequence by permuting over multiple factors, then using the `component` method to alter the components based on the `meta` that is applied during th permutation method.


#### `permute(factors: List[dict], order: 'fixed' | 'latinSquare' | 'random', numSamples: Optional[int]) -> self`


Permutes the the existing components of the sequence over the given `factors`. The permute method can be chained to complex study sequences. By default, the factors are attached as `meta` attributes to each component created.

**Parameters**:  
| Parameter   | Type     | Description                         | Default Value |
|-------------|----------|-------------------------------------|---------------|
| `factors`   | `List[dict]`   | A list of single-key dictionaries to permute over. | _None_     |
| `order` | `'fixed' \| 'latinSquare' \| 'random' ` |The order to assign to the current permuted component block. |  _None_ |
| `numSamples` | `Optional[int]` | The `numSamples` value to assign to the current permuted block. | _None_ |

**Returns**:
- `self`: Returns self for method chaining.

#### **Examples**:

**Simple Permutation**
```python

comp_one = rvt.component(component_name__='my-base', type='markdown', path='./my-markdown.md')

sequence = rvt.component(order='fixed',components=[comp_one])

sequence.permute(
    factors=[{'condition':'A'}, {'condition':'B'}],
    order='random'
)

print(sequence)
'''
Expected Output:
{
    "order": "random", <--- Since there was only one component in the original sequence, order gets overwritten.
    "components": [
        "my-base_condition:A",
        "my-base_condition:B" <--- Note that the default behavior appends the factors to the name
    ]
}

The two components generated are inherently identical, except with different meta attributes. 
These meta attributes are not outputed into the final JSON study config or seen when printing out
the individual components.
'''

sequence.permute(
    factors=[{'type':'1'}, {'type': '2'}]
    order='fixed',
    numSamples=1
)

print(sequence)
'''
Expected Output:
{
    "order": "random",
    "components": [
        {
            "order": "fixed", <--- New order gets added to inner most component blocks.
            "components": [
                "my-base_condition:A_type:1",
                "my-base_condition:A_type:2",
            ],
            "numSamples": 1
        },
        {
            "order": "fixed",
            "components": [
                "my-base_condition:B_type:1",
                "my-base_condition:B_type:2",
            ],
            "numSamples": 1
        },
    ]

}
'''
```

**Using the `component_function` in the `component` method**

```python
# Defining component function.
# Takes in kwargs to prevent conflicts with any existing metadata.
def my_comp_function(**kwargs):
    condition = kwargs.get('condition')
    type_ = kwargs.get('type')
    # If condition and type_ are both defined, return new component.
    if condition is not None and type_ is not None:
        return rvt.component(
            type='website'
            component_name__=f"{condition}__{type_}"
            parameters={
                'condition': condition,
                'type': type_
            },
            response=[
                rvt.response(
                    id=f"response_{condition}_{type_}",
                    type="longText",
                    prompt=f"How do you feel about condition {condition} and type {type_}?",
                    required=True
                )
            ]
        )

    # If not both defined, return a blank component with "BAD-COMPONENT" name.
    # Useful for debugging
    return rvt.component(type='questionnaire',component_name__="BAD-COMPONENT")

sequence = rvt.sequence(order='fixed').permute(
    factors=[{'condition':'A'}, {'condition':'B'}],
    order='random'
).permute(
    factors=[{'type':'1'}, {'type': '2'}]
    order='fixed',
    numSamples=1,
).component(component_function) # <-- Uses component method to map each component to the result of the component_function

print(sequence)
'''
Expected Output:
{
    "order": "random",
    "components": [
        {
            "order": "fixed", <--- New order gets added to inner most component blocks.
            "components": [
                "A__1",
                "A__2",
            ],
            "numSamples": 1
        },
        {
            "order": "fixed",
            "components": [
                "B__1",
                "B__2"
            ],
            "numSamples": 1
        },
    ]

}
'''
```



#### `from_data(data_list) -> self`

The `from_data` method iterates over a list of `DataRows` and appends the data to the `meta` attribute of the components in the sequence. You can generate a list of `DataRows` by using the [data function](./functions.md#datafile_path) to parse a CSV file.

### **Example**:

In the below example, we create the study data using the `data` method, then create a sequence from this data using the `from_data` method. Each component shown in the new sequence will have the respective data added to their `meta` attribute. From here, you can use the `component` method of the `Sequence` class to transform each component based on their respective `meta` attributes that you applied with the `from_data` method.

```python

'''
'my_csv_file.csv' contents

id | value_1 | value_2
---|---------|--------
 1 | 0.3     | 3
 2 | 0.1     | 4
 3 | 1.2     | 1
'''

study_data = rvt.data('path/to/my_csv_file.csv')

sequence = rvt.sequence(order='fixed').from_data(study_data)

print(sequence)
'''
{
    "order": "fixed",
    "components": [
        'id:1__value_1:0.3__value_2:3',
        'id:2__value_1:0.1__value_2:4',
        'id:3__value_1:1.2__value_2:1',
    ]
}
'''
```

# Development

## Building

You may need to install hatch locally (do not use `uv add hatch` since it will add it to project dependencies and be shipped with build).

```bash
uv pip install hatch
uv run hatch build
uv run hatch publish
```

We recommend using [uv](https://github.com/astral-sh/uv) for development.
It will automatically manage virtual environments and dependencies for you.

```sh
uv run jupyter lab example.ipynb
```

Alternatively, create and manage your own virtual environment:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
jupyter lab example.ipynb
```

The widget front-end code bundles it's JavaScript dependencies. After setting up Python,
make sure to install these dependencies locally:

```sh
yarn install
```

While developing, you can run the following in a separate terminal to automatically
rebuild JavaScript as you make changes:

```sh
yarn run dev
```

Open `example.ipynb` in JupyterLab, VS Code, or your favorite editor
to start developing. Changes made in `js/` will be reflected
in the notebook.


## Code Generation

```bash
uv pip install datamodel-code-generator
uv run datamodel-codegen --input src/revisitpy/StudyConfigSchema.json --output src/revisitpy/models.py  --custom-template-dir custom_templates --output-model-type pydantic_v2.BaseModel --additional-imports "typing.TypedDict, warnings" --input-file-type jsonschema --special-field-name-prefix we_are_going_to_replace_this && sed -i '' 's/we_are_going_to_replace_this_//g'  src/revisitpy/models.py
```

## Tests

```bash
cd revisit-py
uv run -m tests.test_module_one
```

## Publishing

Update version number in pyproject.toml

```bash
uv run hatch build
uv run hatch publish
```

If there hatch is not found, run the following:

```bash
uv pip install hatch
```
