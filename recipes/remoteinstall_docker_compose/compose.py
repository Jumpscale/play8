from JumpScale import j
import click

@click.group()
def cli():
    pass

@click.command()
@click.option('--host', '-h', help='connectionstring e.g. myserver:2022')
def preparehost(host=""):
    """
    prepare ssh host to do dockerpcompose on, assuming that keys have been pushed
    e.g.
    python3 do.py preparehost --host '192.168.0.250:22'
    """
    c=j.tools.cuisine.get(host)

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
    c.file_copy(j.sal.fs.joinPaths('kanboard', 'docker-compose.yml'), tmpdir)
    c.run('docker-compose {} up'.format(j.sal.fs.joinPaths(tmpdir, 'docker-compose.yml')))



@click.command()
@click.option('--host', '-h', help='connectionstring e.g. myserver:2022')
@click.option('--url', '-u', help='url for php application e.g. http://kanboard.net/kanboard-latest.zip')
@click.option('--up', '-s', help='True for docker-compose up, False for docker-compose down')
def dockercompose(host="", url="http://kanboard.net/kanboard-latest.zip", up=True):
    """
    python3 compose.py dockercompose --host 'host:22' --url 'http://kanboard.net/kanboard-latest.zip'
    """
    c = j.tools.cuisine.get(host)
    # c = j.tools.cuisine.local
    tmpdir = j.sal.fs.joinPaths(j.dirs.tmpDir, 'composeexample')
    to = j.sal.fs.joinPaths(tmpdir, 'app')
    c.dir_ensure(tmpdir)
    c.dir_ensure(to)
    c.file_download(url, '{}.zip'.format(to))
    c.package.install('unzip')
    c.run('unzip {to}.zip -d {to}'.format(to=to))
    print("Application is downloaded to: {}".format(to))
    c.dir_ensure(j.sal.fs.joinPaths(to, 'cfg'))
    
    composetemplate_vars = {
      'db_username': 'mysql',
      'db_password': 'mysql',
      'web_port': '81',
      'db_hostname': 'db',
      'app_hostname': 'kanboard'
    }


    composetemplate = """
    version: '2'
    services:
      {db_hostname}:
        image: bitnami/mariadb
        environment:
          - MARIADB_DATABASE=kanboard
          - MARIADB_USER={db_username}
          - MARIADB_PASSWORD={db_password}
        volumes:
          - ./app/data:/bitnami/mariadb/data

      kanboard:
        image: bitnami/php-fpm
        volumes:
          - ./app/kanboard:/app
          - ./app/cfg/config.php:/app/config.php
        links:
          - {db_hostname}:{db_hostname}
        ports:
          - "9000:9000"

      web:
        image: bitnami/nginx
        ports:
          - "8080:{web_port}"
          - "443:443"
        links:
          - kanboard:kanboard
        volumes:
          - ./app/cfg/vhosts.conf:/bitnami/nginx/conf/vhosts/kanboard.conf
          - ./app/kanboard:/app
    """
    c.file_write(j.sal.fs.joinPaths(tmpdir, 'docker-compose.yml'), composetemplate.format(**composetemplate_vars))

    vhosts_template = """
    server {{
        listen 0.0.0.0:{web_port};
        #server_name kanboard.com;
        access_log /bitnami/nginx/logs/access.log;
        error_log /bitnami/nginx/logs/error.log;


        root /app;

        location / {{
            index index.php;
            try_files $uri $uri/ index.php;
        }}
        
        location ~ \.php$ {{
            # fastcgi_pass [PHP_FPM_LINK_NAME]:9000;
            fastcgi_pass {app_hostname}:9000;
            fastcgi_index index.php;
            include fastcgi.conf;
        }}
    }}
    """
    c.file_write(j.sal.fs.joinPaths(to, 'cfg', 'vhosts.conf'), vhosts_template.format(**composetemplate_vars))

    configphp_template = """
    <?php

    /*******************************************************************/
    /* Rename this file to config.php if you want to change the values */
    /*******************************************************************/

    // Enable/Disable debug
    define('DEBUG', false);

    // Debug file path
    define('DEBUG_FILE', __DIR__.DIRECTORY_SEPARATOR.'data'.DIRECTORY_SEPARATOR.'debug.log');

    // Plugins directory
    define('PLUGINS_DIR', 'plugins');

    // Folder for uploaded files
    define('FILES_DIR', 'data'.DIRECTORY_SEPARATOR.'files');

    // E-mail address for the "From" header (notifications)
    define('MAIL_FROM', 'notifications@kanboard.local');

    // Mail transport available: "smtp", "sendmail", "mail" (PHP mail function), "postmark", "mailgun", "sendgrid"
    define('MAIL_TRANSPORT', 'mail');

    // SMTP configuration to use when the "smtp" transport is chosen
    define('MAIL_SMTP_HOSTNAME', '');
    define('MAIL_SMTP_PORT', 25);
    define('MAIL_SMTP_USERNAME', '');
    define('MAIL_SMTP_PASSWORD', '');
    define('MAIL_SMTP_ENCRYPTION', null); // Valid values are "null", "ssl" or "tls"

    // Sendmail command to use when the transport is "sendmail"
    define('MAIL_SENDMAIL_COMMAND', '/usr/sbin/sendmail -bs');

    // Database driver: sqlite, mysql or postgres (sqlite by default)
    define('DB_DRIVER', 'mysql');

    // Mysql/Postgres username
    define('DB_USERNAME', '{db_username}');

    // Mysql/Postgres password
    define('DB_PASSWORD', '{db_password}');

    // Mysql/Postgres hostname
    define('DB_HOSTNAME', '{db_hostname}');

    // Mysql/Postgres database name
    define('DB_NAME', 'kanboard');

    // Mysql/Postgres custom port (null = default port)
    define('DB_PORT', null);

    // Enable LDAP authentication (false by default)
    define('LDAP_AUTH', false);

    // LDAP server hostname
    define('LDAP_SERVER', '');

    // LDAP server port (389 by default)
    define('LDAP_PORT', 389);

    // By default, require certificate to be verified for ldaps:// style URL. Set to false to skip the verification
    define('LDAP_SSL_VERIFY', true);

    // Enable LDAP START_TLS
    define('LDAP_START_TLS', false);

    // By default Kanboard lowercase the ldap username to avoid duplicate users (the database is case sensitive)
    // Set to true if you want to preserve the case
    define('LDAP_USERNAME_CASE_SENSITIVE', false);

    // LDAP bind type: "anonymous", "user" or "proxy"
    define('LDAP_BIND_TYPE', 'anonymous');

    // LDAP username to use with proxy mode
    // LDAP username pattern to use with user mode
    define('LDAP_USERNAME', null);

    // LDAP password to use for proxy mode
    define('LDAP_PASSWORD', null);

    // LDAP DN for users
    // Example for ActiveDirectory: CN=Users,DC=kanboard,DC=local
    // Example for OpenLDAP: ou=People,dc=example,dc=com
    define('LDAP_USER_BASE_DN', '');

    // LDAP pattern to use when searching for a user account
    // Example for ActiveDirectory: '(&(objectClass=user)(sAMAccountName=%s))'
    // Example for OpenLDAP: 'uid=%s'
    define('LDAP_USER_FILTER', '');

    // LDAP attribute for username
    // Example for ActiveDirectory: 'samaccountname'
    // Example for OpenLDAP: 'uid'
    define('LDAP_USER_ATTRIBUTE_USERNAME', 'uid');

    // LDAP attribute for user full name
    // Example for ActiveDirectory: 'displayname'
    // Example for OpenLDAP: 'cn'
    define('LDAP_USER_ATTRIBUTE_FULLNAME', 'cn');

    // LDAP attribute for user email
    define('LDAP_USER_ATTRIBUTE_EMAIL', 'mail');

    // LDAP attribute to find groups in user profile
    define('LDAP_USER_ATTRIBUTE_GROUPS', 'memberof');

    // Allow automatic LDAP user creation
    define('LDAP_USER_CREATION', true);

    // LDAP DN for administrators
    // Example: CN=Kanboard-Admins,CN=Users,DC=kanboard,DC=local
    define('LDAP_GROUP_ADMIN_DN', '');

    // LDAP DN for managers
    // Example: CN=Kanboard Managers,CN=Users,DC=kanboard,DC=local
    define('LDAP_GROUP_MANAGER_DN', '');

    // Enable LDAP group provider for project permissions
    // The end-user will be able to browse LDAP groups from the user interface and allow access to specified projects
    define('LDAP_GROUP_PROVIDER', false);

    // LDAP Base DN for groups
    define('LDAP_GROUP_BASE_DN', '');

    // LDAP group filter
    // Example for ActiveDirectory: (&(objectClass=group)(sAMAccountName=%s*))
    define('LDAP_GROUP_FILTER', '');

    // LDAP attribute for the group name
    define('LDAP_GROUP_ATTRIBUTE_NAME', 'cn');

    // Enable/disable the reverse proxy authentication
    define('REVERSE_PROXY_AUTH', false);

    // Header name to use for the username
    define('REVERSE_PROXY_USER_HEADER', 'REMOTE_USER');

    // Username of the admin, by default blank
    define('REVERSE_PROXY_DEFAULT_ADMIN', '');

    // Default domain to use for setting the email address
    define('REVERSE_PROXY_DEFAULT_DOMAIN', '');

    // Enable/disable remember me authentication
    define('REMEMBER_ME_AUTH', true);

    // Enable or disable "Strict-Transport-Security" HTTP header
    define('ENABLE_HSTS', true);

    // Enable or disable "X-Frame-Options: DENY" HTTP header
    define('ENABLE_XFRAME', true);

    // Enable syslog logging
    define('ENABLE_SYSLOG', true);

    // Escape html inside markdown text
    define('MARKDOWN_ESCAPE_HTML', true);

    // API alternative authentication header, the default is HTTP Basic Authentication defined in RFC2617
    define('API_AUTHENTICATION_HEADER', '');

    // Enable/disable url rewrite
    define('ENABLE_URL_REWRITE', false);

    // Hide login form, useful if all your users use Google/Github/ReverseProxy authentication
    define('HIDE_LOGIN_FORM', false);

    // Disabling logout (for external SSO authentication)
    define('DISABLE_LOGOUT', false);

    // Enable captcha after 3 authentication failure
    define('BRUTEFORCE_CAPTCHA', 3);

    // Lock the account after 6 authentication failure
    define('BRUTEFORCE_LOCKDOWN', 6);

    // Lock account duration in minute
    define('BRUTEFORCE_LOCKDOWN_DURATION', 15);

    // Session duration in second (0 = until the browser is closed)
    // See http://php.net/manual/en/session.configuration.php#ini.session.cookie-lifetime
    define('SESSION_DURATION', 0);

    // HTTP client proxy
    define('HTTP_PROXY_HOSTNAME', '');
    define('HTTP_PROXY_PORT', '3128');
    define('HTTP_PROXY_USERNAME', '');
    define('HTTP_PROXY_PASSWORD', '');
    """

    c.file_write(j.sal.fs.joinPaths(to, 'cfg', 'config.php'), configphp_template.format(**composetemplate_vars))
    c.run('docker-compose -f {} up'.format(j.sal.fs.joinPaths(tmpdir, 'docker-compose.yml')))


cli.add_command(preparehost)
cli.add_command(dockercompose)

if __name__ == '__main__':
    cli()