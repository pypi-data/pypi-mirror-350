#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `seamm_ff_util` package."""

import json
import seamm_ff_util  # noqa: F401


def test_bond_angle_explicit(pcff):
    """Test of bond_angle parameters, which should fine explicit ones"""

    expected = {
        "reference": "1",
        "K12": "20.7540",
        "original K12": "20.7540",
        "K23": "11.4210",
        "original K23": "11.4210",
        "R10": "1.5300",
        "R20": "1.1010",
    }

    i = "c"
    j = "c"
    k = "h"
    ptype, key, form, parameters = pcff.bond_angle_parameters(i, j, k)
    assert ptype == "explicit"
    assert key == ("c", "c", "h")
    if parameters != expected:
        print(json.dumps(parameters, indent=4))
    assert parameters == expected


def test_bond_angle_explicit_kji(pcff):
    """known bond_angle parameters, ordered backwards"""

    expected = {
        "K12": "11.4210",
        "K23": "20.7540",
        "reference": "1",
        "R10": "1.5300",
        "R20": "1.1010",
    }
    i = "h"
    j = "c"
    k = "c"
    ptype, key, form, parameters = pcff.bond_angle_parameters(i, j, k)
    assert ptype == "explicit"
    assert key == ("h", "c", "c")
    assert parameters == expected


def test_bond_angle_equivalent(pcff):
    """Simple test of bond_angle parameters using equivalencies"""
    expected = {
        "reference": "1",
        "K12": "20.7540",
        "original K12": "20.7540",
        "K23": "11.4210",
        "original K23": "11.4210",
        "R10": "1.5300",
        "R20": "1.1010",
    }

    i = "c"
    j = "c1"
    k = "h"
    ptype, key, form, parameters = pcff.bond_angle_parameters(i, j, k)
    assert ptype == "equivalent"
    assert key == ("c", "c", "h")
    if parameters != expected:
        print(json.dumps(parameters, indent=4))
    assert parameters == expected
