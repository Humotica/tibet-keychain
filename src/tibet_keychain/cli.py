"""
tibet-keychain CLI — list / show / events / explain.

This v0.1.0 CLI is type-only: it inspects records and prints
human-readable views. Storage backend, sealed-bundle integration,
and rotation flow follow in v0.2+ once design lands with tibet-sam
and tibet-gateway.
"""
from __future__ import annotations

import argparse
import json
import sys

from . import __version__, SecretType, SecretTimelineEvent, ActorClass


def _cmd_types(args):
    """List the vocabulary."""
    print(f"tibet-keychain {__version__}")
    print()
    print(f"Secret types ({len(list(SecretType))}):")
    for t in SecretType:
        print(f"  {t.value}")
    print()
    print(f"Timeline events ({len(list(SecretTimelineEvent))}):")
    for e in SecretTimelineEvent:
        print(f"  {e.value}")
    print()
    print(f"Actor classes ({len(list(ActorClass))}):")
    for a in ActorClass:
        print(f"  {a.value}")
    return 0


def _cmd_family(args):
    """Print the vault family overview."""
    print("""
══════════════════════════════════════════════════════════════════
  THE TIBET VAULT FAMILY
══════════════════════════════════════════════════════════════════

  tibet-vault       WHEN         temporal trigger
                                 "release on date / dead-man-switch"

  tibet-keychain    WHERE/HOW    custody + timeline       ← you are here
                                 "where this secret lives, how it moved"

  tibet-sam         WHY          intent + scope authorization
                                 "why this one specific act is allowed"

  tibet-gateway     WHERE-EXEC   execution boundary
                                 "where the act is safely performed"

══════════════════════════════════════════════════════════════════
""")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="tibet-keychain",
        description=(
            "Causal-aware secret custody. Part of the TIBET vault "
            "family (vault / keychain / sam / gateway)."
        ),
    )
    parser.add_argument(
        "-V", "--version", action="version",
        version=f"tibet-keychain {__version__}",
    )
    sub = parser.add_subparsers(dest="cmd")

    p_types = sub.add_parser("types", help="List vocabulary (secret types, events, actor classes)")
    p_types.set_defaults(func=_cmd_types)

    p_family = sub.add_parser("family", help="Show the TIBET vault family overview")
    p_family.set_defaults(func=_cmd_family)

    args = parser.parse_args(argv)
    if not args.cmd:
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
