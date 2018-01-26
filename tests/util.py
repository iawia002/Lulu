# coding=utf-8

import os
import unittest


NETWORK_ISSUE = 'tests will fail due to the network issue'

skipOnCI = unittest.skipIf('CI' in os.environ, NETWORK_ISSUE)
skipOnAppVeyor = unittest.skipIf('APPVEYOR' in os.environ, NETWORK_ISSUE)
