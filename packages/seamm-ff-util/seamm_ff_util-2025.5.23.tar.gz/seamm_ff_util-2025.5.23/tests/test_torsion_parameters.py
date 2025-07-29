#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `seamm_ff_util` package."""

import json
import seamm_ff_util  # noqa: F401


def test_torsion_explicit(pcff):
    """Test of torsion parameters, which should find explicit ones"""

    expected = {
        "reference": "8",
        "V1": "0.0000",
        "original V1": "0.0000",
        "Phi0_1": "0.0",
        "original Phi0_1": "0.0",
        "V2": "0.0000",
        "original V2": "0.0000",
        "Phi0_2": "0.0",
        "original Phi0_2": "0.0",
        "V3": "-0.2000",
        "original V3": "-0.2000",
        "Phi0_3": "0.0",
        "original Phi0_3": "0.0",
    }

    i = "h"
    j = "c"
    k = "c"
    l = "br"  # noqa: E741
    ptype, key, form, parameters = pcff.torsion_parameters(i, j, k, l)
    assert ptype == "explicit"
    assert key == ("br", "c", "c", "h")
    if parameters != expected:
        print(json.dumps(parameters, indent=4))
    assert parameters == expected


def test_torsion_explicit_lkji(pcff):
    """known torsion parameters, ordered backwards"""
    i = "h"
    j = "c"
    k = "c"
    l = "br"  # noqa: E741
    ptype, key, form, parameters = pcff.torsion_parameters(i, j, k, l)
    ptype2, key2, form, parameters2 = pcff.torsion_parameters(l, k, j, i)
    assert ptype2 == "explicit"
    assert key2 == ("br", "c", "c", "h")
    assert parameters == parameters2


def test_torsion_equivalent(pcff):
    """Simple test of torsion parameters using equivalencies"""
    expected = {
        "reference": "1",
        "V1": "0.0000",
        "original V1": "0.0000",
        "Phi0_1": "0.0",
        "original Phi0_1": "0.0",
        "V2": "1.8769",
        "original V2": "1.8769",
        "Phi0_2": "0.0",
        "original Phi0_2": "0.0",
        "V3": "0.0000",
        "original V3": "0.0000",
        "Phi0_3": "0.0",
        "original Phi0_3": "0.0",
    }

    i = "hp"
    j = "c5"
    k = "c5"
    l = "hp"  # noqa: E741
    ptype, key, form, parameters = pcff.torsion_parameters(i, j, k, l)
    assert ptype == "equivalent"
    assert key == ("h", "cp", "cp", "h")
    if parameters != expected:
        print(json.dumps(parameters, indent=4))
    assert parameters == expected


def test_torsion_auto(pcff):
    """test of torsion parameters using automatic parameters"""
    expected = {
        "reference": "2",
        "KPhi": "3.0000",
        "original KPhi": "3.0000",
        "n": "2",
        "original n": "2",
        "Phi0": "180.0000",
        "original Phi0": "180.0000",
    }

    i = "hp"
    j = "c5"
    k = "c5"
    l = "br"  # noqa: E741
    ptype, key, form, parameters = pcff.torsion_parameters(i, j, k, l)
    assert ptype == "automatic"
    assert key == ("*", "cp_", "cp_", "*")
    if parameters != expected:
        print(json.dumps(parameters, indent=4))
    assert parameters == expected
