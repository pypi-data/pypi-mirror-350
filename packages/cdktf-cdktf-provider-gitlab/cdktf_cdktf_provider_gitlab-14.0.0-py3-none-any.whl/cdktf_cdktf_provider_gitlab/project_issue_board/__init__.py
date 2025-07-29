r'''
# `gitlab_project_issue_board`

Refer to the Terraform Registry for docs: [`gitlab_project_issue_board`](https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board).
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


class ProjectIssueBoard(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.projectIssueBoard.ProjectIssueBoard",
):
    '''Represents a {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board gitlab_project_issue_board}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        project: builtins.str,
        assignee_id: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        lists: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProjectIssueBoardLists", typing.Dict[builtins.str, typing.Any]]]]] = None,
        milestone_id: typing.Optional[jsii.Number] = None,
        weight: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board gitlab_project_issue_board} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the board. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#name ProjectIssueBoard#name}
        :param project: The ID or full path of the project maintained by the authenticated user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#project ProjectIssueBoard#project}
        :param assignee_id: The assignee the board should be scoped to. Requires a GitLab EE license. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#assignee_id ProjectIssueBoard#assignee_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#id ProjectIssueBoard#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The list of label names which the board should be scoped to. Requires a GitLab EE license. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#labels ProjectIssueBoard#labels}
        :param lists: lists block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#lists ProjectIssueBoard#lists}
        :param milestone_id: The milestone the board should be scoped to. Requires a GitLab EE license. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#milestone_id ProjectIssueBoard#milestone_id}
        :param weight: The weight range from 0 to 9, to which the board should be scoped to. Requires a GitLab EE license. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#weight ProjectIssueBoard#weight}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb5e5701210055713ba63b1c0a9e94e1020bcc29fb66230f45122da5c90aded)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ProjectIssueBoardConfig(
            name=name,
            project=project,
            assignee_id=assignee_id,
            id=id,
            labels=labels,
            lists=lists,
            milestone_id=milestone_id,
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
        '''Generates CDKTF code for importing a ProjectIssueBoard resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ProjectIssueBoard to import.
        :param import_from_id: The id of the existing ProjectIssueBoard that should be imported. Refer to the {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ProjectIssueBoard to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__116e0e1aa372601788694185465b28c18bb3b22d7fc306bcd8636624929e78b7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLists")
    def put_lists(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProjectIssueBoardLists", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a3bb9a2c18f8b865d522873fe3306acca65444dcfebed5cef5f199862d1960e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLists", [value]))

    @jsii.member(jsii_name="resetAssigneeId")
    def reset_assignee_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssigneeId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLists")
    def reset_lists(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLists", []))

    @jsii.member(jsii_name="resetMilestoneId")
    def reset_milestone_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMilestoneId", []))

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
    @jsii.member(jsii_name="lists")
    def lists(self) -> "ProjectIssueBoardListsList":
        return typing.cast("ProjectIssueBoardListsList", jsii.get(self, "lists"))

    @builtins.property
    @jsii.member(jsii_name="assigneeIdInput")
    def assignee_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "assigneeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="listsInput")
    def lists_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectIssueBoardLists"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectIssueBoardLists"]]], jsii.get(self, "listsInput"))

    @builtins.property
    @jsii.member(jsii_name="milestoneIdInput")
    def milestone_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "milestoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="assigneeId")
    def assignee_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "assigneeId"))

    @assignee_id.setter
    def assignee_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1616537eef489b089c22fa95a23895ae2c8c9184e953668373b4f40f0526218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assigneeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0737328675170303e94b26cd8c5663c3ddd28ff7684a5db511659ed03e499366)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0623e5e04d0a3e8cfa1e12318af7d92a62c28d9aaa0c12ed67c6f0a9867dd1a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="milestoneId")
    def milestone_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "milestoneId"))

    @milestone_id.setter
    def milestone_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12baa917f76ac08b71b376912763dbe4bf5f4bbf29d9ce5171019a858b03c96d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "milestoneId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f25c2292d0f0468bbde18f5473addf20e49a9b1033ae0c622487347bb4445178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4da77a2676df1cab82638635e1896a44d8262c9d70aa77fa535f2b17da94121c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__372f64ab25ab60d02fc22d6eb2118450cfd76458e1f6187e95308a35cbf023ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.projectIssueBoard.ProjectIssueBoardConfig",
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
        "project": "project",
        "assignee_id": "assigneeId",
        "id": "id",
        "labels": "labels",
        "lists": "lists",
        "milestone_id": "milestoneId",
        "weight": "weight",
    },
)
class ProjectIssueBoardConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        project: builtins.str,
        assignee_id: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        lists: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProjectIssueBoardLists", typing.Dict[builtins.str, typing.Any]]]]] = None,
        milestone_id: typing.Optional[jsii.Number] = None,
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
        :param name: The name of the board. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#name ProjectIssueBoard#name}
        :param project: The ID or full path of the project maintained by the authenticated user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#project ProjectIssueBoard#project}
        :param assignee_id: The assignee the board should be scoped to. Requires a GitLab EE license. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#assignee_id ProjectIssueBoard#assignee_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#id ProjectIssueBoard#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The list of label names which the board should be scoped to. Requires a GitLab EE license. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#labels ProjectIssueBoard#labels}
        :param lists: lists block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#lists ProjectIssueBoard#lists}
        :param milestone_id: The milestone the board should be scoped to. Requires a GitLab EE license. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#milestone_id ProjectIssueBoard#milestone_id}
        :param weight: The weight range from 0 to 9, to which the board should be scoped to. Requires a GitLab EE license. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#weight ProjectIssueBoard#weight}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23086532835d53f1a5b4f7822c1bd687983122142fa3c1f343bd337f3a46f340)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument assignee_id", value=assignee_id, expected_type=type_hints["assignee_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument lists", value=lists, expected_type=type_hints["lists"])
            check_type(argname="argument milestone_id", value=milestone_id, expected_type=type_hints["milestone_id"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if lists is not None:
            self._values["lists"] = lists
        if milestone_id is not None:
            self._values["milestone_id"] = milestone_id
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
    def name(self) -> builtins.str:
        '''The name of the board.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#name ProjectIssueBoard#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''The ID or full path of the project maintained by the authenticated user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#project ProjectIssueBoard#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def assignee_id(self) -> typing.Optional[jsii.Number]:
        '''The assignee the board should be scoped to. Requires a GitLab EE license.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#assignee_id ProjectIssueBoard#assignee_id}
        '''
        result = self._values.get("assignee_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#id ProjectIssueBoard#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of label names which the board should be scoped to. Requires a GitLab EE license.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#labels ProjectIssueBoard#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def lists(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectIssueBoardLists"]]]:
        '''lists block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#lists ProjectIssueBoard#lists}
        '''
        result = self._values.get("lists")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectIssueBoardLists"]]], result)

    @builtins.property
    def milestone_id(self) -> typing.Optional[jsii.Number]:
        '''The milestone the board should be scoped to. Requires a GitLab EE license.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#milestone_id ProjectIssueBoard#milestone_id}
        '''
        result = self._values.get("milestone_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''The weight range from 0 to 9, to which the board should be scoped to.

        Requires a GitLab EE license.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#weight ProjectIssueBoard#weight}
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectIssueBoardConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.projectIssueBoard.ProjectIssueBoardLists",
    jsii_struct_bases=[],
    name_mapping={
        "assignee_id": "assigneeId",
        "iteration_id": "iterationId",
        "label_id": "labelId",
        "milestone_id": "milestoneId",
    },
)
class ProjectIssueBoardLists:
    def __init__(
        self,
        *,
        assignee_id: typing.Optional[jsii.Number] = None,
        iteration_id: typing.Optional[jsii.Number] = None,
        label_id: typing.Optional[jsii.Number] = None,
        milestone_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param assignee_id: The ID of the assignee the list should be scoped to. Requires a GitLab EE license. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#assignee_id ProjectIssueBoard#assignee_id}
        :param iteration_id: The ID of the iteration the list should be scoped to. Requires a GitLab EE license. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#iteration_id ProjectIssueBoard#iteration_id}
        :param label_id: The ID of the label the list should be scoped to. Requires a GitLab EE license. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#label_id ProjectIssueBoard#label_id}
        :param milestone_id: The ID of the milestone the list should be scoped to. Requires a GitLab EE license. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#milestone_id ProjectIssueBoard#milestone_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04f4389c5fb3694b7ba2b9dbb27a39ae762c9d7b238dd60161488363adee9853)
            check_type(argname="argument assignee_id", value=assignee_id, expected_type=type_hints["assignee_id"])
            check_type(argname="argument iteration_id", value=iteration_id, expected_type=type_hints["iteration_id"])
            check_type(argname="argument label_id", value=label_id, expected_type=type_hints["label_id"])
            check_type(argname="argument milestone_id", value=milestone_id, expected_type=type_hints["milestone_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assignee_id is not None:
            self._values["assignee_id"] = assignee_id
        if iteration_id is not None:
            self._values["iteration_id"] = iteration_id
        if label_id is not None:
            self._values["label_id"] = label_id
        if milestone_id is not None:
            self._values["milestone_id"] = milestone_id

    @builtins.property
    def assignee_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of the assignee the list should be scoped to. Requires a GitLab EE license.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#assignee_id ProjectIssueBoard#assignee_id}
        '''
        result = self._values.get("assignee_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def iteration_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of the iteration the list should be scoped to. Requires a GitLab EE license.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#iteration_id ProjectIssueBoard#iteration_id}
        '''
        result = self._values.get("iteration_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def label_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of the label the list should be scoped to. Requires a GitLab EE license.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#label_id ProjectIssueBoard#label_id}
        '''
        result = self._values.get("label_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def milestone_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of the milestone the list should be scoped to. Requires a GitLab EE license.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project_issue_board#milestone_id ProjectIssueBoard#milestone_id}
        '''
        result = self._values.get("milestone_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectIssueBoardLists(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectIssueBoardListsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.projectIssueBoard.ProjectIssueBoardListsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d93202e8342634ef51ff02b0bb50fa220aef0ed14961e2b5569ad71e4f86bc8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ProjectIssueBoardListsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64432d9479aeb6eefc761d711d0a8c322194ff084fdb4903f2db25bd0d50ca4d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProjectIssueBoardListsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b24d0e05ecd1d4e65140447b974dfd2f83c51f0d67a285ea8514d9257917dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6d9c8df5a323f90de5679f445cddcd8006b0791ba84b23395934d690596e8f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82563ed3b222784fb42405a29b148f73bb266fc9adb93a44121b08117af7c20b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectIssueBoardLists]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectIssueBoardLists]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectIssueBoardLists]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e2e30029e5f0e51a8a85214bf04518a963e1bf23ae8bee9bdfec331d499e4a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ProjectIssueBoardListsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.projectIssueBoard.ProjectIssueBoardListsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2303eff9b4aaea57be98227b3004fb0c59ad5e7e9b82cf4d048d00ae6832f32)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAssigneeId")
    def reset_assignee_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssigneeId", []))

    @jsii.member(jsii_name="resetIterationId")
    def reset_iteration_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIterationId", []))

    @jsii.member(jsii_name="resetLabelId")
    def reset_label_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabelId", []))

    @jsii.member(jsii_name="resetMilestoneId")
    def reset_milestone_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMilestoneId", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="position")
    def position(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "position"))

    @builtins.property
    @jsii.member(jsii_name="assigneeIdInput")
    def assignee_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "assigneeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="iterationIdInput")
    def iteration_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "iterationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="labelIdInput")
    def label_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "labelIdInput"))

    @builtins.property
    @jsii.member(jsii_name="milestoneIdInput")
    def milestone_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "milestoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="assigneeId")
    def assignee_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "assigneeId"))

    @assignee_id.setter
    def assignee_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c4eb995cb87e5a2308be81a631e0026f1b8f2b2b69a5cf5a273611f473d9ad5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assigneeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iterationId")
    def iteration_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "iterationId"))

    @iteration_id.setter
    def iteration_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f8974cc9e3e31a9c28b81326ee2063d57f5648133294d98566287a2b4c0094f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iterationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labelId")
    def label_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "labelId"))

    @label_id.setter
    def label_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc984e064481af3f23fa850742537215d8ad96130d05933216d1117e1666a755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labelId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="milestoneId")
    def milestone_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "milestoneId"))

    @milestone_id.setter
    def milestone_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f7f258c0d1990ea00fcd25dceff7dc4e44a9a9e87dcb99160dc280d90027666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "milestoneId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectIssueBoardLists]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectIssueBoardLists]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectIssueBoardLists]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aa7f103517bac6010cd808ebf6c42fbb66d21a8afb0863db77dcfbb432b6db1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ProjectIssueBoard",
    "ProjectIssueBoardConfig",
    "ProjectIssueBoardLists",
    "ProjectIssueBoardListsList",
    "ProjectIssueBoardListsOutputReference",
]

