# revisit-py


## To generate models file:

```bash
datamodel-codegen --input StudyConfigSchema.json --output models.py  --custom-template-dir custom_templates --output-model-type pydantic_v2.BaseModel --additional-imports typing.TypedDict --input-file-type jsonschema --special-field-name-prefix we_are_going_to_replace_this && sed -i '' 's/we_are_going_to_replace_this_//g'  models.py
```