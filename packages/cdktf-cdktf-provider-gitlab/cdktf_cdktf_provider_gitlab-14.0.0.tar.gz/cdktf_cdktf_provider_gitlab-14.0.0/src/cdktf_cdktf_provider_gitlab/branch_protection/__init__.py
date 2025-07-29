r'''
# `gitlab_branch_protection`

Refer to the Terraform Registry for docs: [`gitlab_branch_protection`](https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection).
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


class BranchProtection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.branchProtection.BranchProtection",
):
    '''Represents a {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection gitlab_branch_protection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        branch: builtins.str,
        project: builtins.str,
        allowed_to_merge: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BranchProtectionAllowedToMerge", typing.Dict[builtins.str, typing.Any]]]]] = None,
        allowed_to_push: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BranchProtectionAllowedToPush", typing.Dict[builtins.str, typing.Any]]]]] = None,
        allowed_to_unprotect: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BranchProtectionAllowedToUnprotect", typing.Dict[builtins.str, typing.Any]]]]] = None,
        allow_force_push: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        code_owner_approval_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        merge_access_level: typing.Optional[builtins.str] = None,
        push_access_level: typing.Optional[builtins.str] = None,
        unprotect_access_level: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection gitlab_branch_protection} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param branch: Name of the branch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#branch BranchProtection#branch}
        :param project: The id of the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#project BranchProtection#project}
        :param allowed_to_merge: allowed_to_merge block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#allowed_to_merge BranchProtection#allowed_to_merge}
        :param allowed_to_push: allowed_to_push block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#allowed_to_push BranchProtection#allowed_to_push}
        :param allowed_to_unprotect: allowed_to_unprotect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#allowed_to_unprotect BranchProtection#allowed_to_unprotect}
        :param allow_force_push: Can be set to true to allow users with push access to force push. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#allow_force_push BranchProtection#allow_force_push}
        :param code_owner_approval_required: Can be set to true to require code owner approval before merging. Only available for Premium and Ultimate instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#code_owner_approval_required BranchProtection#code_owner_approval_required}
        :param merge_access_level: Access levels allowed to merge. Valid values are: ``no one``, ``developer``, ``maintainer``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#merge_access_level BranchProtection#merge_access_level}
        :param push_access_level: Access levels allowed to push. Valid values are: ``no one``, ``developer``, ``maintainer``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#push_access_level BranchProtection#push_access_level}
        :param unprotect_access_level: Access levels allowed to unprotect. Valid values are: ``developer``, ``maintainer``, ``admin``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#unprotect_access_level BranchProtection#unprotect_access_level}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b2f0b7f1af00493894fe672adaa934a38a934975c0f5faee023936ebc3e3f97)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = BranchProtectionConfig(
            branch=branch,
            project=project,
            allowed_to_merge=allowed_to_merge,
            allowed_to_push=allowed_to_push,
            allowed_to_unprotect=allowed_to_unprotect,
            allow_force_push=allow_force_push,
            code_owner_approval_required=code_owner_approval_required,
            merge_access_level=merge_access_level,
            push_access_level=push_access_level,
            unprotect_access_level=unprotect_access_level,
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
        '''Generates CDKTF code for importing a BranchProtection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BranchProtection to import.
        :param import_from_id: The id of the existing BranchProtection that should be imported. Refer to the {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BranchProtection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfc5d7813a00a6350cfcc5332af41f071df32107af5006207dfed9af2fcf516d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAllowedToMerge")
    def put_allowed_to_merge(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BranchProtectionAllowedToMerge", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74fc06ce074d208c04307f39b2c5b7843b284c1731846b8a6e3d51ff844ffa51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllowedToMerge", [value]))

    @jsii.member(jsii_name="putAllowedToPush")
    def put_allowed_to_push(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BranchProtectionAllowedToPush", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a01d951730ce0463c0517d5549455e9f04519bb846f3c585500babf9d6fb2526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllowedToPush", [value]))

    @jsii.member(jsii_name="putAllowedToUnprotect")
    def put_allowed_to_unprotect(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BranchProtectionAllowedToUnprotect", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c6683079cd935c8e1ed218d2bb0697cd2698cc31e018362f5b44bf099b1c12e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllowedToUnprotect", [value]))

    @jsii.member(jsii_name="resetAllowedToMerge")
    def reset_allowed_to_merge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedToMerge", []))

    @jsii.member(jsii_name="resetAllowedToPush")
    def reset_allowed_to_push(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedToPush", []))

    @jsii.member(jsii_name="resetAllowedToUnprotect")
    def reset_allowed_to_unprotect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedToUnprotect", []))

    @jsii.member(jsii_name="resetAllowForcePush")
    def reset_allow_force_push(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowForcePush", []))

    @jsii.member(jsii_name="resetCodeOwnerApprovalRequired")
    def reset_code_owner_approval_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodeOwnerApprovalRequired", []))

    @jsii.member(jsii_name="resetMergeAccessLevel")
    def reset_merge_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergeAccessLevel", []))

    @jsii.member(jsii_name="resetPushAccessLevel")
    def reset_push_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPushAccessLevel", []))

    @jsii.member(jsii_name="resetUnprotectAccessLevel")
    def reset_unprotect_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnprotectAccessLevel", []))

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
    @jsii.member(jsii_name="allowedToMerge")
    def allowed_to_merge(self) -> "BranchProtectionAllowedToMergeList":
        return typing.cast("BranchProtectionAllowedToMergeList", jsii.get(self, "allowedToMerge"))

    @builtins.property
    @jsii.member(jsii_name="allowedToPush")
    def allowed_to_push(self) -> "BranchProtectionAllowedToPushList":
        return typing.cast("BranchProtectionAllowedToPushList", jsii.get(self, "allowedToPush"))

    @builtins.property
    @jsii.member(jsii_name="allowedToUnprotect")
    def allowed_to_unprotect(self) -> "BranchProtectionAllowedToUnprotectList":
        return typing.cast("BranchProtectionAllowedToUnprotectList", jsii.get(self, "allowedToUnprotect"))

    @builtins.property
    @jsii.member(jsii_name="branchProtectionId")
    def branch_protection_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "branchProtectionId"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="allowedToMergeInput")
    def allowed_to_merge_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BranchProtectionAllowedToMerge"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BranchProtectionAllowedToMerge"]]], jsii.get(self, "allowedToMergeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedToPushInput")
    def allowed_to_push_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BranchProtectionAllowedToPush"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BranchProtectionAllowedToPush"]]], jsii.get(self, "allowedToPushInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedToUnprotectInput")
    def allowed_to_unprotect_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BranchProtectionAllowedToUnprotect"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BranchProtectionAllowedToUnprotect"]]], jsii.get(self, "allowedToUnprotectInput"))

    @builtins.property
    @jsii.member(jsii_name="allowForcePushInput")
    def allow_force_push_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowForcePushInput"))

    @builtins.property
    @jsii.member(jsii_name="branchInput")
    def branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchInput"))

    @builtins.property
    @jsii.member(jsii_name="codeOwnerApprovalRequiredInput")
    def code_owner_approval_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "codeOwnerApprovalRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="mergeAccessLevelInput")
    def merge_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mergeAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="pushAccessLevelInput")
    def push_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pushAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="unprotectAccessLevelInput")
    def unprotect_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unprotectAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="allowForcePush")
    def allow_force_push(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowForcePush"))

    @allow_force_push.setter
    def allow_force_push(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad5558ebaa86f37b7a6f08b2f1b92258892991923506fcc41d56e2618bdbfd0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowForcePush", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="branch")
    def branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branch"))

    @branch.setter
    def branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f53743344ac12eaec8374256b285c732decc1315a674d7af0178ecab1a0bb5a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="codeOwnerApprovalRequired")
    def code_owner_approval_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "codeOwnerApprovalRequired"))

    @code_owner_approval_required.setter
    def code_owner_approval_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bac89ac79f24e15bb33171db48a46f5c78ec8a5979a0de26b1f5ea097f04d233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codeOwnerApprovalRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mergeAccessLevel")
    def merge_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mergeAccessLevel"))

    @merge_access_level.setter
    def merge_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__798090e920e5d7595996d0105593c329531ef84653f5a158848b811cff2c2b6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mergeAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd08961a00fe0f04b805df4750da9d87a17c99a4cd505f4168b62af5db29501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pushAccessLevel")
    def push_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pushAccessLevel"))

    @push_access_level.setter
    def push_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a93342b0133d8ac60fcaa8236e0f65cc2ee15e36ea066fc6de3e1d4833a54a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pushAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unprotectAccessLevel")
    def unprotect_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unprotectAccessLevel"))

    @unprotect_access_level.setter
    def unprotect_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8519fe5ef3fb2188f9aba6057ae4bb64c074b6dad603d31f7cdd4f2646ddf4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unprotectAccessLevel", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.branchProtection.BranchProtectionAllowedToMerge",
    jsii_struct_bases=[],
    name_mapping={"group_id": "groupId", "user_id": "userId"},
)
class BranchProtectionAllowedToMerge:
    def __init__(
        self,
        *,
        group_id: typing.Optional[jsii.Number] = None,
        user_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param group_id: The ID of a GitLab group allowed to perform the relevant action. Mutually exclusive with ``user_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#group_id BranchProtection#group_id}
        :param user_id: The ID of a GitLab user allowed to perform the relevant action. Mutually exclusive with ``group_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#user_id BranchProtection#user_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f10bc5fb1df6e438ff8f8ed2004a19bfdf8dd675140f2e64bca9c88e2eace03b)
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_id is not None:
            self._values["group_id"] = group_id
        if user_id is not None:
            self._values["user_id"] = user_id

    @builtins.property
    def group_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of a GitLab group allowed to perform the relevant action. Mutually exclusive with ``user_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#group_id BranchProtection#group_id}
        '''
        result = self._values.get("group_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def user_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of a GitLab user allowed to perform the relevant action. Mutually exclusive with ``group_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#user_id BranchProtection#user_id}
        '''
        result = self._values.get("user_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchProtectionAllowedToMerge(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BranchProtectionAllowedToMergeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.branchProtection.BranchProtectionAllowedToMergeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc17a8b8af71491999c2bbdfe458cc6e24ba2e8fb0cd570a9b11909c35dc919e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BranchProtectionAllowedToMergeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__570434eccfc44fa69e9974533d00f5a620874ae2899f6f2be7fd757e7be6a949)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BranchProtectionAllowedToMergeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a2ec216cdfd09d9d6a3f54b4a27d7e007225105d697d2a47bfc06e3f170393c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__649719a621cb0d999080963eb730668b15198e461c7a1dd64e6b9a83f69ed83f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22abd01a70a82606895565dcf146a479f5578a362a219672f1ad905c1f96c14a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionAllowedToMerge]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionAllowedToMerge]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionAllowedToMerge]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26b6bf75c3bf37e7c82e5da45dc9443333b3ea371f89b1ae9d8b86f55e93237e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BranchProtectionAllowedToMergeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.branchProtection.BranchProtectionAllowedToMergeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14005d99a812ce7afc16f3b9cd69990f93f44c15b5d9560f22d33efa874e86aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetGroupId")
    def reset_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupId", []))

    @jsii.member(jsii_name="resetUserId")
    def reset_user_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserId", []))

    @builtins.property
    @jsii.member(jsii_name="accessLevel")
    def access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessLevel"))

    @builtins.property
    @jsii.member(jsii_name="accessLevelDescription")
    def access_level_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessLevelDescription"))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userIdInput")
    def user_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "userIdInput"))

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02bd9257561d4a85c0c5139cc95dadd0fdf3cc8a74d7183548c0e2232a82cb3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "userId"))

    @user_id.setter
    def user_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57c0b60e8a6779b32c7cdf10682ccc3da5e70d0457eddcf7aadd06f497ee1a82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionAllowedToMerge]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionAllowedToMerge]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionAllowedToMerge]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0722d16e6467cbd718b5c98495a2a01836bdd79abd4eef9684af93d76d186e17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.branchProtection.BranchProtectionAllowedToPush",
    jsii_struct_bases=[],
    name_mapping={
        "deploy_key_id": "deployKeyId",
        "group_id": "groupId",
        "user_id": "userId",
    },
)
class BranchProtectionAllowedToPush:
    def __init__(
        self,
        *,
        deploy_key_id: typing.Optional[jsii.Number] = None,
        group_id: typing.Optional[jsii.Number] = None,
        user_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param deploy_key_id: The ID of a GitLab deploy key allowed to perform the relevant action. Mutually exclusive with ``group_id`` and ``user_id``. This field is read-only until Gitlab 17.5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#deploy_key_id BranchProtection#deploy_key_id}
        :param group_id: The ID of a GitLab group allowed to perform the relevant action. Mutually exclusive with ``deploy_key_id`` and ``user_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#group_id BranchProtection#group_id}
        :param user_id: The ID of a GitLab user allowed to perform the relevant action. Mutually exclusive with ``deploy_key_id`` and ``group_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#user_id BranchProtection#user_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a23e6d56a63eb734fe66bc994bb0cbeaaa38774a96d984b255416d994a67add)
            check_type(argname="argument deploy_key_id", value=deploy_key_id, expected_type=type_hints["deploy_key_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deploy_key_id is not None:
            self._values["deploy_key_id"] = deploy_key_id
        if group_id is not None:
            self._values["group_id"] = group_id
        if user_id is not None:
            self._values["user_id"] = user_id

    @builtins.property
    def deploy_key_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of a GitLab deploy key allowed to perform the relevant action.

        Mutually exclusive with ``group_id`` and ``user_id``. This field is read-only until Gitlab 17.5.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#deploy_key_id BranchProtection#deploy_key_id}
        '''
        result = self._values.get("deploy_key_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def group_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of a GitLab group allowed to perform the relevant action. Mutually exclusive with ``deploy_key_id`` and ``user_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#group_id BranchProtection#group_id}
        '''
        result = self._values.get("group_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def user_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of a GitLab user allowed to perform the relevant action. Mutually exclusive with ``deploy_key_id`` and ``group_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#user_id BranchProtection#user_id}
        '''
        result = self._values.get("user_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchProtectionAllowedToPush(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BranchProtectionAllowedToPushList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.branchProtection.BranchProtectionAllowedToPushList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6423f74547e4ce7785b4e03c589282a5a1f58a11da6fdec4208fde25760712ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BranchProtectionAllowedToPushOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__324602f35ee5d0fe7cb97e27cb553ca7a4cfdf1d8940520eafbd0b56e496aa56)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BranchProtectionAllowedToPushOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db072da19a9f001ace2befd75c87b67df5c8f3d1b61fb0d872b3675a18e54a0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d254012eeaad6a41413dade69bb499b0a098a2a1ae90edcb10744d029245a918)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91a96ae76d4d5cc65a9b4f0c259ce2711e19b0de441505f43fb937ef71931277)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionAllowedToPush]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionAllowedToPush]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionAllowedToPush]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af2631658d3e2a0c62036717f98f1b7790300005cfb44efc469686c9f6794311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BranchProtectionAllowedToPushOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.branchProtection.BranchProtectionAllowedToPushOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5adc5c44114c75430b582f30f323832e9ebb5471bd60412185c52794eb0b498e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDeployKeyId")
    def reset_deploy_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeployKeyId", []))

    @jsii.member(jsii_name="resetGroupId")
    def reset_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupId", []))

    @jsii.member(jsii_name="resetUserId")
    def reset_user_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserId", []))

    @builtins.property
    @jsii.member(jsii_name="accessLevel")
    def access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessLevel"))

    @builtins.property
    @jsii.member(jsii_name="accessLevelDescription")
    def access_level_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessLevelDescription"))

    @builtins.property
    @jsii.member(jsii_name="deployKeyIdInput")
    def deploy_key_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "deployKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userIdInput")
    def user_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "userIdInput"))

    @builtins.property
    @jsii.member(jsii_name="deployKeyId")
    def deploy_key_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "deployKeyId"))

    @deploy_key_id.setter
    def deploy_key_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2780ede00da6330e64e561ab51d6a8eecd24eb5c3b3da62db6f3cb6be460ecf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deployKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53fab6e024846876ae17852bc04748144036503349d2d83727757cbd9bbd39e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "userId"))

    @user_id.setter
    def user_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__146a48f0179ad34efc8e463a5372475fc4fd9bc687a49e55702e2b402e2c3916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionAllowedToPush]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionAllowedToPush]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionAllowedToPush]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fdc576e5549f67167579c6dc9d0a4a724d851eece2c9597b0587bc7cb0fd258)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.branchProtection.BranchProtectionAllowedToUnprotect",
    jsii_struct_bases=[],
    name_mapping={"group_id": "groupId", "user_id": "userId"},
)
class BranchProtectionAllowedToUnprotect:
    def __init__(
        self,
        *,
        group_id: typing.Optional[jsii.Number] = None,
        user_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param group_id: The ID of a GitLab group allowed to perform the relevant action. Mutually exclusive with ``user_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#group_id BranchProtection#group_id}
        :param user_id: The ID of a GitLab user allowed to perform the relevant action. Mutually exclusive with ``group_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#user_id BranchProtection#user_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af7e1de8cd311cbe58e1c4f399cc20059d007a3be7efe1598f05037ee238292b)
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_id is not None:
            self._values["group_id"] = group_id
        if user_id is not None:
            self._values["user_id"] = user_id

    @builtins.property
    def group_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of a GitLab group allowed to perform the relevant action. Mutually exclusive with ``user_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#group_id BranchProtection#group_id}
        '''
        result = self._values.get("group_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def user_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of a GitLab user allowed to perform the relevant action. Mutually exclusive with ``group_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#user_id BranchProtection#user_id}
        '''
        result = self._values.get("user_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchProtectionAllowedToUnprotect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BranchProtectionAllowedToUnprotectList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.branchProtection.BranchProtectionAllowedToUnprotectList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__739959532fa434fa643ffc4c02c77732f6f161bfd497341e0a93bf50aac831a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BranchProtectionAllowedToUnprotectOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6446472e240ed0a07286e5d96469b743780ef7b564fb92e265bfeb7bd3f821d5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BranchProtectionAllowedToUnprotectOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18ecd7c1a7d092eb746bb76696a9d9ea0e2250bc90ef454945a19793ac237f57)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68b477172dc4f67b7bfc16ceca2743bf787b0e251d8ec1dbf4f1e7157a527931)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf3acc0c5fc831ab9b1541c7156608e88f1e96d116bc1c5718931ccb7c823a7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionAllowedToUnprotect]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionAllowedToUnprotect]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionAllowedToUnprotect]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85cc3a7cd5afcab34a524161df2131fe73ba527187ba0c349498e5b1d602b33f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BranchProtectionAllowedToUnprotectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.branchProtection.BranchProtectionAllowedToUnprotectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a4237e71db8420d75d1fd64947095ccf5110f8058e46487e6d403a88e61612f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetGroupId")
    def reset_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupId", []))

    @jsii.member(jsii_name="resetUserId")
    def reset_user_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserId", []))

    @builtins.property
    @jsii.member(jsii_name="accessLevel")
    def access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessLevel"))

    @builtins.property
    @jsii.member(jsii_name="accessLevelDescription")
    def access_level_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessLevelDescription"))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userIdInput")
    def user_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "userIdInput"))

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c6f9e79cd78c1979c46f57a0a471e612238926f047fd3102ff7ea7dc21f49b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "userId"))

    @user_id.setter
    def user_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d284a062810ff997eba0cae0372ab888a503090f743122536dd038a3e24c7632)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionAllowedToUnprotect]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionAllowedToUnprotect]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionAllowedToUnprotect]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feb7987f6f4d81a750e145b6b929070266da2b87e5bc7af2570dc411be4d9376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.branchProtection.BranchProtectionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "branch": "branch",
        "project": "project",
        "allowed_to_merge": "allowedToMerge",
        "allowed_to_push": "allowedToPush",
        "allowed_to_unprotect": "allowedToUnprotect",
        "allow_force_push": "allowForcePush",
        "code_owner_approval_required": "codeOwnerApprovalRequired",
        "merge_access_level": "mergeAccessLevel",
        "push_access_level": "pushAccessLevel",
        "unprotect_access_level": "unprotectAccessLevel",
    },
)
class BranchProtectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        branch: builtins.str,
        project: builtins.str,
        allowed_to_merge: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BranchProtectionAllowedToMerge, typing.Dict[builtins.str, typing.Any]]]]] = None,
        allowed_to_push: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BranchProtectionAllowedToPush, typing.Dict[builtins.str, typing.Any]]]]] = None,
        allowed_to_unprotect: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BranchProtectionAllowedToUnprotect, typing.Dict[builtins.str, typing.Any]]]]] = None,
        allow_force_push: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        code_owner_approval_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        merge_access_level: typing.Optional[builtins.str] = None,
        push_access_level: typing.Optional[builtins.str] = None,
        unprotect_access_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param branch: Name of the branch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#branch BranchProtection#branch}
        :param project: The id of the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#project BranchProtection#project}
        :param allowed_to_merge: allowed_to_merge block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#allowed_to_merge BranchProtection#allowed_to_merge}
        :param allowed_to_push: allowed_to_push block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#allowed_to_push BranchProtection#allowed_to_push}
        :param allowed_to_unprotect: allowed_to_unprotect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#allowed_to_unprotect BranchProtection#allowed_to_unprotect}
        :param allow_force_push: Can be set to true to allow users with push access to force push. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#allow_force_push BranchProtection#allow_force_push}
        :param code_owner_approval_required: Can be set to true to require code owner approval before merging. Only available for Premium and Ultimate instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#code_owner_approval_required BranchProtection#code_owner_approval_required}
        :param merge_access_level: Access levels allowed to merge. Valid values are: ``no one``, ``developer``, ``maintainer``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#merge_access_level BranchProtection#merge_access_level}
        :param push_access_level: Access levels allowed to push. Valid values are: ``no one``, ``developer``, ``maintainer``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#push_access_level BranchProtection#push_access_level}
        :param unprotect_access_level: Access levels allowed to unprotect. Valid values are: ``developer``, ``maintainer``, ``admin``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#unprotect_access_level BranchProtection#unprotect_access_level}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a023b46f03e86db1090c4fee7fff440b10d8522c12c0fae35c5486492f057e6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument allowed_to_merge", value=allowed_to_merge, expected_type=type_hints["allowed_to_merge"])
            check_type(argname="argument allowed_to_push", value=allowed_to_push, expected_type=type_hints["allowed_to_push"])
            check_type(argname="argument allowed_to_unprotect", value=allowed_to_unprotect, expected_type=type_hints["allowed_to_unprotect"])
            check_type(argname="argument allow_force_push", value=allow_force_push, expected_type=type_hints["allow_force_push"])
            check_type(argname="argument code_owner_approval_required", value=code_owner_approval_required, expected_type=type_hints["code_owner_approval_required"])
            check_type(argname="argument merge_access_level", value=merge_access_level, expected_type=type_hints["merge_access_level"])
            check_type(argname="argument push_access_level", value=push_access_level, expected_type=type_hints["push_access_level"])
            check_type(argname="argument unprotect_access_level", value=unprotect_access_level, expected_type=type_hints["unprotect_access_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "branch": branch,
            "project": project,
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
        if allowed_to_merge is not None:
            self._values["allowed_to_merge"] = allowed_to_merge
        if allowed_to_push is not None:
            self._values["allowed_to_push"] = allowed_to_push
        if allowed_to_unprotect is not None:
            self._values["allowed_to_unprotect"] = allowed_to_unprotect
        if allow_force_push is not None:
            self._values["allow_force_push"] = allow_force_push
        if code_owner_approval_required is not None:
            self._values["code_owner_approval_required"] = code_owner_approval_required
        if merge_access_level is not None:
            self._values["merge_access_level"] = merge_access_level
        if push_access_level is not None:
            self._values["push_access_level"] = push_access_level
        if unprotect_access_level is not None:
            self._values["unprotect_access_level"] = unprotect_access_level

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
    def branch(self) -> builtins.str:
        '''Name of the branch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#branch BranchProtection#branch}
        '''
        result = self._values.get("branch")
        assert result is not None, "Required property 'branch' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''The id of the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#project BranchProtection#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_to_merge(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionAllowedToMerge]]]:
        '''allowed_to_merge block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#allowed_to_merge BranchProtection#allowed_to_merge}
        '''
        result = self._values.get("allowed_to_merge")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionAllowedToMerge]]], result)

    @builtins.property
    def allowed_to_push(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionAllowedToPush]]]:
        '''allowed_to_push block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#allowed_to_push BranchProtection#allowed_to_push}
        '''
        result = self._values.get("allowed_to_push")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionAllowedToPush]]], result)

    @builtins.property
    def allowed_to_unprotect(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionAllowedToUnprotect]]]:
        '''allowed_to_unprotect block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#allowed_to_unprotect BranchProtection#allowed_to_unprotect}
        '''
        result = self._values.get("allowed_to_unprotect")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionAllowedToUnprotect]]], result)

    @builtins.property
    def allow_force_push(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Can be set to true to allow users with push access to force push.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#allow_force_push BranchProtection#allow_force_push}
        '''
        result = self._values.get("allow_force_push")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def code_owner_approval_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Can be set to true to require code owner approval before merging. Only available for Premium and Ultimate instances.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#code_owner_approval_required BranchProtection#code_owner_approval_required}
        '''
        result = self._values.get("code_owner_approval_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def merge_access_level(self) -> typing.Optional[builtins.str]:
        '''Access levels allowed to merge. Valid values are: ``no one``, ``developer``, ``maintainer``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#merge_access_level BranchProtection#merge_access_level}
        '''
        result = self._values.get("merge_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def push_access_level(self) -> typing.Optional[builtins.str]:
        '''Access levels allowed to push. Valid values are: ``no one``, ``developer``, ``maintainer``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#push_access_level BranchProtection#push_access_level}
        '''
        result = self._values.get("push_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unprotect_access_level(self) -> typing.Optional[builtins.str]:
        '''Access levels allowed to unprotect. Valid values are: ``developer``, ``maintainer``, ``admin``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/branch_protection#unprotect_access_level BranchProtection#unprotect_access_level}
        '''
        result = self._values.get("unprotect_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchProtectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BranchProtection",
    "BranchProtectionAllowedToMerge",
    "BranchProtectionAllowedToMergeList",
    "BranchProtectionAllowedToMergeOutputReference",
    "BranchProtectionAllowedToPush",
    "BranchProtectionAllowedToPushList",
    "BranchProtectionAllowedToPushOutputReference",
    "BranchProtectionAllowedToUnprotect",
    "BranchProtectionAllowedToUnprotectList",
    "BranchProtectionAllowedToUnprotectOutputReference",
    "BranchProtectionConfig",
]

publication.publish()

def _typecheckingstub__7b2f0b7f1af00493894fe672adaa934a38a934975c0f5faee023936ebc3e3f97(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    branch: builtins.str,
    project: builtins.str,
    allowed_to_merge: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BranchProtectionAllowedToMerge, typing.Dict[builtins.str, typing.Any]]]]] = None,
    allowed_to_push: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BranchProtectionAllowedToPush, typing.Dict[builtins.str, typing.Any]]]]] = None,
    allowed_to_unprotect: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BranchProtectionAllowedToUnprotect, typing.Dict[builtins.str, typing.Any]]]]] = None,
    allow_force_push: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    code_owner_approval_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    merge_access_level: typing.Optional[builtins.str] = None,
    push_access_level: typing.Optional[builtins.str] = None,
    unprotect_access_level: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__bfc5d7813a00a6350cfcc5332af41f071df32107af5006207dfed9af2fcf516d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74fc06ce074d208c04307f39b2c5b7843b284c1731846b8a6e3d51ff844ffa51(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BranchProtectionAllowedToMerge, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a01d951730ce0463c0517d5549455e9f04519bb846f3c585500babf9d6fb2526(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BranchProtectionAllowedToPush, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c6683079cd935c8e1ed218d2bb0697cd2698cc31e018362f5b44bf099b1c12e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BranchProtectionAllowedToUnprotect, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5558ebaa86f37b7a6f08b2f1b92258892991923506fcc41d56e2618bdbfd0f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53743344ac12eaec8374256b285c732decc1315a674d7af0178ecab1a0bb5a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac89ac79f24e15bb33171db48a46f5c78ec8a5979a0de26b1f5ea097f04d233(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__798090e920e5d7595996d0105593c329531ef84653f5a158848b811cff2c2b6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd08961a00fe0f04b805df4750da9d87a17c99a4cd505f4168b62af5db29501(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a93342b0133d8ac60fcaa8236e0f65cc2ee15e36ea066fc6de3e1d4833a54a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8519fe5ef3fb2188f9aba6057ae4bb64c074b6dad603d31f7cdd4f2646ddf4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10bc5fb1df6e438ff8f8ed2004a19bfdf8dd675140f2e64bca9c88e2eace03b(
    *,
    group_id: typing.Optional[jsii.Number] = None,
    user_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc17a8b8af71491999c2bbdfe458cc6e24ba2e8fb0cd570a9b11909c35dc919e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570434eccfc44fa69e9974533d00f5a620874ae2899f6f2be7fd757e7be6a949(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2ec216cdfd09d9d6a3f54b4a27d7e007225105d697d2a47bfc06e3f170393c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__649719a621cb0d999080963eb730668b15198e461c7a1dd64e6b9a83f69ed83f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22abd01a70a82606895565dcf146a479f5578a362a219672f1ad905c1f96c14a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b6bf75c3bf37e7c82e5da45dc9443333b3ea371f89b1ae9d8b86f55e93237e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionAllowedToMerge]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14005d99a812ce7afc16f3b9cd69990f93f44c15b5d9560f22d33efa874e86aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02bd9257561d4a85c0c5139cc95dadd0fdf3cc8a74d7183548c0e2232a82cb3b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c0b60e8a6779b32c7cdf10682ccc3da5e70d0457eddcf7aadd06f497ee1a82(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0722d16e6467cbd718b5c98495a2a01836bdd79abd4eef9684af93d76d186e17(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionAllowedToMerge]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a23e6d56a63eb734fe66bc994bb0cbeaaa38774a96d984b255416d994a67add(
    *,
    deploy_key_id: typing.Optional[jsii.Number] = None,
    group_id: typing.Optional[jsii.Number] = None,
    user_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6423f74547e4ce7785b4e03c589282a5a1f58a11da6fdec4208fde25760712ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__324602f35ee5d0fe7cb97e27cb553ca7a4cfdf1d8940520eafbd0b56e496aa56(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db072da19a9f001ace2befd75c87b67df5c8f3d1b61fb0d872b3675a18e54a0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d254012eeaad6a41413dade69bb499b0a098a2a1ae90edcb10744d029245a918(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91a96ae76d4d5cc65a9b4f0c259ce2711e19b0de441505f43fb937ef71931277(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2631658d3e2a0c62036717f98f1b7790300005cfb44efc469686c9f6794311(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionAllowedToPush]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5adc5c44114c75430b582f30f323832e9ebb5471bd60412185c52794eb0b498e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2780ede00da6330e64e561ab51d6a8eecd24eb5c3b3da62db6f3cb6be460ecf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53fab6e024846876ae17852bc04748144036503349d2d83727757cbd9bbd39e3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__146a48f0179ad34efc8e463a5372475fc4fd9bc687a49e55702e2b402e2c3916(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fdc576e5549f67167579c6dc9d0a4a724d851eece2c9597b0587bc7cb0fd258(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionAllowedToPush]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7e1de8cd311cbe58e1c4f399cc20059d007a3be7efe1598f05037ee238292b(
    *,
    group_id: typing.Optional[jsii.Number] = None,
    user_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__739959532fa434fa643ffc4c02c77732f6f161bfd497341e0a93bf50aac831a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6446472e240ed0a07286e5d96469b743780ef7b564fb92e265bfeb7bd3f821d5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18ecd7c1a7d092eb746bb76696a9d9ea0e2250bc90ef454945a19793ac237f57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b477172dc4f67b7bfc16ceca2743bf787b0e251d8ec1dbf4f1e7157a527931(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf3acc0c5fc831ab9b1541c7156608e88f1e96d116bc1c5718931ccb7c823a7e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85cc3a7cd5afcab34a524161df2131fe73ba527187ba0c349498e5b1d602b33f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionAllowedToUnprotect]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4237e71db8420d75d1fd64947095ccf5110f8058e46487e6d403a88e61612f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c6f9e79cd78c1979c46f57a0a471e612238926f047fd3102ff7ea7dc21f49b6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d284a062810ff997eba0cae0372ab888a503090f743122536dd038a3e24c7632(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb7987f6f4d81a750e145b6b929070266da2b87e5bc7af2570dc411be4d9376(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionAllowedToUnprotect]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a023b46f03e86db1090c4fee7fff440b10d8522c12c0fae35c5486492f057e6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    branch: builtins.str,
    project: builtins.str,
    allowed_to_merge: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BranchProtectionAllowedToMerge, typing.Dict[builtins.str, typing.Any]]]]] = None,
    allowed_to_push: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BranchProtectionAllowedToPush, typing.Dict[builtins.str, typing.Any]]]]] = None,
    allowed_to_unprotect: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BranchProtectionAllowedToUnprotect, typing.Dict[builtins.str, typing.Any]]]]] = None,
    allow_force_push: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    code_owner_approval_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    merge_access_level: typing.Optional[builtins.str] = None,
    push_access_level: typing.Optional[builtins.str] = None,
    unprotect_access_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
