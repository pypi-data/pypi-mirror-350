import pytest
import os
import re
import time
from unittest import mock
from MORPHO.uniqueID import (
    generateUUID,
    timestampID,
    randomID,
    customID,
    resetCounter,
    _loadCounter,
    _saveCounter
)

@pytest.fixture(autouse=True)
def cleanCounterFile(tmp_path, monkeypatch):
    # Ensure the counter.txt used in tests is isolated
    test_file = tmp_path / "counter.txt"
    monkeypatch.setattr("MORPHO.uniqueID.open", lambda *args, **kwargs: open(test_file, *args, **kwargs))
    monkeypatch.setattr("MORPHO.uniqueID.os.path.exists", lambda path: test_file.exists())
    return test_file

@mock.patch('MORPHO.uniqueID.open', new_callable=mock.mock_open)

def testGenUUID(mockOpen):
    uid = generateUUID()
    mockOpen.assert_called_once_with("counter.txt", "r")
    assert isinstance(uid, str)
    assert re.fullmatch(r"[0-9a-f\-]{36}", uid)

def testTimestampID():
    ts = timestampID()
    assert ts.isdigit()
    assert abs(int(ts) - int(time.time())) < 3  # Allow small time margin

@mock.patch("MORPHO.uniqueID.time.time", return_value=1712345678)
@mock.patch("MORPHO.uniqueID.random.choices", return_value=list("ABC123"))
def testRandomID(mockChoices, mockTime):
    result = randomID()
    assert result == "ID-1712345678-ABC123"

def testCustomIDIncre(cleanCounterFile):
    id1 = customID("TEST")
    id2 = customID("TEST")
    assert id1.endswith("000001")
    assert id2.endswith("000002")
    assert id1.startswith("TEST-")

def testResetCounter():
    resetCounter()
    assert _loadCounter() == 0

def testSaveAndLoadCounter():
    _saveCounter(42)
    assert _loadCounter() == 42
    assert os.path.exists("counter.txt")

def testCustomIDDefaultPre():
    val = customID()
    assert val.startswith("ID-")

def testLoadCounterInvalidData(cleanCounterFile):
    with open(cleanCounterFile, "w") as f:
        f.write("INVALID")
    assert _loadCounter() == 0