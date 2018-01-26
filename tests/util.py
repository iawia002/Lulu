# coding=utf-8

import os
import unittest
from urllib.error import URLError


NETWORK_ISSUE = 'tests will fail due to the network issue'

skipOnCI = unittest.skipIf('CI' in os.environ, NETWORK_ISSUE)
skipOnAppVeyor = unittest.skipIf('APPVEYOR' in os.environ, NETWORK_ISSUE)
skipOnTravis = unittest.skipIf('TRAVIS' in os.environ, NETWORK_ISSUE)


def skip_network_issue(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except URLError as err:
            print('urllib error {}'.format(err))
            return
        except Exception:
            raise
    return wrapper
