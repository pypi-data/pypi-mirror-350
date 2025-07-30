from __future__ import annotations

from enum import Enum


class S3StoreEnv(Enum):
    """
    S3Store environment
    """

    ENDPOINT_URL = "AWS_ENDPOINT_URL"
    ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
    SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
    SESSION_TOKEN = "AWS_SESSION_TOKEN"
    REGION = "AWS_REGION"
    SIGNATURE_VERSION = "S3_SIGNATURE_VERSION"
