r'''
# `gitlab_integration_slack`

Refer to the Terraform Registry for docs: [`gitlab_integration_slack`](https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack).
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


class IntegrationSlack(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.integrationSlack.IntegrationSlack",
):
    '''Represents a {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack gitlab_integration_slack}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        project: builtins.str,
        webhook: builtins.str,
        branches_to_be_notified: typing.Optional[builtins.str] = None,
        confidential_issue_channel: typing.Optional[builtins.str] = None,
        confidential_issues_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        confidential_note_channel: typing.Optional[builtins.str] = None,
        confidential_note_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        issue_channel: typing.Optional[builtins.str] = None,
        issues_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        merge_request_channel: typing.Optional[builtins.str] = None,
        merge_requests_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        note_channel: typing.Optional[builtins.str] = None,
        note_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        notify_only_broken_pipelines: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        notify_only_default_branch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pipeline_channel: typing.Optional[builtins.str] = None,
        pipeline_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        push_channel: typing.Optional[builtins.str] = None,
        push_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tag_push_channel: typing.Optional[builtins.str] = None,
        tag_push_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        username: typing.Optional[builtins.str] = None,
        wiki_page_channel: typing.Optional[builtins.str] = None,
        wiki_page_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack gitlab_integration_slack} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param project: ID of the project you want to activate integration on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#project IntegrationSlack#project}
        :param webhook: Webhook URL (Example, https://hooks.slack.com/services/...). This value cannot be imported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#webhook IntegrationSlack#webhook}
        :param branches_to_be_notified: Branches to send notifications for. Valid options are "all", "default", "protected", and "default_and_protected". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#branches_to_be_notified IntegrationSlack#branches_to_be_notified}
        :param confidential_issue_channel: The name of the channel to receive confidential issue events notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#confidential_issue_channel IntegrationSlack#confidential_issue_channel}
        :param confidential_issues_events: Enable notifications for confidential issues events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#confidential_issues_events IntegrationSlack#confidential_issues_events}
        :param confidential_note_channel: The name of the channel to receive confidential note events notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#confidential_note_channel IntegrationSlack#confidential_note_channel}
        :param confidential_note_events: Enable notifications for confidential note events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#confidential_note_events IntegrationSlack#confidential_note_events}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#id IntegrationSlack#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issue_channel: The name of the channel to receive issue events notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#issue_channel IntegrationSlack#issue_channel}
        :param issues_events: Enable notifications for issues events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#issues_events IntegrationSlack#issues_events}
        :param merge_request_channel: The name of the channel to receive merge request events notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#merge_request_channel IntegrationSlack#merge_request_channel}
        :param merge_requests_events: Enable notifications for merge requests events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#merge_requests_events IntegrationSlack#merge_requests_events}
        :param note_channel: The name of the channel to receive note events notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#note_channel IntegrationSlack#note_channel}
        :param note_events: Enable notifications for note events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#note_events IntegrationSlack#note_events}
        :param notify_only_broken_pipelines: Send notifications for broken pipelines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#notify_only_broken_pipelines IntegrationSlack#notify_only_broken_pipelines}
        :param notify_only_default_branch: This parameter has been replaced with ``branches_to_be_notified``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#notify_only_default_branch IntegrationSlack#notify_only_default_branch}
        :param pipeline_channel: The name of the channel to receive pipeline events notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#pipeline_channel IntegrationSlack#pipeline_channel}
        :param pipeline_events: Enable notifications for pipeline events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#pipeline_events IntegrationSlack#pipeline_events}
        :param push_channel: The name of the channel to receive push events notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#push_channel IntegrationSlack#push_channel}
        :param push_events: Enable notifications for push events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#push_events IntegrationSlack#push_events}
        :param tag_push_channel: The name of the channel to receive tag push events notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#tag_push_channel IntegrationSlack#tag_push_channel}
        :param tag_push_events: Enable notifications for tag push events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#tag_push_events IntegrationSlack#tag_push_events}
        :param username: Username to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#username IntegrationSlack#username}
        :param wiki_page_channel: The name of the channel to receive wiki page events notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#wiki_page_channel IntegrationSlack#wiki_page_channel}
        :param wiki_page_events: Enable notifications for wiki page events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#wiki_page_events IntegrationSlack#wiki_page_events}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1e7c705a745caea5b78b3043d2836bac0021422dbd750e498091686ea745850)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IntegrationSlackConfig(
            project=project,
            webhook=webhook,
            branches_to_be_notified=branches_to_be_notified,
            confidential_issue_channel=confidential_issue_channel,
            confidential_issues_events=confidential_issues_events,
            confidential_note_channel=confidential_note_channel,
            confidential_note_events=confidential_note_events,
            id=id,
            issue_channel=issue_channel,
            issues_events=issues_events,
            merge_request_channel=merge_request_channel,
            merge_requests_events=merge_requests_events,
            note_channel=note_channel,
            note_events=note_events,
            notify_only_broken_pipelines=notify_only_broken_pipelines,
            notify_only_default_branch=notify_only_default_branch,
            pipeline_channel=pipeline_channel,
            pipeline_events=pipeline_events,
            push_channel=push_channel,
            push_events=push_events,
            tag_push_channel=tag_push_channel,
            tag_push_events=tag_push_events,
            username=username,
            wiki_page_channel=wiki_page_channel,
            wiki_page_events=wiki_page_events,
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
        '''Generates CDKTF code for importing a IntegrationSlack resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IntegrationSlack to import.
        :param import_from_id: The id of the existing IntegrationSlack that should be imported. Refer to the {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IntegrationSlack to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6b486f8cca1c4201342d557f108b08169e93f6a15072be4fe94ea8b57e48cda)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetBranchesToBeNotified")
    def reset_branches_to_be_notified(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBranchesToBeNotified", []))

    @jsii.member(jsii_name="resetConfidentialIssueChannel")
    def reset_confidential_issue_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidentialIssueChannel", []))

    @jsii.member(jsii_name="resetConfidentialIssuesEvents")
    def reset_confidential_issues_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidentialIssuesEvents", []))

    @jsii.member(jsii_name="resetConfidentialNoteChannel")
    def reset_confidential_note_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidentialNoteChannel", []))

    @jsii.member(jsii_name="resetConfidentialNoteEvents")
    def reset_confidential_note_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidentialNoteEvents", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIssueChannel")
    def reset_issue_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssueChannel", []))

    @jsii.member(jsii_name="resetIssuesEvents")
    def reset_issues_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuesEvents", []))

    @jsii.member(jsii_name="resetMergeRequestChannel")
    def reset_merge_request_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergeRequestChannel", []))

    @jsii.member(jsii_name="resetMergeRequestsEvents")
    def reset_merge_requests_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergeRequestsEvents", []))

    @jsii.member(jsii_name="resetNoteChannel")
    def reset_note_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoteChannel", []))

    @jsii.member(jsii_name="resetNoteEvents")
    def reset_note_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoteEvents", []))

    @jsii.member(jsii_name="resetNotifyOnlyBrokenPipelines")
    def reset_notify_only_broken_pipelines(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifyOnlyBrokenPipelines", []))

    @jsii.member(jsii_name="resetNotifyOnlyDefaultBranch")
    def reset_notify_only_default_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifyOnlyDefaultBranch", []))

    @jsii.member(jsii_name="resetPipelineChannel")
    def reset_pipeline_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPipelineChannel", []))

    @jsii.member(jsii_name="resetPipelineEvents")
    def reset_pipeline_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPipelineEvents", []))

    @jsii.member(jsii_name="resetPushChannel")
    def reset_push_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPushChannel", []))

    @jsii.member(jsii_name="resetPushEvents")
    def reset_push_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPushEvents", []))

    @jsii.member(jsii_name="resetTagPushChannel")
    def reset_tag_push_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagPushChannel", []))

    @jsii.member(jsii_name="resetTagPushEvents")
    def reset_tag_push_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagPushEvents", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @jsii.member(jsii_name="resetWikiPageChannel")
    def reset_wiki_page_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWikiPageChannel", []))

    @jsii.member(jsii_name="resetWikiPageEvents")
    def reset_wiki_page_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWikiPageEvents", []))

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
    @jsii.member(jsii_name="jobEvents")
    def job_events(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "jobEvents"))

    @builtins.property
    @jsii.member(jsii_name="branchesToBeNotifiedInput")
    def branches_to_be_notified_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchesToBeNotifiedInput"))

    @builtins.property
    @jsii.member(jsii_name="confidentialIssueChannelInput")
    def confidential_issue_channel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "confidentialIssueChannelInput"))

    @builtins.property
    @jsii.member(jsii_name="confidentialIssuesEventsInput")
    def confidential_issues_events_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "confidentialIssuesEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="confidentialNoteChannelInput")
    def confidential_note_channel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "confidentialNoteChannelInput"))

    @builtins.property
    @jsii.member(jsii_name="confidentialNoteEventsInput")
    def confidential_note_events_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "confidentialNoteEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="issueChannelInput")
    def issue_channel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issueChannelInput"))

    @builtins.property
    @jsii.member(jsii_name="issuesEventsInput")
    def issues_events_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "issuesEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="mergeRequestChannelInput")
    def merge_request_channel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mergeRequestChannelInput"))

    @builtins.property
    @jsii.member(jsii_name="mergeRequestsEventsInput")
    def merge_requests_events_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mergeRequestsEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="noteChannelInput")
    def note_channel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "noteChannelInput"))

    @builtins.property
    @jsii.member(jsii_name="noteEventsInput")
    def note_events_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noteEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyOnlyBrokenPipelinesInput")
    def notify_only_broken_pipelines_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "notifyOnlyBrokenPipelinesInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyOnlyDefaultBranchInput")
    def notify_only_default_branch_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "notifyOnlyDefaultBranchInput"))

    @builtins.property
    @jsii.member(jsii_name="pipelineChannelInput")
    def pipeline_channel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pipelineChannelInput"))

    @builtins.property
    @jsii.member(jsii_name="pipelineEventsInput")
    def pipeline_events_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pipelineEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="pushChannelInput")
    def push_channel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pushChannelInput"))

    @builtins.property
    @jsii.member(jsii_name="pushEventsInput")
    def push_events_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pushEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagPushChannelInput")
    def tag_push_channel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagPushChannelInput"))

    @builtins.property
    @jsii.member(jsii_name="tagPushEventsInput")
    def tag_push_events_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tagPushEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookInput")
    def webhook_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webhookInput"))

    @builtins.property
    @jsii.member(jsii_name="wikiPageChannelInput")
    def wiki_page_channel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "wikiPageChannelInput"))

    @builtins.property
    @jsii.member(jsii_name="wikiPageEventsInput")
    def wiki_page_events_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "wikiPageEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="branchesToBeNotified")
    def branches_to_be_notified(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branchesToBeNotified"))

    @branches_to_be_notified.setter
    def branches_to_be_notified(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c224396012ebf8f88dcfcffcaf470afef7c822602faab336549abb0609d52a5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branchesToBeNotified", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="confidentialIssueChannel")
    def confidential_issue_channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "confidentialIssueChannel"))

    @confidential_issue_channel.setter
    def confidential_issue_channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8204c95dc8967e88a9680768eb53f63f657fac87b18c9ed8e8dc1483d022cc2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidentialIssueChannel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="confidentialIssuesEvents")
    def confidential_issues_events(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "confidentialIssuesEvents"))

    @confidential_issues_events.setter
    def confidential_issues_events(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48a760401393932790ee933f829476b8639eb05cb0da45b1c9451bfdd78faa20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidentialIssuesEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="confidentialNoteChannel")
    def confidential_note_channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "confidentialNoteChannel"))

    @confidential_note_channel.setter
    def confidential_note_channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d0ac97749c20e83c6ad48ee30d0261e8cbdab97ada6a3e1e62c17555831a0e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidentialNoteChannel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="confidentialNoteEvents")
    def confidential_note_events(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "confidentialNoteEvents"))

    @confidential_note_events.setter
    def confidential_note_events(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5971e2cca149d1ee765c0fb8e0115b89fc0ea0de43d9cef0da89d344bbb7eee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidentialNoteEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc79b4fc25362cf69f535cfbd4775cb1fa983bf7e433949f189adb6b9e090633)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issueChannel")
    def issue_channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issueChannel"))

    @issue_channel.setter
    def issue_channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc88aa264c4fa215e5f60da897c39dd974259c447d75214586e5d5e04d088b05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issueChannel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuesEvents")
    def issues_events(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "issuesEvents"))

    @issues_events.setter
    def issues_events(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54991c82b4d283a0f9b6f60314dfe73b2ec41a2c26c9eda4f90f5cd1ac711efd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuesEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mergeRequestChannel")
    def merge_request_channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mergeRequestChannel"))

    @merge_request_channel.setter
    def merge_request_channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__301e946acdfb9e6a4b43a742f7a212d6c4eb2ba96d86bb551d8e2ae335e68c9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mergeRequestChannel", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__844a6d1d8a301240448bba16e92b46ba55860d8d22df90dc68d58eb52682439d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mergeRequestsEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noteChannel")
    def note_channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "noteChannel"))

    @note_channel.setter
    def note_channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cac92c4e78a21eca570a32057e17f80837840d12889c61273c38f7bf54f73bbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noteChannel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noteEvents")
    def note_events(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noteEvents"))

    @note_events.setter
    def note_events(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ae65471371d81855a8e48cea3a47105c4a3a22c24a59dbcc7d86867573c75ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noteEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notifyOnlyBrokenPipelines")
    def notify_only_broken_pipelines(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "notifyOnlyBrokenPipelines"))

    @notify_only_broken_pipelines.setter
    def notify_only_broken_pipelines(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6232834c3e2af61aee82eb3b7f339e7aa8efdef60a517e033da4714431e29cac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyOnlyBrokenPipelines", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notifyOnlyDefaultBranch")
    def notify_only_default_branch(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "notifyOnlyDefaultBranch"))

    @notify_only_default_branch.setter
    def notify_only_default_branch(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f21ca0ba0e55c5a7141a5d340089ac8e5b3a00cebb95b724119d460acbff29d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyOnlyDefaultBranch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pipelineChannel")
    def pipeline_channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pipelineChannel"))

    @pipeline_channel.setter
    def pipeline_channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4caea29eb1ccc44409819fe5c7086ab1190468bb86b4fd11c17792297128741a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pipelineChannel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pipelineEvents")
    def pipeline_events(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pipelineEvents"))

    @pipeline_events.setter
    def pipeline_events(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3df093afd61c8362f8e4c5c95d4ce26716c41ab4cfb5c9767f7102c8e045e428)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pipelineEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa41889a0d5938b4922ac040f0c0e71cbf55a76ef21dc8b2e48a83e0a6100891)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pushChannel")
    def push_channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pushChannel"))

    @push_channel.setter
    def push_channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59a9ca5742db41a998e13ded1a6371c60dcb6c2521c645ddabad7dc083d3234f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pushChannel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pushEvents")
    def push_events(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pushEvents"))

    @push_events.setter
    def push_events(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f848d30a38a8e432bdb5027c3a474ca0436bddc56b40cc49fe41942a70d2c42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pushEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagPushChannel")
    def tag_push_channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagPushChannel"))

    @tag_push_channel.setter
    def tag_push_channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5c5c6683344b5e7ee834a0cd18642cb362741fecbd67a80a596c23b392e55e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagPushChannel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagPushEvents")
    def tag_push_events(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tagPushEvents"))

    @tag_push_events.setter
    def tag_push_events(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d6135add8b6022682deed6e793f4ef6e8e53116228c1f2b96b9cf533d25836d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagPushEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__792eef4e77b674f7efeeb67d1476d593e88e8e49f86ec028787e9a5ea95851fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhook")
    def webhook(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhook"))

    @webhook.setter
    def webhook(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af6a4581afd13b729ded92b0e910a31fc97985742d77da366ecdd8499c7eb37a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhook", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wikiPageChannel")
    def wiki_page_channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "wikiPageChannel"))

    @wiki_page_channel.setter
    def wiki_page_channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a89d6f91e9b99c17f976c4690694974bf182ab1c61bd1e86da69ab0b5960fdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wikiPageChannel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wikiPageEvents")
    def wiki_page_events(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "wikiPageEvents"))

    @wiki_page_events.setter
    def wiki_page_events(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9da827b4d57a662160498773881b077eddfdbea32a16ef8e1040190936bd1f7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wikiPageEvents", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.integrationSlack.IntegrationSlackConfig",
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
        "webhook": "webhook",
        "branches_to_be_notified": "branchesToBeNotified",
        "confidential_issue_channel": "confidentialIssueChannel",
        "confidential_issues_events": "confidentialIssuesEvents",
        "confidential_note_channel": "confidentialNoteChannel",
        "confidential_note_events": "confidentialNoteEvents",
        "id": "id",
        "issue_channel": "issueChannel",
        "issues_events": "issuesEvents",
        "merge_request_channel": "mergeRequestChannel",
        "merge_requests_events": "mergeRequestsEvents",
        "note_channel": "noteChannel",
        "note_events": "noteEvents",
        "notify_only_broken_pipelines": "notifyOnlyBrokenPipelines",
        "notify_only_default_branch": "notifyOnlyDefaultBranch",
        "pipeline_channel": "pipelineChannel",
        "pipeline_events": "pipelineEvents",
        "push_channel": "pushChannel",
        "push_events": "pushEvents",
        "tag_push_channel": "tagPushChannel",
        "tag_push_events": "tagPushEvents",
        "username": "username",
        "wiki_page_channel": "wikiPageChannel",
        "wiki_page_events": "wikiPageEvents",
    },
)
class IntegrationSlackConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        webhook: builtins.str,
        branches_to_be_notified: typing.Optional[builtins.str] = None,
        confidential_issue_channel: typing.Optional[builtins.str] = None,
        confidential_issues_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        confidential_note_channel: typing.Optional[builtins.str] = None,
        confidential_note_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        issue_channel: typing.Optional[builtins.str] = None,
        issues_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        merge_request_channel: typing.Optional[builtins.str] = None,
        merge_requests_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        note_channel: typing.Optional[builtins.str] = None,
        note_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        notify_only_broken_pipelines: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        notify_only_default_branch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pipeline_channel: typing.Optional[builtins.str] = None,
        pipeline_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        push_channel: typing.Optional[builtins.str] = None,
        push_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tag_push_channel: typing.Optional[builtins.str] = None,
        tag_push_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        username: typing.Optional[builtins.str] = None,
        wiki_page_channel: typing.Optional[builtins.str] = None,
        wiki_page_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param project: ID of the project you want to activate integration on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#project IntegrationSlack#project}
        :param webhook: Webhook URL (Example, https://hooks.slack.com/services/...). This value cannot be imported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#webhook IntegrationSlack#webhook}
        :param branches_to_be_notified: Branches to send notifications for. Valid options are "all", "default", "protected", and "default_and_protected". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#branches_to_be_notified IntegrationSlack#branches_to_be_notified}
        :param confidential_issue_channel: The name of the channel to receive confidential issue events notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#confidential_issue_channel IntegrationSlack#confidential_issue_channel}
        :param confidential_issues_events: Enable notifications for confidential issues events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#confidential_issues_events IntegrationSlack#confidential_issues_events}
        :param confidential_note_channel: The name of the channel to receive confidential note events notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#confidential_note_channel IntegrationSlack#confidential_note_channel}
        :param confidential_note_events: Enable notifications for confidential note events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#confidential_note_events IntegrationSlack#confidential_note_events}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#id IntegrationSlack#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issue_channel: The name of the channel to receive issue events notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#issue_channel IntegrationSlack#issue_channel}
        :param issues_events: Enable notifications for issues events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#issues_events IntegrationSlack#issues_events}
        :param merge_request_channel: The name of the channel to receive merge request events notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#merge_request_channel IntegrationSlack#merge_request_channel}
        :param merge_requests_events: Enable notifications for merge requests events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#merge_requests_events IntegrationSlack#merge_requests_events}
        :param note_channel: The name of the channel to receive note events notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#note_channel IntegrationSlack#note_channel}
        :param note_events: Enable notifications for note events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#note_events IntegrationSlack#note_events}
        :param notify_only_broken_pipelines: Send notifications for broken pipelines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#notify_only_broken_pipelines IntegrationSlack#notify_only_broken_pipelines}
        :param notify_only_default_branch: This parameter has been replaced with ``branches_to_be_notified``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#notify_only_default_branch IntegrationSlack#notify_only_default_branch}
        :param pipeline_channel: The name of the channel to receive pipeline events notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#pipeline_channel IntegrationSlack#pipeline_channel}
        :param pipeline_events: Enable notifications for pipeline events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#pipeline_events IntegrationSlack#pipeline_events}
        :param push_channel: The name of the channel to receive push events notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#push_channel IntegrationSlack#push_channel}
        :param push_events: Enable notifications for push events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#push_events IntegrationSlack#push_events}
        :param tag_push_channel: The name of the channel to receive tag push events notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#tag_push_channel IntegrationSlack#tag_push_channel}
        :param tag_push_events: Enable notifications for tag push events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#tag_push_events IntegrationSlack#tag_push_events}
        :param username: Username to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#username IntegrationSlack#username}
        :param wiki_page_channel: The name of the channel to receive wiki page events notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#wiki_page_channel IntegrationSlack#wiki_page_channel}
        :param wiki_page_events: Enable notifications for wiki page events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#wiki_page_events IntegrationSlack#wiki_page_events}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__207ed4dc11ec5174beec385436ea9a0f123e6f5ffa30344c9f2a36a2e5acc238)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument webhook", value=webhook, expected_type=type_hints["webhook"])
            check_type(argname="argument branches_to_be_notified", value=branches_to_be_notified, expected_type=type_hints["branches_to_be_notified"])
            check_type(argname="argument confidential_issue_channel", value=confidential_issue_channel, expected_type=type_hints["confidential_issue_channel"])
            check_type(argname="argument confidential_issues_events", value=confidential_issues_events, expected_type=type_hints["confidential_issues_events"])
            check_type(argname="argument confidential_note_channel", value=confidential_note_channel, expected_type=type_hints["confidential_note_channel"])
            check_type(argname="argument confidential_note_events", value=confidential_note_events, expected_type=type_hints["confidential_note_events"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument issue_channel", value=issue_channel, expected_type=type_hints["issue_channel"])
            check_type(argname="argument issues_events", value=issues_events, expected_type=type_hints["issues_events"])
            check_type(argname="argument merge_request_channel", value=merge_request_channel, expected_type=type_hints["merge_request_channel"])
            check_type(argname="argument merge_requests_events", value=merge_requests_events, expected_type=type_hints["merge_requests_events"])
            check_type(argname="argument note_channel", value=note_channel, expected_type=type_hints["note_channel"])
            check_type(argname="argument note_events", value=note_events, expected_type=type_hints["note_events"])
            check_type(argname="argument notify_only_broken_pipelines", value=notify_only_broken_pipelines, expected_type=type_hints["notify_only_broken_pipelines"])
            check_type(argname="argument notify_only_default_branch", value=notify_only_default_branch, expected_type=type_hints["notify_only_default_branch"])
            check_type(argname="argument pipeline_channel", value=pipeline_channel, expected_type=type_hints["pipeline_channel"])
            check_type(argname="argument pipeline_events", value=pipeline_events, expected_type=type_hints["pipeline_events"])
            check_type(argname="argument push_channel", value=push_channel, expected_type=type_hints["push_channel"])
            check_type(argname="argument push_events", value=push_events, expected_type=type_hints["push_events"])
            check_type(argname="argument tag_push_channel", value=tag_push_channel, expected_type=type_hints["tag_push_channel"])
            check_type(argname="argument tag_push_events", value=tag_push_events, expected_type=type_hints["tag_push_events"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument wiki_page_channel", value=wiki_page_channel, expected_type=type_hints["wiki_page_channel"])
            check_type(argname="argument wiki_page_events", value=wiki_page_events, expected_type=type_hints["wiki_page_events"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project": project,
            "webhook": webhook,
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
        if branches_to_be_notified is not None:
            self._values["branches_to_be_notified"] = branches_to_be_notified
        if confidential_issue_channel is not None:
            self._values["confidential_issue_channel"] = confidential_issue_channel
        if confidential_issues_events is not None:
            self._values["confidential_issues_events"] = confidential_issues_events
        if confidential_note_channel is not None:
            self._values["confidential_note_channel"] = confidential_note_channel
        if confidential_note_events is not None:
            self._values["confidential_note_events"] = confidential_note_events
        if id is not None:
            self._values["id"] = id
        if issue_channel is not None:
            self._values["issue_channel"] = issue_channel
        if issues_events is not None:
            self._values["issues_events"] = issues_events
        if merge_request_channel is not None:
            self._values["merge_request_channel"] = merge_request_channel
        if merge_requests_events is not None:
            self._values["merge_requests_events"] = merge_requests_events
        if note_channel is not None:
            self._values["note_channel"] = note_channel
        if note_events is not None:
            self._values["note_events"] = note_events
        if notify_only_broken_pipelines is not None:
            self._values["notify_only_broken_pipelines"] = notify_only_broken_pipelines
        if notify_only_default_branch is not None:
            self._values["notify_only_default_branch"] = notify_only_default_branch
        if pipeline_channel is not None:
            self._values["pipeline_channel"] = pipeline_channel
        if pipeline_events is not None:
            self._values["pipeline_events"] = pipeline_events
        if push_channel is not None:
            self._values["push_channel"] = push_channel
        if push_events is not None:
            self._values["push_events"] = push_events
        if tag_push_channel is not None:
            self._values["tag_push_channel"] = tag_push_channel
        if tag_push_events is not None:
            self._values["tag_push_events"] = tag_push_events
        if username is not None:
            self._values["username"] = username
        if wiki_page_channel is not None:
            self._values["wiki_page_channel"] = wiki_page_channel
        if wiki_page_events is not None:
            self._values["wiki_page_events"] = wiki_page_events

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
        '''ID of the project you want to activate integration on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#project IntegrationSlack#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def webhook(self) -> builtins.str:
        '''Webhook URL (Example, https://hooks.slack.com/services/...). This value cannot be imported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#webhook IntegrationSlack#webhook}
        '''
        result = self._values.get("webhook")
        assert result is not None, "Required property 'webhook' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def branches_to_be_notified(self) -> typing.Optional[builtins.str]:
        '''Branches to send notifications for. Valid options are "all", "default", "protected", and "default_and_protected".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#branches_to_be_notified IntegrationSlack#branches_to_be_notified}
        '''
        result = self._values.get("branches_to_be_notified")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def confidential_issue_channel(self) -> typing.Optional[builtins.str]:
        '''The name of the channel to receive confidential issue events notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#confidential_issue_channel IntegrationSlack#confidential_issue_channel}
        '''
        result = self._values.get("confidential_issue_channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def confidential_issues_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for confidential issues events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#confidential_issues_events IntegrationSlack#confidential_issues_events}
        '''
        result = self._values.get("confidential_issues_events")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def confidential_note_channel(self) -> typing.Optional[builtins.str]:
        '''The name of the channel to receive confidential note events notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#confidential_note_channel IntegrationSlack#confidential_note_channel}
        '''
        result = self._values.get("confidential_note_channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def confidential_note_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for confidential note events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#confidential_note_events IntegrationSlack#confidential_note_events}
        '''
        result = self._values.get("confidential_note_events")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#id IntegrationSlack#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issue_channel(self) -> typing.Optional[builtins.str]:
        '''The name of the channel to receive issue events notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#issue_channel IntegrationSlack#issue_channel}
        '''
        result = self._values.get("issue_channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issues_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for issues events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#issues_events IntegrationSlack#issues_events}
        '''
        result = self._values.get("issues_events")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def merge_request_channel(self) -> typing.Optional[builtins.str]:
        '''The name of the channel to receive merge request events notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#merge_request_channel IntegrationSlack#merge_request_channel}
        '''
        result = self._values.get("merge_request_channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def merge_requests_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for merge requests events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#merge_requests_events IntegrationSlack#merge_requests_events}
        '''
        result = self._values.get("merge_requests_events")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def note_channel(self) -> typing.Optional[builtins.str]:
        '''The name of the channel to receive note events notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#note_channel IntegrationSlack#note_channel}
        '''
        result = self._values.get("note_channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def note_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for note events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#note_events IntegrationSlack#note_events}
        '''
        result = self._values.get("note_events")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def notify_only_broken_pipelines(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Send notifications for broken pipelines.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#notify_only_broken_pipelines IntegrationSlack#notify_only_broken_pipelines}
        '''
        result = self._values.get("notify_only_broken_pipelines")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def notify_only_default_branch(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This parameter has been replaced with ``branches_to_be_notified``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#notify_only_default_branch IntegrationSlack#notify_only_default_branch}
        '''
        result = self._values.get("notify_only_default_branch")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def pipeline_channel(self) -> typing.Optional[builtins.str]:
        '''The name of the channel to receive pipeline events notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#pipeline_channel IntegrationSlack#pipeline_channel}
        '''
        result = self._values.get("pipeline_channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pipeline_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for pipeline events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#pipeline_events IntegrationSlack#pipeline_events}
        '''
        result = self._values.get("pipeline_events")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def push_channel(self) -> typing.Optional[builtins.str]:
        '''The name of the channel to receive push events notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#push_channel IntegrationSlack#push_channel}
        '''
        result = self._values.get("push_channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def push_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for push events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#push_events IntegrationSlack#push_events}
        '''
        result = self._values.get("push_events")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tag_push_channel(self) -> typing.Optional[builtins.str]:
        '''The name of the channel to receive tag push events notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#tag_push_channel IntegrationSlack#tag_push_channel}
        '''
        result = self._values.get("tag_push_channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_push_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for tag push events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#tag_push_events IntegrationSlack#tag_push_events}
        '''
        result = self._values.get("tag_push_events")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#username IntegrationSlack#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wiki_page_channel(self) -> typing.Optional[builtins.str]:
        '''The name of the channel to receive wiki page events notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#wiki_page_channel IntegrationSlack#wiki_page_channel}
        '''
        result = self._values.get("wiki_page_channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wiki_page_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for wiki page events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/integration_slack#wiki_page_events IntegrationSlack#wiki_page_events}
        '''
        result = self._values.get("wiki_page_events")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationSlackConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IntegrationSlack",
    "IntegrationSlackConfig",
]

publication.publish()

def _typecheckingstub__d1e7c705a745caea5b78b3043d2836bac0021422dbd750e498091686ea745850(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    project: builtins.str,
    webhook: builtins.str,
    branches_to_be_notified: typing.Optional[builtins.str] = None,
    confidential_issue_channel: typing.Optional[builtins.str] = None,
    confidential_issues_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    confidential_note_channel: typing.Optional[builtins.str] = None,
    confidential_note_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    issue_channel: typing.Optional[builtins.str] = None,
    issues_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    merge_request_channel: typing.Optional[builtins.str] = None,
    merge_requests_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    note_channel: typing.Optional[builtins.str] = None,
    note_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    notify_only_broken_pipelines: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    notify_only_default_branch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pipeline_channel: typing.Optional[builtins.str] = None,
    pipeline_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    push_channel: typing.Optional[builtins.str] = None,
    push_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tag_push_channel: typing.Optional[builtins.str] = None,
    tag_push_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    username: typing.Optional[builtins.str] = None,
    wiki_page_channel: typing.Optional[builtins.str] = None,
    wiki_page_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__a6b486f8cca1c4201342d557f108b08169e93f6a15072be4fe94ea8b57e48cda(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c224396012ebf8f88dcfcffcaf470afef7c822602faab336549abb0609d52a5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8204c95dc8967e88a9680768eb53f63f657fac87b18c9ed8e8dc1483d022cc2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48a760401393932790ee933f829476b8639eb05cb0da45b1c9451bfdd78faa20(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d0ac97749c20e83c6ad48ee30d0261e8cbdab97ada6a3e1e62c17555831a0e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5971e2cca149d1ee765c0fb8e0115b89fc0ea0de43d9cef0da89d344bbb7eee0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc79b4fc25362cf69f535cfbd4775cb1fa983bf7e433949f189adb6b9e090633(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc88aa264c4fa215e5f60da897c39dd974259c447d75214586e5d5e04d088b05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54991c82b4d283a0f9b6f60314dfe73b2ec41a2c26c9eda4f90f5cd1ac711efd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__301e946acdfb9e6a4b43a742f7a212d6c4eb2ba96d86bb551d8e2ae335e68c9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844a6d1d8a301240448bba16e92b46ba55860d8d22df90dc68d58eb52682439d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cac92c4e78a21eca570a32057e17f80837840d12889c61273c38f7bf54f73bbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae65471371d81855a8e48cea3a47105c4a3a22c24a59dbcc7d86867573c75ef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6232834c3e2af61aee82eb3b7f339e7aa8efdef60a517e033da4714431e29cac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f21ca0ba0e55c5a7141a5d340089ac8e5b3a00cebb95b724119d460acbff29d9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4caea29eb1ccc44409819fe5c7086ab1190468bb86b4fd11c17792297128741a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3df093afd61c8362f8e4c5c95d4ce26716c41ab4cfb5c9767f7102c8e045e428(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa41889a0d5938b4922ac040f0c0e71cbf55a76ef21dc8b2e48a83e0a6100891(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a9ca5742db41a998e13ded1a6371c60dcb6c2521c645ddabad7dc083d3234f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f848d30a38a8e432bdb5027c3a474ca0436bddc56b40cc49fe41942a70d2c42(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c5c6683344b5e7ee834a0cd18642cb362741fecbd67a80a596c23b392e55e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d6135add8b6022682deed6e793f4ef6e8e53116228c1f2b96b9cf533d25836d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__792eef4e77b674f7efeeb67d1476d593e88e8e49f86ec028787e9a5ea95851fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af6a4581afd13b729ded92b0e910a31fc97985742d77da366ecdd8499c7eb37a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a89d6f91e9b99c17f976c4690694974bf182ab1c61bd1e86da69ab0b5960fdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9da827b4d57a662160498773881b077eddfdbea32a16ef8e1040190936bd1f7b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207ed4dc11ec5174beec385436ea9a0f123e6f5ffa30344c9f2a36a2e5acc238(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: builtins.str,
    webhook: builtins.str,
    branches_to_be_notified: typing.Optional[builtins.str] = None,
    confidential_issue_channel: typing.Optional[builtins.str] = None,
    confidential_issues_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    confidential_note_channel: typing.Optional[builtins.str] = None,
    confidential_note_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    issue_channel: typing.Optional[builtins.str] = None,
    issues_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    merge_request_channel: typing.Optional[builtins.str] = None,
    merge_requests_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    note_channel: typing.Optional[builtins.str] = None,
    note_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    notify_only_broken_pipelines: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    notify_only_default_branch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pipeline_channel: typing.Optional[builtins.str] = None,
    pipeline_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    push_channel: typing.Optional[builtins.str] = None,
    push_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tag_push_channel: typing.Optional[builtins.str] = None,
    tag_push_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    username: typing.Optional[builtins.str] = None,
    wiki_page_channel: typing.Optional[builtins.str] = None,
    wiki_page_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
