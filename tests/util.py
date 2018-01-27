# coding=utf-8

import os
import unittest
from urllib.error import URLError


# 在 CI 上百分百失败用下面的 skipIf，有可能失败的用 ignore_network_issue
# 使用 skip 或者 ignore 的必须在本地上跑通过
NETWORK_ISSUE = 'tests will fail due to the network issue'
skipOnCI = unittest.skipIf('CI' in os.environ, NETWORK_ISSUE)
skipOnAppVeyor = unittest.skipIf('APPVEYOR' in os.environ, NETWORK_ISSUE)
skipOnTravis = unittest.skipIf('TRAVIS' in os.environ, NETWORK_ISSUE)


def ignore_network_issue(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except URLError as err:
            print('{}: urllib error: {}'.format(func.__name__, err))
            return
        except Exception:
            raise
    return wrapper
