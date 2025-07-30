from ara_cli.file_classifier import FileClassifier
from ara_cli.template_manager import DirectoryNavigator
from ara_cli.artefact_reader import ArtefactReader
from ara_cli.file_lister import list_files_in_directory
from ara_cli.artefact import Artefact
from ara_cli.list_filter import ListFilter, filter_list
from ara_cli.artefact_fuzzy_search import suggest_close_name_matches
import os


class ArtefactLister:
    def __init__(self, file_system=None):
        self.file_system = file_system or os

    @staticmethod
    def artefact_content_retrieval(artefact):
        return artefact.content

    @staticmethod
    def artefact_path_retrieval(artefact):
        return artefact.file_path

    @staticmethod
    def artefact_tags_retrieval(artefact):
        return artefact.tags

    def filter_artefacts(self, classified_files: list, list_filter: ListFilter):
        filtered_list = filter_list(
            list_to_filter=classified_files,
            list_filter=list_filter,
            content_retrieval_strategy=ArtefactLister.artefact_content_retrieval,
            file_path_retrieval=ArtefactLister.artefact_path_retrieval,
            tag_retrieval=ArtefactLister.artefact_tags_retrieval
        )
        return filtered_list

    def list_files(
        self,
        tags=None,
        navigate_to_target=False,
        list_filter: ListFilter | None = None
    ):
        # make sure this function is always called from the ara top level directory
        navigator = DirectoryNavigator()
        if navigate_to_target:
            navigator.navigate_to_target()

        file_classifier = FileClassifier(self.file_system)
        classified_files = file_classifier.classify_files(tags=tags)

        classified_files = self.filter_artefacts(classified_files, list_filter)

        file_classifier.print_classified_files(classified_files)

    def list_branch(
        self,
        classifier,
        artefact_name,
        list_filter: ListFilter | None = None
    ):
        file_classifier = FileClassifier(os)

        classified_artefacts = file_classifier.classify_files()
        all_artefact_names = [artefact.file_name for artefact in classified_artefacts.get(classifier, [])]
        if artefact_name not in all_artefact_names:
            suggest_close_name_matches(artefact_name, all_artefact_names)
            return

        artefacts_by_classifier = {classifier: []}
        ArtefactReader.step_through_value_chain(
            artefact_name=artefact_name,
            classifier=classifier,
            artefacts_by_classifier=artefacts_by_classifier
        )
        artefacts_by_classifier = self.filter_artefacts(artefacts_by_classifier, list_filter)

        file_classifier.print_classified_files(artefacts_by_classifier)

    def list_children(
        self,
        classifier,
        artefact_name,
        list_filter: ListFilter | None = None
    ):
        file_classifier = FileClassifier(os)

        classified_artefacts = file_classifier.classify_files()
        all_artefact_names = [artefact.file_name for artefact in classified_artefacts.get(classifier, [])]
        if artefact_name not in all_artefact_names:
            suggest_close_name_matches(artefact_name, all_artefact_names)
            return

        child_artefacts = ArtefactReader.find_children(
                artefact_name=artefact_name,
                classifier=classifier
        )
        child_artefacts = self.filter_artefacts(child_artefacts, list_filter)

        file_classifier.print_classified_files(
            files_by_classifier=child_artefacts
        )

    def list_data(
        self,
        classifier,
        artefact_name,
        list_filter: ListFilter | None = None
    ):
        file_classifier = FileClassifier(os)

        classified_artefacts = file_classifier.classify_files()
        all_artefact_names = [artefact.file_name for artefact in classified_artefacts.get(classifier, [])]
        if artefact_name not in all_artefact_names:
            suggest_close_name_matches(artefact_name, all_artefact_names)
            return

        content, file_path = ArtefactReader.read_artefact(
            classifier=classifier,
            artefact_name=artefact_name
        )

        artefact = Artefact.from_content(content)
        file_path = next((classified_artefact.file_path for classified_artefact in classified_artefacts.get(classifier, []) if classified_artefact.name == artefact.name), artefact)

        file_path = os.path.splitext(file_path)[0] + '.data'
        if os.path.exists(file_path):
            list_files_in_directory(file_path, list_filter)
