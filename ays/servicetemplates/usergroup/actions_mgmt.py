from JumpScale import j


ActionsBase=j.atyourservice.getActionsBaseClassMgmt()

class Actions(ActionsBase):
    
    def input(serviceObj):
        #need to find the members based on tel or email addr
        from IPython import embed
        print ("DEBUG NOW input group")
        embed()
        ActionsBase.input(self,serviceObj)
        

