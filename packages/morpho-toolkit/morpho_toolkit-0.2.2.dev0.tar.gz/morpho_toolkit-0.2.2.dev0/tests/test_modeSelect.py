import pytest
from unittest import mock
import os
import json
from MORPHO.modeSelect import (
    getModeSelection,
    saveModeSelection,
    loadModeSelection,
    handleModeSelection,
    modeSelect,
    Mode,
    CONFIG_DIR,
    MODE_FILE
)

@pytest.fixture
def mockInput():
    with mock.patch('builtins.input') as mockInputFunction:
        yield mockInputFunction

@pytest.fixture
def mockPrint():
    with mock.patch('builtins.print') as mock_print:
        yield mock_print

def testGetModeSelection(mockInput):
    mockInput.return_value = '1'
    selectedMode = getModeSelection()
    assert selectedMode == Mode.TEST_MODE

def testGetModeSelectionUntilValid(mockInput):
    mockInput.side_effect = ['invalid', '2']
    selectedMode = getModeSelection()
    assert selectedMode == Mode.USER_MODE

@mock.patch("os.makedirs")
@mock.patch("json.dump")
@mock.patch("builtins.open", new_callable=mock.mock_open)

def testSaveModeSelection(mockOpen, mockJsonDump, mockMakedirs):
    mode = Mode.USER_MODE
    saveModeSelection(mode)

    mockMakedirs.assert_called_once_with(CONFIG_DIR, exist_ok=True)
    mockOpen.assert_called_once_with(MODE_FILE, 'w')
    mockJsonDump.assert_called_once_with({'mode': 'USER_MODE'}, mockOpen())

@mock.patch("builtins.open", mock.mock_open(read_data='{"mode": "USER_MODE"}'))
def testLoadModeSelectionExists():
    mode = loadModeSelection()
    assert mode == Mode.USER_MODE

@mock.patch("builtins.open", side_effect=FileNotFoundError)
def testLoadModeSelectionFileNotFound(mockOpen):
    mode = loadModeSelection()
    assert mode is None

@mock.patch("builtins.open", mock.mock_open())
@mock.patch("os.path.exists", return_value=False)

def testModeSelectionNotExists(mockExists, mockOpen):
    mode = loadModeSelection()
    assert mode == None
    mockExists.assert_called_once_with(MODE_FILE)

@mock.patch("builtins.print", return_value='1')

def testHandleModeSelectionTestMode(monkeypatch, mockPrint):
    monkeypatch.setattr('builtins.input', lambda _: '1')
    handleModeSelection(Mode.TEST_MODE)  
    monkeypatch.getattr('builtins.input').assert_called_once_with('Choose test mode:')
    mockPrint.assert_called_with("Running in TEST MODE with preset values.\n")

@mock.patch("MORPHO.modeSelect.getUserVals", return_value={"val1": 1, "val2": 2})
@mock.patch("builtins.print")
def testHandleModeSelectionUserMode(mockPrint, mockGetUserVals):
    handleModeSelection(Mode.USER_MODE)
    mockPrint.assert_any_call("Running in USER MODE with user-defined values.\n")

@mock.patch("builtins.print")
def testHandleModeSelectionMaintenanceMode(mockPrint):
    handleModeSelection(Mode.MAINTENANCE_MODE)
    mockPrint.assert_called_with("Running in MAINTENANCE MODE.")

@mock.patch("builtins.input", side_effect=['y'])  # user selects to use the saved mode
@mock.patch("MORPHO.modeSelect.loadModeSelection", return_value=Mode.USER_MODE)
@mock.patch("MORPHO.modeSelect.saveModeSelection")
@mock.patch("MORPHO.modeSelect.handleModeSelection")
@mock.patch("builtins.print")

def testModeSelectUseSavedMode(mockPrint, mockHandleModeSelection, mockSaveModeSelection, mockLoadModeSelection, mockInput):
    modeSelect()
    mockLoadModeSelection.assert_called_once()
    mockHandleModeSelection.assert_called_once_with(Mode.USER_MODE)
    mockSaveModeSelection.assert_called_once_with(Mode.USER_MODE)

@mock.patch("builtins.input", side_effect=['n', '2'])  # user selects not to use the saved mode and chooses 'USER_MODE'
@mock.patch("MORPHO.modeSelect.loadModeSelection", return_value=None)  # No saved mode
@mock.patch("MORPHO.modeSelect.getModeSelection", return_value=Mode.USER_MODE)
@mock.patch("MORPHO.modeSelect.saveModeSelection")
@mock.patch("MORPHO.modeSelect.handleModeSelection")
@mock.patch("builtins.print")

def testModeSelectNoSavedMode(mockPrint, mockHandleModeSelection, mockSaveModeSelection, mockGetModeSelection, mockLoadModeSelection, mockInput):
    modeSelect()
    mockGetModeSelection.assert_called_once()
    mockHandleModeSelection.assert_called_once_with(Mode.USER_MODE)
    mockSaveModeSelection.assert_called_once_with(Mode.USER_MODE)