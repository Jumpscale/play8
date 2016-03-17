from JumpScale import j


c = j.tools.cuisine.local

#dont look at history
c.reset_actions()

# from pudb import set_trace; set_trace() 
c.bash.environ

c.bash.addPath('/tmp')
c.bash.addPath('/tmp2')

from IPython import embed
print ("DEBUG NOW id")
embed()
