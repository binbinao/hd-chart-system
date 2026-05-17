"""Data models for Human Design chart calculation."""
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class CalculateRequest:
    year: int
    month: int
    day: int
    hour: int
    minute: int
    timezone_offset: float  # hours from UTC, e.g. +8 for CST
    lat: float
    lng: float


@dataclass
class PlanetActivation:
    longitude: float  # ecliptic longitude in degrees
    gate: int
    line: int  # 1-6


# Type aliases
Personality = Dict[str, PlanetActivation]
Design = Dict[str, PlanetActivation]


@dataclass
class ChannelActivation:
    gate1: int
    gate2: int
    name_zh: str
    name_en: str
    personality_gates: List[int] = field(default_factory=list)
    design_gates: List[int] = field(default_factory=list)


@dataclass
class CenterInfo:
    name: str  # key like 'Sacral', 'Spleen', etc.
    name_zh: str
    name_en: str
    is_defined: bool
    activated_gates: List[int] = field(default_factory=list)


@dataclass
class ChartResult:
    request: CalculateRequest
    personality: Personality
    design: Design
    design_date_approx: str  # ISO date string for the approximate design date
    channels: List[ChannelActivation]
    centers: Dict[str, CenterInfo]
    type_key: str  # 'Generator', 'ManifestingGenerator', etc.
    type_zh: str
    type_en: str
    authority_zh: str
    authority_en: str
    profile: str  # e.g. "1/5"
    profile_conscious_line: int
    profile_design_line: int
    definition_type: str  # 'single', 'split', 'triple', 'quadruple', 'none'
    incarnation_cross_zh: Optional[str]
    incarnation_cross_en: Optional[str]
    incarnation_cross_gates: List[int]  # [personality_sun, personality_earth, design_sun, design_earth]
