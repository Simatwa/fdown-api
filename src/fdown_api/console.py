import argparse
from os import getcwd

parser = argparse.ArgumentParser(
    prog="fdown",
    description="Download Facebook videos seamlessly.",
    epilog="This script has no official relation with fdown.net.",
)
parser.add_argument("url", help="Link to the target facebook video")
parser.add_argument(
    "-d",
    "--dir",
    help="Directory for saving the video to - %(default)s",
    default=getcwd(),
)
parser.add_argument(
    "-o", "--output", help="Filename under which to save the video to - random"
)
parser.add_argument(
    "-q",
    "--quality",
    help="Video download quality - %(default)s",
    metavar="normal|hd",
    choices=["normal", "hd"],
    default="hd",
)
parser.add_argument(
    "-t",
    "--timeout",
    help="Http request timeout in seconds - %(default)s",
    default=20,
    type=int,
)
parser.add_argument(
    "-c",
    "--chunk-size",
    type=int,
    default=512,
    metavar="chunk-size",
    help="Chunk-size for downloading files in KB - %(default)s",
)
parser.add_argument(
    "-p",
    "--proxy",
    nargs=2,
    help="Http request proxy - %(default)s",
    metavar="PROTOCOL ADDRESS",
)
parser.add_argument(
    "--resume",
    action="store_true",
    help="Resume an incomplete download - %(default)s",
)
parser.add_argument(
    "--quiet",
    action="store_false",
    help="Do not stdout any informational messages - False",
)
parser.add_argument("--version", action="version", version="1.0.0")

args = parser.parse_args()


def main():
    from fdown_api import Fdown

    f = Fdown(args.timeout, {args.proxy[0]: args.proxy[1]} if args.proxy else {})
    try:
        saved_to = f.download_video(
            videolinks=f.get_links(args.url),
            quality=args.quality,
            filename=args.output,
            dir=args.dir,
            progress_bar=args.quiet,
            quiet=False,
            chunk_size=args.chunk_size,
            resume=args.resume,
        )
        if not args.quiet:
            print(saved_to)
    except Exception as e:
        print(f"> Error - {e.args[1] if e.args and len(e.args)>1 else e}.\nQuitting")
        from sys import exit

        exit(1)


if __name__ == "__main__":
    main()
