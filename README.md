# revisit

## Installation

```sh
pip install revisit
```

or with [uv](https://github.com/astral-sh/uv):

```sh
uv add revisit
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
datamodel-codegen --input StudyConfigSchema.json --output models.py  --custom-template-dir custom_templates --output-model-type pydantic_v2.BaseModel --additional-imports typing.TypedDict --input-file-type jsonschema --special-field-name-prefix we_are_going_to_replace_this && sed -i '' 's/we_are_going_to_replace_this_//g'  src/revisit/models.py
```

## TESTS

```bash
cd revisit-py
python -m unittest tests.test_module_one
```