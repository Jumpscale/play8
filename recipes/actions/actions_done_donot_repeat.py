from JumpScale import j


#this is a test to see how actions can be nested and only the one with the error should be shown

def action_error():
    print ("ACTIONERROR")
    raise RuntimeError("ERROR")


def action_1(nr,counter=None):
    print ("ACTION%s"%nr)

def recover_action():
    print ("RECOVER")


j.actions.setRunId("actiontest")
j.actions.resetAll()

for i in range(10):
    a=j.actions.add(action_1,args=[i],kwargs={"counter":i},executeNow=True,force=False)


for i in range(3,13):
    a=j.actions.add(action_1,args=[i],kwargs={"counter":i},executeNow=True,force=False)
