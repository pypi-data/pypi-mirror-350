import random

import pytest
from cdktf import Testing

from src.terrajinja.sbp.datadog.synthetics_test_json import SbpDatadogSyntheticsTestJson
from .helper import stack, has_resource, has_resource_path_value, has_resource_path_value_not_contain


class TestSbpVault:
    def test_json_formatting(self, stack):
        SbpDatadogSyntheticsTestJson(
            scope=stack,
            ns="sbp_synthetic_test",
            synthetic_test="""
                {
                  "created_at": "2024-07-11T11:57:29.225050+00:00",
                  "modified_at": "2024-07-11T11:57:29.225050+00:00",
                  "config": {
                    "assertions": [
                      {
                        "operator": "doesNotContain",
                        "target": "Sign in",
                        "type": "body"
                      },
                      {
                        "operator": "is",
                        "target": 403.0,
                        "type": "statusCode"
                      }
                    ],
                    "config_variables": [],
                    "request": {
                      "headers": {
                        "x-test": "testheader"
                      },
                      "method": "GET",
                      "timeout": 60.0,
                      "url": "https://dummy.url"
                    }
                  },
                  "creator": {
                    "email": "me@email.com",
                    "handle": "me@email.com",
                    "name": "Me"
                  },
                  "locations": [
                    "aws:eu-central-1",
                    "aws:eu-west-1",
                    "aws:eu-west-3"
                  ],
                  "message": "If this alerts, then the portal is available to the public, this should never happen.",
                  "monitor_id": 17982913,
                  "name": "[dummy] portal is shielded from public access",
                  "options": {
                    "allow_insecure": true,
                    "http_version": "any",
                    "min_location_failed": 3,
                    "monitor_name": "[dummy] portal is shielded from public access",
                    "retry": {
                      "count": 3,
                      "interval": 1000.0
                    },
                    "tick_every": 3600
                  },
                  "public_id": "g58-cai-zmf",
                  "status": "live",
                  "subtype": "http",
                  "tags": [
                    "env: test"
                  ],
                  "type": "api"
                }
            """,
        )

        synthesized = Testing.synth(stack)
        print(synthesized)

        assert synthesized == """{
  "resource": {
    "datadog_synthetics_test": {
      "sbp_synthetic_test": {
        "assertion": [
          {
            "operator": "doesNotContain",
            "target": "Sign in",
            "type": "body"
          },
          {
            "operator": "is",
            "target": "403",
            "type": "statusCode"
          }
        ],
        "locations": [
          "aws:eu-central-1",
          "aws:eu-west-1",
          "aws:eu-west-3"
        ],
        "message": "If this alerts, then the portal is available to the public, this should never happen.",
        "name": "[dummy] portal is shielded from public access",
        "options_list": {
          "allow_insecure": true,
          "http_version": "any",
          "min_location_failed": 3,
          "monitor_name": "[dummy] portal is shielded from public access",
          "retry": {
            "count": 3,
            "interval": 1000
          },
          "tick_every": 3600
        },
        "request_definition": {
          "method": "GET",
          "timeout": 60,
          "url": "https://dummy.url"
        },
        "request_headers": {
          "x-test": "testheader"
        },
        "status": "live",
        "subtype": "http",
        "tags": [
          "env: test"
        ],
        "type": "api"
      }
    }
  }
}"""



if __name__ == "__main__":
    pytest.main()
