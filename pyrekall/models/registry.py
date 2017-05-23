import pyrekall.models.common


class Registry(pyrekall.models.common.AbstractWrapper):
    def __init__(self, session):
        super(Registry, self).__init__()

        self.session = session

    def _get_hives(self):
        return self.session.plugins.hives().list_hives()

    def get_hive_names(self):
        names = []
        for hive in self._get_hives():
            name = str(hive.Name).split(" @ ")[0]
            if name != '[no name]':
                names.append(name)
        return names