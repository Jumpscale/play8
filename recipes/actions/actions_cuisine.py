from JumpScale import j

j.actions.setRunId("testcuisine")

c=j.tools.cuisine.get("192.168.0.250")
c.core.run("ls /",force=False)
c.core.run("ls /",force=False)
c.core.run("ls /dd",force=False)
c.core.run("ls /",force=False)