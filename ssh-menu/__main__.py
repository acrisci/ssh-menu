from .config import init_config
from .config import get_servers_config
from .config import get_default_servers_config_path
from .config import Server
from . import widget
from argparse import ArgumentParser

def validate_connection(connection):
    return connection.count('@') == 1 and connection.count(' ') == 0

def add_server(args, config):
    if not validate_connection(args.connection):
        ArgumentParser.exit(1, "Invalid connection string '%s' (must be user@address)" % args.connection)

    (user, address) = args.connection.split('@')
    config.add_server(args.name, user, address)
    config.save()

def run_app(args, config):
    print('running app...')
    print(args)
    choice = widget.start(config)
    print('user chose: %s' % choice)

parser = ArgumentParser()
parser.set_defaults(func=run_app)

subparsers = parser.add_subparsers(title='commands', help='commands', dest='command')

add_subparser = subparsers.add_parser('add',
                                      help='Add a new server',
                                      description='Add a new server',
                                      add_help=True,
                                      usage='add [name] [connection]')

add_subparser.add_argument('name',
                           help='A name to give to the server')
add_subparser.add_argument('connection',
                           help='The connection string (user@address)')
add_subparser.set_defaults(func=add_server)

args = parser.parse_args()

init_config()
path = get_default_servers_config_path()
config = get_servers_config(path)

args.func(args, config)
