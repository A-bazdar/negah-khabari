import sys
import traceback
from base_app.classes.send_error import SendError


class Debug:
    def __init__(self):
        pass

    @classmethod
    def get_exception(cls, sub_system=None, severity=None, tags=None, data=None, send=True, return_error=False):

        exc_type, message, exc_tb = sys.exc_info()
        file_name, line_num, function, code = traceback.extract_tb(exc_tb)[-1]

        file_address = file_name
        file_name = file_name.split('/')[-1]
        # if send:
        #     SendError(sub_system=sub_system, severity=severity, tags=tags, file_name=file_name, file_address=file_address,
        #               function=function, line_num=line_num, code=code, message=message, data=data)

        print 'EXCEPTION IN ({}, LINE {} \'{}\'): {}'.format(file_name, line_num, code, message)
        if return_error:
            return 'EXCEPTION IN ({}, LINE {} \'{}\'): {}'.format(file_name, line_num, code, message)