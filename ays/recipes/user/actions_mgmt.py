import hashlib
from JumpScale import j

ActionsBase = j.atyourservice.getActionsBaseClassMgmt()


class Actions(ActionsBase):

    def todb(self, service_obj):

        service_obj.log("this would dump data to database")
