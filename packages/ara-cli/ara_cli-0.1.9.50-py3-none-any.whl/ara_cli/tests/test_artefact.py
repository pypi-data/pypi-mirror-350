import pytest
import os
from unittest.mock import patch, MagicMock, mock_open
from ara_cli.artefact import Artefact

mock_artefact_titles = ['Document', 'Report']
mock_ordered_classifiers = ['Document', 'Report']
mock_sub_directories = {
    'Document': 'documents',
    'Report': 'reports'
}


@pytest.fixture
def mock_classifier():
    with patch('ara_cli.artefact.Classifier') as MockClassifier:
        MockClassifier.artefact_titles.return_value = mock_artefact_titles
        MockClassifier.ordered_classifiers.return_value = mock_ordered_classifiers
        MockClassifier.get_artefact_classifier.side_effect = lambda x: 'Type1' if x == 'Document' else 'Type2'
        MockClassifier.get_sub_directory.side_effect = lambda x: mock_sub_directories[x]
        yield MockClassifier


@pytest.mark.parametrize(
    "classifier, name, content, expected_content",
    [
        ('Document', 'Test Artefact', 'Document: Test Artefact\nSome content',
         'Document: Test Artefact\n\nContributes to Parent_Artefact Document\nSome content'),

        ('Document', 'Test Artefact', '@a_tag\nDocument: Test Artefact\nSome content',
         '@a_tag\nDocument: Test Artefact\n\nContributes to Parent_Artefact Document\nSome content'),

        ('example', 'Test Artefact', 'Example: Test Artefact\nSome content',
         'Example: Test Artefact\n\nIllustrates Parent_Artefact Document\nSome content'),

        ('Document', 'Test Artefact', 'Some content without title line',
         'Some content without title line'),
    ]
)
def test_create_contributes(mock_classifier, classifier, name, content, expected_content):
    artefact = Artefact(classifier=classifier, name=name, _content=content)

    with patch.object(Artefact, 'parent', new_callable=MagicMock(return_value=Artefact('Document', 'Parent_Artefact'))), \
         patch('ara_cli.artefact.Classifier.get_artefact_title', side_effect=lambda x: 'Document' if x == 'Document' else 'Example'):

        artefact.assemble_content()
        assert artefact._content == expected_content


@pytest.mark.parametrize(
    "initial_content, parent, expected_content",
    [
        ("Contributes to Child Artefact", Artefact('Type1', 'Parent_Artefact'), "Contributes to Parent_Artefact Document"),
        ("Contributes to: Child Artefact", Artefact('Type1', 'Parent_Artefact'), "Contributes to Parent_Artefact Document"),
        ("Illustrates Child Artefact", Artefact('Type1', 'Parent_Artefact'), "Illustrates Parent_Artefact Document"),
        ("Illustrates: Child Artefact", Artefact('Type1', 'Parent_Artefact'), "Illustrates Parent_Artefact Document"),
        ("Contributes to Child Artefact", None, "Contributes to Child Artefact"),
        ("Illustrates Child Artefact", None, "Illustrates Child Artefact")
    ]
)
def test_assemble_content_replace_parent(mock_classifier, initial_content, parent, expected_content):
    artefact = Artefact(classifier='Document', name='Test Artefact', _content=initial_content)

    with patch.object(Artefact, 'parent', new_callable=MagicMock(return_value=parent)), \
         patch('ara_cli.artefact.Classifier.get_artefact_title', return_value='Document'):
        artefact.assemble_content()
        assert artefact._content == expected_content


@pytest.mark.parametrize(
    "initial_content, initial_tags, expected_content",
    [
        ("Some content", {'tag1', 'tag2'}, "@tag1 @tag2\nSome content"),
        ("@oldtag\nContent", {'newtag'}, "@newtag\nContent"),
        ("Content without tags", set(), "Content without tags"),
    ]
)
def test_assemble_content_replace_tags(mock_classifier, initial_content, initial_tags, expected_content):
    artefact = Artefact(classifier='Document', name='Test Artefact', _content=initial_content)
    artefact._tags = initial_tags

    with patch.object(Artefact, 'parent', new_callable=MagicMock(return_value=None)):
        artefact.assemble_content()
        assert artefact._content == expected_content

