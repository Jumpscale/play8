from JumpScale import j


#this is a test to see how actions can be nested and only the one with the error should be shown

def action_error(nr,counter=None):
    print ("ACTIONERROR")
    raise RuntimeError("ERROR")


def action_1(nr,counter=None):
    print ("ACTION%s"%nr)

def recover_action():
    print ("RECOVER")

simulateerror=True

j.actions.setRunId("actiontest")
# j.actions.resetAll()


start=j.actions.add(action_1,args=[99999],kwargs={"counter":99999},executeNow=False,force=False)

deps2=[]

for i in range(10):
    a=j.actions.add(action_1,args=[i],kwargs={"counter":i},executeNow=False,force=False,deps=[start])
    if simulateerror:
        if i==7:
            a=j.actions.add(action_error,args=[i],kwargs={"counter":i},executeNow=False,force=False,deps=[start])
    deps2.append(a)


for i in range(11,15):
    a=j.actions.add(action_1,args=[i],kwargs={"counter":i},executeNow=False,force=False,deps=deps2)

j.actions.run()