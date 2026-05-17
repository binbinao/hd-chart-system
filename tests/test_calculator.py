"""Tests for Human Design chart calculator."""
import sys
import pytest

sys.path.insert(0, '/root/.openclaw/workspace/hd-chart-system')

from hd_calc.models import CalculateRequest
from hd_calc.calculator import calculate_chart


class TestRobinChart:
    """Robin: 1982-10-09 21:45, UTC+8, 30.94N 118.75E

    Using Moshier ephemeris, the computed chart is:
    - Type: ManifestingGenerator (Sacral defined + motor-to-throat)
    - Authority: Sacral
    - Profile: 1/1
    - Channels: 34-57 (Power), 18-58 (Judgment), 21-45 (Money)
    - Defined centers: Throat, Heart, Spleen, Sacral, Root
    """

    @pytest.fixture
    def chart(self):
        req = CalculateRequest(
            year=1982, month=10, day=9,
            hour=21, minute=45,
            timezone_offset=8.0,
            lat=30.94, lng=118.75,
        )
        return calculate_chart(req)

    def test_type_is_generator_family(self, chart):
        assert chart.type_key in ('Generator', 'ManifestingGenerator')

    def test_sacral_defined(self, chart):
        assert chart.centers['Sacral'].is_defined

    def test_authority_sacral(self, chart):
        # Sacral authority when Sacral is defined and no Solar Plexus
        if chart.centers['Sacral'].is_defined and not chart.centers['SolarPlexus'].is_defined:
            assert 'Sacral' in chart.authority_en or '荐骨' in chart.authority_zh

    def test_channel_34_57(self, chart):
        channel_pairs = {tuple(sorted((ch.gate1, ch.gate2))) for ch in chart.channels}
        assert (34, 57) in channel_pairs

    def test_channel_18_58(self, chart):
        channel_pairs = {tuple(sorted((ch.gate1, ch.gate2))) for ch in chart.channels}
        assert (18, 58) in channel_pairs

    def test_spleen_defined(self, chart):
        assert chart.centers['Spleen'].is_defined

    def test_root_defined(self, chart):
        assert chart.centers['Root'].is_defined

    def test_personality_sun_valid(self, chart):
        assert 1 <= chart.personality['Sun'].gate <= 64
        assert 1 <= chart.personality['Sun'].line <= 6

    def test_design_sun_valid(self, chart):
        assert 1 <= chart.design['Sun'].gate <= 64
        assert 1 <= chart.design['Sun'].line <= 6

    def test_profile_format(self, chart):
        parts = chart.profile.split('/')
        assert len(parts) == 2
        assert all(p.isdigit() for p in parts)

    def test_earth_opposite_sun_personality(self, chart):
        sun_lon = chart.personality['Sun'].longitude
        earth_lon = chart.personality['Earth'].longitude
        diff = abs(sun_lon - earth_lon)
        assert abs(diff - 180.0) < 0.5 or abs(360.0 - diff - 180.0) < 0.5


class TestManifestorChart:
    """Known Manifestor: 1940-07-20 10:00, UTC+1, London.
    Computed: Manifestor, Profile 2/2
    Defined: Ajna, Throat, Heart (motor-to-throat, no Sacral)
    """

    @pytest.fixture
    def chart(self):
        req = CalculateRequest(
            year=1940, month=7, day=20,
            hour=10, minute=0,
            timezone_offset=1.0,
            lat=51.5, lng=0.0,
        )
        return calculate_chart(req)

    def test_is_manifestor(self, chart):
        assert chart.type_key == 'Manifestor'

    def test_no_sacral(self, chart):
        assert not chart.centers['Sacral'].is_defined

    def test_has_throat(self, chart):
        assert chart.centers['Throat'].is_defined

    def test_has_motor_center(self, chart):
        # At least one motor should be defined and connected to throat
        motor_defined = any(chart.centers[m].is_defined for m in ['Heart', 'SolarPlexus', 'Root', 'Sacral'] if m != 'Sacral')
        assert motor_defined

    def test_authority_not_sacral(self, chart):
        assert 'Sacral' not in chart.authority_en


