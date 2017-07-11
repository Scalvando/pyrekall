from rekall.plugins.windows.registry.printkey import Services
from pprint import pprint

import pyrekall.helpers.usability
import pyrekall.models.common


class Service(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent services. This class should be expanded to include the process associated with a
    particular service.
    """
    def __init__(self, service):
        super(Service, self).__init__()

        self.name = service.Name.v()
        self.path = service.Path or None
        self.tag = None
        self.group = None
        self.display_name = None
        self.object_name = None
        self.description = None
        self.image_path = None
        self.type = None
        self.start = None
        self.error_control = None
        self.additional_attributes = {}

        metadata = self.__collect_metadata_as_dict(service=service)
        for k, v in metadata.items():
            if k in ['depend_on_service', 'depend_on_group']:
                continue
            elif k in self.__dict__:
                setattr(self, k, v)
            else:
                self.additional_attributes[k] = v

        self.depends_on_services = metadata.get('depend_on_service', [])
        self.depends_on_groups = metadata.get('depend_on_group', [])

    @staticmethod
    def __collect_metadata_as_dict(service):
        metadata = {}
        for value in service.values():
            k = pyrekall.helpers.usability.camelcase_to_snakecase(value.Name.v())
            v = value.DecodedData

            if value.Type == "REG_BINARY":
                continue

            if isinstance(v, list):
                v = [x for x in v if x]

            if k == "type":
                v = Services.SERVICE_TYPE.get(v, v)
            elif k == "start":
                v = Services.START_TYPE.get(v, v)
            elif k == "error_control":
                v = Services.ERROR_CONTROL.get(v, v)

            metadata[k] = v
        return metadata

    def summary(self):
        return {
            'name': self.name,
            'tag': self.tag,
            'group': self.group,
            'display_name': self.display_name,
            'object_name': self.object_name,
            'description': self.description,
            'image_path': self.image_path,
            'type': self.type,
            'start': self.start,
            'error_control': self.error_control,
            'additional_attributes': self.additional_attributes,
            'depends_on_services': self.depends_on_services,
            'depends_on_groups': self.depends_on_groups,
        }