"""
tibet-keychain — Causal-aware secret custody.

Part of the TIBET vault family:
  tibet-vault     WHEN       temporal trigger
  tibet-keychain  WHERE/HOW  custody + timeline    ← this package
  tibet-sam       WHY        intent + scope
  tibet-gateway   WHERE-EXEC execution boundary

Naming decision Jasper van de Meent 12 May 2026:
    "tibet-vault = when
     tibet-keychain = where/how secret lives
     tibet-sam = why this one act is allowed
     tibet-gateway = where the act is performed safely"

Spec source:
    /srv/jtel-stack/hersenspinsels/tibet-vault-key-custody-and-sealed-secret-timeline-2026-05-12.md
"""
from __future__ import annotations

from .types import (
    SecretType,
    SecretTimelineEvent,
    ActorClass,
    ExposureState,
    SecretRecord,
    CustodyTransition,
)


__version__ = "0.1.0"
__author__ = "Jasper van de Meent, Root AI, Codex"


__all__ = [
    "__version__",
    "SecretType",
    "SecretTimelineEvent",
    "ActorClass",
    "ExposureState",
    "SecretRecord",
    "CustodyTransition",
]
