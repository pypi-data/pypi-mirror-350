import pytest
import os
import pandas as pd
import tempfile
from MORPHO.combineCSV import combineCSVFiles
from unittest.mock import patch

def createTempCSV(fileName, data):
    df = pd.DataFrame(data)
    tempFile = tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='w')
    df.to_csv(tempFile.name, index=False)
    tempFile.close()
    return tempFile.name

def testMissingPaths():
    with pytest.raises(ValueError):
        combineCSVFiles("", "output.csv")
    with pytest.raises(ValueError):
        combineCSVFiles("input_directory", "")

def testNoCSVFiles():
    with tempfile.TemporaryDirectory() as tempDir:
        outputFile = os.path.join(tempDir, "combinedOutput.csv")
        with pytest.raises(FileNotFoundError):
            combineCSVFiles(tempDir, outputFile)

def testEmptyCSVFile():
    with tempfile.TemporaryDirectory() as tempDir:
        empty_csv = createTempCSV(os.path.join(tempDir, "empty.csv"), {'A': [], 'B': []})
        csv1 = createTempCSV(os.path.join(tempDir, "file1.csv"), {'A': [1, 2], 'B': [3, 4]})

        outputFile = os.path.join(tempDir, "combinedOutput.csv")
        
        combineCSVFiles(tempDir, outputFile)
        combinedDF = pd.read_csv(outputFile)

        assert os.path.exists(outputFile)
        assert len(combinedDF) == 2  # Only data from the second file
        assert set(combinedDF.columns) == {'A', 'B'}
        assert combinedDF['A'].tolist() == [1, 2]
        assert combinedDF['B'].tolist() == [3, 4]

@pytest.mark.parametrize("file_data, expected_rows", [
    ({'A': [1, 2], 'B': [3, 4]}, 2),
    ({'A': [], 'B': []}, 0),  # Empty file case
    ({'A': [1], 'B': [2]}, 1)  # Single row file
])
def testParametrizedCSVFiles(file_data, expected_rows):
    with tempfile.TemporaryDirectory() as tempDir:
        # Create a temporary CSV file with parametrized data
        temp_csv = createTempCSV(os.path.join(tempDir, "file.csv"), file_data)
        outputFile = os.path.join(tempDir, "combinedOutput.csv")
        
        # Run the combine function
        combineCSVFiles(tempDir, outputFile)
        
        # Verify the output file
        combinedDF = pd.read_csv(outputFile)
        assert len(combinedDF) == expected_rows

def testCombineCSVFiles():
    with tempfile.TemporaryDirectory() as tempDir:
        csv1 = createTempCSV(os.path.join(tempDir, "file1.csv"), {'A': [1, 2], 'B': [3, 4]})
        csv2 = createTempCSV(os.path.join(tempDir, "file2.csv"), {'A': [5, 6], 'B': [7, 8]})

        outputFile = os.path.join(tempDir, "combinedOutput.csv")
        
        assert os.path.exists(csv1)
        assert os.path.exists(csv2)
        
        combineCSVFiles(tempDir, outputFile)
        combinedDF = pd.read_csv(outputFile)

        assert os.path.exists(outputFile)
        assert len(combinedDF) == 4
        assert set(combinedDF.columns) == {'A', 'B'}
        assert combinedDF['A'].tolist() == [1, 2, 5, 6]
        assert combinedDF['B'].tolist() == [3, 4, 7, 8]
        assert combinedDF['A'].iloc[0] == 1
        assert combinedDF['B'].iloc[0] == 3
        
@patch("tqdm.tqdm")
def testProgressBar(mTQDM):
    mTQDM.return_value = iter([None, None, None])
    with tempfile.TemporaryDirectory() as tempDir:
        file1 = createTempCSV(os.path.join(tempDir, "file1.csv"), {'A': [1], 'B': [3]})
        file2 = createTempCSV(os.path.join(tempDir, "file2.csv"), {'A': [2], 'B': [4]})
        file3 = createTempCSV(os.path.join(tempDir, "file3.csv"), {'A': [5], 'B': [6]})

        outputFile = os.path.join(tempDir, "combinedOutput.csv")
        combineCSVFiles(tempDir, outputFile)
        mTQDM.assert_called_once_with(iter([None, None, None]), desc="Processing CSV files")
        assert os.path.exists(outputFile)
