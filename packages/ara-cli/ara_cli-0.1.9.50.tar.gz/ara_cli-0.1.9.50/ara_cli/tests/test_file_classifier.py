import pytest
from unittest.mock import MagicMock, patch, mock_open, call
from ara_cli.file_classifier import FileClassifier
from ara_cli.classifier import Classifier
from ara_cli.artefact import Artefact


@pytest.fixture
def mock_file_system():
    return MagicMock()


@pytest.fixture
def mock_classifier():
    with patch.object(Classifier, 'ordered_classifiers', return_value=['py', 'txt', 'bin']):
        yield


@pytest.fixture
def mock_get_artefact_title():
    with patch.object(Classifier, 'get_artefact_title', side_effect=lambda classifier: f"{classifier.upper()} Title"):
        yield


@pytest.fixture
def mock_artefact():
    with patch.object(Artefact, 'from_content', side_effect=lambda content: Artefact(classifier='', name='', _file_path='')):
        yield


def test_file_classifier_init(mock_file_system):
    classifier = FileClassifier(mock_file_system)
    assert classifier.file_system == mock_file_system


def test_read_file_content(mock_file_system):
    classifier = FileClassifier(mock_file_system)
    test_file_path = "test_file.txt"
    test_file_content = "This is a test file."

    with patch("builtins.open", mock_open(read_data=test_file_content)) as mock_file:
        content = classifier.read_file_content(test_file_path)
        mock_file.assert_called_once_with(test_file_path, 'r', encoding='utf-8')
        assert content == test_file_content


def test_is_binary_file(mock_file_system):
    classifier = FileClassifier(mock_file_system)
    test_binary_file_path = "test_binary_file.bin"
    test_text_file_path = "test_text_file.txt"
    binary_content = b'\x00\x01\x02\x03\x04\x80\x81\x82\x83'
    text_content = "This is a text file."

    with patch("builtins.open", mock_open(read_data=binary_content)) as mock_file:
        result = classifier.is_binary_file(test_binary_file_path)
        mock_file.assert_called_once_with(test_binary_file_path, 'rb')
        assert result is True

    with patch("builtins.open", mock_open(read_data=text_content.encode('utf-8'))) as mock_file:
        result = classifier.is_binary_file(test_text_file_path)
        mock_file.assert_called_once_with(test_text_file_path, 'rb')
        assert result is False

    with patch("builtins.open", side_effect=Exception("Unexpected error")):
        result = classifier.is_binary_file(test_binary_file_path)
        assert result is False


def test_read_file_with_fallback(mock_file_system):
    classifier = FileClassifier(mock_file_system)
    test_file_path = "test_file.txt"
    utf8_content = 'This is a test file.'
    latin1_content = 'This is a test file with latin1 encoding.'

    with patch("builtins.open", mock_open(read_data=utf8_content)) as mock_file:
        content = classifier.read_file_with_fallback(test_file_path)
        mock_file.assert_called_once_with(test_file_path, 'r', encoding='utf-8')
        assert content == utf8_content

    with patch("builtins.open", mock_open(read_data=utf8_content)) as mock_file:
        mock_file.side_effect = [UnicodeDecodeError("mock", b"", 0, 1, "reason"), mock_open(read_data=latin1_content).return_value]
        content = classifier.read_file_with_fallback(test_file_path)
        assert content == latin1_content

    with patch("builtins.open", mock_open(read_data=utf8_content)) as mock_file:
        mock_file.side_effect = [UnicodeDecodeError("mock", b"", 0, 1, "reason"), UnicodeDecodeError("mock", b"", 0, 1, "reason")]
        content = classifier.read_file_with_fallback(test_file_path)
        assert content is None


def test_file_contains_tags(mock_file_system):
    classifier = FileClassifier(mock_file_system)
    test_file_path = "test_file.txt"
    file_content = "tag1 tag2 tag3"

    with patch.object(classifier, 'read_file_with_fallback', return_value=file_content):
        result = classifier.file_contains_tags(test_file_path, ['tag1', 'tag2'])
        assert result is True

        result = classifier.file_contains_tags(test_file_path, ['tag1', 'tag4'])
        assert result is False

        with patch.object(classifier, 'read_file_with_fallback', return_value=None):
            result = classifier.file_contains_tags(test_file_path, ['tag1', 'tag2'])
            assert result is False


