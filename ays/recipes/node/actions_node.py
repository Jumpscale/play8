
from JumpScale import j

ActionsBase = j.atyourservice.getActionsBaseClassNode()


class Actions(ActionsBase):

    def install(self, service_obj):

        print("remote install action")

