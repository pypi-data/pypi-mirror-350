# -*- coding: utf-8 -*-

import typing

import pydantic

from snowprofile._base_classes import AdditionalData, datetime_with_tz, datetime_tuple_with_tz
from snowprofile._constants import GRAIN_SHAPES

__all__ = ['CTStabilityTest', 'CTStabilityTestResult',
           'ECTStabilityTest', 'ECTStabilityTestResult',
           'PSTStabilityTest',
           'RBStabilityTest', 'RBStabilityTestResult',
           'ShearFrameStabilityTest', 'ShearFrameStabilityTestResult']


class _StabilityTest(pydantic.BaseModel):
    """
    Base class for Stability test representation.
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    id: typing.Optional[str] = None
    name: typing.Optional[str] = pydantic.Field(
        None,
        description="Name/short description of the test")
    related_profiles: typing.List[str] = pydantic.Field(
        [],
        description="id of related profiles")
    comment: typing.Optional[str] = None
    test_nr: typing.Optional[int] = pydantic.Field(
        None, ge=0,
        description="Test number (the lower is the higher priority)")
    name: typing.Optional[str] = pydantic.Field(
        None,
        description="Name/short description of the profile")
    comment: typing.Optional[str] = pydantic.Field(
        None,
        description="A comment associated to the profile")
    additional_data: typing.Optional[AdditionalData] = pydantic.Field(
        None,
        description="Field to store additional data for CAAML compatibility (customData), do not use.")


class _StabilityTestResult(pydantic.BaseModel):
    """
    Base class for stability tests result representation.

    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    height: typing.Optional[float] = pydantic.Field(
        None,
        description="Height of the failed layer (with zero at bottom of the snowpack (m)")
    layer_thickness: typing.Optional[float] = pydantic.Field(
        None,
        description="Thickness of the failed layer (m)")
    grain_1: typing.Optional[typing.Literal[tuple(GRAIN_SHAPES)]] = pydantic.Field(
        None,
        description="Primary grain shape of the failed layer")
    grain_2: typing.Optional[typing.Literal[tuple(GRAIN_SHAPES)]] = pydantic.Field(
        None,
        description="Secondary grain shape of the failed layer")
    grain_size: typing.Optional[float] = pydantic.Field(
        None,
        description="Snow grain size of the failed layer (m)")
    grain_size_max: typing.Optional[float] = pydantic.Field(
        None,
        description="Maximum snow grain size of the failed layer (m)")
    layer_formation_time: typing.Optional[datetime_with_tz] = pydantic.Field(
        None,
        description="The formation time of the failed layer.")
    layer_formation_period: typing.Optional[datetime_tuple_with_tz] = pydantic.Field(
        (None, None),
        description="The formation period (begin, end) of the failed layer.")
    layer_comment: typing.Optional[str] = pydantic.Field(
        None,
        description="Comment associated to layer description (for CAAML compatibility only, do not fill).")
    layer_additional_data: typing.Optional[AdditionalData] = pydantic.Field(
        None,
        description="Field to store additional data for CAAML compatibility (customData), do not use.")


