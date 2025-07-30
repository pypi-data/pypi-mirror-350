"""
Tiny Jinja2 wrapper that gives YAML authors helper functions:

    * ``state``   – dict of runtime variables
    * ``noise()`` – Gaussian noise helper
    * ``set(k,v)``– update ``state[k]`` and return ``v``

Both query *and* write responses are rendered through this engine.
"""

from __future__ import annotations

import random
from typing import Any, Dict

from jinja2 import Environment, StrictUndefined


def _noise(mu: float = 0.0, sigma: float = 1.0) -> float:  # noqa: D401
    return random.gauss(mu, sigma)


def make_env(state: Dict[str, Any]) -> Environment:  # noqa: D401
    env = Environment(undefined=StrictUndefined)
    env.globals.update(
        noise=_noise,
        set=lambda k, v: state.__setitem__(k, v) or v,
        state=state,
    )
    return env
