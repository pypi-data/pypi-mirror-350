import pytest
from unittest.mock import MagicMock, patch
from ara_cli.artefact_lister import ArtefactLister


@pytest.fixture
def artefact_lister():
    return ArtefactLister()


@pytest.mark.parametrize("artefact_content, artefact_path", [
    ("content1", "path1"),
    ("content2", "path2"),
    ("content3", "path3"),
])
def test_artefact_content_retrieval(artefact_content, artefact_path):
    artefact_mock = MagicMock()
    artefact_mock.content = artefact_content
    artefact_mock.file_path = artefact_path

    content = ArtefactLister.artefact_content_retrieval(artefact_mock)
    assert content == artefact_content


@pytest.mark.parametrize("artefact_content, artefact_path", [
    ("content1", "path1"),
    ("content2", "path2"),
    ("content3", "path3"),
])
def test_artefact_path_retrieval(artefact_content, artefact_path):
    artefact_mock = MagicMock()
    artefact_mock.content = artefact_content
    artefact_mock.file_path = artefact_path

    path = ArtefactLister.artefact_path_retrieval(artefact_mock)
    assert path == artefact_path


@pytest.mark.parametrize("tags, navigate_to_target", [
    (None, False),
    (["tag1", "tag2"], False),
    (["tag1"], True),
    ([], True)
])
@patch('ara_cli.artefact_lister.FileClassifier')
@patch('ara_cli.artefact_lister.DirectoryNavigator')
def test_list_files(mock_directory_navigator, mock_file_classifier, artefact_lister, tags, navigate_to_target):
    mock_navigator_instance = mock_directory_navigator.return_value
    mock_navigator_instance.navigate_to_target = MagicMock()

    mock_classifier_instance = mock_file_classifier.return_value
    mock_classifier_instance.classify_files = MagicMock(return_value={'mocked_files': []})
    mock_classifier_instance.print_classified_files = MagicMock()

    artefact_lister.list_files(tags=tags, navigate_to_target=navigate_to_target)

    if navigate_to_target:
        mock_navigator_instance.navigate_to_target.assert_called_once()
    else:
        mock_navigator_instance.navigate_to_target.assert_not_called()

    mock_classifier_instance.classify_files.assert_called_once_with(tags=tags)

    mock_classifier_instance.print_classified_files.assert_called_once_with({'mocked_files': []})


@pytest.mark.parametrize("classifier, artefact_name, classified_artefacts, expected_suggestions", [
    ("classifier1", "missing_artefact", {"classifier1": []}, []),
    ("classifier2", "artefact1", {"classifier2": [MagicMock(file_name="artefact1")]}, None)
])
@patch('ara_cli.artefact_lister.FileClassifier')
@patch('ara_cli.artefact_lister.suggest_close_name_matches')
@patch('ara_cli.artefact_lister.ArtefactReader')
def test_list_branch_no_match(mock_artefact_reader, mock_suggest, mock_file_classifier, classifier, artefact_name, classified_artefacts, expected_suggestions, artefact_lister):
    mock_classifier_instance = mock_file_classifier.return_value
    mock_classifier_instance.classify_files = MagicMock(return_value=classified_artefacts)
    mock_classifier_instance.print_classified_files = MagicMock()

    mock_artefact_reader.step_through_value_chain = MagicMock()

    artefact_lister.list_branch(classifier, artefact_name)

    if expected_suggestions is not None:
        mock_suggest.assert_called_once_with(artefact_name, [])
        mock_artefact_reader.step_through_value_chain.assert_not_called()
        mock_classifier_instance.print_classified_files.assert_not_called()
    else:
        mock_suggest.assert_not_called()
        mock_artefact_reader.step_through_value_chain.assert_called_once_with(
            artefact_name=artefact_name,
            classifier=classifier,
            artefacts_by_classifier={classifier: []}
        )
        mock_classifier_instance.print_classified_files.assert_called_once()


@pytest.mark.parametrize("classifier, artefact_name, classified_artefacts, expected_suggestions", [
    ("classifier1", "missing_artefact", {"classifier1": []}, []),
    ("classifier2", "artefact1", {"classifier2": [MagicMock(file_name="artefact1")]}, None)
])
@patch('ara_cli.artefact_lister.FileClassifier')
@patch('ara_cli.artefact_lister.suggest_close_name_matches')
@patch('ara_cli.artefact_lister.ArtefactReader')
def test_list_children_no_match(mock_artefact_reader, mock_suggest, mock_file_classifier, classifier, artefact_name, classified_artefacts, expected_suggestions, artefact_lister):
    # Mock the FileClassifier and its methods
    mock_classifier_instance = mock_file_classifier.return_value
    mock_classifier_instance.classify_files = MagicMock(return_value=classified_artefacts)
    mock_classifier_instance.print_classified_files = MagicMock()

    mock_artefact_reader.find_children = MagicMock()

    artefact_lister.list_children(classifier, artefact_name)

    if expected_suggestions is not None:
        mock_suggest.assert_called_once_with(artefact_name, [])
        mock_artefact_reader.find_children.assert_not_called()
        mock_classifier_instance.print_classified_files.assert_not_called()
    else:
        mock_suggest.assert_not_called()
        mock_artefact_reader.find_children.assert_called_once_with(
            artefact_name=artefact_name,
            classifier=classifier
        )
        mock_classifier_instance.print_classified_files.assert_called_once()

