from JumpScale import j
import click

@click.group()
def cli():
    pass

@click.command()
@click.option('--host', '-h', help='connectionstring e.g. myserver:2022')
def preparehost(host="", keyname="",pushkey=False):
    """
    prepare ssh host to do dockerpcompose on, assuming that keys have been pushed
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

    print ("INSTALL DOCKER-COMPOSE, THIS WILL TAKE A WHILE")
    c.package.install('docker-compose')

@click.command()
@click.option('--host', '-h', help='connectionstring e.g. myserver:2022')
@click.option('--url', '-h', help='url for php application e.g. http://kanboard.net/kanboard-latest.zip')
def downloadsource(host="", url="http://kanboard.net/kanboard-latest.zip"):
    """
    download source file for the php app on the remote machine

    :param url:
    :return:
    """
    c = j.tools.cuisine.get(host)
    tmpdir = j.sal.fs.joinPaths(j.dirs.tmpDir, 'composeexample')
    c.run("rm -rf {tmpdir};mkdir {tmpdir}".format(tmpdir=tmpdir))
    to = j.sal.fs.joinPaths(tmpdir, 'application')
    c.file_download(url, '{}.zip'.format(to))
    c.run('unzip {to}.zip -d {to}'.format(to=to))

    print("Application is downloaded to: %s"%to)


@click.command()
@click.option('--host', '-h', help='connectionstring e.g. myserver:2022')
@click.option('--url', '-h', help='url for php application e.g. http://kanboard.net/kanboard-latest.zip')
def downloadsource(host="", url="http://kanboard.net/kanboard-latest.zip"):







cli.add_command(preparehost)
cli.add_command(downloadsource)

if __name__ == '__main__':
    cli()