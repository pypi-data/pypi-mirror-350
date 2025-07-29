r'''
# `gitlab_project_issue`

Refer to the Terraform Registry for docs: [`gitlab_project_issue`](https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue).
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


class ProjectIssue(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.projectIssue.ProjectIssue",
):
    '''Represents a {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue gitlab_project_issue}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        project: builtins.str,
        title: builtins.str,
        assignee_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
        confidential: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        created_at: typing.Optional[builtins.str] = None,
        delete_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        discussion_locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        discussion_to_resolve: typing.Optional[builtins.str] = None,
        due_date: typing.Optional[builtins.str] = None,
        epic_issue_id: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        iid: typing.Optional[jsii.Number] = None,
        issue_type: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        merge_request_to_resolve_discussions_of: typing.Optional[jsii.Number] = None,
        milestone_id: typing.Optional[jsii.Number] = None,
        state: typing.Optional[builtins.str] = None,
        updated_at: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue gitlab_project_issue} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param project: The name or ID of the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#project ProjectIssue#project}
        :param title: The title of the issue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#title ProjectIssue#title}
        :param assignee_ids: The IDs of the users to assign the issue to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#assignee_ids ProjectIssue#assignee_ids}
        :param confidential: Set an issue to be confidential. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#confidential ProjectIssue#confidential}
        :param created_at: When the issue was created. Date time string, ISO 8601 formatted, for example 2016-03-11T03:45:40Z. Requires administrator or project/group owner rights. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#created_at ProjectIssue#created_at}
        :param delete_on_destroy: Whether the issue is deleted instead of closed during destroy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#delete_on_destroy ProjectIssue#delete_on_destroy}
        :param description: The description of an issue. Limited to 1,048,576 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#description ProjectIssue#description}
        :param discussion_locked: Whether the issue is locked for discussions or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#discussion_locked ProjectIssue#discussion_locked}
        :param discussion_to_resolve: The ID of a discussion to resolve. This fills out the issue with a default description and mark the discussion as resolved. Use in combination with merge_request_to_resolve_discussions_of. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#discussion_to_resolve ProjectIssue#discussion_to_resolve}
        :param due_date: The due date. Date time string in the format YYYY-MM-DD, for example 2016-03-11. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#due_date ProjectIssue#due_date}
        :param epic_issue_id: The ID of the epic issue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#epic_issue_id ProjectIssue#epic_issue_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#id ProjectIssue#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param iid: The internal ID of the project's issue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#iid ProjectIssue#iid}
        :param issue_type: The type of issue. Valid values are: ``issue``, ``incident``, ``test_case``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#issue_type ProjectIssue#issue_type}
        :param labels: The labels of an issue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#labels ProjectIssue#labels}
        :param merge_request_to_resolve_discussions_of: The IID of a merge request in which to resolve all issues. This fills out the issue with a default description and mark all discussions as resolved. When passing a description or title, these values take precedence over the default values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#merge_request_to_resolve_discussions_of ProjectIssue#merge_request_to_resolve_discussions_of}
        :param milestone_id: The global ID of a milestone to assign issue. To find the milestone_id associated with a milestone, view an issue with the milestone assigned and use the API to retrieve the issue's details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#milestone_id ProjectIssue#milestone_id}
        :param state: The state of the issue. Valid values are: ``opened``, ``closed``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#state ProjectIssue#state}
        :param updated_at: When the issue was updated. Date time string, ISO 8601 formatted, for example 2016-03-11T03:45:40Z. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#updated_at ProjectIssue#updated_at}
        :param weight: The weight of the issue. Valid values are greater than or equal to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#weight ProjectIssue#weight}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5c8a5003c89b7fd480660d816e45897da43a3772f7ccbd20fbe9ee70ca0def0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ProjectIssueConfig(
            project=project,
            title=title,
            assignee_ids=assignee_ids,
            confidential=confidential,
            created_at=created_at,
            delete_on_destroy=delete_on_destroy,
            description=description,
            discussion_locked=discussion_locked,
            discussion_to_resolve=discussion_to_resolve,
            due_date=due_date,
            epic_issue_id=epic_issue_id,
            id=id,
            iid=iid,
            issue_type=issue_type,
            labels=labels,
            merge_request_to_resolve_discussions_of=merge_request_to_resolve_discussions_of,
            milestone_id=milestone_id,
            state=state,
            updated_at=updated_at,
            weight=weight,
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
        '''Generates CDKTF code for importing a ProjectIssue resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ProjectIssue to import.
        :param import_from_id: The id of the existing ProjectIssue that should be imported. Refer to the {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ProjectIssue to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f214ec6164a543ce526667be2fcc6845048167e770d95ce8e852048e6a463c1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAssigneeIds")
    def reset_assignee_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssigneeIds", []))

    @jsii.member(jsii_name="resetConfidential")
    def reset_confidential(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidential", []))

    @jsii.member(jsii_name="resetCreatedAt")
    def reset_created_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreatedAt", []))

    @jsii.member(jsii_name="resetDeleteOnDestroy")
    def reset_delete_on_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteOnDestroy", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDiscussionLocked")
    def reset_discussion_locked(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiscussionLocked", []))

    @jsii.member(jsii_name="resetDiscussionToResolve")
    def reset_discussion_to_resolve(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiscussionToResolve", []))

    @jsii.member(jsii_name="resetDueDate")
    def reset_due_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDueDate", []))

    @jsii.member(jsii_name="resetEpicIssueId")
    def reset_epic_issue_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEpicIssueId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIid")
    def reset_iid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIid", []))

    @jsii.member(jsii_name="resetIssueType")
    def reset_issue_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssueType", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMergeRequestToResolveDiscussionsOf")
    def reset_merge_request_to_resolve_discussions_of(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergeRequestToResolveDiscussionsOf", []))

    @jsii.member(jsii_name="resetMilestoneId")
    def reset_milestone_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMilestoneId", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @jsii.member(jsii_name="resetUpdatedAt")
    def reset_updated_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdatedAt", []))

    @jsii.member(jsii_name="resetWeight")
    def reset_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeight", []))

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
    @jsii.member(jsii_name="authorId")
    def author_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "authorId"))

    @builtins.property
    @jsii.member(jsii_name="closedAt")
    def closed_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "closedAt"))

    @builtins.property
    @jsii.member(jsii_name="closedByUserId")
    def closed_by_user_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "closedByUserId"))

    @builtins.property
    @jsii.member(jsii_name="downvotes")
    def downvotes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "downvotes"))

    @builtins.property
    @jsii.member(jsii_name="epicId")
    def epic_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "epicId"))

    @builtins.property
    @jsii.member(jsii_name="externalId")
    def external_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalId"))

    @builtins.property
    @jsii.member(jsii_name="humanTimeEstimate")
    def human_time_estimate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "humanTimeEstimate"))

    @builtins.property
    @jsii.member(jsii_name="humanTotalTimeSpent")
    def human_total_time_spent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "humanTotalTimeSpent"))

    @builtins.property
    @jsii.member(jsii_name="issueId")
    def issue_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "issueId"))

    @builtins.property
    @jsii.member(jsii_name="issueLinkId")
    def issue_link_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "issueLinkId"))

    @builtins.property
    @jsii.member(jsii_name="links")
    def links(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "links"))

    @builtins.property
    @jsii.member(jsii_name="mergeRequestsCount")
    def merge_requests_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mergeRequestsCount"))

    @builtins.property
    @jsii.member(jsii_name="movedToId")
    def moved_to_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "movedToId"))

    @builtins.property
    @jsii.member(jsii_name="references")
    def references(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "references"))

    @builtins.property
    @jsii.member(jsii_name="subscribed")
    def subscribed(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "subscribed"))

    @builtins.property
    @jsii.member(jsii_name="taskCompletionStatus")
    def task_completion_status(self) -> "ProjectIssueTaskCompletionStatusList":
        return typing.cast("ProjectIssueTaskCompletionStatusList", jsii.get(self, "taskCompletionStatus"))

    @builtins.property
    @jsii.member(jsii_name="timeEstimate")
    def time_estimate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeEstimate"))

    @builtins.property
    @jsii.member(jsii_name="totalTimeSpent")
    def total_time_spent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalTimeSpent"))

    @builtins.property
    @jsii.member(jsii_name="upvotes")
    def upvotes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "upvotes"))

    @builtins.property
    @jsii.member(jsii_name="userNotesCount")
    def user_notes_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "userNotesCount"))

    @builtins.property
    @jsii.member(jsii_name="webUrl")
    def web_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webUrl"))

    @builtins.property
    @jsii.member(jsii_name="assigneeIdsInput")
    def assignee_ids_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "assigneeIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="confidentialInput")
    def confidential_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "confidentialInput"))

    @builtins.property
    @jsii.member(jsii_name="createdAtInput")
    def created_at_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createdAtInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteOnDestroyInput")
    def delete_on_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteOnDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="discussionLockedInput")
    def discussion_locked_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "discussionLockedInput"))

    @builtins.property
    @jsii.member(jsii_name="discussionToResolveInput")
    def discussion_to_resolve_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "discussionToResolveInput"))

    @builtins.property
    @jsii.member(jsii_name="dueDateInput")
    def due_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dueDateInput"))

    @builtins.property
    @jsii.member(jsii_name="epicIssueIdInput")
    def epic_issue_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "epicIssueIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="iidInput")
    def iid_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "iidInput"))

    @builtins.property
    @jsii.member(jsii_name="issueTypeInput")
    def issue_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issueTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="mergeRequestToResolveDiscussionsOfInput")
    def merge_request_to_resolve_discussions_of_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "mergeRequestToResolveDiscussionsOfInput"))

    @builtins.property
    @jsii.member(jsii_name="milestoneIdInput")
    def milestone_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "milestoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="updatedAtInput")
    def updated_at_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updatedAtInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="assigneeIds")
    def assignee_ids(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "assigneeIds"))

    @assignee_ids.setter
    def assignee_ids(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f7a8ab0a0aaa2871e2b0c7972fa33e716193dc55aede8bf8c3a1d0090714a4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assigneeIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="confidential")
    def confidential(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "confidential"))

    @confidential.setter
    def confidential(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98d6c651bce954e8e9ae8aff8307599f83b8b6e108ccdd90f639986f198bb2bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidential", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @created_at.setter
    def created_at(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa9da33a6b7b6201e48b9ab8c1bc59b8063a15096dada4f3177c9c5d02cd3398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteOnDestroy")
    def delete_on_destroy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteOnDestroy"))

    @delete_on_destroy.setter
    def delete_on_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae1b09c9928ade3c0fce87dbd42204b167ffdc89bbaa39805dae700dd8ea2a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteOnDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d54de4936419e03f35052bbe52addfeedb567c40583ae3c3ed3ebd4262a5360a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="discussionLocked")
    def discussion_locked(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "discussionLocked"))

    @discussion_locked.setter
    def discussion_locked(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93d00d776058c0ba24b146a26c5d2b2ab1d3d2ef069130321b05f0aafa87dabe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "discussionLocked", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="discussionToResolve")
    def discussion_to_resolve(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "discussionToResolve"))

    @discussion_to_resolve.setter
    def discussion_to_resolve(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7237d7ba24e19e41b8b8df255b6431a9bd0fd439dac1ac87f446e7e1ba2dab1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "discussionToResolve", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dueDate")
    def due_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dueDate"))

    @due_date.setter
    def due_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efa0afcb7b31667c08204a736c201382dac3e985485d3809a0e25923724b1b58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dueDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="epicIssueId")
    def epic_issue_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "epicIssueId"))

    @epic_issue_id.setter
    def epic_issue_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4f2476d79ba901e4a41ed30a3032fbfad6df5785f9b40e79fc4bad19678a3d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "epicIssueId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__218e1cd7ff5515bc69ed80c63cc11c5afefc8018817ea2ea449ef18ce39693f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iid")
    def iid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "iid"))

    @iid.setter
    def iid(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee748f756afba6699fcba7fd2512c93be07540d2abf7cbe4189714413a0585fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issueType")
    def issue_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issueType"))

    @issue_type.setter
    def issue_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d62447e71a1b268cfc9ed32a090fbc50d544743096f940b4ff07f3cdd5c5949)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issueType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__239b2bb9734876b08a8c104b6a5265736a9f85016f165b3b63d7c6c9ada7c3d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mergeRequestToResolveDiscussionsOf")
    def merge_request_to_resolve_discussions_of(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mergeRequestToResolveDiscussionsOf"))

    @merge_request_to_resolve_discussions_of.setter
    def merge_request_to_resolve_discussions_of(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5800daf734d16638e928ca439256a72dcde4e97e19c7da88a09b062bb9e89a3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mergeRequestToResolveDiscussionsOf", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="milestoneId")
    def milestone_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "milestoneId"))

    @milestone_id.setter
    def milestone_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b2bb12c7007e1b072ad109ab6a52c394ad93523197338229e4cb3ddc88cbaa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "milestoneId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccf77c383b1188a3c16338ad5ec0247d76afb5476bc080f0c872f6b9eab84f85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faa5734ed6a9a56a8cb127e837a3868c88e83889e1216382b689cde93e623c38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16a956978a74869f4d1067f97a9613f9901fdb8d5642b1589ba9d8e8d3b202c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @updated_at.setter
    def updated_at(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__561027ffb3626005fa14a4e8d4138ee5f1aa54202cde539d6cd084f734cd1fd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updatedAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d20ce0f85c857330b171f79e48068fccea06db29f4fd35f5bf12248b18e102b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.projectIssue.ProjectIssueConfig",
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
        "title": "title",
        "assignee_ids": "assigneeIds",
        "confidential": "confidential",
        "created_at": "createdAt",
        "delete_on_destroy": "deleteOnDestroy",
        "description": "description",
        "discussion_locked": "discussionLocked",
        "discussion_to_resolve": "discussionToResolve",
        "due_date": "dueDate",
        "epic_issue_id": "epicIssueId",
        "id": "id",
        "iid": "iid",
        "issue_type": "issueType",
        "labels": "labels",
        "merge_request_to_resolve_discussions_of": "mergeRequestToResolveDiscussionsOf",
        "milestone_id": "milestoneId",
        "state": "state",
        "updated_at": "updatedAt",
        "weight": "weight",
    },
)
class ProjectIssueConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        title: builtins.str,
        assignee_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
        confidential: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        created_at: typing.Optional[builtins.str] = None,
        delete_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        discussion_locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        discussion_to_resolve: typing.Optional[builtins.str] = None,
        due_date: typing.Optional[builtins.str] = None,
        epic_issue_id: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        iid: typing.Optional[jsii.Number] = None,
        issue_type: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        merge_request_to_resolve_discussions_of: typing.Optional[jsii.Number] = None,
        milestone_id: typing.Optional[jsii.Number] = None,
        state: typing.Optional[builtins.str] = None,
        updated_at: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param project: The name or ID of the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#project ProjectIssue#project}
        :param title: The title of the issue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#title ProjectIssue#title}
        :param assignee_ids: The IDs of the users to assign the issue to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#assignee_ids ProjectIssue#assignee_ids}
        :param confidential: Set an issue to be confidential. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#confidential ProjectIssue#confidential}
        :param created_at: When the issue was created. Date time string, ISO 8601 formatted, for example 2016-03-11T03:45:40Z. Requires administrator or project/group owner rights. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#created_at ProjectIssue#created_at}
        :param delete_on_destroy: Whether the issue is deleted instead of closed during destroy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#delete_on_destroy ProjectIssue#delete_on_destroy}
        :param description: The description of an issue. Limited to 1,048,576 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#description ProjectIssue#description}
        :param discussion_locked: Whether the issue is locked for discussions or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#discussion_locked ProjectIssue#discussion_locked}
        :param discussion_to_resolve: The ID of a discussion to resolve. This fills out the issue with a default description and mark the discussion as resolved. Use in combination with merge_request_to_resolve_discussions_of. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#discussion_to_resolve ProjectIssue#discussion_to_resolve}
        :param due_date: The due date. Date time string in the format YYYY-MM-DD, for example 2016-03-11. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#due_date ProjectIssue#due_date}
        :param epic_issue_id: The ID of the epic issue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#epic_issue_id ProjectIssue#epic_issue_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#id ProjectIssue#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param iid: The internal ID of the project's issue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#iid ProjectIssue#iid}
        :param issue_type: The type of issue. Valid values are: ``issue``, ``incident``, ``test_case``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#issue_type ProjectIssue#issue_type}
        :param labels: The labels of an issue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#labels ProjectIssue#labels}
        :param merge_request_to_resolve_discussions_of: The IID of a merge request in which to resolve all issues. This fills out the issue with a default description and mark all discussions as resolved. When passing a description or title, these values take precedence over the default values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#merge_request_to_resolve_discussions_of ProjectIssue#merge_request_to_resolve_discussions_of}
        :param milestone_id: The global ID of a milestone to assign issue. To find the milestone_id associated with a milestone, view an issue with the milestone assigned and use the API to retrieve the issue's details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#milestone_id ProjectIssue#milestone_id}
        :param state: The state of the issue. Valid values are: ``opened``, ``closed``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#state ProjectIssue#state}
        :param updated_at: When the issue was updated. Date time string, ISO 8601 formatted, for example 2016-03-11T03:45:40Z. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#updated_at ProjectIssue#updated_at}
        :param weight: The weight of the issue. Valid values are greater than or equal to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#weight ProjectIssue#weight}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc0298435ebc5f7288fb2efcb4a7b9df9475aac392af4f16fc00c9753a63b3d2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument assignee_ids", value=assignee_ids, expected_type=type_hints["assignee_ids"])
            check_type(argname="argument confidential", value=confidential, expected_type=type_hints["confidential"])
            check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
            check_type(argname="argument delete_on_destroy", value=delete_on_destroy, expected_type=type_hints["delete_on_destroy"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument discussion_locked", value=discussion_locked, expected_type=type_hints["discussion_locked"])
            check_type(argname="argument discussion_to_resolve", value=discussion_to_resolve, expected_type=type_hints["discussion_to_resolve"])
            check_type(argname="argument due_date", value=due_date, expected_type=type_hints["due_date"])
            check_type(argname="argument epic_issue_id", value=epic_issue_id, expected_type=type_hints["epic_issue_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument iid", value=iid, expected_type=type_hints["iid"])
            check_type(argname="argument issue_type", value=issue_type, expected_type=type_hints["issue_type"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument merge_request_to_resolve_discussions_of", value=merge_request_to_resolve_discussions_of, expected_type=type_hints["merge_request_to_resolve_discussions_of"])
            check_type(argname="argument milestone_id", value=milestone_id, expected_type=type_hints["milestone_id"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project": project,
            "title": title,
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
        if assignee_ids is not None:
            self._values["assignee_ids"] = assignee_ids
        if confidential is not None:
            self._values["confidential"] = confidential
        if created_at is not None:
            self._values["created_at"] = created_at
        if delete_on_destroy is not None:
            self._values["delete_on_destroy"] = delete_on_destroy
        if description is not None:
            self._values["description"] = description
        if discussion_locked is not None:
            self._values["discussion_locked"] = discussion_locked
        if discussion_to_resolve is not None:
            self._values["discussion_to_resolve"] = discussion_to_resolve
        if due_date is not None:
            self._values["due_date"] = due_date
        if epic_issue_id is not None:
            self._values["epic_issue_id"] = epic_issue_id
        if id is not None:
            self._values["id"] = id
        if iid is not None:
            self._values["iid"] = iid
        if issue_type is not None:
            self._values["issue_type"] = issue_type
        if labels is not None:
            self._values["labels"] = labels
        if merge_request_to_resolve_discussions_of is not None:
            self._values["merge_request_to_resolve_discussions_of"] = merge_request_to_resolve_discussions_of
        if milestone_id is not None:
            self._values["milestone_id"] = milestone_id
        if state is not None:
            self._values["state"] = state
        if updated_at is not None:
            self._values["updated_at"] = updated_at
        if weight is not None:
            self._values["weight"] = weight

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
        '''The name or ID of the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#project ProjectIssue#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''The title of the issue.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#title ProjectIssue#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def assignee_ids(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The IDs of the users to assign the issue to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#assignee_ids ProjectIssue#assignee_ids}
        '''
        result = self._values.get("assignee_ids")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def confidential(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set an issue to be confidential.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#confidential ProjectIssue#confidential}
        '''
        result = self._values.get("confidential")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def created_at(self) -> typing.Optional[builtins.str]:
        '''When the issue was created.

        Date time string, ISO 8601 formatted, for example 2016-03-11T03:45:40Z. Requires administrator or project/group owner rights.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#created_at ProjectIssue#created_at}
        '''
        result = self._values.get("created_at")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the issue is deleted instead of closed during destroy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#delete_on_destroy ProjectIssue#delete_on_destroy}
        '''
        result = self._values.get("delete_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of an issue. Limited to 1,048,576 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#description ProjectIssue#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def discussion_locked(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the issue is locked for discussions or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#discussion_locked ProjectIssue#discussion_locked}
        '''
        result = self._values.get("discussion_locked")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def discussion_to_resolve(self) -> typing.Optional[builtins.str]:
        '''The ID of a discussion to resolve.

        This fills out the issue with a default description and mark the discussion as resolved. Use in combination with merge_request_to_resolve_discussions_of.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#discussion_to_resolve ProjectIssue#discussion_to_resolve}
        '''
        result = self._values.get("discussion_to_resolve")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def due_date(self) -> typing.Optional[builtins.str]:
        '''The due date. Date time string in the format YYYY-MM-DD, for example 2016-03-11.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#due_date ProjectIssue#due_date}
        '''
        result = self._values.get("due_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def epic_issue_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of the epic issue.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#epic_issue_id ProjectIssue#epic_issue_id}
        '''
        result = self._values.get("epic_issue_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#id ProjectIssue#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iid(self) -> typing.Optional[jsii.Number]:
        '''The internal ID of the project's issue.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#iid ProjectIssue#iid}
        '''
        result = self._values.get("iid")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def issue_type(self) -> typing.Optional[builtins.str]:
        '''The type of issue. Valid values are: ``issue``, ``incident``, ``test_case``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#issue_type ProjectIssue#issue_type}
        '''
        result = self._values.get("issue_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The labels of an issue.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#labels ProjectIssue#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def merge_request_to_resolve_discussions_of(self) -> typing.Optional[jsii.Number]:
        '''The IID of a merge request in which to resolve all issues.

        This fills out the issue with a default description and mark all discussions as resolved. When passing a description or title, these values take precedence over the default values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#merge_request_to_resolve_discussions_of ProjectIssue#merge_request_to_resolve_discussions_of}
        '''
        result = self._values.get("merge_request_to_resolve_discussions_of")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def milestone_id(self) -> typing.Optional[jsii.Number]:
        '''The global ID of a milestone to assign issue.

        To find the milestone_id associated with a milestone, view an issue with the milestone assigned and use the API to retrieve the issue's details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#milestone_id ProjectIssue#milestone_id}
        '''
        result = self._values.get("milestone_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the issue. Valid values are: ``opened``, ``closed``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#state ProjectIssue#state}
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def updated_at(self) -> typing.Optional[builtins.str]:
        '''When the issue was updated. Date time string, ISO 8601 formatted, for example 2016-03-11T03:45:40Z.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#updated_at ProjectIssue#updated_at}
        '''
        result = self._values.get("updated_at")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''The weight of the issue. Valid values are greater than or equal to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue#weight ProjectIssue#weight}
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectIssueConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.projectIssue.ProjectIssueTaskCompletionStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class ProjectIssueTaskCompletionStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectIssueTaskCompletionStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectIssueTaskCompletionStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.projectIssue.ProjectIssueTaskCompletionStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0340b2bb54105ffa9fd3653980e0646717210e7e608e3a07ae5f3f392a80f3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ProjectIssueTaskCompletionStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d793e2561968b4dd165335a2e72c0f145d02e97e547bcc4fbd998cb942bd4ac)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProjectIssueTaskCompletionStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d23a4815ec882757a5761ed96350a74ba6d21beaa70619193199f6212170be2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c8273633446a6c1a8f1bf3de7510375255da3e26c0633bd49461912ef278c6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e0aa72a38fdf244d9fc4e7de8ad07e49250fe79bcafcf8ed60d1945f3071501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ProjectIssueTaskCompletionStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.projectIssue.ProjectIssueTaskCompletionStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d114c2e68585394cf2edc786dde47c8c4c28fc478b4249a5b9de3415fef23d8a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="completedCount")
    def completed_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "completedCount"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ProjectIssueTaskCompletionStatus]:
        return typing.cast(typing.Optional[ProjectIssueTaskCompletionStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ProjectIssueTaskCompletionStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfae7ec96a0bccf3737e531d4efe90c12dd43482fa4e0d197c4854a138bc3f16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ProjectIssue",
    "ProjectIssueConfig",
    "ProjectIssueTaskCompletionStatus",
    "ProjectIssueTaskCompletionStatusList",
    "ProjectIssueTaskCompletionStatusOutputReference",
]

publication.publish()

def _typecheckingstub__f5c8a5003c89b7fd480660d816e45897da43a3772f7ccbd20fbe9ee70ca0def0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    project: builtins.str,
    title: builtins.str,
    assignee_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
    confidential: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    created_at: typing.Optional[builtins.str] = None,
    delete_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    discussion_locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    discussion_to_resolve: typing.Optional[builtins.str] = None,
    due_date: typing.Optional[builtins.str] = None,
    epic_issue_id: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    iid: typing.Optional[jsii.Number] = None,
    issue_type: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    merge_request_to_resolve_discussions_of: typing.Optional[jsii.Number] = None,
    milestone_id: typing.Optional[jsii.Number] = None,
    state: typing.Optional[builtins.str] = None,
    updated_at: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__1f214ec6164a543ce526667be2fcc6845048167e770d95ce8e852048e6a463c1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f7a8ab0a0aaa2871e2b0c7972fa33e716193dc55aede8bf8c3a1d0090714a4e(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d6c651bce954e8e9ae8aff8307599f83b8b6e108ccdd90f639986f198bb2bf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9da33a6b7b6201e48b9ab8c1bc59b8063a15096dada4f3177c9c5d02cd3398(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae1b09c9928ade3c0fce87dbd42204b167ffdc89bbaa39805dae700dd8ea2a2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d54de4936419e03f35052bbe52addfeedb567c40583ae3c3ed3ebd4262a5360a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d00d776058c0ba24b146a26c5d2b2ab1d3d2ef069130321b05f0aafa87dabe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7237d7ba24e19e41b8b8df255b6431a9bd0fd439dac1ac87f446e7e1ba2dab1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa0afcb7b31667c08204a736c201382dac3e985485d3809a0e25923724b1b58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f2476d79ba901e4a41ed30a3032fbfad6df5785f9b40e79fc4bad19678a3d9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__218e1cd7ff5515bc69ed80c63cc11c5afefc8018817ea2ea449ef18ce39693f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee748f756afba6699fcba7fd2512c93be07540d2abf7cbe4189714413a0585fb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d62447e71a1b268cfc9ed32a090fbc50d544743096f940b4ff07f3cdd5c5949(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__239b2bb9734876b08a8c104b6a5265736a9f85016f165b3b63d7c6c9ada7c3d0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5800daf734d16638e928ca439256a72dcde4e97e19c7da88a09b062bb9e89a3f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b2bb12c7007e1b072ad109ab6a52c394ad93523197338229e4cb3ddc88cbaa9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf77c383b1188a3c16338ad5ec0247d76afb5476bc080f0c872f6b9eab84f85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa5734ed6a9a56a8cb127e837a3868c88e83889e1216382b689cde93e623c38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a956978a74869f4d1067f97a9613f9901fdb8d5642b1589ba9d8e8d3b202c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__561027ffb3626005fa14a4e8d4138ee5f1aa54202cde539d6cd084f734cd1fd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d20ce0f85c857330b171f79e48068fccea06db29f4fd35f5bf12248b18e102b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0298435ebc5f7288fb2efcb4a7b9df9475aac392af4f16fc00c9753a63b3d2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: builtins.str,
    title: builtins.str,
    assignee_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
    confidential: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    created_at: typing.Optional[builtins.str] = None,
    delete_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    discussion_locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    discussion_to_resolve: typing.Optional[builtins.str] = None,
    due_date: typing.Optional[builtins.str] = None,
    epic_issue_id: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    iid: typing.Optional[jsii.Number] = None,
    issue_type: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    merge_request_to_resolve_discussions_of: typing.Optional[jsii.Number] = None,
    milestone_id: typing.Optional[jsii.Number] = None,
    state: typing.Optional[builtins.str] = None,
    updated_at: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0340b2bb54105ffa9fd3653980e0646717210e7e608e3a07ae5f3f392a80f3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d793e2561968b4dd165335a2e72c0f145d02e97e547bcc4fbd998cb942bd4ac(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23a4815ec882757a5761ed96350a74ba6d21beaa70619193199f6212170be2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c8273633446a6c1a8f1bf3de7510375255da3e26c0633bd49461912ef278c6c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e0aa72a38fdf244d9fc4e7de8ad07e49250fe79bcafcf8ed60d1945f3071501(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d114c2e68585394cf2edc786dde47c8c4c28fc478b4249a5b9de3415fef23d8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfae7ec96a0bccf3737e531d4efe90c12dd43482fa4e0d197c4854a138bc3f16(
    value: typing.Optional[ProjectIssueTaskCompletionStatus],
) -> None:
    """Type checking stubs"""
    pass
