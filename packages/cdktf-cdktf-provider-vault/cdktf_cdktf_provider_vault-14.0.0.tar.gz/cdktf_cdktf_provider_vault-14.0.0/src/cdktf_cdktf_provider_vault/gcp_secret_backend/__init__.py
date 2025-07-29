r'''
# `vault_gcp_secret_backend`

Refer to the Terraform Registry for docs: [`vault_gcp_secret_backend`](https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend).
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


class GcpSecretBackend(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.gcpSecretBackend.GcpSecretBackend",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend vault_gcp_secret_backend}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        credentials: typing.Optional[builtins.str] = None,
        default_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        disable_automated_rotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_remount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity_token_audience: typing.Optional[builtins.str] = None,
        identity_token_key: typing.Optional[builtins.str] = None,
        identity_token_ttl: typing.Optional[jsii.Number] = None,
        local: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
        namespace: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        rotation_period: typing.Optional[jsii.Number] = None,
        rotation_schedule: typing.Optional[builtins.str] = None,
        rotation_window: typing.Optional[jsii.Number] = None,
        service_account_email: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend vault_gcp_secret_backend} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param credentials: JSON-encoded credentials to use to connect to GCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#credentials GcpSecretBackend#credentials}
        :param default_lease_ttl_seconds: Default lease duration for secrets in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#default_lease_ttl_seconds GcpSecretBackend#default_lease_ttl_seconds}
        :param description: Human-friendly description of the mount for the backend. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#description GcpSecretBackend#description}
        :param disable_automated_rotation: Stops rotation of the root credential until set to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#disable_automated_rotation GcpSecretBackend#disable_automated_rotation}
        :param disable_remount: If set, opts out of mount migration on path updates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#disable_remount GcpSecretBackend#disable_remount}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#id GcpSecretBackend#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity_token_audience: The audience claim value for plugin identity tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#identity_token_audience GcpSecretBackend#identity_token_audience}
        :param identity_token_key: The key to use for signing identity tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#identity_token_key GcpSecretBackend#identity_token_key}
        :param identity_token_ttl: The TTL of generated tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#identity_token_ttl GcpSecretBackend#identity_token_ttl}
        :param local: Local mount flag that can be explicitly set to true to enforce local mount in HA environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#local GcpSecretBackend#local}
        :param max_lease_ttl_seconds: Maximum possible lease duration for secrets in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#max_lease_ttl_seconds GcpSecretBackend#max_lease_ttl_seconds}
        :param namespace: Target namespace. (requires Enterprise). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#namespace GcpSecretBackend#namespace}
        :param path: Path to mount the backend at. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#path GcpSecretBackend#path}
        :param rotation_period: The period of time in seconds between each rotation of the root credential. Cannot be used with rotation_schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#rotation_period GcpSecretBackend#rotation_period}
        :param rotation_schedule: The cron-style schedule for the root credential to be rotated on. Cannot be used with rotation_period. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#rotation_schedule GcpSecretBackend#rotation_schedule}
        :param rotation_window: The maximum amount of time in seconds Vault is allowed to complete a rotation once a scheduled rotation is triggered. Can only be used with rotation_schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#rotation_window GcpSecretBackend#rotation_window}
        :param service_account_email: Service Account to impersonate for plugin workload identity federation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#service_account_email GcpSecretBackend#service_account_email}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40db0a4e2cf966c67b591ecb94db0b247b1d9fcf191fecfcc0664cfc5f035643)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GcpSecretBackendConfig(
            credentials=credentials,
            default_lease_ttl_seconds=default_lease_ttl_seconds,
            description=description,
            disable_automated_rotation=disable_automated_rotation,
            disable_remount=disable_remount,
            id=id,
            identity_token_audience=identity_token_audience,
            identity_token_key=identity_token_key,
            identity_token_ttl=identity_token_ttl,
            local=local,
            max_lease_ttl_seconds=max_lease_ttl_seconds,
            namespace=namespace,
            path=path,
            rotation_period=rotation_period,
            rotation_schedule=rotation_schedule,
            rotation_window=rotation_window,
            service_account_email=service_account_email,
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
        '''Generates CDKTF code for importing a GcpSecretBackend resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GcpSecretBackend to import.
        :param import_from_id: The id of the existing GcpSecretBackend that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GcpSecretBackend to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6851f53d856833878f9217c4b0e8666222669478e7bdadbabce5f0628200884c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetCredentials")
    def reset_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentials", []))

    @jsii.member(jsii_name="resetDefaultLeaseTtlSeconds")
    def reset_default_lease_ttl_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultLeaseTtlSeconds", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisableAutomatedRotation")
    def reset_disable_automated_rotation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableAutomatedRotation", []))

    @jsii.member(jsii_name="resetDisableRemount")
    def reset_disable_remount(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableRemount", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentityTokenAudience")
    def reset_identity_token_audience(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityTokenAudience", []))

    @jsii.member(jsii_name="resetIdentityTokenKey")
    def reset_identity_token_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityTokenKey", []))

    @jsii.member(jsii_name="resetIdentityTokenTtl")
    def reset_identity_token_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityTokenTtl", []))

    @jsii.member(jsii_name="resetLocal")
    def reset_local(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocal", []))

    @jsii.member(jsii_name="resetMaxLeaseTtlSeconds")
    def reset_max_lease_ttl_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxLeaseTtlSeconds", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetRotationPeriod")
    def reset_rotation_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRotationPeriod", []))

    @jsii.member(jsii_name="resetRotationSchedule")
    def reset_rotation_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRotationSchedule", []))

    @jsii.member(jsii_name="resetRotationWindow")
    def reset_rotation_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRotationWindow", []))

    @jsii.member(jsii_name="resetServiceAccountEmail")
    def reset_service_account_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountEmail", []))

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
    @jsii.member(jsii_name="accessor")
    def accessor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessor"))

    @builtins.property
    @jsii.member(jsii_name="credentialsInput")
    def credentials_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultLeaseTtlSecondsInput")
    def default_lease_ttl_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultLeaseTtlSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="disableAutomatedRotationInput")
    def disable_automated_rotation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableAutomatedRotationInput"))

    @builtins.property
    @jsii.member(jsii_name="disableRemountInput")
    def disable_remount_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableRemountInput"))

    @builtins.property
    @jsii.member(jsii_name="identityTokenAudienceInput")
    def identity_token_audience_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityTokenAudienceInput"))

    @builtins.property
    @jsii.member(jsii_name="identityTokenKeyInput")
    def identity_token_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityTokenKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="identityTokenTtlInput")
    def identity_token_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "identityTokenTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="localInput")
    def local_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "localInput"))

    @builtins.property
    @jsii.member(jsii_name="maxLeaseTtlSecondsInput")
    def max_lease_ttl_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxLeaseTtlSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="rotationPeriodInput")
    def rotation_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rotationPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="rotationScheduleInput")
    def rotation_schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rotationScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="rotationWindowInput")
    def rotation_window_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rotationWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmailInput")
    def service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="credentials")
    def credentials(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentials"))

    @credentials.setter
    def credentials(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0966d1fd1026edde85a0a00cf3165ee8e8ab9020e8a0f9881e1ccff2db478834)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultLeaseTtlSeconds")
    def default_lease_ttl_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultLeaseTtlSeconds"))

    @default_lease_ttl_seconds.setter
    def default_lease_ttl_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64e901f77fbff84573aa6dad40442948241bad273de4a0e311c3b2b9f9e39b67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLeaseTtlSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__590dc459289e0f2369fc44037f8b1b23f05edfda5399f766607d46357616fe42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableAutomatedRotation")
    def disable_automated_rotation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableAutomatedRotation"))

    @disable_automated_rotation.setter
    def disable_automated_rotation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be11550c7931de90b9c361b603c2a27a99f1586ca436f29c9db3572bd36cc491)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableAutomatedRotation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableRemount")
    def disable_remount(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableRemount"))

    @disable_remount.setter
    def disable_remount(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a921403de038496183927161bcc65d089c89329d016944f949b4f65fca00456)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableRemount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5892aaf451c67107cf728068d60e12559a3aa22dda7a191de6ed8236b1fcd31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityTokenAudience")
    def identity_token_audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityTokenAudience"))

    @identity_token_audience.setter
    def identity_token_audience(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c662d86f4c3d46513d39156c3584817f573ef5c01415e40378ed3878cd88fd1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityTokenAudience", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityTokenKey")
    def identity_token_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityTokenKey"))

    @identity_token_key.setter
    def identity_token_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd05510363a83574e06d56f26a90b978003624f6a46b59d7d446688b425c660c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityTokenKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityTokenTtl")
    def identity_token_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "identityTokenTtl"))

    @identity_token_ttl.setter
    def identity_token_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__083ef131a616505c5ab3668f0e5ef5914562c1f4c9de3aeb73ce83f29f7990b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityTokenTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="local")
    def local(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "local"))

    @local.setter
    def local(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd7f146590b25abf93eb4f57a594ceacaaa73be77a430c4df513517e889d05bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "local", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxLeaseTtlSeconds")
    def max_lease_ttl_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxLeaseTtlSeconds"))

    @max_lease_ttl_seconds.setter
    def max_lease_ttl_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad060922ef6dad970a19954b63daa678eb0f6b7cbeed4b5c54c96e1a725b42b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxLeaseTtlSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__243f386ca13b344de5d5fe565a4a97ece8fb04151a8cdf4678e840091d781c40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3471734d1916c907c3d3aa2e46f9a8134a031939a26149739dbe3a0a4cb3538)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rotationPeriod")
    def rotation_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rotationPeriod"))

    @rotation_period.setter
    def rotation_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cd7e762936c1cf7948030c6892ea82b0fbf30723035efbb457e45addf1a18d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rotationSchedule")
    def rotation_schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rotationSchedule"))

    @rotation_schedule.setter
    def rotation_schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc17bfafde247c55e939fa9edb22b3b1072624d161dd79f961dd6c5a1e0afc12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationSchedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rotationWindow")
    def rotation_window(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rotationWindow"))

    @rotation_window.setter
    def rotation_window(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38e24de30e8e5f4e8d3e320712c80a55399212176ab7ead1f847b3425e5e5b94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationWindow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80261c97e504a6b8bd491761d98b8697f2a218bf02b1ee902ee4c54b429f3819)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.gcpSecretBackend.GcpSecretBackendConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "credentials": "credentials",
        "default_lease_ttl_seconds": "defaultLeaseTtlSeconds",
        "description": "description",
        "disable_automated_rotation": "disableAutomatedRotation",
        "disable_remount": "disableRemount",
        "id": "id",
        "identity_token_audience": "identityTokenAudience",
        "identity_token_key": "identityTokenKey",
        "identity_token_ttl": "identityTokenTtl",
        "local": "local",
        "max_lease_ttl_seconds": "maxLeaseTtlSeconds",
        "namespace": "namespace",
        "path": "path",
        "rotation_period": "rotationPeriod",
        "rotation_schedule": "rotationSchedule",
        "rotation_window": "rotationWindow",
        "service_account_email": "serviceAccountEmail",
    },
)
class GcpSecretBackendConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        credentials: typing.Optional[builtins.str] = None,
        default_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        disable_automated_rotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_remount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity_token_audience: typing.Optional[builtins.str] = None,
        identity_token_key: typing.Optional[builtins.str] = None,
        identity_token_ttl: typing.Optional[jsii.Number] = None,
        local: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
        namespace: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        rotation_period: typing.Optional[jsii.Number] = None,
        rotation_schedule: typing.Optional[builtins.str] = None,
        rotation_window: typing.Optional[jsii.Number] = None,
        service_account_email: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param credentials: JSON-encoded credentials to use to connect to GCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#credentials GcpSecretBackend#credentials}
        :param default_lease_ttl_seconds: Default lease duration for secrets in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#default_lease_ttl_seconds GcpSecretBackend#default_lease_ttl_seconds}
        :param description: Human-friendly description of the mount for the backend. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#description GcpSecretBackend#description}
        :param disable_automated_rotation: Stops rotation of the root credential until set to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#disable_automated_rotation GcpSecretBackend#disable_automated_rotation}
        :param disable_remount: If set, opts out of mount migration on path updates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#disable_remount GcpSecretBackend#disable_remount}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#id GcpSecretBackend#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity_token_audience: The audience claim value for plugin identity tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#identity_token_audience GcpSecretBackend#identity_token_audience}
        :param identity_token_key: The key to use for signing identity tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#identity_token_key GcpSecretBackend#identity_token_key}
        :param identity_token_ttl: The TTL of generated tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#identity_token_ttl GcpSecretBackend#identity_token_ttl}
        :param local: Local mount flag that can be explicitly set to true to enforce local mount in HA environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#local GcpSecretBackend#local}
        :param max_lease_ttl_seconds: Maximum possible lease duration for secrets in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#max_lease_ttl_seconds GcpSecretBackend#max_lease_ttl_seconds}
        :param namespace: Target namespace. (requires Enterprise). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#namespace GcpSecretBackend#namespace}
        :param path: Path to mount the backend at. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#path GcpSecretBackend#path}
        :param rotation_period: The period of time in seconds between each rotation of the root credential. Cannot be used with rotation_schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#rotation_period GcpSecretBackend#rotation_period}
        :param rotation_schedule: The cron-style schedule for the root credential to be rotated on. Cannot be used with rotation_period. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#rotation_schedule GcpSecretBackend#rotation_schedule}
        :param rotation_window: The maximum amount of time in seconds Vault is allowed to complete a rotation once a scheduled rotation is triggered. Can only be used with rotation_schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#rotation_window GcpSecretBackend#rotation_window}
        :param service_account_email: Service Account to impersonate for plugin workload identity federation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#service_account_email GcpSecretBackend#service_account_email}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca9d953c9e8ffb94a7d989922ca70c0064f22d263b8d67839464f56bf50f97d0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument default_lease_ttl_seconds", value=default_lease_ttl_seconds, expected_type=type_hints["default_lease_ttl_seconds"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_automated_rotation", value=disable_automated_rotation, expected_type=type_hints["disable_automated_rotation"])
            check_type(argname="argument disable_remount", value=disable_remount, expected_type=type_hints["disable_remount"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity_token_audience", value=identity_token_audience, expected_type=type_hints["identity_token_audience"])
            check_type(argname="argument identity_token_key", value=identity_token_key, expected_type=type_hints["identity_token_key"])
            check_type(argname="argument identity_token_ttl", value=identity_token_ttl, expected_type=type_hints["identity_token_ttl"])
            check_type(argname="argument local", value=local, expected_type=type_hints["local"])
            check_type(argname="argument max_lease_ttl_seconds", value=max_lease_ttl_seconds, expected_type=type_hints["max_lease_ttl_seconds"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument rotation_period", value=rotation_period, expected_type=type_hints["rotation_period"])
            check_type(argname="argument rotation_schedule", value=rotation_schedule, expected_type=type_hints["rotation_schedule"])
            check_type(argname="argument rotation_window", value=rotation_window, expected_type=type_hints["rotation_window"])
            check_type(argname="argument service_account_email", value=service_account_email, expected_type=type_hints["service_account_email"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if credentials is not None:
            self._values["credentials"] = credentials
        if default_lease_ttl_seconds is not None:
            self._values["default_lease_ttl_seconds"] = default_lease_ttl_seconds
        if description is not None:
            self._values["description"] = description
        if disable_automated_rotation is not None:
            self._values["disable_automated_rotation"] = disable_automated_rotation
        if disable_remount is not None:
            self._values["disable_remount"] = disable_remount
        if id is not None:
            self._values["id"] = id
        if identity_token_audience is not None:
            self._values["identity_token_audience"] = identity_token_audience
        if identity_token_key is not None:
            self._values["identity_token_key"] = identity_token_key
        if identity_token_ttl is not None:
            self._values["identity_token_ttl"] = identity_token_ttl
        if local is not None:
            self._values["local"] = local
        if max_lease_ttl_seconds is not None:
            self._values["max_lease_ttl_seconds"] = max_lease_ttl_seconds
        if namespace is not None:
            self._values["namespace"] = namespace
        if path is not None:
            self._values["path"] = path
        if rotation_period is not None:
            self._values["rotation_period"] = rotation_period
        if rotation_schedule is not None:
            self._values["rotation_schedule"] = rotation_schedule
        if rotation_window is not None:
            self._values["rotation_window"] = rotation_window
        if service_account_email is not None:
            self._values["service_account_email"] = service_account_email

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
    def credentials(self) -> typing.Optional[builtins.str]:
        '''JSON-encoded credentials to use to connect to GCP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#credentials GcpSecretBackend#credentials}
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_lease_ttl_seconds(self) -> typing.Optional[jsii.Number]:
        '''Default lease duration for secrets in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#default_lease_ttl_seconds GcpSecretBackend#default_lease_ttl_seconds}
        '''
        result = self._values.get("default_lease_ttl_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Human-friendly description of the mount for the backend.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#description GcpSecretBackend#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_automated_rotation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Stops rotation of the root credential until set to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#disable_automated_rotation GcpSecretBackend#disable_automated_rotation}
        '''
        result = self._values.get("disable_automated_rotation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_remount(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set, opts out of mount migration on path updates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#disable_remount GcpSecretBackend#disable_remount}
        '''
        result = self._values.get("disable_remount")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#id GcpSecretBackend#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_token_audience(self) -> typing.Optional[builtins.str]:
        '''The audience claim value for plugin identity tokens.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#identity_token_audience GcpSecretBackend#identity_token_audience}
        '''
        result = self._values.get("identity_token_audience")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_token_key(self) -> typing.Optional[builtins.str]:
        '''The key to use for signing identity tokens.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#identity_token_key GcpSecretBackend#identity_token_key}
        '''
        result = self._values.get("identity_token_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_token_ttl(self) -> typing.Optional[jsii.Number]:
        '''The TTL of generated tokens.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#identity_token_ttl GcpSecretBackend#identity_token_ttl}
        '''
        result = self._values.get("identity_token_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def local(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Local mount flag that can be explicitly set to true to enforce local mount in HA environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#local GcpSecretBackend#local}
        '''
        result = self._values.get("local")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_lease_ttl_seconds(self) -> typing.Optional[jsii.Number]:
        '''Maximum possible lease duration for secrets in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#max_lease_ttl_seconds GcpSecretBackend#max_lease_ttl_seconds}
        '''
        result = self._values.get("max_lease_ttl_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Target namespace. (requires Enterprise).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#namespace GcpSecretBackend#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to mount the backend at.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#path GcpSecretBackend#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rotation_period(self) -> typing.Optional[jsii.Number]:
        '''The period of time in seconds between each rotation of the root credential. Cannot be used with rotation_schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#rotation_period GcpSecretBackend#rotation_period}
        '''
        result = self._values.get("rotation_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rotation_schedule(self) -> typing.Optional[builtins.str]:
        '''The cron-style schedule for the root credential to be rotated on. Cannot be used with rotation_period.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#rotation_schedule GcpSecretBackend#rotation_schedule}
        '''
        result = self._values.get("rotation_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rotation_window(self) -> typing.Optional[jsii.Number]:
        '''The maximum amount of time in seconds Vault is allowed to complete a rotation once a scheduled rotation is triggered.

        Can only be used with rotation_schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#rotation_window GcpSecretBackend#rotation_window}
        '''
        result = self._values.get("rotation_window")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_account_email(self) -> typing.Optional[builtins.str]:
        '''Service Account to impersonate for plugin workload identity federation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/gcp_secret_backend#service_account_email GcpSecretBackend#service_account_email}
        '''
        result = self._values.get("service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GcpSecretBackendConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "GcpSecretBackend",
    "GcpSecretBackendConfig",
]

publication.publish()

def _typecheckingstub__40db0a4e2cf966c67b591ecb94db0b247b1d9fcf191fecfcc0664cfc5f035643(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    credentials: typing.Optional[builtins.str] = None,
    default_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    disable_automated_rotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_remount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity_token_audience: typing.Optional[builtins.str] = None,
    identity_token_key: typing.Optional[builtins.str] = None,
    identity_token_ttl: typing.Optional[jsii.Number] = None,
    local: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
    namespace: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    rotation_period: typing.Optional[jsii.Number] = None,
    rotation_schedule: typing.Optional[builtins.str] = None,
    rotation_window: typing.Optional[jsii.Number] = None,
    service_account_email: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__6851f53d856833878f9217c4b0e8666222669478e7bdadbabce5f0628200884c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0966d1fd1026edde85a0a00cf3165ee8e8ab9020e8a0f9881e1ccff2db478834(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e901f77fbff84573aa6dad40442948241bad273de4a0e311c3b2b9f9e39b67(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__590dc459289e0f2369fc44037f8b1b23f05edfda5399f766607d46357616fe42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be11550c7931de90b9c361b603c2a27a99f1586ca436f29c9db3572bd36cc491(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a921403de038496183927161bcc65d089c89329d016944f949b4f65fca00456(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5892aaf451c67107cf728068d60e12559a3aa22dda7a191de6ed8236b1fcd31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c662d86f4c3d46513d39156c3584817f573ef5c01415e40378ed3878cd88fd1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd05510363a83574e06d56f26a90b978003624f6a46b59d7d446688b425c660c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083ef131a616505c5ab3668f0e5ef5914562c1f4c9de3aeb73ce83f29f7990b6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd7f146590b25abf93eb4f57a594ceacaaa73be77a430c4df513517e889d05bd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad060922ef6dad970a19954b63daa678eb0f6b7cbeed4b5c54c96e1a725b42b4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__243f386ca13b344de5d5fe565a4a97ece8fb04151a8cdf4678e840091d781c40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3471734d1916c907c3d3aa2e46f9a8134a031939a26149739dbe3a0a4cb3538(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd7e762936c1cf7948030c6892ea82b0fbf30723035efbb457e45addf1a18d4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc17bfafde247c55e939fa9edb22b3b1072624d161dd79f961dd6c5a1e0afc12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e24de30e8e5f4e8d3e320712c80a55399212176ab7ead1f847b3425e5e5b94(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80261c97e504a6b8bd491761d98b8697f2a218bf02b1ee902ee4c54b429f3819(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca9d953c9e8ffb94a7d989922ca70c0064f22d263b8d67839464f56bf50f97d0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    credentials: typing.Optional[builtins.str] = None,
    default_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    disable_automated_rotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_remount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity_token_audience: typing.Optional[builtins.str] = None,
    identity_token_key: typing.Optional[builtins.str] = None,
    identity_token_ttl: typing.Optional[jsii.Number] = None,
    local: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
    namespace: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    rotation_period: typing.Optional[jsii.Number] = None,
    rotation_schedule: typing.Optional[builtins.str] = None,
    rotation_window: typing.Optional[jsii.Number] = None,
    service_account_email: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
