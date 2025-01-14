# revisit

## Installation

```sh
pip install revisit
```

or with [uv](https://github.com/astral-sh/uv):

```sh
uv add revisit
```

## Usage

The reVISit python package wraps the standard items of the reVISit configuration file with readable, easy-to-use functions. We expose a factory function for each top-level item in the reVISit configuration: `studyMetadata`, `uiConfig`, `components`, `sequence`, and `studyMetadata`. Currently, we do not expose a `baseComponents` function. Instead, base components are still well-defined components and can be passed during the creation of another component. The final configuration will not include base components but will have the expected inherited output. 

Each factory function takes in the same parameters as the reVISit configuration file. For example, the `studyMetadata` function requires the author, organizations, title, version, and description parameters. Robust error output will help you, the user, understand what is required in each function. For the sake of brevity, we do not list every possible parameter since these are already defined in the current study configuration. Instead, we will show additional required/optional parameters as well as additional methods and other exposed functions.

### Functions

#### `component(component_name__: str, base__: Optional[component], **kwargs: dict) -> Component`

**Description**:  

Instantiates a Component class with the given input parameters.

#### **Parameters**:
| Parameter | Type   | Description                     | Default Value |
|-----------|--------|---------------------------------|---------------|
| `component_name__`  | `str` | Names the component for use in the final configuration file.   | _None_     |
| `base__`  | `Optional[component]` | When a base component is passed, all properties of the base are inherited by the component. Any other specified property during input will override base properties. | _None_        |
| `**kwargs` | `dict` | The component function requires any property that the component already requires, such as "type". Refer to the configuration documentation for required properties. | _None_ |

#### **Returns**:
- `Component`: Returns an instantiation of the Component class.

#### **Raises**:
- `RevisitError`: If the required properties are not specified, and exception will be raised.

#### **Example**:
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


#### `response(**kwargs: dict) -> Response`

**Description**:  

Instantiates a Response class with the given input parameters.

#### **Parameters**:
| Parameter | Type   | Description                     | Default Value |
|-----------|--------|---------------------------------|---------------|
| `**kwargs` | `dict` | The component function requires any property that the component already requires, such as "type". Refer to the configuration documentation for required properties. | _None_ |

#### **Returns**:
- `Response`: Returns an instantiation of the Response class.

#### **Raises**:
- `RevisitError`: If the required properties are not specified, and exception will be raised.

#### **Example**:
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

### Classes 

#### `Component`

**Description**:  
A brief summary of the class's purpose and functionality.

#### **Attributes**:
| Attribute   | Type     | Description                         | Default Value |
|-------------|----------|-------------------------------------|---------------|
| `component_name__`     | `type`   | Description of attribute 1.         | `default`     |
| `base__`     | `type`   | Description of attribute 2.         | _None_        |


#### **Methods**:
##### `responses(responses: List[Response]) -> self`

**Description**:  
Sets responses for the component

**Parameters**:  
| Parameter   | Type     | Description                         | Default Value |
|-------------|----------|-------------------------------------|---------------|
| `responses`    | `List[Response]`   | Valid list of responses.         | _None_     |

**Returns**:  
- `self`: Returns self for method chaining.

**Raises**:  
- `RevisitError`: If the list is not a valid list of responses, raises and exception.

#### **Example**:
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

**Description**:
Returns the response of the component with the given ID. If the Response does not exist, returns `None`.

**Parameters**:  
| Parameter   | Type     | Description                         | Default Value |
|-------------|----------|-------------------------------------|---------------|
| `id`    | `str`   | ID of Response         | _None_     |

**Returns**:
- `Response`: The response with the given ID.

#### **Examples**:
```python
the_response = my_component.get_response(id='the_response')

if the_response is not None:
    print(the_response)
```

#### `edit_response(id: str, **kwargs: dict) -> self`

**Description**:
Edits the Response in the Component with the given ID. This is done by creating a new copy of the existing Response.

**Parameters**:  
| Parameter   | Type     | Description                         | Default Value |
|-------------|----------|-------------------------------------|---------------|
| `id`    | `str`   | ID of Response         | _None_     |

**Returns**:
- `self`: Returns self for method chaining.

#### **Examples**:
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



## Development

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


## CODE GEN

```bash
datamodel-codegen --input src/revisit/StudyConfigSchema.json --output src/revisit/models.py  --custom-template-dir custom_templates --output-model-type pydantic_v2.BaseModel --additional-imports "typing.TypedDict, warnings" --input-file-type jsonschema --special-field-name-prefix we_are_going_to_replace_this && sed -i '' 's/we_are_going_to_replace_this_//g'  src/revisit/models.py
```

## TESTS

```bash
cd revisit-py
python -m unittest tests.test_module_one
```