"""
instrubyte.core.types
~~~~~~~~~~~~~~~~~~~~~~~~~

Centralised **dataclass-style** models (using Pydantic) that every other
sub-package imports.  They cover

* the *capability manifest* a driver advertises, and
* the *JSONTaskGraph* Copilot ships over the wire.

Keep them *pure*: no I/O, no business logic—just structure & validation.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, root_validator, validator


# --------------------------------------------------------------------------- #
# 1.  Capability Manifest primitives
# --------------------------------------------------------------------------- #

class CapabilityCategory(str, Enum):
    """Whether a capability is mandatory for class compliance or not."""
    BASE = "base"
    OPTIONAL = "optional"


class Capability(BaseModel):
    """
    One verb that a concrete driver exposes (see §3.2 of the design doc).

    Example
    -------
    ```json
    {
        "verb": "measure_voltage",
        "params": { "mode": { "enum": ["AC", "DC"] }, "range": { "type": "number" } },
        "returns": "float",
        "category": "base"
    }
    ```
    """
    verb: str = Field(...,
                      description="snake_case verb name, e.g. ``measure_voltage``")
    params: Dict[str, Any] = Field(default_factory=dict,
                                   description="JSON-Schema fragment for parameters")
    returns: str = Field(...,
                         description="Return-type identifier (JSON-serialisable)")
    category: CapabilityCategory = Field(default=CapabilityCategory.BASE,
                                         description="'base' or 'optional'")

    # --- basic hygiene ----------------------------------------------------- #
    @validator("verb")
    def _validate_snake_case(cls, v: str) -> str:          # noqa: D401
        if not v.islower() or " " in v:
            raise ValueError("verb must be lower snake_case with no spaces")
        return v


# --------------------------------------------------------------------------- #
# 2.  Planner / Policy metadata
# --------------------------------------------------------------------------- #

class PolicyTag(str, Enum):
    SAFE = "safe"
    DANGEROUS = "dangerous"
    HAZARDOUS_VOLTAGE = "hazardous_voltage"
    # Add further tags that your lab policy requires


# --------------------------------------------------------------------------- #
# 3.  Task-graph primitives
# --------------------------------------------------------------------------- #

class TaskNode(BaseModel):
    """
    A single node inside a ``JSONTaskGraph`` DAG.

    Matches the contract shown in §2.2 *Architectural Contract*.
    """
    id: str = Field(..., description="Unique node identifier")
    instrument_id: str = Field(...,
                               description="Logical name resolved to a driver instance")
    verb: str = Field(..., description="Capability to invoke, e.g. ``measure_voltage``")
    params: Dict[str, Any] = Field(default_factory=dict,
                                   description="Concrete arguments for *verb*")
    policy_md: List[PolicyTag] = Field(default_factory=list,
                                       description="Planner-applied safety tags")
    depends_on: List[str] = Field(default_factory=list,
                                  description="IDs this node must wait for")


class JSONTaskGraph(BaseModel):
    """
    Top-level container exchanged between Copilot and Instrument-SDK.
    """
    nodes: List[TaskNode] = Field(...,
                                  description="Whole DAG (preferably topological order)")
    metadata: Optional[Dict[str, Any]] = Field(default=None,
                                               description="Opaque planner/runtime info")

    # --- DAG-level validation --------------------------------------------- #
    @root_validator(skip_on_failure=True)
    def _validate_dag(cls, values):                        # noqa: D401
        nodes = values.get("nodes") or []
        ids = [n.id for n in nodes]

        # 1. no duplicate node IDs
        if len(ids) != len(set(ids)):
            dupes = {i for i in ids if ids.count(i) > 1}
            raise ValueError(f"Duplicate node id(s) in graph: {', '.join(sorted(dupes))}")

        # 2. every dependency must reference an existing node
        id_set = set(ids)
        for node in nodes:
            missing = [d for d in node.depends_on if d not in id_set]
            if missing:
                raise ValueError(
                    f"Node '{node.id}' depends on unknown id(s): {', '.join(missing)}"
                )

        return values


__all__ = [
    "CapabilityCategory",
    "Capability",
    "PolicyTag",
    "TaskNode",
    "JSONTaskGraph",
]
