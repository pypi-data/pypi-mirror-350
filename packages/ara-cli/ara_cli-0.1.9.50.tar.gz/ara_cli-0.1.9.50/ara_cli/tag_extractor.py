import os
from ara_cli.artefact_models.artefact_load import artefact_from_content


class TagExtractor:
    def __init__(self, file_system=None):
        self.file_system = file_system or os

    def extract_tags(self, navigate_to_target=False):
        from ara_cli.template_manager import DirectoryNavigator
        from ara_cli.file_classifier import FileClassifier

        navigator = DirectoryNavigator()
        if navigate_to_target:
            navigator.navigate_to_target()

        file_classifier = FileClassifier(self.file_system)
        classified_files = file_classifier.classify_files_new()

        unique_tags = set()

        for artefacts in classified_files.values():
            for artefact in artefacts:
                with open(artefact, 'r') as file:
                    artefact_content = file.read()
                try:
                    artefact_object = artefact_from_content(artefact_content)
                except ValueError:
                    continue
                if not artefact_object:
                    continue
                status_list = ([artefact_object.status] if artefact_object.status is not None else [])
                users_list = [f"user_{user}" for user in artefact_object.users]
                tags = artefact_object.tags + users_list + status_list
                unique_tags.update(tags)

        sorted_tags = sorted(unique_tags)
        return sorted_tags
