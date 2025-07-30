import csv
import json
from pathlib import Path
from typing import Iterator
import chevron
from pydantic import FilePath

from .prompt import Prompt


class PromptTemplate:

    def __init__(
            self,
            template_file_name: FilePath | None = None,
            template_string: str | None = None):
        if template_string is not None:
            if template_file_name is None:
                self._template_string = template_string
            else:
                raise ValueError("Both file_name and template_string were provided")
        elif template_file_name is not None:
            with open(template_file_name) as template_file:
                self._template_string = template_file.read()
        else:
            raise ValueError("Neither file_name nor template_string were provided")

    def render(
            self,
            data: dict | str = {},
            data_file_name: FilePath | None = None) -> Prompt:
        if data_file_name is not None:
            with open(data_file_name) as data_file:
                return self.render(data_file.read())

        if type(data) is str:
            return self.render(json.loads(data))
        elif type(data) is dict:
            rendered: str = chevron.render(self._template_string, data)
            return Prompt.model_validate_json(rendered)
        else:
            raise ValueError("invalid data type")

    def render_from_dicts(self, data_stream: Iterator[dict]) -> Iterator[Prompt]:
        for data in data_stream:
            yield self.render(data)

    def render_from_csv(self, file_name: FilePath, **kwargs) -> Iterator[Prompt]:
        with open(file_name, newline="") as csv_file:
            # read complete file as it closes after with
            for row in csv.DictReader(csv_file, **kwargs):
                yield self.render(row)

    def render_from_tsv(self, file_name: FilePath, **kwargs) -> Iterator[Prompt]:
        return self.render_from_csv(file_name, delimiter="\t", **kwargs)

    def render_from_ndjson(self, file_name: FilePath) -> Iterator[Prompt]:
        with open(file_name) as ndjson_file:
            for line in ndjson_file:
                trimmed_line = line.strip()
                if trimmed_line != "":
                    yield self.render(json.loads(trimmed_line))

    def render_from_file(self, file_name: FilePath, file_type: str | None = None, **kwargs) -> Iterator[Prompt]:
        if type(file_name) is str:
            return self.render_from_file(Path(file_name), file_type=file_type, **kwargs)
        if file_type == "csv" or file_name.suffix == ".csv":
            return self.render_from_csv(file_name, **kwargs)
        if file_type == "tsv" or file_name.suffix == ".tsv":
            return self.render_from_tsv(file_name, **kwargs)
        if file_type == "ndjson" or file_name.suffix == ".ndjson":
            return self.render_from_ndjson(file_name, **kwargs)
        raise ValueError(f"Unknown file type of file {file_name}")
