#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `seamm_ff_util` package."""

import json
import seamm_ff_util  # noqa: F401


def test_end_bond_torsion_3_explicit(pcff):
    """Test of end_bond_torsion_3 parameters, which should find
    explicit ones"""

    expected = {
        "V1_L": "0.0870",
        "V1_R": "0.2217",
        "V2_L": "0.5143",
        "V2_R": "0.4780",
        "V3_L": "-0.2448",
        "V3_R": "-0.0817",
        "reference": "1",
        "R0_L": "1.5140",
        "R0_R": "1.1010",
    }

    i = "h"
    j = "c"
    k = "c"
    l = "c_0"  # noqa: E741
    ptype, key, form, parameters = pcff.end_bond_torsion_3_parameters(i, j, k, l)
    assert ptype == "explicit"
    assert key == ("h", "c", "c", "c_0")
    if parameters != expected:
        print(json.dumps(parameters, indent=4))
    assert parameters == expected


def test_end_bond_torsion_3_explicit_kji(pcff):
    """known end_bond_torsion_3 parameters, ordered backwards"""

    expected = {
        "reference": "1",
        "V1_L": "0.2217",
        "original V1_L": "0.2217",
        "V2_L": "0.4780",
        "original V2_L": "0.4780",
        "V3_L": "-0.0817",
        "original V3_L": "-0.0817",
        "V1_R": "0.0870",
        "original V1_R": "0.0870",
        "V2_R": "0.5143",
        "original V2_R": "0.5143",
        "V3_R": "-0.2448",
        "original V3_R": "-0.2448",
        "R0_L": "1.5140",
        "R0_R": "1.1010",
    }

    i = "c_0"
    j = "c"
    k = "c"
    l = "h"  # noqa: E741
    ptype, key, form, parameters = pcff.end_bond_torsion_3_parameters(i, j, k, l)
    assert ptype == "explicit"
    assert key == ("c_0", "c", "c", "h")
    if parameters != expected:
        print(json.dumps(parameters, indent=4))
    assert parameters == expected


def test_end_bond_torsion_3_equivalent(pcff):
    """Simple test of end_bond_torsion_3 parameters using equivalencies"""
    expected = {
        "reference": "1",
        "V1_L": "1.3997",
        "original V1_L": "1.3997",
        "V2_L": "0.7756",
        "original V2_L": "0.7756",
        "V3_L": "0.0000",
        "original V3_L": "0.0000",
        "V1_R": "-0.5835",
        "original V1_R": "-0.5835",
        "V2_R": "1.1220",
        "original V2_R": "1.1220",
        "V3_R": "0.3978",
        "original V3_R": "0.3978",
        "R0_L": "1.1010",
        "R0_R": "1.4170",
    }

    i = "h"
    j = "c"
    k = "c5"
    l = "c5"  # noqa: E741
    ptype, key, form, parameters = pcff.end_bond_torsion_3_parameters(i, j, k, l)
    assert ptype == "equivalent"
    assert key == ("h", "c", "cp", "cp")
    if parameters != expected:
        print(json.dumps(parameters, indent=4))
    assert parameters == expected
