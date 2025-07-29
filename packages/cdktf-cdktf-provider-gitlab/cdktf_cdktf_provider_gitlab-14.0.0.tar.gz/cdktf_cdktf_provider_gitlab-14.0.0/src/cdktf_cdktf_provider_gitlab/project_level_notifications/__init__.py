r'''
# `gitlab_project_level_notifications`

Refer to the Terraform Registry for docs: [`gitlab_project_level_notifications`](https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications).
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


class ProjectLevelNotifications(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.projectLevelNotifications.ProjectLevelNotifications",
):
    '''Represents a {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications gitlab_project_level_notifications}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        project: builtins.str,
        close_issue: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        close_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        failed_pipeline: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fixed_pipeline: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        issue_due: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        level: typing.Optional[builtins.str] = None,
        merge_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        merge_when_pipeline_succeeds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        moved_project: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        new_issue: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        new_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        new_note: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        push_to_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reassign_issue: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reassign_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reopen_issue: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reopen_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        success_pipeline: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications gitlab_project_level_notifications} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param project: The ID or URL-encoded path of a project where notifications will be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#project ProjectLevelNotifications#project}
        :param close_issue: Enable notifications for closed issues. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#close_issue ProjectLevelNotifications#close_issue}
        :param close_merge_request: Enable notifications for closed merge requests. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#close_merge_request ProjectLevelNotifications#close_merge_request}
        :param failed_pipeline: Enable notifications for failed pipelines. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#failed_pipeline ProjectLevelNotifications#failed_pipeline}
        :param fixed_pipeline: Enable notifications for fixed pipelines. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#fixed_pipeline ProjectLevelNotifications#fixed_pipeline}
        :param issue_due: Enable notifications for due issues. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#issue_due ProjectLevelNotifications#issue_due}
        :param level: The level of the notification. Valid values are: ``disabled``, ``participating``, ``watch``, ``global``, ``mention``, ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#level ProjectLevelNotifications#level}
        :param merge_merge_request: Enable notifications for merged merge requests. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#merge_merge_request ProjectLevelNotifications#merge_merge_request}
        :param merge_when_pipeline_succeeds: Enable notifications for merged merge requests when the pipeline succeeds. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#merge_when_pipeline_succeeds ProjectLevelNotifications#merge_when_pipeline_succeeds}
        :param moved_project: Enable notifications for moved projects. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#moved_project ProjectLevelNotifications#moved_project}
        :param new_issue: Enable notifications for new issues. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#new_issue ProjectLevelNotifications#new_issue}
        :param new_merge_request: Enable notifications for new merge requests. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#new_merge_request ProjectLevelNotifications#new_merge_request}
        :param new_note: Enable notifications for new notes on merge requests. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#new_note ProjectLevelNotifications#new_note}
        :param push_to_merge_request: Enable notifications for push to merge request branches. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#push_to_merge_request ProjectLevelNotifications#push_to_merge_request}
        :param reassign_issue: Enable notifications for issue reassignments. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#reassign_issue ProjectLevelNotifications#reassign_issue}
        :param reassign_merge_request: Enable notifications for merge request reassignments. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#reassign_merge_request ProjectLevelNotifications#reassign_merge_request}
        :param reopen_issue: Enable notifications for reopened issues. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#reopen_issue ProjectLevelNotifications#reopen_issue}
        :param reopen_merge_request: Enable notifications for reopened merge requests. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#reopen_merge_request ProjectLevelNotifications#reopen_merge_request}
        :param success_pipeline: Enable notifications for successful pipelines. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#success_pipeline ProjectLevelNotifications#success_pipeline}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57d3cd3c396fb7cb5e00d36e119da98d6154f9948427ae5fca178ba0da34bdea)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ProjectLevelNotificationsConfig(
            project=project,
            close_issue=close_issue,
            close_merge_request=close_merge_request,
            failed_pipeline=failed_pipeline,
            fixed_pipeline=fixed_pipeline,
            issue_due=issue_due,
            level=level,
            merge_merge_request=merge_merge_request,
            merge_when_pipeline_succeeds=merge_when_pipeline_succeeds,
            moved_project=moved_project,
            new_issue=new_issue,
            new_merge_request=new_merge_request,
            new_note=new_note,
            push_to_merge_request=push_to_merge_request,
            reassign_issue=reassign_issue,
            reassign_merge_request=reassign_merge_request,
            reopen_issue=reopen_issue,
            reopen_merge_request=reopen_merge_request,
            success_pipeline=success_pipeline,
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
        '''Generates CDKTF code for importing a ProjectLevelNotifications resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ProjectLevelNotifications to import.
        :param import_from_id: The id of the existing ProjectLevelNotifications that should be imported. Refer to the {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ProjectLevelNotifications to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97d5183ef71c0202209a57d7bf123c1d1e9f1e8d827632741d2649df6bec0162)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetCloseIssue")
    def reset_close_issue(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloseIssue", []))

    @jsii.member(jsii_name="resetCloseMergeRequest")
    def reset_close_merge_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloseMergeRequest", []))

    @jsii.member(jsii_name="resetFailedPipeline")
    def reset_failed_pipeline(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailedPipeline", []))

    @jsii.member(jsii_name="resetFixedPipeline")
    def reset_fixed_pipeline(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedPipeline", []))

    @jsii.member(jsii_name="resetIssueDue")
    def reset_issue_due(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssueDue", []))

    @jsii.member(jsii_name="resetLevel")
    def reset_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLevel", []))

    @jsii.member(jsii_name="resetMergeMergeRequest")
    def reset_merge_merge_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergeMergeRequest", []))

    @jsii.member(jsii_name="resetMergeWhenPipelineSucceeds")
    def reset_merge_when_pipeline_succeeds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergeWhenPipelineSucceeds", []))

    @jsii.member(jsii_name="resetMovedProject")
    def reset_moved_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMovedProject", []))

    @jsii.member(jsii_name="resetNewIssue")
    def reset_new_issue(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNewIssue", []))

    @jsii.member(jsii_name="resetNewMergeRequest")
    def reset_new_merge_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNewMergeRequest", []))

    @jsii.member(jsii_name="resetNewNote")
    def reset_new_note(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNewNote", []))

    @jsii.member(jsii_name="resetPushToMergeRequest")
    def reset_push_to_merge_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPushToMergeRequest", []))

    @jsii.member(jsii_name="resetReassignIssue")
    def reset_reassign_issue(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReassignIssue", []))

    @jsii.member(jsii_name="resetReassignMergeRequest")
    def reset_reassign_merge_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReassignMergeRequest", []))

    @jsii.member(jsii_name="resetReopenIssue")
    def reset_reopen_issue(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReopenIssue", []))

    @jsii.member(jsii_name="resetReopenMergeRequest")
    def reset_reopen_merge_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReopenMergeRequest", []))

    @jsii.member(jsii_name="resetSuccessPipeline")
    def reset_success_pipeline(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessPipeline", []))

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
    @jsii.member(jsii_name="closeIssueInput")
    def close_issue_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "closeIssueInput"))

    @builtins.property
    @jsii.member(jsii_name="closeMergeRequestInput")
    def close_merge_request_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "closeMergeRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="failedPipelineInput")
    def failed_pipeline_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failedPipelineInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedPipelineInput")
    def fixed_pipeline_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fixedPipelineInput"))

    @builtins.property
    @jsii.member(jsii_name="issueDueInput")
    def issue_due_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "issueDueInput"))

    @builtins.property
    @jsii.member(jsii_name="levelInput")
    def level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "levelInput"))

    @builtins.property
    @jsii.member(jsii_name="mergeMergeRequestInput")
    def merge_merge_request_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mergeMergeRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="mergeWhenPipelineSucceedsInput")
    def merge_when_pipeline_succeeds_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mergeWhenPipelineSucceedsInput"))

    @builtins.property
    @jsii.member(jsii_name="movedProjectInput")
    def moved_project_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "movedProjectInput"))

    @builtins.property
    @jsii.member(jsii_name="newIssueInput")
    def new_issue_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "newIssueInput"))

    @builtins.property
    @jsii.member(jsii_name="newMergeRequestInput")
    def new_merge_request_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "newMergeRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="newNoteInput")
    def new_note_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "newNoteInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="pushToMergeRequestInput")
    def push_to_merge_request_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pushToMergeRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="reassignIssueInput")
    def reassign_issue_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "reassignIssueInput"))

    @builtins.property
    @jsii.member(jsii_name="reassignMergeRequestInput")
    def reassign_merge_request_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "reassignMergeRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="reopenIssueInput")
    def reopen_issue_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "reopenIssueInput"))

    @builtins.property
    @jsii.member(jsii_name="reopenMergeRequestInput")
    def reopen_merge_request_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "reopenMergeRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="successPipelineInput")
    def success_pipeline_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "successPipelineInput"))

    @builtins.property
    @jsii.member(jsii_name="closeIssue")
    def close_issue(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "closeIssue"))

    @close_issue.setter
    def close_issue(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__115e6fd2afcba0a8b738de7a83642602876a07e8f957b1c4363f8f66744505a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "closeIssue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="closeMergeRequest")
    def close_merge_request(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "closeMergeRequest"))

    @close_merge_request.setter
    def close_merge_request(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7d0700f53f78b893f4ac01a0ab5c5f696ee8f0837626e0da08fb1b11d4ce52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "closeMergeRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failedPipeline")
    def failed_pipeline(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failedPipeline"))

    @failed_pipeline.setter
    def failed_pipeline(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__940d3eafd015d26c8b5fdd8aef413fe5df08e365b8d5b00b83d08a2525c0230f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failedPipeline", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fixedPipeline")
    def fixed_pipeline(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fixedPipeline"))

    @fixed_pipeline.setter
    def fixed_pipeline(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa90a8c370b2310cc9cf851b537b438c160f5cc5207ca717be047129705c66f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedPipeline", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issueDue")
    def issue_due(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "issueDue"))

    @issue_due.setter
    def issue_due(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7a3145e43c976acd281457bfbffe5548f9aacb4120c6582756d3b3f42dcb5c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issueDue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14fbb9db29b88a4b50c554c42232028d6e2d3b94497de0e0ac9e885fbcd93520)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mergeMergeRequest")
    def merge_merge_request(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mergeMergeRequest"))

    @merge_merge_request.setter
    def merge_merge_request(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0adfecf4c03bb97168d434e984378f35201530d6bee60d098bce4d4ffb0eb24c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mergeMergeRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mergeWhenPipelineSucceeds")
    def merge_when_pipeline_succeeds(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mergeWhenPipelineSucceeds"))

    @merge_when_pipeline_succeeds.setter
    def merge_when_pipeline_succeeds(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7a6d50e2dd5e2bce7becd5b2b4534b1554859c1d5ff763673fc30634d96515a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mergeWhenPipelineSucceeds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="movedProject")
    def moved_project(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "movedProject"))

    @moved_project.setter
    def moved_project(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baa5f16b09c154b29407f688bd1aa2eaf702bbdf8d9e27faa616f0f4123f55a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "movedProject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="newIssue")
    def new_issue(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "newIssue"))

    @new_issue.setter
    def new_issue(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c2af151cb0d01adc673ee16849cf72d905efab98d7eef96230a2c8166da0df3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newIssue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="newMergeRequest")
    def new_merge_request(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "newMergeRequest"))

    @new_merge_request.setter
    def new_merge_request(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34475eaf722853d9e031a5d2a484231c5ff0990593f09118123bb0c72ff0a881)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newMergeRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="newNote")
    def new_note(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "newNote"))

    @new_note.setter
    def new_note(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bc9b046c3f070dfbe40d5485fda821d464440fb9abac5560a35dc0d09be9873)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newNote", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53fcb2b990f32338e1fd6feb7828b5a54b1b1cbcbe9165477908e4d59144c541)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pushToMergeRequest")
    def push_to_merge_request(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pushToMergeRequest"))

    @push_to_merge_request.setter
    def push_to_merge_request(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac3fe4ab8a014e53e838e044b4bc22be324b0d6f013b7617ff3ece6f982d879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pushToMergeRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reassignIssue")
    def reassign_issue(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "reassignIssue"))

    @reassign_issue.setter
    def reassign_issue(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__513ab3a73bc8fcdd340736c5569f4acc02f0876913ec0792cbf084352bfd2623)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reassignIssue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reassignMergeRequest")
    def reassign_merge_request(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "reassignMergeRequest"))

    @reassign_merge_request.setter
    def reassign_merge_request(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dd48528a5eb907a6f88a4b2e74d4ff0f6f56530bc8efc13bb8a89f602714c98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reassignMergeRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reopenIssue")
    def reopen_issue(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "reopenIssue"))

    @reopen_issue.setter
    def reopen_issue(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af4b4f9efb1c5924b4226aebfacc50778834e6a063d0eca279b9a8a4c8d7c42b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reopenIssue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reopenMergeRequest")
    def reopen_merge_request(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "reopenMergeRequest"))

    @reopen_merge_request.setter
    def reopen_merge_request(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0d652e16b1f5e30ade5f4b9a72bbf2e4954120cb0168f582084940182acbf09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reopenMergeRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successPipeline")
    def success_pipeline(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "successPipeline"))

    @success_pipeline.setter
    def success_pipeline(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b96c26175df7b9ea3ebe01c47779c0eeb4b9e81ff195a1beb69ff36bac907fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successPipeline", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.projectLevelNotifications.ProjectLevelNotificationsConfig",
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
        "close_issue": "closeIssue",
        "close_merge_request": "closeMergeRequest",
        "failed_pipeline": "failedPipeline",
        "fixed_pipeline": "fixedPipeline",
        "issue_due": "issueDue",
        "level": "level",
        "merge_merge_request": "mergeMergeRequest",
        "merge_when_pipeline_succeeds": "mergeWhenPipelineSucceeds",
        "moved_project": "movedProject",
        "new_issue": "newIssue",
        "new_merge_request": "newMergeRequest",
        "new_note": "newNote",
        "push_to_merge_request": "pushToMergeRequest",
        "reassign_issue": "reassignIssue",
        "reassign_merge_request": "reassignMergeRequest",
        "reopen_issue": "reopenIssue",
        "reopen_merge_request": "reopenMergeRequest",
        "success_pipeline": "successPipeline",
    },
)
class ProjectLevelNotificationsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        close_issue: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        close_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        failed_pipeline: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fixed_pipeline: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        issue_due: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        level: typing.Optional[builtins.str] = None,
        merge_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        merge_when_pipeline_succeeds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        moved_project: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        new_issue: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        new_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        new_note: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        push_to_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reassign_issue: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reassign_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reopen_issue: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reopen_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        success_pipeline: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param project: The ID or URL-encoded path of a project where notifications will be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#project ProjectLevelNotifications#project}
        :param close_issue: Enable notifications for closed issues. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#close_issue ProjectLevelNotifications#close_issue}
        :param close_merge_request: Enable notifications for closed merge requests. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#close_merge_request ProjectLevelNotifications#close_merge_request}
        :param failed_pipeline: Enable notifications for failed pipelines. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#failed_pipeline ProjectLevelNotifications#failed_pipeline}
        :param fixed_pipeline: Enable notifications for fixed pipelines. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#fixed_pipeline ProjectLevelNotifications#fixed_pipeline}
        :param issue_due: Enable notifications for due issues. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#issue_due ProjectLevelNotifications#issue_due}
        :param level: The level of the notification. Valid values are: ``disabled``, ``participating``, ``watch``, ``global``, ``mention``, ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#level ProjectLevelNotifications#level}
        :param merge_merge_request: Enable notifications for merged merge requests. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#merge_merge_request ProjectLevelNotifications#merge_merge_request}
        :param merge_when_pipeline_succeeds: Enable notifications for merged merge requests when the pipeline succeeds. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#merge_when_pipeline_succeeds ProjectLevelNotifications#merge_when_pipeline_succeeds}
        :param moved_project: Enable notifications for moved projects. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#moved_project ProjectLevelNotifications#moved_project}
        :param new_issue: Enable notifications for new issues. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#new_issue ProjectLevelNotifications#new_issue}
        :param new_merge_request: Enable notifications for new merge requests. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#new_merge_request ProjectLevelNotifications#new_merge_request}
        :param new_note: Enable notifications for new notes on merge requests. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#new_note ProjectLevelNotifications#new_note}
        :param push_to_merge_request: Enable notifications for push to merge request branches. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#push_to_merge_request ProjectLevelNotifications#push_to_merge_request}
        :param reassign_issue: Enable notifications for issue reassignments. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#reassign_issue ProjectLevelNotifications#reassign_issue}
        :param reassign_merge_request: Enable notifications for merge request reassignments. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#reassign_merge_request ProjectLevelNotifications#reassign_merge_request}
        :param reopen_issue: Enable notifications for reopened issues. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#reopen_issue ProjectLevelNotifications#reopen_issue}
        :param reopen_merge_request: Enable notifications for reopened merge requests. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#reopen_merge_request ProjectLevelNotifications#reopen_merge_request}
        :param success_pipeline: Enable notifications for successful pipelines. Can only be used when ``level`` is ``custom``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#success_pipeline ProjectLevelNotifications#success_pipeline}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__394ed55e5864ef6b7748d3350ba1226d4b6f9508f530b53a3c82883dd82196fc)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument close_issue", value=close_issue, expected_type=type_hints["close_issue"])
            check_type(argname="argument close_merge_request", value=close_merge_request, expected_type=type_hints["close_merge_request"])
            check_type(argname="argument failed_pipeline", value=failed_pipeline, expected_type=type_hints["failed_pipeline"])
            check_type(argname="argument fixed_pipeline", value=fixed_pipeline, expected_type=type_hints["fixed_pipeline"])
            check_type(argname="argument issue_due", value=issue_due, expected_type=type_hints["issue_due"])
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            check_type(argname="argument merge_merge_request", value=merge_merge_request, expected_type=type_hints["merge_merge_request"])
            check_type(argname="argument merge_when_pipeline_succeeds", value=merge_when_pipeline_succeeds, expected_type=type_hints["merge_when_pipeline_succeeds"])
            check_type(argname="argument moved_project", value=moved_project, expected_type=type_hints["moved_project"])
            check_type(argname="argument new_issue", value=new_issue, expected_type=type_hints["new_issue"])
            check_type(argname="argument new_merge_request", value=new_merge_request, expected_type=type_hints["new_merge_request"])
            check_type(argname="argument new_note", value=new_note, expected_type=type_hints["new_note"])
            check_type(argname="argument push_to_merge_request", value=push_to_merge_request, expected_type=type_hints["push_to_merge_request"])
            check_type(argname="argument reassign_issue", value=reassign_issue, expected_type=type_hints["reassign_issue"])
            check_type(argname="argument reassign_merge_request", value=reassign_merge_request, expected_type=type_hints["reassign_merge_request"])
            check_type(argname="argument reopen_issue", value=reopen_issue, expected_type=type_hints["reopen_issue"])
            check_type(argname="argument reopen_merge_request", value=reopen_merge_request, expected_type=type_hints["reopen_merge_request"])
            check_type(argname="argument success_pipeline", value=success_pipeline, expected_type=type_hints["success_pipeline"])
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
        if close_issue is not None:
            self._values["close_issue"] = close_issue
        if close_merge_request is not None:
            self._values["close_merge_request"] = close_merge_request
        if failed_pipeline is not None:
            self._values["failed_pipeline"] = failed_pipeline
        if fixed_pipeline is not None:
            self._values["fixed_pipeline"] = fixed_pipeline
        if issue_due is not None:
            self._values["issue_due"] = issue_due
        if level is not None:
            self._values["level"] = level
        if merge_merge_request is not None:
            self._values["merge_merge_request"] = merge_merge_request
        if merge_when_pipeline_succeeds is not None:
            self._values["merge_when_pipeline_succeeds"] = merge_when_pipeline_succeeds
        if moved_project is not None:
            self._values["moved_project"] = moved_project
        if new_issue is not None:
            self._values["new_issue"] = new_issue
        if new_merge_request is not None:
            self._values["new_merge_request"] = new_merge_request
        if new_note is not None:
            self._values["new_note"] = new_note
        if push_to_merge_request is not None:
            self._values["push_to_merge_request"] = push_to_merge_request
        if reassign_issue is not None:
            self._values["reassign_issue"] = reassign_issue
        if reassign_merge_request is not None:
            self._values["reassign_merge_request"] = reassign_merge_request
        if reopen_issue is not None:
            self._values["reopen_issue"] = reopen_issue
        if reopen_merge_request is not None:
            self._values["reopen_merge_request"] = reopen_merge_request
        if success_pipeline is not None:
            self._values["success_pipeline"] = success_pipeline

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
        '''The ID or URL-encoded path of a project where notifications will be configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#project ProjectLevelNotifications#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def close_issue(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for closed issues. Can only be used when ``level`` is ``custom``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#close_issue ProjectLevelNotifications#close_issue}
        '''
        result = self._values.get("close_issue")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def close_merge_request(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for closed merge requests. Can only be used when ``level`` is ``custom``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#close_merge_request ProjectLevelNotifications#close_merge_request}
        '''
        result = self._values.get("close_merge_request")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def failed_pipeline(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for failed pipelines. Can only be used when ``level`` is ``custom``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#failed_pipeline ProjectLevelNotifications#failed_pipeline}
        '''
        result = self._values.get("failed_pipeline")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fixed_pipeline(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for fixed pipelines. Can only be used when ``level`` is ``custom``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#fixed_pipeline ProjectLevelNotifications#fixed_pipeline}
        '''
        result = self._values.get("fixed_pipeline")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def issue_due(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for due issues. Can only be used when ``level`` is ``custom``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#issue_due ProjectLevelNotifications#issue_due}
        '''
        result = self._values.get("issue_due")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def level(self) -> typing.Optional[builtins.str]:
        '''The level of the notification. Valid values are: ``disabled``, ``participating``, ``watch``, ``global``, ``mention``, ``custom``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#level ProjectLevelNotifications#level}
        '''
        result = self._values.get("level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def merge_merge_request(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for merged merge requests. Can only be used when ``level`` is ``custom``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#merge_merge_request ProjectLevelNotifications#merge_merge_request}
        '''
        result = self._values.get("merge_merge_request")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def merge_when_pipeline_succeeds(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for merged merge requests when the pipeline succeeds. Can only be used when ``level`` is ``custom``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#merge_when_pipeline_succeeds ProjectLevelNotifications#merge_when_pipeline_succeeds}
        '''
        result = self._values.get("merge_when_pipeline_succeeds")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def moved_project(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for moved projects. Can only be used when ``level`` is ``custom``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#moved_project ProjectLevelNotifications#moved_project}
        '''
        result = self._values.get("moved_project")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def new_issue(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for new issues. Can only be used when ``level`` is ``custom``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#new_issue ProjectLevelNotifications#new_issue}
        '''
        result = self._values.get("new_issue")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def new_merge_request(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for new merge requests. Can only be used when ``level`` is ``custom``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#new_merge_request ProjectLevelNotifications#new_merge_request}
        '''
        result = self._values.get("new_merge_request")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def new_note(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for new notes on merge requests. Can only be used when ``level`` is ``custom``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#new_note ProjectLevelNotifications#new_note}
        '''
        result = self._values.get("new_note")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def push_to_merge_request(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for push to merge request branches. Can only be used when ``level`` is ``custom``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#push_to_merge_request ProjectLevelNotifications#push_to_merge_request}
        '''
        result = self._values.get("push_to_merge_request")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reassign_issue(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for issue reassignments. Can only be used when ``level`` is ``custom``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#reassign_issue ProjectLevelNotifications#reassign_issue}
        '''
        result = self._values.get("reassign_issue")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reassign_merge_request(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for merge request reassignments. Can only be used when ``level`` is ``custom``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#reassign_merge_request ProjectLevelNotifications#reassign_merge_request}
        '''
        result = self._values.get("reassign_merge_request")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reopen_issue(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for reopened issues. Can only be used when ``level`` is ``custom``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#reopen_issue ProjectLevelNotifications#reopen_issue}
        '''
        result = self._values.get("reopen_issue")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reopen_merge_request(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for reopened merge requests. Can only be used when ``level`` is ``custom``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#reopen_merge_request ProjectLevelNotifications#reopen_merge_request}
        '''
        result = self._values.get("reopen_merge_request")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def success_pipeline(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notifications for successful pipelines. Can only be used when ``level`` is ``custom``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_level_notifications#success_pipeline ProjectLevelNotifications#success_pipeline}
        '''
        result = self._values.get("success_pipeline")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectLevelNotificationsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ProjectLevelNotifications",
    "ProjectLevelNotificationsConfig",
]

publication.publish()

def _typecheckingstub__57d3cd3c396fb7cb5e00d36e119da98d6154f9948427ae5fca178ba0da34bdea(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    project: builtins.str,
    close_issue: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    close_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    failed_pipeline: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fixed_pipeline: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    issue_due: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    level: typing.Optional[builtins.str] = None,
    merge_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    merge_when_pipeline_succeeds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    moved_project: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    new_issue: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    new_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    new_note: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    push_to_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reassign_issue: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reassign_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reopen_issue: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reopen_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    success_pipeline: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__97d5183ef71c0202209a57d7bf123c1d1e9f1e8d827632741d2649df6bec0162(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__115e6fd2afcba0a8b738de7a83642602876a07e8f957b1c4363f8f66744505a5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7d0700f53f78b893f4ac01a0ab5c5f696ee8f0837626e0da08fb1b11d4ce52(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__940d3eafd015d26c8b5fdd8aef413fe5df08e365b8d5b00b83d08a2525c0230f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa90a8c370b2310cc9cf851b537b438c160f5cc5207ca717be047129705c66f2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a3145e43c976acd281457bfbffe5548f9aacb4120c6582756d3b3f42dcb5c4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14fbb9db29b88a4b50c554c42232028d6e2d3b94497de0e0ac9e885fbcd93520(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0adfecf4c03bb97168d434e984378f35201530d6bee60d098bce4d4ffb0eb24c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7a6d50e2dd5e2bce7becd5b2b4534b1554859c1d5ff763673fc30634d96515a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baa5f16b09c154b29407f688bd1aa2eaf702bbdf8d9e27faa616f0f4123f55a1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c2af151cb0d01adc673ee16849cf72d905efab98d7eef96230a2c8166da0df3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34475eaf722853d9e031a5d2a484231c5ff0990593f09118123bb0c72ff0a881(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bc9b046c3f070dfbe40d5485fda821d464440fb9abac5560a35dc0d09be9873(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53fcb2b990f32338e1fd6feb7828b5a54b1b1cbcbe9165477908e4d59144c541(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac3fe4ab8a014e53e838e044b4bc22be324b0d6f013b7617ff3ece6f982d879(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__513ab3a73bc8fcdd340736c5569f4acc02f0876913ec0792cbf084352bfd2623(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dd48528a5eb907a6f88a4b2e74d4ff0f6f56530bc8efc13bb8a89f602714c98(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af4b4f9efb1c5924b4226aebfacc50778834e6a063d0eca279b9a8a4c8d7c42b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0d652e16b1f5e30ade5f4b9a72bbf2e4954120cb0168f582084940182acbf09(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b96c26175df7b9ea3ebe01c47779c0eeb4b9e81ff195a1beb69ff36bac907fd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394ed55e5864ef6b7748d3350ba1226d4b6f9508f530b53a3c82883dd82196fc(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: builtins.str,
    close_issue: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    close_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    failed_pipeline: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fixed_pipeline: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    issue_due: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    level: typing.Optional[builtins.str] = None,
    merge_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    merge_when_pipeline_succeeds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    moved_project: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    new_issue: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    new_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    new_note: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    push_to_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reassign_issue: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reassign_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reopen_issue: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reopen_merge_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    success_pipeline: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
