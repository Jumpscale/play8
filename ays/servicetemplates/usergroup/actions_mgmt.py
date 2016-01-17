from JumpScale import j



ActionsBase=j.atyourservice.getActionsBaseClassMgmt()

class Actions(ActionsBase):
    
    def input(self,serviceObj):
        #need to find the members based on tel or email addr

        #prob not needed
        # j.atyourservice.reset() #make sure we reload all

        membersfound=[]

        if "users" in serviceObj.args:            
            serviceObj.args["users"]=j.data.text.getList(serviceObj.args["users"])
            for email_tel_name in serviceObj.args["users"]:
                #find the member
                found=False
                for user in j.atyourservice.findServices(role="user"):
                    if email_tel_name in user.hrd.getList("email"):
                        membersfound.append(user.instance)
                        found=True
                        continue
                    if email_tel_name in user.hrd.getList("mobile"):
                        membersfound.append(user.instance)
                        found=True
                        continue
                if found==False:
                    msg="could not find user:\n%s\ntrying to create group:\n%s"%(user,serviceObj)
                    raise RuntimeError(msg)

        if "groups" in serviceObj.args:
            serviceObj.args["groups"]=j.data.text.getList(serviceObj.args["groups"])
            for groupname in serviceObj.args["groups"]:
                #find the group
                groups= j.atyourservice.findServices(role="usergroup",instance=groupname)
                if len(groups)==0:
                    msg="could not find group:\n%s\ntrying to create group:\n%s"%(groupname,serviceObj)
                    raise RuntimeError(msg)
                elif len(groups)>1:
                    msg="found more than 1 group:\n%s\ntrying to create group:\n%s"%(groupname,serviceObj)
                    raise RuntimeError(msg)
                else:
                    group=groups[0]
                    for member in group.hrd.getList("members"): 
                        if member not in membersfound:
                            membersfound.append(member)

        #this gives us the instance names, independant from which tel or email address was used for identification
        serviceObj.args["members"]=membersfound

        ActionsBase.input(self,serviceObj)
        

    def install_pre(self, service_obj):

        print("check with id mgmt system if user exists")

    def install_post(self, service_obj):

        print("send email to customer to let him know he exists")