publication.publish()

def _typecheckingstub__ddb5e5701210055713ba63b1c0a9e94e1020bcc29fb66230f45122da5c90aded(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    project: builtins.str,
    assignee_id: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    lists: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectIssueBoardLists, typing.Dict[builtins.str, typing.Any]]]]] = None,
    milestone_id: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__116e0e1aa372601788694185465b28c18bb3b22d7fc306bcd8636624929e78b7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a3bb9a2c18f8b865d522873fe3306acca65444dcfebed5cef5f199862d1960e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectIssueBoardLists, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1616537eef489b089c22fa95a23895ae2c8c9184e953668373b4f40f0526218(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0737328675170303e94b26cd8c5663c3ddd28ff7684a5db511659ed03e499366(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0623e5e04d0a3e8cfa1e12318af7d92a62c28d9aaa0c12ed67c6f0a9867dd1a3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12baa917f76ac08b71b376912763dbe4bf5f4bbf29d9ce5171019a858b03c96d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25c2292d0f0468bbde18f5473addf20e49a9b1033ae0c622487347bb4445178(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4da77a2676df1cab82638635e1896a44d8262c9d70aa77fa535f2b17da94121c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__372f64ab25ab60d02fc22d6eb2118450cfd76458e1f6187e95308a35cbf023ce(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23086532835d53f1a5b4f7822c1bd687983122142fa3c1f343bd337f3a46f340(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    project: builtins.str,
    assignee_id: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    lists: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectIssueBoardLists, typing.Dict[builtins.str, typing.Any]]]]] = None,
    milestone_id: typing.Optional[jsii.Number] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f4389c5fb3694b7ba2b9dbb27a39ae762c9d7b238dd60161488363adee9853(
    *,
    assignee_id: typing.Optional[jsii.Number] = None,
    iteration_id: typing.Optional[jsii.Number] = None,
    label_id: typing.Optional[jsii.Number] = None,
    milestone_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d93202e8342634ef51ff02b0bb50fa220aef0ed14961e2b5569ad71e4f86bc8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64432d9479aeb6eefc761d711d0a8c322194ff084fdb4903f2db25bd0d50ca4d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b24d0e05ecd1d4e65140447b974dfd2f83c51f0d67a285ea8514d9257917dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d9c8df5a323f90de5679f445cddcd8006b0791ba84b23395934d690596e8f7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82563ed3b222784fb42405a29b148f73bb266fc9adb93a44121b08117af7c20b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e2e30029e5f0e51a8a85214bf04518a963e1bf23ae8bee9bdfec331d499e4a3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectIssueBoardLists]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2303eff9b4aaea57be98227b3004fb0c59ad5e7e9b82cf4d048d00ae6832f32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c4eb995cb87e5a2308be81a631e0026f1b8f2b2b69a5cf5a273611f473d9ad5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f8974cc9e3e31a9c28b81326ee2063d57f5648133294d98566287a2b4c0094f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc984e064481af3f23fa850742537215d8ad96130d05933216d1117e1666a755(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f7f258c0d1990ea00fcd25dceff7dc4e44a9a9e87dcb99160dc280d90027666(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aa7f103517bac6010cd808ebf6c42fbb66d21a8afb0863db77dcfbb432b6db1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectIssueBoardLists]],
) -> None:
    """Type checking stubs"""
    pass
