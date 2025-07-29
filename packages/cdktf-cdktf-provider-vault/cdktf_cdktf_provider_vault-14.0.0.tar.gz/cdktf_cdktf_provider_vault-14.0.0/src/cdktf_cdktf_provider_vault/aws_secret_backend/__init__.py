r'''
# `vault_aws_secret_backend`

Refer to the Terraform Registry for docs: [`vault_aws_secret_backend`](https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend).
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


class AwsSecretBackend(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.awsSecretBackend.AwsSecretBackend",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend vault_aws_secret_backend}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        access_key: typing.Optional[builtins.str] = None,
        default_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        disable_automated_rotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_remount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        iam_endpoint: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        identity_token_audience: typing.Optional[builtins.str] = None,
        identity_token_key: typing.Optional[builtins.str] = None,
        identity_token_ttl: typing.Optional[jsii.Number] = None,
        local: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
        namespace: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        rotation_period: typing.Optional[jsii.Number] = None,
        rotation_schedule: typing.Optional[builtins.str] = None,
        rotation_window: typing.Optional[jsii.Number] = None,
        secret_key: typing.Optional[builtins.str] = None,
        sts_endpoint: typing.Optional[builtins.str] = None,
        sts_fallback_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
        sts_fallback_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        sts_region: typing.Optional[builtins.str] = None,
        username_template: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend vault_aws_secret_backend} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param access_key: The AWS Access Key ID to use when generating new credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#access_key AwsSecretBackend#access_key}
        :param default_lease_ttl_seconds: Default lease duration for secrets in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#default_lease_ttl_seconds AwsSecretBackend#default_lease_ttl_seconds}
        :param description: Human-friendly description of the mount for the backend. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#description AwsSecretBackend#description}
        :param disable_automated_rotation: Stops rotation of the root credential until set to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#disable_automated_rotation AwsSecretBackend#disable_automated_rotation}
        :param disable_remount: If set, opts out of mount migration on path updates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#disable_remount AwsSecretBackend#disable_remount}
        :param iam_endpoint: Specifies a custom HTTP IAM endpoint to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#iam_endpoint AwsSecretBackend#iam_endpoint}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#id AwsSecretBackend#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity_token_audience: The audience claim value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#identity_token_audience AwsSecretBackend#identity_token_audience}
        :param identity_token_key: The key to use for signing identity tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#identity_token_key AwsSecretBackend#identity_token_key}
        :param identity_token_ttl: The TTL of generated identity tokens in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#identity_token_ttl AwsSecretBackend#identity_token_ttl}
        :param local: Specifies if the secret backend is local only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#local AwsSecretBackend#local}
        :param max_lease_ttl_seconds: Maximum possible lease duration for secrets in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#max_lease_ttl_seconds AwsSecretBackend#max_lease_ttl_seconds}
        :param namespace: Target namespace. (requires Enterprise). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#namespace AwsSecretBackend#namespace}
        :param path: Path to mount the backend at. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#path AwsSecretBackend#path}
        :param region: The AWS region to make API calls against. Defaults to us-east-1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#region AwsSecretBackend#region}
        :param role_arn: Role ARN to assume for plugin identity token federation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#role_arn AwsSecretBackend#role_arn}
        :param rotation_period: The period of time in seconds between each rotation of the root credential. Cannot be used with rotation_schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#rotation_period AwsSecretBackend#rotation_period}
        :param rotation_schedule: The cron-style schedule for the root credential to be rotated on. Cannot be used with rotation_period. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#rotation_schedule AwsSecretBackend#rotation_schedule}
        :param rotation_window: The maximum amount of time in seconds Vault is allowed to complete a rotation once a scheduled rotation is triggered. Can only be used with rotation_schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#rotation_window AwsSecretBackend#rotation_window}
        :param secret_key: The AWS Secret Access Key to use when generating new credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#secret_key AwsSecretBackend#secret_key}
        :param sts_endpoint: Specifies a custom HTTP STS endpoint to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#sts_endpoint AwsSecretBackend#sts_endpoint}
        :param sts_fallback_endpoints: Specifies a list of custom STS fallback endpoints to use (in order). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#sts_fallback_endpoints AwsSecretBackend#sts_fallback_endpoints}
        :param sts_fallback_regions: Specifies a list of custom STS fallback regions to use (in order). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#sts_fallback_regions AwsSecretBackend#sts_fallback_regions}
        :param sts_region: Specifies a custom STS region to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#sts_region AwsSecretBackend#sts_region}
        :param username_template: Template describing how dynamic usernames are generated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#username_template AwsSecretBackend#username_template}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e702e92e0d37483ecf5acde7f5d86551cb65c49046e3d10948876d689fd8caab)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AwsSecretBackendConfig(
            access_key=access_key,
            default_lease_ttl_seconds=default_lease_ttl_seconds,
            description=description,
            disable_automated_rotation=disable_automated_rotation,
            disable_remount=disable_remount,
            iam_endpoint=iam_endpoint,
            id=id,
            identity_token_audience=identity_token_audience,
            identity_token_key=identity_token_key,
            identity_token_ttl=identity_token_ttl,
            local=local,
            max_lease_ttl_seconds=max_lease_ttl_seconds,
            namespace=namespace,
            path=path,
            region=region,
            role_arn=role_arn,
            rotation_period=rotation_period,
            rotation_schedule=rotation_schedule,
            rotation_window=rotation_window,
            secret_key=secret_key,
            sts_endpoint=sts_endpoint,
            sts_fallback_endpoints=sts_fallback_endpoints,
            sts_fallback_regions=sts_fallback_regions,
            sts_region=sts_region,
            username_template=username_template,
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
        '''Generates CDKTF code for importing a AwsSecretBackend resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AwsSecretBackend to import.
        :param import_from_id: The id of the existing AwsSecretBackend that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AwsSecretBackend to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bbf6149cc942bff7252fcd9a29b15c5e6603909eebcb8f41a64f7efb3fa13a6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAccessKey")
    def reset_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessKey", []))

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

    @jsii.member(jsii_name="resetIamEndpoint")
    def reset_iam_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIamEndpoint", []))

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

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRoleArn")
    def reset_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoleArn", []))

    @jsii.member(jsii_name="resetRotationPeriod")
    def reset_rotation_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRotationPeriod", []))

    @jsii.member(jsii_name="resetRotationSchedule")
    def reset_rotation_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRotationSchedule", []))

    @jsii.member(jsii_name="resetRotationWindow")
    def reset_rotation_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRotationWindow", []))

    @jsii.member(jsii_name="resetSecretKey")
    def reset_secret_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretKey", []))

    @jsii.member(jsii_name="resetStsEndpoint")
    def reset_sts_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStsEndpoint", []))

    @jsii.member(jsii_name="resetStsFallbackEndpoints")
    def reset_sts_fallback_endpoints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStsFallbackEndpoints", []))

    @jsii.member(jsii_name="resetStsFallbackRegions")
    def reset_sts_fallback_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStsFallbackRegions", []))

    @jsii.member(jsii_name="resetStsRegion")
    def reset_sts_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStsRegion", []))

    @jsii.member(jsii_name="resetUsernameTemplate")
    def reset_username_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernameTemplate", []))

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
    @jsii.member(jsii_name="accessKeyInput")
    def access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKeyInput"))

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
    @jsii.member(jsii_name="iamEndpointInput")
    def iam_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamEndpointInput"))

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
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

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
    @jsii.member(jsii_name="secretKeyInput")
    def secret_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="stsEndpointInput")
    def sts_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stsEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="stsFallbackEndpointsInput")
    def sts_fallback_endpoints_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "stsFallbackEndpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="stsFallbackRegionsInput")
    def sts_fallback_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "stsFallbackRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="stsRegionInput")
    def sts_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stsRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameTemplateInput")
    def username_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKey")
    def access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessKey"))

    @access_key.setter
    def access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33db25a807aebf5fa573ebaef2d967d8193db78998ef58d32db28adf4fb4efbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultLeaseTtlSeconds")
    def default_lease_ttl_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultLeaseTtlSeconds"))

    @default_lease_ttl_seconds.setter
    def default_lease_ttl_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18bdcacfd30e0bddbd710a05f1313302188b6a66c07781172938e2ed5891c6fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLeaseTtlSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__516ed0d3071c00f75b21c7138c8f3c2c21df52c94ca2b856d82f6a7c3b0c9988)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1153849fe1b146b21baec8df429f4baff7cbd7f71781105de92a6af467739ef1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31c96ebef9866074b04bf0b685cd1aa73e78e26ff4404b7523659e4a3f5e182e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableRemount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iamEndpoint")
    def iam_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iamEndpoint"))

    @iam_endpoint.setter
    def iam_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ce321fe6191e76ad46797d07b9a5ac7d578a808bbf21d49d304d6022f8fe44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6108bfa9b61606bd745913e7eaf9852a829715d25840f8eddb25c8453f65e2da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityTokenAudience")
    def identity_token_audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityTokenAudience"))

    @identity_token_audience.setter
    def identity_token_audience(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc335de0d3d6662a49c5cfd60f3038e472143dffc58a13e7ff8d01526346b69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityTokenAudience", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityTokenKey")
    def identity_token_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityTokenKey"))

    @identity_token_key.setter
    def identity_token_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b944a6a00f5dd96d163aeea03f12ca9b4aab9d4b5dd4ea81ec40df6909ff054)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityTokenKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityTokenTtl")
    def identity_token_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "identityTokenTtl"))

    @identity_token_ttl.setter
    def identity_token_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__779799ae496c7be9971535cf4ce5bc8b41175c63028f9823269ba18bdf353570)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2840395e6a3705c6d2a8dc00a8ba6300cab1b7fda257c4fedea50ddcbfeab88a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "local", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxLeaseTtlSeconds")
    def max_lease_ttl_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxLeaseTtlSeconds"))

    @max_lease_ttl_seconds.setter
    def max_lease_ttl_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fa93f8e121967e8d381d882106075956973d013254f5da05157d595fad7bed6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxLeaseTtlSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__226529c12393c3b897d54cdce04c2564e0cb77919cf4056ad65122caac64a066)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea342e39d0c38f78884414953bb6ed75fc5fc91e5ecc22ba7189f27355fbdafc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b1c7b5b67cdde385c32b366729718ae30fed0bf2d8a8addc140900eb9fd03fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fe50d096eebf73a9dc2e3d0b3335a3a26c6837e3e263801b38b3771d30abbf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rotationPeriod")
    def rotation_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rotationPeriod"))

    @rotation_period.setter
    def rotation_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__045ce17547617ac316ad9279cb0a9d0e7b49444a4ae9561b3ca9707bc7a0c70c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rotationSchedule")
    def rotation_schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rotationSchedule"))

    @rotation_schedule.setter
    def rotation_schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23f7be7b2ce4b941863029b93f7c27f94f1ff9f6d136905278369c6717191492)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationSchedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rotationWindow")
    def rotation_window(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rotationWindow"))

    @rotation_window.setter
    def rotation_window(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73e35e7653b6e6ae4b4b99e7086a9d4b54c4b146205d509b790f712b924a530f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationWindow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretKey")
    def secret_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretKey"))

    @secret_key.setter
    def secret_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47de37c34ada6cd67548e26acc9d6837c62ec0e4448b0bc8de608a7d0ce7b87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stsEndpoint")
    def sts_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stsEndpoint"))

    @sts_endpoint.setter
    def sts_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f68a10cca758ed2d061447f2e04cd0485eccb04454d86a8a5df725983ca03c18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stsEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stsFallbackEndpoints")
    def sts_fallback_endpoints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stsFallbackEndpoints"))

    @sts_fallback_endpoints.setter
    def sts_fallback_endpoints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a98d5b40334571c4da1a03d6832789b71ad9e2828bdcf2700eece81902bde7b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stsFallbackEndpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stsFallbackRegions")
    def sts_fallback_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stsFallbackRegions"))

    @sts_fallback_regions.setter
    def sts_fallback_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f782ea49bf72e7dc9ddeb17b75b20f21c2246bb8e3aa6d31e609854d89e1c73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stsFallbackRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stsRegion")
    def sts_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stsRegion"))

    @sts_region.setter
    def sts_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83df76641ed20fdb6ef152447e90c7901db5f1d9e5fe58d41684d830f421fcf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stsRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="usernameTemplate")
    def username_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernameTemplate"))

    @username_template.setter
    def username_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2de3e10a47eae2326b717ba729f403037cb9e53604333a300b69c9430547e2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameTemplate", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.awsSecretBackend.AwsSecretBackendConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "access_key": "accessKey",
        "default_lease_ttl_seconds": "defaultLeaseTtlSeconds",
        "description": "description",
        "disable_automated_rotation": "disableAutomatedRotation",
        "disable_remount": "disableRemount",
        "iam_endpoint": "iamEndpoint",
        "id": "id",
        "identity_token_audience": "identityTokenAudience",
        "identity_token_key": "identityTokenKey",
        "identity_token_ttl": "identityTokenTtl",
        "local": "local",
        "max_lease_ttl_seconds": "maxLeaseTtlSeconds",
        "namespace": "namespace",
        "path": "path",
        "region": "region",
        "role_arn": "roleArn",
        "rotation_period": "rotationPeriod",
        "rotation_schedule": "rotationSchedule",
        "rotation_window": "rotationWindow",
        "secret_key": "secretKey",
        "sts_endpoint": "stsEndpoint",
        "sts_fallback_endpoints": "stsFallbackEndpoints",
        "sts_fallback_regions": "stsFallbackRegions",
        "sts_region": "stsRegion",
        "username_template": "usernameTemplate",
    },
)
class AwsSecretBackendConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        access_key: typing.Optional[builtins.str] = None,
        default_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        disable_automated_rotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_remount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        iam_endpoint: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        identity_token_audience: typing.Optional[builtins.str] = None,
        identity_token_key: typing.Optional[builtins.str] = None,
        identity_token_ttl: typing.Optional[jsii.Number] = None,
        local: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
        namespace: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        rotation_period: typing.Optional[jsii.Number] = None,
        rotation_schedule: typing.Optional[builtins.str] = None,
        rotation_window: typing.Optional[jsii.Number] = None,
        secret_key: typing.Optional[builtins.str] = None,
        sts_endpoint: typing.Optional[builtins.str] = None,
        sts_fallback_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
        sts_fallback_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        sts_region: typing.Optional[builtins.str] = None,
        username_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param access_key: The AWS Access Key ID to use when generating new credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#access_key AwsSecretBackend#access_key}
        :param default_lease_ttl_seconds: Default lease duration for secrets in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#default_lease_ttl_seconds AwsSecretBackend#default_lease_ttl_seconds}
        :param description: Human-friendly description of the mount for the backend. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#description AwsSecretBackend#description}
        :param disable_automated_rotation: Stops rotation of the root credential until set to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#disable_automated_rotation AwsSecretBackend#disable_automated_rotation}
        :param disable_remount: If set, opts out of mount migration on path updates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#disable_remount AwsSecretBackend#disable_remount}
        :param iam_endpoint: Specifies a custom HTTP IAM endpoint to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#iam_endpoint AwsSecretBackend#iam_endpoint}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#id AwsSecretBackend#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity_token_audience: The audience claim value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#identity_token_audience AwsSecretBackend#identity_token_audience}
        :param identity_token_key: The key to use for signing identity tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#identity_token_key AwsSecretBackend#identity_token_key}
        :param identity_token_ttl: The TTL of generated identity tokens in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#identity_token_ttl AwsSecretBackend#identity_token_ttl}
        :param local: Specifies if the secret backend is local only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#local AwsSecretBackend#local}
        :param max_lease_ttl_seconds: Maximum possible lease duration for secrets in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#max_lease_ttl_seconds AwsSecretBackend#max_lease_ttl_seconds}
        :param namespace: Target namespace. (requires Enterprise). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#namespace AwsSecretBackend#namespace}
        :param path: Path to mount the backend at. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#path AwsSecretBackend#path}
        :param region: The AWS region to make API calls against. Defaults to us-east-1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#region AwsSecretBackend#region}
        :param role_arn: Role ARN to assume for plugin identity token federation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#role_arn AwsSecretBackend#role_arn}
        :param rotation_period: The period of time in seconds between each rotation of the root credential. Cannot be used with rotation_schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#rotation_period AwsSecretBackend#rotation_period}
        :param rotation_schedule: The cron-style schedule for the root credential to be rotated on. Cannot be used with rotation_period. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#rotation_schedule AwsSecretBackend#rotation_schedule}
        :param rotation_window: The maximum amount of time in seconds Vault is allowed to complete a rotation once a scheduled rotation is triggered. Can only be used with rotation_schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#rotation_window AwsSecretBackend#rotation_window}
        :param secret_key: The AWS Secret Access Key to use when generating new credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#secret_key AwsSecretBackend#secret_key}
        :param sts_endpoint: Specifies a custom HTTP STS endpoint to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#sts_endpoint AwsSecretBackend#sts_endpoint}
        :param sts_fallback_endpoints: Specifies a list of custom STS fallback endpoints to use (in order). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#sts_fallback_endpoints AwsSecretBackend#sts_fallback_endpoints}
        :param sts_fallback_regions: Specifies a list of custom STS fallback regions to use (in order). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#sts_fallback_regions AwsSecretBackend#sts_fallback_regions}
        :param sts_region: Specifies a custom STS region to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#sts_region AwsSecretBackend#sts_region}
        :param username_template: Template describing how dynamic usernames are generated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#username_template AwsSecretBackend#username_template}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0072d1cb2fcd6ac0d634d6fddcffb8657b791d9773a1a8b6154dce38b5eb07a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument default_lease_ttl_seconds", value=default_lease_ttl_seconds, expected_type=type_hints["default_lease_ttl_seconds"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_automated_rotation", value=disable_automated_rotation, expected_type=type_hints["disable_automated_rotation"])
            check_type(argname="argument disable_remount", value=disable_remount, expected_type=type_hints["disable_remount"])
            check_type(argname="argument iam_endpoint", value=iam_endpoint, expected_type=type_hints["iam_endpoint"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity_token_audience", value=identity_token_audience, expected_type=type_hints["identity_token_audience"])
            check_type(argname="argument identity_token_key", value=identity_token_key, expected_type=type_hints["identity_token_key"])
            check_type(argname="argument identity_token_ttl", value=identity_token_ttl, expected_type=type_hints["identity_token_ttl"])
            check_type(argname="argument local", value=local, expected_type=type_hints["local"])
            check_type(argname="argument max_lease_ttl_seconds", value=max_lease_ttl_seconds, expected_type=type_hints["max_lease_ttl_seconds"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument rotation_period", value=rotation_period, expected_type=type_hints["rotation_period"])
            check_type(argname="argument rotation_schedule", value=rotation_schedule, expected_type=type_hints["rotation_schedule"])
            check_type(argname="argument rotation_window", value=rotation_window, expected_type=type_hints["rotation_window"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
            check_type(argname="argument sts_endpoint", value=sts_endpoint, expected_type=type_hints["sts_endpoint"])
            check_type(argname="argument sts_fallback_endpoints", value=sts_fallback_endpoints, expected_type=type_hints["sts_fallback_endpoints"])
            check_type(argname="argument sts_fallback_regions", value=sts_fallback_regions, expected_type=type_hints["sts_fallback_regions"])
            check_type(argname="argument sts_region", value=sts_region, expected_type=type_hints["sts_region"])
            check_type(argname="argument username_template", value=username_template, expected_type=type_hints["username_template"])
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
        if access_key is not None:
            self._values["access_key"] = access_key
        if default_lease_ttl_seconds is not None:
            self._values["default_lease_ttl_seconds"] = default_lease_ttl_seconds
        if description is not None:
            self._values["description"] = description
        if disable_automated_rotation is not None:
            self._values["disable_automated_rotation"] = disable_automated_rotation
        if disable_remount is not None:
            self._values["disable_remount"] = disable_remount
        if iam_endpoint is not None:
            self._values["iam_endpoint"] = iam_endpoint
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
        if region is not None:
            self._values["region"] = region
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if rotation_period is not None:
            self._values["rotation_period"] = rotation_period
        if rotation_schedule is not None:
            self._values["rotation_schedule"] = rotation_schedule
        if rotation_window is not None:
            self._values["rotation_window"] = rotation_window
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if sts_endpoint is not None:
            self._values["sts_endpoint"] = sts_endpoint
        if sts_fallback_endpoints is not None:
            self._values["sts_fallback_endpoints"] = sts_fallback_endpoints
        if sts_fallback_regions is not None:
            self._values["sts_fallback_regions"] = sts_fallback_regions
        if sts_region is not None:
            self._values["sts_region"] = sts_region
        if username_template is not None:
            self._values["username_template"] = username_template

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
    def access_key(self) -> typing.Optional[builtins.str]:
        '''The AWS Access Key ID to use when generating new credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#access_key AwsSecretBackend#access_key}
        '''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_lease_ttl_seconds(self) -> typing.Optional[jsii.Number]:
        '''Default lease duration for secrets in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#default_lease_ttl_seconds AwsSecretBackend#default_lease_ttl_seconds}
        '''
        result = self._values.get("default_lease_ttl_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Human-friendly description of the mount for the backend.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#description AwsSecretBackend#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_automated_rotation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Stops rotation of the root credential until set to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#disable_automated_rotation AwsSecretBackend#disable_automated_rotation}
        '''
        result = self._values.get("disable_automated_rotation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_remount(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set, opts out of mount migration on path updates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#disable_remount AwsSecretBackend#disable_remount}
        '''
        result = self._values.get("disable_remount")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def iam_endpoint(self) -> typing.Optional[builtins.str]:
        '''Specifies a custom HTTP IAM endpoint to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#iam_endpoint AwsSecretBackend#iam_endpoint}
        '''
        result = self._values.get("iam_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#id AwsSecretBackend#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_token_audience(self) -> typing.Optional[builtins.str]:
        '''The audience claim value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#identity_token_audience AwsSecretBackend#identity_token_audience}
        '''
        result = self._values.get("identity_token_audience")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_token_key(self) -> typing.Optional[builtins.str]:
        '''The key to use for signing identity tokens.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#identity_token_key AwsSecretBackend#identity_token_key}
        '''
        result = self._values.get("identity_token_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_token_ttl(self) -> typing.Optional[jsii.Number]:
        '''The TTL of generated identity tokens in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#identity_token_ttl AwsSecretBackend#identity_token_ttl}
        '''
        result = self._values.get("identity_token_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def local(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the secret backend is local only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#local AwsSecretBackend#local}
        '''
        result = self._values.get("local")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_lease_ttl_seconds(self) -> typing.Optional[jsii.Number]:
        '''Maximum possible lease duration for secrets in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#max_lease_ttl_seconds AwsSecretBackend#max_lease_ttl_seconds}
        '''
        result = self._values.get("max_lease_ttl_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Target namespace. (requires Enterprise).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#namespace AwsSecretBackend#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to mount the backend at.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#path AwsSecretBackend#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region to make API calls against. Defaults to us-east-1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#region AwsSecretBackend#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''Role ARN to assume for plugin identity token federation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#role_arn AwsSecretBackend#role_arn}
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rotation_period(self) -> typing.Optional[jsii.Number]:
        '''The period of time in seconds between each rotation of the root credential. Cannot be used with rotation_schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#rotation_period AwsSecretBackend#rotation_period}
        '''
        result = self._values.get("rotation_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rotation_schedule(self) -> typing.Optional[builtins.str]:
        '''The cron-style schedule for the root credential to be rotated on. Cannot be used with rotation_period.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#rotation_schedule AwsSecretBackend#rotation_schedule}
        '''
        result = self._values.get("rotation_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rotation_window(self) -> typing.Optional[jsii.Number]:
        '''The maximum amount of time in seconds Vault is allowed to complete a rotation once a scheduled rotation is triggered.

        Can only be used with rotation_schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#rotation_window AwsSecretBackend#rotation_window}
        '''
        result = self._values.get("rotation_window")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''The AWS Secret Access Key to use when generating new credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#secret_key AwsSecretBackend#secret_key}
        '''
        result = self._values.get("secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sts_endpoint(self) -> typing.Optional[builtins.str]:
        '''Specifies a custom HTTP STS endpoint to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#sts_endpoint AwsSecretBackend#sts_endpoint}
        '''
        result = self._values.get("sts_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sts_fallback_endpoints(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of custom STS fallback endpoints to use (in order).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#sts_fallback_endpoints AwsSecretBackend#sts_fallback_endpoints}
        '''
        result = self._values.get("sts_fallback_endpoints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sts_fallback_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of custom STS fallback regions to use (in order).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#sts_fallback_regions AwsSecretBackend#sts_fallback_regions}
        '''
        result = self._values.get("sts_fallback_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sts_region(self) -> typing.Optional[builtins.str]:
        '''Specifies a custom STS region to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#sts_region AwsSecretBackend#sts_region}
        '''
        result = self._values.get("sts_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username_template(self) -> typing.Optional[builtins.str]:
        '''Template describing how dynamic usernames are generated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/4.8.0/docs/resources/aws_secret_backend#username_template AwsSecretBackend#username_template}
        '''
        result = self._values.get("username_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsSecretBackendConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsSecretBackend",
    "AwsSecretBackendConfig",
]

publication.publish()

def _typecheckingstub__e702e92e0d37483ecf5acde7f5d86551cb65c49046e3d10948876d689fd8caab(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    access_key: typing.Optional[builtins.str] = None,
    default_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    disable_automated_rotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_remount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    iam_endpoint: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    identity_token_audience: typing.Optional[builtins.str] = None,
    identity_token_key: typing.Optional[builtins.str] = None,
    identity_token_ttl: typing.Optional[jsii.Number] = None,
    local: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
    namespace: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    rotation_period: typing.Optional[jsii.Number] = None,
    rotation_schedule: typing.Optional[builtins.str] = None,
    rotation_window: typing.Optional[jsii.Number] = None,
    secret_key: typing.Optional[builtins.str] = None,
    sts_endpoint: typing.Optional[builtins.str] = None,
    sts_fallback_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
    sts_fallback_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    sts_region: typing.Optional[builtins.str] = None,
    username_template: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__0bbf6149cc942bff7252fcd9a29b15c5e6603909eebcb8f41a64f7efb3fa13a6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33db25a807aebf5fa573ebaef2d967d8193db78998ef58d32db28adf4fb4efbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18bdcacfd30e0bddbd710a05f1313302188b6a66c07781172938e2ed5891c6fc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__516ed0d3071c00f75b21c7138c8f3c2c21df52c94ca2b856d82f6a7c3b0c9988(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1153849fe1b146b21baec8df429f4baff7cbd7f71781105de92a6af467739ef1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c96ebef9866074b04bf0b685cd1aa73e78e26ff4404b7523659e4a3f5e182e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ce321fe6191e76ad46797d07b9a5ac7d578a808bbf21d49d304d6022f8fe44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6108bfa9b61606bd745913e7eaf9852a829715d25840f8eddb25c8453f65e2da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc335de0d3d6662a49c5cfd60f3038e472143dffc58a13e7ff8d01526346b69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b944a6a00f5dd96d163aeea03f12ca9b4aab9d4b5dd4ea81ec40df6909ff054(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__779799ae496c7be9971535cf4ce5bc8b41175c63028f9823269ba18bdf353570(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2840395e6a3705c6d2a8dc00a8ba6300cab1b7fda257c4fedea50ddcbfeab88a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa93f8e121967e8d381d882106075956973d013254f5da05157d595fad7bed6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__226529c12393c3b897d54cdce04c2564e0cb77919cf4056ad65122caac64a066(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea342e39d0c38f78884414953bb6ed75fc5fc91e5ecc22ba7189f27355fbdafc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b1c7b5b67cdde385c32b366729718ae30fed0bf2d8a8addc140900eb9fd03fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe50d096eebf73a9dc2e3d0b3335a3a26c6837e3e263801b38b3771d30abbf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__045ce17547617ac316ad9279cb0a9d0e7b49444a4ae9561b3ca9707bc7a0c70c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23f7be7b2ce4b941863029b93f7c27f94f1ff9f6d136905278369c6717191492(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e35e7653b6e6ae4b4b99e7086a9d4b54c4b146205d509b790f712b924a530f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47de37c34ada6cd67548e26acc9d6837c62ec0e4448b0bc8de608a7d0ce7b87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f68a10cca758ed2d061447f2e04cd0485eccb04454d86a8a5df725983ca03c18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a98d5b40334571c4da1a03d6832789b71ad9e2828bdcf2700eece81902bde7b9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f782ea49bf72e7dc9ddeb17b75b20f21c2246bb8e3aa6d31e609854d89e1c73(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83df76641ed20fdb6ef152447e90c7901db5f1d9e5fe58d41684d830f421fcf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2de3e10a47eae2326b717ba729f403037cb9e53604333a300b69c9430547e2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0072d1cb2fcd6ac0d634d6fddcffb8657b791d9773a1a8b6154dce38b5eb07a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    access_key: typing.Optional[builtins.str] = None,
    default_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    disable_automated_rotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_remount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    iam_endpoint: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    identity_token_audience: typing.Optional[builtins.str] = None,
    identity_token_key: typing.Optional[builtins.str] = None,
    identity_token_ttl: typing.Optional[jsii.Number] = None,
    local: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
    namespace: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    rotation_period: typing.Optional[jsii.Number] = None,
    rotation_schedule: typing.Optional[builtins.str] = None,
    rotation_window: typing.Optional[jsii.Number] = None,
    secret_key: typing.Optional[builtins.str] = None,
    sts_endpoint: typing.Optional[builtins.str] = None,
    sts_fallback_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
    sts_fallback_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    sts_region: typing.Optional[builtins.str] = None,
    username_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
