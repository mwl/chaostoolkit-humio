# -*- coding: utf-8 -*-
from datetime import datetime, timezone
import time
import types
from unittest.mock import MagicMock, patch

from chaoslib.notification import RunFlowEvent
import pytest
import requests
import requests_mock

from chaoshumio.notification import notify


def test_notify():
    payload = {
        "msg": "hello"
    }
    timestamp = time.time()
    isotimestamp = datetime.fromtimestamp(timestamp, timezone.utc).isoformat()

    event_payload = {
        "ts": timestamp,
        "event": str(RunFlowEvent.RunStarted),
        "phase": "run",
        "payload": payload
    }
    with requests_mock.mock() as m:
        m.post(
            'https://cloud.humio.com/api/v1/dataspaces/my-space/ingest',
            status_code=200,
            json=[ { 
                "tags": {
                    "host": "fake-host"
                },
                "events": [
                    {
                        "timestamp": isotimestamp,
                        "attributes": payload
                    },
                ]
            } ]
        )

        notify(
            {
                "token": "my-token",
                "dataspace": "my-space"
            },
            event_payload
        )

        assert m.called
