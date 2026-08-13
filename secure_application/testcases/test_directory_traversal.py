
import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import secure_version

def test_directory_traversal_prevention():
    reports_dir = os.path.realpath(secure_version.REPORTS_DIRECTORY)
    requested_path = os.path.realpath(os.path.join(reports_dir, "../README.md"))
    
    common_path = os.path.commonpath([reports_dir, requested_path])
    assert common_path != reports_dir
