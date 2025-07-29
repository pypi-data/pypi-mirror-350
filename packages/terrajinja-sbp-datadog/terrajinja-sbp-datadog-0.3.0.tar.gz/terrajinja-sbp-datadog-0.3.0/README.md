# terrajinja-sbp-datadog

This is an extension to the datadog provider for the following modules.
The original documentation can be found [here](https://registry.terraform.io/providers/hashicorp/datadog/latest/docs)

# SBP Specific implementations
Here is a list of supported resources and their modifications

## sbp.datadog.synthetics_test_json
Original provider: [datadog.synthetics_test](https://registry.terraform.io/providers/hashicorp/datadog/latest/docs/resources/synthetics_test)

This custom provider adds the following:
- accepts json as input for synthetics_test

### terrajinja-cli example
the following is a code snipet you can used in a terrajinja-cli template file.
This creates a s3 policy

```
terraform:
  resources:
    - task: "s3-policy"
      module: sbp.aws.iam_user_policy
      synthetic_test: '{json object}'
```

