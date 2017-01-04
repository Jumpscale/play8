from JumpScale import j
import prettytable


def printAgents(agents):
    table = prettytable.PrettyTable(['Agent', 'Hostname', 'Roles', 'CPU', 'Mem'])

    print '# Agents'
    for agent in agents:
        table.add_row([
            '%d:%d' % (agent.gid, agent.nid),
            agent.hostname,
            ', '.join(agent.roles),
            '%d%%' % agent.cpu,
            agent.mem
        ])

    print table

    print ''
    for agent in agents:
        print '# Agent %d:%d' % (agent.gid, agent.nid)
        networking = prettytable.PrettyTable(['Interface', 'MAC', 'Addresses'])
        for interface, mac in agent.macaddr.iteritems():
            addresses = agent.ipaddr.get(interface, [])
            networking.add_row([interface, mac, ', '.join(addresses)])
        print networking


def main():
    client = j.clients.ac.get()  # Gets the client to local redis
    agents = client.getAgents()
    printAgents(agents)

    # open tunnel from agent 1.2 9900 -> agent 1.1 9800

    client.tunnel_create(1, 2, 9900, 1, 1, '127.0.0.1', 9800)

    job = client.executeAsync('nc -l -p 9800', gid=1, nid=1)[0]  # expecting one job
    status, out, err = client.executeBash('echo "Hello Agent" | nc -q 0 localhost 9900', gid=1, nid=2)

    job.wait()  # waits until the job terminates.

    print job.state
    print job.streams

    # close tunnel
    client.tunnel_close(1, 2, 9900, 1, 1, '127.0.0.1', 9800)


if __name__ == '__main__':
    main()
