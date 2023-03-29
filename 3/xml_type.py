import xml.dom.minidom as minidom

from dataclasses import dataclass
from typing import Generator, Literal

TypeNodeInfo = tuple[str, Literal["new", "old"]]


@dataclass
class IterationInfo:
    q: list[minidom.Element]
    labeled_nodes: dict[str, minidom.Element]
    visited_nodes: set[minidom.Element]
    total_nodes: int

    @property
    def all_nodes_visited(self) -> bool:
        return len(self.visited_nodes) == self.total_nodes


def _count_nodes(node: minidom.Element) -> int:
    return 1 + sum(
        _count_nodes(child)
        for child in node.childNodes
        if child.nodeType == minidom.Element.ELEMENT_NODE
    )


def iterate_type(
    filename: str, stop_when_all_visited=True
) -> Generator[tuple[minidom.Element, IterationInfo], bool | None, None]:
    doc = minidom.parse(filename)
    iteration_info = IterationInfo(
        q=[doc.childNodes[0]],
        labeled_nodes=dict(),
        visited_nodes=set(),
        total_nodes=_count_nodes(doc.childNodes[0]),
    )
    continue_: bool | None = None

    while (
        iteration_info.q
        and (continue_ is None or continue_)
        and not (stop_when_all_visited and iteration_info.all_nodes_visited)
    ):
        t = iteration_info.q[0]
        iteration_info.q = iteration_info.q[1:]
        _info = "old" if t in iteration_info.visited_nodes else "new"
        iteration_info.visited_nodes.add(t)

        if t.tagName == "type-ref":
            _t = iteration_info.labeled_nodes[t.getAttribute("ref")]
            continue_ = yield (_t, iteration_info)
            iteration_info.q.extend(
                [c for c in _t.childNodes if c.nodeType == minidom.Element.ELEMENT_NODE]
            )
        else:
            continue_ = yield (t, iteration_info)
            iteration_info.q.extend(
                [c for c in t.childNodes if c.nodeType == minidom.Element.ELEMENT_NODE]
            )

        if _id := t.getAttribute("id"):
            iteration_info.labeled_nodes[_id] = t


def diff_types(filename_l: str, filename_r: str, MAX_ITER=500) -> tuple[int, minidom.Element | None, minidom.Element | None]:
    for i, (l, r) in enumerate(
        zip(
            iterate_type(filename_l, stop_when_all_visited=False),
            iterate_type(filename_r, stop_when_all_visited=False),
        )
    ):
        if l[0].tagName != r[0].tagName:
            return i, l[0], r[0]
        if l[1].all_nodes_visited and r[1].all_nodes_visited:
            return 0, None, None
        if i > MAX_ITER:
            raise Exception(f"Exceeded {MAX_ITER=}")
    return 0, None, None


if __name__ == "__main__":
    import argparse
    import sys

    argparser = argparse.ArgumentParser()
    argparser.add_argument("-p", "--print")
    argparser.add_argument("-d", "--diff", nargs=2)
    argparser.add_argument("-v", "--verbose", action="store_true")
    args = argparser.parse_args(sys.argv[1:])

    if args.print:
        for node, info in iterate_type(args.print):
            if args.verbose:
                print(f"{node.tagName} {len(info.visited_nodes)}/{info.total_nodes}")
            else:
                print(f"{node.tagName}")
    else:
        if len(args.diff) < 2:
            raise Exception("If not printing, then two diff args must be present")
        dist, l, r = diff_types(args.diff[0], args.diff[1])
        if args.verbose:
            print(f"{dist=} {l.tagName if l is not None else None} {r.tagName if r is not None else None}")
        else:
            print(f"{dist}")

