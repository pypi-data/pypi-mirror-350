#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `seamm_ff_util` package."""

import json
import seamm_ff_util  # noqa: F401


def test_oop_explicit(pcff):
    """Test of out-of-plane parameters, which should find explicit ones"""

    expected = {
        "reference": "1",
        "K": "10.8102",
        "original K": "10.8102",
        "Chi0": "0.0000",
        "original Chi0": "0.0000",
    }

    i = "h"
    j = "cp"
    k = "np"
    l = "op"  # noqa: E741
    ptype, key, form, parameters = pcff.oop_parameters(i, j, k, l)
    assert ptype == "explicit"
    assert key == ("h", "cp", "np", "op")
    if parameters != expected:
        print(json.dumps(parameters, indent=4))
    assert parameters == expected


def test_oop_explicit_lkji(pcff):
    """known out-of-plane parameters, ordered backwards"""
    i = "h"
    j = "cp"
    k = "np"
    l = "op"  # noqa: E741
    ptype, key, form, parameters = pcff.oop_parameters(i, j, k, l)
    ptype2, key2, form, parameters2 = pcff.oop_parameters(l, j, k, i)
    assert ptype2 == "explicit"
    assert key == ("h", "cp", "np", "op")
    assert parameters == parameters2


def test_oop_equivalent(pcff):
    """Simple test of out-of-plane parameters using equivalencies"""
    expected = {
        "reference": "1",
        "K": "10.8102",
        "original K": "10.8102",
        "Chi0": "0.0000",
        "original Chi0": "0.0000",
    }

    i = "hp"
    j = "c5"
    k = "np"
    l = "op"  # noqa: E741
    ptype, key, form, parameters = pcff.oop_parameters(i, j, k, l)
    assert ptype == "equivalent"
    assert key == ("h", "cp", "np", "op")
    if parameters != expected:
        print(json.dumps(parameters, indent=4))
    assert parameters == expected


def test_oop_auto(pcff):
    """test of out-of-plane parameters using automatic parameters"""
    expected = {
        "reference": "1",
        "K": "36.0000",
        "original K": "36.0000",
        "Chi0": "0.0000",
        "original Chi0": "0.0000",
    }

    i = "hp"
    j = "c_0"
    k = "co"
    l = "br"  # noqa: E741
    ptype, key, form, parameters = pcff.oop_parameters(i, j, k, l)
    assert ptype == "automatic"
    assert key == ("*", "c'_", "*", "*")
    if parameters != expected:
        print(json.dumps(parameters, indent=4))
    assert parameters == expected
