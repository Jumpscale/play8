from JumpScale import j

"""
make sure to load the ssh-agent before running this script"
"""

sshkey = j.atyourservice.new(name='sshkey', args={'key.name': 'id_rda'})

data = {
    'jumpscale.branch': 'ays_unstable',
    'jumpscale.enable': False,
    'ssh.port': 22,
    'login': 'root',
    'password': 'rooter',
    'ip': '172.20.0.21'
}
node1 = j.atyourservice.new(name='node.ssh', instance='node1', args=data)
data = {
    'jumpscale.branch': 'ays_unstable',
    'jumpscale.enable': False,
    'ssh.port': 22,
    'login': 'root',
    'password': 'rooter',
    'ip': '172.20.0.22'
}
node2 = j.atyourservice.new(name='node.ssh', instance='node2', args=data)
data = {
    'jumpscale.branch': 'ays_unstable',
    'jumpscale.enable': False,
    'ssh.port': 22,
    'login': 'root',
    'password': 'rooter',
    'ip': '172.20.0.23'
}
node3 = j.atyourservice.new(name='node.ssh', instance='node3', args=data)
nodes = [node1, node2, node3]

redis = j.atyourservice.new(name='redis.system', parent=node1)

data = {
    'tcp.addr': 'localhost',
    'admin.login': 'root',
    'admin.password': 'root',
}
influxdb = j.atyourservice.new(name='influxdb', args=data, parent=node1)

data = {'param.port': '18384'}
syncthing = j.atyourservice.new(name='syncthing', args=data, parent=node1)
data = {'param.webservice.host': '172.20.0.21:8966'}
ac2 = j.atyourservice.new(name='agentcontroller2', args=data, parent=node1, consume='!node1@redis')


data = {
    'gid': 1,
    'nid': 1,
    'roles': 'node'
}
agent = j.atyourservice.new(name='agent2', args=data, parent=node2, consume='agentcontroller2')

data = {
    'gid': 1,
    'nid': 2,
    'roles': 'node'
}
agent = j.atyourservice.new(name='agent2', args=data, parent=node3, consume='agentcontroller2')

j.atyourservice.apply()