def test_classify_file(mock_file_system, mock_classifier):
    classifier = FileClassifier(mock_file_system)
    test_file_path = "test_file.py"

    with patch.object(classifier, 'is_binary_file', return_value=False), \
         patch.object(classifier, 'file_contains_tags', return_value=True):
        result = classifier.classify_file(test_file_path, tags=['tag1'])
        assert result == 'py'

    with patch.object(classifier, 'is_binary_file', return_value=True):
        result = classifier.classify_file(test_file_path, tags=['tag1'])
        assert result is None

    with patch.object(classifier, 'file_contains_tags', return_value=False):
        result = classifier.classify_file(test_file_path, tags=['tag1'])
        assert result is None


def test_classify_files_skips_binary_files(mock_file_system, mock_classifier):
    mock_file_system.walk.return_value = [('.', [], ['file1.py', 'file2.txt', 'file3.bin'])]
    mock_file_system.path.join.side_effect = lambda root, file: f"{root}/{file}"

    classifier = FileClassifier(mock_file_system)

    with patch.object(classifier, 'is_binary_file', return_value=True):
        result = classifier.classify_files(tags=['tag1', 'tag2'])

    expected = {
        'py': [],
        'txt': [],
        'bin': []
    }
    assert result == expected


def test_classify_file_no_match(mock_file_system, mock_classifier):
    classifier = FileClassifier(mock_file_system)
    test_file_path = "test_file.unknown"

    with patch.object(classifier, 'is_binary_file', return_value=False), \
         patch.object(classifier, 'file_contains_tags', return_value=True):
        result = classifier.classify_file(test_file_path, tags=['tag1'])
        assert result is None


@pytest.mark.parametrize("walk_return_value, classify_file_side_effect, expected_result", [
    (
        [('.', [], ['file1.py', 'file2.txt', 'file3.bin'])],
        ['py', 'txt', 'bin'],
        {'py': ['./file1.py'], 'txt': ['./file2.txt'], 'bin': ['./file3.bin']}
    ),
    (
        [('.', [], [])],
        [],
        {'py': [], 'txt': [], 'bin': []}
    ),
    (
        [('.', [], ['file1.py', 'file2.unknown'])],
        ['py', None],
        {'py': ['./file1.py'], 'txt': [], 'bin': []}
    ),
    (
        [('.', [], ['file1.py', 'file2.txt', 'file3.unknown', 'file4.bin'])],
        ['py', 'txt', None, 'bin'],
        {'py': ['./file1.py'], 'txt': ['./file2.txt'], 'bin': ['./file4.bin']}
    ),
])
def test_classify_files(mock_file_system, mock_classifier, walk_return_value, classify_file_side_effect, expected_result):
    mock_file_system.walk.return_value = walk_return_value
    mock_file_system.path.join.side_effect = lambda root, file: f"{root}/{file}"

    classifier = FileClassifier(mock_file_system)

    with patch.object(classifier, 'classify_file', side_effect=classify_file_side_effect):
        result = classifier.classify_files_new()

    assert result == expected_result


@pytest.mark.parametrize("files_by_classifier, expected_output", [
    (
        {'py': [MagicMock(file_path='file1.py')], 'txt': [], 'bin': []},
        "PY Title files:\n  - file1.py\n\n"
    ),
    (
        {'py': [], 'txt': [MagicMock(file_path='file2.txt')], 'bin': []},
        "TXT Title files:\n  - file2.txt\n\n"
    ),
    (
        {'py': [], 'txt': [], 'bin': [MagicMock(file_path='file3.bin')]},
        "BIN Title files:\n  - file3.bin\n\n"
    ),
    (
        {'py': [MagicMock(file_path='file1.py')], 'txt': [MagicMock(file_path='file2.txt')], 'bin': []},
        "PY Title files:\n  - file1.py\n\nTXT Title files:\n  - file2.txt\n\n"
    ),
])
def test_print_classified_files(mock_file_system, mock_classifier, mock_get_artefact_title, files_by_classifier, expected_output, capsys):
    classifier = FileClassifier(mock_file_system)

    classifier.print_classified_files(files_by_classifier)

    captured = capsys.readouterr()
    assert captured.out == expected_output
