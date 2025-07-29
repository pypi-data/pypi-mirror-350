r'''
# `gitlab_group_protected_environment`

Refer to the Terraform Registry for docs: [`gitlab_group_protected_environment`](https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment).
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


class GroupProtectedEnvironment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.groupProtectedEnvironment.GroupProtectedEnvironment",
):
    '''Represents a {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment gitlab_group_protected_environment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        deploy_access_levels: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GroupProtectedEnvironmentDeployAccessLevels", typing.Dict[builtins.str, typing.Any]]]],
        environment: builtins.str,
        group: builtins.str,
        approval_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GroupProtectedEnvironmentApprovalRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment gitlab_group_protected_environment} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param deploy_access_levels: Array of access levels allowed to deploy, with each described by a hash. Elements in the ``deploy_access_levels`` should be one of ``user_id``, ``group_id`` or ``access_level``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#deploy_access_levels GroupProtectedEnvironment#deploy_access_levels}
        :param environment: The deployment tier of the environment. Valid values are ``production``, ``staging``, ``testing``, ``development``, ``other``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#environment GroupProtectedEnvironment#environment}
        :param group: The ID or full path of the group which the protected environment is created against. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#group GroupProtectedEnvironment#group}
        :param approval_rules: Array of approval rules to deploy, with each described by a hash. Elements in the ``approval_rules`` should be one of ``user_id``, ``group_id`` or ``access_level``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#approval_rules GroupProtectedEnvironment#approval_rules}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2adc328e10c572b1b25220c2681decce0fe30f5d8ef18225266ea6c7452c536)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = GroupProtectedEnvironmentConfig(
            deploy_access_levels=deploy_access_levels,
            environment=environment,
            group=group,
            approval_rules=approval_rules,
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
        '''Generates CDKTF code for importing a GroupProtectedEnvironment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GroupProtectedEnvironment to import.
        :param import_from_id: The id of the existing GroupProtectedEnvironment that should be imported. Refer to the {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GroupProtectedEnvironment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62b30e2b73028b4301e62c6dfd49110d857921823268b457944f617741bb7369)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putApprovalRules")
    def put_approval_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GroupProtectedEnvironmentApprovalRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8101d1b5a13774fdc4478efae93e930c4973f586923edffe32e4c2b43c676ece)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putApprovalRules", [value]))

    @jsii.member(jsii_name="putDeployAccessLevels")
    def put_deploy_access_levels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GroupProtectedEnvironmentDeployAccessLevels", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc6278e53a304a9031461175fb2bdf5dee1c47e0e022c3fae6733a30d754aa35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDeployAccessLevels", [value]))

    @jsii.member(jsii_name="resetApprovalRules")
    def reset_approval_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApprovalRules", []))

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
    @jsii.member(jsii_name="approvalRules")
    def approval_rules(self) -> "GroupProtectedEnvironmentApprovalRulesList":
        return typing.cast("GroupProtectedEnvironmentApprovalRulesList", jsii.get(self, "approvalRules"))

    @builtins.property
    @jsii.member(jsii_name="deployAccessLevels")
    def deploy_access_levels(self) -> "GroupProtectedEnvironmentDeployAccessLevelsList":
        return typing.cast("GroupProtectedEnvironmentDeployAccessLevelsList", jsii.get(self, "deployAccessLevels"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="approvalRulesInput")
    def approval_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GroupProtectedEnvironmentApprovalRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GroupProtectedEnvironmentApprovalRules"]]], jsii.get(self, "approvalRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="deployAccessLevelsInput")
    def deploy_access_levels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GroupProtectedEnvironmentDeployAccessLevels"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GroupProtectedEnvironmentDeployAccessLevels"]]], jsii.get(self, "deployAccessLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="groupInput")
    def group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupInput"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environment"))

    @environment.setter
    def environment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec517dfdb973aea341363e6d3757a04edaa2b66386be0f1697c3bb6159c2a1f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "group"))

    @group.setter
    def group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ab1a09db7c2e7ac97a88a277d32ab9c431a725a796cbca5127090d01a627842)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.groupProtectedEnvironment.GroupProtectedEnvironmentApprovalRules",
    jsii_struct_bases=[],
    name_mapping={
        "access_level": "accessLevel",
        "group_id": "groupId",
        "group_inheritance_type": "groupInheritanceType",
        "required_approvals": "requiredApprovals",
        "user_id": "userId",
    },
)
class GroupProtectedEnvironmentApprovalRules:
    def __init__(
        self,
        *,
        access_level: typing.Optional[builtins.str] = None,
        group_id: typing.Optional[jsii.Number] = None,
        group_inheritance_type: typing.Optional[jsii.Number] = None,
        required_approvals: typing.Optional[jsii.Number] = None,
        user_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param access_level: Levels of access allowed to approve a deployment to this protected environment. Mutually exclusive with ``user_id`` and ``group_id``. Valid values are ``developer``, ``maintainer``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#access_level GroupProtectedEnvironment#access_level}
        :param group_id: The ID of the group allowed to approve a deployment to this protected environment. TThe group must be a sub-group under the given group. Mutually exclusive with ``access_level`` and ``user_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#group_id GroupProtectedEnvironment#group_id}
        :param group_inheritance_type: Group inheritance allows access rules to take inherited group membership into account. Valid values are ``0``, ``1``. ``0`` => Direct group membership only, ``1`` => All inherited groups. Default: ``0`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#group_inheritance_type GroupProtectedEnvironment#group_inheritance_type}
        :param required_approvals: The number of approval required to allow deployment to this protected environment. This is mutually exclusive with user_id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#required_approvals GroupProtectedEnvironment#required_approvals}
        :param user_id: The ID of the user allowed to approve a deployment to this protected environment. The user must be a member of the group with Maintainer role or higher. Mutually exclusive with ``access_level`` and ``group_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#user_id GroupProtectedEnvironment#user_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c8192582acd0df1b27447268fc314096d6f0b3ae71bebbb8a97537c71b58614)
            check_type(argname="argument access_level", value=access_level, expected_type=type_hints["access_level"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument group_inheritance_type", value=group_inheritance_type, expected_type=type_hints["group_inheritance_type"])
            check_type(argname="argument required_approvals", value=required_approvals, expected_type=type_hints["required_approvals"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_level is not None:
            self._values["access_level"] = access_level
        if group_id is not None:
            self._values["group_id"] = group_id
        if group_inheritance_type is not None:
            self._values["group_inheritance_type"] = group_inheritance_type
        if required_approvals is not None:
            self._values["required_approvals"] = required_approvals
        if user_id is not None:
            self._values["user_id"] = user_id

    @builtins.property
    def access_level(self) -> typing.Optional[builtins.str]:
        '''Levels of access allowed to approve a deployment to this protected environment.

        Mutually exclusive with ``user_id`` and ``group_id``. Valid values are ``developer``, ``maintainer``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#access_level GroupProtectedEnvironment#access_level}
        '''
        result = self._values.get("access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of the group allowed to approve a deployment to this protected environment.

        TThe group must be a sub-group under the given group. Mutually exclusive with ``access_level`` and ``user_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#group_id GroupProtectedEnvironment#group_id}
        '''
        result = self._values.get("group_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def group_inheritance_type(self) -> typing.Optional[jsii.Number]:
        '''Group inheritance allows access rules to take inherited group membership into account.

        Valid values are ``0``, ``1``. ``0`` => Direct group membership only, ``1`` => All inherited groups. Default: ``0``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#group_inheritance_type GroupProtectedEnvironment#group_inheritance_type}
        '''
        result = self._values.get("group_inheritance_type")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def required_approvals(self) -> typing.Optional[jsii.Number]:
        '''The number of approval required to allow deployment to this protected environment. This is mutually exclusive with user_id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#required_approvals GroupProtectedEnvironment#required_approvals}
        '''
        result = self._values.get("required_approvals")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def user_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of the user allowed to approve a deployment to this protected environment.

        The user must be a member of the group with Maintainer role or higher. Mutually exclusive with ``access_level`` and ``group_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#user_id GroupProtectedEnvironment#user_id}
        '''
        result = self._values.get("user_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupProtectedEnvironmentApprovalRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupProtectedEnvironmentApprovalRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.groupProtectedEnvironment.GroupProtectedEnvironmentApprovalRulesList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a3bdc5687fbe90bcd78d73112ebc4663363cbb07cf16dcc9cf46990017ec0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GroupProtectedEnvironmentApprovalRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__646ba5fdbcc38ff15238ac7e0362ffebb1b99a6502cd48d18183b581cdfb452b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GroupProtectedEnvironmentApprovalRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1925e85672741dbeef190e5f4c578d5beeb57b3a6c8862d759e087d4cd28546)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4f543850ef8bec789d28089fa146483f2fbef722c7ecc02777f2c5881558f7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__408200df010fd9e66a03148bc9427058b5f7c099a6d6b1324a97e984ac3aad0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupProtectedEnvironmentApprovalRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupProtectedEnvironmentApprovalRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupProtectedEnvironmentApprovalRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08c244cbe0849af1fc4ff199fa5f3de277e823c38c1071dd67ee89e68358a38b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GroupProtectedEnvironmentApprovalRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.groupProtectedEnvironment.GroupProtectedEnvironmentApprovalRulesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63efffde48e6b97b8401e7c2045cdd3330e6fd1e9f976294e208367864edf6f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccessLevel")
    def reset_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessLevel", []))

    @jsii.member(jsii_name="resetGroupId")
    def reset_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupId", []))

    @jsii.member(jsii_name="resetGroupInheritanceType")
    def reset_group_inheritance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupInheritanceType", []))

    @jsii.member(jsii_name="resetRequiredApprovals")
    def reset_required_approvals(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredApprovals", []))

    @jsii.member(jsii_name="resetUserId")
    def reset_user_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserId", []))

    @builtins.property
    @jsii.member(jsii_name="accessLevelDescription")
    def access_level_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessLevelDescription"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="accessLevelInput")
    def access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="groupInheritanceTypeInput")
    def group_inheritance_type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "groupInheritanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredApprovalsInput")
    def required_approvals_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "requiredApprovalsInput"))

    @builtins.property
    @jsii.member(jsii_name="userIdInput")
    def user_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "userIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevel")
    def access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessLevel"))

    @access_level.setter
    def access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fda6b7ab07f81cb3c582615daf0b7a1d5b9146ef0e6bdba10d7e81c2c5753ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e2a8d86e612ffcbc0e8edbde2e6bed5547dccd0076a8bbf898ab6bc2c9c1158)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupInheritanceType")
    def group_inheritance_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "groupInheritanceType"))

    @group_inheritance_type.setter
    def group_inheritance_type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__771de75c9d0e30ceb40869917ee9d62194f186bcf36f24a8ad10bdaf5f0f054e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupInheritanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requiredApprovals")
    def required_approvals(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "requiredApprovals"))

    @required_approvals.setter
    def required_approvals(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a9840c085d9ae068e45a855bf6efec1190b4dafbfc2ef48ea01134cc9d36eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiredApprovals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "userId"))

    @user_id.setter
    def user_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1165ae1884299db0cd59448099a9917182a7eed8664bb88c67a998b59d702608)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GroupProtectedEnvironmentApprovalRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GroupProtectedEnvironmentApprovalRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GroupProtectedEnvironmentApprovalRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e18f32cd77580787c8226e76e17d2d54ff9d0dad7966de3b206a99b1097baaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.groupProtectedEnvironment.GroupProtectedEnvironmentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "deploy_access_levels": "deployAccessLevels",
        "environment": "environment",
        "group": "group",
        "approval_rules": "approvalRules",
    },
)
class GroupProtectedEnvironmentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        deploy_access_levels: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GroupProtectedEnvironmentDeployAccessLevels", typing.Dict[builtins.str, typing.Any]]]],
        environment: builtins.str,
        group: builtins.str,
        approval_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GroupProtectedEnvironmentApprovalRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param deploy_access_levels: Array of access levels allowed to deploy, with each described by a hash. Elements in the ``deploy_access_levels`` should be one of ``user_id``, ``group_id`` or ``access_level``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#deploy_access_levels GroupProtectedEnvironment#deploy_access_levels}
        :param environment: The deployment tier of the environment. Valid values are ``production``, ``staging``, ``testing``, ``development``, ``other``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#environment GroupProtectedEnvironment#environment}
        :param group: The ID or full path of the group which the protected environment is created against. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#group GroupProtectedEnvironment#group}
        :param approval_rules: Array of approval rules to deploy, with each described by a hash. Elements in the ``approval_rules`` should be one of ``user_id``, ``group_id`` or ``access_level``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#approval_rules GroupProtectedEnvironment#approval_rules}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15d82aeeb90fdebcc460e683715da244d27975bf298697484661a8ae0fb23f86)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument deploy_access_levels", value=deploy_access_levels, expected_type=type_hints["deploy_access_levels"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument approval_rules", value=approval_rules, expected_type=type_hints["approval_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "deploy_access_levels": deploy_access_levels,
            "environment": environment,
            "group": group,
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
        if approval_rules is not None:
            self._values["approval_rules"] = approval_rules

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
    def deploy_access_levels(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GroupProtectedEnvironmentDeployAccessLevels"]]:
        '''Array of access levels allowed to deploy, with each described by a hash.

        Elements in the ``deploy_access_levels`` should be one of ``user_id``, ``group_id`` or ``access_level``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#deploy_access_levels GroupProtectedEnvironment#deploy_access_levels}
        '''
        result = self._values.get("deploy_access_levels")
        assert result is not None, "Required property 'deploy_access_levels' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GroupProtectedEnvironmentDeployAccessLevels"]], result)

    @builtins.property
    def environment(self) -> builtins.str:
        '''The deployment tier of the environment.  Valid values are ``production``, ``staging``, ``testing``, ``development``, ``other``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#environment GroupProtectedEnvironment#environment}
        '''
        result = self._values.get("environment")
        assert result is not None, "Required property 'environment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group(self) -> builtins.str:
        '''The ID or full path of the group which the protected environment is created against.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#group GroupProtectedEnvironment#group}
        '''
        result = self._values.get("group")
        assert result is not None, "Required property 'group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def approval_rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupProtectedEnvironmentApprovalRules]]]:
        '''Array of approval rules to deploy, with each described by a hash.

        Elements in the ``approval_rules`` should be one of ``user_id``, ``group_id`` or ``access_level``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#approval_rules GroupProtectedEnvironment#approval_rules}
        '''
        result = self._values.get("approval_rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupProtectedEnvironmentApprovalRules]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupProtectedEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.groupProtectedEnvironment.GroupProtectedEnvironmentDeployAccessLevels",
    jsii_struct_bases=[],
    name_mapping={
        "access_level": "accessLevel",
        "group_id": "groupId",
        "group_inheritance_type": "groupInheritanceType",
        "user_id": "userId",
    },
)
class GroupProtectedEnvironmentDeployAccessLevels:
    def __init__(
        self,
        *,
        access_level: typing.Optional[builtins.str] = None,
        group_id: typing.Optional[jsii.Number] = None,
        group_inheritance_type: typing.Optional[jsii.Number] = None,
        user_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param access_level: Levels of access required to deploy to this protected environment. Mutually exclusive with ``user_id`` and ``group_id``. Valid values are ``developer``, ``maintainer``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#access_level GroupProtectedEnvironment#access_level}
        :param group_id: The ID of the group allowed to deploy to this protected environment. The group must be a sub-group under the given group. Mutually exclusive with ``access_level`` and ``user_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#group_id GroupProtectedEnvironment#group_id}
        :param group_inheritance_type: Group inheritance allows deploy access levels to take inherited group membership into account. Valid values are ``0``, ``1``. ``0`` => Direct group membership only, ``1`` => All inherited groups. Default: ``0`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#group_inheritance_type GroupProtectedEnvironment#group_inheritance_type}
        :param user_id: The ID of the user allowed to deploy to this protected environment. The user must be a member of the group with Maintainer role or higher. Mutually exclusive with ``access_level`` and ``group_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#user_id GroupProtectedEnvironment#user_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__decac2ec950305d365003dd84dfc2a1a7b401527d304545d75ef842b0dcde237)
            check_type(argname="argument access_level", value=access_level, expected_type=type_hints["access_level"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument group_inheritance_type", value=group_inheritance_type, expected_type=type_hints["group_inheritance_type"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_level is not None:
            self._values["access_level"] = access_level
        if group_id is not None:
            self._values["group_id"] = group_id
        if group_inheritance_type is not None:
            self._values["group_inheritance_type"] = group_inheritance_type
        if user_id is not None:
            self._values["user_id"] = user_id

    @builtins.property
    def access_level(self) -> typing.Optional[builtins.str]:
        '''Levels of access required to deploy to this protected environment.

        Mutually exclusive with ``user_id`` and ``group_id``. Valid values are ``developer``, ``maintainer``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#access_level GroupProtectedEnvironment#access_level}
        '''
        result = self._values.get("access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of the group allowed to deploy to this protected environment.

        The group must be a sub-group under the given group. Mutually exclusive with ``access_level`` and ``user_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#group_id GroupProtectedEnvironment#group_id}
        '''
        result = self._values.get("group_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def group_inheritance_type(self) -> typing.Optional[jsii.Number]:
        '''Group inheritance allows deploy access levels to take inherited group membership into account.

        Valid values are ``0``, ``1``. ``0`` => Direct group membership only, ``1`` => All inherited groups. Default: ``0``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#group_inheritance_type GroupProtectedEnvironment#group_inheritance_type}
        '''
        result = self._values.get("group_inheritance_type")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def user_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of the user allowed to deploy to this protected environment.

        The user must be a member of the group with Maintainer role or higher. Mutually exclusive with ``access_level`` and ``group_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group_protected_environment#user_id GroupProtectedEnvironment#user_id}
        '''
        result = self._values.get("user_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupProtectedEnvironmentDeployAccessLevels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupProtectedEnvironmentDeployAccessLevelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.groupProtectedEnvironment.GroupProtectedEnvironmentDeployAccessLevelsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18f863e2d24fb0fea623d8d4c75abc3dcd09580b16a89e41de8d65a54226442b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GroupProtectedEnvironmentDeployAccessLevelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99225fc6783bc479d260bb46189c441d0a7f1b4b3be3854b6eb016cfede16b74)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GroupProtectedEnvironmentDeployAccessLevelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe85d70231274b0c34aa0034194be76d8a1a3dc84368b517d430311d2f6bf017)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ea035233c5c6dd3a3573332d06fb27f6756c1817455d2e56a65bfff72456408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e29cb1d976abed7113cd72577a307405339d658cdc56bb841c1c4e7e5b79ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupProtectedEnvironmentDeployAccessLevels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupProtectedEnvironmentDeployAccessLevels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupProtectedEnvironmentDeployAccessLevels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d31b6b32831cc5410d486b12cdf7b6287d900730f9d38a30c9b91345d419405)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GroupProtectedEnvironmentDeployAccessLevelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.groupProtectedEnvironment.GroupProtectedEnvironmentDeployAccessLevelsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__910e077a941218d6289a47873be773b1860b6a5ab82d7e203f79800f01e930a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccessLevel")
    def reset_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessLevel", []))

    @jsii.member(jsii_name="resetGroupId")
    def reset_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupId", []))

    @jsii.member(jsii_name="resetGroupInheritanceType")
    def reset_group_inheritance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupInheritanceType", []))

    @jsii.member(jsii_name="resetUserId")
    def reset_user_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserId", []))

    @builtins.property
    @jsii.member(jsii_name="accessLevelDescription")
    def access_level_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessLevelDescription"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="accessLevelInput")
    def access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="groupInheritanceTypeInput")
    def group_inheritance_type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "groupInheritanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="userIdInput")
    def user_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "userIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevel")
    def access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessLevel"))

    @access_level.setter
    def access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15d4333afaf0adf8e57114fc04dda5279139350090c16af20443e1df8c95c21b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acd34a02b6889449bc5973302192bf8a844c1decfa58537710f132abe3c8d25d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupInheritanceType")
    def group_inheritance_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "groupInheritanceType"))

    @group_inheritance_type.setter
    def group_inheritance_type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__160c96917b8995cb2c336b41a47c4daccbce7c8f900ff52989dfa77468d98380)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupInheritanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "userId"))

    @user_id.setter
    def user_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__052b4b39788700c5c1e2bb236ed21cd1e55a5e43bc1a434359665e5fd7729f8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GroupProtectedEnvironmentDeployAccessLevels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GroupProtectedEnvironmentDeployAccessLevels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GroupProtectedEnvironmentDeployAccessLevels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f23c12d369f1e81d4b4b80c72edfda2f8a9fe1823716251aecf78a1cfbecad4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GroupProtectedEnvironment",
    "GroupProtectedEnvironmentApprovalRules",
    "GroupProtectedEnvironmentApprovalRulesList",
    "GroupProtectedEnvironmentApprovalRulesOutputReference",
    "GroupProtectedEnvironmentConfig",
    "GroupProtectedEnvironmentDeployAccessLevels",
    "GroupProtectedEnvironmentDeployAccessLevelsList",
    "GroupProtectedEnvironmentDeployAccessLevelsOutputReference",
]

publication.publish()

def _typecheckingstub__c2adc328e10c572b1b25220c2681decce0fe30f5d8ef18225266ea6c7452c536(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    deploy_access_levels: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GroupProtectedEnvironmentDeployAccessLevels, typing.Dict[builtins.str, typing.Any]]]],
    environment: builtins.str,
    group: builtins.str,
    approval_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GroupProtectedEnvironmentApprovalRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__62b30e2b73028b4301e62c6dfd49110d857921823268b457944f617741bb7369(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8101d1b5a13774fdc4478efae93e930c4973f586923edffe32e4c2b43c676ece(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GroupProtectedEnvironmentApprovalRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6278e53a304a9031461175fb2bdf5dee1c47e0e022c3fae6733a30d754aa35(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GroupProtectedEnvironmentDeployAccessLevels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec517dfdb973aea341363e6d3757a04edaa2b66386be0f1697c3bb6159c2a1f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab1a09db7c2e7ac97a88a277d32ab9c431a725a796cbca5127090d01a627842(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c8192582acd0df1b27447268fc314096d6f0b3ae71bebbb8a97537c71b58614(
    *,
    access_level: typing.Optional[builtins.str] = None,
    group_id: typing.Optional[jsii.Number] = None,
    group_inheritance_type: typing.Optional[jsii.Number] = None,
    required_approvals: typing.Optional[jsii.Number] = None,
    user_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a3bdc5687fbe90bcd78d73112ebc4663363cbb07cf16dcc9cf46990017ec0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__646ba5fdbcc38ff15238ac7e0362ffebb1b99a6502cd48d18183b581cdfb452b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1925e85672741dbeef190e5f4c578d5beeb57b3a6c8862d759e087d4cd28546(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f543850ef8bec789d28089fa146483f2fbef722c7ecc02777f2c5881558f7f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__408200df010fd9e66a03148bc9427058b5f7c099a6d6b1324a97e984ac3aad0f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c244cbe0849af1fc4ff199fa5f3de277e823c38c1071dd67ee89e68358a38b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupProtectedEnvironmentApprovalRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63efffde48e6b97b8401e7c2045cdd3330e6fd1e9f976294e208367864edf6f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fda6b7ab07f81cb3c582615daf0b7a1d5b9146ef0e6bdba10d7e81c2c5753ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2a8d86e612ffcbc0e8edbde2e6bed5547dccd0076a8bbf898ab6bc2c9c1158(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__771de75c9d0e30ceb40869917ee9d62194f186bcf36f24a8ad10bdaf5f0f054e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a9840c085d9ae068e45a855bf6efec1190b4dafbfc2ef48ea01134cc9d36eb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1165ae1884299db0cd59448099a9917182a7eed8664bb88c67a998b59d702608(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e18f32cd77580787c8226e76e17d2d54ff9d0dad7966de3b206a99b1097baaa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GroupProtectedEnvironmentApprovalRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d82aeeb90fdebcc460e683715da244d27975bf298697484661a8ae0fb23f86(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    deploy_access_levels: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GroupProtectedEnvironmentDeployAccessLevels, typing.Dict[builtins.str, typing.Any]]]],
    environment: builtins.str,
    group: builtins.str,
    approval_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GroupProtectedEnvironmentApprovalRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__decac2ec950305d365003dd84dfc2a1a7b401527d304545d75ef842b0dcde237(
    *,
    access_level: typing.Optional[builtins.str] = None,
    group_id: typing.Optional[jsii.Number] = None,
    group_inheritance_type: typing.Optional[jsii.Number] = None,
    user_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18f863e2d24fb0fea623d8d4c75abc3dcd09580b16a89e41de8d65a54226442b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99225fc6783bc479d260bb46189c441d0a7f1b4b3be3854b6eb016cfede16b74(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe85d70231274b0c34aa0034194be76d8a1a3dc84368b517d430311d2f6bf017(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea035233c5c6dd3a3573332d06fb27f6756c1817455d2e56a65bfff72456408(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e29cb1d976abed7113cd72577a307405339d658cdc56bb841c1c4e7e5b79ed(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d31b6b32831cc5410d486b12cdf7b6287d900730f9d38a30c9b91345d419405(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupProtectedEnvironmentDeployAccessLevels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__910e077a941218d6289a47873be773b1860b6a5ab82d7e203f79800f01e930a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d4333afaf0adf8e57114fc04dda5279139350090c16af20443e1df8c95c21b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd34a02b6889449bc5973302192bf8a844c1decfa58537710f132abe3c8d25d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__160c96917b8995cb2c336b41a47c4daccbce7c8f900ff52989dfa77468d98380(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052b4b39788700c5c1e2bb236ed21cd1e55a5e43bc1a434359665e5fd7729f8d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f23c12d369f1e81d4b4b80c72edfda2f8a9fe1823716251aecf78a1cfbecad4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GroupProtectedEnvironmentDeployAccessLevels]],
) -> None:
    """Type checking stubs"""
    pass
