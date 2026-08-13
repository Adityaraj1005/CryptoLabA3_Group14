
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import secure_version

def test_require_authentication_unauthenticated():
    secure_version.AUTHENTICATED = False
    assert secure_version.require_authentication() is False

def test_authentication_state_toggle():
    secure_version.AUTHENTICATED = True
    assert secure_version.require_authentication() is True
    secure_version.AUTHENTICATED = False
