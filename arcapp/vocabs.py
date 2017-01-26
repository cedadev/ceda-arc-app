class DictByAttr(dict):

    def __getattr__(self, key):
        return self.__getitem__(key)


STATUS_VALUES_DICT = {
        'COMPLETED': 'completed',
        'IN_PROGRESS': 'in progress',
        'NOT_STARTED': 'not started',
        'NOT_SUBMITTED': 'not submitted',
        'FAILED': 'failed'
    }

STATUS_VALUES = DictByAttr(STATUS_VALUES_DICT.items())
