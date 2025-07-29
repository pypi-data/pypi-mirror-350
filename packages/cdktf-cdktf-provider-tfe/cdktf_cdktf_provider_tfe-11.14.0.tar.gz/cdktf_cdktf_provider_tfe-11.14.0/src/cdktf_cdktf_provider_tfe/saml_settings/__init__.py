r'''
# `tfe_saml_settings`

Refer to the Terraform Registry for docs: [`tfe_saml_settings`](https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings).
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


class SamlSettings(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.samlSettings.SamlSettings",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings tfe_saml_settings}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        idp_cert: builtins.str,
        slo_endpoint_url: builtins.str,
        sso_endpoint_url: builtins.str,
        attr_groups: typing.Optional[builtins.str] = None,
        attr_site_admin: typing.Optional[builtins.str] = None,
        attr_username: typing.Optional[builtins.str] = None,
        authn_requests_signed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        certificate: typing.Optional[builtins.str] = None,
        debug: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_key: typing.Optional[builtins.str] = None,
        private_key_wo: typing.Optional[builtins.str] = None,
        signature_digest_method: typing.Optional[builtins.str] = None,
        signature_signing_method: typing.Optional[builtins.str] = None,
        site_admin_role: typing.Optional[builtins.str] = None,
        sso_api_token_session_timeout: typing.Optional[jsii.Number] = None,
        team_management_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        want_assertions_signed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings tfe_saml_settings} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param idp_cert: Identity Provider Certificate specifies the PEM encoded X.509 Certificate as provided by the IdP configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#idp_cert SamlSettings#idp_cert}
        :param slo_endpoint_url: Single Log Out URL specifies the HTTPS endpoint on your IdP for single logout requests. This value is provided by the IdP configuration Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#slo_endpoint_url SamlSettings#slo_endpoint_url}
        :param sso_endpoint_url: Single Sign On URL specifies the HTTPS endpoint on your IdP for single sign-on requests. This value is provided by the IdP configuration Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#sso_endpoint_url SamlSettings#sso_endpoint_url}
        :param attr_groups: Team Attribute Name specifies the name of the SAML attribute that determines team membership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#attr_groups SamlSettings#attr_groups}
        :param attr_site_admin: Specifies the role for site admin access. Overrides the "Site Admin Role" method. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#attr_site_admin SamlSettings#attr_site_admin}
        :param attr_username: Username Attribute Name specifies the name of the SAML attribute that determines the user's username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#attr_username SamlSettings#attr_username}
        :param authn_requests_signed: Ensure that `samlp:AuthnRequest <samlp:AuthnRequest>`_ messages are signed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#authn_requests_signed SamlSettings#authn_requests_signed}
        :param certificate: The certificate used for request and assertion signing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#certificate SamlSettings#certificate}
        :param debug: When sign-on fails and this is enabled, the SAMLResponse XML will be displayed on the login page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#debug SamlSettings#debug}
        :param private_key: The private key used for request and assertion signing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#private_key SamlSettings#private_key}
        :param private_key_wo: The private key in write-only mode used for request and assertion signing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#private_key_wo SamlSettings#private_key_wo}
        :param signature_digest_method: Signature Digest Method. Must be either ``SHA1`` or ``SHA256``. Defaults to ``SHA256``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#signature_digest_method SamlSettings#signature_digest_method}
        :param signature_signing_method: Signature Signing Method. Must be either ``SHA1`` or ``SHA256``. Defaults to ``SHA256``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#signature_signing_method SamlSettings#signature_signing_method}
        :param site_admin_role: Specifies the role for site admin access, provided in the list of roles sent in the Team Attribute Name attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#site_admin_role SamlSettings#site_admin_role}
        :param sso_api_token_session_timeout: Specifies the Single Sign On session timeout in seconds. Defaults to 14 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#sso_api_token_session_timeout SamlSettings#sso_api_token_session_timeout}
        :param team_management_enabled: Set it to false if you would rather use Terraform Enterprise to manage team membership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#team_management_enabled SamlSettings#team_management_enabled}
        :param want_assertions_signed: Ensure that `saml:Assertion <saml:Assertion>`_ elements are signed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#want_assertions_signed SamlSettings#want_assertions_signed}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ec101603e2a339660df455d6fe62df46992821d7d68fc47d6f922edcb876b57)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = SamlSettingsConfig(
            idp_cert=idp_cert,
            slo_endpoint_url=slo_endpoint_url,
            sso_endpoint_url=sso_endpoint_url,
            attr_groups=attr_groups,
            attr_site_admin=attr_site_admin,
            attr_username=attr_username,
            authn_requests_signed=authn_requests_signed,
            certificate=certificate,
            debug=debug,
            private_key=private_key,
            private_key_wo=private_key_wo,
            signature_digest_method=signature_digest_method,
            signature_signing_method=signature_signing_method,
            site_admin_role=site_admin_role,
            sso_api_token_session_timeout=sso_api_token_session_timeout,
            team_management_enabled=team_management_enabled,
            want_assertions_signed=want_assertions_signed,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a SamlSettings resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SamlSettings to import.
        :param import_from_id: The id of the existing SamlSettings that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SamlSettings to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d1e4a24315e1da3db92cc917ed6c9286be9d1a8a4e6d9d3c16a92af11e0e56c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAttrGroups")
    def reset_attr_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttrGroups", []))

    @jsii.member(jsii_name="resetAttrSiteAdmin")
    def reset_attr_site_admin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttrSiteAdmin", []))

    @jsii.member(jsii_name="resetAttrUsername")
    def reset_attr_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttrUsername", []))

    @jsii.member(jsii_name="resetAuthnRequestsSigned")
    def reset_authn_requests_signed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthnRequestsSigned", []))

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetDebug")
    def reset_debug(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDebug", []))

    @jsii.member(jsii_name="resetPrivateKey")
    def reset_private_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateKey", []))

    @jsii.member(jsii_name="resetPrivateKeyWo")
    def reset_private_key_wo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateKeyWo", []))

    @jsii.member(jsii_name="resetSignatureDigestMethod")
    def reset_signature_digest_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignatureDigestMethod", []))

    @jsii.member(jsii_name="resetSignatureSigningMethod")
    def reset_signature_signing_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignatureSigningMethod", []))

    @jsii.member(jsii_name="resetSiteAdminRole")
    def reset_site_admin_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSiteAdminRole", []))

    @jsii.member(jsii_name="resetSsoApiTokenSessionTimeout")
    def reset_sso_api_token_session_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsoApiTokenSessionTimeout", []))

    @jsii.member(jsii_name="resetTeamManagementEnabled")
    def reset_team_management_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTeamManagementEnabled", []))

    @jsii.member(jsii_name="resetWantAssertionsSigned")
    def reset_want_assertions_signed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWantAssertionsSigned", []))

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
    @jsii.member(jsii_name="acsConsumerUrl")
    def acs_consumer_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acsConsumerUrl"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="metadataUrl")
    def metadata_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataUrl"))

    @builtins.property
    @jsii.member(jsii_name="oldIdpCert")
    def old_idp_cert(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oldIdpCert"))

    @builtins.property
    @jsii.member(jsii_name="attrGroupsInput")
    def attr_groups_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attrGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="attrSiteAdminInput")
    def attr_site_admin_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attrSiteAdminInput"))

    @builtins.property
    @jsii.member(jsii_name="attrUsernameInput")
    def attr_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attrUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="authnRequestsSignedInput")
    def authn_requests_signed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "authnRequestsSignedInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="debugInput")
    def debug_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "debugInput"))

    @builtins.property
    @jsii.member(jsii_name="idpCertInput")
    def idp_cert_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idpCertInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyInput")
    def private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyWoInput")
    def private_key_wo_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyWoInput"))

    @builtins.property
    @jsii.member(jsii_name="signatureDigestMethodInput")
    def signature_digest_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signatureDigestMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="signatureSigningMethodInput")
    def signature_signing_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signatureSigningMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="siteAdminRoleInput")
    def site_admin_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "siteAdminRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="sloEndpointUrlInput")
    def slo_endpoint_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sloEndpointUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="ssoApiTokenSessionTimeoutInput")
    def sso_api_token_session_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ssoApiTokenSessionTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="ssoEndpointUrlInput")
    def sso_endpoint_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ssoEndpointUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="teamManagementEnabledInput")
    def team_management_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "teamManagementEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="wantAssertionsSignedInput")
    def want_assertions_signed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "wantAssertionsSignedInput"))

    @builtins.property
    @jsii.member(jsii_name="attrGroups")
    def attr_groups(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attrGroups"))

    @attr_groups.setter
    def attr_groups(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__290d1699088a13a034aadf84eb912c4e65ba5a7187108581d924afe3e2b4156e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attrGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="attrSiteAdmin")
    def attr_site_admin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attrSiteAdmin"))

    @attr_site_admin.setter
    def attr_site_admin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a54d689e98795818db58967e2ac7a237770aba9fb1a4534301a7da4b87405a29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attrSiteAdmin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="attrUsername")
    def attr_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attrUsername"))

    @attr_username.setter
    def attr_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1bf66e3e3b58fdbdae7580f51800562b05cebd60b7df460519de7ee23360dd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attrUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authnRequestsSigned")
    def authn_requests_signed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "authnRequestsSigned"))

    @authn_requests_signed.setter
    def authn_requests_signed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a52d759d9a59c7c32ba0d10812dd97468edacb44a22b70c572320b8aaef447d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authnRequestsSigned", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__222194a497b0c82665aa2d93f1dc03016f35c129fc36cec4ce92bc4d312c32e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="debug")
    def debug(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "debug"))

    @debug.setter
    def debug(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e610a4c6a48ba97d7636fa47ed61077b52791606cb6783d88dd59f0260d418f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "debug", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idpCert")
    def idp_cert(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idpCert"))

    @idp_cert.setter
    def idp_cert(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a862c6600ff3cd24050d210240683a4d4e814a6b69dcbc5abbb1fbaf0c94d3be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idpCert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a134351cf04a5c3861102146215a44beea6d32323123cb0d53d27fc3871e7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKeyWo")
    def private_key_wo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKeyWo"))

    @private_key_wo.setter
    def private_key_wo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4b63e917a650be50bcc5b2a8e0ec691ac629d3bf6a4b37019bfaf172d2d6dd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKeyWo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signatureDigestMethod")
    def signature_digest_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signatureDigestMethod"))

    @signature_digest_method.setter
    def signature_digest_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a55a05f2c011708154ec9a01b2c597212e3c5dc66bed66c410bb55bf40c9d807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signatureDigestMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signatureSigningMethod")
    def signature_signing_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signatureSigningMethod"))

    @signature_signing_method.setter
    def signature_signing_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1022e721acde3ebccc35a0787ac632b7766aab438ed1eaa1ee867cdd08f37bbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signatureSigningMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="siteAdminRole")
    def site_admin_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "siteAdminRole"))

    @site_admin_role.setter
    def site_admin_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ef94bacd8039286f7f112311e17fe7b9bfacb734515f866a52f1666392e9592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "siteAdminRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sloEndpointUrl")
    def slo_endpoint_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sloEndpointUrl"))

    @slo_endpoint_url.setter
    def slo_endpoint_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66994db2d1bcf279ff19516cd19327691b1e15c8f601a592607ccf6bfc51311d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sloEndpointUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ssoApiTokenSessionTimeout")
    def sso_api_token_session_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ssoApiTokenSessionTimeout"))

    @sso_api_token_session_timeout.setter
    def sso_api_token_session_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbe2cefccdf8477d308663b1f6c580a89d1b5ae04444a60b7ca6db371918010c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssoApiTokenSessionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ssoEndpointUrl")
    def sso_endpoint_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ssoEndpointUrl"))

    @sso_endpoint_url.setter
    def sso_endpoint_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7b81c6de7ec606afbee37fa52b77a14d0244cba1a8f95c579898b44de1a4e13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssoEndpointUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="teamManagementEnabled")
    def team_management_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "teamManagementEnabled"))

    @team_management_enabled.setter
    def team_management_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f7b23f356962eff11855b4d3f7f6502775e62a2b20a5e9214681b95b9f5b3f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teamManagementEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wantAssertionsSigned")
    def want_assertions_signed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "wantAssertionsSigned"))

    @want_assertions_signed.setter
    def want_assertions_signed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__683dbdbe8863069e15360ae5aff561ce63b9caa1a1a4a5d5675552a7043829c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wantAssertionsSigned", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.samlSettings.SamlSettingsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "idp_cert": "idpCert",
        "slo_endpoint_url": "sloEndpointUrl",
        "sso_endpoint_url": "ssoEndpointUrl",
        "attr_groups": "attrGroups",
        "attr_site_admin": "attrSiteAdmin",
        "attr_username": "attrUsername",
        "authn_requests_signed": "authnRequestsSigned",
        "certificate": "certificate",
        "debug": "debug",
        "private_key": "privateKey",
        "private_key_wo": "privateKeyWo",
        "signature_digest_method": "signatureDigestMethod",
        "signature_signing_method": "signatureSigningMethod",
        "site_admin_role": "siteAdminRole",
        "sso_api_token_session_timeout": "ssoApiTokenSessionTimeout",
        "team_management_enabled": "teamManagementEnabled",
        "want_assertions_signed": "wantAssertionsSigned",
    },
)
class SamlSettingsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        idp_cert: builtins.str,
        slo_endpoint_url: builtins.str,
        sso_endpoint_url: builtins.str,
        attr_groups: typing.Optional[builtins.str] = None,
        attr_site_admin: typing.Optional[builtins.str] = None,
        attr_username: typing.Optional[builtins.str] = None,
        authn_requests_signed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        certificate: typing.Optional[builtins.str] = None,
        debug: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_key: typing.Optional[builtins.str] = None,
        private_key_wo: typing.Optional[builtins.str] = None,
        signature_digest_method: typing.Optional[builtins.str] = None,
        signature_signing_method: typing.Optional[builtins.str] = None,
        site_admin_role: typing.Optional[builtins.str] = None,
        sso_api_token_session_timeout: typing.Optional[jsii.Number] = None,
        team_management_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        want_assertions_signed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param idp_cert: Identity Provider Certificate specifies the PEM encoded X.509 Certificate as provided by the IdP configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#idp_cert SamlSettings#idp_cert}
        :param slo_endpoint_url: Single Log Out URL specifies the HTTPS endpoint on your IdP for single logout requests. This value is provided by the IdP configuration Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#slo_endpoint_url SamlSettings#slo_endpoint_url}
        :param sso_endpoint_url: Single Sign On URL specifies the HTTPS endpoint on your IdP for single sign-on requests. This value is provided by the IdP configuration Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#sso_endpoint_url SamlSettings#sso_endpoint_url}
        :param attr_groups: Team Attribute Name specifies the name of the SAML attribute that determines team membership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#attr_groups SamlSettings#attr_groups}
        :param attr_site_admin: Specifies the role for site admin access. Overrides the "Site Admin Role" method. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#attr_site_admin SamlSettings#attr_site_admin}
        :param attr_username: Username Attribute Name specifies the name of the SAML attribute that determines the user's username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#attr_username SamlSettings#attr_username}
        :param authn_requests_signed: Ensure that `samlp:AuthnRequest <samlp:AuthnRequest>`_ messages are signed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#authn_requests_signed SamlSettings#authn_requests_signed}
        :param certificate: The certificate used for request and assertion signing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#certificate SamlSettings#certificate}
        :param debug: When sign-on fails and this is enabled, the SAMLResponse XML will be displayed on the login page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#debug SamlSettings#debug}
        :param private_key: The private key used for request and assertion signing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#private_key SamlSettings#private_key}
        :param private_key_wo: The private key in write-only mode used for request and assertion signing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#private_key_wo SamlSettings#private_key_wo}
        :param signature_digest_method: Signature Digest Method. Must be either ``SHA1`` or ``SHA256``. Defaults to ``SHA256``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#signature_digest_method SamlSettings#signature_digest_method}
        :param signature_signing_method: Signature Signing Method. Must be either ``SHA1`` or ``SHA256``. Defaults to ``SHA256``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#signature_signing_method SamlSettings#signature_signing_method}
        :param site_admin_role: Specifies the role for site admin access, provided in the list of roles sent in the Team Attribute Name attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#site_admin_role SamlSettings#site_admin_role}
        :param sso_api_token_session_timeout: Specifies the Single Sign On session timeout in seconds. Defaults to 14 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#sso_api_token_session_timeout SamlSettings#sso_api_token_session_timeout}
        :param team_management_enabled: Set it to false if you would rather use Terraform Enterprise to manage team membership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#team_management_enabled SamlSettings#team_management_enabled}
        :param want_assertions_signed: Ensure that `saml:Assertion <saml:Assertion>`_ elements are signed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#want_assertions_signed SamlSettings#want_assertions_signed}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97797dba9de1c91ed6407460b373553a6a2267977376c35b1ecbf5de2609cc7a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument idp_cert", value=idp_cert, expected_type=type_hints["idp_cert"])
            check_type(argname="argument slo_endpoint_url", value=slo_endpoint_url, expected_type=type_hints["slo_endpoint_url"])
            check_type(argname="argument sso_endpoint_url", value=sso_endpoint_url, expected_type=type_hints["sso_endpoint_url"])
            check_type(argname="argument attr_groups", value=attr_groups, expected_type=type_hints["attr_groups"])
            check_type(argname="argument attr_site_admin", value=attr_site_admin, expected_type=type_hints["attr_site_admin"])
            check_type(argname="argument attr_username", value=attr_username, expected_type=type_hints["attr_username"])
            check_type(argname="argument authn_requests_signed", value=authn_requests_signed, expected_type=type_hints["authn_requests_signed"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument debug", value=debug, expected_type=type_hints["debug"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument private_key_wo", value=private_key_wo, expected_type=type_hints["private_key_wo"])
            check_type(argname="argument signature_digest_method", value=signature_digest_method, expected_type=type_hints["signature_digest_method"])
            check_type(argname="argument signature_signing_method", value=signature_signing_method, expected_type=type_hints["signature_signing_method"])
            check_type(argname="argument site_admin_role", value=site_admin_role, expected_type=type_hints["site_admin_role"])
            check_type(argname="argument sso_api_token_session_timeout", value=sso_api_token_session_timeout, expected_type=type_hints["sso_api_token_session_timeout"])
            check_type(argname="argument team_management_enabled", value=team_management_enabled, expected_type=type_hints["team_management_enabled"])
            check_type(argname="argument want_assertions_signed", value=want_assertions_signed, expected_type=type_hints["want_assertions_signed"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "idp_cert": idp_cert,
            "slo_endpoint_url": slo_endpoint_url,
            "sso_endpoint_url": sso_endpoint_url,
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
        if attr_groups is not None:
            self._values["attr_groups"] = attr_groups
        if attr_site_admin is not None:
            self._values["attr_site_admin"] = attr_site_admin
        if attr_username is not None:
            self._values["attr_username"] = attr_username
        if authn_requests_signed is not None:
            self._values["authn_requests_signed"] = authn_requests_signed
        if certificate is not None:
            self._values["certificate"] = certificate
        if debug is not None:
            self._values["debug"] = debug
        if private_key is not None:
            self._values["private_key"] = private_key
        if private_key_wo is not None:
            self._values["private_key_wo"] = private_key_wo
        if signature_digest_method is not None:
            self._values["signature_digest_method"] = signature_digest_method
        if signature_signing_method is not None:
            self._values["signature_signing_method"] = signature_signing_method
        if site_admin_role is not None:
            self._values["site_admin_role"] = site_admin_role
        if sso_api_token_session_timeout is not None:
            self._values["sso_api_token_session_timeout"] = sso_api_token_session_timeout
        if team_management_enabled is not None:
            self._values["team_management_enabled"] = team_management_enabled
        if want_assertions_signed is not None:
            self._values["want_assertions_signed"] = want_assertions_signed

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
    def idp_cert(self) -> builtins.str:
        '''Identity Provider Certificate specifies the PEM encoded X.509 Certificate as provided by the IdP configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#idp_cert SamlSettings#idp_cert}
        '''
        result = self._values.get("idp_cert")
        assert result is not None, "Required property 'idp_cert' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slo_endpoint_url(self) -> builtins.str:
        '''Single Log Out URL specifies the HTTPS endpoint on your IdP for single logout requests.

        This value is provided by the IdP configuration

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#slo_endpoint_url SamlSettings#slo_endpoint_url}
        '''
        result = self._values.get("slo_endpoint_url")
        assert result is not None, "Required property 'slo_endpoint_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sso_endpoint_url(self) -> builtins.str:
        '''Single Sign On URL specifies the HTTPS endpoint on your IdP for single sign-on requests.

        This value is provided by the IdP configuration

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#sso_endpoint_url SamlSettings#sso_endpoint_url}
        '''
        result = self._values.get("sso_endpoint_url")
        assert result is not None, "Required property 'sso_endpoint_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attr_groups(self) -> typing.Optional[builtins.str]:
        '''Team Attribute Name specifies the name of the SAML attribute that determines team membership.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#attr_groups SamlSettings#attr_groups}
        '''
        result = self._values.get("attr_groups")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attr_site_admin(self) -> typing.Optional[builtins.str]:
        '''Specifies the role for site admin access. Overrides the "Site Admin Role" method.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#attr_site_admin SamlSettings#attr_site_admin}
        '''
        result = self._values.get("attr_site_admin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attr_username(self) -> typing.Optional[builtins.str]:
        '''Username Attribute Name specifies the name of the SAML attribute that determines the user's username.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#attr_username SamlSettings#attr_username}
        '''
        result = self._values.get("attr_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authn_requests_signed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Ensure that `samlp:AuthnRequest <samlp:AuthnRequest>`_ messages are signed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#authn_requests_signed SamlSettings#authn_requests_signed}
        '''
        result = self._values.get("authn_requests_signed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The certificate used for request and assertion signing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#certificate SamlSettings#certificate}
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def debug(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When sign-on fails and this is enabled, the SAMLResponse XML will be displayed on the login page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#debug SamlSettings#debug}
        '''
        result = self._values.get("debug")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The private key used for request and assertion signing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#private_key SamlSettings#private_key}
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key_wo(self) -> typing.Optional[builtins.str]:
        '''The private key in write-only mode used for request and assertion signing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#private_key_wo SamlSettings#private_key_wo}
        '''
        result = self._values.get("private_key_wo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signature_digest_method(self) -> typing.Optional[builtins.str]:
        '''Signature Digest Method. Must be either ``SHA1`` or ``SHA256``. Defaults to ``SHA256``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#signature_digest_method SamlSettings#signature_digest_method}
        '''
        result = self._values.get("signature_digest_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signature_signing_method(self) -> typing.Optional[builtins.str]:
        '''Signature Signing Method. Must be either ``SHA1`` or ``SHA256``. Defaults to ``SHA256``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#signature_signing_method SamlSettings#signature_signing_method}
        '''
        result = self._values.get("signature_signing_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def site_admin_role(self) -> typing.Optional[builtins.str]:
        '''Specifies the role for site admin access, provided in the list of roles sent in the Team Attribute Name attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#site_admin_role SamlSettings#site_admin_role}
        '''
        result = self._values.get("site_admin_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sso_api_token_session_timeout(self) -> typing.Optional[jsii.Number]:
        '''Specifies the Single Sign On session timeout in seconds. Defaults to 14 days.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#sso_api_token_session_timeout SamlSettings#sso_api_token_session_timeout}
        '''
        result = self._values.get("sso_api_token_session_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def team_management_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set it to false if you would rather use Terraform Enterprise to manage team membership.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#team_management_enabled SamlSettings#team_management_enabled}
        '''
        result = self._values.get("team_management_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def want_assertions_signed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Ensure that `saml:Assertion <saml:Assertion>`_ elements are signed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tfe/0.66.0/docs/resources/saml_settings#want_assertions_signed SamlSettings#want_assertions_signed}
        '''
        result = self._values.get("want_assertions_signed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SamlSettingsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SamlSettings",
    "SamlSettingsConfig",
]

publication.publish()

def _typecheckingstub__0ec101603e2a339660df455d6fe62df46992821d7d68fc47d6f922edcb876b57(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    idp_cert: builtins.str,
    slo_endpoint_url: builtins.str,
    sso_endpoint_url: builtins.str,
    attr_groups: typing.Optional[builtins.str] = None,
    attr_site_admin: typing.Optional[builtins.str] = None,
    attr_username: typing.Optional[builtins.str] = None,
    authn_requests_signed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    certificate: typing.Optional[builtins.str] = None,
    debug: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_key: typing.Optional[builtins.str] = None,
    private_key_wo: typing.Optional[builtins.str] = None,
    signature_digest_method: typing.Optional[builtins.str] = None,
    signature_signing_method: typing.Optional[builtins.str] = None,
    site_admin_role: typing.Optional[builtins.str] = None,
    sso_api_token_session_timeout: typing.Optional[jsii.Number] = None,
    team_management_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    want_assertions_signed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__1d1e4a24315e1da3db92cc917ed6c9286be9d1a8a4e6d9d3c16a92af11e0e56c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__290d1699088a13a034aadf84eb912c4e65ba5a7187108581d924afe3e2b4156e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54d689e98795818db58967e2ac7a237770aba9fb1a4534301a7da4b87405a29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1bf66e3e3b58fdbdae7580f51800562b05cebd60b7df460519de7ee23360dd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a52d759d9a59c7c32ba0d10812dd97468edacb44a22b70c572320b8aaef447d5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__222194a497b0c82665aa2d93f1dc03016f35c129fc36cec4ce92bc4d312c32e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e610a4c6a48ba97d7636fa47ed61077b52791606cb6783d88dd59f0260d418f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a862c6600ff3cd24050d210240683a4d4e814a6b69dcbc5abbb1fbaf0c94d3be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a134351cf04a5c3861102146215a44beea6d32323123cb0d53d27fc3871e7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4b63e917a650be50bcc5b2a8e0ec691ac629d3bf6a4b37019bfaf172d2d6dd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55a05f2c011708154ec9a01b2c597212e3c5dc66bed66c410bb55bf40c9d807(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1022e721acde3ebccc35a0787ac632b7766aab438ed1eaa1ee867cdd08f37bbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ef94bacd8039286f7f112311e17fe7b9bfacb734515f866a52f1666392e9592(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66994db2d1bcf279ff19516cd19327691b1e15c8f601a592607ccf6bfc51311d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbe2cefccdf8477d308663b1f6c580a89d1b5ae04444a60b7ca6db371918010c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b81c6de7ec606afbee37fa52b77a14d0244cba1a8f95c579898b44de1a4e13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7b23f356962eff11855b4d3f7f6502775e62a2b20a5e9214681b95b9f5b3f7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__683dbdbe8863069e15360ae5aff561ce63b9caa1a1a4a5d5675552a7043829c8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97797dba9de1c91ed6407460b373553a6a2267977376c35b1ecbf5de2609cc7a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    idp_cert: builtins.str,
    slo_endpoint_url: builtins.str,
    sso_endpoint_url: builtins.str,
    attr_groups: typing.Optional[builtins.str] = None,
    attr_site_admin: typing.Optional[builtins.str] = None,
    attr_username: typing.Optional[builtins.str] = None,
    authn_requests_signed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    certificate: typing.Optional[builtins.str] = None,
    debug: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_key: typing.Optional[builtins.str] = None,
    private_key_wo: typing.Optional[builtins.str] = None,
    signature_digest_method: typing.Optional[builtins.str] = None,
    signature_signing_method: typing.Optional[builtins.str] = None,
    site_admin_role: typing.Optional[builtins.str] = None,
    sso_api_token_session_timeout: typing.Optional[jsii.Number] = None,
    team_management_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    want_assertions_signed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
