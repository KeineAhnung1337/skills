#!/usr/bin/env python3
"""Read-only, dependency-free inventory for a QF-Test XML suite.

Not a QF-Test parser or validator. Never executes suite scripts or opens URLs.
"""

import argparse
import collections
import pathlib
import sys
import xml.etree.ElementTree as ET


def local_name(tag):
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else str(tag)


def inspect(path):
    print("Suite:", path)
    try:
        # QF-Test files commonly contain <!DOCTYPE RootStep>. ElementTree does
        # not fetch external DTDs; reject explicit entity declarations here.
        data = path.read_bytes()
        if b"<!ENTITY" in data.upper():
            print("Inventory skipped: entity declarations require QF-Test's own parser")
            return 2
        root = ET.fromstring(data)
    except (OSError, ET.ParseError) as error:
        print("Cannot parse XML:", error)
        return 2

    counts = collections.Counter(local_name(node.tag) for node in root.iter())
    print("Root:", local_name(root.tag))
    print("Node types (XML names; not validated):")
    for tag, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        print("  {}: {}".format(tag, count))
    print("All top-level child elements:")
    for child in root:
        print("  {}".format(local_name(child.tag)))
    print("Includes and named test nodes:")
    for node in root.iter():
        tag = local_name(node.tag)
        if tag == "include" and node.text:
            print("  include: {}".format(node.text.strip()))
        elif tag in ("TestSet", "TestCase", "Test", "Package", "Procedure"):
            print("  {}: {}".format(tag, node.get("name", "(unnamed)")))
    print("XML is well-formed; only QF-Test can verify suite semantics.")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("suites", metavar="suite.qft", nargs="+", type=pathlib.Path)
    args = parser.parse_args()
    return max(inspect(path) for path in args.suites)


if __name__ == "__main__":
    sys.exit(main())
