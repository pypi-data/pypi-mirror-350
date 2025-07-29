r'''
# `tfe_workspace_run`

Refer to the Terraform Registry for docs: [`tfe_workspace_run`](https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run).
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


class WorkspaceRun(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.workspaceRun.WorkspaceRun",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run tfe_workspace_run}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        workspace_id: builtins.str,
        apply: typing.Optional[typing.Union["WorkspaceRunApply", typing.Dict[builtins.str, typing.Any]]] = None,
        destroy: typing.Optional[typing.Union["WorkspaceRunDestroy", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run tfe_workspace_run} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#workspace_id WorkspaceRun#workspace_id}.
        :param apply: apply block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#apply WorkspaceRun#apply}
        :param destroy: destroy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#destroy WorkspaceRun#destroy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#id WorkspaceRun#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b76716b50c93fba8668fa42e9f6a38db35965679afe1e772105fdffc2a41ade5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WorkspaceRunConfig(
            workspace_id=workspace_id,
            apply=apply,
            destroy=destroy,
            id=id,
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
        '''Generates CDKTF code for importing a WorkspaceRun resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WorkspaceRun to import.
        :param import_from_id: The id of the existing WorkspaceRun that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WorkspaceRun to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e4bd457712a2cbde77eb9361af52dcd849148265e907bcbb0d5f1bc6b7ac07b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putApply")
    def put_apply(
        self,
        *,
        manual_confirm: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        retry: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        retry_backoff_max: typing.Optional[jsii.Number] = None,
        retry_backoff_min: typing.Optional[jsii.Number] = None,
        wait_for_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param manual_confirm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#manual_confirm WorkspaceRun#manual_confirm}.
        :param retry: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry WorkspaceRun#retry}.
        :param retry_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry_attempts WorkspaceRun#retry_attempts}.
        :param retry_backoff_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry_backoff_max WorkspaceRun#retry_backoff_max}.
        :param retry_backoff_min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry_backoff_min WorkspaceRun#retry_backoff_min}.
        :param wait_for_run: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#wait_for_run WorkspaceRun#wait_for_run}.
        '''
        value = WorkspaceRunApply(
            manual_confirm=manual_confirm,
            retry=retry,
            retry_attempts=retry_attempts,
            retry_backoff_max=retry_backoff_max,
            retry_backoff_min=retry_backoff_min,
            wait_for_run=wait_for_run,
        )

        return typing.cast(None, jsii.invoke(self, "putApply", [value]))

    @jsii.member(jsii_name="putDestroy")
    def put_destroy(
        self,
        *,
        manual_confirm: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        retry: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        retry_backoff_max: typing.Optional[jsii.Number] = None,
        retry_backoff_min: typing.Optional[jsii.Number] = None,
        wait_for_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param manual_confirm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#manual_confirm WorkspaceRun#manual_confirm}.
        :param retry: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry WorkspaceRun#retry}.
        :param retry_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry_attempts WorkspaceRun#retry_attempts}.
        :param retry_backoff_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry_backoff_max WorkspaceRun#retry_backoff_max}.
        :param retry_backoff_min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry_backoff_min WorkspaceRun#retry_backoff_min}.
        :param wait_for_run: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#wait_for_run WorkspaceRun#wait_for_run}.
        '''
        value = WorkspaceRunDestroy(
            manual_confirm=manual_confirm,
            retry=retry,
            retry_attempts=retry_attempts,
            retry_backoff_max=retry_backoff_max,
            retry_backoff_min=retry_backoff_min,
            wait_for_run=wait_for_run,
        )

        return typing.cast(None, jsii.invoke(self, "putDestroy", [value]))

    @jsii.member(jsii_name="resetApply")
    def reset_apply(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApply", []))

    @jsii.member(jsii_name="resetDestroy")
    def reset_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestroy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="apply")
    def apply(self) -> "WorkspaceRunApplyOutputReference":
        return typing.cast("WorkspaceRunApplyOutputReference", jsii.get(self, "apply"))

    @builtins.property
    @jsii.member(jsii_name="destroy")
    def destroy(self) -> "WorkspaceRunDestroyOutputReference":
        return typing.cast("WorkspaceRunDestroyOutputReference", jsii.get(self, "destroy"))

    @builtins.property
    @jsii.member(jsii_name="applyInput")
    def apply_input(self) -> typing.Optional["WorkspaceRunApply"]:
        return typing.cast(typing.Optional["WorkspaceRunApply"], jsii.get(self, "applyInput"))

    @builtins.property
    @jsii.member(jsii_name="destroyInput")
    def destroy_input(self) -> typing.Optional["WorkspaceRunDestroy"]:
        return typing.cast(typing.Optional["WorkspaceRunDestroy"], jsii.get(self, "destroyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="workspaceIdInput")
    def workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9c2f1755adb3dae792275da58f6af31772326345c1cc87e17dffce0102d6c42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5372c94460de437e45320c5fa215be29ad1cee4a4233bf5c36e2e540547c908f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.workspaceRun.WorkspaceRunApply",
    jsii_struct_bases=[],
    name_mapping={
        "manual_confirm": "manualConfirm",
        "retry": "retry",
        "retry_attempts": "retryAttempts",
        "retry_backoff_max": "retryBackoffMax",
        "retry_backoff_min": "retryBackoffMin",
        "wait_for_run": "waitForRun",
    },
)
class WorkspaceRunApply:
    def __init__(
        self,
        *,
        manual_confirm: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        retry: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        retry_backoff_max: typing.Optional[jsii.Number] = None,
        retry_backoff_min: typing.Optional[jsii.Number] = None,
        wait_for_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param manual_confirm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#manual_confirm WorkspaceRun#manual_confirm}.
        :param retry: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry WorkspaceRun#retry}.
        :param retry_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry_attempts WorkspaceRun#retry_attempts}.
        :param retry_backoff_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry_backoff_max WorkspaceRun#retry_backoff_max}.
        :param retry_backoff_min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry_backoff_min WorkspaceRun#retry_backoff_min}.
        :param wait_for_run: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#wait_for_run WorkspaceRun#wait_for_run}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8433703e98ec657a31e080b2baeaa66a5e7eb8c68b75a1c6c3df385c478c8782)
            check_type(argname="argument manual_confirm", value=manual_confirm, expected_type=type_hints["manual_confirm"])
            check_type(argname="argument retry", value=retry, expected_type=type_hints["retry"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument retry_backoff_max", value=retry_backoff_max, expected_type=type_hints["retry_backoff_max"])
            check_type(argname="argument retry_backoff_min", value=retry_backoff_min, expected_type=type_hints["retry_backoff_min"])
            check_type(argname="argument wait_for_run", value=wait_for_run, expected_type=type_hints["wait_for_run"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "manual_confirm": manual_confirm,
        }
        if retry is not None:
            self._values["retry"] = retry
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if retry_backoff_max is not None:
            self._values["retry_backoff_max"] = retry_backoff_max
        if retry_backoff_min is not None:
            self._values["retry_backoff_min"] = retry_backoff_min
        if wait_for_run is not None:
            self._values["wait_for_run"] = wait_for_run

    @builtins.property
    def manual_confirm(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#manual_confirm WorkspaceRun#manual_confirm}.'''
        result = self._values.get("manual_confirm")
        assert result is not None, "Required property 'manual_confirm' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def retry(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry WorkspaceRun#retry}.'''
        result = self._values.get("retry")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry_attempts WorkspaceRun#retry_attempts}.'''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_backoff_max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry_backoff_max WorkspaceRun#retry_backoff_max}.'''
        result = self._values.get("retry_backoff_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_backoff_min(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry_backoff_min WorkspaceRun#retry_backoff_min}.'''
        result = self._values.get("retry_backoff_min")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def wait_for_run(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#wait_for_run WorkspaceRun#wait_for_run}.'''
        result = self._values.get("wait_for_run")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspaceRunApply(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkspaceRunApplyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.workspaceRun.WorkspaceRunApplyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d5c59ab0ab24779b07edbf100872dcad9bd44569ffe4fba33bf197fbbdf4de5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRetry")
    def reset_retry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetry", []))

    @jsii.member(jsii_name="resetRetryAttempts")
    def reset_retry_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryAttempts", []))

    @jsii.member(jsii_name="resetRetryBackoffMax")
    def reset_retry_backoff_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryBackoffMax", []))

    @jsii.member(jsii_name="resetRetryBackoffMin")
    def reset_retry_backoff_min(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryBackoffMin", []))

    @jsii.member(jsii_name="resetWaitForRun")
    def reset_wait_for_run(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWaitForRun", []))

    @builtins.property
    @jsii.member(jsii_name="manualConfirmInput")
    def manual_confirm_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "manualConfirmInput"))

    @builtins.property
    @jsii.member(jsii_name="retryAttemptsInput")
    def retry_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="retryBackoffMaxInput")
    def retry_backoff_max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryBackoffMaxInput"))

    @builtins.property
    @jsii.member(jsii_name="retryBackoffMinInput")
    def retry_backoff_min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryBackoffMinInput"))

    @builtins.property
    @jsii.member(jsii_name="retryInput")
    def retry_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "retryInput"))

    @builtins.property
    @jsii.member(jsii_name="waitForRunInput")
    def wait_for_run_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "waitForRunInput"))

    @builtins.property
    @jsii.member(jsii_name="manualConfirm")
    def manual_confirm(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "manualConfirm"))

    @manual_confirm.setter
    def manual_confirm(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd714376d7f31f06d7755620bc7ae5f49b26378ad392407aaeefcb7cb437582a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manualConfirm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retry")
    def retry(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "retry"))

    @retry.setter
    def retry(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b47e1074d6abc5c13aef996d68da2db73f62baaf1cee44d8ecfe2c0e236100e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retry", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryAttempts")
    def retry_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retryAttempts"))

    @retry_attempts.setter
    def retry_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4af0deb3268197ef24a33ce066e98cc70f8e695cef406fe38b940ad2ffb311b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryBackoffMax")
    def retry_backoff_max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retryBackoffMax"))

    @retry_backoff_max.setter
    def retry_backoff_max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37fbbf151f270aba6fa4c75a9cce1a9fa7c5a252ff8c71aa0fa7f1c90c804a34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryBackoffMax", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryBackoffMin")
    def retry_backoff_min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retryBackoffMin"))

    @retry_backoff_min.setter
    def retry_backoff_min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__020c0be7b805001c4af3994e5b6cae191b3590f3207731701b0a44df9d48b205)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryBackoffMin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="waitForRun")
    def wait_for_run(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "waitForRun"))

    @wait_for_run.setter
    def wait_for_run(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__588842ffa07bf627078b7afbc69beb212d83bd70868e4c3042c4f686250a7d6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForRun", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WorkspaceRunApply]:
        return typing.cast(typing.Optional[WorkspaceRunApply], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[WorkspaceRunApply]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7d05ab2debbf4cfebae0a5c91dc475af06bd9f72b8c99da60d31dd632cef553)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.workspaceRun.WorkspaceRunConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "workspace_id": "workspaceId",
        "apply": "apply",
        "destroy": "destroy",
        "id": "id",
    },
)
class WorkspaceRunConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        workspace_id: builtins.str,
        apply: typing.Optional[typing.Union[WorkspaceRunApply, typing.Dict[builtins.str, typing.Any]]] = None,
        destroy: typing.Optional[typing.Union["WorkspaceRunDestroy", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#workspace_id WorkspaceRun#workspace_id}.
        :param apply: apply block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#apply WorkspaceRun#apply}
        :param destroy: destroy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#destroy WorkspaceRun#destroy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#id WorkspaceRun#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(apply, dict):
            apply = WorkspaceRunApply(**apply)
        if isinstance(destroy, dict):
            destroy = WorkspaceRunDestroy(**destroy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa432bbe644bd8321109034284aa8a7ed0e00f10697051f31f800bf7c438a180)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
            check_type(argname="argument apply", value=apply, expected_type=type_hints["apply"])
            check_type(argname="argument destroy", value=destroy, expected_type=type_hints["destroy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "workspace_id": workspace_id,
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
        if apply is not None:
            self._values["apply"] = apply
        if destroy is not None:
            self._values["destroy"] = destroy
        if id is not None:
            self._values["id"] = id

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
    def workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#workspace_id WorkspaceRun#workspace_id}.'''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def apply(self) -> typing.Optional[WorkspaceRunApply]:
        '''apply block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#apply WorkspaceRun#apply}
        '''
        result = self._values.get("apply")
        return typing.cast(typing.Optional[WorkspaceRunApply], result)

    @builtins.property
    def destroy(self) -> typing.Optional["WorkspaceRunDestroy"]:
        '''destroy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#destroy WorkspaceRun#destroy}
        '''
        result = self._values.get("destroy")
        return typing.cast(typing.Optional["WorkspaceRunDestroy"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#id WorkspaceRun#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspaceRunConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.workspaceRun.WorkspaceRunDestroy",
    jsii_struct_bases=[],
    name_mapping={
        "manual_confirm": "manualConfirm",
        "retry": "retry",
        "retry_attempts": "retryAttempts",
        "retry_backoff_max": "retryBackoffMax",
        "retry_backoff_min": "retryBackoffMin",
        "wait_for_run": "waitForRun",
    },
)
class WorkspaceRunDestroy:
    def __init__(
        self,
        *,
        manual_confirm: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        retry: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        retry_backoff_max: typing.Optional[jsii.Number] = None,
        retry_backoff_min: typing.Optional[jsii.Number] = None,
        wait_for_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param manual_confirm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#manual_confirm WorkspaceRun#manual_confirm}.
        :param retry: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry WorkspaceRun#retry}.
        :param retry_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry_attempts WorkspaceRun#retry_attempts}.
        :param retry_backoff_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry_backoff_max WorkspaceRun#retry_backoff_max}.
        :param retry_backoff_min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry_backoff_min WorkspaceRun#retry_backoff_min}.
        :param wait_for_run: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#wait_for_run WorkspaceRun#wait_for_run}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95cc0af3725dc167b805847eee490883953cbf554cea9913046bb7ad3c14ea80)
            check_type(argname="argument manual_confirm", value=manual_confirm, expected_type=type_hints["manual_confirm"])
            check_type(argname="argument retry", value=retry, expected_type=type_hints["retry"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument retry_backoff_max", value=retry_backoff_max, expected_type=type_hints["retry_backoff_max"])
            check_type(argname="argument retry_backoff_min", value=retry_backoff_min, expected_type=type_hints["retry_backoff_min"])
            check_type(argname="argument wait_for_run", value=wait_for_run, expected_type=type_hints["wait_for_run"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "manual_confirm": manual_confirm,
        }
        if retry is not None:
            self._values["retry"] = retry
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if retry_backoff_max is not None:
            self._values["retry_backoff_max"] = retry_backoff_max
        if retry_backoff_min is not None:
            self._values["retry_backoff_min"] = retry_backoff_min
        if wait_for_run is not None:
            self._values["wait_for_run"] = wait_for_run

    @builtins.property
    def manual_confirm(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#manual_confirm WorkspaceRun#manual_confirm}.'''
        result = self._values.get("manual_confirm")
        assert result is not None, "Required property 'manual_confirm' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def retry(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry WorkspaceRun#retry}.'''
        result = self._values.get("retry")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry_attempts WorkspaceRun#retry_attempts}.'''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_backoff_max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry_backoff_max WorkspaceRun#retry_backoff_max}.'''
        result = self._values.get("retry_backoff_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_backoff_min(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#retry_backoff_min WorkspaceRun#retry_backoff_min}.'''
        result = self._values.get("retry_backoff_min")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def wait_for_run(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/workspace_run#wait_for_run WorkspaceRun#wait_for_run}.'''
        result = self._values.get("wait_for_run")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspaceRunDestroy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkspaceRunDestroyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.workspaceRun.WorkspaceRunDestroyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59701a4ca5ae9cbc63577c2b5ce3402b4592aa247bed3c5a8e5a5ca81c1fc10f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRetry")
    def reset_retry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetry", []))

    @jsii.member(jsii_name="resetRetryAttempts")
    def reset_retry_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryAttempts", []))

    @jsii.member(jsii_name="resetRetryBackoffMax")
    def reset_retry_backoff_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryBackoffMax", []))

    @jsii.member(jsii_name="resetRetryBackoffMin")
    def reset_retry_backoff_min(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryBackoffMin", []))

    @jsii.member(jsii_name="resetWaitForRun")
    def reset_wait_for_run(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWaitForRun", []))

    @builtins.property
    @jsii.member(jsii_name="manualConfirmInput")
    def manual_confirm_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "manualConfirmInput"))

    @builtins.property
    @jsii.member(jsii_name="retryAttemptsInput")
    def retry_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="retryBackoffMaxInput")
    def retry_backoff_max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryBackoffMaxInput"))

    @builtins.property
    @jsii.member(jsii_name="retryBackoffMinInput")
    def retry_backoff_min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryBackoffMinInput"))

    @builtins.property
    @jsii.member(jsii_name="retryInput")
    def retry_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "retryInput"))

    @builtins.property
    @jsii.member(jsii_name="waitForRunInput")
    def wait_for_run_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "waitForRunInput"))

    @builtins.property
    @jsii.member(jsii_name="manualConfirm")
    def manual_confirm(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "manualConfirm"))

    @manual_confirm.setter
    def manual_confirm(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2449df50d49151833ca0f32c01f80b5cfa5db53f2d2e1754c0ecd4cb5bf89232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manualConfirm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retry")
    def retry(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "retry"))

    @retry.setter
    def retry(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__782540e91b91122d7055f2cbdb994a719102762496303ea21d407e5fe418e8da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retry", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryAttempts")
    def retry_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retryAttempts"))

    @retry_attempts.setter
    def retry_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ac231bfa3fdf973229e81412f9243c7f8540cc62ed41a854f0d1b4ca71fcf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryBackoffMax")
    def retry_backoff_max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retryBackoffMax"))

    @retry_backoff_max.setter
    def retry_backoff_max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6403d91b37ad0c07d27ba7b9583cf3d4ea86489b8a74db754f44314eec4acf14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryBackoffMax", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryBackoffMin")
    def retry_backoff_min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retryBackoffMin"))

    @retry_backoff_min.setter
    def retry_backoff_min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd2139fdf7c2c061973ead4b1e1619d46082597d7f5658d4cffeac28ccd671c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryBackoffMin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="waitForRun")
    def wait_for_run(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "waitForRun"))

    @wait_for_run.setter
    def wait_for_run(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff6846ffb394f6d370e15de5b1a5e0c5affcb1a290ce187680b4e4a4e95d000)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForRun", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WorkspaceRunDestroy]:
        return typing.cast(typing.Optional[WorkspaceRunDestroy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[WorkspaceRunDestroy]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f69981d74de0522df2226ec179d2e55473e2f454c67eaa26ac54905848f93ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WorkspaceRun",
    "WorkspaceRunApply",
    "WorkspaceRunApplyOutputReference",
    "WorkspaceRunConfig",
    "WorkspaceRunDestroy",
    "WorkspaceRunDestroyOutputReference",
]

publication.publish()

def _typecheckingstub__b76716b50c93fba8668fa42e9f6a38db35965679afe1e772105fdffc2a41ade5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    workspace_id: builtins.str,
    apply: typing.Optional[typing.Union[WorkspaceRunApply, typing.Dict[builtins.str, typing.Any]]] = None,
    destroy: typing.Optional[typing.Union[WorkspaceRunDestroy, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__8e4bd457712a2cbde77eb9361af52dcd849148265e907bcbb0d5f1bc6b7ac07b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c2f1755adb3dae792275da58f6af31772326345c1cc87e17dffce0102d6c42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5372c94460de437e45320c5fa215be29ad1cee4a4233bf5c36e2e540547c908f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8433703e98ec657a31e080b2baeaa66a5e7eb8c68b75a1c6c3df385c478c8782(
    *,
    manual_confirm: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    retry: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    retry_backoff_max: typing.Optional[jsii.Number] = None,
    retry_backoff_min: typing.Optional[jsii.Number] = None,
    wait_for_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d5c59ab0ab24779b07edbf100872dcad9bd44569ffe4fba33bf197fbbdf4de5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd714376d7f31f06d7755620bc7ae5f49b26378ad392407aaeefcb7cb437582a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47e1074d6abc5c13aef996d68da2db73f62baaf1cee44d8ecfe2c0e236100e8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af0deb3268197ef24a33ce066e98cc70f8e695cef406fe38b940ad2ffb311b7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37fbbf151f270aba6fa4c75a9cce1a9fa7c5a252ff8c71aa0fa7f1c90c804a34(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020c0be7b805001c4af3994e5b6cae191b3590f3207731701b0a44df9d48b205(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__588842ffa07bf627078b7afbc69beb212d83bd70868e4c3042c4f686250a7d6b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d05ab2debbf4cfebae0a5c91dc475af06bd9f72b8c99da60d31dd632cef553(
    value: typing.Optional[WorkspaceRunApply],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa432bbe644bd8321109034284aa8a7ed0e00f10697051f31f800bf7c438a180(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    workspace_id: builtins.str,
    apply: typing.Optional[typing.Union[WorkspaceRunApply, typing.Dict[builtins.str, typing.Any]]] = None,
    destroy: typing.Optional[typing.Union[WorkspaceRunDestroy, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95cc0af3725dc167b805847eee490883953cbf554cea9913046bb7ad3c14ea80(
    *,
    manual_confirm: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    retry: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    retry_backoff_max: typing.Optional[jsii.Number] = None,
    retry_backoff_min: typing.Optional[jsii.Number] = None,
    wait_for_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59701a4ca5ae9cbc63577c2b5ce3402b4592aa247bed3c5a8e5a5ca81c1fc10f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2449df50d49151833ca0f32c01f80b5cfa5db53f2d2e1754c0ecd4cb5bf89232(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__782540e91b91122d7055f2cbdb994a719102762496303ea21d407e5fe418e8da(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ac231bfa3fdf973229e81412f9243c7f8540cc62ed41a854f0d1b4ca71fcf6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6403d91b37ad0c07d27ba7b9583cf3d4ea86489b8a74db754f44314eec4acf14(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd2139fdf7c2c061973ead4b1e1619d46082597d7f5658d4cffeac28ccd671c6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff6846ffb394f6d370e15de5b1a5e0c5affcb1a290ce187680b4e4a4e95d000(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f69981d74de0522df2226ec179d2e55473e2f454c67eaa26ac54905848f93ed(
    value: typing.Optional[WorkspaceRunDestroy],
) -> None:
    """Type checking stubs"""
    pass
