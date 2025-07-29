from python_sdk_remote.our_object import OurObject

ENTITY_NAME = "Organization"


class Organization(OurObject):

    # TODO Add all fields
    fields = {
        "organization_id",
        "display_as",
    }

    def __init__(self, entity_name=ENTITY_NAME, **kwargs):
        super().__init__(entity_name, **kwargs)

    # Mandatory pure virtual method from OurObject
    def get_name(self):
        print(f"{ENTITY_NAME} get_name() self.fields.display_as={self.fields.display_as}")
        return self.fields.display_as