@pytest.mark.parametrize("classifier, artefact_name, child_artefacts, filtered_child_artefacts", [
    ("classifier2", "artefact1", [MagicMock(), MagicMock()], [MagicMock()]),
])
@patch('ara_cli.artefact_lister.FileClassifier')
@patch('ara_cli.artefact_lister.filter_list')
@patch('ara_cli.artefact_lister.ArtefactReader')
def test_list_children_with_children(mock_artefact_reader, mock_filter_list, mock_file_classifier, classifier, artefact_name, child_artefacts, filtered_child_artefacts, artefact_lister):
    mock_classifier_instance = mock_file_classifier.return_value
    mock_classifier_instance.classify_files = MagicMock(return_value={classifier: [MagicMock(file_name=artefact_name)]})
    mock_classifier_instance.print_classified_files = MagicMock()

    mock_artefact_reader.find_children = MagicMock(return_value=child_artefacts)

    mock_filter_list.return_value = filtered_child_artefacts

    artefact_lister.list_children(classifier, artefact_name)

    mock_artefact_reader.find_children.assert_called_once_with(
        artefact_name=artefact_name,
        classifier=classifier
    )

    mock_filter_list.assert_called_once_with(
        list_to_filter=child_artefacts,
        list_filter=None,
        content_retrieval_strategy=ArtefactLister.artefact_content_retrieval,
        file_path_retrieval=ArtefactLister.artefact_path_retrieval,
        tag_retrieval=ArtefactLister.artefact_tags_retrieval
    )

    mock_classifier_instance.print_classified_files.assert_called_once_with(
        files_by_classifier=filtered_child_artefacts
    )


@pytest.mark.parametrize("classifier, artefact_name, classified_artefacts, expected_suggestions", [
    ("classifier1", "missing_artefact", {"classifier1": []}, True),
])
@patch('ara_cli.artefact_lister.FileClassifier')
@patch('ara_cli.artefact_lister.suggest_close_name_matches')
@patch('ara_cli.artefact_lister.ArtefactReader')
def test_list_data_no_match(mock_artefact_reader, mock_suggest, mock_file_classifier, classifier, artefact_name, classified_artefacts, expected_suggestions, artefact_lister):
    mock_classifier_instance = mock_file_classifier.return_value
    mock_classifier_instance.classify_files = MagicMock(return_value=classified_artefacts)

    artefact_lister.list_data(classifier, artefact_name)

    if expected_suggestions:
        mock_suggest.assert_called_once_with(artefact_name, [])
    else:
        mock_suggest.assert_not_called()

@pytest.mark.parametrize("classifier, artefact_name, content, file_path, file_exists", [
    ("classifier2", "artefact1", "some content", "path/to/artefact", True),
    ("classifier2", "artefact1", "some content", "path/to/artefact", False)
])
@patch('ara_cli.artefact_lister.FileClassifier')
@patch('ara_cli.artefact_lister.ArtefactReader')
@patch('ara_cli.artefact_lister.Artefact')
@patch('ara_cli.artefact_lister.os.path')
@patch('ara_cli.artefact_lister.list_files_in_directory')
def test_list_data_with_match(mock_list_files, mock_os_path, mock_artefact, mock_artefact_reader, mock_file_classifier, classifier, artefact_name, content, file_path, file_exists, artefact_lister):
    mock_classifier_instance = mock_file_classifier.return_value
    mock_classifier_instance.classify_files = MagicMock(return_value={classifier: [MagicMock(file_name=artefact_name)]})

    mock_artefact_reader.read_artefact = MagicMock(return_value=(content, file_path))

    artefact_instance = MagicMock(name=artefact_name)
    mock_artefact.from_content = MagicMock(return_value=artefact_instance)

    mock_os_path.splitext = MagicMock(return_value=(file_path, '.ext'))
    mock_os_path.exists = MagicMock(return_value=file_exists)

    artefact_lister.list_data(classifier, artefact_name)

    if file_exists:
        mock_list_files.assert_called_once_with(file_path + '.data', None)
    else:
        mock_list_files.assert_not_called()
