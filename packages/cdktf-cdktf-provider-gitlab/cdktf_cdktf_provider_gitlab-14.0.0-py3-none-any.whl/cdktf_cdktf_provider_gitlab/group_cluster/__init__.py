r'''
# `gitlab_group_cluster`

Refer to the Terraform Registry for docs: [`gitlab_group_cluster`](https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster).
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


class GroupCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.groupCluster.GroupCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster gitlab_group_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        group: builtins.str,
        kubernetes_api_url: builtins.str,
        kubernetes_token: builtins.str,
        name: builtins.str,
        domain: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        environment_scope: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kubernetes_authorization_type: typing.Optional[builtins.str] = None,
        kubernetes_ca_cert: typing.Optional[builtins.str] = None,
        managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        management_project_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster gitlab_group_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param group: The id of the group to add the cluster to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#group GroupCluster#group}
        :param kubernetes_api_url: The URL to access the Kubernetes API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#kubernetes_api_url GroupCluster#kubernetes_api_url}
        :param kubernetes_token: The token to authenticate against Kubernetes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#kubernetes_token GroupCluster#kubernetes_token}
        :param name: The name of cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#name GroupCluster#name}
        :param domain: The base domain of the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#domain GroupCluster#domain}
        :param enabled: Determines if cluster is active or not. Defaults to ``true``. This attribute cannot be read. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#enabled GroupCluster#enabled}
        :param environment_scope: The associated environment to the cluster. Defaults to ``*``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#environment_scope GroupCluster#environment_scope}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#id GroupCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kubernetes_authorization_type: The cluster authorization type. Valid values are ``rbac``, ``abac``, ``unknown_authorization``. Defaults to ``rbac``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#kubernetes_authorization_type GroupCluster#kubernetes_authorization_type}
        :param kubernetes_ca_cert: TLS certificate (needed if API is using a self-signed TLS certificate). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#kubernetes_ca_cert GroupCluster#kubernetes_ca_cert}
        :param managed: Determines if cluster is managed by gitlab or not. Defaults to ``true``. This attribute cannot be read. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#managed GroupCluster#managed}
        :param management_project_id: The ID of the management project for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#management_project_id GroupCluster#management_project_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d0c00aec5b9057ca65354fd0bab38cf126ee7808772c16c7364ffb84dceaa1b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GroupClusterConfig(
            group=group,
            kubernetes_api_url=kubernetes_api_url,
            kubernetes_token=kubernetes_token,
            name=name,
            domain=domain,
            enabled=enabled,
            environment_scope=environment_scope,
            id=id,
            kubernetes_authorization_type=kubernetes_authorization_type,
            kubernetes_ca_cert=kubernetes_ca_cert,
            managed=managed,
            management_project_id=management_project_id,
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
        '''Generates CDKTF code for importing a GroupCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GroupCluster to import.
        :param import_from_id: The id of the existing GroupCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GroupCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e0e07567c3bb6fa1c70d3523501b50ee9392d8301725c0e6c82ce8c5e226e6c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetDomain")
    def reset_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomain", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEnvironmentScope")
    def reset_environment_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironmentScope", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKubernetesAuthorizationType")
    def reset_kubernetes_authorization_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubernetesAuthorizationType", []))

    @jsii.member(jsii_name="resetKubernetesCaCert")
    def reset_kubernetes_ca_cert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubernetesCaCert", []))

    @jsii.member(jsii_name="resetManaged")
    def reset_managed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManaged", []))

    @jsii.member(jsii_name="resetManagementProjectId")
    def reset_management_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagementProjectId", []))

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
    @jsii.member(jsii_name="clusterType")
    def cluster_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterType"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="platformType")
    def platform_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platformType"))

    @builtins.property
    @jsii.member(jsii_name="providerType")
    def provider_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerType"))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentScopeInput")
    def environment_scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="groupInput")
    def group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesApiUrlInput")
    def kubernetes_api_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubernetesApiUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesAuthorizationTypeInput")
    def kubernetes_authorization_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubernetesAuthorizationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesCaCertInput")
    def kubernetes_ca_cert_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubernetesCaCertInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesTokenInput")
    def kubernetes_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubernetesTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="managedInput")
    def managed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "managedInput"))

    @builtins.property
    @jsii.member(jsii_name="managementProjectIdInput")
    def management_project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managementProjectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c7bf97c17e31788e83ce50b0025ccda1a9f12f79362cd79882e476a76fbee22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96291d2f4ea83f905dbe65d7df8ab91545f7af8448718bd9fc7e6dd624823b75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environmentScope")
    def environment_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environmentScope"))

    @environment_scope.setter
    def environment_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01dc7cfe7e97840a7c3049a51b358acfddd1152a6dd2245a4c95bd2f420aac53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentScope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "group"))

    @group.setter
    def group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b293b059318f25232d25cd9dc93467b89a119551212b39c692ddc563b9594c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__063b16510348fd8cdc79940125779c69dfd29e17baf164688b1f568811ea9b41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kubernetesApiUrl")
    def kubernetes_api_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesApiUrl"))

    @kubernetes_api_url.setter
    def kubernetes_api_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__092b8684c2b305d3710dcc0ceda000a497d1aa1f58e05f5d75e380c56d014a6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubernetesApiUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kubernetesAuthorizationType")
    def kubernetes_authorization_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesAuthorizationType"))

    @kubernetes_authorization_type.setter
    def kubernetes_authorization_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7154e06d656c6f41d0bc0da622df4c78f62eb4583aa8216f7101ecd2c24f73ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubernetesAuthorizationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kubernetesCaCert")
    def kubernetes_ca_cert(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesCaCert"))

    @kubernetes_ca_cert.setter
    def kubernetes_ca_cert(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f18141c553f19c81fd7046b68e8a2bff3a4cd978ecfe02b833880664087c2aab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubernetesCaCert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kubernetesToken")
    def kubernetes_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesToken"))

    @kubernetes_token.setter
    def kubernetes_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce7dc8fe10bfd4c1cb0e352df0496e73cdb6cacfaaffd2d267031b58aba13b0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubernetesToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managed")
    def managed(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "managed"))

    @managed.setter
    def managed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9bf0948288dc6e9f256c3b0346e0be678d0341cd040b8c774492086cfa74174)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managementProjectId")
    def management_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managementProjectId"))

    @management_project_id.setter
    def management_project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79f8da4c80a385021e9cd27eb61c6d3f4c465a3cc4b9368c07c2ba76dd52d98c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managementProjectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f2ba294f1040502277fda3500f60ac3a34ec2902b22912e2cae3e2b0883e0b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.groupCluster.GroupClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "group": "group",
        "kubernetes_api_url": "kubernetesApiUrl",
        "kubernetes_token": "kubernetesToken",
        "name": "name",
        "domain": "domain",
        "enabled": "enabled",
        "environment_scope": "environmentScope",
        "id": "id",
        "kubernetes_authorization_type": "kubernetesAuthorizationType",
        "kubernetes_ca_cert": "kubernetesCaCert",
        "managed": "managed",
        "management_project_id": "managementProjectId",
    },
)
class GroupClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        group: builtins.str,
        kubernetes_api_url: builtins.str,
        kubernetes_token: builtins.str,
        name: builtins.str,
        domain: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        environment_scope: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kubernetes_authorization_type: typing.Optional[builtins.str] = None,
        kubernetes_ca_cert: typing.Optional[builtins.str] = None,
        managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        management_project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param group: The id of the group to add the cluster to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#group GroupCluster#group}
        :param kubernetes_api_url: The URL to access the Kubernetes API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#kubernetes_api_url GroupCluster#kubernetes_api_url}
        :param kubernetes_token: The token to authenticate against Kubernetes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#kubernetes_token GroupCluster#kubernetes_token}
        :param name: The name of cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#name GroupCluster#name}
        :param domain: The base domain of the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#domain GroupCluster#domain}
        :param enabled: Determines if cluster is active or not. Defaults to ``true``. This attribute cannot be read. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#enabled GroupCluster#enabled}
        :param environment_scope: The associated environment to the cluster. Defaults to ``*``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#environment_scope GroupCluster#environment_scope}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#id GroupCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kubernetes_authorization_type: The cluster authorization type. Valid values are ``rbac``, ``abac``, ``unknown_authorization``. Defaults to ``rbac``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#kubernetes_authorization_type GroupCluster#kubernetes_authorization_type}
        :param kubernetes_ca_cert: TLS certificate (needed if API is using a self-signed TLS certificate). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#kubernetes_ca_cert GroupCluster#kubernetes_ca_cert}
        :param managed: Determines if cluster is managed by gitlab or not. Defaults to ``true``. This attribute cannot be read. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#managed GroupCluster#managed}
        :param management_project_id: The ID of the management project for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#management_project_id GroupCluster#management_project_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7b3f1e40772d50199c0c635f98d3f57c556ec4e9cee31e4a9a3d1980a785f03)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument kubernetes_api_url", value=kubernetes_api_url, expected_type=type_hints["kubernetes_api_url"])
            check_type(argname="argument kubernetes_token", value=kubernetes_token, expected_type=type_hints["kubernetes_token"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument environment_scope", value=environment_scope, expected_type=type_hints["environment_scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kubernetes_authorization_type", value=kubernetes_authorization_type, expected_type=type_hints["kubernetes_authorization_type"])
            check_type(argname="argument kubernetes_ca_cert", value=kubernetes_ca_cert, expected_type=type_hints["kubernetes_ca_cert"])
            check_type(argname="argument managed", value=managed, expected_type=type_hints["managed"])
            check_type(argname="argument management_project_id", value=management_project_id, expected_type=type_hints["management_project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group": group,
            "kubernetes_api_url": kubernetes_api_url,
            "kubernetes_token": kubernetes_token,
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
        if domain is not None:
            self._values["domain"] = domain
        if enabled is not None:
            self._values["enabled"] = enabled
        if environment_scope is not None:
            self._values["environment_scope"] = environment_scope
        if id is not None:
            self._values["id"] = id
        if kubernetes_authorization_type is not None:
            self._values["kubernetes_authorization_type"] = kubernetes_authorization_type
        if kubernetes_ca_cert is not None:
            self._values["kubernetes_ca_cert"] = kubernetes_ca_cert
        if managed is not None:
            self._values["managed"] = managed
        if management_project_id is not None:
            self._values["management_project_id"] = management_project_id

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
    def group(self) -> builtins.str:
        '''The id of the group to add the cluster to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#group GroupCluster#group}
        '''
        result = self._values.get("group")
        assert result is not None, "Required property 'group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kubernetes_api_url(self) -> builtins.str:
        '''The URL to access the Kubernetes API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#kubernetes_api_url GroupCluster#kubernetes_api_url}
        '''
        result = self._values.get("kubernetes_api_url")
        assert result is not None, "Required property 'kubernetes_api_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kubernetes_token(self) -> builtins.str:
        '''The token to authenticate against Kubernetes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#kubernetes_token GroupCluster#kubernetes_token}
        '''
        result = self._values.get("kubernetes_token")
        assert result is not None, "Required property 'kubernetes_token' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#name GroupCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''The base domain of the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#domain GroupCluster#domain}
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines if cluster is active or not. Defaults to ``true``. This attribute cannot be read.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#enabled GroupCluster#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def environment_scope(self) -> typing.Optional[builtins.str]:
        '''The associated environment to the cluster. Defaults to ``*``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#environment_scope GroupCluster#environment_scope}
        '''
        result = self._values.get("environment_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#id GroupCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kubernetes_authorization_type(self) -> typing.Optional[builtins.str]:
        '''The cluster authorization type. Valid values are ``rbac``, ``abac``, ``unknown_authorization``. Defaults to ``rbac``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#kubernetes_authorization_type GroupCluster#kubernetes_authorization_type}
        '''
        result = self._values.get("kubernetes_authorization_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kubernetes_ca_cert(self) -> typing.Optional[builtins.str]:
        '''TLS certificate (needed if API is using a self-signed TLS certificate).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#kubernetes_ca_cert GroupCluster#kubernetes_ca_cert}
        '''
        result = self._values.get("kubernetes_ca_cert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines if cluster is managed by gitlab or not. Defaults to ``true``. This attribute cannot be read.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#managed GroupCluster#managed}
        '''
        result = self._values.get("managed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def management_project_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the management project for the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_cluster#management_project_id GroupCluster#management_project_id}
        '''
        result = self._values.get("management_project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "GroupCluster",
    "GroupClusterConfig",
]

publication.publish()

def _typecheckingstub__5d0c00aec5b9057ca65354fd0bab38cf126ee7808772c16c7364ffb84dceaa1b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    group: builtins.str,
    kubernetes_api_url: builtins.str,
    kubernetes_token: builtins.str,
    name: builtins.str,
    domain: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    environment_scope: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kubernetes_authorization_type: typing.Optional[builtins.str] = None,
    kubernetes_ca_cert: typing.Optional[builtins.str] = None,
    managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    management_project_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__6e0e07567c3bb6fa1c70d3523501b50ee9392d8301725c0e6c82ce8c5e226e6c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c7bf97c17e31788e83ce50b0025ccda1a9f12f79362cd79882e476a76fbee22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96291d2f4ea83f905dbe65d7df8ab91545f7af8448718bd9fc7e6dd624823b75(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01dc7cfe7e97840a7c3049a51b358acfddd1152a6dd2245a4c95bd2f420aac53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b293b059318f25232d25cd9dc93467b89a119551212b39c692ddc563b9594c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063b16510348fd8cdc79940125779c69dfd29e17baf164688b1f568811ea9b41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__092b8684c2b305d3710dcc0ceda000a497d1aa1f58e05f5d75e380c56d014a6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7154e06d656c6f41d0bc0da622df4c78f62eb4583aa8216f7101ecd2c24f73ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18141c553f19c81fd7046b68e8a2bff3a4cd978ecfe02b833880664087c2aab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce7dc8fe10bfd4c1cb0e352df0496e73cdb6cacfaaffd2d267031b58aba13b0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9bf0948288dc6e9f256c3b0346e0be678d0341cd040b8c774492086cfa74174(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f8da4c80a385021e9cd27eb61c6d3f4c465a3cc4b9368c07c2ba76dd52d98c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2ba294f1040502277fda3500f60ac3a34ec2902b22912e2cae3e2b0883e0b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b3f1e40772d50199c0c635f98d3f57c556ec4e9cee31e4a9a3d1980a785f03(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    group: builtins.str,
    kubernetes_api_url: builtins.str,
    kubernetes_token: builtins.str,
    name: builtins.str,
    domain: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    environment_scope: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kubernetes_authorization_type: typing.Optional[builtins.str] = None,
    kubernetes_ca_cert: typing.Optional[builtins.str] = None,
    managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    management_project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
