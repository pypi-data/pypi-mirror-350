import pytest
from unittest.mock import MagicMock, patch, mock_open
from ara_cli.tag_extractor import TagExtractor
from ara_cli.artefact_models.artefact_load import artefact_from_content

@pytest.fixture
def mock_file_system():
    return MagicMock()

@pytest.fixture
def mock_directory_navigator():
    with patch('ara_cli.template_manager.DirectoryNavigator') as MockNavigator:
        yield MockNavigator

@pytest.fixture
def mock_file_classifier():
    with patch('ara_cli.file_classifier.FileClassifier') as MockClassifier:
        instance = MockClassifier.return_value
        instance.classify_files_new.return_value = {
            'py': ['file1.py'],
            'txt': ['file2.txt'],
            'bin': []
        }
        yield instance

@pytest.fixture
def mock_artefact_from_content():
    with patch('ara_cli.tag_extractor.artefact_from_content') as mock_artefact:
        def artefact_side_effect(content):
            if "invalid" not in content:
                mock_artefact_object = MagicMock()
                mock_artefact_object.tags = ["tag1"]
                mock_artefact_object.users = ["user1"]
                mock_artefact_object.status = "status1"
                return mock_artefact_object
            else:
                raise ValueError("Invalid content")

        mock_artefact.side_effect = artefact_side_effect
        yield mock_artefact

def test_extract_tags(mock_file_system, mock_directory_navigator, mock_file_classifier, mock_artefact_from_content):
    file_content_map = {
        'file1.py': 'valid content for file1',
        'file2.txt': 'invalid content for file2'
    }

    def mock_open_file(file, mode):
        if mode == 'r':
            return mock_open(read_data=file_content_map[file]).return_value
        else:
            raise ValueError("Unsupported mode")

    with patch('builtins.open', mock_open_file):
        tag_extractor = TagExtractor(file_system=mock_file_system)

        # Test without navigating to target
        tags = tag_extractor.extract_tags(navigate_to_target=False)
        assert tags == ['status1', 'tag1', 'user_user1']

        # Test with navigating to target
        tags = tag_extractor.extract_tags(navigate_to_target=True)
        mock_directory_navigator.return_value.navigate_to_target.assert_called_once()
        assert tags == ['status1', 'tag1', 'user_user1']
