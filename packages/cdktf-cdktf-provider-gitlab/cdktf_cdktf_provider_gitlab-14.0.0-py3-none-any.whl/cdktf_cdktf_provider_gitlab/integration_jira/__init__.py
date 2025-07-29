r'''
# `gitlab_integration_jira`

Refer to the Terraform Registry for docs: [`gitlab_integration_jira`](https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira).
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


class IntegrationJira(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.integrationJira.IntegrationJira",
):
    '''Represents a {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira gitlab_integration_jira}.'''

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
        '''Create a new {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira gitlab_integration_jira} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param password: The Jira API token, password, or personal access token to be used with Jira. When your authentication method is basic (jira_auth_type is 0), use an API token for Jira Cloud or a password for Jira Data Center or Jira Server. When your authentication method is a Jira personal access token (jira_auth_type is 1), use the personal access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#password IntegrationJira#password}
        :param project: ID of the project you want to activate integration on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#project IntegrationJira#project}
        :param url: The URL to the JIRA project which is being linked to this GitLab project. For example, https://jira.example.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#url IntegrationJira#url}
        :param api_url: The base URL to the Jira instance API. Web URL value is used if not set. For example, https://jira-api.example.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#api_url IntegrationJira#api_url}
        :param comment_on_event_enabled: Enable comments inside Jira issues on each GitLab event (commit / merge request). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#comment_on_event_enabled IntegrationJira#comment_on_event_enabled}
        :param commit_events: Enable notifications for commit events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#commit_events IntegrationJira#commit_events}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#id IntegrationJira#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issues_enabled: Enable viewing Jira issues in GitLab. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#issues_enabled IntegrationJira#issues_enabled}
        :param jira_auth_type: The authentication method to be used with Jira. 0 means Basic Authentication. 1 means Jira personal access token. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#jira_auth_type IntegrationJira#jira_auth_type}
        :param jira_issue_prefix: Prefix to match Jira issue keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#jira_issue_prefix IntegrationJira#jira_issue_prefix}
        :param jira_issue_regex: Regular expression to match Jira issue keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#jira_issue_regex IntegrationJira#jira_issue_regex}
        :param jira_issue_transition_automatic: Enable automatic issue transitions. Takes precedence over jira_issue_transition_id if enabled. Defaults to false. This value cannot be imported, and will not perform drift detection if changed outside Terraform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#jira_issue_transition_automatic IntegrationJira#jira_issue_transition_automatic}
        :param jira_issue_transition_id: The ID of a transition that moves issues to a closed state. You can find this number under the JIRA workflow administration (Administration > Issues > Workflows) by selecting View under Operations of the desired workflow of your project. By default, this ID is set to 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#jira_issue_transition_id IntegrationJira#jira_issue_transition_id}
        :param merge_requests_events: Enable notifications for merge request events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#merge_requests_events IntegrationJira#merge_requests_events}
        :param project_key: The short identifier for your JIRA project. Must be all uppercase. For example, ``PROJ``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#project_key IntegrationJira#project_key}
        :param project_keys: Keys of Jira projects. When issues_enabled is true, this setting specifies which Jira projects to view issues from in GitLab. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#project_keys IntegrationJira#project_keys}
        :param use_inherited_settings: Indicates whether or not to inherit default settings. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#use_inherited_settings IntegrationJira#use_inherited_settings}
        :param username: The email or username to be used with Jira. For Jira Cloud use an email, for Jira Data Center and Jira Server use a username. Required when using Basic authentication (jira_auth_type is 0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#username IntegrationJira#username}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b40bb48260c22641caa5771623c466364542c57f4f6ff2d533d2e31fdaa7fb0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IntegrationJiraConfig(
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
        '''Generates CDKTF code for importing a IntegrationJira resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IntegrationJira to import.
        :param import_from_id: The id of the existing IntegrationJira that should be imported. Refer to the {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IntegrationJira to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__888dc8e1108abdf5d25850d08ff288b7a08002d9b01b4af208eb196b286d3323)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5249f193b152cb230ef9df48f52806d5bcd4ac4a1247548699ba417cf8eec45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be1b78a7c9b70268e06433c068e494b904265b543d1abe2f8e4f97f44da2aab2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f8bcbc985f0343f55ce6fda1f5fcc9ac55653cd3d6044c75ea9c94446368ef4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b1bb5d989560bd1bb72febadc1eed8f61590aec5c40e0781a3f79dee91197d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38c1ba3a99d80a688a78e6fab727b0c5f3861a462283ceb560feaf78b487c270)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jiraAuthType")
    def jira_auth_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "jiraAuthType"))

    @jira_auth_type.setter
    def jira_auth_type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__038e008516cc05cb8a5b717ada2ed10f51ece3ade8aa959854d34fafb2d11db3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jiraAuthType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jiraIssuePrefix")
    def jira_issue_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jiraIssuePrefix"))

    @jira_issue_prefix.setter
    def jira_issue_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a99c795a13db8a8f0e07b17938c43ddd804c127cd5d74b93d129f185d1d192d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jiraIssuePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jiraIssueRegex")
    def jira_issue_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jiraIssueRegex"))

    @jira_issue_regex.setter
    def jira_issue_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae542ba6c30c02b0b59285550baa184381f07efa5997c2faa9cd9898b43f84a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76f93a69d8b9a0fa58b2f2bb47156344d9e3db4eee9ede89b7cf1c0d358e5389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jiraIssueTransitionAutomatic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jiraIssueTransitionId")
    def jira_issue_transition_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jiraIssueTransitionId"))

    @jira_issue_transition_id.setter
    def jira_issue_transition_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d2934bbf8a5bf27830993b1def98c70c84a60aca489ff7ca8755c6615735337)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06db58e89da6c344fccbda994b90bab6051b7e2010630ed218daf504d942fcfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mergeRequestsEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf792b5f1b6947f4e66e349fd8ff3b6ab5286fff20dc0869eae1a6b895428bbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b13fb0d83d4ad314769794e20176e731c4fdc6858862e02cd6f9bd2da3ab8a93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectKey")
    def project_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectKey"))

    @project_key.setter
    def project_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__632dbc735587c0c8334e6edfa48e9762f2f4cf46d88e4f4709db3660bbaafe4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectKeys")
    def project_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "projectKeys"))

    @project_keys.setter
    def project_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b62dbe7847caa0b8c0ec090497d5187620597a8ef19ff36eed18e4cc76027b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a207d10ae43453cb550675e8acb7aa795b884b3b4479a3929ef27bb84c2f5aa1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b78b7d9256dd581c3c56f780c8659f6eebfe7d5d83728daff22174ff19d4e93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useInheritedSettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f82f71009b87be7585ad8d4b9d0c095d19c50fab9d86bed6bdacef10941952db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.integrationJira.IntegrationJiraConfig",
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
class IntegrationJiraConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        :param password: The Jira API token, password, or personal access token to be used with Jira. When your authentication method is basic (jira_auth_type is 0), use an API token for Jira Cloud or a password for Jira Data Center or Jira Server. When your authentication method is a Jira personal access token (jira_auth_type is 1), use the personal access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#password IntegrationJira#password}
        :param project: ID of the project you want to activate integration on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#project IntegrationJira#project}
        :param url: The URL to the JIRA project which is being linked to this GitLab project. For example, https://jira.example.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#url IntegrationJira#url}
        :param api_url: The base URL to the Jira instance API. Web URL value is used if not set. For example, https://jira-api.example.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#api_url IntegrationJira#api_url}
        :param comment_on_event_enabled: Enable comments inside Jira issues on each GitLab event (commit / merge request). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#comment_on_event_enabled IntegrationJira#comment_on_event_enabled}
        :param commit_events: Enable notifications for commit events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#commit_events IntegrationJira#commit_events}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#id IntegrationJira#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issues_enabled: Enable viewing Jira issues in GitLab. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#issues_enabled IntegrationJira#issues_enabled}
        :param jira_auth_type: The authentication method to be used with Jira. 0 means Basic Authentication. 1 means Jira personal access token. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#jira_auth_type IntegrationJira#jira_auth_type}
        :param jira_issue_prefix: Prefix to match Jira issue keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#jira_issue_prefix IntegrationJira#jira_issue_prefix}
        :param jira_issue_regex: Regular expression to match Jira issue keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#jira_issue_regex IntegrationJira#jira_issue_regex}
        :param jira_issue_transition_automatic: Enable automatic issue transitions. Takes precedence over jira_issue_transition_id if enabled. Defaults to false. This value cannot be imported, and will not perform drift detection if changed outside Terraform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#jira_issue_transition_automatic IntegrationJira#jira_issue_transition_automatic}
        :param jira_issue_transition_id: The ID of a transition that moves issues to a closed state. You can find this number under the JIRA workflow administration (Administration > Issues > Workflows) by selecting View under Operations of the desired workflow of your project. By default, this ID is set to 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#jira_issue_transition_id IntegrationJira#jira_issue_transition_id}
        :param merge_requests_events: Enable notifications for merge request events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#merge_requests_events IntegrationJira#merge_requests_events}
        :param project_key: The short identifier for your JIRA project. Must be all uppercase. For example, ``PROJ``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#project_key IntegrationJira#project_key}
        :param project_keys: Keys of Jira projects. When issues_enabled is true, this setting specifies which Jira projects to view issues from in GitLab. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#project_keys IntegrationJira#project_keys}
        :param use_inherited_settings: Indicates whether or not to inherit default settings. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#use_inherited_settings IntegrationJira#use_inherited_settings}
        :param username: The email or username to be used with Jira. For Jira Cloud use an email, for Jira Data Center and Jira Server use a username. Required when using Basic authentication (jira_auth_type is 0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#username IntegrationJira#username}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f148553b43afef0272890fe499ed1b407e664306f303568b60286a0b7acfca7f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#password IntegrationJira#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''ID of the project you want to activate integration on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#project IntegrationJira#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''The URL to the JIRA project which is being linked to this GitLab project. For example, https://jira.example.com.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#url IntegrationJira#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_url(self) -> typing.Optional[builtins.str]:
        '''The base URL to the Jira instance API. Web URL value is used if not set. For example, https://jira-api.example.com.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#api_url IntegrationJira#api_url}
        '''
        result = self._values.get("api_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment_on_event_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable comments inside Jira issues on each GitLab event (commit / merge request).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#comment_on_event_enabled IntegrationJira#comment_on_event_enabled}
        '''
        result = self._values.get("comment_on_event_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def commit_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for commit events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#commit_events IntegrationJira#commit_events}
        '''
        result = self._values.get("commit_events")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#id IntegrationJira#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#issues_enabled IntegrationJira#issues_enabled}
        '''
        result = self._values.get("issues_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def jira_auth_type(self) -> typing.Optional[jsii.Number]:
        '''The authentication method to be used with Jira.

        0 means Basic Authentication. 1 means Jira personal access token. Defaults to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#jira_auth_type IntegrationJira#jira_auth_type}
        '''
        result = self._values.get("jira_auth_type")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def jira_issue_prefix(self) -> typing.Optional[builtins.str]:
        '''Prefix to match Jira issue keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#jira_issue_prefix IntegrationJira#jira_issue_prefix}
        '''
        result = self._values.get("jira_issue_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jira_issue_regex(self) -> typing.Optional[builtins.str]:
        '''Regular expression to match Jira issue keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#jira_issue_regex IntegrationJira#jira_issue_regex}
        '''
        result = self._values.get("jira_issue_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jira_issue_transition_automatic(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable automatic issue transitions.

        Takes precedence over jira_issue_transition_id if enabled. Defaults to false. This value cannot be imported, and will not perform drift detection if changed outside Terraform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#jira_issue_transition_automatic IntegrationJira#jira_issue_transition_automatic}
        '''
        result = self._values.get("jira_issue_transition_automatic")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def jira_issue_transition_id(self) -> typing.Optional[builtins.str]:
        '''The ID of a transition that moves issues to a closed state.

        You can find this number under the JIRA workflow administration (Administration > Issues > Workflows) by selecting View under Operations of the desired workflow of your project. By default, this ID is set to 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#jira_issue_transition_id IntegrationJira#jira_issue_transition_id}
        '''
        result = self._values.get("jira_issue_transition_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def merge_requests_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for merge request events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#merge_requests_events IntegrationJira#merge_requests_events}
        '''
        result = self._values.get("merge_requests_events")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project_key(self) -> typing.Optional[builtins.str]:
        '''The short identifier for your JIRA project. Must be all uppercase. For example, ``PROJ``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#project_key IntegrationJira#project_key}
        '''
        result = self._values.get("project_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Keys of Jira projects.

        When issues_enabled is true, this setting specifies which Jira projects to view issues from in GitLab.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#project_keys IntegrationJira#project_keys}
        '''
        result = self._values.get("project_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def use_inherited_settings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether or not to inherit default settings. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#use_inherited_settings IntegrationJira#use_inherited_settings}
        '''
        result = self._values.get("use_inherited_settings")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The email or username to be used with Jira.

        For Jira Cloud use an email, for Jira Data Center and Jira Server use a username. Required when using Basic authentication (jira_auth_type is 0).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_jira#username IntegrationJira#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationJiraConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IntegrationJira",
    "IntegrationJiraConfig",
]

publication.publish()

def _typecheckingstub__3b40bb48260c22641caa5771623c466364542c57f4f6ff2d533d2e31fdaa7fb0(
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

def _typecheckingstub__888dc8e1108abdf5d25850d08ff288b7a08002d9b01b4af208eb196b286d3323(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5249f193b152cb230ef9df48f52806d5bcd4ac4a1247548699ba417cf8eec45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1b78a7c9b70268e06433c068e494b904265b543d1abe2f8e4f97f44da2aab2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f8bcbc985f0343f55ce6fda1f5fcc9ac55653cd3d6044c75ea9c94446368ef4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1bb5d989560bd1bb72febadc1eed8f61590aec5c40e0781a3f79dee91197d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c1ba3a99d80a688a78e6fab727b0c5f3861a462283ceb560feaf78b487c270(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__038e008516cc05cb8a5b717ada2ed10f51ece3ade8aa959854d34fafb2d11db3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a99c795a13db8a8f0e07b17938c43ddd804c127cd5d74b93d129f185d1d192d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae542ba6c30c02b0b59285550baa184381f07efa5997c2faa9cd9898b43f84a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f93a69d8b9a0fa58b2f2bb47156344d9e3db4eee9ede89b7cf1c0d358e5389(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2934bbf8a5bf27830993b1def98c70c84a60aca489ff7ca8755c6615735337(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06db58e89da6c344fccbda994b90bab6051b7e2010630ed218daf504d942fcfc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf792b5f1b6947f4e66e349fd8ff3b6ab5286fff20dc0869eae1a6b895428bbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b13fb0d83d4ad314769794e20176e731c4fdc6858862e02cd6f9bd2da3ab8a93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__632dbc735587c0c8334e6edfa48e9762f2f4cf46d88e4f4709db3660bbaafe4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b62dbe7847caa0b8c0ec090497d5187620597a8ef19ff36eed18e4cc76027b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a207d10ae43453cb550675e8acb7aa795b884b3b4479a3929ef27bb84c2f5aa1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b78b7d9256dd581c3c56f780c8659f6eebfe7d5d83728daff22174ff19d4e93(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f82f71009b87be7585ad8d4b9d0c095d19c50fab9d86bed6bdacef10941952db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f148553b43afef0272890fe499ed1b407e664306f303568b60286a0b7acfca7f(
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
