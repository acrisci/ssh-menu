from .config import init_config
from .config import get_servers_config
from .config import get_default_servers_config_path
from .config import Server
from .commands import add_server, remove_server, run_app
from argparse import ArgumentParser

parser = ArgumentParser()
parser.set_defaults(func=run_app)

subparsers = parser.add_subparsers(title='commands', help='commands', dest='command')

# The `add` subparser adds a new server
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

# The `remove` subparser removes an existing server
remove_subparser = subparsers.add_parser('rm',
                                         help='Remove a server',
                                         description='Remove a server',
                                         add_help=True,
                                         usage='rm [name]')
remove_subparser.add_argument('name',
                              help='The name of the server to remove')
remove_subparser.set_defaults(func=remove_server)


args = parser.parse_args()

init_config()
path = get_default_servers_config_path()
config = get_servers_config(path)

args.func(args, config)
