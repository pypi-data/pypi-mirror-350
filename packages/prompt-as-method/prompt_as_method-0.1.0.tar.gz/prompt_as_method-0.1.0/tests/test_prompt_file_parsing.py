import json
from pathlib import Path
import unittest

import jsonschema

from prompt_as_method import PromptTemplate

test_inputs_path = Path("tests") / "test-inputs"
examples_path = Path("tests") / "examples"
expected_outputs_path = Path("tests") / "expected-outputs"


class TestPromptFileParsing(unittest.TestCase):

    def test_minimal_no_template(self):
        file_name = "test-minimal-no-template.json"
        data = {}
        with open(expected_outputs_path / file_name) as file:
            expected = json.load(file)

        prompt_template = PromptTemplate(test_inputs_path / file_name)
        self.assertDictEqual(
            expected,
            prompt_template.render(data).model_dump(exclude_none=True)
        )

    def test_minimal_templated_content(self):
        file_name = "test-minimal-templated-content.json"
        data = {
            "thing": "apple"
        }
        with open(expected_outputs_path / file_name) as file:
            expected = json.load(file)

        prompt_template = PromptTemplate(test_inputs_path / file_name)
        self.assertDictEqual(
            expected,
            prompt_template.render(data).model_dump(exclude_none=True)
        )

    def test_minimal_templated_content_missing_variable(self):
        file_name = "test-minimal-templated-content.json"
        file_name_expected = "test-minimal-templated-content-missing-variable.json"
        data = {
            "nothing": "apple"
        }
        with open(expected_outputs_path / file_name_expected) as file:
            expected = json.load(file)

        prompt_template = PromptTemplate(test_inputs_path / file_name)
        self.assertDictEqual(
            expected,
            prompt_template.render(data).model_dump(exclude_none=True)
        )

    def test_minimal_templated_multiple(self):
        file_name = "test-minimal-templated-multiple.json"
        data = {
            "thing": "apple",
            "thing2": "pear",
        }
        with open(expected_outputs_path / file_name) as file:
            expected = json.load(file)

        prompt_template = PromptTemplate(test_inputs_path / file_name)
        self.assertDictEqual(
            expected,
            prompt_template.render(data).model_dump(exclude_none=True)
        )

    def test_full(self):
        file_name = "test-full.json"
        data = {
            "thing": "apple",
            "thing2": "pear"
        }
        with open(expected_outputs_path / file_name) as file:
            expected = json.load(file)

        prompt_template = PromptTemplate(test_inputs_path / file_name)
        self.assertDictEqual(
            expected,
            prompt_template.render(data).model_dump()
        )

    def test_full_message_template(self):
        file_name = "test-full-message-template.mustache"
        file_name_expected = "test-full-message-template.json"
        data = {
            "thing": "apple",
            "otherThings": ["pear", "banana"]
        }
        with open(expected_outputs_path / file_name_expected) as file:
            expected = json.load(file)

        prompt_template = PromptTemplate(test_inputs_path / file_name)
        self.assertDictEqual(
            expected,
            prompt_template.render(data).model_dump()
        )

    def test_full_message_template_empty(self):
        file_name = "test-full-message-template.mustache"
        file_name_expected = "test-full-message-template-empty.json"
        data = {
            "thing": "apple"
        }
        with open(expected_outputs_path / file_name_expected) as file:
            expected = json.load(file)

        prompt_template = PromptTemplate(test_inputs_path / file_name)
        self.assertDictEqual(
            expected,
            prompt_template.render(data).model_dump()
        )

    def test_example_sentiment_ndjson(self):
        file_name = "example-sentiment.json"
        file_name_data = "example-sentiment-data.ndjson"
        file_name_expected = "example-sentiment.json"
        with open(expected_outputs_path / file_name_expected) as file:
            expected = json.load(file)

        prompt_template = PromptTemplate(examples_path / file_name)
        prompts = list(prompt_template.render_from_file(examples_path / file_name_data))
        self.assertListEqual(
            expected,
            [prompt.model_dump(exclude_none=True) for prompt in prompts]
        )

    def test_example_sentiment_csv(self):
        file_name = "example-sentiment.json"
        file_name_data = "example-sentiment-data.csv"
        file_name_expected = "example-sentiment.json"
        with open(expected_outputs_path / file_name_expected) as file:
            expected = json.load(file)

        prompt_template = PromptTemplate(examples_path / file_name)
        prompts = list(prompt_template.render_from_file(examples_path / file_name_data))
        self.assertListEqual(
            expected,
            [prompt.model_dump(exclude_none=True) for prompt in prompts]
        )

    def test_example_sentiment_tsv(self):
        file_name = "example-sentiment.json"
        file_name_data = "example-sentiment-data.tsv"
        file_name_expected = "example-sentiment.json"
        with open(expected_outputs_path / file_name_expected) as file:
            expected = json.load(file)

        prompt_template = PromptTemplate(examples_path / file_name)
        prompts = list(prompt_template.render_from_file(examples_path / file_name_data))
        self.assertListEqual(
            expected,
            [prompt.model_dump(exclude_none=True) for prompt in prompts]
        )

    def test_fail_empty_messages(self):
        file_name = "test-fail-empty-messages.json"
        data = {}
        prompt_template = PromptTemplate(test_inputs_path / file_name)
        with self.assertRaises(ValueError):
            prompt_template.render(data)

    def test_fail_empty(self):
        file_name = "test-fail-empty.json"
        data = {}
        prompt_template = PromptTemplate(test_inputs_path / file_name)
        with self.assertRaises(ValueError):
            prompt_template.render(data)

    def test_fail_invalid_role(self):
        file_name = "test-fail-invalid-role.json"
        data = {}
        prompt_template = PromptTemplate(test_inputs_path / file_name)
        with self.assertRaises(ValueError):
            prompt_template.render(data)

    def test_fail_list(self):
        file_name = "test-fail-list.json"
        data = {}
        prompt_template = PromptTemplate(test_inputs_path / file_name)
        with self.assertRaises(ValueError):
            prompt_template.render(data)

    def test_fail_no_json(self):
        file_name = "test-fail-no-json.txt"
        data = {}
        prompt_template = PromptTemplate(test_inputs_path / file_name)
        with self.assertRaises(ValueError):
            prompt_template.render(data)

    def test_fail_no_messages(self):
        file_name = "test-fail-no-messages.json"
        data = {}
        prompt_template = PromptTemplate(test_inputs_path / file_name)
        with self.assertRaises(ValueError):
            prompt_template.render(data)

    def test_fail_last_message_not_of_user(self):
        file_name = "test-fail-last-message-not-of-user.json"
        data = {}
        prompt_template = PromptTemplate(test_inputs_path / file_name)
        with self.assertRaises(ValueError):
            prompt_template.render(data)

    def test_fail_no_model(self):
        file_name = "test-fail-no-model.json"
        data = {}
        prompt_template = PromptTemplate(test_inputs_path / file_name)
        with self.assertRaises(ValueError):
            prompt_template.render(data)

    def test_fail_no_role(self):
        file_name = "test-fail-no-role.json"
        data = {}
        prompt_template = PromptTemplate(test_inputs_path / file_name)
        with self.assertRaises(ValueError):
            prompt_template.render(data)

    def test_fail_only_text(self):
        file_name = "test-fail-only-text.json"
        data = {}
        prompt_template = PromptTemplate(test_inputs_path / file_name)
        with self.assertRaises(ValueError):
            prompt_template.render(data)

    def test_fail_invalid_schema(self):
        file_name = "test-fail-invalid-schema.json"
        data = {
            "thing": "apple",
            "thing2": "pear"
        }
        prompt_template = PromptTemplate(test_inputs_path / file_name)
        with self.assertRaises(jsonschema.SchemaError):
            prompt_template.render(data)


if __name__ == '__main__':
    unittest.main()
