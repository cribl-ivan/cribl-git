import pytest
import pathlib
from tests.YamlFile import YamlFile
    
@pytest.hookimpl()
def pytest_collect_file(parent, file_path : pathlib.PosixPath):
    if (file_path.suffix == ".yml" and 'pipelines' in file_path.parts and 'local' in file_path.parts):
        return YamlFile.from_parent(parent, path=file_path)
