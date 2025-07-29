r'''
# `gitlab_service_jira`

Refer to the Terraform Registry for docs: [`gitlab_service_jira`](https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira).
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


class ServiceJira(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.serviceJira.ServiceJira",
):
    '''Represents a {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira gitlab_service_jira}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        password: builtins.str,
        project: builtins.str,
        url: builtins.str,
        api_url: typing.Optional[builtins.str] = None,
        comment_on_event_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        commit_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        issues_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jira_auth_type: typing.Optional[jsii.Number] = None,
        jira_issue_prefix: typing.Optional[builtins.str] = None,
        jira_issue_regex: typing.Optional[builtins.str] = None,
        jira_issue_transition_automatic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jira_issue_transition_id: typing.Optional[builtins.str] = None,
        merge_requests_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project_key: typing.Optional[builtins.str] = None,
        project_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        use_inherited_settings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        username: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira gitlab_service_jira} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param password: The Jira API token, password, or personal access token to be used with Jira. When your authentication method is basic (jira_auth_type is 0), use an API token for Jira Cloud or a password for Jira Data Center or Jira Server. When your authentication method is a Jira personal access token (jira_auth_type is 1), use the personal access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#password ServiceJira#password}
        :param project: ID of the project you want to activate integration on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#project ServiceJira#project}
        :param url: The URL to the JIRA project which is being linked to this GitLab project. For example, https://jira.example.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#url ServiceJira#url}
        :param api_url: The base URL to the Jira instance API. Web URL value is used if not set. For example, https://jira-api.example.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#api_url ServiceJira#api_url}
        :param comment_on_event_enabled: Enable comments inside Jira issues on each GitLab event (commit / merge request). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#comment_on_event_enabled ServiceJira#comment_on_event_enabled}
        :param commit_events: Enable notifications for commit events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#commit_events ServiceJira#commit_events}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#id ServiceJira#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issues_enabled: Enable viewing Jira issues in GitLab. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#issues_enabled ServiceJira#issues_enabled}
        :param jira_auth_type: The authentication method to be used with Jira. 0 means Basic Authentication. 1 means Jira personal access token. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#jira_auth_type ServiceJira#jira_auth_type}
        :param jira_issue_prefix: Prefix to match Jira issue keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#jira_issue_prefix ServiceJira#jira_issue_prefix}
        :param jira_issue_regex: Regular expression to match Jira issue keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#jira_issue_regex ServiceJira#jira_issue_regex}
        :param jira_issue_transition_automatic: Enable automatic issue transitions. Takes precedence over jira_issue_transition_id if enabled. Defaults to false. This value cannot be imported, and will not perform drift detection if changed outside Terraform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#jira_issue_transition_automatic ServiceJira#jira_issue_transition_automatic}
        :param jira_issue_transition_id: The ID of a transition that moves issues to a closed state. You can find this number under the JIRA workflow administration (Administration > Issues > Workflows) by selecting View under Operations of the desired workflow of your project. By default, this ID is set to 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#jira_issue_transition_id ServiceJira#jira_issue_transition_id}
        :param merge_requests_events: Enable notifications for merge request events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#merge_requests_events ServiceJira#merge_requests_events}
        :param project_key: The short identifier for your JIRA project. Must be all uppercase. For example, ``PROJ``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#project_key ServiceJira#project_key}
        :param project_keys: Keys of Jira projects. When issues_enabled is true, this setting specifies which Jira projects to view issues from in GitLab. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#project_keys ServiceJira#project_keys}
        :param use_inherited_settings: Indicates whether or not to inherit default settings. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#use_inherited_settings ServiceJira#use_inherited_settings}
        :param username: The email or username to be used with Jira. For Jira Cloud use an email, for Jira Data Center and Jira Server use a username. Required when using Basic authentication (jira_auth_type is 0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#username ServiceJira#username}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86aa6319e4e2ba83a10c1a2d0e6ce7b4ca5b29fd14dcd3d12774a410fb23a7db)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ServiceJiraConfig(
            password=password,
            project=project,
            url=url,
            api_url=api_url,
            comment_on_event_enabled=comment_on_event_enabled,
            commit_events=commit_events,
            id=id,
            issues_enabled=issues_enabled,
            jira_auth_type=jira_auth_type,
            jira_issue_prefix=jira_issue_prefix,
            jira_issue_regex=jira_issue_regex,
            jira_issue_transition_automatic=jira_issue_transition_automatic,
            jira_issue_transition_id=jira_issue_transition_id,
            merge_requests_events=merge_requests_events,
            project_key=project_key,
            project_keys=project_keys,
            use_inherited_settings=use_inherited_settings,
            username=username,
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
        '''Generates CDKTF code for importing a ServiceJira resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ServiceJira to import.
        :param import_from_id: The id of the existing ServiceJira that should be imported. Refer to the {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ServiceJira to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d59214d9ef9bf36e0ac043b758e2a606ab0fe3d3d891fbaa71932da3f33c3aeb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetApiUrl")
    def reset_api_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiUrl", []))

    @jsii.member(jsii_name="resetCommentOnEventEnabled")
    def reset_comment_on_event_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommentOnEventEnabled", []))

    @jsii.member(jsii_name="resetCommitEvents")
    def reset_commit_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitEvents", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIssuesEnabled")
    def reset_issues_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuesEnabled", []))

    @jsii.member(jsii_name="resetJiraAuthType")
    def reset_jira_auth_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJiraAuthType", []))

    @jsii.member(jsii_name="resetJiraIssuePrefix")
    def reset_jira_issue_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJiraIssuePrefix", []))

    @jsii.member(jsii_name="resetJiraIssueRegex")
    def reset_jira_issue_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJiraIssueRegex", []))

    @jsii.member(jsii_name="resetJiraIssueTransitionAutomatic")
    def reset_jira_issue_transition_automatic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJiraIssueTransitionAutomatic", []))

    @jsii.member(jsii_name="resetJiraIssueTransitionId")
    def reset_jira_issue_transition_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJiraIssueTransitionId", []))

    @jsii.member(jsii_name="resetMergeRequestsEvents")
    def reset_merge_requests_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergeRequestsEvents", []))

    @jsii.member(jsii_name="resetProjectKey")
    def reset_project_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectKey", []))

    @jsii.member(jsii_name="resetProjectKeys")
    def reset_project_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectKeys", []))

    @jsii.member(jsii_name="resetUseInheritedSettings")
    def reset_use_inherited_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseInheritedSettings", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

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
    @jsii.member(jsii_name="active")
    def active(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "active"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="apiUrlInput")
    def api_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="commentOnEventEnabledInput")
    def comment_on_event_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "commentOnEventEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="commitEventsInput")
    def commit_events_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "commitEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="issuesEnabledInput")
    def issues_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "issuesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="jiraAuthTypeInput")
    def jira_auth_type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "jiraAuthTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="jiraIssuePrefixInput")
    def jira_issue_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jiraIssuePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="jiraIssueRegexInput")
    def jira_issue_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jiraIssueRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="jiraIssueTransitionAutomaticInput")
    def jira_issue_transition_automatic_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "jiraIssueTransitionAutomaticInput"))

    @builtins.property
    @jsii.member(jsii_name="jiraIssueTransitionIdInput")
    def jira_issue_transition_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jiraIssueTransitionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="mergeRequestsEventsInput")
    def merge_requests_events_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mergeRequestsEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="projectKeyInput")
    def project_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="projectKeysInput")
    def project_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "projectKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="useInheritedSettingsInput")
    def use_inherited_settings_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useInheritedSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="apiUrl")
    def api_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiUrl"))

    @api_url.setter
    def api_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3df5da237ad58254784f7d0b9fe7e47b5c309261ca1fe943f7f1226d80acfbee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commentOnEventEnabled")
    def comment_on_event_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "commentOnEventEnabled"))

    @comment_on_event_enabled.setter
    def comment_on_event_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30df50b39e929792d68bf4274141458bc6cf3f97178c0eca5baf7b4aa919b5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commentOnEventEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commitEvents")
    def commit_events(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "commitEvents"))

    @commit_events.setter
    def commit_events(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b50a799744161ce615ed9752e4293cc21fafd52c2edd63ccc4e3760f8b6777e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0f41fda6394e0a35951c6ce8c4852d0a793359c55f5e5ce6904c0c5b9569169)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuesEnabled")
    def issues_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "issuesEnabled"))

    @issues_enabled.setter
    def issues_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d914db814580e57932345d3fc9b7f4ab4ccc3d35e67ac3685f5a176bf4af501c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jiraAuthType")
    def jira_auth_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "jiraAuthType"))

    @jira_auth_type.setter
    def jira_auth_type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa24a10bbf88f0d90c922c1299539a45d8a49b430f491a5c7d7d2d55ffc7e96d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jiraAuthType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jiraIssuePrefix")
    def jira_issue_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jiraIssuePrefix"))

    @jira_issue_prefix.setter
    def jira_issue_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48443948e6bd7484959fff49c35fd87eca9c18986f91aa42aeea9e818cfcc314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jiraIssuePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jiraIssueRegex")
    def jira_issue_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jiraIssueRegex"))

    @jira_issue_regex.setter
    def jira_issue_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d32ebcf7fc98c5e302a10fd86473445ac9fbe4305035f719589d925503e234b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jiraIssueRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jiraIssueTransitionAutomatic")
    def jira_issue_transition_automatic(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "jiraIssueTransitionAutomatic"))

    @jira_issue_transition_automatic.setter
    def jira_issue_transition_automatic(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eedb85e515603340baeb785cacbebfab59d7dd13becc389f307e8bd087eaff6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jiraIssueTransitionAutomatic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jiraIssueTransitionId")
    def jira_issue_transition_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jiraIssueTransitionId"))

    @jira_issue_transition_id.setter
    def jira_issue_transition_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98ad7d744d3cd7278ee2fc1146f60b1706b85120620ff49867cc6279b594ca75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jiraIssueTransitionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mergeRequestsEvents")
    def merge_requests_events(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mergeRequestsEvents"))

    @merge_requests_events.setter
    def merge_requests_events(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__564575ec8b91a860799ecffb6d56bb2dd951d783fbaba4e616c01bb90ac801f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mergeRequestsEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7e96faf3ab6fbc714477ccdf4bfe16af7a39dc44c0b3259f1b364a5a3e1e835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5a11b263ec1299d8e0875ade65209bdb76f5243ec50316c948f0a749c53c822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectKey")
    def project_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectKey"))

    @project_key.setter
    def project_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__381a8d552b32fe27d8adcc5e404ab33efaabba1ad09105c4a5b035091819a053)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectKeys")
    def project_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "projectKeys"))

    @project_keys.setter
    def project_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c13282c25c1c233dccb9cd00c713e224bc1762b77356fac13711bb74b024f662)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f2d9e14960bb5c0c7c9bd8c48444eedb51d3fc798d96116bbdcb9ef448a9621)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useInheritedSettings")
    def use_inherited_settings(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useInheritedSettings"))

    @use_inherited_settings.setter
    def use_inherited_settings(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__198d659cdc4068a76333bc24ab97d934bb1e089f9462c243c9162040b2648720)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useInheritedSettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0757c7ea8c28108bd39e69ddd10e4829f475461fd38e46f23ffcc6a0f30f201a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.serviceJira.ServiceJiraConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "password": "password",
        "project": "project",
        "url": "url",
        "api_url": "apiUrl",
        "comment_on_event_enabled": "commentOnEventEnabled",
        "commit_events": "commitEvents",
        "id": "id",
        "issues_enabled": "issuesEnabled",
        "jira_auth_type": "jiraAuthType",
        "jira_issue_prefix": "jiraIssuePrefix",
        "jira_issue_regex": "jiraIssueRegex",
        "jira_issue_transition_automatic": "jiraIssueTransitionAutomatic",
        "jira_issue_transition_id": "jiraIssueTransitionId",
        "merge_requests_events": "mergeRequestsEvents",
        "project_key": "projectKey",
        "project_keys": "projectKeys",
        "use_inherited_settings": "useInheritedSettings",
        "username": "username",
    },
)
class ServiceJiraConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        password: builtins.str,
        project: builtins.str,
        url: builtins.str,
        api_url: typing.Optional[builtins.str] = None,
        comment_on_event_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        commit_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        issues_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jira_auth_type: typing.Optional[jsii.Number] = None,
        jira_issue_prefix: typing.Optional[builtins.str] = None,
        jira_issue_regex: typing.Optional[builtins.str] = None,
        jira_issue_transition_automatic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jira_issue_transition_id: typing.Optional[builtins.str] = None,
        merge_requests_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project_key: typing.Optional[builtins.str] = None,
        project_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        use_inherited_settings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param password: The Jira API token, password, or personal access token to be used with Jira. When your authentication method is basic (jira_auth_type is 0), use an API token for Jira Cloud or a password for Jira Data Center or Jira Server. When your authentication method is a Jira personal access token (jira_auth_type is 1), use the personal access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#password ServiceJira#password}
        :param project: ID of the project you want to activate integration on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#project ServiceJira#project}
        :param url: The URL to the JIRA project which is being linked to this GitLab project. For example, https://jira.example.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#url ServiceJira#url}
        :param api_url: The base URL to the Jira instance API. Web URL value is used if not set. For example, https://jira-api.example.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#api_url ServiceJira#api_url}
        :param comment_on_event_enabled: Enable comments inside Jira issues on each GitLab event (commit / merge request). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#comment_on_event_enabled ServiceJira#comment_on_event_enabled}
        :param commit_events: Enable notifications for commit events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#commit_events ServiceJira#commit_events}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#id ServiceJira#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issues_enabled: Enable viewing Jira issues in GitLab. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#issues_enabled ServiceJira#issues_enabled}
        :param jira_auth_type: The authentication method to be used with Jira. 0 means Basic Authentication. 1 means Jira personal access token. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#jira_auth_type ServiceJira#jira_auth_type}
        :param jira_issue_prefix: Prefix to match Jira issue keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#jira_issue_prefix ServiceJira#jira_issue_prefix}
        :param jira_issue_regex: Regular expression to match Jira issue keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#jira_issue_regex ServiceJira#jira_issue_regex}
        :param jira_issue_transition_automatic: Enable automatic issue transitions. Takes precedence over jira_issue_transition_id if enabled. Defaults to false. This value cannot be imported, and will not perform drift detection if changed outside Terraform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#jira_issue_transition_automatic ServiceJira#jira_issue_transition_automatic}
        :param jira_issue_transition_id: The ID of a transition that moves issues to a closed state. You can find this number under the JIRA workflow administration (Administration > Issues > Workflows) by selecting View under Operations of the desired workflow of your project. By default, this ID is set to 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#jira_issue_transition_id ServiceJira#jira_issue_transition_id}
        :param merge_requests_events: Enable notifications for merge request events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#merge_requests_events ServiceJira#merge_requests_events}
        :param project_key: The short identifier for your JIRA project. Must be all uppercase. For example, ``PROJ``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#project_key ServiceJira#project_key}
        :param project_keys: Keys of Jira projects. When issues_enabled is true, this setting specifies which Jira projects to view issues from in GitLab. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#project_keys ServiceJira#project_keys}
        :param use_inherited_settings: Indicates whether or not to inherit default settings. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#use_inherited_settings ServiceJira#use_inherited_settings}
        :param username: The email or username to be used with Jira. For Jira Cloud use an email, for Jira Data Center and Jira Server use a username. Required when using Basic authentication (jira_auth_type is 0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#username ServiceJira#username}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b126cddc07e63985584ed9325c10c57833061e6962b3ece3124c2ba5a0c2d10f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument api_url", value=api_url, expected_type=type_hints["api_url"])
            check_type(argname="argument comment_on_event_enabled", value=comment_on_event_enabled, expected_type=type_hints["comment_on_event_enabled"])
            check_type(argname="argument commit_events", value=commit_events, expected_type=type_hints["commit_events"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument issues_enabled", value=issues_enabled, expected_type=type_hints["issues_enabled"])
            check_type(argname="argument jira_auth_type", value=jira_auth_type, expected_type=type_hints["jira_auth_type"])
            check_type(argname="argument jira_issue_prefix", value=jira_issue_prefix, expected_type=type_hints["jira_issue_prefix"])
            check_type(argname="argument jira_issue_regex", value=jira_issue_regex, expected_type=type_hints["jira_issue_regex"])
            check_type(argname="argument jira_issue_transition_automatic", value=jira_issue_transition_automatic, expected_type=type_hints["jira_issue_transition_automatic"])
            check_type(argname="argument jira_issue_transition_id", value=jira_issue_transition_id, expected_type=type_hints["jira_issue_transition_id"])
            check_type(argname="argument merge_requests_events", value=merge_requests_events, expected_type=type_hints["merge_requests_events"])
            check_type(argname="argument project_key", value=project_key, expected_type=type_hints["project_key"])
            check_type(argname="argument project_keys", value=project_keys, expected_type=type_hints["project_keys"])
            check_type(argname="argument use_inherited_settings", value=use_inherited_settings, expected_type=type_hints["use_inherited_settings"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "project": project,
            "url": url,
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
        if api_url is not None:
            self._values["api_url"] = api_url
        if comment_on_event_enabled is not None:
            self._values["comment_on_event_enabled"] = comment_on_event_enabled
        if commit_events is not None:
            self._values["commit_events"] = commit_events
        if id is not None:
            self._values["id"] = id
        if issues_enabled is not None:
            self._values["issues_enabled"] = issues_enabled
        if jira_auth_type is not None:
            self._values["jira_auth_type"] = jira_auth_type
        if jira_issue_prefix is not None:
            self._values["jira_issue_prefix"] = jira_issue_prefix
        if jira_issue_regex is not None:
            self._values["jira_issue_regex"] = jira_issue_regex
        if jira_issue_transition_automatic is not None:
            self._values["jira_issue_transition_automatic"] = jira_issue_transition_automatic
        if jira_issue_transition_id is not None:
            self._values["jira_issue_transition_id"] = jira_issue_transition_id
        if merge_requests_events is not None:
            self._values["merge_requests_events"] = merge_requests_events
        if project_key is not None:
            self._values["project_key"] = project_key
        if project_keys is not None:
            self._values["project_keys"] = project_keys
        if use_inherited_settings is not None:
            self._values["use_inherited_settings"] = use_inherited_settings
        if username is not None:
            self._values["username"] = username

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
    def password(self) -> builtins.str:
        '''The Jira API token, password, or personal access token to be used with Jira.

        When your authentication method is basic (jira_auth_type is 0), use an API token for Jira Cloud or a password for Jira Data Center or Jira Server. When your authentication method is a Jira personal access token (jira_auth_type is 1), use the personal access token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#password ServiceJira#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''ID of the project you want to activate integration on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#project ServiceJira#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''The URL to the JIRA project which is being linked to this GitLab project. For example, https://jira.example.com.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#url ServiceJira#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_url(self) -> typing.Optional[builtins.str]:
        '''The base URL to the Jira instance API. Web URL value is used if not set. For example, https://jira-api.example.com.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#api_url ServiceJira#api_url}
        '''
        result = self._values.get("api_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment_on_event_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable comments inside Jira issues on each GitLab event (commit / merge request).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#comment_on_event_enabled ServiceJira#comment_on_event_enabled}
        '''
        result = self._values.get("comment_on_event_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def commit_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for commit events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#commit_events ServiceJira#commit_events}
        '''
        result = self._values.get("commit_events")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#id ServiceJira#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issues_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable viewing Jira issues in GitLab.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#issues_enabled ServiceJira#issues_enabled}
        '''
        result = self._values.get("issues_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def jira_auth_type(self) -> typing.Optional[jsii.Number]:
        '''The authentication method to be used with Jira.

        0 means Basic Authentication. 1 means Jira personal access token. Defaults to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#jira_auth_type ServiceJira#jira_auth_type}
        '''
        result = self._values.get("jira_auth_type")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def jira_issue_prefix(self) -> typing.Optional[builtins.str]:
        '''Prefix to match Jira issue keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#jira_issue_prefix ServiceJira#jira_issue_prefix}
        '''
        result = self._values.get("jira_issue_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jira_issue_regex(self) -> typing.Optional[builtins.str]:
        '''Regular expression to match Jira issue keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#jira_issue_regex ServiceJira#jira_issue_regex}
        '''
        result = self._values.get("jira_issue_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jira_issue_transition_automatic(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable automatic issue transitions.

        Takes precedence over jira_issue_transition_id if enabled. Defaults to false. This value cannot be imported, and will not perform drift detection if changed outside Terraform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#jira_issue_transition_automatic ServiceJira#jira_issue_transition_automatic}
        '''
        result = self._values.get("jira_issue_transition_automatic")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def jira_issue_transition_id(self) -> typing.Optional[builtins.str]:
        '''The ID of a transition that moves issues to a closed state.

        You can find this number under the JIRA workflow administration (Administration > Issues > Workflows) by selecting View under Operations of the desired workflow of your project. By default, this ID is set to 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#jira_issue_transition_id ServiceJira#jira_issue_transition_id}
        '''
        result = self._values.get("jira_issue_transition_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def merge_requests_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for merge request events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#merge_requests_events ServiceJira#merge_requests_events}
        '''
        result = self._values.get("merge_requests_events")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project_key(self) -> typing.Optional[builtins.str]:
        '''The short identifier for your JIRA project. Must be all uppercase. For example, ``PROJ``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#project_key ServiceJira#project_key}
        '''
        result = self._values.get("project_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Keys of Jira projects.

        When issues_enabled is true, this setting specifies which Jira projects to view issues from in GitLab.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#project_keys ServiceJira#project_keys}
        '''
        result = self._values.get("project_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def use_inherited_settings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether or not to inherit default settings. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#use_inherited_settings ServiceJira#use_inherited_settings}
        '''
        result = self._values.get("use_inherited_settings")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The email or username to be used with Jira.

        For Jira Cloud use an email, for Jira Data Center and Jira Server use a username. Required when using Basic authentication (jira_auth_type is 0).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/service_jira#username ServiceJira#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceJiraConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ServiceJira",
    "ServiceJiraConfig",
]

publication.publish()

def _typecheckingstub__86aa6319e4e2ba83a10c1a2d0e6ce7b4ca5b29fd14dcd3d12774a410fb23a7db(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    password: builtins.str,
    project: builtins.str,
    url: builtins.str,
    api_url: typing.Optional[builtins.str] = None,
    comment_on_event_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    commit_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    issues_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jira_auth_type: typing.Optional[jsii.Number] = None,
    jira_issue_prefix: typing.Optional[builtins.str] = None,
    jira_issue_regex: typing.Optional[builtins.str] = None,
    jira_issue_transition_automatic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jira_issue_transition_id: typing.Optional[builtins.str] = None,
    merge_requests_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project_key: typing.Optional[builtins.str] = None,
    project_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    use_inherited_settings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    username: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__d59214d9ef9bf36e0ac043b758e2a606ab0fe3d3d891fbaa71932da3f33c3aeb(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3df5da237ad58254784f7d0b9fe7e47b5c309261ca1fe943f7f1226d80acfbee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30df50b39e929792d68bf4274141458bc6cf3f97178c0eca5baf7b4aa919b5b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50a799744161ce615ed9752e4293cc21fafd52c2edd63ccc4e3760f8b6777e6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f41fda6394e0a35951c6ce8c4852d0a793359c55f5e5ce6904c0c5b9569169(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d914db814580e57932345d3fc9b7f4ab4ccc3d35e67ac3685f5a176bf4af501c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa24a10bbf88f0d90c922c1299539a45d8a49b430f491a5c7d7d2d55ffc7e96d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48443948e6bd7484959fff49c35fd87eca9c18986f91aa42aeea9e818cfcc314(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d32ebcf7fc98c5e302a10fd86473445ac9fbe4305035f719589d925503e234b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eedb85e515603340baeb785cacbebfab59d7dd13becc389f307e8bd087eaff6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ad7d744d3cd7278ee2fc1146f60b1706b85120620ff49867cc6279b594ca75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__564575ec8b91a860799ecffb6d56bb2dd951d783fbaba4e616c01bb90ac801f7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e96faf3ab6fbc714477ccdf4bfe16af7a39dc44c0b3259f1b364a5a3e1e835(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5a11b263ec1299d8e0875ade65209bdb76f5243ec50316c948f0a749c53c822(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381a8d552b32fe27d8adcc5e404ab33efaabba1ad09105c4a5b035091819a053(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13282c25c1c233dccb9cd00c713e224bc1762b77356fac13711bb74b024f662(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2d9e14960bb5c0c7c9bd8c48444eedb51d3fc798d96116bbdcb9ef448a9621(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198d659cdc4068a76333bc24ab97d934bb1e089f9462c243c9162040b2648720(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0757c7ea8c28108bd39e69ddd10e4829f475461fd38e46f23ffcc6a0f30f201a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b126cddc07e63985584ed9325c10c57833061e6962b3ece3124c2ba5a0c2d10f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    password: builtins.str,
    project: builtins.str,
    url: builtins.str,
    api_url: typing.Optional[builtins.str] = None,
    comment_on_event_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    commit_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    issues_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jira_auth_type: typing.Optional[jsii.Number] = None,
    jira_issue_prefix: typing.Optional[builtins.str] = None,
    jira_issue_regex: typing.Optional[builtins.str] = None,
    jira_issue_transition_automatic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jira_issue_transition_id: typing.Optional[builtins.str] = None,
    merge_requests_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project_key: typing.Optional[builtins.str] = None,
    project_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    use_inherited_settings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
