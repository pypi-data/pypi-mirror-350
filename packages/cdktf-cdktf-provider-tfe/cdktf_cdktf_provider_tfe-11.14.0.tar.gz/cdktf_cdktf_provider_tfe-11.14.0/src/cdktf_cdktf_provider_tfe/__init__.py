r'''
# CDKTF prebuilt bindings for hashicorp/tfe provider version 0.66.0

This repo builds and publishes the [Terraform tfe provider](https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs) bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-tfe](https://www.npmjs.com/package/@cdktf/provider-tfe).

`npm install @cdktf/provider-tfe`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-tfe](https://pypi.org/project/cdktf-cdktf-provider-tfe).

`pipenv install cdktf-cdktf-provider-tfe`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Tfe](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Tfe).

`dotnet add package HashiCorp.Cdktf.Providers.Tfe`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-tfe](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-tfe).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-tfe</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-tfe-go`](https://github.com/cdktf/cdktf-provider-tfe-go) package.

`go get github.com/cdktf/cdktf-provider-tfe-go/tfe/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktf/cdktf-provider-tfe-go/blob/main/tfe/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-tfe).

## Versioning

This project is explicitly not tracking the Terraform tfe provider version 1:1. In fact, it always tracks `latest` of `~> 0.33` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by [generating the provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [CDK for Terraform](https://cdk.tf)
* [Terraform tfe provider](https://registry.terraform.io/providers/hashicorp/tfe/0.66.0)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped.

## Features / Issues / Bugs

Please report bugs and issues to the [CDK for Terraform](https://cdk.tf) project:

* [Create bug report](https://cdk.tf/bug)
* [Create feature request](https://cdk.tf/feature)

## Contributing

### Projen

This is mostly based on [Projen](https://github.com/projen/projen), which takes care of generating the entire repository.

### cdktf-provider-project based on Projen

There's a custom [project builder](https://github.com/cdktf/cdktf-provider-project) which encapsulate the common settings for all `cdktf` prebuilt providers.

### Provider Version

The provider version can be adjusted in [./.projenrc.js](./.projenrc.js).

### Repository Management

The repository is managed by [CDKTF Repository Manager](https://github.com/cdktf/cdktf-repository-manager/).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

__all__ = [
    "admin_organization_settings",
    "agent_pool",
    "agent_pool_allowed_workspaces",
    "agent_token",
    "audit_trail_token",
    "data_retention_policy",
    "data_tfe_agent_pool",
    "data_tfe_github_app_installation",
    "data_tfe_ip_ranges",
    "data_tfe_no_code_module",
    "data_tfe_oauth_client",
    "data_tfe_organization",
    "data_tfe_organization_members",
    "data_tfe_organization_membership",
    "data_tfe_organization_run_task",
    "data_tfe_organization_run_task_global_settings",
    "data_tfe_organization_tags",
    "data_tfe_organizations",
    "data_tfe_outputs",
    "data_tfe_policy_set",
    "data_tfe_project",
    "data_tfe_projects",
    "data_tfe_registry_gpg_key",
    "data_tfe_registry_gpg_keys",
    "data_tfe_registry_module",
    "data_tfe_registry_provider",
    "data_tfe_registry_providers",
    "data_tfe_saml_settings",
    "data_tfe_slug",
    "data_tfe_ssh_key",
    "data_tfe_team",
    "data_tfe_team_access",
    "data_tfe_team_project_access",
    "data_tfe_teams",
    "data_tfe_variable_set",
    "data_tfe_variables",
    "data_tfe_workspace",
    "data_tfe_workspace_ids",
    "data_tfe_workspace_run_task",
    "no_code_module",
    "notification_configuration",
    "oauth_client",
    "opa_version",
    "organization",
    "organization_default_settings",
    "organization_membership",
    "organization_module_sharing",
    "organization_run_task",
    "organization_run_task_global_settings",
    "organization_token",
    "policy",
    "policy_set",
    "policy_set_parameter",
    "project",
    "project_oauth_client",
    "project_policy_set",
    "project_variable_set",
    "provider",
    "registry_gpg_key",
    "registry_module",
    "registry_provider",
    "run_trigger",
    "saml_settings",
    "sentinel_policy",
    "sentinel_version",
    "ssh_key",
    "stack",
    "team",
    "team_access",
    "team_member",
    "team_members",
    "team_notification_configuration",
    "team_organization_member",
    "team_organization_members",
    "team_project_access",
    "team_token",
    "terraform_version",
    "test_variable",
    "variable",
    "variable_set",
    "workspace",
    "workspace_policy_set",
    "workspace_policy_set_exclusion",
    "workspace_run",
    "workspace_run_task",
    "workspace_settings",
    "workspace_variable_set",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import admin_organization_settings
from . import agent_pool
from . import agent_pool_allowed_workspaces
from . import agent_token
from . import audit_trail_token
from . import data_retention_policy
from . import data_tfe_agent_pool
from . import data_tfe_github_app_installation
from . import data_tfe_ip_ranges
from . import data_tfe_no_code_module
from . import data_tfe_oauth_client
from . import data_tfe_organization
from . import data_tfe_organization_members
from . import data_tfe_organization_membership
from . import data_tfe_organization_run_task
from . import data_tfe_organization_run_task_global_settings
from . import data_tfe_organization_tags
from . import data_tfe_organizations
from . import data_tfe_outputs
from . import data_tfe_policy_set
from . import data_tfe_project
from . import data_tfe_projects
from . import data_tfe_registry_gpg_key
from . import data_tfe_registry_gpg_keys
from . import data_tfe_registry_module
from . import data_tfe_registry_provider
from . import data_tfe_registry_providers
from . import data_tfe_saml_settings
from . import data_tfe_slug
from . import data_tfe_ssh_key
from . import data_tfe_team
from . import data_tfe_team_access
from . import data_tfe_team_project_access
from . import data_tfe_teams
from . import data_tfe_variable_set
from . import data_tfe_variables
from . import data_tfe_workspace
from . import data_tfe_workspace_ids
from . import data_tfe_workspace_run_task
from . import no_code_module
from . import notification_configuration
from . import oauth_client
from . import opa_version
from . import organization
from . import organization_default_settings
from . import organization_membership
from . import organization_module_sharing
from . import organization_run_task
from . import organization_run_task_global_settings
from . import organization_token
from . import policy
from . import policy_set
from . import policy_set_parameter
from . import project
from . import project_oauth_client
from . import project_policy_set
from . import project_variable_set
from . import provider
from . import registry_gpg_key
from . import registry_module
from . import registry_provider
from . import run_trigger
from . import saml_settings
from . import sentinel_policy
from . import sentinel_version
from . import ssh_key
from . import stack
from . import team
from . import team_access
from . import team_member
from . import team_members
from . import team_notification_configuration
from . import team_organization_member
from . import team_organization_members
from . import team_project_access
from . import team_token
from . import terraform_version
from . import test_variable
from . import variable
from . import variable_set
from . import workspace
from . import workspace_policy_set
from . import workspace_policy_set_exclusion
from . import workspace_run
from . import workspace_run_task
from . import workspace_settings
from . import workspace_variable_set
