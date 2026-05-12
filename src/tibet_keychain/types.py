"""
Core types for tibet-keychain.

Defines the vocabulary used across the package: secret types, timeline
event types, actor classes, exposure states, and the two main records
(SecretRecord and CustodyTransition).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class SecretType(str, Enum):
    """Recognised secret-material classes.

    The TIBET vault family does not invent new credential formats —
    it provides a custody substrate around existing ones.
    """
    API_KEY = "api_key"
    OAUTH_TOKEN = "oauth_token"
    SIGNING_KEY = "signing_key"
    SERVICE_ACCOUNT_CREDENTIAL = "service_account_credential"
    PYPI_TOKEN = "pypi_token"
    CRATES_TOKEN = "crates_token"
    GITHUB_PAT = "github_pat"
    SSH_KEY = "ssh_key"
    ROOT_PASSWORD = "root_password"
    SMART_CONTRACT_SIGNER = "smart_contract_signer"
    TLS_CERT = "tls_cert"
    WEBHOOK_SIGNER = "webhook_signer"


class SecretTimelineEvent(str, Enum):
    """Every meaningful state change a secret can go through.

    The keychain's value is precisely that every one of these events
    is recorded with actor / authority / parent_action_id, making the
    custody chain walkable from any point in time.
    """
    CREATED = "secret-created"
    IMPORTED = "secret-imported"
    SEALED = "secret-sealed"
    UNSEALED = "secret-unsealed"
    PROXIED = "secret-proxied"
    DELEGATED = "secret-delegated"
    EXPOSED = "secret-exposed"
    ROTATED = "secret-rotated"
    REVOKED = "secret-revoked"
    ARCHIVED = "secret-archived"


class ActorClass(str, Enum):
    """Who touched the secret. Not every actor is equal.

    A timeline that records HUMAN unsealing has different policy
    implications than one that records GATEWAY proxying.
    """
    HUMAN = "human"
    MACHINE = "machine"
    EXTERNAL = "external"
    MCP_SERVER = "mcp-server"
    GATEWAY = "gateway"
    SYSTEM = "system"


class ExposureState(str, Enum):
    """Current exposure assessment of the secret material."""
    SEALED = "sealed"
    IN_USE = "in-use"
    CHAT_DISCLOSED = "chat-disclosed"
    GIT_LEAKED = "git-leaked"
    LOG_LEAKED = "log-leaked"
    SUSPECTED = "suspected"
    ROTATED = "rotated"


@dataclass
class SecretRecord:
    """The metadata view of a secret in the keychain.

    The actual secret material lives inside a sealed `.tza` payload
    block; this record is the auditable metadata projection.
    """
    secret_id: str
    secret_type: SecretType
    issuer: str                 # who minted the underlying credential
    scope: str                  # what it is allowed to authorise
    created_at: str             # RFC3339
    expires_at: Optional[str] = None
    owner_id: Optional[str] = None         # JIS-DID of nominal owner
    custodian_id: Optional[str] = None     # who currently holds it
    active_operator_id: Optional[str] = None  # who is allowed to use it
    last_access_action_id: Optional[str] = None
    last_rotation_action_id: Optional[str] = None
    exposure_state: ExposureState = ExposureState.SEALED
    rotation_required: bool = False
    notes: list[str] = field(default_factory=list)


@dataclass
class CustodyTransition:
    """A single transition in a secret's custody timeline.

    Mirrors the shape of tibet-cbom ownership-transition events so
    that keychain transitions can be walked by `tcbom timeline`
    when an audit-file is supplied.
    """
    action_id: str
    parent_action_id: Optional[str]
    secret_id: str
    event: SecretTimelineEvent
    actor_id: str
    actor_class: ActorClass
    timestamp: str              # RFC3339
    reason: str = ""
    authority_mode: str = "system"  # agent / admin / triage / shared / system
    target_assignee: Optional[str] = None
    policy_lane: Optional[str] = None
