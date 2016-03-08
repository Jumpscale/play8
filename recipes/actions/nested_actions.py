from JumpScale import j


#this is a test to see how actions can be nested and only the one with the error should be shown

class testactions():

    def action_error():
        print ("ACTIONERROR")
        raise RuntimeError("ERROR")


    def action_3():
        nr=3
        print ("ACTION%s"%nr)
        res=j.actions.add(j.testactions.action_error,die=True, stdOutput=True, errorOutput=True, executeNow=True,force=True)

    def action_2():
        nr=2
        print ("ACTION%s"%nr)
        res=j.actions.add(j.testactions.action_3,die=True, stdOutput=True, errorOutput=True, executeNow=True,force=True)

    def action_1():
        nr=1
        print ("ACTION%s"%nr)
        res=j.actions.add(j.testactions.action_2,die=True, stdOutput=True, errorOutput=True, executeNow=True,force=True)
        

    def recoveraction1():
        print("recoveraction1")

#each action cannot see the file where we start from, we need to bind to j
#when actions are executed in process then j stays visible

j.testactions=testactions()


j.actions.setRunId("actiontest")

recoveraction=j.actions.add(j.testactions.recoveraction1,executeNow=False,force=True)

res=j.actions.add(j.testactions.action_1, actionRecover=recoveraction, args=(), kwargs={}, die=True, stdOutput=True, errorOutput=True, retry=0, serviceObj=None, deps=None, executeNow=True,force=True)

