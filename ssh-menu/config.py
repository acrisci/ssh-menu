import os
import json

VERSION = "1"

VERSION_KEY = "version"
SERVERS_KEY = "servers"

SERVER_NAME_KEY = "name"
SERVER_USER_KEY = "user"
SERVER_DESCRIPTION_KEY = "description"
SERVER_ADDRESS_KEY = "address"

home = os.environ['HOME']
default_config_dir = "%s/.ssh-menu" % home
default_servers_config = '%s/servers' % default_config_dir


class InvalidConfigException(Exception):
    pass


def get_default_servers_config_path():
    """Return the default path of the servers config file"""
    return default_servers_config


def init_config():
    """Initialize the config. If a config file already exists, it does nothing."""

    if not os.path.exists(default_config_dir):
        os.mkdir(default_config_dir)

    if os.path.exists(default_servers_config):
        # the servers config already exists
        return

    config_template = { VERSION_KEY: VERSION, SERVERS_KEY: [] }

    with open(default_servers_config, mode='w') as f:
        f.writelines(json.dumps(config_template, indent=2))


def get_servers_config(path):
    """Parse the file into a ServersConfig object. Throws InvalidConfigException if the config is not valid"""

    with open(path, 'r') as f:
        config = json.loads(f.read())

        if not VERSION_KEY in config or config[VERSION_KEY] != VERSION:
            raise InvalidConfigException("unsupported config version")

        if not SERVERS_KEY in config or not isinstance(config[SERVERS_KEY], list):
            raise InvalidConfigException("malformed or missing %s from config" % SERVERS_KEY)

        servers = []

        for server in config[SERVERS_KEY]:
            # validate the server
            required_keys = [ SERVER_NAME_KEY, SERVER_USER_KEY, SERVER_ADDRESS_KEY ]
            for k in required_keys:
                if k not in server:
                    raise InvalidConfigException("server missing required key: %s" % k)

            # add defaults
            if SERVER_DESCRIPTION_KEY not in server:
                server[SERVER_DESCRIPTION_KEY] = ""

            servers.append(Server(name=server[SERVER_NAME_KEY],
                                  user=server[SERVER_USER_KEY],
                                  address=server[SERVER_ADDRESS_KEY],
                                  description=server[SERVER_DESCRIPTION_KEY]))

        return ServersConfig(path, servers)


class Server():
    """A class for an individual server that a user can connect to"""
    def __init__(self, name, user, address, description):
        # TODO: last time it connected for sorting
        self.name = name
        self.user = user
        self.address= address
        self.description = description


class ServersConfig():
    """A class for accessing the server config and persistence"""
    def __init__(self, path, servers):
        self.path = path
        self.servers = servers