@pytest.mark.parametrize(
    "initial_content, parent, initial_tags, expected_content",
    [
        ("Contributes to Child Artefact", Artefact('Type1', 'Parent_Artefact'), {'tag1'}, "@tag1\nContributes to Parent_Artefact Document"),
        ("@oldtag\nIllustrates Child Artefact", Artefact('Type1', 'Parent_Artefact'), {'newtag'}, "@newtag\nIllustrates Parent_Artefact Document"),
        ("Content without parent", None, {'tag1', 'tag2'}, "@tag1 @tag2\nContent without parent"),
    ]
)
def test_assemble_content_full(mock_classifier, initial_content, parent, initial_tags, expected_content):
    artefact = Artefact(classifier='Document', name='Test Artefact', _content=initial_content)
    artefact._tags = initial_tags

    with patch.object(Artefact, 'parent', new_callable=MagicMock(return_value=parent)), \
         patch('ara_cli.artefact.Classifier.get_artefact_title', return_value='Document'):
        artefact.assemble_content()
        assert artefact._content == expected_content


@pytest.mark.parametrize(
    "content, expected_parent",
    [
        ("Contributes to: Parent Artefact Document", Artefact('Type1', 'Parent_Artefact')),
        ("Contributes to Parent Report", Artefact('Type2', 'Parent')),
        ("No parent defined here", None),
        ("", None),
    ]
)
def test_parent_property(mock_classifier, content, expected_parent):
    artefact = Artefact(classifier='Document', name='Test Artefact', _content=content)

    parent = artefact.parent

    if expected_parent is None:
        assert parent is None
    else:
        assert parent is not None
        assert parent.name == expected_parent.name
        assert parent.classifier == expected_parent.classifier


@pytest.mark.parametrize(
    "initial_parent, expected_parent",
    [
        (Artefact('Document', 'Existing Parent'), Artefact('Document', 'Existing Parent')),
    ]
)
def test_parent_property_initial_parent(mock_classifier, initial_parent, expected_parent):
    artefact = Artefact(classifier='Document', name='Test Artefact', _content="Contributes to: New Parent Document")
    artefact._parent = initial_parent  # Directly set _parent to simulate pre-existing condition

    parent = artefact.parent

    assert parent is not None
    assert parent.name == expected_parent.name
    assert parent.classifier == expected_parent.classifier


@pytest.mark.parametrize(
    "classifier, name, expected_file_path",
    [
        ('Document', 'Test Artefact', 'documents/Test_Artefact.Document'),
        ('Report', 'Another Report', 'reports/Another_Report.Report'),
        ('Document', 'Report with spaces', 'documents/Report_with_spaces.Document'),
    ]
)
def test_file_path_property(mock_classifier, classifier, name, expected_file_path):
    artefact = Artefact(classifier=classifier, name=name)
    file_path = artefact.file_path
    assert file_path == expected_file_path


@pytest.mark.parametrize(
    "content, expected_tags",
    [
        ("@tag1 @tag2 Some content here", {'tag1', 'tag2'}),
        ("@singleTag Content follows", {'singleTag'}),
        ("No tags in this content", set()),
        ("", set()),
        ("@mixedCase @AnotherTag @123numeric", {'mixedCase', 'AnotherTag', '123numeric'}),
        ("  @leadingSpaceTag  @another  ", {'leadingSpaceTag', 'another'}),
        ("Not a tag @notatag", set()),
    ]
)
def test_tags_property(mock_classifier, content, expected_tags):
    artefact = Artefact(classifier='Document', name='Test Artefact', _content=content)
    tags = artefact.tags
    assert tags == expected_tags


@pytest.mark.parametrize(
    "initial_tags, content, expected_tags",
    [
        ({'preExistingTag'}, "@tag1 @tag2", {'preExistingTag'}),
        (None, "@tag1 @tag2", {'tag1', 'tag2'}),
        ({'anotherTag'}, "", {'anotherTag'}),
        (set(), "No tags in this content", set()),
    ]
)
def test_tags_property_when_tags_pre_set(mock_classifier, initial_tags, content, expected_tags):
    artefact = Artefact(classifier='Document', name='Test Artefact', _content=content)
    artefact._tags = initial_tags  # Directly set _tags to simulate pre-existing condition

    tags = artefact.tags

    assert tags == expected_tags


