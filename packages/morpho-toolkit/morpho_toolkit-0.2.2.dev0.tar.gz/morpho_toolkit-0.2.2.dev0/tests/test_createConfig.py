import pytest
import os
from unittest import mock
from MORPHO.createConfig import createConfigFolder

@pytest.fixture
def mockOSMkdir():
    with mock.patch("os.makedirs") as mockMkdir:
        yield mockMkdir

@pytest.fixture
def mockOSPathExists():
    with mock.patch("os.path.exists") as mockExists:
        yield mockExists

@pytest.fixture
def mockOpen():
    with mock.patch("builtins.open", mock.mock_open()) as mockFile:
        yield mockFile

def testCreateConfigFolderNew(mockOSPathExists, mockOSMkdir, mockOpen):
    mockOSPathExists.side_effect = lambda x: x == 'config' or x == '.gitignore'
    createConfigFolder()

    mockOSMkdir.assert_called_once_with('config')
    mockOpen.assert_any_call('.gitignore', 'w')
    mockOpen.assert_any_call('.gitignore', 'a')
    mockOpen.return_value.write.assert_called_with('\n/config/\n')

    mockOSMkdir.assert_called_once()
    mockOpen.assert_not_called()

def testCreateConfigFolderExists(mockOSPathExists, mockOSMkdir, mockOpen):
    mockOSPathExists.side_effect = lambda x: x == 'config' or x == '.gitignore'
    createConfigFolder()

    mockOSMkdir.assert_not_called()
    mockOpen.assert_not_called()

def testAddConfigToGitignore(mockOSPathExists, mockOSMkdir, mockOpen):
    mockOSPathExists.side_effect = lambda x: x == 'config' or x == '.gitignore'
    mockOpen.return_value.readlines.return_value = ['.env\n', '# Some other files\n']
    createConfigFolder()

    mockOpen.return_value.write.assert_any_call('\n/config/\n')

def testConfigAlreadyInGitignore(mockOSPathExists, mockOSMkdir, mockOpen):
    mockOSPathExists.side_effect = lambda x: x == 'config' or x == '.gitignore'
    mockOpen.return_value.readlines.return_value = ['.env\n', '/config/\n']
    createConfigFolder()

    mockOpen.return_value.write.assert_not_called()