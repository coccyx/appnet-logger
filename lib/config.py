from ConfigParser import ConfigParser
import logging, logging.handlers
import os


class Config:
	# Stolen from http://code.activestate.com/recipes/66531/
    # This implements a Borg patterns, similar to Singleton
    # It allows numerous instantiations but always shared state
    __sharedState = {}

    _conf = None

    max_bytes = None
    backup_files = None
    file_name = None

    access_token = None
    global_stream_url = None
    min_id = None

    sleep_time = None

    grandparent_dir = None

    def __init__(self):
        # Rebind the internal datastore of the class to an Instance variable
        self.__dict__ = self.__sharedState

        logger = logging.getLogger('appnet')
        logger.propagate = False
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)

        self.grandparent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self._conf = ConfigParser()
        self._conf.read([self.grandparent_dir+'/conf/global.conf'])

        for sect in self._conf.sections():
            for item in self._conf.items(sect):
                setattr(self, item[0], item[1])

                if item[0] == 'sleep_time':
                    setattr(self, item[0], float(item[1]))

    def set_min_id(self, min_id):
        self.min_id = min_id
        self._conf.set('appnet', 'min_id', min_id)
        f = open(self.grandparent_dir+'/conf/global.conf', 'w')
        self._conf.write(f)
