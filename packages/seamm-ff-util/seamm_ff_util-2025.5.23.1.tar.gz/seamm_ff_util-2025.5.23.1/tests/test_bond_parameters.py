#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `seamm_ff_util` package."""

import json
import seamm_ff_util  # noqa: F401


def test_bond_explicit(pcff):
    """Simple test of known bond parameters"""
    expected = {
        "reference": "8",
        "R0": "1.1010",
        "original R0": "1.1010",
        "K2": "345.0000",
        "original K2": "345.0000",
        "K3": "-691.8900",
        "original K3": "-691.8900",
        "K4": "844.6000",
        "original K4": "844.6000",
    }

    i = "c"
    j = "h"
    ptype, key, form, parameters = pcff.bond_parameters(i, j)
    assert ptype == "explicit"
    assert key == ("c", "h")
    if parameters != expected:
        print(json.dumps(parameters, indent=4))
    assert parameters == expected


def test_bond_explicit_ji(pcff):
    """Simple test of known bond parameters, ordered backwards"""
    i = "c"
    j = "h"
    ptype, key, form, parameters = pcff.bond_parameters(i, j)
    ptype2, key2, form, parameters2 = pcff.bond_parameters(j, i)
    assert ptype2 == "explicit"
    assert key2 == ("c", "h")
    assert parameters == parameters2


def test_bond_equivalent(pcff):
    """Simple test of bond parameters using equivalencies"""
    expected = {
        "reference": "8",
        "R0": "1.0982",
        "original R0": "1.0982",
        "K2": "372.8251",
        "original K2": "372.8251",
        "K3": "-803.4526",
        "original K3": "-803.4526",
        "K4": "894.3173",
        "original K4": "894.3173",
    }

    i = "c5"
    j = "hp"
    ptype, key, form, parameters = pcff.bond_parameters(i, j)
    assert ptype == "equivalent"
    assert key == ("cp", "h")
    if parameters != expected:
        print(json.dumps(parameters, indent=4))
    assert parameters == expected


def test_bond_auto(pcff):
    """Simple test of bond parameters using automatic parameters"""
    expected = {
        "reference": "2",
        "R0": "1.9200",
        "original R0": "1.9200",
        "K2": "223.6000",
        "original K2": "223.6000",
    }

    i = "c5"
    j = "br"
    ptype, key, form, parameters = pcff.bond_parameters(i, j)
    assert ptype == "automatic"
    assert key == ("br_", "cp_")
    if parameters != expected:
        print(json.dumps(parameters, indent=4))
    assert parameters == expected