class RBStabilityTestResult(_StabilityTestResult):
    """
    Class for RB (Rutschblock) stability test results.
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    test_score: int = pydantic.Field(
        description="RB result [1-7], 7 meaning no fracture",
        ge=1, le=7)
    release_type: typing.Optional[typing.Literal[
        'WB', 'MB', 'EB']] = pydantic.Field(
            None,
            description="Release type among:\n\n"
            "- WB: Whole block\n"
            "- MB: Most of the block\n"
            "- EB: Edge of the block")
    fracture_character: typing.Optional[typing.Literal[
        'SDN', 'SP', 'SC', 'RES', 'RP', 'PC', 'BRK',
        'Clean', 'Rough', 'Irregular',
        'Q1', 'Q2', 'Q3']] = pydantic.Field(
            None,
            description="Fracture characteristic among: \n\n"
            "- SP: Sudden planar\n"
        "- SC: Sudden collapse\n"
        "- SDN: Sudden (both)\n"
        "- RP: Resistant planar\n"
        "- PC: Progressive compression\n"
        "- RES: Resistant (both)\n"
        "- BRK or B: Break\n"
        "- Clean\n"
        "- Rough\n"
        "- Irregular\n"
        "- Q1\n"
        "- Q2\n"
        "- Q3")


class RBStabilityTest(_StabilityTest):
    """
    Class for RB (Rutschblock) stability test.
    """
    results: typing.List[RBStabilityTestResult] = pydantic.Field(
        [],
        description="Successive results of a single RB test. No results mean RB7.")
    type: typing.Literal['Rutschblock'] = 'Rutschblock'


class CTStabilityTestResult(_StabilityTestResult):
    """
    Class for CT (Comprerssion test) stability test results.
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    test_score: int = pydantic.Field(
        description="CT result [0-30]",
        ge=0, le=30)
    fracture_character: typing.Optional[typing.Literal[
        'SDN', 'SP', 'SC', 'RES', 'RP', 'PC', 'BRK',
        'Clean', 'Rough', 'Irregular',
        'Q1', 'Q2', 'Q3']] = pydantic.Field(
            None,
            description="Fracture characteristic among: \n\n"
            "- SP: Sudden planar\n"
        "- SC: Sudden collapse\n"
        "- SDN: Sudden (both)\n"
        "- RP: Resistant planar\n"
        "- PC: Progressive compression\n"
        "- RES: Resistant (both)\n"
        "- BRK or B: Break\n"
        "- Clean\n"
        "- Rough\n"
        "- Irregular\n"
        "- Q1\n"
        "- Q2\n"
        "- Q3")


class CTStabilityTest(_StabilityTest):
    """
    Class for CT (Compression test) stability test.
    """
    results: typing.List[CTStabilityTestResult] = pydantic.Field(
        [],
        description="Successive results of a single CT test. No results mean CT31.")
    type: typing.Literal['CT'] = 'CT'


class ECTStabilityTestResult(_StabilityTestResult):
    """
    Class for ECT (extended column test) stability test result.

    Set score=0 for ECTPV.
    """
    test_score: int = pydantic.Field(
        description="CT result [0-30]",
        ge=0, le=30)
    propagation: bool = False


class ECTStabilityTest(_StabilityTest):
    """
    Class for ECT (Extended column test) stability test.
    """
    results: typing.List[ECTStabilityTestResult] = pydantic.Field(
        [],
        description="Successive results of a single ECT test. No results mean ECTN.")
    type: typing.Literal['ECT'] = 'ECT'


class PSTStabilityTest(_StabilityTest, _StabilityTestResult):
    """
    Class for PST (Propagation Saw test) stability test.
    """
    column_length: typing.Optional[float] = pydantic.Field(
        None,
        description="Length of the column used for stability test (m).")
    cut_length: float = pydantic.Field(
        description="The cut length necessary to start the propagation.")
    propagation: typing.Literal['End', 'SF', 'Arr'] = pydantic.Field(
        description="Propagation type: \n\n"
        "- End means the fracture propagate through the end of the column,\n"
        "- SF means slab fracture,\n"
        "- Arr means arrest of the propagation before the end of the column.")
    type: typing.Literal['PST'] = 'PST'


class ShearFrameStabilityTestResult(_StabilityTestResult):
    """
    Class for shear frame stability test results.
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    force: float = pydantic.Field(
        description="Failure force (N).",
        ge=0)
    fracture_character: typing.Optional[typing.Literal[
        'SDN', 'SP', 'SC', 'RES', 'RP', 'PC', 'BRK',
        'Clean', 'Rough', 'Irregular',
        'Q1', 'Q2', 'Q3']] = pydantic.Field(
            None,
            description="Fracture characteristic among: \n\n"
            "- SP: Sudden planar\n"
        "- SC: Sudden collapse\n"
        "- SDN: Sudden (both)\n"
        "- RP: Resistant planar\n"
        "- PC: Progressive compression\n"
        "- RES: Resistant (both)\n"
        "- BRK or B: Break\n"
        "- Clean\n"
        "- Rough\n"
        "- Irregular\n"
        "- Q1\n"
        "- Q2\n"
        "- Q3")


class ShearFrameStabilityTest(_StabilityTest):
    """
    Class for Shear frame stability test.
    """
    results: typing.List[ShearFrameStabilityTestResult] = pydantic.Field(
        [],
        description="Successive results of a single SF test. No results mean no failure.")
    type: typing.Literal['Shear Frame'] = 'Shear Frame'
