from JumpScale import j

"""
make sure to load the ssh-agent before running this script"
"""


def createDocker(name, consume, parent, pf=''):
    data = {
        'docker.image': 'jumpscale/ubuntu1504',
        'docker.portsforwards': pf,
        'docker.volumes': '',
        'jumpscale.branch': 'ays_unstable',
        'jumpscale.enable': False,
        'jumpscale.sharecode': False,
    }
    return j.atyourservice.new(name='node.docker', instance=name, args=data, consume=consume, parent=parent)

def installAgent(nid, consume, parent):
    data = {
        'gid': 1,
        'nid': nid,
        'roles': 'node'
    }
    agent = j.atyourservice.new(name='agent2', args=data, parent=parent, consume=consume)

cfssl = j.atyourservice.new(name='cfssl', args={'initca': True})
sshkey = j.atyourservice.new(name='sshkey', args={'key.name': 'ovh_rsa'})
data = {
    'jumpscale.branch': 'ays_unstable',
    'jumpscale.enable': False,
    'ssh.port': 22,
    'login': '',
    'password': '',
    'ip': '94.23.38.89'
}
ovh4 = j.atyourservice.new(name='node.ssh', instance='ovh4', args=data, consume=sshkey)
master = createDocker('master', consume='%s,%s' % (sshkey, ovh4), parent=ovh4, pf="8966:8966 18384:18384")

node1 = createDocker('node1', sshkey, ovh4)
# node2 = createDocker('node2', sshkey, ovh4)
# node3 = createDocker('node3', sshkey, ovh4)

j.atyourservice.apply()

redis = j.atyourservice.new(name='redis.system', parent=master)

data = {
    'tcp.addr': 'localhost',
    'admin.login': 'root',
    'admin.password': 'root',
}
influxdb = j.atyourservice.new(name='influxdb', args=data, parent=master)

data = {'param.port': '18384'}
syncthing = j.atyourservice.new(name='syncthing', args=data, parent=master)
data = {'param.webservice.host': '%s:8966' % master.hrd.getStr('node.tcp.addr')}
ac2 = j.atyourservice.new(name='agentcontroller2', args=data, parent=master, consume="%s,%s" %(redis,cfssl))


installAgent(1, "%s,%s" % (ac2, cfssl), node1)
# installAgent(2, "%s,%s" % (ac2, cfssl), node2)
# installAgent(3, "%s,%s" % (ac2, cfssl), node3)

# j.atyourservice.apply()