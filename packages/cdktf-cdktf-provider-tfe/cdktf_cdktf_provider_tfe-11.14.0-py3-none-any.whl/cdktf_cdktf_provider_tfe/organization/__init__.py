r'''
# `tfe_organization`

Refer to the Terraform Registry for docs: [`tfe_organization`](https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization).
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

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class Organization(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.organization.Organization",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization tfe_organization}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        email: builtins.str,
        name: builtins.str,
        aggregated_commit_status_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_force_delete_workspaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        assessments_enforced: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        collaborator_auth_policy: typing.Optional[builtins.str] = None,
        cost_estimation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        owners_team_saml_role_id: typing.Optional[builtins.str] = None,
        send_passing_statuses_for_untriggered_speculative_plans: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        session_remember_minutes: typing.Optional[jsii.Number] = None,
        session_timeout_minutes: typing.Optional[jsii.Number] = None,
        speculative_plan_management_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization tfe_organization} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#email Organization#email}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#name Organization#name}.
        :param aggregated_commit_status_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#aggregated_commit_status_enabled Organization#aggregated_commit_status_enabled}.
        :param allow_force_delete_workspaces: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#allow_force_delete_workspaces Organization#allow_force_delete_workspaces}.
        :param assessments_enforced: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#assessments_enforced Organization#assessments_enforced}.
        :param collaborator_auth_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#collaborator_auth_policy Organization#collaborator_auth_policy}.
        :param cost_estimation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#cost_estimation_enabled Organization#cost_estimation_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#id Organization#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param owners_team_saml_role_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#owners_team_saml_role_id Organization#owners_team_saml_role_id}.
        :param send_passing_statuses_for_untriggered_speculative_plans: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#send_passing_statuses_for_untriggered_speculative_plans Organization#send_passing_statuses_for_untriggered_speculative_plans}.
        :param session_remember_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#session_remember_minutes Organization#session_remember_minutes}.
        :param session_timeout_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#session_timeout_minutes Organization#session_timeout_minutes}.
        :param speculative_plan_management_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#speculative_plan_management_enabled Organization#speculative_plan_management_enabled}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6449e3ef9f933e7e0b019cbbc14e996201ef002b68481915160874cc1ccbe29)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OrganizationConfig(
            email=email,
            name=name,
            aggregated_commit_status_enabled=aggregated_commit_status_enabled,
            allow_force_delete_workspaces=allow_force_delete_workspaces,
            assessments_enforced=assessments_enforced,
            collaborator_auth_policy=collaborator_auth_policy,
            cost_estimation_enabled=cost_estimation_enabled,
            id=id,
            owners_team_saml_role_id=owners_team_saml_role_id,
            send_passing_statuses_for_untriggered_speculative_plans=send_passing_statuses_for_untriggered_speculative_plans,
            session_remember_minutes=session_remember_minutes,
            session_timeout_minutes=session_timeout_minutes,
            speculative_plan_management_enabled=speculative_plan_management_enabled,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a Organization resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Organization to import.
        :param import_from_id: The id of the existing Organization that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Organization to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69b4b8e2d01e6cdc96693cd13fb5cc4319293ecc1e88d2e09bcbf5a0dae44a8b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAggregatedCommitStatusEnabled")
    def reset_aggregated_commit_status_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregatedCommitStatusEnabled", []))

    @jsii.member(jsii_name="resetAllowForceDeleteWorkspaces")
    def reset_allow_force_delete_workspaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowForceDeleteWorkspaces", []))

    @jsii.member(jsii_name="resetAssessmentsEnforced")
    def reset_assessments_enforced(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssessmentsEnforced", []))

    @jsii.member(jsii_name="resetCollaboratorAuthPolicy")
    def reset_collaborator_auth_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollaboratorAuthPolicy", []))

    @jsii.member(jsii_name="resetCostEstimationEnabled")
    def reset_cost_estimation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCostEstimationEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOwnersTeamSamlRoleId")
    def reset_owners_team_saml_role_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwnersTeamSamlRoleId", []))

    @jsii.member(jsii_name="resetSendPassingStatusesForUntriggeredSpeculativePlans")
    def reset_send_passing_statuses_for_untriggered_speculative_plans(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendPassingStatusesForUntriggeredSpeculativePlans", []))

    @jsii.member(jsii_name="resetSessionRememberMinutes")
    def reset_session_remember_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionRememberMinutes", []))

    @jsii.member(jsii_name="resetSessionTimeoutMinutes")
    def reset_session_timeout_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionTimeoutMinutes", []))

    @jsii.member(jsii_name="resetSpeculativePlanManagementEnabled")
    def reset_speculative_plan_management_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpeculativePlanManagementEnabled", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="defaultProjectId")
    def default_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultProjectId"))

    @builtins.property
    @jsii.member(jsii_name="aggregatedCommitStatusEnabledInput")
    def aggregated_commit_status_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "aggregatedCommitStatusEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="allowForceDeleteWorkspacesInput")
    def allow_force_delete_workspaces_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowForceDeleteWorkspacesInput"))

    @builtins.property
    @jsii.member(jsii_name="assessmentsEnforcedInput")
    def assessments_enforced_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "assessmentsEnforcedInput"))

    @builtins.property
    @jsii.member(jsii_name="collaboratorAuthPolicyInput")
    def collaborator_auth_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collaboratorAuthPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="costEstimationEnabledInput")
    def cost_estimation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "costEstimationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="ownersTeamSamlRoleIdInput")
    def owners_team_saml_role_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownersTeamSamlRoleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sendPassingStatusesForUntriggeredSpeculativePlansInput")
    def send_passing_statuses_for_untriggered_speculative_plans_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendPassingStatusesForUntriggeredSpeculativePlansInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionRememberMinutesInput")
    def session_remember_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionRememberMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionTimeoutMinutesInput")
    def session_timeout_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionTimeoutMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="speculativePlanManagementEnabledInput")
    def speculative_plan_management_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "speculativePlanManagementEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregatedCommitStatusEnabled")
    def aggregated_commit_status_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "aggregatedCommitStatusEnabled"))

    @aggregated_commit_status_enabled.setter
    def aggregated_commit_status_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d94aaf32183514c31e94c8ba3c0d5bf4b6ba671527d2b8dbbf6b0fb8a44319d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregatedCommitStatusEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowForceDeleteWorkspaces")
    def allow_force_delete_workspaces(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowForceDeleteWorkspaces"))

    @allow_force_delete_workspaces.setter
    def allow_force_delete_workspaces(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9611e0358808111a834c00aabbb893997f2cb77bea5117700b483e36f720cab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowForceDeleteWorkspaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="assessmentsEnforced")
    def assessments_enforced(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "assessmentsEnforced"))

    @assessments_enforced.setter
    def assessments_enforced(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b38b9b1d1eeedcbfe8cb9eeeb17e0b0d83faa640511ab4a5ca5e3f121cfe86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assessmentsEnforced", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="collaboratorAuthPolicy")
    def collaborator_auth_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collaboratorAuthPolicy"))

    @collaborator_auth_policy.setter
    def collaborator_auth_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b279b424261a050ea78c5a8e646bfd5153a5db41f03a7be843a70fc6152eaef4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collaboratorAuthPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="costEstimationEnabled")
    def cost_estimation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "costEstimationEnabled"))

    @cost_estimation_enabled.setter
    def cost_estimation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5007bb3fdc68e598a40e4e2877ce853be8000f0ee85875b1342815f16fc96c0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "costEstimationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d6d68476568424409560f7802d11a752dacf7648bccbfa14af07585e3ab7da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76b6f78c161c28dce78f8144dbcf01cf052a980447063ef509f4ed2819941f7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d06de2f7f7ef274bda74835e5166f518713a4d0b448810abc9e790dd2f33c52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ownersTeamSamlRoleId")
    def owners_team_saml_role_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownersTeamSamlRoleId"))

    @owners_team_saml_role_id.setter
    def owners_team_saml_role_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ecb860aea470ea713a7e05d0ee55bed78c2fa81a5cfd2e8eeb5601c7ad6019f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ownersTeamSamlRoleId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sendPassingStatusesForUntriggeredSpeculativePlans")
    def send_passing_statuses_for_untriggered_speculative_plans(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendPassingStatusesForUntriggeredSpeculativePlans"))

    @send_passing_statuses_for_untriggered_speculative_plans.setter
    def send_passing_statuses_for_untriggered_speculative_plans(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaef25ddf5f48d2ed815be089a8378feede89e3d984b1586a1f75eb2a932aefa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendPassingStatusesForUntriggeredSpeculativePlans", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionRememberMinutes")
    def session_remember_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionRememberMinutes"))

    @session_remember_minutes.setter
    def session_remember_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ded4ece5beae43c3709101a35402001dfed83b08b544f116f945f54a162c3f18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionRememberMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionTimeoutMinutes")
    def session_timeout_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionTimeoutMinutes"))

    @session_timeout_minutes.setter
    def session_timeout_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23c7f7d38e7e2bd4a02233683cdd12a843c4e8ed8076adb334c89aeb9b7708db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionTimeoutMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="speculativePlanManagementEnabled")
    def speculative_plan_management_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "speculativePlanManagementEnabled"))

    @speculative_plan_management_enabled.setter
    def speculative_plan_management_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325ffcdb92d8e29399cc27caec4dfa61c3f8541d4c5a28f38d6618853af72d64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "speculativePlanManagementEnabled", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.organization.OrganizationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "email": "email",
        "name": "name",
        "aggregated_commit_status_enabled": "aggregatedCommitStatusEnabled",
        "allow_force_delete_workspaces": "allowForceDeleteWorkspaces",
        "assessments_enforced": "assessmentsEnforced",
        "collaborator_auth_policy": "collaboratorAuthPolicy",
        "cost_estimation_enabled": "costEstimationEnabled",
        "id": "id",
        "owners_team_saml_role_id": "ownersTeamSamlRoleId",
        "send_passing_statuses_for_untriggered_speculative_plans": "sendPassingStatusesForUntriggeredSpeculativePlans",
        "session_remember_minutes": "sessionRememberMinutes",
        "session_timeout_minutes": "sessionTimeoutMinutes",
        "speculative_plan_management_enabled": "speculativePlanManagementEnabled",
    },
)
class OrganizationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        email: builtins.str,
        name: builtins.str,
        aggregated_commit_status_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_force_delete_workspaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        assessments_enforced: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        collaborator_auth_policy: typing.Optional[builtins.str] = None,
        cost_estimation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        owners_team_saml_role_id: typing.Optional[builtins.str] = None,
        send_passing_statuses_for_untriggered_speculative_plans: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        session_remember_minutes: typing.Optional[jsii.Number] = None,
        session_timeout_minutes: typing.Optional[jsii.Number] = None,
        speculative_plan_management_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#email Organization#email}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#name Organization#name}.
        :param aggregated_commit_status_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#aggregated_commit_status_enabled Organization#aggregated_commit_status_enabled}.
        :param allow_force_delete_workspaces: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#allow_force_delete_workspaces Organization#allow_force_delete_workspaces}.
        :param assessments_enforced: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#assessments_enforced Organization#assessments_enforced}.
        :param collaborator_auth_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#collaborator_auth_policy Organization#collaborator_auth_policy}.
        :param cost_estimation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#cost_estimation_enabled Organization#cost_estimation_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#id Organization#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param owners_team_saml_role_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#owners_team_saml_role_id Organization#owners_team_saml_role_id}.
        :param send_passing_statuses_for_untriggered_speculative_plans: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#send_passing_statuses_for_untriggered_speculative_plans Organization#send_passing_statuses_for_untriggered_speculative_plans}.
        :param session_remember_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#session_remember_minutes Organization#session_remember_minutes}.
        :param session_timeout_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#session_timeout_minutes Organization#session_timeout_minutes}.
        :param speculative_plan_management_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#speculative_plan_management_enabled Organization#speculative_plan_management_enabled}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f91fe2dabc5e7b94e8a3c960d4e164fa7bfc7284e306e9061f5b602bddd44d73)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument aggregated_commit_status_enabled", value=aggregated_commit_status_enabled, expected_type=type_hints["aggregated_commit_status_enabled"])
            check_type(argname="argument allow_force_delete_workspaces", value=allow_force_delete_workspaces, expected_type=type_hints["allow_force_delete_workspaces"])
            check_type(argname="argument assessments_enforced", value=assessments_enforced, expected_type=type_hints["assessments_enforced"])
            check_type(argname="argument collaborator_auth_policy", value=collaborator_auth_policy, expected_type=type_hints["collaborator_auth_policy"])
            check_type(argname="argument cost_estimation_enabled", value=cost_estimation_enabled, expected_type=type_hints["cost_estimation_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument owners_team_saml_role_id", value=owners_team_saml_role_id, expected_type=type_hints["owners_team_saml_role_id"])
            check_type(argname="argument send_passing_statuses_for_untriggered_speculative_plans", value=send_passing_statuses_for_untriggered_speculative_plans, expected_type=type_hints["send_passing_statuses_for_untriggered_speculative_plans"])
            check_type(argname="argument session_remember_minutes", value=session_remember_minutes, expected_type=type_hints["session_remember_minutes"])
            check_type(argname="argument session_timeout_minutes", value=session_timeout_minutes, expected_type=type_hints["session_timeout_minutes"])
            check_type(argname="argument speculative_plan_management_enabled", value=speculative_plan_management_enabled, expected_type=type_hints["speculative_plan_management_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "email": email,
            "name": name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if aggregated_commit_status_enabled is not None:
            self._values["aggregated_commit_status_enabled"] = aggregated_commit_status_enabled
        if allow_force_delete_workspaces is not None:
            self._values["allow_force_delete_workspaces"] = allow_force_delete_workspaces
        if assessments_enforced is not None:
            self._values["assessments_enforced"] = assessments_enforced
        if collaborator_auth_policy is not None:
            self._values["collaborator_auth_policy"] = collaborator_auth_policy
        if cost_estimation_enabled is not None:
            self._values["cost_estimation_enabled"] = cost_estimation_enabled
        if id is not None:
            self._values["id"] = id
        if owners_team_saml_role_id is not None:
            self._values["owners_team_saml_role_id"] = owners_team_saml_role_id
        if send_passing_statuses_for_untriggered_speculative_plans is not None:
            self._values["send_passing_statuses_for_untriggered_speculative_plans"] = send_passing_statuses_for_untriggered_speculative_plans
        if session_remember_minutes is not None:
            self._values["session_remember_minutes"] = session_remember_minutes
        if session_timeout_minutes is not None:
            self._values["session_timeout_minutes"] = session_timeout_minutes
        if speculative_plan_management_enabled is not None:
            self._values["speculative_plan_management_enabled"] = speculative_plan_management_enabled

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def email(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#email Organization#email}.'''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#name Organization#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aggregated_commit_status_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#aggregated_commit_status_enabled Organization#aggregated_commit_status_enabled}.'''
        result = self._values.get("aggregated_commit_status_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_force_delete_workspaces(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#allow_force_delete_workspaces Organization#allow_force_delete_workspaces}.'''
        result = self._values.get("allow_force_delete_workspaces")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def assessments_enforced(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#assessments_enforced Organization#assessments_enforced}.'''
        result = self._values.get("assessments_enforced")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def collaborator_auth_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#collaborator_auth_policy Organization#collaborator_auth_policy}.'''
        result = self._values.get("collaborator_auth_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cost_estimation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#cost_estimation_enabled Organization#cost_estimation_enabled}.'''
        result = self._values.get("cost_estimation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#id Organization#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owners_team_saml_role_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#owners_team_saml_role_id Organization#owners_team_saml_role_id}.'''
        result = self._values.get("owners_team_saml_role_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def send_passing_statuses_for_untriggered_speculative_plans(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#send_passing_statuses_for_untriggered_speculative_plans Organization#send_passing_statuses_for_untriggered_speculative_plans}.'''
        result = self._values.get("send_passing_statuses_for_untriggered_speculative_plans")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def session_remember_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#session_remember_minutes Organization#session_remember_minutes}.'''
        result = self._values.get("session_remember_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def session_timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#session_timeout_minutes Organization#session_timeout_minutes}.'''
        result = self._values.get("session_timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def speculative_plan_management_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/organization#speculative_plan_management_enabled Organization#speculative_plan_management_enabled}.'''
        result = self._values.get("speculative_plan_management_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Organization",
    "OrganizationConfig",
]

publication.publish()

def _typecheckingstub__b6449e3ef9f933e7e0b019cbbc14e996201ef002b68481915160874cc1ccbe29(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    email: builtins.str,
    name: builtins.str,
    aggregated_commit_status_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_force_delete_workspaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    assessments_enforced: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    collaborator_auth_policy: typing.Optional[builtins.str] = None,
    cost_estimation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    owners_team_saml_role_id: typing.Optional[builtins.str] = None,
    send_passing_statuses_for_untriggered_speculative_plans: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    session_remember_minutes: typing.Optional[jsii.Number] = None,
    session_timeout_minutes: typing.Optional[jsii.Number] = None,
    speculative_plan_management_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b4b8e2d01e6cdc96693cd13fb5cc4319293ecc1e88d2e09bcbf5a0dae44a8b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d94aaf32183514c31e94c8ba3c0d5bf4b6ba671527d2b8dbbf6b0fb8a44319d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9611e0358808111a834c00aabbb893997f2cb77bea5117700b483e36f720cab5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b38b9b1d1eeedcbfe8cb9eeeb17e0b0d83faa640511ab4a5ca5e3f121cfe86(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b279b424261a050ea78c5a8e646bfd5153a5db41f03a7be843a70fc6152eaef4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5007bb3fdc68e598a40e4e2877ce853be8000f0ee85875b1342815f16fc96c0f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d6d68476568424409560f7802d11a752dacf7648bccbfa14af07585e3ab7da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76b6f78c161c28dce78f8144dbcf01cf052a980447063ef509f4ed2819941f7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d06de2f7f7ef274bda74835e5166f518713a4d0b448810abc9e790dd2f33c52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ecb860aea470ea713a7e05d0ee55bed78c2fa81a5cfd2e8eeb5601c7ad6019f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaef25ddf5f48d2ed815be089a8378feede89e3d984b1586a1f75eb2a932aefa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded4ece5beae43c3709101a35402001dfed83b08b544f116f945f54a162c3f18(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23c7f7d38e7e2bd4a02233683cdd12a843c4e8ed8076adb334c89aeb9b7708db(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325ffcdb92d8e29399cc27caec4dfa61c3f8541d4c5a28f38d6618853af72d64(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f91fe2dabc5e7b94e8a3c960d4e164fa7bfc7284e306e9061f5b602bddd44d73(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    email: builtins.str,
    name: builtins.str,
    aggregated_commit_status_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_force_delete_workspaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    assessments_enforced: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    collaborator_auth_policy: typing.Optional[builtins.str] = None,
    cost_estimation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    owners_team_saml_role_id: typing.Optional[builtins.str] = None,
    send_passing_statuses_for_untriggered_speculative_plans: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    session_remember_minutes: typing.Optional[jsii.Number] = None,
    session_timeout_minutes: typing.Optional[jsii.Number] = None,
    speculative_plan_management_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
