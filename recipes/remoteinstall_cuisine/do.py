from JumpScale import j
import click

@click.group()
def cli():
    pass

@click.command()
@click.option('--host', '-h', help='connectionstring e.g. myserver:2022')
@click.option('--passwd', '-h', help='passwd')
@click.option('--keyname', '-k', help='nameof key to use, if not given will ask', default="")
def pushsshkey(host, keyname="",passwd=""):
    """
    python3 do.py pushsshkey --host '192.168.0.250:22' --passwd 'rooter' --keyname 'ovh_install'
    """
    pubkey=j.clients.ssh.getSSHKeyFromAgentPub(keyname)
    cl=j.tools.cuisine.getPushKey(addr=host, login='root', passwd=passwd, pubkey=pubkey)


@click.command()
@click.option('--host', '-h', help='connectionstring e.g. myserver:2022')
def preparehost(host="", keyname="",pushkey=False):
    """
    prepare ssh host to do docker on
    e.g.
    python3 do.py preparehost --host '192.168.0.250:22' 
    """
    c=j.tools.cuisine.get(host)

    print ("install jumpscale, this will take a while")
    #be carefull this will remove history, will be installed in read write mode
    c.installer.jumpscale8(rw=True, reset=True)


    print ("INSTALL DOCKER, THIS WILL TAKE A WHILE")
    #install docker
    c.docker.install()        


@click.command()
@click.option('--host', '-h', help='connectionstring e.g. myserver:2022')
@click.option('--keyname', '-k', help='nameof key to use, if not given will ask', default="")
def buildallInDocker(host="", keyname=""):
    """
    example:
    python3 do.py buildall --host '192.168.0.250:22' --keyname 'ovh_install'
    """
    def dockerbuild(host):
        c=j.tools.cuisine.get(host)

        #build ubuntu from docker file
        print ("BUILD UBUNTU WITH SSH SUPPORT")
        c.docker.ubuntuBuild()

    buildaction=j.actions.add(dockerbuild,args=[host],stdOutput=True,retry=2,executeNow=False)

    
    def dockerstart(keyname,host):
        c=j.tools.cuisine.get(host)
        pubkey=j.clients.ssh.getSSHKeyFromAgentPub(keyname)
        print ("LAUNCH UBUNTU DOCKER WITH MY PUB LOCAL SSH KEY")
        connstr=c.docker.ubuntu(name="ubuntu_build", image='jumpscale/ubuntu1510', ports=None, volumes=None, pubkey=pubkey, aydofs=False)
        return connstr


    dockerstart=j.actions.add(dockerbuild,args=[keyname,host],stdOutput=True,retry=2,executeNow=False,deps=[buildaction])

    connstr=dockerstart.result

    def dockerbuildjs8(connstr):
        print ("DOCKERBUILD JS8")
        print ("connectionstring of docker:%s"%connstr)
        c2=j.tools.cuisine.get(connstr)
        c2.builder.all()

    dockerbuildjs8=j.actions.add(dockerbuildjs8,args=[connstr],stdOutput=True,retry=2,executeNow=False,deps=[dockerstart])

    def pushdocker(host):
        c=j.tools.cuisine.get(host)
        from IPython import embed
        print ("DEBUG NOW pushdocker")
        embed()
        

    dockerbuildjs8=j.actions.add(pushdocker,args=[host],stdOutput=True,retry=2,executeNow=False,deps=[dockerbuildjs8])

    j.actions.run()



cli.add_command(pushsshkey)
cli.add_command(preparehost)
cli.add_command(buildallInDocker)

if __name__ == '__main__':
    cli()

