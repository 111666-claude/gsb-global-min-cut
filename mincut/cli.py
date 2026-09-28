"""命令行入口：算无向图的全局最小割。"""

import argparse
import sys

from .cut import CutError, global_min_cut, parse_edges


def build_parser():
    parser = argparse.ArgumentParser(prog="global-min-cut", description="无向图全局最小割")
    parser.add_argument("--edges", help="逗号分隔的 u-v:容量")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if not args.edges:
        print("错误：需要 --edges", file=sys.stderr)
        return 2
    try:
        edges = parse_edges(args.edges)
        capacity, side = global_min_cut(edges)
    except (CutError, ValueError) as error:
        print("错误：%s" % error, file=sys.stderr)
        return 1
    print("cut=%d" % capacity)
    print("side=%s" % ",".join(side))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
