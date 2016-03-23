import hashlib
from JumpScale import j

ActionsBase = j.atyourservice.getActionsBaseClassMgmt()


class Actions(ActionsBase):

    def install_pre(self, service_obj):

        print("we would do some capacity planning action to reality db")

    def install_post(self, service_obj):

        print("send email to customer")

    def monitor(self,service_obj):
        return
        raise j.exceptions.RuntimeError("fake error")