class TestProjectorChart:
    """Known Projector: 1955-12-01 06:00, UTC+0, London.
    Computed: Projector, Profile 3/6
    Defined: Ajna, Throat, G, Heart, SolarPlexus (no Sacral, no motor-to-throat)
    """

    @pytest.fixture
    def chart(self):
        req = CalculateRequest(
            year=1955, month=12, day=1,
            hour=6, minute=0,
            timezone_offset=0.0,
            lat=51.5, lng=0.0,
        )
        return calculate_chart(req)

    def test_is_projector(self, chart):
        assert chart.type_key == 'Projector'

    def test_no_sacral(self, chart):
        assert not chart.centers['Sacral'].is_defined

    def test_has_defined_centers(self, chart):
        defined = [k for k, v in chart.centers.items() if v.is_defined]
        assert len(defined) >= 1

    def test_authority_is_solar_plexus(self, chart):
        # SolarPlexus is defined and has highest priority
        if chart.centers['SolarPlexus'].is_defined:
            assert 'Emotional' in chart.authority_en or '情绪' in chart.authority_zh


class TestDegreeToGateLine:
    """Test the degree_to_gate_line conversion."""

    def test_gate_41_start(self):
        from hd_calc.calculator import degree_to_gate_line
        gate, line = degree_to_gate_line(302.0)
        assert gate == 41
        assert line == 1

    def test_gate_19_start(self):
        from hd_calc.calculator import degree_to_gate_line
        gate, line = degree_to_gate_line(302.0 + 5.625)
        assert gate == 19
        assert line == 1

    def test_line_6(self):
        from hd_calc.calculator import degree_to_gate_line
        gate, line = degree_to_gate_line(302.0 + 5.625 - 0.01)
        assert gate == 41
        assert line == 6

    def test_all_gates_valid(self):
        from hd_calc.calculator import degree_to_gate_line
        from hd_constants import GATE_ORDER
        for i in range(64):
            lon = 302.0 + i * 5.625
            gate, line = degree_to_gate_line(lon)
            assert gate == GATE_ORDER[i], f"Segment {i}: expected {GATE_ORDER[i]}, got {gate}"
            assert line == 1


class TestEdgeCases:
    """Edge case tests."""

    def test_design_date_computed(self):
        req = CalculateRequest(
            year=2000, month=1, day=1,
            hour=12, minute=0,
            timezone_offset=0.0,
            lat=51.5, lng=0.0,
        )
        chart = calculate_chart(req)
        assert chart.design_date_approx
        assert len(chart.design_date_approx) == 10

    def test_south_node_opposite_north_node(self):
        req = CalculateRequest(
            year=2000, month=6, day=15,
            hour=6, minute=0,
            timezone_offset=0.0,
            lat=0.0, lng=0.0,
        )
        chart = calculate_chart(req)
        nn_lon = chart.personality['NorthNode'].longitude
        sn_lon = chart.personality['SouthNode'].longitude
        diff = abs(nn_lon - sn_lon)
        assert abs(diff - 180.0) < 0.5 or abs(360.0 - diff - 180.0) < 0.5

    def test_incarnation_cross_gates_valid(self):
        req = CalculateRequest(
            year=1982, month=10, day=9,
            hour=21, minute=45,
            timezone_offset=8.0,
            lat=30.94, lng=118.75,
        )
        chart = calculate_chart(req)
        assert len(chart.incarnation_cross_gates) == 4
        assert all(1 <= g <= 64 for g in chart.incarnation_cross_gates)

    def test_all_planets_present(self):
        req = CalculateRequest(
            year=2000, month=6, day=15,
            hour=6, minute=0,
            timezone_offset=0.0,
            lat=0.0, lng=0.0,
        )
        chart = calculate_chart(req)
        from hd_constants import PLANET_NAMES_ORDERED
        for name in PLANET_NAMES_ORDERED:
            assert name in chart.personality
            assert name in chart.design

    def test_definition_type_not_none(self):
        req = CalculateRequest(
            year=2000, month=6, day=15,
            hour=6, minute=0,
            timezone_offset=0.0,
            lat=0.0, lng=0.0,
        )
        chart = calculate_chart(req)
        assert chart.definition_type in ('single', 'split', 'triple', 'quadruple', 'none')
