import os
import re
import subprocess

from argparse import ArgumentParser

PROTO_FILE_REGEXP = re.compile(r'.*\.proto')


def protoc(root_dir, proto_dest, conf):
    """
    build protoc files for golang
    """

    cmd = [
        "protowrap",
        "-I{0}".format(root_dir),
        f"--{conf['outname']}_out={conf['outdir']}",
    ]

    if len(conf.get('options', [])) > 0:
        options = conf['options']
        for option in options:
            cmd.append(option)

    files = []
    for f in os.listdir(proto_dest):
        fp = os.path.join(proto_dest, f)
        if PROTO_FILE_REGEXP.match(fp):
            files.append(fp)

    if files:
        subprocess.run(cmd + files)


def build_directory(root_dir, pwd, conf):
    """
    Builds all .proto files in a directory, will recurse if provided file is a dir
    """

    protoc(root_dir, pwd, conf)
    for f in os.listdir(pwd):
        fp = os.path.join(pwd, f)
        if os.path.isdir(fp):
            build_directory(root_dir, fp, conf)


def main():
    """
    main function
    """
    build_conf = {
        'python': {
            'outname': 'python',
            'outdir': 'schema-python',
        },
        'go': {
            'outname': 'go',
            'outdir': '.',
        },
        'ts': {
            'outname': 'ts_proto',
            'outdir': 'github.com/dailydotdev/schema-ts',
            'options': ['--ts_proto_opt=oneof=unions', '--ts_proto_opt=unrecognizedEnum=false'],
        },
    }

    parser = ArgumentParser(description='builder for proto files')

    parser.add_argument('language', help='language to build')
    parser.add_argument('root', help='directory to search for proto files in')

    args = parser.parse_args()

    if not build_conf.get(args.language):
        print(f'unknown language: {args.language}')

    else:
        build_directory(
            args.root,
            args.root,
            build_conf.get(args.language),
        )

    return 0


if __name__ == '__main__':
    print('building...')
    main()
