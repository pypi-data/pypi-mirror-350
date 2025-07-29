r'''
# `gitlab_instance_cluster`

Refer to the Terraform Registry for docs: [`gitlab_instance_cluster`](https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster).
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


class InstanceCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.instanceCluster.InstanceCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster gitlab_instance_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        kubernetes_api_url: builtins.str,
        kubernetes_token: builtins.str,
        name: builtins.str,
        domain: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        environment_scope: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kubernetes_authorization_type: typing.Optional[builtins.str] = None,
        kubernetes_ca_cert: typing.Optional[builtins.str] = None,
        kubernetes_namespace: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster gitlab_instance_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param kubernetes_api_url: The URL to access the Kubernetes API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#kubernetes_api_url InstanceCluster#kubernetes_api_url}
        :param kubernetes_token: The token to authenticate against Kubernetes. This attribute cannot be read. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#kubernetes_token InstanceCluster#kubernetes_token}
        :param name: The name of cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#name InstanceCluster#name}
        :param domain: The base domain of the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#domain InstanceCluster#domain}
        :param enabled: Determines if cluster is active or not. Defaults to ``true``. This attribute cannot be read. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#enabled InstanceCluster#enabled}
        :param environment_scope: The associated environment to the cluster. Defaults to ``*``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#environment_scope InstanceCluster#environment_scope}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#id InstanceCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kubernetes_authorization_type: The cluster authorization type. Valid values are ``rbac``, ``abac``, ``unknown_authorization``. Defaults to ``rbac``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#kubernetes_authorization_type InstanceCluster#kubernetes_authorization_type}
        :param kubernetes_ca_cert: TLS certificate (needed if API is using a self-signed TLS certificate). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#kubernetes_ca_cert InstanceCluster#kubernetes_ca_cert}
        :param kubernetes_namespace: The unique namespace related to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#kubernetes_namespace InstanceCluster#kubernetes_namespace}
        :param managed: Determines if cluster is managed by gitlab or not. Defaults to ``true``. This attribute cannot be read. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#managed InstanceCluster#managed}
        :param management_project_id: The ID of the management project for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#management_project_id InstanceCluster#management_project_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa7afc23b1ef140b47e4035195fdbd0a52386e88e6647efb7f4975403208fd4e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = InstanceClusterConfig(
            kubernetes_api_url=kubernetes_api_url,
            kubernetes_token=kubernetes_token,
            name=name,
            domain=domain,
            enabled=enabled,
            environment_scope=environment_scope,
            id=id,
            kubernetes_authorization_type=kubernetes_authorization_type,
            kubernetes_ca_cert=kubernetes_ca_cert,
            kubernetes_namespace=kubernetes_namespace,
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
        '''Generates CDKTF code for importing a InstanceCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the InstanceCluster to import.
        :param import_from_id: The id of the existing InstanceCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the InstanceCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c35e39ef5c005b3911df25a47fd6cf39ec02f90a1fae33ba87f2d64259c8eac0)
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

    @jsii.member(jsii_name="resetKubernetesNamespace")
    def reset_kubernetes_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubernetesNamespace", []))

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
    @jsii.member(jsii_name="kubernetesNamespaceInput")
    def kubernetes_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubernetesNamespaceInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3dca0269355b420c61a20a9dcb0c064f0f687d655408a02279942156217969d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33c71fa67232e609081a9cdb194bf43ac18e07d8e09584e2d664264186ec4d3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environmentScope")
    def environment_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environmentScope"))

    @environment_scope.setter
    def environment_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7760012c73dd845dd8b27056bc061156db664f7df8d000710c96d225744dd02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentScope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c9c75e65c32dc4762c8d38c7b64b7f81615d94bae0227e9faa088e51c9c99cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kubernetesApiUrl")
    def kubernetes_api_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesApiUrl"))

    @kubernetes_api_url.setter
    def kubernetes_api_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c8a0496a1c9fe42d624a2384a68ac4c12140b3f38d299c73ca7133cb0180716)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubernetesApiUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kubernetesAuthorizationType")
    def kubernetes_authorization_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesAuthorizationType"))

    @kubernetes_authorization_type.setter
    def kubernetes_authorization_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a3ed57ca6ff36f417528121322d9b9b92a8f400896798c6831a130a175809d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubernetesAuthorizationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kubernetesCaCert")
    def kubernetes_ca_cert(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesCaCert"))

    @kubernetes_ca_cert.setter
    def kubernetes_ca_cert(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5291ed96df41abf6cedb96a7a575329c25cfec22e017b2df1ccb620ff5cc0ecb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubernetesCaCert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kubernetesNamespace")
    def kubernetes_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesNamespace"))

    @kubernetes_namespace.setter
    def kubernetes_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a7abd0c93c63b4fddc2aaca942e388a1f141016cfa0359cb31eeec771fbaef2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubernetesNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kubernetesToken")
    def kubernetes_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesToken"))

    @kubernetes_token.setter
    def kubernetes_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e30fd861aa700b1951d9a96a1f54608fcac24795f2dfc1cb2508bff1f15fe624)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c41c7baba98935195000826297bd34be0ba82d1804c2e516ac411106d5a7b90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managementProjectId")
    def management_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managementProjectId"))

    @management_project_id.setter
    def management_project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9982d43f4284a090152805d3a3ece7d51dcbea4511142b82fdd6be7139ebd62e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managementProjectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ee8e1733eaa17f21576bb56b0f096961f3a4dc96ec075ce995937fd3c7d37b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.instanceCluster.InstanceClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "kubernetes_api_url": "kubernetesApiUrl",
        "kubernetes_token": "kubernetesToken",
        "name": "name",
        "domain": "domain",
        "enabled": "enabled",
        "environment_scope": "environmentScope",
        "id": "id",
        "kubernetes_authorization_type": "kubernetesAuthorizationType",
        "kubernetes_ca_cert": "kubernetesCaCert",
        "kubernetes_namespace": "kubernetesNamespace",
        "managed": "managed",
        "management_project_id": "managementProjectId",
    },
)
class InstanceClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        kubernetes_api_url: builtins.str,
        kubernetes_token: builtins.str,
        name: builtins.str,
        domain: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        environment_scope: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kubernetes_authorization_type: typing.Optional[builtins.str] = None,
        kubernetes_ca_cert: typing.Optional[builtins.str] = None,
        kubernetes_namespace: typing.Optional[builtins.str] = None,
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
        :param kubernetes_api_url: The URL to access the Kubernetes API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#kubernetes_api_url InstanceCluster#kubernetes_api_url}
        :param kubernetes_token: The token to authenticate against Kubernetes. This attribute cannot be read. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#kubernetes_token InstanceCluster#kubernetes_token}
        :param name: The name of cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#name InstanceCluster#name}
        :param domain: The base domain of the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#domain InstanceCluster#domain}
        :param enabled: Determines if cluster is active or not. Defaults to ``true``. This attribute cannot be read. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#enabled InstanceCluster#enabled}
        :param environment_scope: The associated environment to the cluster. Defaults to ``*``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#environment_scope InstanceCluster#environment_scope}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#id InstanceCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kubernetes_authorization_type: The cluster authorization type. Valid values are ``rbac``, ``abac``, ``unknown_authorization``. Defaults to ``rbac``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#kubernetes_authorization_type InstanceCluster#kubernetes_authorization_type}
        :param kubernetes_ca_cert: TLS certificate (needed if API is using a self-signed TLS certificate). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#kubernetes_ca_cert InstanceCluster#kubernetes_ca_cert}
        :param kubernetes_namespace: The unique namespace related to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#kubernetes_namespace InstanceCluster#kubernetes_namespace}
        :param managed: Determines if cluster is managed by gitlab or not. Defaults to ``true``. This attribute cannot be read. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#managed InstanceCluster#managed}
        :param management_project_id: The ID of the management project for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#management_project_id InstanceCluster#management_project_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__183bbf8701c9ea7db5b547bb5f5c4cbaf8456e012d468f71c723848cc2b5343d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument kubernetes_api_url", value=kubernetes_api_url, expected_type=type_hints["kubernetes_api_url"])
            check_type(argname="argument kubernetes_token", value=kubernetes_token, expected_type=type_hints["kubernetes_token"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument environment_scope", value=environment_scope, expected_type=type_hints["environment_scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kubernetes_authorization_type", value=kubernetes_authorization_type, expected_type=type_hints["kubernetes_authorization_type"])
            check_type(argname="argument kubernetes_ca_cert", value=kubernetes_ca_cert, expected_type=type_hints["kubernetes_ca_cert"])
            check_type(argname="argument kubernetes_namespace", value=kubernetes_namespace, expected_type=type_hints["kubernetes_namespace"])
            check_type(argname="argument managed", value=managed, expected_type=type_hints["managed"])
            check_type(argname="argument management_project_id", value=management_project_id, expected_type=type_hints["management_project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if kubernetes_namespace is not None:
            self._values["kubernetes_namespace"] = kubernetes_namespace
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
    def kubernetes_api_url(self) -> builtins.str:
        '''The URL to access the Kubernetes API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#kubernetes_api_url InstanceCluster#kubernetes_api_url}
        '''
        result = self._values.get("kubernetes_api_url")
        assert result is not None, "Required property 'kubernetes_api_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kubernetes_token(self) -> builtins.str:
        '''The token to authenticate against Kubernetes. This attribute cannot be read.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#kubernetes_token InstanceCluster#kubernetes_token}
        '''
        result = self._values.get("kubernetes_token")
        assert result is not None, "Required property 'kubernetes_token' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#name InstanceCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''The base domain of the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#domain InstanceCluster#domain}
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines if cluster is active or not. Defaults to ``true``. This attribute cannot be read.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#enabled InstanceCluster#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def environment_scope(self) -> typing.Optional[builtins.str]:
        '''The associated environment to the cluster. Defaults to ``*``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#environment_scope InstanceCluster#environment_scope}
        '''
        result = self._values.get("environment_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#id InstanceCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kubernetes_authorization_type(self) -> typing.Optional[builtins.str]:
        '''The cluster authorization type. Valid values are ``rbac``, ``abac``, ``unknown_authorization``. Defaults to ``rbac``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#kubernetes_authorization_type InstanceCluster#kubernetes_authorization_type}
        '''
        result = self._values.get("kubernetes_authorization_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kubernetes_ca_cert(self) -> typing.Optional[builtins.str]:
        '''TLS certificate (needed if API is using a self-signed TLS certificate).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#kubernetes_ca_cert InstanceCluster#kubernetes_ca_cert}
        '''
        result = self._values.get("kubernetes_ca_cert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kubernetes_namespace(self) -> typing.Optional[builtins.str]:
        '''The unique namespace related to the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#kubernetes_namespace InstanceCluster#kubernetes_namespace}
        '''
        result = self._values.get("kubernetes_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines if cluster is managed by gitlab or not. Defaults to ``true``. This attribute cannot be read.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#managed InstanceCluster#managed}
        '''
        result = self._values.get("managed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def management_project_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the management project for the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/instance_cluster#management_project_id InstanceCluster#management_project_id}
        '''
        result = self._values.get("management_project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InstanceClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "InstanceCluster",
    "InstanceClusterConfig",
]

publication.publish()

def _typecheckingstub__fa7afc23b1ef140b47e4035195fdbd0a52386e88e6647efb7f4975403208fd4e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    kubernetes_api_url: builtins.str,
    kubernetes_token: builtins.str,
    name: builtins.str,
    domain: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    environment_scope: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kubernetes_authorization_type: typing.Optional[builtins.str] = None,
    kubernetes_ca_cert: typing.Optional[builtins.str] = None,
    kubernetes_namespace: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__c35e39ef5c005b3911df25a47fd6cf39ec02f90a1fae33ba87f2d64259c8eac0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dca0269355b420c61a20a9dcb0c064f0f687d655408a02279942156217969d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c71fa67232e609081a9cdb194bf43ac18e07d8e09584e2d664264186ec4d3e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7760012c73dd845dd8b27056bc061156db664f7df8d000710c96d225744dd02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9c75e65c32dc4762c8d38c7b64b7f81615d94bae0227e9faa088e51c9c99cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c8a0496a1c9fe42d624a2384a68ac4c12140b3f38d299c73ca7133cb0180716(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a3ed57ca6ff36f417528121322d9b9b92a8f400896798c6831a130a175809d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5291ed96df41abf6cedb96a7a575329c25cfec22e017b2df1ccb620ff5cc0ecb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7abd0c93c63b4fddc2aaca942e388a1f141016cfa0359cb31eeec771fbaef2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e30fd861aa700b1951d9a96a1f54608fcac24795f2dfc1cb2508bff1f15fe624(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c41c7baba98935195000826297bd34be0ba82d1804c2e516ac411106d5a7b90(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9982d43f4284a090152805d3a3ece7d51dcbea4511142b82fdd6be7139ebd62e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee8e1733eaa17f21576bb56b0f096961f3a4dc96ec075ce995937fd3c7d37b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183bbf8701c9ea7db5b547bb5f5c4cbaf8456e012d468f71c723848cc2b5343d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    kubernetes_api_url: builtins.str,
    kubernetes_token: builtins.str,
    name: builtins.str,
    domain: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    environment_scope: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kubernetes_authorization_type: typing.Optional[builtins.str] = None,
    kubernetes_ca_cert: typing.Optional[builtins.str] = None,
    kubernetes_namespace: typing.Optional[builtins.str] = None,
    managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    management_project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
