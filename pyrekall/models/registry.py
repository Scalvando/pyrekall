import pyrekall.models.common


class Registry(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent objects discovered within the Windows registry
    """
    def __init__(self, session):
        super(Registry, self).__init__()

        self.session = session

    def _get_hives(self):
        """
        This function is used for the purpose of identifying the registry hives which have been loaded into the Windows
        registry

        :return: a list of registry hives
        """
        return self.session.plugins.hives().list_hives()

    def get_hive_names(self):
        """
        This function is used for the purpose of identifying the names of the registry hives which have been loaded into
        the Windows registry. Currently, this list does not include unnamed registry hives.

        :return: a list of registry hive names
        """
        names = []
        for hive in self._get_hives():
            name = str(hive.Name).split(" @ ")[0]
            if name != '[no name]':
                names.append(name)
        return names

    def summary(self):
        return {
            'hives': self.get_hive_names()
        }