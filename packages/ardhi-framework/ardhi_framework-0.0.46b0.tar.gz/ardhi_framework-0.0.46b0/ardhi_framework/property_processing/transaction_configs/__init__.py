from .base import *

"""
Import these configs and redefine those not required,
then call the class ValidateTransactabeParcel
"""


# import and update as per request module
def get_config(process: str = None):
    if process:
        file = 'c_' + process
        assert hasattr(file, 'CONFIGURATIONS'), 'Process not fully implemented. Must have a configuration file for validation'
        return DEFAULT.copy().update(file.CONFIGURATIONS.copy())

    return DEFAULT.copy()
