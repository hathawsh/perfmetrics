#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

from hamcrest.core.matcher import Matcher
from hamcrest.core.base_matcher import BaseMatcher

from hamcrest import all_of
from hamcrest import instance_of
from hamcrest import is_
from hamcrest import has_properties
from hamcrest import none

from .observation import OBSERVATION_KIND_COUNTER as METRIC_COUNTER_KIND
from .observation import OBSERVATION_KIND_GAUGE as METRIC_GAUGE_KIND
from .observation import OBSERVATION_KIND_SET as METRIC_SET_KIND
from .observation import OBSERVATION_KIND_TIMER as METRIC_TIMER_KIND

from .observation import Observation

__all__ = [
    'is_observation',
    'is_counter',
    'is_gauge',
    'is_set',
    'is_timer',
]

_marker = object()

_metric_kind_display_name = {
    'c': 'counter',
    'g': 'gauge',
    'ms': 'timer',
    's': 'set'
}

class IsMetric(BaseMatcher):

    def __init__(self, kwargs):
        matchers = {}
        for key, value in kwargs.items():
            if value is None:
                value = none()
            elif key == 'sampling_rate':
                # This one is special, it doesn't get
                # to be a string, it's kept as a number.
                value = is_(value)
            elif not isinstance(value, Matcher):
                value = str(value)
            matchers[key] = value

        self._matcher = all_of(
            instance_of(Observation),
            has_properties(**matchers)
        )

    def _matches(self, item):
        return self._matcher.matches(item)

    def describe_to(self, description):
        self._matcher.describe_to(description)

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append_text('was ').append_text(repr(item))

def _is_metric(args, kwargs):
    for arg_ix, name in enumerate((
            'kind',
            'name',
            'value',
            'sampling_rate'
    )):
        if name in kwargs or len(args) <= arg_ix:
            continue
        kwargs[name] = args[arg_ix]

    return IsMetric(kwargs)


def is_observation(*args, **kwargs):
    """
    is_observation(*, kind, name, value, sampling_rate) -> matcher

    A hamcrest matcher that validates the specific parts of a `~.Observation`.
    All arguments are optional and can be provided by name or position.

    :keyword str kind: A hamcrest matcher or string that matches the kind for this metric
    :keyword str name: A hamcrest matcher or string that matches the name for this metric
    :keyword str value: A hamcrest matcher or string that matches the value for this metric
    :keyword float sampling_rate: A hamcrest matcher or
        number that matches the sampling rate this metric was collected with
    """
    return _is_metric(args, kwargs)


def is_counter(*args, **kwargs):
    """
    is_counter(*, name, value, sampling_rate) -> matcher

    A hamcrest matcher validating the parts of a counter `~.Observation`.

    .. seealso:: `is_metric`
    """
    kwargs['kind'] = METRIC_COUNTER_KIND
    args = (None,) + args
    return _is_metric(args, kwargs)


def is_gauge(*args, **kwargs):
    """
    is_gauge(*, name, value, sampling_rate) -> matcher

    A hamcrest matcher validating the parts of a gauge `~.Observation`

    .. seealso:: `is_metric`
    """
    kwargs['kind'] = METRIC_GAUGE_KIND
    args = (None,) + args
    return _is_metric(args, kwargs)


def is_timer(*args, **kwargs):
    """
    is_timer(*, name, value, sampling_rate) -> matcher

    A hamcrest matcher validating the parts of a timer `~.Observation`

    .. seealso:: `is_metric`
    """
    kwargs['kind'] = METRIC_TIMER_KIND
    args = (None,) + args
    return _is_metric(args, kwargs)

def is_set(*args, **kwargs):
    """
    is_set(*, name, value, sampling_rate) -> matcher

    A hamcrest matcher validating the parts of a set `~.Observation`

    .. seealso:: `is_metric`
    """
    kwargs['kind'] = METRIC_SET_KIND
    args = (None,) + args
    return _is_metric(args, kwargs)
