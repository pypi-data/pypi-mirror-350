r'''
# `gitlab_group`

Refer to the Terraform Registry for docs: [`gitlab_group`](https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group).
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


class Group(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.group.Group",
):
    '''Represents a {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group gitlab_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        path: builtins.str,
        allowed_email_domains_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        auto_devops_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        avatar: typing.Optional[builtins.str] = None,
        avatar_hash: typing.Optional[builtins.str] = None,
        default_branch: typing.Optional[builtins.str] = None,
        default_branch_protection: typing.Optional[jsii.Number] = None,
        default_branch_protection_defaults: typing.Optional[typing.Union["GroupDefaultBranchProtectionDefaults", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        emails_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        extra_shared_runners_minutes_limit: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        ip_restriction_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        lfs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        membership_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mentions_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        parent_id: typing.Optional[jsii.Number] = None,
        permanently_remove_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prevent_forking_outside_group: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project_creation_level: typing.Optional[builtins.str] = None,
        push_rules: typing.Optional[typing.Union["GroupPushRules", typing.Dict[builtins.str, typing.Any]]] = None,
        request_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_two_factor_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        shared_runners_minutes_limit: typing.Optional[jsii.Number] = None,
        shared_runners_setting: typing.Optional[builtins.str] = None,
        share_with_group_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subgroup_creation_level: typing.Optional[builtins.str] = None,
        two_factor_grace_period: typing.Optional[jsii.Number] = None,
        visibility_level: typing.Optional[builtins.str] = None,
        wiki_access_level: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group gitlab_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#name Group#name}
        :param path: The path of the group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#path Group#path}
        :param allowed_email_domains_list: A list of email address domains to allow group access. Will be concatenated together into a comma separated string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#allowed_email_domains_list Group#allowed_email_domains_list}
        :param auto_devops_enabled: Default to Auto DevOps pipeline for all projects within this group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#auto_devops_enabled Group#auto_devops_enabled}
        :param avatar: A local path to the avatar image to upload. **Note**: not available for imported resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#avatar Group#avatar}
        :param avatar_hash: The hash of the avatar image. Use ``filesha256("path/to/avatar.png")`` whenever possible. **Note**: this is used to trigger an update of the avatar. If it's not given, but an avatar is given, the avatar will be updated each time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#avatar_hash Group#avatar_hash}
        :param default_branch: Initial default branch name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#default_branch Group#default_branch}
        :param default_branch_protection: See https://docs.gitlab.com/api/groups/#options-for-default_branch_protection. Valid values are: ``0``, ``1``, ``2``, ``3``, ``4``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#default_branch_protection Group#default_branch_protection}
        :param default_branch_protection_defaults: default_branch_protection_defaults block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#default_branch_protection_defaults Group#default_branch_protection_defaults}
        :param description: The group's description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#description Group#description}
        :param emails_enabled: Enable email notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#emails_enabled Group#emails_enabled}
        :param extra_shared_runners_minutes_limit: Can be set by administrators only. Additional CI/CD minutes for this group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#extra_shared_runners_minutes_limit Group#extra_shared_runners_minutes_limit}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#id Group#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_restriction_ranges: A list of IP addresses or subnet masks to restrict group access. Will be concatenated together into a comma separated string. Only allowed on top level groups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#ip_restriction_ranges Group#ip_restriction_ranges}
        :param lfs_enabled: Enable/disable Large File Storage (LFS) for the projects in this group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#lfs_enabled Group#lfs_enabled}
        :param membership_lock: Users cannot be added to projects in this group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#membership_lock Group#membership_lock}
        :param mentions_disabled: Disable the capability of a group from getting mentioned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#mentions_disabled Group#mentions_disabled}
        :param parent_id: Id of the parent group (creates a nested group). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#parent_id Group#parent_id}
        :param permanently_remove_on_delete: Whether the group should be permanently removed during a ``delete`` operation. This only works with subgroups. Must be configured via an ``apply`` before the ``destroy`` is run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#permanently_remove_on_delete Group#permanently_remove_on_delete}
        :param prevent_forking_outside_group: Defaults to false. When enabled, users can not fork projects from this group to external namespaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#prevent_forking_outside_group Group#prevent_forking_outside_group}
        :param project_creation_level: Determine if developers can create projects in the group. Valid values are: ``noone``, ``owner``, ``maintainer``, ``developer``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#project_creation_level Group#project_creation_level}
        :param push_rules: push_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#push_rules Group#push_rules}
        :param request_access_enabled: Allow users to request member access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#request_access_enabled Group#request_access_enabled}
        :param require_two_factor_authentication: Require all users in this group to setup Two-factor authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#require_two_factor_authentication Group#require_two_factor_authentication}
        :param shared_runners_minutes_limit: Can be set by administrators only. Maximum number of monthly CI/CD minutes for this group. Can be nil (default; inherit system default), 0 (unlimited), or > 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#shared_runners_minutes_limit Group#shared_runners_minutes_limit}
        :param shared_runners_setting: Enable or disable shared runners for a group’s subgroups and projects. Valid values are: ``enabled``, ``disabled_and_overridable``, ``disabled_and_unoverridable``, ``disabled_with_override``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#shared_runners_setting Group#shared_runners_setting}
        :param share_with_group_lock: Prevent sharing a project with another group within this group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#share_with_group_lock Group#share_with_group_lock}
        :param subgroup_creation_level: Allowed to create subgroups. Valid values are: ``owner``, ``maintainer``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#subgroup_creation_level Group#subgroup_creation_level}
        :param two_factor_grace_period: Defaults to 48. Time before Two-factor authentication is enforced (in hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#two_factor_grace_period Group#two_factor_grace_period}
        :param visibility_level: The group's visibility. Can be ``private``, ``internal``, or ``public``. Valid values are: ``private``, ``internal``, ``public``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#visibility_level Group#visibility_level}
        :param wiki_access_level: The group's wiki access level. Only available on Premium and Ultimate plans. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#wiki_access_level Group#wiki_access_level}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ba99799c3dfc0c212cdf9860e0ebe4109245373801789101a41d768bfb63c07)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GroupConfig(
            name=name,
            path=path,
            allowed_email_domains_list=allowed_email_domains_list,
            auto_devops_enabled=auto_devops_enabled,
            avatar=avatar,
            avatar_hash=avatar_hash,
            default_branch=default_branch,
            default_branch_protection=default_branch_protection,
            default_branch_protection_defaults=default_branch_protection_defaults,
            description=description,
            emails_enabled=emails_enabled,
            extra_shared_runners_minutes_limit=extra_shared_runners_minutes_limit,
            id=id,
            ip_restriction_ranges=ip_restriction_ranges,
            lfs_enabled=lfs_enabled,
            membership_lock=membership_lock,
            mentions_disabled=mentions_disabled,
            parent_id=parent_id,
            permanently_remove_on_delete=permanently_remove_on_delete,
            prevent_forking_outside_group=prevent_forking_outside_group,
            project_creation_level=project_creation_level,
            push_rules=push_rules,
            request_access_enabled=request_access_enabled,
            require_two_factor_authentication=require_two_factor_authentication,
            shared_runners_minutes_limit=shared_runners_minutes_limit,
            shared_runners_setting=shared_runners_setting,
            share_with_group_lock=share_with_group_lock,
            subgroup_creation_level=subgroup_creation_level,
            two_factor_grace_period=two_factor_grace_period,
            visibility_level=visibility_level,
            wiki_access_level=wiki_access_level,
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
        '''Generates CDKTF code for importing a Group resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Group to import.
        :param import_from_id: The id of the existing Group that should be imported. Refer to the {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Group to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9eebe69803e07a85ec4e8f611a727d5a6b6a34d84175638f68ed4a41af6cfe3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDefaultBranchProtectionDefaults")
    def put_default_branch_protection_defaults(
        self,
        *,
        allowed_to_merge: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_to_push: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_force_push: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        developer_can_initial_push: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_to_merge: An array of access levels allowed to merge. Valid values are: ``developer``, ``maintainer``, ``no one``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#allowed_to_merge Group#allowed_to_merge}
        :param allowed_to_push: An array of access levels allowed to push. Valid values are: ``developer``, ``maintainer``, ``no one``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#allowed_to_push Group#allowed_to_push}
        :param allow_force_push: Allow force push for all users with push access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#allow_force_push Group#allow_force_push}
        :param developer_can_initial_push: Allow developers to initial push. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#developer_can_initial_push Group#developer_can_initial_push}
        '''
        value = GroupDefaultBranchProtectionDefaults(
            allowed_to_merge=allowed_to_merge,
            allowed_to_push=allowed_to_push,
            allow_force_push=allow_force_push,
            developer_can_initial_push=developer_can_initial_push,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultBranchProtectionDefaults", [value]))

    @jsii.member(jsii_name="putPushRules")
    def put_push_rules(
        self,
        *,
        author_email_regex: typing.Optional[builtins.str] = None,
        branch_name_regex: typing.Optional[builtins.str] = None,
        commit_committer_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        commit_committer_name_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        commit_message_negative_regex: typing.Optional[builtins.str] = None,
        commit_message_regex: typing.Optional[builtins.str] = None,
        deny_delete_tag: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        file_name_regex: typing.Optional[builtins.str] = None,
        max_file_size: typing.Optional[jsii.Number] = None,
        member_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prevent_secrets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reject_non_dco_commits: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reject_unsigned_commits: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param author_email_regex: All commit author emails must match this regex, e.g. ``@my-company.com$``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#author_email_regex Group#author_email_regex}
        :param branch_name_regex: All branch names must match this regex, e.g. ``(feature|hotfix)\\/*``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#branch_name_regex Group#branch_name_regex}
        :param commit_committer_check: Only commits pushed using verified emails are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#commit_committer_check Group#commit_committer_check}
        :param commit_committer_name_check: Users can only push commits to this repository if the commit author name is consistent with their GitLab account name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#commit_committer_name_check Group#commit_committer_name_check}
        :param commit_message_negative_regex: No commit message is allowed to match this regex, for example ``ssh\\:\\/\\/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#commit_message_negative_regex Group#commit_message_negative_regex}
        :param commit_message_regex: All commit messages must match this regex, e.g. ``Fixed \\d+\\..*``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#commit_message_regex Group#commit_message_regex}
        :param deny_delete_tag: Deny deleting a tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#deny_delete_tag Group#deny_delete_tag}
        :param file_name_regex: Filenames matching the regular expression provided in this attribute are not allowed, for example, ``(jar|exe)$``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#file_name_regex Group#file_name_regex}
        :param max_file_size: Maximum file size (MB) allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#max_file_size Group#max_file_size}
        :param member_check: Allows only GitLab users to author commits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#member_check Group#member_check}
        :param prevent_secrets: GitLab will reject any files that are likely to contain secrets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#prevent_secrets Group#prevent_secrets}
        :param reject_non_dco_commits: Reject commit when it’s not DCO certified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#reject_non_dco_commits Group#reject_non_dco_commits}
        :param reject_unsigned_commits: Only commits signed through GPG are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#reject_unsigned_commits Group#reject_unsigned_commits}
        '''
        value = GroupPushRules(
            author_email_regex=author_email_regex,
            branch_name_regex=branch_name_regex,
            commit_committer_check=commit_committer_check,
            commit_committer_name_check=commit_committer_name_check,
            commit_message_negative_regex=commit_message_negative_regex,
            commit_message_regex=commit_message_regex,
            deny_delete_tag=deny_delete_tag,
            file_name_regex=file_name_regex,
            max_file_size=max_file_size,
            member_check=member_check,
            prevent_secrets=prevent_secrets,
            reject_non_dco_commits=reject_non_dco_commits,
            reject_unsigned_commits=reject_unsigned_commits,
        )

        return typing.cast(None, jsii.invoke(self, "putPushRules", [value]))

    @jsii.member(jsii_name="resetAllowedEmailDomainsList")
    def reset_allowed_email_domains_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedEmailDomainsList", []))

    @jsii.member(jsii_name="resetAutoDevopsEnabled")
    def reset_auto_devops_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDevopsEnabled", []))

    @jsii.member(jsii_name="resetAvatar")
    def reset_avatar(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvatar", []))

    @jsii.member(jsii_name="resetAvatarHash")
    def reset_avatar_hash(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvatarHash", []))

    @jsii.member(jsii_name="resetDefaultBranch")
    def reset_default_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultBranch", []))

    @jsii.member(jsii_name="resetDefaultBranchProtection")
    def reset_default_branch_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultBranchProtection", []))

    @jsii.member(jsii_name="resetDefaultBranchProtectionDefaults")
    def reset_default_branch_protection_defaults(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultBranchProtectionDefaults", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEmailsEnabled")
    def reset_emails_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailsEnabled", []))

    @jsii.member(jsii_name="resetExtraSharedRunnersMinutesLimit")
    def reset_extra_shared_runners_minutes_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtraSharedRunnersMinutesLimit", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpRestrictionRanges")
    def reset_ip_restriction_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpRestrictionRanges", []))

    @jsii.member(jsii_name="resetLfsEnabled")
    def reset_lfs_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLfsEnabled", []))

    @jsii.member(jsii_name="resetMembershipLock")
    def reset_membership_lock(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMembershipLock", []))

    @jsii.member(jsii_name="resetMentionsDisabled")
    def reset_mentions_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMentionsDisabled", []))

    @jsii.member(jsii_name="resetParentId")
    def reset_parent_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParentId", []))

    @jsii.member(jsii_name="resetPermanentlyRemoveOnDelete")
    def reset_permanently_remove_on_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermanentlyRemoveOnDelete", []))

    @jsii.member(jsii_name="resetPreventForkingOutsideGroup")
    def reset_prevent_forking_outside_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreventForkingOutsideGroup", []))

    @jsii.member(jsii_name="resetProjectCreationLevel")
    def reset_project_creation_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectCreationLevel", []))

    @jsii.member(jsii_name="resetPushRules")
    def reset_push_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPushRules", []))

    @jsii.member(jsii_name="resetRequestAccessEnabled")
    def reset_request_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestAccessEnabled", []))

    @jsii.member(jsii_name="resetRequireTwoFactorAuthentication")
    def reset_require_two_factor_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireTwoFactorAuthentication", []))

    @jsii.member(jsii_name="resetSharedRunnersMinutesLimit")
    def reset_shared_runners_minutes_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedRunnersMinutesLimit", []))

    @jsii.member(jsii_name="resetSharedRunnersSetting")
    def reset_shared_runners_setting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedRunnersSetting", []))

    @jsii.member(jsii_name="resetShareWithGroupLock")
    def reset_share_with_group_lock(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShareWithGroupLock", []))

    @jsii.member(jsii_name="resetSubgroupCreationLevel")
    def reset_subgroup_creation_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubgroupCreationLevel", []))

    @jsii.member(jsii_name="resetTwoFactorGracePeriod")
    def reset_two_factor_grace_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTwoFactorGracePeriod", []))

    @jsii.member(jsii_name="resetVisibilityLevel")
    def reset_visibility_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisibilityLevel", []))

    @jsii.member(jsii_name="resetWikiAccessLevel")
    def reset_wiki_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWikiAccessLevel", []))

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
    @jsii.member(jsii_name="avatarUrl")
    def avatar_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "avatarUrl"))

    @builtins.property
    @jsii.member(jsii_name="defaultBranchProtectionDefaults")
    def default_branch_protection_defaults(
        self,
    ) -> "GroupDefaultBranchProtectionDefaultsOutputReference":
        return typing.cast("GroupDefaultBranchProtectionDefaultsOutputReference", jsii.get(self, "defaultBranchProtectionDefaults"))

    @builtins.property
    @jsii.member(jsii_name="fullName")
    def full_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullName"))

    @builtins.property
    @jsii.member(jsii_name="fullPath")
    def full_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullPath"))

    @builtins.property
    @jsii.member(jsii_name="pushRules")
    def push_rules(self) -> "GroupPushRulesOutputReference":
        return typing.cast("GroupPushRulesOutputReference", jsii.get(self, "pushRules"))

    @builtins.property
    @jsii.member(jsii_name="runnersToken")
    def runners_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runnersToken"))

    @builtins.property
    @jsii.member(jsii_name="webUrl")
    def web_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webUrl"))

    @builtins.property
    @jsii.member(jsii_name="allowedEmailDomainsListInput")
    def allowed_email_domains_list_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedEmailDomainsListInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDevopsEnabledInput")
    def auto_devops_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoDevopsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="avatarHashInput")
    def avatar_hash_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "avatarHashInput"))

    @builtins.property
    @jsii.member(jsii_name="avatarInput")
    def avatar_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "avatarInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultBranchInput")
    def default_branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultBranchInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultBranchProtectionDefaultsInput")
    def default_branch_protection_defaults_input(
        self,
    ) -> typing.Optional["GroupDefaultBranchProtectionDefaults"]:
        return typing.cast(typing.Optional["GroupDefaultBranchProtectionDefaults"], jsii.get(self, "defaultBranchProtectionDefaultsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultBranchProtectionInput")
    def default_branch_protection_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultBranchProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="emailsEnabledInput")
    def emails_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "emailsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="extraSharedRunnersMinutesLimitInput")
    def extra_shared_runners_minutes_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "extraSharedRunnersMinutesLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipRestrictionRangesInput")
    def ip_restriction_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipRestrictionRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="lfsEnabledInput")
    def lfs_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "lfsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="membershipLockInput")
    def membership_lock_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "membershipLockInput"))

    @builtins.property
    @jsii.member(jsii_name="mentionsDisabledInput")
    def mentions_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mentionsDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parentIdInput")
    def parent_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "parentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="permanentlyRemoveOnDeleteInput")
    def permanently_remove_on_delete_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "permanentlyRemoveOnDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="preventForkingOutsideGroupInput")
    def prevent_forking_outside_group_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preventForkingOutsideGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="projectCreationLevelInput")
    def project_creation_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectCreationLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="pushRulesInput")
    def push_rules_input(self) -> typing.Optional["GroupPushRules"]:
        return typing.cast(typing.Optional["GroupPushRules"], jsii.get(self, "pushRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="requestAccessEnabledInput")
    def request_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requestAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="requireTwoFactorAuthenticationInput")
    def require_two_factor_authentication_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireTwoFactorAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedRunnersMinutesLimitInput")
    def shared_runners_minutes_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sharedRunnersMinutesLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedRunnersSettingInput")
    def shared_runners_setting_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sharedRunnersSettingInput"))

    @builtins.property
    @jsii.member(jsii_name="shareWithGroupLockInput")
    def share_with_group_lock_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "shareWithGroupLockInput"))

    @builtins.property
    @jsii.member(jsii_name="subgroupCreationLevelInput")
    def subgroup_creation_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subgroupCreationLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="twoFactorGracePeriodInput")
    def two_factor_grace_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "twoFactorGracePeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="visibilityLevelInput")
    def visibility_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "visibilityLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="wikiAccessLevelInput")
    def wiki_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "wikiAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedEmailDomainsList")
    def allowed_email_domains_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedEmailDomainsList"))

    @allowed_email_domains_list.setter
    def allowed_email_domains_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86b83a8bb563d83180de328406f4ccbff317e001b2997d67c67cefeb23cba99f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedEmailDomainsList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoDevopsEnabled")
    def auto_devops_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoDevopsEnabled"))

    @auto_devops_enabled.setter
    def auto_devops_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb5ee5197e43d532cde3f273652c07112905095d2a6f1152af4a95c6019175c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDevopsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="avatar")
    def avatar(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "avatar"))

    @avatar.setter
    def avatar(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__148615bce1ee99aa2d48211049300b3e948839f3bbdcfa7197835c4374b5de38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "avatar", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="avatarHash")
    def avatar_hash(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "avatarHash"))

    @avatar_hash.setter
    def avatar_hash(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd2bd69b6327aa6af28520634ffeceddf190fc35372e700e9fad0f7ba4ed8545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "avatarHash", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultBranch")
    def default_branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultBranch"))

    @default_branch.setter
    def default_branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b90197c9e43fb9f71d3ff4875ab327f746d05b6d8d6b88b5a69c5912b3d4ea09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultBranch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultBranchProtection")
    def default_branch_protection(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultBranchProtection"))

    @default_branch_protection.setter
    def default_branch_protection(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f646129ff3b1ac94eb5501e160b860cbb3e843f10267e6a04e15d7814cdafbe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultBranchProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75058c67534df7bfbb41c981ca9fe3afcbbd097d46590b76fca8d8d0b37761a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailsEnabled")
    def emails_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "emailsEnabled"))

    @emails_enabled.setter
    def emails_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa5233cd262ef4ec404baa4cf1c85e9a6996674c4fa35b997aad9a2455ae422)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extraSharedRunnersMinutesLimit")
    def extra_shared_runners_minutes_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "extraSharedRunnersMinutesLimit"))

    @extra_shared_runners_minutes_limit.setter
    def extra_shared_runners_minutes_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__186e16f0071bd89da8cafd37afba2bb9cbe972375b25824705ccad4c94c20e06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extraSharedRunnersMinutesLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f527c7e04b91b3e7bf7660d3a5c08d27554b9f0ebce9bb4032da93059618a6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipRestrictionRanges")
    def ip_restriction_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipRestrictionRanges"))

    @ip_restriction_ranges.setter
    def ip_restriction_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac15cf8f5ca5b75376e0803f6a765dcaa011c184d4bcceaf7772170c451e59f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipRestrictionRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lfsEnabled")
    def lfs_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "lfsEnabled"))

    @lfs_enabled.setter
    def lfs_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc16ededb6f38b6e437e96239bb840eae9b13730a79acd1a5d99c4aec64a20a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lfsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="membershipLock")
    def membership_lock(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "membershipLock"))

    @membership_lock.setter
    def membership_lock(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b62648375b591a55aee7e12b34809299183acd6e2b72812e23ba582e52509783)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "membershipLock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mentionsDisabled")
    def mentions_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mentionsDisabled"))

    @mentions_disabled.setter
    def mentions_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af60ddd8447ffb32fecca83476a5340d51db60bb2b71f3900068f5977ee8ff05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mentionsDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0bb14e6c07cf1a8841b8e273c6f66d252f8e373eb0c2fd9b8b56ea1093c9041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parentId")
    def parent_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parentId"))

    @parent_id.setter
    def parent_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49fcb463e1b0993fbe3f14f4c83b5aaf2d7df9133c1ab81663c61deb253d4e31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25d6772179f5c1fabd99f58cbea49ded94499d31416518a02eb863f6ee637476)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permanentlyRemoveOnDelete")
    def permanently_remove_on_delete(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "permanentlyRemoveOnDelete"))

    @permanently_remove_on_delete.setter
    def permanently_remove_on_delete(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54896e1e9f3bfc82697b709e1b9a0ff628771c8629f0b675fd73d2922ae78f78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permanentlyRemoveOnDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preventForkingOutsideGroup")
    def prevent_forking_outside_group(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preventForkingOutsideGroup"))

    @prevent_forking_outside_group.setter
    def prevent_forking_outside_group(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70fbab9c6f08d8155eb21fd3f032cc519c3b189c6e8fc6f1538f947486c27ae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preventForkingOutsideGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectCreationLevel")
    def project_creation_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectCreationLevel"))

    @project_creation_level.setter
    def project_creation_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40f064449daebdd56116e7ae8f05437b22e235d31fed5df91af54fac8cf57584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectCreationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestAccessEnabled")
    def request_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requestAccessEnabled"))

    @request_access_enabled.setter
    def request_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f91700aba15219c4f1bbc556e377633b4a649dbbb8407382a4992f215ced69e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireTwoFactorAuthentication")
    def require_two_factor_authentication(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireTwoFactorAuthentication"))

    @require_two_factor_authentication.setter
    def require_two_factor_authentication(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d2fb1ebe02f044414605cb03da58f20f78839a6461b40c908b6ebe0affdc381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireTwoFactorAuthentication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sharedRunnersMinutesLimit")
    def shared_runners_minutes_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sharedRunnersMinutesLimit"))

    @shared_runners_minutes_limit.setter
    def shared_runners_minutes_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19d16b8dd1c124966d12c1dae51287669d9a65c697c8032580b0c084025d1e97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedRunnersMinutesLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sharedRunnersSetting")
    def shared_runners_setting(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharedRunnersSetting"))

    @shared_runners_setting.setter
    def shared_runners_setting(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d0aecf3b5987c15346821d0e04f99365d76cd485ec47bf6142730dfe0ca9da0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedRunnersSetting", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shareWithGroupLock")
    def share_with_group_lock(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "shareWithGroupLock"))

    @share_with_group_lock.setter
    def share_with_group_lock(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__801deadad61e26b6e115bfd915cdc95cbb50b79391824f42de599f8513bd2faa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shareWithGroupLock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subgroupCreationLevel")
    def subgroup_creation_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subgroupCreationLevel"))

    @subgroup_creation_level.setter
    def subgroup_creation_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b1a536720055250a6c0d277303240e4c40d34655d16c329857c0181a095820)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subgroupCreationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="twoFactorGracePeriod")
    def two_factor_grace_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "twoFactorGracePeriod"))

    @two_factor_grace_period.setter
    def two_factor_grace_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be17fd058a0353a8216e9d840411aa6246fa3762369ac7003e066949b7d4019)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twoFactorGracePeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visibilityLevel")
    def visibility_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibilityLevel"))

    @visibility_level.setter
    def visibility_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da56533c35403379cc486ca51558b7465c7715143e7439b1f43894cfe434c733)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibilityLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wikiAccessLevel")
    def wiki_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "wikiAccessLevel"))

    @wiki_access_level.setter
    def wiki_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb8ebbf5a8002e74cab69c6b86c11879bdce11da469fa7277e55269318a3d6b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wikiAccessLevel", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.group.GroupConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "path": "path",
        "allowed_email_domains_list": "allowedEmailDomainsList",
        "auto_devops_enabled": "autoDevopsEnabled",
        "avatar": "avatar",
        "avatar_hash": "avatarHash",
        "default_branch": "defaultBranch",
        "default_branch_protection": "defaultBranchProtection",
        "default_branch_protection_defaults": "defaultBranchProtectionDefaults",
        "description": "description",
        "emails_enabled": "emailsEnabled",
        "extra_shared_runners_minutes_limit": "extraSharedRunnersMinutesLimit",
        "id": "id",
        "ip_restriction_ranges": "ipRestrictionRanges",
        "lfs_enabled": "lfsEnabled",
        "membership_lock": "membershipLock",
        "mentions_disabled": "mentionsDisabled",
        "parent_id": "parentId",
        "permanently_remove_on_delete": "permanentlyRemoveOnDelete",
        "prevent_forking_outside_group": "preventForkingOutsideGroup",
        "project_creation_level": "projectCreationLevel",
        "push_rules": "pushRules",
        "request_access_enabled": "requestAccessEnabled",
        "require_two_factor_authentication": "requireTwoFactorAuthentication",
        "shared_runners_minutes_limit": "sharedRunnersMinutesLimit",
        "shared_runners_setting": "sharedRunnersSetting",
        "share_with_group_lock": "shareWithGroupLock",
        "subgroup_creation_level": "subgroupCreationLevel",
        "two_factor_grace_period": "twoFactorGracePeriod",
        "visibility_level": "visibilityLevel",
        "wiki_access_level": "wikiAccessLevel",
    },
)
class GroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        path: builtins.str,
        allowed_email_domains_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        auto_devops_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        avatar: typing.Optional[builtins.str] = None,
        avatar_hash: typing.Optional[builtins.str] = None,
        default_branch: typing.Optional[builtins.str] = None,
        default_branch_protection: typing.Optional[jsii.Number] = None,
        default_branch_protection_defaults: typing.Optional[typing.Union["GroupDefaultBranchProtectionDefaults", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        emails_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        extra_shared_runners_minutes_limit: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        ip_restriction_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        lfs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        membership_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mentions_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        parent_id: typing.Optional[jsii.Number] = None,
        permanently_remove_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prevent_forking_outside_group: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project_creation_level: typing.Optional[builtins.str] = None,
        push_rules: typing.Optional[typing.Union["GroupPushRules", typing.Dict[builtins.str, typing.Any]]] = None,
        request_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_two_factor_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        shared_runners_minutes_limit: typing.Optional[jsii.Number] = None,
        shared_runners_setting: typing.Optional[builtins.str] = None,
        share_with_group_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subgroup_creation_level: typing.Optional[builtins.str] = None,
        two_factor_grace_period: typing.Optional[jsii.Number] = None,
        visibility_level: typing.Optional[builtins.str] = None,
        wiki_access_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#name Group#name}
        :param path: The path of the group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#path Group#path}
        :param allowed_email_domains_list: A list of email address domains to allow group access. Will be concatenated together into a comma separated string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#allowed_email_domains_list Group#allowed_email_domains_list}
        :param auto_devops_enabled: Default to Auto DevOps pipeline for all projects within this group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#auto_devops_enabled Group#auto_devops_enabled}
        :param avatar: A local path to the avatar image to upload. **Note**: not available for imported resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#avatar Group#avatar}
        :param avatar_hash: The hash of the avatar image. Use ``filesha256("path/to/avatar.png")`` whenever possible. **Note**: this is used to trigger an update of the avatar. If it's not given, but an avatar is given, the avatar will be updated each time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#avatar_hash Group#avatar_hash}
        :param default_branch: Initial default branch name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#default_branch Group#default_branch}
        :param default_branch_protection: See https://docs.gitlab.com/api/groups/#options-for-default_branch_protection. Valid values are: ``0``, ``1``, ``2``, ``3``, ``4``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#default_branch_protection Group#default_branch_protection}
        :param default_branch_protection_defaults: default_branch_protection_defaults block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#default_branch_protection_defaults Group#default_branch_protection_defaults}
        :param description: The group's description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#description Group#description}
        :param emails_enabled: Enable email notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#emails_enabled Group#emails_enabled}
        :param extra_shared_runners_minutes_limit: Can be set by administrators only. Additional CI/CD minutes for this group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#extra_shared_runners_minutes_limit Group#extra_shared_runners_minutes_limit}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#id Group#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_restriction_ranges: A list of IP addresses or subnet masks to restrict group access. Will be concatenated together into a comma separated string. Only allowed on top level groups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#ip_restriction_ranges Group#ip_restriction_ranges}
        :param lfs_enabled: Enable/disable Large File Storage (LFS) for the projects in this group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#lfs_enabled Group#lfs_enabled}
        :param membership_lock: Users cannot be added to projects in this group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#membership_lock Group#membership_lock}
        :param mentions_disabled: Disable the capability of a group from getting mentioned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#mentions_disabled Group#mentions_disabled}
        :param parent_id: Id of the parent group (creates a nested group). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#parent_id Group#parent_id}
        :param permanently_remove_on_delete: Whether the group should be permanently removed during a ``delete`` operation. This only works with subgroups. Must be configured via an ``apply`` before the ``destroy`` is run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#permanently_remove_on_delete Group#permanently_remove_on_delete}
        :param prevent_forking_outside_group: Defaults to false. When enabled, users can not fork projects from this group to external namespaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#prevent_forking_outside_group Group#prevent_forking_outside_group}
        :param project_creation_level: Determine if developers can create projects in the group. Valid values are: ``noone``, ``owner``, ``maintainer``, ``developer``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#project_creation_level Group#project_creation_level}
        :param push_rules: push_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#push_rules Group#push_rules}
        :param request_access_enabled: Allow users to request member access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#request_access_enabled Group#request_access_enabled}
        :param require_two_factor_authentication: Require all users in this group to setup Two-factor authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#require_two_factor_authentication Group#require_two_factor_authentication}
        :param shared_runners_minutes_limit: Can be set by administrators only. Maximum number of monthly CI/CD minutes for this group. Can be nil (default; inherit system default), 0 (unlimited), or > 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#shared_runners_minutes_limit Group#shared_runners_minutes_limit}
        :param shared_runners_setting: Enable or disable shared runners for a group’s subgroups and projects. Valid values are: ``enabled``, ``disabled_and_overridable``, ``disabled_and_unoverridable``, ``disabled_with_override``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#shared_runners_setting Group#shared_runners_setting}
        :param share_with_group_lock: Prevent sharing a project with another group within this group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#share_with_group_lock Group#share_with_group_lock}
        :param subgroup_creation_level: Allowed to create subgroups. Valid values are: ``owner``, ``maintainer``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#subgroup_creation_level Group#subgroup_creation_level}
        :param two_factor_grace_period: Defaults to 48. Time before Two-factor authentication is enforced (in hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#two_factor_grace_period Group#two_factor_grace_period}
        :param visibility_level: The group's visibility. Can be ``private``, ``internal``, or ``public``. Valid values are: ``private``, ``internal``, ``public``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#visibility_level Group#visibility_level}
        :param wiki_access_level: The group's wiki access level. Only available on Premium and Ultimate plans. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#wiki_access_level Group#wiki_access_level}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(default_branch_protection_defaults, dict):
            default_branch_protection_defaults = GroupDefaultBranchProtectionDefaults(**default_branch_protection_defaults)
        if isinstance(push_rules, dict):
            push_rules = GroupPushRules(**push_rules)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b46134b12f9e1fce1e34db566aea38b84df83b20de8e3094a6537f60b3321e3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument allowed_email_domains_list", value=allowed_email_domains_list, expected_type=type_hints["allowed_email_domains_list"])
            check_type(argname="argument auto_devops_enabled", value=auto_devops_enabled, expected_type=type_hints["auto_devops_enabled"])
            check_type(argname="argument avatar", value=avatar, expected_type=type_hints["avatar"])
            check_type(argname="argument avatar_hash", value=avatar_hash, expected_type=type_hints["avatar_hash"])
            check_type(argname="argument default_branch", value=default_branch, expected_type=type_hints["default_branch"])
            check_type(argname="argument default_branch_protection", value=default_branch_protection, expected_type=type_hints["default_branch_protection"])
            check_type(argname="argument default_branch_protection_defaults", value=default_branch_protection_defaults, expected_type=type_hints["default_branch_protection_defaults"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument emails_enabled", value=emails_enabled, expected_type=type_hints["emails_enabled"])
            check_type(argname="argument extra_shared_runners_minutes_limit", value=extra_shared_runners_minutes_limit, expected_type=type_hints["extra_shared_runners_minutes_limit"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_restriction_ranges", value=ip_restriction_ranges, expected_type=type_hints["ip_restriction_ranges"])
            check_type(argname="argument lfs_enabled", value=lfs_enabled, expected_type=type_hints["lfs_enabled"])
            check_type(argname="argument membership_lock", value=membership_lock, expected_type=type_hints["membership_lock"])
            check_type(argname="argument mentions_disabled", value=mentions_disabled, expected_type=type_hints["mentions_disabled"])
            check_type(argname="argument parent_id", value=parent_id, expected_type=type_hints["parent_id"])
            check_type(argname="argument permanently_remove_on_delete", value=permanently_remove_on_delete, expected_type=type_hints["permanently_remove_on_delete"])
            check_type(argname="argument prevent_forking_outside_group", value=prevent_forking_outside_group, expected_type=type_hints["prevent_forking_outside_group"])
            check_type(argname="argument project_creation_level", value=project_creation_level, expected_type=type_hints["project_creation_level"])
            check_type(argname="argument push_rules", value=push_rules, expected_type=type_hints["push_rules"])
            check_type(argname="argument request_access_enabled", value=request_access_enabled, expected_type=type_hints["request_access_enabled"])
            check_type(argname="argument require_two_factor_authentication", value=require_two_factor_authentication, expected_type=type_hints["require_two_factor_authentication"])
            check_type(argname="argument shared_runners_minutes_limit", value=shared_runners_minutes_limit, expected_type=type_hints["shared_runners_minutes_limit"])
            check_type(argname="argument shared_runners_setting", value=shared_runners_setting, expected_type=type_hints["shared_runners_setting"])
            check_type(argname="argument share_with_group_lock", value=share_with_group_lock, expected_type=type_hints["share_with_group_lock"])
            check_type(argname="argument subgroup_creation_level", value=subgroup_creation_level, expected_type=type_hints["subgroup_creation_level"])
            check_type(argname="argument two_factor_grace_period", value=two_factor_grace_period, expected_type=type_hints["two_factor_grace_period"])
            check_type(argname="argument visibility_level", value=visibility_level, expected_type=type_hints["visibility_level"])
            check_type(argname="argument wiki_access_level", value=wiki_access_level, expected_type=type_hints["wiki_access_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "path": path,
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
        if allowed_email_domains_list is not None:
            self._values["allowed_email_domains_list"] = allowed_email_domains_list
        if auto_devops_enabled is not None:
            self._values["auto_devops_enabled"] = auto_devops_enabled
        if avatar is not None:
            self._values["avatar"] = avatar
        if avatar_hash is not None:
            self._values["avatar_hash"] = avatar_hash
        if default_branch is not None:
            self._values["default_branch"] = default_branch
        if default_branch_protection is not None:
            self._values["default_branch_protection"] = default_branch_protection
        if default_branch_protection_defaults is not None:
            self._values["default_branch_protection_defaults"] = default_branch_protection_defaults
        if description is not None:
            self._values["description"] = description
        if emails_enabled is not None:
            self._values["emails_enabled"] = emails_enabled
        if extra_shared_runners_minutes_limit is not None:
            self._values["extra_shared_runners_minutes_limit"] = extra_shared_runners_minutes_limit
        if id is not None:
            self._values["id"] = id
        if ip_restriction_ranges is not None:
            self._values["ip_restriction_ranges"] = ip_restriction_ranges
        if lfs_enabled is not None:
            self._values["lfs_enabled"] = lfs_enabled
        if membership_lock is not None:
            self._values["membership_lock"] = membership_lock
        if mentions_disabled is not None:
            self._values["mentions_disabled"] = mentions_disabled
        if parent_id is not None:
            self._values["parent_id"] = parent_id
        if permanently_remove_on_delete is not None:
            self._values["permanently_remove_on_delete"] = permanently_remove_on_delete
        if prevent_forking_outside_group is not None:
            self._values["prevent_forking_outside_group"] = prevent_forking_outside_group
        if project_creation_level is not None:
            self._values["project_creation_level"] = project_creation_level
        if push_rules is not None:
            self._values["push_rules"] = push_rules
        if request_access_enabled is not None:
            self._values["request_access_enabled"] = request_access_enabled
        if require_two_factor_authentication is not None:
            self._values["require_two_factor_authentication"] = require_two_factor_authentication
        if shared_runners_minutes_limit is not None:
            self._values["shared_runners_minutes_limit"] = shared_runners_minutes_limit
        if shared_runners_setting is not None:
            self._values["shared_runners_setting"] = shared_runners_setting
        if share_with_group_lock is not None:
            self._values["share_with_group_lock"] = share_with_group_lock
        if subgroup_creation_level is not None:
            self._values["subgroup_creation_level"] = subgroup_creation_level
        if two_factor_grace_period is not None:
            self._values["two_factor_grace_period"] = two_factor_grace_period
        if visibility_level is not None:
            self._values["visibility_level"] = visibility_level
        if wiki_access_level is not None:
            self._values["wiki_access_level"] = wiki_access_level

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
    def name(self) -> builtins.str:
        '''The name of the group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#name Group#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''The path of the group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#path Group#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_email_domains_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of email address domains to allow group access. Will be concatenated together into a comma separated string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#allowed_email_domains_list Group#allowed_email_domains_list}
        '''
        result = self._values.get("allowed_email_domains_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def auto_devops_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Default to Auto DevOps pipeline for all projects within this group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#auto_devops_enabled Group#auto_devops_enabled}
        '''
        result = self._values.get("auto_devops_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def avatar(self) -> typing.Optional[builtins.str]:
        '''A local path to the avatar image to upload. **Note**: not available for imported resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#avatar Group#avatar}
        '''
        result = self._values.get("avatar")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def avatar_hash(self) -> typing.Optional[builtins.str]:
        '''The hash of the avatar image.

        Use ``filesha256("path/to/avatar.png")`` whenever possible. **Note**: this is used to trigger an update of the avatar. If it's not given, but an avatar is given, the avatar will be updated each time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#avatar_hash Group#avatar_hash}
        '''
        result = self._values.get("avatar_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_branch(self) -> typing.Optional[builtins.str]:
        '''Initial default branch name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#default_branch Group#default_branch}
        '''
        result = self._values.get("default_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_branch_protection(self) -> typing.Optional[jsii.Number]:
        '''See https://docs.gitlab.com/api/groups/#options-for-default_branch_protection. Valid values are: ``0``, ``1``, ``2``, ``3``, ``4``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#default_branch_protection Group#default_branch_protection}
        '''
        result = self._values.get("default_branch_protection")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_branch_protection_defaults(
        self,
    ) -> typing.Optional["GroupDefaultBranchProtectionDefaults"]:
        '''default_branch_protection_defaults block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#default_branch_protection_defaults Group#default_branch_protection_defaults}
        '''
        result = self._values.get("default_branch_protection_defaults")
        return typing.cast(typing.Optional["GroupDefaultBranchProtectionDefaults"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The group's description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#description Group#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def emails_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable email notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#emails_enabled Group#emails_enabled}
        '''
        result = self._values.get("emails_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def extra_shared_runners_minutes_limit(self) -> typing.Optional[jsii.Number]:
        '''Can be set by administrators only. Additional CI/CD minutes for this group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#extra_shared_runners_minutes_limit Group#extra_shared_runners_minutes_limit}
        '''
        result = self._values.get("extra_shared_runners_minutes_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#id Group#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_restriction_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IP addresses or subnet masks to restrict group access.

        Will be concatenated together into a comma separated string. Only allowed on top level groups.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#ip_restriction_ranges Group#ip_restriction_ranges}
        '''
        result = self._values.get("ip_restriction_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def lfs_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable/disable Large File Storage (LFS) for the projects in this group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#lfs_enabled Group#lfs_enabled}
        '''
        result = self._values.get("lfs_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def membership_lock(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Users cannot be added to projects in this group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#membership_lock Group#membership_lock}
        '''
        result = self._values.get("membership_lock")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def mentions_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable the capability of a group from getting mentioned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#mentions_disabled Group#mentions_disabled}
        '''
        result = self._values.get("mentions_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def parent_id(self) -> typing.Optional[jsii.Number]:
        '''Id of the parent group (creates a nested group).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#parent_id Group#parent_id}
        '''
        result = self._values.get("parent_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def permanently_remove_on_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the group should be permanently removed during a ``delete`` operation.

        This only works with subgroups. Must be configured via an ``apply`` before the ``destroy`` is run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#permanently_remove_on_delete Group#permanently_remove_on_delete}
        '''
        result = self._values.get("permanently_remove_on_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prevent_forking_outside_group(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defaults to false. When enabled, users can not fork projects from this group to external namespaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#prevent_forking_outside_group Group#prevent_forking_outside_group}
        '''
        result = self._values.get("prevent_forking_outside_group")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project_creation_level(self) -> typing.Optional[builtins.str]:
        '''Determine if developers can create projects in the group. Valid values are: ``noone``, ``owner``, ``maintainer``, ``developer``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#project_creation_level Group#project_creation_level}
        '''
        result = self._values.get("project_creation_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def push_rules(self) -> typing.Optional["GroupPushRules"]:
        '''push_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#push_rules Group#push_rules}
        '''
        result = self._values.get("push_rules")
        return typing.cast(typing.Optional["GroupPushRules"], result)

    @builtins.property
    def request_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow users to request member access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#request_access_enabled Group#request_access_enabled}
        '''
        result = self._values.get("request_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_two_factor_authentication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Require all users in this group to setup Two-factor authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#require_two_factor_authentication Group#require_two_factor_authentication}
        '''
        result = self._values.get("require_two_factor_authentication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def shared_runners_minutes_limit(self) -> typing.Optional[jsii.Number]:
        '''Can be set by administrators only.

        Maximum number of monthly CI/CD minutes for this group. Can be nil (default; inherit system default), 0 (unlimited), or > 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#shared_runners_minutes_limit Group#shared_runners_minutes_limit}
        '''
        result = self._values.get("shared_runners_minutes_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def shared_runners_setting(self) -> typing.Optional[builtins.str]:
        '''Enable or disable shared runners for a group’s subgroups and projects. Valid values are: ``enabled``, ``disabled_and_overridable``, ``disabled_and_unoverridable``, ``disabled_with_override``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#shared_runners_setting Group#shared_runners_setting}
        '''
        result = self._values.get("shared_runners_setting")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def share_with_group_lock(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Prevent sharing a project with another group within this group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#share_with_group_lock Group#share_with_group_lock}
        '''
        result = self._values.get("share_with_group_lock")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def subgroup_creation_level(self) -> typing.Optional[builtins.str]:
        '''Allowed to create subgroups. Valid values are: ``owner``, ``maintainer``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#subgroup_creation_level Group#subgroup_creation_level}
        '''
        result = self._values.get("subgroup_creation_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def two_factor_grace_period(self) -> typing.Optional[jsii.Number]:
        '''Defaults to 48. Time before Two-factor authentication is enforced (in hours).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#two_factor_grace_period Group#two_factor_grace_period}
        '''
        result = self._values.get("two_factor_grace_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def visibility_level(self) -> typing.Optional[builtins.str]:
        '''The group's visibility. Can be ``private``, ``internal``, or ``public``. Valid values are: ``private``, ``internal``, ``public``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#visibility_level Group#visibility_level}
        '''
        result = self._values.get("visibility_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wiki_access_level(self) -> typing.Optional[builtins.str]:
        '''The group's wiki access level. Only available on Premium and Ultimate plans. Valid values are ``disabled``, ``private``, ``enabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#wiki_access_level Group#wiki_access_level}
        '''
        result = self._values.get("wiki_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.group.GroupDefaultBranchProtectionDefaults",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_to_merge": "allowedToMerge",
        "allowed_to_push": "allowedToPush",
        "allow_force_push": "allowForcePush",
        "developer_can_initial_push": "developerCanInitialPush",
    },
)
class GroupDefaultBranchProtectionDefaults:
    def __init__(
        self,
        *,
        allowed_to_merge: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_to_push: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_force_push: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        developer_can_initial_push: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_to_merge: An array of access levels allowed to merge. Valid values are: ``developer``, ``maintainer``, ``no one``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#allowed_to_merge Group#allowed_to_merge}
        :param allowed_to_push: An array of access levels allowed to push. Valid values are: ``developer``, ``maintainer``, ``no one``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#allowed_to_push Group#allowed_to_push}
        :param allow_force_push: Allow force push for all users with push access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#allow_force_push Group#allow_force_push}
        :param developer_can_initial_push: Allow developers to initial push. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#developer_can_initial_push Group#developer_can_initial_push}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d225d22954028e2cce0967b844f18ecc299c5fe3f1b7539434d706146496f7f)
            check_type(argname="argument allowed_to_merge", value=allowed_to_merge, expected_type=type_hints["allowed_to_merge"])
            check_type(argname="argument allowed_to_push", value=allowed_to_push, expected_type=type_hints["allowed_to_push"])
            check_type(argname="argument allow_force_push", value=allow_force_push, expected_type=type_hints["allow_force_push"])
            check_type(argname="argument developer_can_initial_push", value=developer_can_initial_push, expected_type=type_hints["developer_can_initial_push"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_to_merge is not None:
            self._values["allowed_to_merge"] = allowed_to_merge
        if allowed_to_push is not None:
            self._values["allowed_to_push"] = allowed_to_push
        if allow_force_push is not None:
            self._values["allow_force_push"] = allow_force_push
        if developer_can_initial_push is not None:
            self._values["developer_can_initial_push"] = developer_can_initial_push

    @builtins.property
    def allowed_to_merge(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of access levels allowed to merge. Valid values are: ``developer``, ``maintainer``, ``no one``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#allowed_to_merge Group#allowed_to_merge}
        '''
        result = self._values.get("allowed_to_merge")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_to_push(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of access levels allowed to push. Valid values are: ``developer``, ``maintainer``, ``no one``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#allowed_to_push Group#allowed_to_push}
        '''
        result = self._values.get("allowed_to_push")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allow_force_push(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow force push for all users with push access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#allow_force_push Group#allow_force_push}
        '''
        result = self._values.get("allow_force_push")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def developer_can_initial_push(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow developers to initial push.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#developer_can_initial_push Group#developer_can_initial_push}
        '''
        result = self._values.get("developer_can_initial_push")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupDefaultBranchProtectionDefaults(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupDefaultBranchProtectionDefaultsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.group.GroupDefaultBranchProtectionDefaultsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4b91584f693cb9c2aaec86aeca4318bcf92446a2a20c15d1292ab51afb434df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedToMerge")
    def reset_allowed_to_merge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedToMerge", []))

    @jsii.member(jsii_name="resetAllowedToPush")
    def reset_allowed_to_push(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedToPush", []))

    @jsii.member(jsii_name="resetAllowForcePush")
    def reset_allow_force_push(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowForcePush", []))

    @jsii.member(jsii_name="resetDeveloperCanInitialPush")
    def reset_developer_can_initial_push(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeveloperCanInitialPush", []))

    @builtins.property
    @jsii.member(jsii_name="allowedToMergeInput")
    def allowed_to_merge_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedToMergeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedToPushInput")
    def allowed_to_push_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedToPushInput"))

    @builtins.property
    @jsii.member(jsii_name="allowForcePushInput")
    def allow_force_push_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowForcePushInput"))

    @builtins.property
    @jsii.member(jsii_name="developerCanInitialPushInput")
    def developer_can_initial_push_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "developerCanInitialPushInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedToMerge")
    def allowed_to_merge(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedToMerge"))

    @allowed_to_merge.setter
    def allowed_to_merge(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2342717eb91da11b37a222806d5cb44ab49eb5d4ef369c8f9cc6e2f52195d13c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedToMerge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedToPush")
    def allowed_to_push(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedToPush"))

    @allowed_to_push.setter
    def allowed_to_push(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__988d6ca69dfe7290ccb9996fc3a03395156124ce767036ad934b40b33f3bbbff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedToPush", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__cc7f3a1e26da2272d693c1783b5ec3b62105ac1292f6b962a0b0694f1939ac3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowForcePush", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="developerCanInitialPush")
    def developer_can_initial_push(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "developerCanInitialPush"))

    @developer_can_initial_push.setter
    def developer_can_initial_push(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39de5fe5b94983695451211edc1493c4ce24b39ddd35bc8f0aeec92ebf26a8e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "developerCanInitialPush", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GroupDefaultBranchProtectionDefaults]:
        return typing.cast(typing.Optional[GroupDefaultBranchProtectionDefaults], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GroupDefaultBranchProtectionDefaults],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78ef82fb8a11b8c1c982cfe3cf885a43b16c3bb0020d0af5bd1ba231a82661ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.group.GroupPushRules",
    jsii_struct_bases=[],
    name_mapping={
        "author_email_regex": "authorEmailRegex",
        "branch_name_regex": "branchNameRegex",
        "commit_committer_check": "commitCommitterCheck",
        "commit_committer_name_check": "commitCommitterNameCheck",
        "commit_message_negative_regex": "commitMessageNegativeRegex",
        "commit_message_regex": "commitMessageRegex",
        "deny_delete_tag": "denyDeleteTag",
        "file_name_regex": "fileNameRegex",
        "max_file_size": "maxFileSize",
        "member_check": "memberCheck",
        "prevent_secrets": "preventSecrets",
        "reject_non_dco_commits": "rejectNonDcoCommits",
        "reject_unsigned_commits": "rejectUnsignedCommits",
    },
)
class GroupPushRules:
    def __init__(
        self,
        *,
        author_email_regex: typing.Optional[builtins.str] = None,
        branch_name_regex: typing.Optional[builtins.str] = None,
        commit_committer_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        commit_committer_name_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        commit_message_negative_regex: typing.Optional[builtins.str] = None,
        commit_message_regex: typing.Optional[builtins.str] = None,
        deny_delete_tag: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        file_name_regex: typing.Optional[builtins.str] = None,
        max_file_size: typing.Optional[jsii.Number] = None,
        member_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prevent_secrets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reject_non_dco_commits: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reject_unsigned_commits: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param author_email_regex: All commit author emails must match this regex, e.g. ``@my-company.com$``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#author_email_regex Group#author_email_regex}
        :param branch_name_regex: All branch names must match this regex, e.g. ``(feature|hotfix)\\/*``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#branch_name_regex Group#branch_name_regex}
        :param commit_committer_check: Only commits pushed using verified emails are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#commit_committer_check Group#commit_committer_check}
        :param commit_committer_name_check: Users can only push commits to this repository if the commit author name is consistent with their GitLab account name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#commit_committer_name_check Group#commit_committer_name_check}
        :param commit_message_negative_regex: No commit message is allowed to match this regex, for example ``ssh\\:\\/\\/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#commit_message_negative_regex Group#commit_message_negative_regex}
        :param commit_message_regex: All commit messages must match this regex, e.g. ``Fixed \\d+\\..*``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#commit_message_regex Group#commit_message_regex}
        :param deny_delete_tag: Deny deleting a tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#deny_delete_tag Group#deny_delete_tag}
        :param file_name_regex: Filenames matching the regular expression provided in this attribute are not allowed, for example, ``(jar|exe)$``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#file_name_regex Group#file_name_regex}
        :param max_file_size: Maximum file size (MB) allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#max_file_size Group#max_file_size}
        :param member_check: Allows only GitLab users to author commits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#member_check Group#member_check}
        :param prevent_secrets: GitLab will reject any files that are likely to contain secrets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#prevent_secrets Group#prevent_secrets}
        :param reject_non_dco_commits: Reject commit when it’s not DCO certified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#reject_non_dco_commits Group#reject_non_dco_commits}
        :param reject_unsigned_commits: Only commits signed through GPG are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#reject_unsigned_commits Group#reject_unsigned_commits}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd00b5cb1e872a0d32d959906ae6c3dbaa6f375100d73598898655e44645d38)
            check_type(argname="argument author_email_regex", value=author_email_regex, expected_type=type_hints["author_email_regex"])
            check_type(argname="argument branch_name_regex", value=branch_name_regex, expected_type=type_hints["branch_name_regex"])
            check_type(argname="argument commit_committer_check", value=commit_committer_check, expected_type=type_hints["commit_committer_check"])
            check_type(argname="argument commit_committer_name_check", value=commit_committer_name_check, expected_type=type_hints["commit_committer_name_check"])
            check_type(argname="argument commit_message_negative_regex", value=commit_message_negative_regex, expected_type=type_hints["commit_message_negative_regex"])
            check_type(argname="argument commit_message_regex", value=commit_message_regex, expected_type=type_hints["commit_message_regex"])
            check_type(argname="argument deny_delete_tag", value=deny_delete_tag, expected_type=type_hints["deny_delete_tag"])
            check_type(argname="argument file_name_regex", value=file_name_regex, expected_type=type_hints["file_name_regex"])
            check_type(argname="argument max_file_size", value=max_file_size, expected_type=type_hints["max_file_size"])
            check_type(argname="argument member_check", value=member_check, expected_type=type_hints["member_check"])
            check_type(argname="argument prevent_secrets", value=prevent_secrets, expected_type=type_hints["prevent_secrets"])
            check_type(argname="argument reject_non_dco_commits", value=reject_non_dco_commits, expected_type=type_hints["reject_non_dco_commits"])
            check_type(argname="argument reject_unsigned_commits", value=reject_unsigned_commits, expected_type=type_hints["reject_unsigned_commits"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if author_email_regex is not None:
            self._values["author_email_regex"] = author_email_regex
        if branch_name_regex is not None:
            self._values["branch_name_regex"] = branch_name_regex
        if commit_committer_check is not None:
            self._values["commit_committer_check"] = commit_committer_check
        if commit_committer_name_check is not None:
            self._values["commit_committer_name_check"] = commit_committer_name_check
        if commit_message_negative_regex is not None:
            self._values["commit_message_negative_regex"] = commit_message_negative_regex
        if commit_message_regex is not None:
            self._values["commit_message_regex"] = commit_message_regex
        if deny_delete_tag is not None:
            self._values["deny_delete_tag"] = deny_delete_tag
        if file_name_regex is not None:
            self._values["file_name_regex"] = file_name_regex
        if max_file_size is not None:
            self._values["max_file_size"] = max_file_size
        if member_check is not None:
            self._values["member_check"] = member_check
        if prevent_secrets is not None:
            self._values["prevent_secrets"] = prevent_secrets
        if reject_non_dco_commits is not None:
            self._values["reject_non_dco_commits"] = reject_non_dco_commits
        if reject_unsigned_commits is not None:
            self._values["reject_unsigned_commits"] = reject_unsigned_commits

    @builtins.property
    def author_email_regex(self) -> typing.Optional[builtins.str]:
        '''All commit author emails must match this regex, e.g. ``@my-company.com$``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#author_email_regex Group#author_email_regex}
        '''
        result = self._values.get("author_email_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def branch_name_regex(self) -> typing.Optional[builtins.str]:
        '''All branch names must match this regex, e.g. ``(feature|hotfix)\\/*``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#branch_name_regex Group#branch_name_regex}
        '''
        result = self._values.get("branch_name_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def commit_committer_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only commits pushed using verified emails are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#commit_committer_check Group#commit_committer_check}
        '''
        result = self._values.get("commit_committer_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def commit_committer_name_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Users can only push commits to this repository if the commit author name is consistent with their GitLab account name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#commit_committer_name_check Group#commit_committer_name_check}
        '''
        result = self._values.get("commit_committer_name_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def commit_message_negative_regex(self) -> typing.Optional[builtins.str]:
        '''No commit message is allowed to match this regex, for example ``ssh\\:\\/\\/``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#commit_message_negative_regex Group#commit_message_negative_regex}
        '''
        result = self._values.get("commit_message_negative_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def commit_message_regex(self) -> typing.Optional[builtins.str]:
        '''All commit messages must match this regex, e.g. ``Fixed \\d+\\..*``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#commit_message_regex Group#commit_message_regex}
        '''
        result = self._values.get("commit_message_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deny_delete_tag(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Deny deleting a tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#deny_delete_tag Group#deny_delete_tag}
        '''
        result = self._values.get("deny_delete_tag")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def file_name_regex(self) -> typing.Optional[builtins.str]:
        '''Filenames matching the regular expression provided in this attribute are not allowed, for example, ``(jar|exe)$``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#file_name_regex Group#file_name_regex}
        '''
        result = self._values.get("file_name_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_file_size(self) -> typing.Optional[jsii.Number]:
        '''Maximum file size (MB) allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#max_file_size Group#max_file_size}
        '''
        result = self._values.get("max_file_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def member_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allows only GitLab users to author commits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#member_check Group#member_check}
        '''
        result = self._values.get("member_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prevent_secrets(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''GitLab will reject any files that are likely to contain secrets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#prevent_secrets Group#prevent_secrets}
        '''
        result = self._values.get("prevent_secrets")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reject_non_dco_commits(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Reject commit when it’s not DCO certified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#reject_non_dco_commits Group#reject_non_dco_commits}
        '''
        result = self._values.get("reject_non_dco_commits")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reject_unsigned_commits(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only commits signed through GPG are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/group#reject_unsigned_commits Group#reject_unsigned_commits}
        '''
        result = self._values.get("reject_unsigned_commits")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupPushRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupPushRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.group.GroupPushRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec72a20314f89c6f506304165c563f7ff8945813651e6bfa0cc786e6e67f79d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthorEmailRegex")
    def reset_author_email_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorEmailRegex", []))

    @jsii.member(jsii_name="resetBranchNameRegex")
    def reset_branch_name_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBranchNameRegex", []))

    @jsii.member(jsii_name="resetCommitCommitterCheck")
    def reset_commit_committer_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitCommitterCheck", []))

    @jsii.member(jsii_name="resetCommitCommitterNameCheck")
    def reset_commit_committer_name_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitCommitterNameCheck", []))

    @jsii.member(jsii_name="resetCommitMessageNegativeRegex")
    def reset_commit_message_negative_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitMessageNegativeRegex", []))

    @jsii.member(jsii_name="resetCommitMessageRegex")
    def reset_commit_message_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitMessageRegex", []))

    @jsii.member(jsii_name="resetDenyDeleteTag")
    def reset_deny_delete_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDenyDeleteTag", []))

    @jsii.member(jsii_name="resetFileNameRegex")
    def reset_file_name_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileNameRegex", []))

    @jsii.member(jsii_name="resetMaxFileSize")
    def reset_max_file_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxFileSize", []))

    @jsii.member(jsii_name="resetMemberCheck")
    def reset_member_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemberCheck", []))

    @jsii.member(jsii_name="resetPreventSecrets")
    def reset_prevent_secrets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreventSecrets", []))

    @jsii.member(jsii_name="resetRejectNonDcoCommits")
    def reset_reject_non_dco_commits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRejectNonDcoCommits", []))

    @jsii.member(jsii_name="resetRejectUnsignedCommits")
    def reset_reject_unsigned_commits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRejectUnsignedCommits", []))

    @builtins.property
    @jsii.member(jsii_name="authorEmailRegexInput")
    def author_email_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorEmailRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="branchNameRegexInput")
    def branch_name_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchNameRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="commitCommitterCheckInput")
    def commit_committer_check_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "commitCommitterCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="commitCommitterNameCheckInput")
    def commit_committer_name_check_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "commitCommitterNameCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="commitMessageNegativeRegexInput")
    def commit_message_negative_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitMessageNegativeRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="commitMessageRegexInput")
    def commit_message_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitMessageRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="denyDeleteTagInput")
    def deny_delete_tag_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "denyDeleteTagInput"))

    @builtins.property
    @jsii.member(jsii_name="fileNameRegexInput")
    def file_name_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileNameRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFileSizeInput")
    def max_file_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxFileSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="memberCheckInput")
    def member_check_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "memberCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="preventSecretsInput")
    def prevent_secrets_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preventSecretsInput"))

    @builtins.property
    @jsii.member(jsii_name="rejectNonDcoCommitsInput")
    def reject_non_dco_commits_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rejectNonDcoCommitsInput"))

    @builtins.property
    @jsii.member(jsii_name="rejectUnsignedCommitsInput")
    def reject_unsigned_commits_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rejectUnsignedCommitsInput"))

    @builtins.property
    @jsii.member(jsii_name="authorEmailRegex")
    def author_email_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorEmailRegex"))

    @author_email_regex.setter
    def author_email_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4145809e63529ab82119bcc9c3f3c3a2429b440ee0f1a4de584c6ff74dc55805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorEmailRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="branchNameRegex")
    def branch_name_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branchNameRegex"))

    @branch_name_regex.setter
    def branch_name_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9715749781fc0985da5f1f9c6ab5887e99a61c06f9d405e5be48076cf3037796)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branchNameRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commitCommitterCheck")
    def commit_committer_check(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "commitCommitterCheck"))

    @commit_committer_check.setter
    def commit_committer_check(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bff69425d2e8b65c8075a1a090065326eec01ce4ee5f24e0582aec8c26ee85e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitCommitterCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commitCommitterNameCheck")
    def commit_committer_name_check(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "commitCommitterNameCheck"))

    @commit_committer_name_check.setter
    def commit_committer_name_check(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42162a0123cd4d1597483454bc6bc1c32a433024fcc0b18e4ea602d66484abae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitCommitterNameCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commitMessageNegativeRegex")
    def commit_message_negative_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitMessageNegativeRegex"))

    @commit_message_negative_regex.setter
    def commit_message_negative_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1159c1e36e6a9948be3e8266ab78f971a3eb3ed3c9d17c352771b44d299c1ad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitMessageNegativeRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commitMessageRegex")
    def commit_message_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitMessageRegex"))

    @commit_message_regex.setter
    def commit_message_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15699eddbc95845ef6510d849c359c3c7fb0c45e73436d476acbbd417b272f67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitMessageRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="denyDeleteTag")
    def deny_delete_tag(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "denyDeleteTag"))

    @deny_delete_tag.setter
    def deny_delete_tag(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a7d0a5e96303a823320c2f43a24af40c4719f5fe15d80f4f724a1e596ad6db1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "denyDeleteTag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileNameRegex")
    def file_name_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileNameRegex"))

    @file_name_regex.setter
    def file_name_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__351b513d6c9adacfa74884cc48ba83744af5692674453459d11ecc2561f43749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileNameRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxFileSize")
    def max_file_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxFileSize"))

    @max_file_size.setter
    def max_file_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc740436a0fa2cbfabb0628b4d36beea546b17b3cebdc0f23abf681926581f34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFileSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memberCheck")
    def member_check(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "memberCheck"))

    @member_check.setter
    def member_check(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6e530bdc6c90f6f3346e182d4170213ae7bf50a62696c5c2e23fd99123ec5b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preventSecrets")
    def prevent_secrets(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preventSecrets"))

    @prevent_secrets.setter
    def prevent_secrets(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd970191e5909c705851cb62df42b05ef54df7e40afb1a723c1b3729b344e034)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preventSecrets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rejectNonDcoCommits")
    def reject_non_dco_commits(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rejectNonDcoCommits"))

    @reject_non_dco_commits.setter
    def reject_non_dco_commits(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5650e301ff86edb4b8d0af5b0d2d7b16ba673bc64a083bd82029a52fad422e53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rejectNonDcoCommits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rejectUnsignedCommits")
    def reject_unsigned_commits(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rejectUnsignedCommits"))

    @reject_unsigned_commits.setter
    def reject_unsigned_commits(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24fcad344ab9bdc0011a46829540ecc1016a3c5f37e01e546c2865cdd34c1046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rejectUnsignedCommits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GroupPushRules]:
        return typing.cast(typing.Optional[GroupPushRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GroupPushRules]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e12668c20d36c76cc8f295b892202b314e4c83c0c14d9fff7382061dda895449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Group",
    "GroupConfig",
    "GroupDefaultBranchProtectionDefaults",
    "GroupDefaultBranchProtectionDefaultsOutputReference",
    "GroupPushRules",
    "GroupPushRulesOutputReference",
]

publication.publish()

def _typecheckingstub__2ba99799c3dfc0c212cdf9860e0ebe4109245373801789101a41d768bfb63c07(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    path: builtins.str,
    allowed_email_domains_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    auto_devops_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    avatar: typing.Optional[builtins.str] = None,
    avatar_hash: typing.Optional[builtins.str] = None,
    default_branch: typing.Optional[builtins.str] = None,
    default_branch_protection: typing.Optional[jsii.Number] = None,
    default_branch_protection_defaults: typing.Optional[typing.Union[GroupDefaultBranchProtectionDefaults, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    emails_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    extra_shared_runners_minutes_limit: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    ip_restriction_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    lfs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    membership_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mentions_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    parent_id: typing.Optional[jsii.Number] = None,
    permanently_remove_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prevent_forking_outside_group: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project_creation_level: typing.Optional[builtins.str] = None,
    push_rules: typing.Optional[typing.Union[GroupPushRules, typing.Dict[builtins.str, typing.Any]]] = None,
    request_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_two_factor_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    shared_runners_minutes_limit: typing.Optional[jsii.Number] = None,
    shared_runners_setting: typing.Optional[builtins.str] = None,
    share_with_group_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subgroup_creation_level: typing.Optional[builtins.str] = None,
    two_factor_grace_period: typing.Optional[jsii.Number] = None,
    visibility_level: typing.Optional[builtins.str] = None,
    wiki_access_level: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__c9eebe69803e07a85ec4e8f611a727d5a6b6a34d84175638f68ed4a41af6cfe3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b83a8bb563d83180de328406f4ccbff317e001b2997d67c67cefeb23cba99f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb5ee5197e43d532cde3f273652c07112905095d2a6f1152af4a95c6019175c6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__148615bce1ee99aa2d48211049300b3e948839f3bbdcfa7197835c4374b5de38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd2bd69b6327aa6af28520634ffeceddf190fc35372e700e9fad0f7ba4ed8545(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90197c9e43fb9f71d3ff4875ab327f746d05b6d8d6b88b5a69c5912b3d4ea09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f646129ff3b1ac94eb5501e160b860cbb3e843f10267e6a04e15d7814cdafbe1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75058c67534df7bfbb41c981ca9fe3afcbbd097d46590b76fca8d8d0b37761a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa5233cd262ef4ec404baa4cf1c85e9a6996674c4fa35b997aad9a2455ae422(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186e16f0071bd89da8cafd37afba2bb9cbe972375b25824705ccad4c94c20e06(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f527c7e04b91b3e7bf7660d3a5c08d27554b9f0ebce9bb4032da93059618a6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac15cf8f5ca5b75376e0803f6a765dcaa011c184d4bcceaf7772170c451e59f4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc16ededb6f38b6e437e96239bb840eae9b13730a79acd1a5d99c4aec64a20a2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b62648375b591a55aee7e12b34809299183acd6e2b72812e23ba582e52509783(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af60ddd8447ffb32fecca83476a5340d51db60bb2b71f3900068f5977ee8ff05(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0bb14e6c07cf1a8841b8e273c6f66d252f8e373eb0c2fd9b8b56ea1093c9041(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49fcb463e1b0993fbe3f14f4c83b5aaf2d7df9133c1ab81663c61deb253d4e31(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d6772179f5c1fabd99f58cbea49ded94499d31416518a02eb863f6ee637476(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54896e1e9f3bfc82697b709e1b9a0ff628771c8629f0b675fd73d2922ae78f78(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70fbab9c6f08d8155eb21fd3f032cc519c3b189c6e8fc6f1538f947486c27ae5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f064449daebdd56116e7ae8f05437b22e235d31fed5df91af54fac8cf57584(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f91700aba15219c4f1bbc556e377633b4a649dbbb8407382a4992f215ced69e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d2fb1ebe02f044414605cb03da58f20f78839a6461b40c908b6ebe0affdc381(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19d16b8dd1c124966d12c1dae51287669d9a65c697c8032580b0c084025d1e97(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0aecf3b5987c15346821d0e04f99365d76cd485ec47bf6142730dfe0ca9da0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__801deadad61e26b6e115bfd915cdc95cbb50b79391824f42de599f8513bd2faa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b1a536720055250a6c0d277303240e4c40d34655d16c329857c0181a095820(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be17fd058a0353a8216e9d840411aa6246fa3762369ac7003e066949b7d4019(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da56533c35403379cc486ca51558b7465c7715143e7439b1f43894cfe434c733(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb8ebbf5a8002e74cab69c6b86c11879bdce11da469fa7277e55269318a3d6b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b46134b12f9e1fce1e34db566aea38b84df83b20de8e3094a6537f60b3321e3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    path: builtins.str,
    allowed_email_domains_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    auto_devops_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    avatar: typing.Optional[builtins.str] = None,
    avatar_hash: typing.Optional[builtins.str] = None,
    default_branch: typing.Optional[builtins.str] = None,
    default_branch_protection: typing.Optional[jsii.Number] = None,
    default_branch_protection_defaults: typing.Optional[typing.Union[GroupDefaultBranchProtectionDefaults, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    emails_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    extra_shared_runners_minutes_limit: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    ip_restriction_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    lfs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    membership_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mentions_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    parent_id: typing.Optional[jsii.Number] = None,
    permanently_remove_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prevent_forking_outside_group: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project_creation_level: typing.Optional[builtins.str] = None,
    push_rules: typing.Optional[typing.Union[GroupPushRules, typing.Dict[builtins.str, typing.Any]]] = None,
    request_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_two_factor_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    shared_runners_minutes_limit: typing.Optional[jsii.Number] = None,
    shared_runners_setting: typing.Optional[builtins.str] = None,
    share_with_group_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subgroup_creation_level: typing.Optional[builtins.str] = None,
    two_factor_grace_period: typing.Optional[jsii.Number] = None,
    visibility_level: typing.Optional[builtins.str] = None,
    wiki_access_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d225d22954028e2cce0967b844f18ecc299c5fe3f1b7539434d706146496f7f(
    *,
    allowed_to_merge: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_to_push: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_force_push: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    developer_can_initial_push: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4b91584f693cb9c2aaec86aeca4318bcf92446a2a20c15d1292ab51afb434df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2342717eb91da11b37a222806d5cb44ab49eb5d4ef369c8f9cc6e2f52195d13c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__988d6ca69dfe7290ccb9996fc3a03395156124ce767036ad934b40b33f3bbbff(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7f3a1e26da2272d693c1783b5ec3b62105ac1292f6b962a0b0694f1939ac3d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39de5fe5b94983695451211edc1493c4ce24b39ddd35bc8f0aeec92ebf26a8e5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78ef82fb8a11b8c1c982cfe3cf885a43b16c3bb0020d0af5bd1ba231a82661ef(
    value: typing.Optional[GroupDefaultBranchProtectionDefaults],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd00b5cb1e872a0d32d959906ae6c3dbaa6f375100d73598898655e44645d38(
    *,
    author_email_regex: typing.Optional[builtins.str] = None,
    branch_name_regex: typing.Optional[builtins.str] = None,
    commit_committer_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    commit_committer_name_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    commit_message_negative_regex: typing.Optional[builtins.str] = None,
    commit_message_regex: typing.Optional[builtins.str] = None,
    deny_delete_tag: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    file_name_regex: typing.Optional[builtins.str] = None,
    max_file_size: typing.Optional[jsii.Number] = None,
    member_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prevent_secrets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reject_non_dco_commits: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reject_unsigned_commits: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec72a20314f89c6f506304165c563f7ff8945813651e6bfa0cc786e6e67f79d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4145809e63529ab82119bcc9c3f3c3a2429b440ee0f1a4de584c6ff74dc55805(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9715749781fc0985da5f1f9c6ab5887e99a61c06f9d405e5be48076cf3037796(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bff69425d2e8b65c8075a1a090065326eec01ce4ee5f24e0582aec8c26ee85e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42162a0123cd4d1597483454bc6bc1c32a433024fcc0b18e4ea602d66484abae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1159c1e36e6a9948be3e8266ab78f971a3eb3ed3c9d17c352771b44d299c1ad9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15699eddbc95845ef6510d849c359c3c7fb0c45e73436d476acbbd417b272f67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a7d0a5e96303a823320c2f43a24af40c4719f5fe15d80f4f724a1e596ad6db1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__351b513d6c9adacfa74884cc48ba83744af5692674453459d11ecc2561f43749(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc740436a0fa2cbfabb0628b4d36beea546b17b3cebdc0f23abf681926581f34(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e530bdc6c90f6f3346e182d4170213ae7bf50a62696c5c2e23fd99123ec5b2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd970191e5909c705851cb62df42b05ef54df7e40afb1a723c1b3729b344e034(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5650e301ff86edb4b8d0af5b0d2d7b16ba673bc64a083bd82029a52fad422e53(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24fcad344ab9bdc0011a46829540ecc1016a3c5f37e01e546c2865cdd34c1046(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12668c20d36c76cc8f295b892202b314e4c83c0c14d9fff7382061dda895449(
    value: typing.Optional[GroupPushRules],
) -> None:
    """Type checking stubs"""
    pass
