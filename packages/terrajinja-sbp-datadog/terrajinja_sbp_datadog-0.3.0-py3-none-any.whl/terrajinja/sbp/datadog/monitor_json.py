from cdktf_cdktf_provider_datadog.monitor_json import MonitorJson
from constructs import Construct
import json
import re


def replace_template_variables(data, variables):
    if isinstance(data, dict):
        return {k: replace_template_variables(v, variables) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_template_variables(i, variables) for i in data]
    elif isinstance(data, str):
        for k, v in variables.items():
            data = data.replace(f"%% {k} %%", str(v))
        return data
    return data


def validate_no_placeholders(data):
    json_str = json.dumps(data)
    if re.search(r"%%\s*[\w\.]+\s*%%", json_str):
        raise ValueError(f"Unresolved placeholders found in JSON: {json_str}")


class SbpDatadogMonitorJson(MonitorJson):
    def __init__(self, scope: Construct, ns: str, monitor: str, template_variables: dict = None):
        # Parse monitor from JSON string
        monitor_dict = json.loads(monitor)

        # Replace placeholders
        if template_variables:
            monitor_dict = replace_template_variables(monitor, template_variables)
            validate_no_placeholders(monitor_dict)

        # Pass dict into the superclass
        super().__init__(scope=scope, id_=ns, monitor=monitor_dict)
