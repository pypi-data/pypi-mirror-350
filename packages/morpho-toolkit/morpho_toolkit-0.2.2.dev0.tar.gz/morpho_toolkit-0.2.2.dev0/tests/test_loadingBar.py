import pytest
import time
import sys
from unittest.mock import patch
from io import StringIO
from MORPHO.loadingBar import LoadingBar

def testLoadingBarInit():
    duration = 5
    length = 50
    loadingBar = LoadingBar(duration, length)

    assert loadingBar.duration == duration
    assert loadingBar.length == length
    assert loadingBar.display() is None  # display() should return None

@patch("sys.stdout", new_callable=StringIO)
@patch("time.sleep", return_value=None)

def testLoadingBarDisplay(mockStdout, mockSleep):
    mockSleep.return_value = '[...]'
    duration = 5
    length = 10
    loadingBar = LoadingBar(duration, length)

    loadingBar.display()

    output = mockStdout.getvalue()
    assert "[" in output
    assert "]" in output
    assert output.count("=") == length
    assert "Loading complete!" in output
    assert mockSleep.call_count == length