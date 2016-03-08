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
    to = j.sal.fs.joinPaths(tmpdir, 'app')
    c.file_download(url, '{}.zip'.format(to))
    c.run('unzip {to}.zip -d {to}'.format(to=to))
    print("Application is downloaded to: {}".format(to))
    c.dir_ensure(j.sal.fs.joinPaths(to, 'cfg'))
    c.file_copy(j.sal.fs.joinPaths('kanboard', 'app', 'cfg', 'config.php'), j.sal.fs.joinPaths(to, 'cfg'))
    c.file_copy(j.sal.fs.joinPaths('kanboard', 'app', 'cfg', 'vhosts.conf'), j.sal.fs.joinPaths(to, 'cfg'))
    c.file_copy(j.sal.fs.joinPaths('kanboard', 'docker-compose.yaml'), tmpdir)
    c.run('docker-compose {} up'.format(j.sal.fs.joinPaths(tmpdir, 'docker-compose.yaml')))



@click.command()
@click.option('--host', '-h', help='connectionstring e.g. myserver:2022')
@click.option('--up', '-h', help='True for docker-compose up, False for docker-compose down')
def dockercompose(host="", up=True):
    c = j.tools.cuisine.get(host)
    dc = """
    version: '2'
    services:
      db:
        image: bitnami/mariadb
        environment:
          - MARIADB_DATABASE=kanboard
          - MARIADB_USER=mysql
          - MARIADB_PASSWORD=mysql
        volumes:
          - ./app/data:/bitnami/mariadb/data

      kanboard:
        image: bitnami/php-fpm
        volumes:
          - ./app/kanboard:/app
          - ./app/cfg/config.php:/app/config.php
        links:
          - db:db
        ports:
          - "9000:9000"

      web:
        image: bitnami/nginx
        ports:
          - "8080:81"
          - "443:443"
        links:
          - kanboard:kanboard
        volumes:
          - ./app/cfg/vhosts.conf:/bitnami/nginx/conf/vhosts/kanboard.conf
          - ./app/kanboard:/app
    """








cli.add_command(preparehost)
cli.add_command(downloadsource)

if __name__ == '__main__':
    cli()