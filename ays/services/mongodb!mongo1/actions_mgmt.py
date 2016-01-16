import hashlib
from JumpScale import j

ActionsBase = j.atyourservice.getActionsBaseClass()


class Actions(ActionsBase):

    def install_pre(self, service_obj):

        print("we would do some capacity planning action to reality db")

    def install_post(self, service_obj):

        print.log("send email to customer")