def test_content_property_reads_file(mock_classifier):
    artefact = Artefact(classifier='Document', name='Test Artefact')
    mock_file_content = "This is the file content."

    # Mock the open function within the specific context
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        content = artefact.content

    assert content == mock_file_content

def test_content_property_caches_content(mock_classifier):
    artefact = Artefact(classifier='Document', name='Test Artefact')
    mock_file_content = "This is the file content."

    # Mock the open function within the specific context
    with patch("builtins.open", mock_open(read_data=mock_file_content)) as mocked_open:
        content_first_call = artefact.content
        content_second_call = artefact.content

    # Ensure the file is only read once
    mocked_open.assert_called_once_with(artefact.file_path, 'r')
    assert content_first_call == mock_file_content
    assert content_second_call == mock_file_content

def test_content_property_with_existing_content(mock_classifier):
    existing_content = "Existing content should be returned."
    artefact = Artefact(classifier='Document', name='Test Artefact', _content=existing_content)

    with patch("builtins.open", mock_open()) as mocked_open:
        content = artefact.content

    # Ensure that the file is never opened because _content is already set
    mocked_open.assert_not_called()
    assert content == existing_content


@pytest.mark.parametrize(
    "content, expected_classifier, expected_name",
    [
        ("Document: Parent Artefact", 'Type1', 'Parent Artefact'),
        ("Report: Another Report", 'Type2', 'Another Report')
    ]
)
def test_from_content_valid(mock_classifier, content, expected_classifier, expected_name):
    artefact = Artefact.from_content(content)
    assert artefact.classifier == expected_classifier
    assert artefact.name == expected_name
    assert artefact.content == content


@pytest.mark.parametrize(
    "content",
    [
        "Invalid content without proper structure",
        "Classifier: Name: Missing title",
        "",
        None,
    ]
)
def test_from_content_invalid(mock_classifier, content):
    with pytest.raises(ValueError, match="Content does not contain valid artefact information"):
        Artefact.from_content(content)


@pytest.mark.parametrize(
    "content, should_raise_error",
    [
        ("Some valid content", False),  # Content is valid, should not raise
    ]
)
def test_write_to_file_content_check(mock_classifier, content, should_raise_error):
    artefact = Artefact(classifier='Document', name='Test Artefact', _content=content)
    if should_raise_error:
        with pytest.raises(ValueError, match="Artefact object does not contain content information"):
            artefact.write_to_file()
    else:
        with patch('builtins.open', mock_open()) as mocked_file, \
             patch('os.makedirs') as mocked_makedirs, \
             patch.object(artefact, 'assemble_content') as mocked_assemble_content:
            artefact.write_to_file()
            mocked_assemble_content.assert_called_once()
            mocked_makedirs.assert_called_once_with('documents/Test_Artefact.data', exist_ok=True)
            mocked_file.assert_called_once_with('documents/Test_Artefact.Document', 'w')
            mocked_file().write.assert_called_once_with(content)


@pytest.mark.parametrize(
    "file_path",
    [
        ('documents/Test_Artefact.Document'),
        ('reports/Another_Report.Report')
    ]
)
def test_write_to_file_directory_creation(mock_classifier, file_path):
    artefact = Artefact(classifier='Document', name='Test Artefact', _content="Some content")
    artefact._file_path = file_path  # Directly set file path for testing
    with patch('os.makedirs') as mocked_makedirs, \
         patch('builtins.open', mock_open()):
        artefact.write_to_file()
        data_directory = f"{os.path.splitext(file_path)[0]}.data"
        mocked_makedirs.assert_called_once_with(data_directory, exist_ok=True)


def test_write_to_file_writes_content(mock_classifier):
    content = "Some valid content"
    artefact = Artefact(classifier='Document', name='Test Artefact', _content=content)
    with patch('builtins.open', mock_open()) as mocked_file, \
         patch('os.makedirs'), \
         patch.object(Artefact, 'assemble_content'):
        artefact.write_to_file()
        mocked_file.assert_called_once_with('documents/Test_Artefact.Document', 'w')
        mocked_file().write.assert_called_once_with(content)
