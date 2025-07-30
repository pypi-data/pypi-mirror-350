from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, Optional
from ara_cli.classifier import Classifier
import re
import os

@dataclass
class Artefact:
    classifier: Literal(Classifier.ordered_classifiers())
    name: str
    _content: str | None = None
    _parent: Artefact | None = field(init=False, default=None)
    _file_path: Optional[str] = None
    _tags: set[str] | None = None

    def assemble_content(self):
        def replace_parent(content):
            parent = self.parent
            if parent is None:
                return content
            parent_name = parent.name
            parent_classifier = parent.classifier
            parent_title = Classifier.get_artefact_title(parent_classifier)
            parent_string = f"{parent_name} {parent_title}"

            contribute_string = "Contributes to"
            illustrate_string = "Illustrates"

            regex_pattern = f'(?m)^(.*(?:{contribute_string}|{illustrate_string}))(.*)$'

            def replacement_function(match):
                return f"{match.group(1)} {parent_string}"

            def create_contributes(content):
                own_classifier_title = Classifier.get_artefact_title(self.classifier)
                own_title_line = f"{own_classifier_title}: {self.name}"
                contribution = contribute_string
                if self.classifier == 'example':
                    contribution = illustrate_string
                parent_line = f"{contribution} {parent_string}"
                lines = content.splitlines()
                for i, line in enumerate(lines):
                    if line.startswith(own_title_line):
                        lines.insert(i + 1, "")
                        lines.insert(i + 2, parent_line)
                        break
                content = '\n'.join(lines)
                return content

            if not re.search(regex_pattern, content):
                return create_contributes(content)

            return re.sub(regex_pattern, replacement_function, content, count=1)

        def replace_tags(content):
            tag_set = self.tags
            if tag_set is None or not tag_set:
                return content
            tags = ' '.join(sorted([f'@{tag}' for tag in tag_set]))

            lines = content.splitlines()
            if lines and lines[0].startswith('@'):
                lines[0] = tags
                return '\n'.join(lines)
            lines.insert(0, tags)
            return '\n'.join(lines)

        content = self.content
        content = replace_tags(content)
        content = replace_parent(content)
        self._content = content

    @property
    def file_name(self) -> str:
        basename = os.path.basename(self.file_path)
        return os.path.splitext(basename)[0]

    @property
    def content(self) -> str:
        if self._content is not None:
            return self._content
        with open(self.file_path, 'r') as file:
            self._content = file.read()
            return self._content

    @property
    def parent(self) -> Artefact | None:
        if self._parent is not None:
            return self._parent

        if self.content is None:
            with open(self.file_path, 'r') as file:
                self.content = file.read()

        artefact_titles = Classifier.artefact_titles()
        title_segment = '|'.join(artefact_titles)

        regex_pattern = rf'(?:Contributes to|Illustrates)\s*:*\s*(.*)\s+({title_segment}).*'
        regex = re.compile(regex_pattern)
        match = re.search(regex, self.content)

        if match:
            parent_name = match.group(1).strip()
            parent_name = parent_name.replace(' ', '_')
            parent_title = match.group(2).strip()
            parent_type = Classifier.get_artefact_classifier(parent_title)
            self._parent = Artefact(classifier=parent_type, name=parent_name)

        return self._parent

    @property
    def file_path(self) -> str:
        if self._file_path is None:
            sub_directory = Classifier.get_sub_directory(self.classifier)
            underscore_name = self.name.replace(' ', '_')
            self._file_path = f"{sub_directory}/{underscore_name}.{self.classifier}"
        return self._file_path

    @property
    def tags(self) -> set[str]:
        if self._tags is not None:
            return self._tags

        if self.content is None:
            return set()

        lines = self.content.splitlines()
        first_line = lines[0].strip() if lines else ""

        if not first_line.startswith('@'):
            self._tags = set()
            return self._tags

        self._tags = {tag[1:] for tag in first_line.split() if tag.startswith('@')}
        return self._tags

    @classmethod
    def from_content(cls, content: str, file_path: str | None = None) -> Artefact:
        """
        Create an Artefact object from the given content.
        """
        error_message = "Content does not contain valid artefact information"

        if content is None:
            raise ValueError(error_message)

        artefact_titles = Classifier.artefact_titles()
        title_segment = '|'.join(artefact_titles)

        regex_pattern = rf'({title_segment})\s*:*\s*(.*)\s*'
        regex = re.compile(regex_pattern)
        match = re.search(regex, content)

        if not match:
            raise ValueError(error_message)

        title = match.group(1).strip()
        classifier = Classifier.get_artefact_classifier(title)
        name = match.group(2).strip()

        return cls(classifier=classifier, name=name, _content=content, _file_path=file_path)

    def write_to_file(self):
        if self.content is None:
            raise ValueError("Artefact object does not contain content information")
        self.assemble_content()
        file_path = self.file_path
        data_directory = f"{os.path.splitext(file_path)[0]}.data"
        os.makedirs(data_directory, exist_ok=True)
        with open(self.file_path, 'w') as file:
            file.write(self.content)
