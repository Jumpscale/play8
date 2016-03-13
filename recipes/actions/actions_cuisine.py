from JumpScale import j

j.actions.setRunId("testcuisine")

c=j.tools.cuisine.get("192.168.0.250")
c.run("ls /")
c.run("ls /")
c.run("ls /dd")
