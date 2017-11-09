class DictByAttr(dict):

    def __getattr__(self, key):
        return self.__getitem__(key)


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
