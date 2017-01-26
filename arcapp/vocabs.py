class DictByAttr(dict):

    def __getattr__(self, key):
        return self.__getitem__(key)


STATUS_VALUES = DictByAttr(
    {
        'COMPLETED': 'completed',
        'IN_PROGRESS': 'in progress',
        'NOT_STARTED': 'not started',
        'NOT_SUBMITTED': 'not submitted',
        'FAILED': 'failed'
    }.items())

VARIABLES = DictByAttr(
    {
        'tas': 'Mean air temperature',
        'u-wind': 'Eastward wind speed',
        'v-wind': 'Northward wind speed'
    }.items())


DATA_FILES =  DictByAttr(
    {
        'data1.txt': 'eg_files/data1.txt',
        'data2.txt': 'eg_files/data2.txt',
        'data3.txt': 'eg_files/data3.txt'
    }.items())
