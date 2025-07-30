# -*- coding: utf-8 -*-

from enum_mate.api import BetterIntEnum, BetterStrEnum


class CodeEnum(BetterIntEnum):
    succeeded = 200
    failed = 404


class StatusEnum(BetterStrEnum):
    succeeded = "SUCCEEDED"
    failed = "FAILED"
