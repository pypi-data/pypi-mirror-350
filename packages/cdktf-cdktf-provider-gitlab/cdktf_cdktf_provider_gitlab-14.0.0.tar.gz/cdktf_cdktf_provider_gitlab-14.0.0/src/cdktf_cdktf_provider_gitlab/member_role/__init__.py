r'''
# `gitlab_member_role`

Refer to the Terraform Registry for docs: [`gitlab_member_role`](https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/member_role).
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


class MemberRole(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.memberRole.MemberRole",
):
    '''Represents a {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/member_role gitlab_member_role}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        base_access_level: builtins.str,
        enabled_permissions: typing.Sequence[builtins.str],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        group_path: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/member_role gitlab_member_role} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param base_access_level: The base access level for the custom role. Valid values are: ``DEVELOPER``, ``GUEST``, ``MAINTAINER``, ``MINIMAL_ACCESS``, ``OWNER``, ``REPORTER``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/member_role#base_access_level MemberRole#base_access_level}
        :param enabled_permissions: All permissions enabled for the custom role. Valid values are: ``ADMIN_CICD_VARIABLES``, ``ADMIN_COMPLIANCE_FRAMEWORK``, ``ADMIN_GROUP_MEMBER``, ``ADMIN_INTEGRATIONS``, ``ADMIN_MERGE_REQUEST``, ``ADMIN_PROTECTED_BRANCH``, ``ADMIN_PUSH_RULES``, ``ADMIN_RUNNERS``, ``ADMIN_TERRAFORM_STATE``, ``ADMIN_VULNERABILITY``, ``ADMIN_WEB_HOOK``, ``ARCHIVE_PROJECT``, ``MANAGE_DEPLOY_TOKENS``, ``MANAGE_GROUP_ACCESS_TOKENS``, ``MANAGE_MERGE_REQUEST_SETTINGS``, ``MANAGE_PROJECT_ACCESS_TOKENS``, ``MANAGE_SECURITY_POLICY_LINK``, ``READ_ADMIN_CICD``, ``READ_ADMIN_DASHBOARD``, ``READ_CODE``, ``READ_COMPLIANCE_DASHBOARD``, ``READ_CRM_CONTACT``, ``READ_DEPENDENCY``, ``READ_RUNNERS``, ``READ_VULNERABILITY``, ``REMOVE_GROUP``, ``REMOVE_PROJECT`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/member_role#enabled_permissions MemberRole#enabled_permissions}
        :param name: Name for the member role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/member_role#name MemberRole#name}
        :param description: Description for the member role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/member_role#description MemberRole#description}
        :param group_path: Full path of the namespace to create the member role in. **Required for SAAS** **Not allowed for self-managed**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/member_role#group_path MemberRole#group_path}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3e8ec79a65a87169f784e2b2bd427bfe18d2cd073d31fc9655b83af686b8461)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = MemberRoleConfig(
            base_access_level=base_access_level,
            enabled_permissions=enabled_permissions,
            name=name,
            description=description,
            group_path=group_path,
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
        '''Generates CDKTF code for importing a MemberRole resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MemberRole to import.
        :param import_from_id: The id of the existing MemberRole that should be imported. Refer to the {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/member_role#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MemberRole to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72fed7911fd588acf05e965e89c9964417220f02ddd60152cf2e1ce27397c1b1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetGroupPath")
    def reset_group_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupPath", []))

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
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="editPath")
    def edit_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "editPath"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="iid")
    def iid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "iid"))

    @builtins.property
    @jsii.member(jsii_name="baseAccessLevelInput")
    def base_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledPermissionsInput")
    def enabled_permissions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "enabledPermissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="groupPathInput")
    def group_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupPathInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="baseAccessLevel")
    def base_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseAccessLevel"))

    @base_access_level.setter
    def base_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1134e1eb373011f33b9e3515a40834165607fbc723422f1fa82bb9313ef3e50a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48671b036bef532382b4885b3792031fcb6e83ac2e667181a11a7fff47777e7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabledPermissions")
    def enabled_permissions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "enabledPermissions"))

    @enabled_permissions.setter
    def enabled_permissions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__833523ff1a70cfb1d4c641916652da7ac775c39016fba3004214c141718d7562)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabledPermissions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupPath")
    def group_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupPath"))

    @group_path.setter
    def group_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8015e632f0b2556025d09fd89266f229cf76bf8dacd43d1d7593365a712c771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264bfbca12ad8eae235118b6f620afdc8c0b40472531632e31ebd350b95927eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.memberRole.MemberRoleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "base_access_level": "baseAccessLevel",
        "enabled_permissions": "enabledPermissions",
        "name": "name",
        "description": "description",
        "group_path": "groupPath",
    },
)
class MemberRoleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        base_access_level: builtins.str,
        enabled_permissions: typing.Sequence[builtins.str],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        group_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param base_access_level: The base access level for the custom role. Valid values are: ``DEVELOPER``, ``GUEST``, ``MAINTAINER``, ``MINIMAL_ACCESS``, ``OWNER``, ``REPORTER``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/member_role#base_access_level MemberRole#base_access_level}
        :param enabled_permissions: All permissions enabled for the custom role. Valid values are: ``ADMIN_CICD_VARIABLES``, ``ADMIN_COMPLIANCE_FRAMEWORK``, ``ADMIN_GROUP_MEMBER``, ``ADMIN_INTEGRATIONS``, ``ADMIN_MERGE_REQUEST``, ``ADMIN_PROTECTED_BRANCH``, ``ADMIN_PUSH_RULES``, ``ADMIN_RUNNERS``, ``ADMIN_TERRAFORM_STATE``, ``ADMIN_VULNERABILITY``, ``ADMIN_WEB_HOOK``, ``ARCHIVE_PROJECT``, ``MANAGE_DEPLOY_TOKENS``, ``MANAGE_GROUP_ACCESS_TOKENS``, ``MANAGE_MERGE_REQUEST_SETTINGS``, ``MANAGE_PROJECT_ACCESS_TOKENS``, ``MANAGE_SECURITY_POLICY_LINK``, ``READ_ADMIN_CICD``, ``READ_ADMIN_DASHBOARD``, ``READ_CODE``, ``READ_COMPLIANCE_DASHBOARD``, ``READ_CRM_CONTACT``, ``READ_DEPENDENCY``, ``READ_RUNNERS``, ``READ_VULNERABILITY``, ``REMOVE_GROUP``, ``REMOVE_PROJECT`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/member_role#enabled_permissions MemberRole#enabled_permissions}
        :param name: Name for the member role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/member_role#name MemberRole#name}
        :param description: Description for the member role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/member_role#description MemberRole#description}
        :param group_path: Full path of the namespace to create the member role in. **Required for SAAS** **Not allowed for self-managed**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/member_role#group_path MemberRole#group_path}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f061b05f916f71c5c804b80f82ae0ef2870e00c62a4d9a67396fd24e2bbd105)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument base_access_level", value=base_access_level, expected_type=type_hints["base_access_level"])
            check_type(argname="argument enabled_permissions", value=enabled_permissions, expected_type=type_hints["enabled_permissions"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument group_path", value=group_path, expected_type=type_hints["group_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "base_access_level": base_access_level,
            "enabled_permissions": enabled_permissions,
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
        if description is not None:
            self._values["description"] = description
        if group_path is not None:
            self._values["group_path"] = group_path

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
    def base_access_level(self) -> builtins.str:
        '''The base access level for the custom role. Valid values are: ``DEVELOPER``, ``GUEST``, ``MAINTAINER``, ``MINIMAL_ACCESS``, ``OWNER``, ``REPORTER``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/member_role#base_access_level MemberRole#base_access_level}
        '''
        result = self._values.get("base_access_level")
        assert result is not None, "Required property 'base_access_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled_permissions(self) -> typing.List[builtins.str]:
        '''All permissions enabled for the custom role.

        Valid values are: ``ADMIN_CICD_VARIABLES``, ``ADMIN_COMPLIANCE_FRAMEWORK``, ``ADMIN_GROUP_MEMBER``, ``ADMIN_INTEGRATIONS``, ``ADMIN_MERGE_REQUEST``, ``ADMIN_PROTECTED_BRANCH``, ``ADMIN_PUSH_RULES``, ``ADMIN_RUNNERS``, ``ADMIN_TERRAFORM_STATE``, ``ADMIN_VULNERABILITY``, ``ADMIN_WEB_HOOK``, ``ARCHIVE_PROJECT``, ``MANAGE_DEPLOY_TOKENS``, ``MANAGE_GROUP_ACCESS_TOKENS``, ``MANAGE_MERGE_REQUEST_SETTINGS``, ``MANAGE_PROJECT_ACCESS_TOKENS``, ``MANAGE_SECURITY_POLICY_LINK``, ``READ_ADMIN_CICD``, ``READ_ADMIN_DASHBOARD``, ``READ_CODE``, ``READ_COMPLIANCE_DASHBOARD``, ``READ_CRM_CONTACT``, ``READ_DEPENDENCY``, ``READ_RUNNERS``, ``READ_VULNERABILITY``, ``REMOVE_GROUP``, ``REMOVE_PROJECT``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/member_role#enabled_permissions MemberRole#enabled_permissions}
        '''
        result = self._values.get("enabled_permissions")
        assert result is not None, "Required property 'enabled_permissions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name for the member role.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/member_role#name MemberRole#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description for the member role.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/member_role#description MemberRole#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_path(self) -> typing.Optional[builtins.str]:
        '''Full path of the namespace to create the member role in. **Required for SAAS** **Not allowed for self-managed**.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/member_role#group_path MemberRole#group_path}
        '''
        result = self._values.get("group_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemberRoleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "MemberRole",
    "MemberRoleConfig",
]

publication.publish()

def _typecheckingstub__a3e8ec79a65a87169f784e2b2bd427bfe18d2cd073d31fc9655b83af686b8461(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    base_access_level: builtins.str,
    enabled_permissions: typing.Sequence[builtins.str],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    group_path: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__72fed7911fd588acf05e965e89c9964417220f02ddd60152cf2e1ce27397c1b1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1134e1eb373011f33b9e3515a40834165607fbc723422f1fa82bb9313ef3e50a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48671b036bef532382b4885b3792031fcb6e83ac2e667181a11a7fff47777e7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__833523ff1a70cfb1d4c641916652da7ac775c39016fba3004214c141718d7562(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8015e632f0b2556025d09fd89266f229cf76bf8dacd43d1d7593365a712c771(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264bfbca12ad8eae235118b6f620afdc8c0b40472531632e31ebd350b95927eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f061b05f916f71c5c804b80f82ae0ef2870e00c62a4d9a67396fd24e2bbd105(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    base_access_level: builtins.str,
    enabled_permissions: typing.Sequence[builtins.str],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    group_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
