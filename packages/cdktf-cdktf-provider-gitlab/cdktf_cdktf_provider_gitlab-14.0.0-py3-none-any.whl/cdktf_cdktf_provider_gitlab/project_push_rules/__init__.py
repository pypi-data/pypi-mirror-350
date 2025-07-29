r'''
# `gitlab_project_push_rules`

Refer to the Terraform Registry for docs: [`gitlab_project_push_rules`](https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules).
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


class ProjectPushRulesA(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.projectPushRules.ProjectPushRulesA",
):
    '''Represents a {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules gitlab_project_push_rules}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        project: builtins.str,
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
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules gitlab_project_push_rules} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param project: The ID or URL-encoded path of the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#project ProjectPushRulesA#project}
        :param author_email_regex: All commit author emails must match this regex, e.g. ``@my-company.com$``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#author_email_regex ProjectPushRulesA#author_email_regex}
        :param branch_name_regex: All branch names must match this regex, e.g. ``(feature|hotfix)\\/*``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#branch_name_regex ProjectPushRulesA#branch_name_regex}
        :param commit_committer_check: Users can only push commits to this repository that were committed with one of their own verified emails. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#commit_committer_check ProjectPushRulesA#commit_committer_check}
        :param commit_committer_name_check: Users can only push commits to this repository if the commit author name is consistent with their GitLab account name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#commit_committer_name_check ProjectPushRulesA#commit_committer_name_check}
        :param commit_message_negative_regex: No commit message is allowed to match this regex, e.g. ``ssh\\:\\/\\/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#commit_message_negative_regex ProjectPushRulesA#commit_message_negative_regex}
        :param commit_message_regex: All commit messages must match this regex, e.g. ``Fixed \\d+\\..*``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#commit_message_regex ProjectPushRulesA#commit_message_regex}
        :param deny_delete_tag: Deny deleting a tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#deny_delete_tag ProjectPushRulesA#deny_delete_tag}
        :param file_name_regex: All committed filenames must not match this regex, e.g. ``(jar|exe)$``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#file_name_regex ProjectPushRulesA#file_name_regex}
        :param max_file_size: Maximum file size (MB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#max_file_size ProjectPushRulesA#max_file_size}
        :param member_check: Restrict commits by author (email) to existing GitLab users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#member_check ProjectPushRulesA#member_check}
        :param prevent_secrets: GitLab will reject any files that are likely to contain secrets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#prevent_secrets ProjectPushRulesA#prevent_secrets}
        :param reject_non_dco_commits: Reject commit when it’s not DCO certified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#reject_non_dco_commits ProjectPushRulesA#reject_non_dco_commits}
        :param reject_unsigned_commits: Reject commit when it’s not signed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#reject_unsigned_commits ProjectPushRulesA#reject_unsigned_commits}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b404524055f8f499856d4f5abb4dcf6764abddaeacace70dd118a216f5b6b185)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ProjectPushRulesAConfig(
            project=project,
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
        '''Generates CDKTF code for importing a ProjectPushRulesA resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ProjectPushRulesA to import.
        :param import_from_id: The id of the existing ProjectPushRulesA that should be imported. Refer to the {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ProjectPushRulesA to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2348f8db3aecec9d0cebb15484c73c984f6dad60c39e12a1478e9d7ae3c6282)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

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
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4ee661423457fd6b2e8b5acd62434e1bf33fc8d66c56180e28faafd4b391c0c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorEmailRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="branchNameRegex")
    def branch_name_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branchNameRegex"))

    @branch_name_regex.setter
    def branch_name_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48c0ae73d7e8072e015b1ff298101a13b3c5f05de2bf06fbfc5a5d983e1e35da)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c9bbfbedcf874d5b0ad8d7ef12f0243bbe30cd49f37b583bb013971f29344a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__325bff64dba93c28f81532318506acfaf16ca4ac7f60a65f1856e8f85752b120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitCommitterNameCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commitMessageNegativeRegex")
    def commit_message_negative_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitMessageNegativeRegex"))

    @commit_message_negative_regex.setter
    def commit_message_negative_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c8e1f3c18fd1344d439d4cb58b2b258b6236e92a1d2f45f867eca72b0739ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitMessageNegativeRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commitMessageRegex")
    def commit_message_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitMessageRegex"))

    @commit_message_regex.setter
    def commit_message_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd75f19538bb1cd15f6f26bebc297d532ecbff86c525832767addf17798becfa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f4f7c21f2e024c28cb93d99f16481e5cd5d456f2c6b62fbc9922cb8185e9ee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "denyDeleteTag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileNameRegex")
    def file_name_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileNameRegex"))

    @file_name_regex.setter
    def file_name_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b4edb05582a96b26d4c403afee5c2b91fe89b2ce2c473ea500964bebc11f21a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileNameRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxFileSize")
    def max_file_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxFileSize"))

    @max_file_size.setter
    def max_file_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89a071431d2f440476cfe5b745720f9e68f650d9a2f67b08ef1f2b475ed6eae6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4713ced05ef607da446f58d043444228a739956eb11a0d3199a9f9de4b670831)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aaa367ad39091fbe724515309216d93a28b8716a1b0ade73121474fb683bc9f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preventSecrets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f889887014638bfeeb079ad71c769b6768c9288ed691ffa82acff913def2e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__47ad4de65f1a1efd0eefd9fada8cbfe01f725f236ea530d662ca25cb346b4087)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0691bbe394b2fe4d6fce492854f8a6fed7d5e37620cd746221d391f07fbb203f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rejectUnsignedCommits", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.projectPushRules.ProjectPushRulesAConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "project": "project",
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
class ProjectPushRulesAConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        project: builtins.str,
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
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param project: The ID or URL-encoded path of the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#project ProjectPushRulesA#project}
        :param author_email_regex: All commit author emails must match this regex, e.g. ``@my-company.com$``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#author_email_regex ProjectPushRulesA#author_email_regex}
        :param branch_name_regex: All branch names must match this regex, e.g. ``(feature|hotfix)\\/*``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#branch_name_regex ProjectPushRulesA#branch_name_regex}
        :param commit_committer_check: Users can only push commits to this repository that were committed with one of their own verified emails. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#commit_committer_check ProjectPushRulesA#commit_committer_check}
        :param commit_committer_name_check: Users can only push commits to this repository if the commit author name is consistent with their GitLab account name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#commit_committer_name_check ProjectPushRulesA#commit_committer_name_check}
        :param commit_message_negative_regex: No commit message is allowed to match this regex, e.g. ``ssh\\:\\/\\/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#commit_message_negative_regex ProjectPushRulesA#commit_message_negative_regex}
        :param commit_message_regex: All commit messages must match this regex, e.g. ``Fixed \\d+\\..*``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#commit_message_regex ProjectPushRulesA#commit_message_regex}
        :param deny_delete_tag: Deny deleting a tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#deny_delete_tag ProjectPushRulesA#deny_delete_tag}
        :param file_name_regex: All committed filenames must not match this regex, e.g. ``(jar|exe)$``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#file_name_regex ProjectPushRulesA#file_name_regex}
        :param max_file_size: Maximum file size (MB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#max_file_size ProjectPushRulesA#max_file_size}
        :param member_check: Restrict commits by author (email) to existing GitLab users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#member_check ProjectPushRulesA#member_check}
        :param prevent_secrets: GitLab will reject any files that are likely to contain secrets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#prevent_secrets ProjectPushRulesA#prevent_secrets}
        :param reject_non_dco_commits: Reject commit when it’s not DCO certified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#reject_non_dco_commits ProjectPushRulesA#reject_non_dco_commits}
        :param reject_unsigned_commits: Reject commit when it’s not signed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#reject_unsigned_commits ProjectPushRulesA#reject_unsigned_commits}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__430a23dec998e6f9367f785c532b7fb349d30bfae98556d66f57505b7f58631b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
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
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
    def project(self) -> builtins.str:
        '''The ID or URL-encoded path of the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#project ProjectPushRulesA#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def author_email_regex(self) -> typing.Optional[builtins.str]:
        '''All commit author emails must match this regex, e.g. ``@my-company.com$``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#author_email_regex ProjectPushRulesA#author_email_regex}
        '''
        result = self._values.get("author_email_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def branch_name_regex(self) -> typing.Optional[builtins.str]:
        '''All branch names must match this regex, e.g. ``(feature|hotfix)\\/*``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#branch_name_regex ProjectPushRulesA#branch_name_regex}
        '''
        result = self._values.get("branch_name_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def commit_committer_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Users can only push commits to this repository that were committed with one of their own verified emails.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#commit_committer_check ProjectPushRulesA#commit_committer_check}
        '''
        result = self._values.get("commit_committer_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def commit_committer_name_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Users can only push commits to this repository if the commit author name is consistent with their GitLab account name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#commit_committer_name_check ProjectPushRulesA#commit_committer_name_check}
        '''
        result = self._values.get("commit_committer_name_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def commit_message_negative_regex(self) -> typing.Optional[builtins.str]:
        '''No commit message is allowed to match this regex, e.g. ``ssh\\:\\/\\/``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#commit_message_negative_regex ProjectPushRulesA#commit_message_negative_regex}
        '''
        result = self._values.get("commit_message_negative_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def commit_message_regex(self) -> typing.Optional[builtins.str]:
        '''All commit messages must match this regex, e.g. ``Fixed \\d+\\..*``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#commit_message_regex ProjectPushRulesA#commit_message_regex}
        '''
        result = self._values.get("commit_message_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deny_delete_tag(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Deny deleting a tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#deny_delete_tag ProjectPushRulesA#deny_delete_tag}
        '''
        result = self._values.get("deny_delete_tag")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def file_name_regex(self) -> typing.Optional[builtins.str]:
        '''All committed filenames must not match this regex, e.g. ``(jar|exe)$``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#file_name_regex ProjectPushRulesA#file_name_regex}
        '''
        result = self._values.get("file_name_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_file_size(self) -> typing.Optional[jsii.Number]:
        '''Maximum file size (MB).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#max_file_size ProjectPushRulesA#max_file_size}
        '''
        result = self._values.get("max_file_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def member_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Restrict commits by author (email) to existing GitLab users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#member_check ProjectPushRulesA#member_check}
        '''
        result = self._values.get("member_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prevent_secrets(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''GitLab will reject any files that are likely to contain secrets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#prevent_secrets ProjectPushRulesA#prevent_secrets}
        '''
        result = self._values.get("prevent_secrets")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reject_non_dco_commits(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Reject commit when it’s not DCO certified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#reject_non_dco_commits ProjectPushRulesA#reject_non_dco_commits}
        '''
        result = self._values.get("reject_non_dco_commits")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reject_unsigned_commits(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Reject commit when it’s not signed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_push_rules#reject_unsigned_commits ProjectPushRulesA#reject_unsigned_commits}
        '''
        result = self._values.get("reject_unsigned_commits")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectPushRulesAConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ProjectPushRulesA",
    "ProjectPushRulesAConfig",
]

publication.publish()

def _typecheckingstub__b404524055f8f499856d4f5abb4dcf6764abddaeacace70dd118a216f5b6b185(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    project: builtins.str,
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

def _typecheckingstub__f2348f8db3aecec9d0cebb15484c73c984f6dad60c39e12a1478e9d7ae3c6282(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee661423457fd6b2e8b5acd62434e1bf33fc8d66c56180e28faafd4b391c0c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c0ae73d7e8072e015b1ff298101a13b3c5f05de2bf06fbfc5a5d983e1e35da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9bbfbedcf874d5b0ad8d7ef12f0243bbe30cd49f37b583bb013971f29344a6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325bff64dba93c28f81532318506acfaf16ca4ac7f60a65f1856e8f85752b120(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c8e1f3c18fd1344d439d4cb58b2b258b6236e92a1d2f45f867eca72b0739ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd75f19538bb1cd15f6f26bebc297d532ecbff86c525832767addf17798becfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4f7c21f2e024c28cb93d99f16481e5cd5d456f2c6b62fbc9922cb8185e9ee4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4edb05582a96b26d4c403afee5c2b91fe89b2ce2c473ea500964bebc11f21a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a071431d2f440476cfe5b745720f9e68f650d9a2f67b08ef1f2b475ed6eae6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4713ced05ef607da446f58d043444228a739956eb11a0d3199a9f9de4b670831(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaa367ad39091fbe724515309216d93a28b8716a1b0ade73121474fb683bc9f9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f889887014638bfeeb079ad71c769b6768c9288ed691ffa82acff913def2e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ad4de65f1a1efd0eefd9fada8cbfe01f725f236ea530d662ca25cb346b4087(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0691bbe394b2fe4d6fce492854f8a6fed7d5e37620cd746221d391f07fbb203f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__430a23dec998e6f9367f785c532b7fb349d30bfae98556d66f57505b7f58631b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: builtins.str,
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
