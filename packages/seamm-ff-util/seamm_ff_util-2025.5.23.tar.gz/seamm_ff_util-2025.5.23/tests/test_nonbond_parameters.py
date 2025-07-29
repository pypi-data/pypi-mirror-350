#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `seamm_ff_util` package."""

import json
import seamm_ff_util  # noqa: F401


def test_nonbond_explicit(pcff):
    """Simple test of known nonbond parameters"""
    expected = {
        "reference": "1",
        "rmin": 2.995,
        "eps": 0.02,
        "original rmin": "2.9950",
        "original eps": "0.02000",
    }

    i = "h"
    ptype, key, form, parameters = pcff.nonbond_parameters(i, form="nonbond(9-6)")
    assert ptype == "explicit"
    assert key == ("h",)
    if parameters != expected:
        print(json.dumps(parameters, indent=4))
    assert parameters == expected


def test_nonbond_equivalent(pcff):
    """Simple test of nonbond parameters using equivalencies"""
    expected = {
        "reference": "1",
        "rmin": 4.01,
        "eps": 0.064,
        "original rmin": "4.0100",
        "original eps": "0.06400",
    }

    i = "c5"
    ptype, key, form, parameters = pcff.nonbond_parameters(i, form="nonbond(9-6)")
    assert ptype == "equivalent"
    assert key == ("cp",)
    if parameters != expected:
        print(json.dumps(parameters, indent=4))
    assert parameters == expected
