r'''
# `data_gitlab_project_issues`

Refer to the Terraform Registry for docs: [`data_gitlab_project_issues`](https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues).
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


class DataGitlabProjectIssues(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjectIssues.DataGitlabProjectIssues",
):
    '''Represents a {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues gitlab_project_issues}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        project: builtins.str,
        assignee_id: typing.Optional[jsii.Number] = None,
        assignee_username: typing.Optional[builtins.str] = None,
        author_id: typing.Optional[jsii.Number] = None,
        confidential: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        created_after: typing.Optional[builtins.str] = None,
        created_before: typing.Optional[builtins.str] = None,
        due_date: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        iids: typing.Optional[typing.Sequence[jsii.Number]] = None,
        issue_type: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        milestone: typing.Optional[builtins.str] = None,
        my_reaction_emoji: typing.Optional[builtins.str] = None,
        not_assignee_id: typing.Optional[typing.Sequence[jsii.Number]] = None,
        not_author_id: typing.Optional[typing.Sequence[jsii.Number]] = None,
        not_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        not_milestone: typing.Optional[builtins.str] = None,
        not_my_reaction_emoji: typing.Optional[typing.Sequence[builtins.str]] = None,
        order_by: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        search: typing.Optional[builtins.str] = None,
        sort: typing.Optional[builtins.str] = None,
        updated_after: typing.Optional[builtins.str] = None,
        updated_before: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
        with_labels_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues gitlab_project_issues} Data Source.

        :param scope_: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param project: The name or id of the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#project DataGitlabProjectIssues#project}
        :param assignee_id: Return issues assigned to the given user id. Mutually exclusive with assignee_username. None returns unassigned issues. Any returns issues with an assignee. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#assignee_id DataGitlabProjectIssues#assignee_id}
        :param assignee_username: Return issues assigned to the given username. Similar to assignee_id and mutually exclusive with assignee_id. In GitLab CE, the assignee_username array should only contain a single value. Otherwise, an invalid parameter error is returned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#assignee_username DataGitlabProjectIssues#assignee_username}
        :param author_id: Return issues created by the given user id. Combine with scope=all or scope=assigned_to_me. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#author_id DataGitlabProjectIssues#author_id}
        :param confidential: Filter confidential or public issues. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#confidential DataGitlabProjectIssues#confidential}
        :param created_after: Return issues created on or after the given time. Expected in ISO 8601 format (2019-03-15T08:00:00Z). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#created_after DataGitlabProjectIssues#created_after}
        :param created_before: Return issues created on or before the given time. Expected in ISO 8601 format (2019-03-15T08:00:00Z). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#created_before DataGitlabProjectIssues#created_before}
        :param due_date: Return issues that have no due date, are overdue, or whose due date is this week, this month, or between two weeks ago and next month. Accepts: 0 (no due date), any, today, tomorrow, overdue, week, month, next_month_and_previous_two_weeks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#due_date DataGitlabProjectIssues#due_date}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#id DataGitlabProjectIssues#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param iids: Return only the issues having the given iid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#iids DataGitlabProjectIssues#iids}
        :param issue_type: Filter to a given type of issue. Valid values are [issue incident test_case]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#issue_type DataGitlabProjectIssues#issue_type}
        :param labels: Return issues with labels. Issues must have all labels to be returned. None lists all issues with no labels. Any lists all issues with at least one label. No+Label (Deprecated) lists all issues with no labels. Predefined names are case-insensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#labels DataGitlabProjectIssues#labels}
        :param milestone: The milestone title. None lists all issues with no milestone. Any lists all issues that have an assigned milestone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#milestone DataGitlabProjectIssues#milestone}
        :param my_reaction_emoji: Return issues reacted by the authenticated user by the given emoji. None returns issues not given a reaction. Any returns issues given at least one reaction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#my_reaction_emoji DataGitlabProjectIssues#my_reaction_emoji}
        :param not_assignee_id: Return issues that do not match the assignee id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#not_assignee_id DataGitlabProjectIssues#not_assignee_id}
        :param not_author_id: Return issues that do not match the author id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#not_author_id DataGitlabProjectIssues#not_author_id}
        :param not_labels: Return issues that do not match the labels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#not_labels DataGitlabProjectIssues#not_labels}
        :param not_milestone: Return issues that do not match the milestone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#not_milestone DataGitlabProjectIssues#not_milestone}
        :param not_my_reaction_emoji: Return issues not reacted by the authenticated user by the given emoji. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#not_my_reaction_emoji DataGitlabProjectIssues#not_my_reaction_emoji}
        :param order_by: Return issues ordered by. Valid values are ``created_at``, ``updated_at``, ``priority``, ``due_date``, ``relative_position``, ``label_priority``, ``milestone_due``, ``popularity``, ``weight``. Default is created_at. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#order_by DataGitlabProjectIssues#order_by}
        :param scope: Return issues for the given scope. Valid values are ``created_by_me``, ``assigned_to_me``, ``all``. Defaults to all. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#scope DataGitlabProjectIssues#scope}
        :param search: Search project issues against their title and description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#search DataGitlabProjectIssues#search}
        :param sort: Return issues sorted in asc or desc order. Default is desc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#sort DataGitlabProjectIssues#sort}
        :param updated_after: Return issues updated on or after the given time. Expected in ISO 8601 format (2019-03-15T08:00:00Z). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#updated_after DataGitlabProjectIssues#updated_after}
        :param updated_before: Return issues updated on or before the given time. Expected in ISO 8601 format (2019-03-15T08:00:00Z). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#updated_before DataGitlabProjectIssues#updated_before}
        :param weight: Return issues with the specified weight. None returns issues with no weight assigned. Any returns issues with a weight assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#weight DataGitlabProjectIssues#weight}
        :param with_labels_details: If true, the response returns more details for each label in labels field: :name, :color, :description, :description_html, :text_color. Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#with_labels_details DataGitlabProjectIssues#with_labels_details}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4172e0413e98c79659f7ad96c8b9719724c5bb35fffa3c8c740e6baed4978222)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataGitlabProjectIssuesConfig(
            project=project,
            assignee_id=assignee_id,
            assignee_username=assignee_username,
            author_id=author_id,
            confidential=confidential,
            created_after=created_after,
            created_before=created_before,
            due_date=due_date,
            id=id,
            iids=iids,
            issue_type=issue_type,
            labels=labels,
            milestone=milestone,
            my_reaction_emoji=my_reaction_emoji,
            not_assignee_id=not_assignee_id,
            not_author_id=not_author_id,
            not_labels=not_labels,
            not_milestone=not_milestone,
            not_my_reaction_emoji=not_my_reaction_emoji,
            order_by=order_by,
            scope=scope,
            search=search,
            sort=sort,
            updated_after=updated_after,
            updated_before=updated_before,
            weight=weight,
            with_labels_details=with_labels_details,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope_, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a DataGitlabProjectIssues resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataGitlabProjectIssues to import.
        :param import_from_id: The id of the existing DataGitlabProjectIssues that should be imported. Refer to the {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataGitlabProjectIssues to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d17b5123c0726bcdaa6fcfc90e8cb3b9eb6ebb040d8b0e1b4a3629e64ba80b00)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAssigneeId")
    def reset_assignee_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssigneeId", []))

    @jsii.member(jsii_name="resetAssigneeUsername")
    def reset_assignee_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssigneeUsername", []))

    @jsii.member(jsii_name="resetAuthorId")
    def reset_author_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorId", []))

    @jsii.member(jsii_name="resetConfidential")
    def reset_confidential(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidential", []))

    @jsii.member(jsii_name="resetCreatedAfter")
    def reset_created_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreatedAfter", []))

    @jsii.member(jsii_name="resetCreatedBefore")
    def reset_created_before(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreatedBefore", []))

    @jsii.member(jsii_name="resetDueDate")
    def reset_due_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDueDate", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIids")
    def reset_iids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIids", []))

    @jsii.member(jsii_name="resetIssueType")
    def reset_issue_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssueType", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMilestone")
    def reset_milestone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMilestone", []))

    @jsii.member(jsii_name="resetMyReactionEmoji")
    def reset_my_reaction_emoji(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMyReactionEmoji", []))

    @jsii.member(jsii_name="resetNotAssigneeId")
    def reset_not_assignee_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotAssigneeId", []))

    @jsii.member(jsii_name="resetNotAuthorId")
    def reset_not_author_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotAuthorId", []))

    @jsii.member(jsii_name="resetNotLabels")
    def reset_not_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotLabels", []))

    @jsii.member(jsii_name="resetNotMilestone")
    def reset_not_milestone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotMilestone", []))

    @jsii.member(jsii_name="resetNotMyReactionEmoji")
    def reset_not_my_reaction_emoji(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotMyReactionEmoji", []))

    @jsii.member(jsii_name="resetOrderBy")
    def reset_order_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrderBy", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @jsii.member(jsii_name="resetSearch")
    def reset_search(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearch", []))

    @jsii.member(jsii_name="resetSort")
    def reset_sort(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSort", []))

    @jsii.member(jsii_name="resetUpdatedAfter")
    def reset_updated_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdatedAfter", []))

    @jsii.member(jsii_name="resetUpdatedBefore")
    def reset_updated_before(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdatedBefore", []))

    @jsii.member(jsii_name="resetWeight")
    def reset_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeight", []))

    @jsii.member(jsii_name="resetWithLabelsDetails")
    def reset_with_labels_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWithLabelsDetails", []))

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
    @jsii.member(jsii_name="issues")
    def issues(self) -> "DataGitlabProjectIssuesIssuesList":
        return typing.cast("DataGitlabProjectIssuesIssuesList", jsii.get(self, "issues"))

    @builtins.property
    @jsii.member(jsii_name="assigneeIdInput")
    def assignee_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "assigneeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="assigneeUsernameInput")
    def assignee_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assigneeUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="authorIdInput")
    def author_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "authorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="confidentialInput")
    def confidential_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "confidentialInput"))

    @builtins.property
    @jsii.member(jsii_name="createdAfterInput")
    def created_after_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createdAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="createdBeforeInput")
    def created_before_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createdBeforeInput"))

    @builtins.property
    @jsii.member(jsii_name="dueDateInput")
    def due_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dueDateInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="iidsInput")
    def iids_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "iidsInput"))

    @builtins.property
    @jsii.member(jsii_name="issueTypeInput")
    def issue_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issueTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="milestoneInput")
    def milestone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "milestoneInput"))

    @builtins.property
    @jsii.member(jsii_name="myReactionEmojiInput")
    def my_reaction_emoji_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "myReactionEmojiInput"))

    @builtins.property
    @jsii.member(jsii_name="notAssigneeIdInput")
    def not_assignee_id_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "notAssigneeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="notAuthorIdInput")
    def not_author_id_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "notAuthorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="notLabelsInput")
    def not_labels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="notMilestoneInput")
    def not_milestone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notMilestoneInput"))

    @builtins.property
    @jsii.member(jsii_name="notMyReactionEmojiInput")
    def not_my_reaction_emoji_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notMyReactionEmojiInput"))

    @builtins.property
    @jsii.member(jsii_name="orderByInput")
    def order_by_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orderByInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="searchInput")
    def search_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "searchInput"))

    @builtins.property
    @jsii.member(jsii_name="sortInput")
    def sort_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sortInput"))

    @builtins.property
    @jsii.member(jsii_name="updatedAfterInput")
    def updated_after_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updatedAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="updatedBeforeInput")
    def updated_before_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updatedBeforeInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="withLabelsDetailsInput")
    def with_labels_details_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "withLabelsDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="assigneeId")
    def assignee_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "assigneeId"))

    @assignee_id.setter
    def assignee_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1fdeee3fb1fe348233ab6120dca7354b3c525e11cf7e07ee5cddc8f243c20ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assigneeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="assigneeUsername")
    def assignee_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assigneeUsername"))

    @assignee_username.setter
    def assignee_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__214ba90b0e34593f563bba5758a0e0e7ff90910aab79889da2541ccfd6a9dee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assigneeUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authorId")
    def author_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "authorId"))

    @author_id.setter
    def author_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__415ebea6b263c39e8d6ba8ee71a42c95a3d907ce2062d7cfc81b3acc49e9e493)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorId", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__2a7bb5f3e4a5d6807d5846f3893e9c55c0689e176c23db8b6523d450cc9d272c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidential", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createdAfter")
    def created_after(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAfter"))

    @created_after.setter
    def created_after(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b8636690c5d55687df9cb25d081c92f664896b7684e7089d57a543c05ec9082)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createdBefore")
    def created_before(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdBefore"))

    @created_before.setter
    def created_before(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__707934e2fb1023ac3f316bc4d67cc40d6c1cc40e3415fb462d7b5ad2a99e1e80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdBefore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dueDate")
    def due_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dueDate"))

    @due_date.setter
    def due_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49f56adc8b64674edb57c43e0f417d49a7c736940332d54a28dae030e852a3ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dueDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b08edead9e5b40c2eda95f2832200a046e6e1d0ff7b770e9617fe6d4623411)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iids")
    def iids(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "iids"))

    @iids.setter
    def iids(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec0460fe1a22e8c5982458b7402416cfc8dc41b44a9a8f8864b7b22eccda7268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iids", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issueType")
    def issue_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issueType"))

    @issue_type.setter
    def issue_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed5f4040d0f339d701664b3ac601ed9d8c5fea0d8f74c003f11219c9d252a316)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issueType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3137278c3de848531d17ba1b0fcab4c233ba2a99553e053873598c16a4a0234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="milestone")
    def milestone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "milestone"))

    @milestone.setter
    def milestone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8eb33a2a76ae1202706c712cc215d6a803baa2d62a4d4b9ae6f4d2d5fe04033)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "milestone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="myReactionEmoji")
    def my_reaction_emoji(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "myReactionEmoji"))

    @my_reaction_emoji.setter
    def my_reaction_emoji(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d1d9886a864f5835e2f34b561cc99323f1e29a04e402d19eebdaa7d30c61eed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "myReactionEmoji", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notAssigneeId")
    def not_assignee_id(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "notAssigneeId"))

    @not_assignee_id.setter
    def not_assignee_id(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ca2892d281b27e69ddd9921d404a6d7d6efce9a47130500e63e1ea723b4e6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notAssigneeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notAuthorId")
    def not_author_id(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "notAuthorId"))

    @not_author_id.setter
    def not_author_id(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bac85bfbdbb025fbb9c6a4ef5d8324704419e873400a24e660934d5ec9f5e2d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notAuthorId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notLabels")
    def not_labels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notLabels"))

    @not_labels.setter
    def not_labels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9142d465a0787957266dda5bcf56a561827239aef85d21351787431b73447a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notMilestone")
    def not_milestone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notMilestone"))

    @not_milestone.setter
    def not_milestone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bb24071ea865dc14885266a8d2e85730a68d58c54730b325ad7275dac523491)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notMilestone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notMyReactionEmoji")
    def not_my_reaction_emoji(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notMyReactionEmoji"))

    @not_my_reaction_emoji.setter
    def not_my_reaction_emoji(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9f95b7c07b7733587db27c9d2d320ef29255f9a446c420fd4015161e1cd2516)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notMyReactionEmoji", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orderBy")
    def order_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orderBy"))

    @order_by.setter
    def order_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e83c34e7aa0c704c65406d2cfb55b9bfeb2e9d3ebd54d5da5811694d30ed800)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orderBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c491e355f56c376490c68b9ead7e0a388f0e8486bf01756909a7ed48fd358e25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe4c6de42f35145cc66538cb2970d02ce1a0225d786bb4251f46f765bf0332ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="search")
    def search(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "search"))

    @search.setter
    def search(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54602a2b6df509384fef35a139ed73f4df894470dce80650bdec866605a89af0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "search", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sort")
    def sort(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sort"))

    @sort.setter
    def sort(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55abf7f6e8ecb23590a4407c63cde82c84d9d0ca85b9ef76aee0a0839f8b4c6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updatedAfter")
    def updated_after(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAfter"))

    @updated_after.setter
    def updated_after(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3974a80789d1fb233a7907150ee320bd9f53ecf6c649bdc5081fe1851e04a98e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updatedAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updatedBefore")
    def updated_before(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedBefore"))

    @updated_before.setter
    def updated_before(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e552e48e595a7068e79345684bedd34525a1ba8e740772198a2fb4295a933613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updatedBefore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cebb289d046b9d80889a9c8f4c4f0aca3c5c88480d059f82bb0888e02454a6d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="withLabelsDetails")
    def with_labels_details(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "withLabelsDetails"))

    @with_labels_details.setter
    def with_labels_details(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e37a717584cdea7a5a59619f8f3462a4afc24ed472c8a67d3bc27f85e91bd665)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withLabelsDetails", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjectIssues.DataGitlabProjectIssuesConfig",
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
        "assignee_id": "assigneeId",
        "assignee_username": "assigneeUsername",
        "author_id": "authorId",
        "confidential": "confidential",
        "created_after": "createdAfter",
        "created_before": "createdBefore",
        "due_date": "dueDate",
        "id": "id",
        "iids": "iids",
        "issue_type": "issueType",
        "labels": "labels",
        "milestone": "milestone",
        "my_reaction_emoji": "myReactionEmoji",
        "not_assignee_id": "notAssigneeId",
        "not_author_id": "notAuthorId",
        "not_labels": "notLabels",
        "not_milestone": "notMilestone",
        "not_my_reaction_emoji": "notMyReactionEmoji",
        "order_by": "orderBy",
        "scope": "scope",
        "search": "search",
        "sort": "sort",
        "updated_after": "updatedAfter",
        "updated_before": "updatedBefore",
        "weight": "weight",
        "with_labels_details": "withLabelsDetails",
    },
)
class DataGitlabProjectIssuesConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        assignee_id: typing.Optional[jsii.Number] = None,
        assignee_username: typing.Optional[builtins.str] = None,
        author_id: typing.Optional[jsii.Number] = None,
        confidential: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        created_after: typing.Optional[builtins.str] = None,
        created_before: typing.Optional[builtins.str] = None,
        due_date: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        iids: typing.Optional[typing.Sequence[jsii.Number]] = None,
        issue_type: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        milestone: typing.Optional[builtins.str] = None,
        my_reaction_emoji: typing.Optional[builtins.str] = None,
        not_assignee_id: typing.Optional[typing.Sequence[jsii.Number]] = None,
        not_author_id: typing.Optional[typing.Sequence[jsii.Number]] = None,
        not_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        not_milestone: typing.Optional[builtins.str] = None,
        not_my_reaction_emoji: typing.Optional[typing.Sequence[builtins.str]] = None,
        order_by: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        search: typing.Optional[builtins.str] = None,
        sort: typing.Optional[builtins.str] = None,
        updated_after: typing.Optional[builtins.str] = None,
        updated_before: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
        with_labels_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param project: The name or id of the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#project DataGitlabProjectIssues#project}
        :param assignee_id: Return issues assigned to the given user id. Mutually exclusive with assignee_username. None returns unassigned issues. Any returns issues with an assignee. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#assignee_id DataGitlabProjectIssues#assignee_id}
        :param assignee_username: Return issues assigned to the given username. Similar to assignee_id and mutually exclusive with assignee_id. In GitLab CE, the assignee_username array should only contain a single value. Otherwise, an invalid parameter error is returned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#assignee_username DataGitlabProjectIssues#assignee_username}
        :param author_id: Return issues created by the given user id. Combine with scope=all or scope=assigned_to_me. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#author_id DataGitlabProjectIssues#author_id}
        :param confidential: Filter confidential or public issues. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#confidential DataGitlabProjectIssues#confidential}
        :param created_after: Return issues created on or after the given time. Expected in ISO 8601 format (2019-03-15T08:00:00Z). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#created_after DataGitlabProjectIssues#created_after}
        :param created_before: Return issues created on or before the given time. Expected in ISO 8601 format (2019-03-15T08:00:00Z). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#created_before DataGitlabProjectIssues#created_before}
        :param due_date: Return issues that have no due date, are overdue, or whose due date is this week, this month, or between two weeks ago and next month. Accepts: 0 (no due date), any, today, tomorrow, overdue, week, month, next_month_and_previous_two_weeks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#due_date DataGitlabProjectIssues#due_date}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#id DataGitlabProjectIssues#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param iids: Return only the issues having the given iid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#iids DataGitlabProjectIssues#iids}
        :param issue_type: Filter to a given type of issue. Valid values are [issue incident test_case]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#issue_type DataGitlabProjectIssues#issue_type}
        :param labels: Return issues with labels. Issues must have all labels to be returned. None lists all issues with no labels. Any lists all issues with at least one label. No+Label (Deprecated) lists all issues with no labels. Predefined names are case-insensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#labels DataGitlabProjectIssues#labels}
        :param milestone: The milestone title. None lists all issues with no milestone. Any lists all issues that have an assigned milestone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#milestone DataGitlabProjectIssues#milestone}
        :param my_reaction_emoji: Return issues reacted by the authenticated user by the given emoji. None returns issues not given a reaction. Any returns issues given at least one reaction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#my_reaction_emoji DataGitlabProjectIssues#my_reaction_emoji}
        :param not_assignee_id: Return issues that do not match the assignee id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#not_assignee_id DataGitlabProjectIssues#not_assignee_id}
        :param not_author_id: Return issues that do not match the author id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#not_author_id DataGitlabProjectIssues#not_author_id}
        :param not_labels: Return issues that do not match the labels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#not_labels DataGitlabProjectIssues#not_labels}
        :param not_milestone: Return issues that do not match the milestone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#not_milestone DataGitlabProjectIssues#not_milestone}
        :param not_my_reaction_emoji: Return issues not reacted by the authenticated user by the given emoji. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#not_my_reaction_emoji DataGitlabProjectIssues#not_my_reaction_emoji}
        :param order_by: Return issues ordered by. Valid values are ``created_at``, ``updated_at``, ``priority``, ``due_date``, ``relative_position``, ``label_priority``, ``milestone_due``, ``popularity``, ``weight``. Default is created_at. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#order_by DataGitlabProjectIssues#order_by}
        :param scope: Return issues for the given scope. Valid values are ``created_by_me``, ``assigned_to_me``, ``all``. Defaults to all. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#scope DataGitlabProjectIssues#scope}
        :param search: Search project issues against their title and description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#search DataGitlabProjectIssues#search}
        :param sort: Return issues sorted in asc or desc order. Default is desc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#sort DataGitlabProjectIssues#sort}
        :param updated_after: Return issues updated on or after the given time. Expected in ISO 8601 format (2019-03-15T08:00:00Z). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#updated_after DataGitlabProjectIssues#updated_after}
        :param updated_before: Return issues updated on or before the given time. Expected in ISO 8601 format (2019-03-15T08:00:00Z). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#updated_before DataGitlabProjectIssues#updated_before}
        :param weight: Return issues with the specified weight. None returns issues with no weight assigned. Any returns issues with a weight assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#weight DataGitlabProjectIssues#weight}
        :param with_labels_details: If true, the response returns more details for each label in labels field: :name, :color, :description, :description_html, :text_color. Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#with_labels_details DataGitlabProjectIssues#with_labels_details}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1a96398ce62aa091159f0e1111f7a42bb2bddd4b8218a23b443afce18b8909c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument assignee_id", value=assignee_id, expected_type=type_hints["assignee_id"])
            check_type(argname="argument assignee_username", value=assignee_username, expected_type=type_hints["assignee_username"])
            check_type(argname="argument author_id", value=author_id, expected_type=type_hints["author_id"])
            check_type(argname="argument confidential", value=confidential, expected_type=type_hints["confidential"])
            check_type(argname="argument created_after", value=created_after, expected_type=type_hints["created_after"])
            check_type(argname="argument created_before", value=created_before, expected_type=type_hints["created_before"])
            check_type(argname="argument due_date", value=due_date, expected_type=type_hints["due_date"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument iids", value=iids, expected_type=type_hints["iids"])
            check_type(argname="argument issue_type", value=issue_type, expected_type=type_hints["issue_type"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument milestone", value=milestone, expected_type=type_hints["milestone"])
            check_type(argname="argument my_reaction_emoji", value=my_reaction_emoji, expected_type=type_hints["my_reaction_emoji"])
            check_type(argname="argument not_assignee_id", value=not_assignee_id, expected_type=type_hints["not_assignee_id"])
            check_type(argname="argument not_author_id", value=not_author_id, expected_type=type_hints["not_author_id"])
            check_type(argname="argument not_labels", value=not_labels, expected_type=type_hints["not_labels"])
            check_type(argname="argument not_milestone", value=not_milestone, expected_type=type_hints["not_milestone"])
            check_type(argname="argument not_my_reaction_emoji", value=not_my_reaction_emoji, expected_type=type_hints["not_my_reaction_emoji"])
            check_type(argname="argument order_by", value=order_by, expected_type=type_hints["order_by"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument search", value=search, expected_type=type_hints["search"])
            check_type(argname="argument sort", value=sort, expected_type=type_hints["sort"])
            check_type(argname="argument updated_after", value=updated_after, expected_type=type_hints["updated_after"])
            check_type(argname="argument updated_before", value=updated_before, expected_type=type_hints["updated_before"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            check_type(argname="argument with_labels_details", value=with_labels_details, expected_type=type_hints["with_labels_details"])
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
        if assignee_id is not None:
            self._values["assignee_id"] = assignee_id
        if assignee_username is not None:
            self._values["assignee_username"] = assignee_username
        if author_id is not None:
            self._values["author_id"] = author_id
        if confidential is not None:
            self._values["confidential"] = confidential
        if created_after is not None:
            self._values["created_after"] = created_after
        if created_before is not None:
            self._values["created_before"] = created_before
        if due_date is not None:
            self._values["due_date"] = due_date
        if id is not None:
            self._values["id"] = id
        if iids is not None:
            self._values["iids"] = iids
        if issue_type is not None:
            self._values["issue_type"] = issue_type
        if labels is not None:
            self._values["labels"] = labels
        if milestone is not None:
            self._values["milestone"] = milestone
        if my_reaction_emoji is not None:
            self._values["my_reaction_emoji"] = my_reaction_emoji
        if not_assignee_id is not None:
            self._values["not_assignee_id"] = not_assignee_id
        if not_author_id is not None:
            self._values["not_author_id"] = not_author_id
        if not_labels is not None:
            self._values["not_labels"] = not_labels
        if not_milestone is not None:
            self._values["not_milestone"] = not_milestone
        if not_my_reaction_emoji is not None:
            self._values["not_my_reaction_emoji"] = not_my_reaction_emoji
        if order_by is not None:
            self._values["order_by"] = order_by
        if scope is not None:
            self._values["scope"] = scope
        if search is not None:
            self._values["search"] = search
        if sort is not None:
            self._values["sort"] = sort
        if updated_after is not None:
            self._values["updated_after"] = updated_after
        if updated_before is not None:
            self._values["updated_before"] = updated_before
        if weight is not None:
            self._values["weight"] = weight
        if with_labels_details is not None:
            self._values["with_labels_details"] = with_labels_details

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
        '''The name or id of the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#project DataGitlabProjectIssues#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def assignee_id(self) -> typing.Optional[jsii.Number]:
        '''Return issues assigned to the given user id.

        Mutually exclusive with assignee_username. None returns unassigned issues. Any returns issues with an assignee.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#assignee_id DataGitlabProjectIssues#assignee_id}
        '''
        result = self._values.get("assignee_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def assignee_username(self) -> typing.Optional[builtins.str]:
        '''Return issues assigned to the given username.

        Similar to assignee_id and mutually exclusive with assignee_id. In GitLab CE, the assignee_username array should only contain a single value. Otherwise, an invalid parameter error is returned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#assignee_username DataGitlabProjectIssues#assignee_username}
        '''
        result = self._values.get("assignee_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def author_id(self) -> typing.Optional[jsii.Number]:
        '''Return issues created by the given user id. Combine with scope=all or scope=assigned_to_me.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#author_id DataGitlabProjectIssues#author_id}
        '''
        result = self._values.get("author_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def confidential(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Filter confidential or public issues.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#confidential DataGitlabProjectIssues#confidential}
        '''
        result = self._values.get("confidential")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def created_after(self) -> typing.Optional[builtins.str]:
        '''Return issues created on or after the given time. Expected in ISO 8601 format (2019-03-15T08:00:00Z).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#created_after DataGitlabProjectIssues#created_after}
        '''
        result = self._values.get("created_after")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def created_before(self) -> typing.Optional[builtins.str]:
        '''Return issues created on or before the given time. Expected in ISO 8601 format (2019-03-15T08:00:00Z).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#created_before DataGitlabProjectIssues#created_before}
        '''
        result = self._values.get("created_before")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def due_date(self) -> typing.Optional[builtins.str]:
        '''Return issues that have no due date, are overdue, or whose due date is this week, this month, or between two weeks ago and next month.

        Accepts: 0 (no due date), any, today, tomorrow, overdue, week, month, next_month_and_previous_two_weeks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#due_date DataGitlabProjectIssues#due_date}
        '''
        result = self._values.get("due_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#id DataGitlabProjectIssues#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iids(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Return only the issues having the given iid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#iids DataGitlabProjectIssues#iids}
        '''
        result = self._values.get("iids")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def issue_type(self) -> typing.Optional[builtins.str]:
        '''Filter to a given type of issue. Valid values are [issue incident test_case].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#issue_type DataGitlabProjectIssues#issue_type}
        '''
        result = self._values.get("issue_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Return issues with labels.

        Issues must have all labels to be returned. None lists all issues with no labels. Any lists all issues with at least one label. No+Label (Deprecated) lists all issues with no labels. Predefined names are case-insensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#labels DataGitlabProjectIssues#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def milestone(self) -> typing.Optional[builtins.str]:
        '''The milestone title. None lists all issues with no milestone. Any lists all issues that have an assigned milestone.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#milestone DataGitlabProjectIssues#milestone}
        '''
        result = self._values.get("milestone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def my_reaction_emoji(self) -> typing.Optional[builtins.str]:
        '''Return issues reacted by the authenticated user by the given emoji.

        None returns issues not given a reaction. Any returns issues given at least one reaction.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#my_reaction_emoji DataGitlabProjectIssues#my_reaction_emoji}
        '''
        result = self._values.get("my_reaction_emoji")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def not_assignee_id(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Return issues that do not match the assignee id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#not_assignee_id DataGitlabProjectIssues#not_assignee_id}
        '''
        result = self._values.get("not_assignee_id")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def not_author_id(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Return issues that do not match the author id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#not_author_id DataGitlabProjectIssues#not_author_id}
        '''
        result = self._values.get("not_author_id")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def not_labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Return issues that do not match the labels.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#not_labels DataGitlabProjectIssues#not_labels}
        '''
        result = self._values.get("not_labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def not_milestone(self) -> typing.Optional[builtins.str]:
        '''Return issues that do not match the milestone.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#not_milestone DataGitlabProjectIssues#not_milestone}
        '''
        result = self._values.get("not_milestone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def not_my_reaction_emoji(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Return issues not reacted by the authenticated user by the given emoji.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#not_my_reaction_emoji DataGitlabProjectIssues#not_my_reaction_emoji}
        '''
        result = self._values.get("not_my_reaction_emoji")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def order_by(self) -> typing.Optional[builtins.str]:
        '''Return issues ordered by. Valid values are ``created_at``, ``updated_at``, ``priority``, ``due_date``, ``relative_position``, ``label_priority``, ``milestone_due``, ``popularity``, ``weight``. Default is created_at.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#order_by DataGitlabProjectIssues#order_by}
        '''
        result = self._values.get("order_by")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''Return issues for the given scope. Valid values are ``created_by_me``, ``assigned_to_me``, ``all``. Defaults to all.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#scope DataGitlabProjectIssues#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def search(self) -> typing.Optional[builtins.str]:
        '''Search project issues against their title and description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#search DataGitlabProjectIssues#search}
        '''
        result = self._values.get("search")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sort(self) -> typing.Optional[builtins.str]:
        '''Return issues sorted in asc or desc order. Default is desc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#sort DataGitlabProjectIssues#sort}
        '''
        result = self._values.get("sort")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def updated_after(self) -> typing.Optional[builtins.str]:
        '''Return issues updated on or after the given time. Expected in ISO 8601 format (2019-03-15T08:00:00Z).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#updated_after DataGitlabProjectIssues#updated_after}
        '''
        result = self._values.get("updated_after")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def updated_before(self) -> typing.Optional[builtins.str]:
        '''Return issues updated on or before the given time. Expected in ISO 8601 format (2019-03-15T08:00:00Z).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#updated_before DataGitlabProjectIssues#updated_before}
        '''
        result = self._values.get("updated_before")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''Return issues with the specified weight.

        None returns issues with no weight assigned. Any returns issues with a weight assigned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#weight DataGitlabProjectIssues#weight}
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def with_labels_details(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the response returns more details for each label in labels field: :name, :color, :description, :description_html, :text_color.

        Default is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/project_issues#with_labels_details DataGitlabProjectIssues#with_labels_details}
        '''
        result = self._values.get("with_labels_details")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGitlabProjectIssuesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjectIssues.DataGitlabProjectIssuesIssues",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGitlabProjectIssuesIssues:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGitlabProjectIssuesIssues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGitlabProjectIssuesIssuesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjectIssues.DataGitlabProjectIssuesIssuesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcdad6694df690467f280ee8b652d3b7fb0c1283a1a6d4e3b498297c1f994674)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataGitlabProjectIssuesIssuesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65913044843c946997b8bb6744b0bd21f80b8158678cfe80120f8260dc33a464)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGitlabProjectIssuesIssuesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee965e03725a229eeef6fa1906f1e703eacdfac52886e39799dba029fe87186)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80a7a18f1f36c3cfe25ed83f2f2e4733422f90df92d1f617c221b20321989187)
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
            type_hints = typing.get_type_hints(_typecheckingstub__469d0ef16457ad2320ff13432b88c7c3115ad0dcf5c62a745ba095bf1d32d85c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGitlabProjectIssuesIssuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjectIssues.DataGitlabProjectIssuesIssuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e3431fb1db8e7734b44efed2b0dc7b9fc7dc9851b7f37f1bde2ec0220cb2195)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="assigneeIds")
    def assignee_ids(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "assigneeIds"))

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
    @jsii.member(jsii_name="confidential")
    def confidential(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "confidential"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="discussionLocked")
    def discussion_locked(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "discussionLocked"))

    @builtins.property
    @jsii.member(jsii_name="discussionToResolve")
    def discussion_to_resolve(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "discussionToResolve"))

    @builtins.property
    @jsii.member(jsii_name="downvotes")
    def downvotes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "downvotes"))

    @builtins.property
    @jsii.member(jsii_name="dueDate")
    def due_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dueDate"))

    @builtins.property
    @jsii.member(jsii_name="epicId")
    def epic_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "epicId"))

    @builtins.property
    @jsii.member(jsii_name="epicIssueId")
    def epic_issue_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "epicIssueId"))

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
    @jsii.member(jsii_name="iid")
    def iid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "iid"))

    @builtins.property
    @jsii.member(jsii_name="issueId")
    def issue_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "issueId"))

    @builtins.property
    @jsii.member(jsii_name="issueLinkId")
    def issue_link_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "issueLinkId"))

    @builtins.property
    @jsii.member(jsii_name="issueType")
    def issue_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issueType"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="links")
    def links(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "links"))

    @builtins.property
    @jsii.member(jsii_name="mergeRequestsCount")
    def merge_requests_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mergeRequestsCount"))

    @builtins.property
    @jsii.member(jsii_name="mergeRequestToResolveDiscussionsOf")
    def merge_request_to_resolve_discussions_of(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mergeRequestToResolveDiscussionsOf"))

    @builtins.property
    @jsii.member(jsii_name="milestoneId")
    def milestone_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "milestoneId"))

    @builtins.property
    @jsii.member(jsii_name="movedToId")
    def moved_to_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "movedToId"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @builtins.property
    @jsii.member(jsii_name="references")
    def references(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "references"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="subscribed")
    def subscribed(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "subscribed"))

    @builtins.property
    @jsii.member(jsii_name="taskCompletionStatus")
    def task_completion_status(
        self,
    ) -> "DataGitlabProjectIssuesIssuesTaskCompletionStatusList":
        return typing.cast("DataGitlabProjectIssuesIssuesTaskCompletionStatusList", jsii.get(self, "taskCompletionStatus"))

    @builtins.property
    @jsii.member(jsii_name="timeEstimate")
    def time_estimate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeEstimate"))

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @builtins.property
    @jsii.member(jsii_name="totalTimeSpent")
    def total_time_spent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalTimeSpent"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

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
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataGitlabProjectIssuesIssues]:
        return typing.cast(typing.Optional[DataGitlabProjectIssuesIssues], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGitlabProjectIssuesIssues],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f05018a85a9b62439b99039217f9b2f616e8983f7541e98f3c954cb340b27d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjectIssues.DataGitlabProjectIssuesIssuesTaskCompletionStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGitlabProjectIssuesIssuesTaskCompletionStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGitlabProjectIssuesIssuesTaskCompletionStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGitlabProjectIssuesIssuesTaskCompletionStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjectIssues.DataGitlabProjectIssuesIssuesTaskCompletionStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__083ebf8dcacc4a4827d3c39f6e648f83263cc6feac6a8f51edaec2ac74a29bff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGitlabProjectIssuesIssuesTaskCompletionStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0746a7030b30c19cc6d4b43282a43f58897e695893a6c36fed62e56958ab23b0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGitlabProjectIssuesIssuesTaskCompletionStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a924bc5f154a6affa1bed99f3ac64c8518689e9a5772271e7171b6450d4a67c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a9a651aecf4694f61e6d3ce28a1c00cc922df741e3f2db87ded49c061512d46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ac0641a120c4ed5d82221a171291f0f86366e2bd8c3a0474dd4560c372869b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGitlabProjectIssuesIssuesTaskCompletionStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjectIssues.DataGitlabProjectIssuesIssuesTaskCompletionStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a81b0bd3a4e8c370f11ee6759717e3d36136391afe29a8808e2b4e47473c865)
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
    def internal_value(
        self,
    ) -> typing.Optional[DataGitlabProjectIssuesIssuesTaskCompletionStatus]:
        return typing.cast(typing.Optional[DataGitlabProjectIssuesIssuesTaskCompletionStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGitlabProjectIssuesIssuesTaskCompletionStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33acea89c5344a9108a93c22fae8e595f8dfe75ad949a8b65a31bcdc11f1796c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataGitlabProjectIssues",
    "DataGitlabProjectIssuesConfig",
    "DataGitlabProjectIssuesIssues",
    "DataGitlabProjectIssuesIssuesList",
    "DataGitlabProjectIssuesIssuesOutputReference",
    "DataGitlabProjectIssuesIssuesTaskCompletionStatus",
    "DataGitlabProjectIssuesIssuesTaskCompletionStatusList",
    "DataGitlabProjectIssuesIssuesTaskCompletionStatusOutputReference",
]

publication.publish()

def _typecheckingstub__4172e0413e98c79659f7ad96c8b9719724c5bb35fffa3c8c740e6baed4978222(
    scope_: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    project: builtins.str,
    assignee_id: typing.Optional[jsii.Number] = None,
    assignee_username: typing.Optional[builtins.str] = None,
    author_id: typing.Optional[jsii.Number] = None,
    confidential: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    created_after: typing.Optional[builtins.str] = None,
    created_before: typing.Optional[builtins.str] = None,
    due_date: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    iids: typing.Optional[typing.Sequence[jsii.Number]] = None,
    issue_type: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    milestone: typing.Optional[builtins.str] = None,
    my_reaction_emoji: typing.Optional[builtins.str] = None,
    not_assignee_id: typing.Optional[typing.Sequence[jsii.Number]] = None,
    not_author_id: typing.Optional[typing.Sequence[jsii.Number]] = None,
    not_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_milestone: typing.Optional[builtins.str] = None,
    not_my_reaction_emoji: typing.Optional[typing.Sequence[builtins.str]] = None,
    order_by: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    search: typing.Optional[builtins.str] = None,
    sort: typing.Optional[builtins.str] = None,
    updated_after: typing.Optional[builtins.str] = None,
    updated_before: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
    with_labels_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__d17b5123c0726bcdaa6fcfc90e8cb3b9eb6ebb040d8b0e1b4a3629e64ba80b00(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1fdeee3fb1fe348233ab6120dca7354b3c525e11cf7e07ee5cddc8f243c20ef(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__214ba90b0e34593f563bba5758a0e0e7ff90910aab79889da2541ccfd6a9dee6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415ebea6b263c39e8d6ba8ee71a42c95a3d907ce2062d7cfc81b3acc49e9e493(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a7bb5f3e4a5d6807d5846f3893e9c55c0689e176c23db8b6523d450cc9d272c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b8636690c5d55687df9cb25d081c92f664896b7684e7089d57a543c05ec9082(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__707934e2fb1023ac3f316bc4d67cc40d6c1cc40e3415fb462d7b5ad2a99e1e80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49f56adc8b64674edb57c43e0f417d49a7c736940332d54a28dae030e852a3ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b08edead9e5b40c2eda95f2832200a046e6e1d0ff7b770e9617fe6d4623411(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec0460fe1a22e8c5982458b7402416cfc8dc41b44a9a8f8864b7b22eccda7268(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed5f4040d0f339d701664b3ac601ed9d8c5fea0d8f74c003f11219c9d252a316(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3137278c3de848531d17ba1b0fcab4c233ba2a99553e053873598c16a4a0234(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8eb33a2a76ae1202706c712cc215d6a803baa2d62a4d4b9ae6f4d2d5fe04033(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d1d9886a864f5835e2f34b561cc99323f1e29a04e402d19eebdaa7d30c61eed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ca2892d281b27e69ddd9921d404a6d7d6efce9a47130500e63e1ea723b4e6d(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac85bfbdbb025fbb9c6a4ef5d8324704419e873400a24e660934d5ec9f5e2d1(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9142d465a0787957266dda5bcf56a561827239aef85d21351787431b73447a3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb24071ea865dc14885266a8d2e85730a68d58c54730b325ad7275dac523491(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f95b7c07b7733587db27c9d2d320ef29255f9a446c420fd4015161e1cd2516(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e83c34e7aa0c704c65406d2cfb55b9bfeb2e9d3ebd54d5da5811694d30ed800(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c491e355f56c376490c68b9ead7e0a388f0e8486bf01756909a7ed48fd358e25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4c6de42f35145cc66538cb2970d02ce1a0225d786bb4251f46f765bf0332ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54602a2b6df509384fef35a139ed73f4df894470dce80650bdec866605a89af0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55abf7f6e8ecb23590a4407c63cde82c84d9d0ca85b9ef76aee0a0839f8b4c6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3974a80789d1fb233a7907150ee320bd9f53ecf6c649bdc5081fe1851e04a98e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e552e48e595a7068e79345684bedd34525a1ba8e740772198a2fb4295a933613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cebb289d046b9d80889a9c8f4c4f0aca3c5c88480d059f82bb0888e02454a6d6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37a717584cdea7a5a59619f8f3462a4afc24ed472c8a67d3bc27f85e91bd665(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1a96398ce62aa091159f0e1111f7a42bb2bddd4b8218a23b443afce18b8909c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: builtins.str,
    assignee_id: typing.Optional[jsii.Number] = None,
    assignee_username: typing.Optional[builtins.str] = None,
    author_id: typing.Optional[jsii.Number] = None,
    confidential: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    created_after: typing.Optional[builtins.str] = None,
    created_before: typing.Optional[builtins.str] = None,
    due_date: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    iids: typing.Optional[typing.Sequence[jsii.Number]] = None,
    issue_type: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    milestone: typing.Optional[builtins.str] = None,
    my_reaction_emoji: typing.Optional[builtins.str] = None,
    not_assignee_id: typing.Optional[typing.Sequence[jsii.Number]] = None,
    not_author_id: typing.Optional[typing.Sequence[jsii.Number]] = None,
    not_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_milestone: typing.Optional[builtins.str] = None,
    not_my_reaction_emoji: typing.Optional[typing.Sequence[builtins.str]] = None,
    order_by: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    search: typing.Optional[builtins.str] = None,
    sort: typing.Optional[builtins.str] = None,
    updated_after: typing.Optional[builtins.str] = None,
    updated_before: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
    with_labels_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcdad6694df690467f280ee8b652d3b7fb0c1283a1a6d4e3b498297c1f994674(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65913044843c946997b8bb6744b0bd21f80b8158678cfe80120f8260dc33a464(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee965e03725a229eeef6fa1906f1e703eacdfac52886e39799dba029fe87186(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a7a18f1f36c3cfe25ed83f2f2e4733422f90df92d1f617c221b20321989187(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__469d0ef16457ad2320ff13432b88c7c3115ad0dcf5c62a745ba095bf1d32d85c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e3431fb1db8e7734b44efed2b0dc7b9fc7dc9851b7f37f1bde2ec0220cb2195(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f05018a85a9b62439b99039217f9b2f616e8983f7541e98f3c954cb340b27d4(
    value: typing.Optional[DataGitlabProjectIssuesIssues],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083ebf8dcacc4a4827d3c39f6e648f83263cc6feac6a8f51edaec2ac74a29bff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0746a7030b30c19cc6d4b43282a43f58897e695893a6c36fed62e56958ab23b0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a924bc5f154a6affa1bed99f3ac64c8518689e9a5772271e7171b6450d4a67c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a9a651aecf4694f61e6d3ce28a1c00cc922df741e3f2db87ded49c061512d46(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac0641a120c4ed5d82221a171291f0f86366e2bd8c3a0474dd4560c372869b9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a81b0bd3a4e8c370f11ee6759717e3d36136391afe29a8808e2b4e47473c865(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33acea89c5344a9108a93c22fae8e595f8dfe75ad949a8b65a31bcdc11f1796c(
    value: typing.Optional[DataGitlabProjectIssuesIssuesTaskCompletionStatus],
) -> None:
    """Type checking stubs"""
    pass
