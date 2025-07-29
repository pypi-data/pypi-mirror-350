from argparse import ArgumentParser

from pygallery.build import build
from pygallery.serve import serve

commands = {
    'serve': serve,
    'build': build,
}


def main():
    parser = ArgumentParser(prog='pygallery', description='Python Static Photo Gallery Generator v0.0.8')
    parser.add_argument("-p", "--path", required=True, type=str, help="Path to the images")
    parser.add_argument('-o', '--output', required=True, type=str, help="Output path to save static galleries")
    parser.add_argument('-t', '--title', type=str, help="Title of the gallery", default="Gallery")
    parser.add_argument('-H', '--host', type=str, help="Host name to serve at", default="0.0.0.0")
    parser.add_argument('-P', '--port', type=int, help="Port number to serve at", default=8000)
    parser.add_argument('command', choices=commands.keys(), help="Command to run")
    args = parser.parse_args()
    if args.command not in commands:
        parser.print_help()
        return
    commands[args.command](args)
