from __future__ import absolute_import, unicode_literals
import os

EXEC_PROFILE = os.environ.get('EXEC_PROFILE','dev')
print('EXEC PROFILE : %s ====================================='%EXEC_PROFILE)
#si on est en prod...
if EXEC_PROFILE == 'prod' :
    from korrigan_manager.prod_settings import *
elif EXEC_PROFILE == 'dev' :
    from korrigan_manager.dev_settings import *
elif EXEC_PROFILE == 'test' :
    from korrigan_manager.test_settings import *
