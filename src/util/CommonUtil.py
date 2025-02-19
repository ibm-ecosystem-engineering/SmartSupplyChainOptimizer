from datetime import datetime, timedelta
import logging
import os

### Static methods
class CommonUtil :

    logger = logging.getLogger(__name__)
    logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    @staticmethod
    def str_to_float(num_str, defaultValue):
        result = defaultValue
        try:
            result = float(num_str)
        except Exception as e:
            # DictionaryUtil.logger.debug (f' Error in getValue_key1 : {e} ')
           result = defaultValue
        return result

