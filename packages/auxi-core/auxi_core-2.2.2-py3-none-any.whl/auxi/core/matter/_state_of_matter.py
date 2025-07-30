from enum import IntEnum

class StateOfMatter(IntEnum):
    """An enumeration representing the state of matter."""

    u = 0
    """Unknown."""

    s = 1
    """Solid."""
    
    l = 2  # noqa: E741
    """Liquid."""

    g = 4
    """Gas."""

    p = 8
    """Plasma."""

    sl = s | l
    sg = s | g
    slg = s | l | g
    sp = s | p
    slp = s | l | p
    slgp = s | l | g | p
    lp = l | p
    lgp = l | g | p
    gp = g | p
