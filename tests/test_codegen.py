import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class TestCodeGeneration(unittest.TestCase):
    def test_schema_alias_and_numeric_enum_values(self):
        schema = {
            "title": "CodegenRegression",
            "type": "object",
            "properties": {
                "$schema": {"type": "string"},
                "format": {"type": "string", "enum": ["12h", "24h"]},
            },
            "required": ["$schema", "format"],
            "additionalProperties": False,
        }
        with tempfile.TemporaryDirectory() as directory:
            schema_path = Path(directory) / "schema.json"
            schema_path.write_text(json.dumps(schema))
            # Read the same pyproject configuration used by both release jobs.
            subprocess.run(
                [
                    sys.executable, "-m", "datamodel_code_generator",
                    "--input", str(schema_path),
                    "--output", str(Path(directory) / "generated.py"),
                ],
                cwd=Path(__file__).resolve().parents[1],
                check=True,
            )
            subprocess.run(
                [
                    sys.executable, "-c",
                    "from generated import CodegenRegression; "
                    "model = CodegenRegression.model_validate("
                    "{'$schema': 'schema.json', 'format': '12h'}); "
                    "assert model.schema == 'schema.json'; "
                    "assert model.model_dump(by_alias=True) == "
                    "{'$schema': 'schema.json', 'format': '12h'}; "
                    "assert CodegenRegression.model_validate("
                    "{'$schema': 'schema.json', 'format': '24h'}).format == '24h'",
                ],
                cwd=directory,
                check=True,
            )


if __name__ == "__main__":
    unittest.main()
