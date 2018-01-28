# coding=utf-8

import os
import unittest
import functools
from string import Formatter
from urllib.error import URLError
from http.client import IncompleteRead


# 在 CI 上百分百失败用下面的 skipIf，有可能失败的用 ignore_network_issue
# 使用 skip 或者 ignore 的必须在本地上跑通过
NETWORK_ISSUE = 'tests will fail due to the network issue'
skipOnCI = unittest.skipIf('CI' in os.environ, NETWORK_ISSUE)
skipOnAppVeyor = unittest.skipIf('APPVEYOR' in os.environ, NETWORK_ISSUE)
skipOnTravis = unittest.skipIf('TRAVIS' in os.environ, NETWORK_ISSUE)


class ErrorMessageFormatter(Formatter):
    def __init__(self, namespace={}):
        super().__init__()
        self.namespace = namespace

    def get_value(self, key, args, kwargs):
        if isinstance(key, str):
            try:
                return kwargs[key]
            except KeyError:
                return self.namespace[key]
        else:
            return super().get_value(key, args, kwargs)


def ignore_network_issue(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        error = ErrorMessageFormatter({
            'func_name': func.__name__,
        })
        error_message = '{func_name}: {module_name} error: {err}'
        try:
            func(*args, **kwargs)
        except URLError as err:
            print(error.format(
                error_message, module_name='urllib', err=err
            ))
        except IncompleteRead as err:
            print(error.format(
                error_message, module_name='httplib', err=err
            ))
        except Exception:
            raise
    return wrapper


if __name__ == '__main__':
    __import__('ipdb').set_trace()
