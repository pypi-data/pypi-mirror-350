import json
import re

from cdktf_cdktf_provider_datadog.synthetics_test import SyntheticsTest
from constructs import Construct


def replace_template_variables(data: dict, variables: dict) -> dict:
    """
    Recursively replaces placeholders in dictionary values using provided variables.

    Args:
        data (dict): Dictionary to process.
        variables (dict): Mapping of placeholder names to values.

    Returns:
        dict: Updated dictionary with replaced values.
    """
    if isinstance(data, dict):
        return {key: replace_template_variables(value, variables) for key, value in data.items()}
    elif isinstance(data, list):
        return [replace_template_variables(item, variables) for item in data]
    elif isinstance(data, str):
        for key, value in variables.items():
            data = data.replace(f"{{{{ {key} }}}}", str(value))
        return data
    return data


def validate_no_placeholders(data: dict):
    """
    Validates that there are no unresolved placeholders in the dictionary.

    Args:
        data (dict): Processed dictionary.

    Raises:
        ValueError: If unresolved placeholders are found.
    """
    json_str = json.dumps(data)
    if re.search(r"\{\{.*?\}\}", json_str):
        raise ValueError(f"Unresolved placeholders found in JSON: {json_str}")


def dict_to_terraform(synthetic: dict) -> dict:
    # converts the synthetic to a terraform dict
    config = synthetic.get('config')
    if config:
        del synthetic['config']

        # config.assertions is assertions
        synthetic['assertion'] = config.get('assertions')

        # convert assertion target to string if it is an int
        for assertion in synthetic['assertion']:
            if isinstance(assertion['target'], (int, float)):
                # ensure status code has no decimal
                if assertion['type'] == 'statusCode':
                    assertion['target'] = "%.0f" % (assertion['target'])
                else:
                    # ensure target is a string
                    assertion['target'] = str(assertion['target'])

        # config.request is request_headers + request_definitions
        request = config.get('request')
        if request:
            synthetic['request_headers'] = request.get('headers')
            request.pop('headers', None)
            synthetic['request_definition'] = request

    name = synthetic.get('name')

    # these fields are not in the terraform resource
    synthetic.pop('created_at', None)
    synthetic.pop('modified_at', None)
    synthetic.pop('creator', None)
    synthetic.pop('monitor_id', None)
    synthetic.pop('public_id', None)

    options = synthetic.get('options')
    if options:
        del synthetic['options']

        # ensure monitor name is same as check name for consistency
        options['monitor_name'] = name

        # bindings is not an option in the terraform resource
        options.pop('bindings', None)

        monitor_options = options.get('monitor_options')
        if monitor_options:
            # this is not an option in the terraform resource
            monitor_options.pop('notification_preset_name', None)
            options['monitor_options'] = monitor_options

        # options should be options_list
        synthetic['options_list'] = options

    return synthetic


class SbpDatadogSyntheticsTestJson(SyntheticsTest):
    """Custom Datadog Synthetic Test with Template Variable Support"""

    def __init__(self, scope: Construct, ns: str, synthetic_test: str, template_variables: dict = None, **kwargs):
        """
        Custom Datadog Synthetics Test constructor.

        Args:
            scope (Construct): Cdktf App
            ns (str): Unique name of the resource
            synthetic_test (str): JSON string specifying the synthetic test
            template_variables (dict, optional): Template variables to replace placeholders
        """
        # Load the JSON test definition
        synthetic_dict = json.loads(synthetic_test)

        # Replace template variables if provided
        if template_variables:
            synthetic_dict = replace_template_variables(synthetic_dict, template_variables)
            validate_no_placeholders(synthetic_dict)

        # Convert to Terraform format
        terraform_ready_dict = dict_to_terraform(synthetic_dict)

        # Pass processed data to the Terraform provider
        super().__init__(scope=scope, id_=ns, **terraform_ready_dict)
