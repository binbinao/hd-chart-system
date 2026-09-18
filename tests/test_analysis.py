"""Unit tests for hd_calc.analysis primitives.

These exercise _determine_definition_type / _determine_authority / _determine_profile
directly with constructed centers, independent of the ephemeris, so the HD rules
can be pinned per input.
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from hd_constants import CENTERS
from hd_calc.models import CenterInfo


def _centers(defined_names):
    """Build a full 9-center dict with only `defined_names` marked defined.

    With no activated channels, each defined center is its own connected
    component, so the component count == len(defined_names).
    """
    return {
        name: CenterInfo(
            name=name,
            name_zh=data['zh'],
            name_en=data['en'],
            is_defined=(name in defined_names),
            activated_gates=[],
        )
        for name, data in CENTERS.items()
    }


class TestDefinitionTypeSpelling:
    """The contract (models.ChartResult.definition_type docstring) is the short
    set: single / split / triple / quadruple / none. Code previously emitted
    'triple_split' / 'quadruple_split', which leaked to the API, DB, and UI.
    """

    def test_triple_is_short_form(self):
        from hd_calc.analysis import _determine_definition_type
        # 3 defined centers, no channels -> 3 components
        result = _determine_definition_type(_centers({'Sacral', 'Head', 'Root'}), [])
        assert result == 'triple'

    def test_quadruple_is_short_form(self):
        from hd_calc.analysis import _determine_definition_type
        result = _determine_definition_type(_centers({'Sacral', 'Head', 'Root', 'Spleen'}), [])
        assert result == 'quadruple'


class TestAuthority:
    """Authority determination per HD doctrine.

    - 'Throat Authority' is not a real HD authority and must never be emitted.
    - Mental Projectors (non-Reflector, no inner-authority center defined) have
      Outer authority. 'Lunar' is Reflector-only and must not be assigned to a
      non-Reflector.
    """

    def test_mental_projector_without_throat_is_outer(self):
        from hd_calc.analysis import _determine_authority
        # Head+Ajna only: no motor, no Sacral, no Throat, no G -> Mental Projector.
        auth = _determine_authority(_centers({'Head', 'Ajna'}), 'Projector')
        assert auth['en'] == 'Outer Authority'
        assert auth['zh'] == '外在权威'

    def test_mental_projector_with_throat_is_outer_not_throat(self):
        from hd_calc.analysis import _determine_authority
        # Throat defined but no motor-to-Throat -> still a Mental Projector;
        # previously mislabeled as 'Throat Authority'.
        auth = _determine_authority(_centers({'Head', 'Ajna', 'Throat'}), 'Projector')
        assert auth['en'] == 'Outer Authority'
        assert 'Throat' not in auth['en']

    def test_reflector_is_lunar(self):
        from hd_calc.analysis import _determine_authority
        auth = _determine_authority(_centers(set()), 'Reflector')
        assert auth['en'] == 'Lunar Authority'
        assert auth['zh'] == '月循环权威'

    def test_sacral_authority_preserved(self):
        from hd_calc.analysis import _determine_authority
        auth = _determine_authority(_centers({'Sacral'}), 'Generator')
        assert auth['en'] == 'Sacral Authority'


class TestPlanetActivationValidation:
    """PlanetActivation must reject out-of-range gate/line at construction.

    This stops a missing-planet sentinel (gate 0) from silently producing a
    fabricated '1/1' profile downstream.
    """

    def test_gate_zero_rejected(self):
        from hd_calc.models import PlanetActivation
        with pytest.raises(ValueError):
            PlanetActivation(longitude=0.0, gate=0, line=1)

    def test_gate_too_high_rejected(self):
        from hd_calc.models import PlanetActivation
        with pytest.raises(ValueError):
            PlanetActivation(longitude=0.0, gate=65, line=1)

    def test_line_out_of_range_rejected(self):
        from hd_calc.models import PlanetActivation
        with pytest.raises(ValueError):
            PlanetActivation(longitude=0.0, gate=1, line=7)
        with pytest.raises(ValueError):
            PlanetActivation(longitude=0.0, gate=1, line=0)


class TestProfileRequiresSun:
    """A missing Sun must raise, not silently yield an invalid '1/1' profile."""

    @staticmethod
    def _sun():
        from hd_calc.models import PlanetActivation
        # Gate 41 starts at 302deg on the HD wheel; a consistent Sun activation.
        return PlanetActivation(longitude=302.0, gate=41, line=1)

    def test_missing_personality_sun_raises(self):
        from hd_calc.analysis import _determine_profile
        with pytest.raises(KeyError):
            _determine_profile({}, {'Sun': self._sun()})

    def test_missing_design_sun_raises(self):
        from hd_calc.analysis import _determine_profile
        with pytest.raises(KeyError):
            _determine_profile({'Sun': self._sun()}, {})
