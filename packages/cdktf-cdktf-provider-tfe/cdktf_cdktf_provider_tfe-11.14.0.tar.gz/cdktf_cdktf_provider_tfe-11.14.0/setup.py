import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-tfe",
    "version": "11.14.0",
    "description": "Prebuilt tfe Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktf/cdktf-provider-tfe.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktf/cdktf-provider-tfe.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_tfe",
        "cdktf_cdktf_provider_tfe._jsii",
        "cdktf_cdktf_provider_tfe.admin_organization_settings",
        "cdktf_cdktf_provider_tfe.agent_pool",
        "cdktf_cdktf_provider_tfe.agent_pool_allowed_workspaces",
        "cdktf_cdktf_provider_tfe.agent_token",
        "cdktf_cdktf_provider_tfe.audit_trail_token",
        "cdktf_cdktf_provider_tfe.data_retention_policy",
        "cdktf_cdktf_provider_tfe.data_tfe_agent_pool",
        "cdktf_cdktf_provider_tfe.data_tfe_github_app_installation",
        "cdktf_cdktf_provider_tfe.data_tfe_ip_ranges",
        "cdktf_cdktf_provider_tfe.data_tfe_no_code_module",
        "cdktf_cdktf_provider_tfe.data_tfe_oauth_client",
        "cdktf_cdktf_provider_tfe.data_tfe_organization",
        "cdktf_cdktf_provider_tfe.data_tfe_organization_members",
        "cdktf_cdktf_provider_tfe.data_tfe_organization_membership",
        "cdktf_cdktf_provider_tfe.data_tfe_organization_run_task",
        "cdktf_cdktf_provider_tfe.data_tfe_organization_run_task_global_settings",
        "cdktf_cdktf_provider_tfe.data_tfe_organization_tags",
        "cdktf_cdktf_provider_tfe.data_tfe_organizations",
        "cdktf_cdktf_provider_tfe.data_tfe_outputs",
        "cdktf_cdktf_provider_tfe.data_tfe_policy_set",
        "cdktf_cdktf_provider_tfe.data_tfe_project",
        "cdktf_cdktf_provider_tfe.data_tfe_projects",
        "cdktf_cdktf_provider_tfe.data_tfe_registry_gpg_key",
        "cdktf_cdktf_provider_tfe.data_tfe_registry_gpg_keys",
        "cdktf_cdktf_provider_tfe.data_tfe_registry_module",
        "cdktf_cdktf_provider_tfe.data_tfe_registry_provider",
        "cdktf_cdktf_provider_tfe.data_tfe_registry_providers",
        "cdktf_cdktf_provider_tfe.data_tfe_saml_settings",
        "cdktf_cdktf_provider_tfe.data_tfe_slug",
        "cdktf_cdktf_provider_tfe.data_tfe_ssh_key",
        "cdktf_cdktf_provider_tfe.data_tfe_team",
        "cdktf_cdktf_provider_tfe.data_tfe_team_access",
        "cdktf_cdktf_provider_tfe.data_tfe_team_project_access",
        "cdktf_cdktf_provider_tfe.data_tfe_teams",
        "cdktf_cdktf_provider_tfe.data_tfe_variable_set",
        "cdktf_cdktf_provider_tfe.data_tfe_variables",
        "cdktf_cdktf_provider_tfe.data_tfe_workspace",
        "cdktf_cdktf_provider_tfe.data_tfe_workspace_ids",
        "cdktf_cdktf_provider_tfe.data_tfe_workspace_run_task",
        "cdktf_cdktf_provider_tfe.no_code_module",
        "cdktf_cdktf_provider_tfe.notification_configuration",
        "cdktf_cdktf_provider_tfe.oauth_client",
        "cdktf_cdktf_provider_tfe.opa_version",
        "cdktf_cdktf_provider_tfe.organization",
        "cdktf_cdktf_provider_tfe.organization_default_settings",
        "cdktf_cdktf_provider_tfe.organization_membership",
        "cdktf_cdktf_provider_tfe.organization_module_sharing",
        "cdktf_cdktf_provider_tfe.organization_run_task",
        "cdktf_cdktf_provider_tfe.organization_run_task_global_settings",
        "cdktf_cdktf_provider_tfe.organization_token",
        "cdktf_cdktf_provider_tfe.policy",
        "cdktf_cdktf_provider_tfe.policy_set",
        "cdktf_cdktf_provider_tfe.policy_set_parameter",
        "cdktf_cdktf_provider_tfe.project",
        "cdktf_cdktf_provider_tfe.project_oauth_client",
        "cdktf_cdktf_provider_tfe.project_policy_set",
        "cdktf_cdktf_provider_tfe.project_variable_set",
        "cdktf_cdktf_provider_tfe.provider",
        "cdktf_cdktf_provider_tfe.registry_gpg_key",
        "cdktf_cdktf_provider_tfe.registry_module",
        "cdktf_cdktf_provider_tfe.registry_provider",
        "cdktf_cdktf_provider_tfe.run_trigger",
        "cdktf_cdktf_provider_tfe.saml_settings",
        "cdktf_cdktf_provider_tfe.sentinel_policy",
        "cdktf_cdktf_provider_tfe.sentinel_version",
        "cdktf_cdktf_provider_tfe.ssh_key",
        "cdktf_cdktf_provider_tfe.stack",
        "cdktf_cdktf_provider_tfe.team",
        "cdktf_cdktf_provider_tfe.team_access",
        "cdktf_cdktf_provider_tfe.team_member",
        "cdktf_cdktf_provider_tfe.team_members",
        "cdktf_cdktf_provider_tfe.team_notification_configuration",
        "cdktf_cdktf_provider_tfe.team_organization_member",
        "cdktf_cdktf_provider_tfe.team_organization_members",
        "cdktf_cdktf_provider_tfe.team_project_access",
        "cdktf_cdktf_provider_tfe.team_token",
        "cdktf_cdktf_provider_tfe.terraform_version",
        "cdktf_cdktf_provider_tfe.test_variable",
        "cdktf_cdktf_provider_tfe.variable",
        "cdktf_cdktf_provider_tfe.variable_set",
        "cdktf_cdktf_provider_tfe.workspace",
        "cdktf_cdktf_provider_tfe.workspace_policy_set",
        "cdktf_cdktf_provider_tfe.workspace_policy_set_exclusion",
        "cdktf_cdktf_provider_tfe.workspace_run",
        "cdktf_cdktf_provider_tfe.workspace_run_task",
        "cdktf_cdktf_provider_tfe.workspace_settings",
        "cdktf_cdktf_provider_tfe.workspace_variable_set"
    ],
    "package_data": {
        "cdktf_cdktf_provider_tfe._jsii": [
            "provider-tfe@11.14.0.jsii.tgz"
        ],
        "cdktf_cdktf_provider_tfe": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "cdktf>=0.20.0, <0.21.0",
        "constructs>=10.3.0, <11.0.0",
        "jsii>=1.111.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
