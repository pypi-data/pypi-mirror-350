r'''
# `gitlab_value_stream_analytics`

Refer to the Terraform Registry for docs: [`gitlab_value_stream_analytics`](https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics).
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


class ValueStreamAnalytics(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.valueStreamAnalytics.ValueStreamAnalytics",
):
    '''Represents a {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics gitlab_value_stream_analytics}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        stages: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ValueStreamAnalyticsStages", typing.Dict[builtins.str, typing.Any]]]],
        group_full_path: typing.Optional[builtins.str] = None,
        project_full_path: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics gitlab_value_stream_analytics} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the value stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#name ValueStreamAnalytics#name}
        :param stages: Stages of the value stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#stages ValueStreamAnalytics#stages}
        :param group_full_path: Full path of the group the value stream is created in. **One of ``group_full_path`` OR ``project_full_path`` is required.**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#group_full_path ValueStreamAnalytics#group_full_path}
        :param project_full_path: Full path of the project the value stream is created in. **One of ``group_full_path`` OR ``project_full_path`` is required.**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#project_full_path ValueStreamAnalytics#project_full_path}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57e0acd6111a09cfa2060076c6b0bc12ace64d3ecc8f0bf1b526258c89a56d61)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ValueStreamAnalyticsConfig(
            name=name,
            stages=stages,
            group_full_path=group_full_path,
            project_full_path=project_full_path,
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
        '''Generates CDKTF code for importing a ValueStreamAnalytics resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ValueStreamAnalytics to import.
        :param import_from_id: The id of the existing ValueStreamAnalytics that should be imported. Refer to the {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ValueStreamAnalytics to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e78ef38a0e9f3d86e1d03f8fc65b4b7129f6fa07271b532eb59ef58028e9aabf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putStages")
    def put_stages(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ValueStreamAnalyticsStages", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d190bbfbae0ca5e69eae687c69b7763c55653f1da2c63e633009aac84ef867c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStages", [value]))

    @jsii.member(jsii_name="resetGroupFullPath")
    def reset_group_full_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupFullPath", []))

    @jsii.member(jsii_name="resetProjectFullPath")
    def reset_project_full_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectFullPath", []))

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
    @jsii.member(jsii_name="stages")
    def stages(self) -> "ValueStreamAnalyticsStagesList":
        return typing.cast("ValueStreamAnalyticsStagesList", jsii.get(self, "stages"))

    @builtins.property
    @jsii.member(jsii_name="groupFullPathInput")
    def group_full_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupFullPathInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectFullPathInput")
    def project_full_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectFullPathInput"))

    @builtins.property
    @jsii.member(jsii_name="stagesInput")
    def stages_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ValueStreamAnalyticsStages"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ValueStreamAnalyticsStages"]]], jsii.get(self, "stagesInput"))

    @builtins.property
    @jsii.member(jsii_name="groupFullPath")
    def group_full_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupFullPath"))

    @group_full_path.setter
    def group_full_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c169090aac50e32d5cb886bb5c24d7077c563c32ed6f2969849664b2fbbcdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupFullPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95c61313779a6347221cb7630d3b421716d461f0dc152a49b6cd65e3244d7b55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectFullPath")
    def project_full_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectFullPath"))

    @project_full_path.setter
    def project_full_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61c8b206f40f0f99e377f8535f8c786cd92054d56c4688fdbc1a0720be5b45f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectFullPath", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.valueStreamAnalytics.ValueStreamAnalyticsConfig",
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
        "stages": "stages",
        "group_full_path": "groupFullPath",
        "project_full_path": "projectFullPath",
    },
)
class ValueStreamAnalyticsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        stages: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ValueStreamAnalyticsStages", typing.Dict[builtins.str, typing.Any]]]],
        group_full_path: typing.Optional[builtins.str] = None,
        project_full_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the value stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#name ValueStreamAnalytics#name}
        :param stages: Stages of the value stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#stages ValueStreamAnalytics#stages}
        :param group_full_path: Full path of the group the value stream is created in. **One of ``group_full_path`` OR ``project_full_path`` is required.**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#group_full_path ValueStreamAnalytics#group_full_path}
        :param project_full_path: Full path of the project the value stream is created in. **One of ``group_full_path`` OR ``project_full_path`` is required.**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#project_full_path ValueStreamAnalytics#project_full_path}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a074a05fa329189efe1af57541c86959699134568c83192d06420ff520898779)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument stages", value=stages, expected_type=type_hints["stages"])
            check_type(argname="argument group_full_path", value=group_full_path, expected_type=type_hints["group_full_path"])
            check_type(argname="argument project_full_path", value=project_full_path, expected_type=type_hints["project_full_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "stages": stages,
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
        if group_full_path is not None:
            self._values["group_full_path"] = group_full_path
        if project_full_path is not None:
            self._values["project_full_path"] = project_full_path

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
        '''The name of the value stream.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#name ValueStreamAnalytics#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stages(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ValueStreamAnalyticsStages"]]:
        '''Stages of the value stream.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#stages ValueStreamAnalytics#stages}
        '''
        result = self._values.get("stages")
        assert result is not None, "Required property 'stages' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ValueStreamAnalyticsStages"]], result)

    @builtins.property
    def group_full_path(self) -> typing.Optional[builtins.str]:
        '''Full path of the group the value stream is created in. **One of ``group_full_path`` OR ``project_full_path`` is required.**.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#group_full_path ValueStreamAnalytics#group_full_path}
        '''
        result = self._values.get("group_full_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_full_path(self) -> typing.Optional[builtins.str]:
        '''Full path of the project the value stream is created in. **One of ``group_full_path`` OR ``project_full_path`` is required.**.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#project_full_path ValueStreamAnalytics#project_full_path}
        '''
        result = self._values.get("project_full_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ValueStreamAnalyticsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.valueStreamAnalytics.ValueStreamAnalyticsStages",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "custom": "custom",
        "end_event_identifier": "endEventIdentifier",
        "end_event_label_id": "endEventLabelId",
        "hidden": "hidden",
        "start_event_identifier": "startEventIdentifier",
        "start_event_label_id": "startEventLabelId",
    },
)
class ValueStreamAnalyticsStages:
    def __init__(
        self,
        *,
        name: builtins.str,
        custom: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        end_event_identifier: typing.Optional[builtins.str] = None,
        end_event_label_id: typing.Optional[builtins.str] = None,
        hidden: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        start_event_identifier: typing.Optional[builtins.str] = None,
        start_event_label_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the value stream stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#name ValueStreamAnalytics#name}
        :param custom: Boolean whether the stage is customized. If false, it assigns a built-in default stage by name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#custom ValueStreamAnalytics#custom}
        :param end_event_identifier: End event identifier. Valid values are: ``CODE_STAGE_START``, ``ISSUE_CLOSED``, ``ISSUE_CREATED``, ``ISSUE_DEPLOYED_TO_PRODUCTION``, ``ISSUE_FIRST_ADDED_TO_BOARD``, ``ISSUE_FIRST_ADDED_TO_ITERATION``, ``ISSUE_FIRST_ASSIGNED_AT``, ``ISSUE_FIRST_ASSOCIATED_WITH_MILESTONE``, ``ISSUE_FIRST_MENTIONED_IN_COMMIT``, ``ISSUE_LABEL_ADDED``, ``ISSUE_LABEL_REMOVED``, ``ISSUE_LAST_EDITED``, ``ISSUE_STAGE_END``, ``MERGE_REQUEST_CLOSED``, ``MERGE_REQUEST_CREATED``, ``MERGE_REQUEST_FIRST_ASSIGNED_AT``, ``MERGE_REQUEST_FIRST_COMMIT_AT``, ``MERGE_REQUEST_FIRST_DEPLOYED_TO_PRODUCTION``, ``MERGE_REQUEST_LABEL_ADDED``, ``MERGE_REQUEST_LABEL_REMOVED``, ``MERGE_REQUEST_LAST_BUILD_FINISHED``, ``MERGE_REQUEST_LAST_BUILD_STARTED``, ``MERGE_REQUEST_LAST_EDITED``, ``MERGE_REQUEST_MERGED``, ``MERGE_REQUEST_REVIEWER_FIRST_ASSIGNED``, ``MERGE_REQUEST_PLAN_STAGE_START`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#end_event_identifier ValueStreamAnalytics#end_event_identifier}
        :param end_event_label_id: Label ID associated with the end event identifier. In the format of ``gid://gitlab/GroupLabel/<id>`` or ``gid://gitlab/ProjectLabel/<id>``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#end_event_label_id ValueStreamAnalytics#end_event_label_id}
        :param hidden: Boolean whether the stage is hidden, GitLab provided default stages are hidden by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#hidden ValueStreamAnalytics#hidden}
        :param start_event_identifier: Start event identifier. Valid values are: ``CODE_STAGE_START``, ``ISSUE_CLOSED``, ``ISSUE_CREATED``, ``ISSUE_DEPLOYED_TO_PRODUCTION``, ``ISSUE_FIRST_ADDED_TO_BOARD``, ``ISSUE_FIRST_ADDED_TO_ITERATION``, ``ISSUE_FIRST_ASSIGNED_AT``, ``ISSUE_FIRST_ASSOCIATED_WITH_MILESTONE``, ``ISSUE_FIRST_MENTIONED_IN_COMMIT``, ``ISSUE_LABEL_ADDED``, ``ISSUE_LABEL_REMOVED``, ``ISSUE_LAST_EDITED``, ``ISSUE_STAGE_END``, ``MERGE_REQUEST_CLOSED``, ``MERGE_REQUEST_CREATED``, ``MERGE_REQUEST_FIRST_ASSIGNED_AT``, ``MERGE_REQUEST_FIRST_COMMIT_AT``, ``MERGE_REQUEST_FIRST_DEPLOYED_TO_PRODUCTION``, ``MERGE_REQUEST_LABEL_ADDED``, ``MERGE_REQUEST_LABEL_REMOVED``, ``MERGE_REQUEST_LAST_BUILD_FINISHED``, ``MERGE_REQUEST_LAST_BUILD_STARTED``, ``MERGE_REQUEST_LAST_EDITED``, ``MERGE_REQUEST_MERGED``, ``MERGE_REQUEST_REVIEWER_FIRST_ASSIGNED``, ``MERGE_REQUEST_PLAN_STAGE_START`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#start_event_identifier ValueStreamAnalytics#start_event_identifier}
        :param start_event_label_id: Label ID associated with the start event identifier. In the format of ``gid://gitlab/GroupLabel/<id>`` or ``gid://gitlab/ProjectLabel/<id>``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#start_event_label_id ValueStreamAnalytics#start_event_label_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5a4723ed0f5e3dded5a24d39ef47c1cacccdd68139bf42d6529b281dcbd899b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument custom", value=custom, expected_type=type_hints["custom"])
            check_type(argname="argument end_event_identifier", value=end_event_identifier, expected_type=type_hints["end_event_identifier"])
            check_type(argname="argument end_event_label_id", value=end_event_label_id, expected_type=type_hints["end_event_label_id"])
            check_type(argname="argument hidden", value=hidden, expected_type=type_hints["hidden"])
            check_type(argname="argument start_event_identifier", value=start_event_identifier, expected_type=type_hints["start_event_identifier"])
            check_type(argname="argument start_event_label_id", value=start_event_label_id, expected_type=type_hints["start_event_label_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if custom is not None:
            self._values["custom"] = custom
        if end_event_identifier is not None:
            self._values["end_event_identifier"] = end_event_identifier
        if end_event_label_id is not None:
            self._values["end_event_label_id"] = end_event_label_id
        if hidden is not None:
            self._values["hidden"] = hidden
        if start_event_identifier is not None:
            self._values["start_event_identifier"] = start_event_identifier
        if start_event_label_id is not None:
            self._values["start_event_label_id"] = start_event_label_id

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the value stream stage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#name ValueStreamAnalytics#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean whether the stage is customized. If false, it assigns a built-in default stage by name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#custom ValueStreamAnalytics#custom}
        '''
        result = self._values.get("custom")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def end_event_identifier(self) -> typing.Optional[builtins.str]:
        '''End event identifier.

        Valid values are: ``CODE_STAGE_START``, ``ISSUE_CLOSED``, ``ISSUE_CREATED``, ``ISSUE_DEPLOYED_TO_PRODUCTION``, ``ISSUE_FIRST_ADDED_TO_BOARD``, ``ISSUE_FIRST_ADDED_TO_ITERATION``, ``ISSUE_FIRST_ASSIGNED_AT``, ``ISSUE_FIRST_ASSOCIATED_WITH_MILESTONE``, ``ISSUE_FIRST_MENTIONED_IN_COMMIT``, ``ISSUE_LABEL_ADDED``, ``ISSUE_LABEL_REMOVED``, ``ISSUE_LAST_EDITED``, ``ISSUE_STAGE_END``, ``MERGE_REQUEST_CLOSED``, ``MERGE_REQUEST_CREATED``, ``MERGE_REQUEST_FIRST_ASSIGNED_AT``, ``MERGE_REQUEST_FIRST_COMMIT_AT``, ``MERGE_REQUEST_FIRST_DEPLOYED_TO_PRODUCTION``, ``MERGE_REQUEST_LABEL_ADDED``, ``MERGE_REQUEST_LABEL_REMOVED``, ``MERGE_REQUEST_LAST_BUILD_FINISHED``, ``MERGE_REQUEST_LAST_BUILD_STARTED``, ``MERGE_REQUEST_LAST_EDITED``, ``MERGE_REQUEST_MERGED``, ``MERGE_REQUEST_REVIEWER_FIRST_ASSIGNED``, ``MERGE_REQUEST_PLAN_STAGE_START``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#end_event_identifier ValueStreamAnalytics#end_event_identifier}
        '''
        result = self._values.get("end_event_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def end_event_label_id(self) -> typing.Optional[builtins.str]:
        '''Label ID associated with the end event identifier. In the format of ``gid://gitlab/GroupLabel/<id>`` or ``gid://gitlab/ProjectLabel/<id>``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#end_event_label_id ValueStreamAnalytics#end_event_label_id}
        '''
        result = self._values.get("end_event_label_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hidden(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean whether the stage is hidden, GitLab provided default stages are hidden by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#hidden ValueStreamAnalytics#hidden}
        '''
        result = self._values.get("hidden")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def start_event_identifier(self) -> typing.Optional[builtins.str]:
        '''Start event identifier.

        Valid values are: ``CODE_STAGE_START``, ``ISSUE_CLOSED``, ``ISSUE_CREATED``, ``ISSUE_DEPLOYED_TO_PRODUCTION``, ``ISSUE_FIRST_ADDED_TO_BOARD``, ``ISSUE_FIRST_ADDED_TO_ITERATION``, ``ISSUE_FIRST_ASSIGNED_AT``, ``ISSUE_FIRST_ASSOCIATED_WITH_MILESTONE``, ``ISSUE_FIRST_MENTIONED_IN_COMMIT``, ``ISSUE_LABEL_ADDED``, ``ISSUE_LABEL_REMOVED``, ``ISSUE_LAST_EDITED``, ``ISSUE_STAGE_END``, ``MERGE_REQUEST_CLOSED``, ``MERGE_REQUEST_CREATED``, ``MERGE_REQUEST_FIRST_ASSIGNED_AT``, ``MERGE_REQUEST_FIRST_COMMIT_AT``, ``MERGE_REQUEST_FIRST_DEPLOYED_TO_PRODUCTION``, ``MERGE_REQUEST_LABEL_ADDED``, ``MERGE_REQUEST_LABEL_REMOVED``, ``MERGE_REQUEST_LAST_BUILD_FINISHED``, ``MERGE_REQUEST_LAST_BUILD_STARTED``, ``MERGE_REQUEST_LAST_EDITED``, ``MERGE_REQUEST_MERGED``, ``MERGE_REQUEST_REVIEWER_FIRST_ASSIGNED``, ``MERGE_REQUEST_PLAN_STAGE_START``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#start_event_identifier ValueStreamAnalytics#start_event_identifier}
        '''
        result = self._values.get("start_event_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_event_label_id(self) -> typing.Optional[builtins.str]:
        '''Label ID associated with the start event identifier. In the format of ``gid://gitlab/GroupLabel/<id>`` or ``gid://gitlab/ProjectLabel/<id>``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/value_stream_analytics#start_event_label_id ValueStreamAnalytics#start_event_label_id}
        '''
        result = self._values.get("start_event_label_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ValueStreamAnalyticsStages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ValueStreamAnalyticsStagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.valueStreamAnalytics.ValueStreamAnalyticsStagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b66df318fac552356de5887505ac8c9e4ba5349728db192597491d73680717f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ValueStreamAnalyticsStagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee50e59c5a3821277e66f7d1592f707553eaf1071a89dc33969f87116f48d1a4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ValueStreamAnalyticsStagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1b999426a187fede2bfbfad558e55f72ad955111ee008da7ad9f67fe697808e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d75884de977c56ff561e7a59abdb4af0b70cf776bf8cdaeef0253c88cc516df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8085b82353aa9d4cd104bbe746fefd1091dde5cd6f3e4172dc26846fdbbc2f3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ValueStreamAnalyticsStages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ValueStreamAnalyticsStages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ValueStreamAnalyticsStages]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e799d0216d08c1090bb1d1b0a7eee0a6ccbffc433f1528d6b9a64f6ca2b5d1e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ValueStreamAnalyticsStagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.valueStreamAnalytics.ValueStreamAnalyticsStagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d19367f8bd6a92270d2ea8839b5b8f129395b9314f737b065256cae716497eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCustom")
    def reset_custom(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustom", []))

    @jsii.member(jsii_name="resetEndEventIdentifier")
    def reset_end_event_identifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndEventIdentifier", []))

    @jsii.member(jsii_name="resetEndEventLabelId")
    def reset_end_event_label_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndEventLabelId", []))

    @jsii.member(jsii_name="resetHidden")
    def reset_hidden(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHidden", []))

    @jsii.member(jsii_name="resetStartEventIdentifier")
    def reset_start_event_identifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartEventIdentifier", []))

    @jsii.member(jsii_name="resetStartEventLabelId")
    def reset_start_event_label_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartEventLabelId", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="customInput")
    def custom_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "customInput"))

    @builtins.property
    @jsii.member(jsii_name="endEventIdentifierInput")
    def end_event_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endEventIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="endEventLabelIdInput")
    def end_event_label_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endEventLabelIdInput"))

    @builtins.property
    @jsii.member(jsii_name="hiddenInput")
    def hidden_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hiddenInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="startEventIdentifierInput")
    def start_event_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startEventIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="startEventLabelIdInput")
    def start_event_label_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startEventLabelIdInput"))

    @builtins.property
    @jsii.member(jsii_name="custom")
    def custom(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "custom"))

    @custom.setter
    def custom(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75b925cdb419138f5354d681e0a9b9ee74e6ca0c363045eb1dca7ecdbd0cc521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "custom", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endEventIdentifier")
    def end_event_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endEventIdentifier"))

    @end_event_identifier.setter
    def end_event_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8466c5c9a4183fd6fadaaca904e9a09750b50d9fc6a49e0822e8325b8067d5b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endEventIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endEventLabelId")
    def end_event_label_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endEventLabelId"))

    @end_event_label_id.setter
    def end_event_label_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae128bbdc4a5256883fa7ab891fb0b96d62ec73a4770b9cd313b08f0ce491f05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endEventLabelId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hidden")
    def hidden(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hidden"))

    @hidden.setter
    def hidden(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7ddc0f5fb520d5b6363e3a98ec0d617de96197fa3057eda1d8ffddf668bd9f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hidden", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78bdecae1a1d0fd2b1ac123106484bec80507b044082e387280c89ab3a29663f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startEventIdentifier")
    def start_event_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startEventIdentifier"))

    @start_event_identifier.setter
    def start_event_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12c371a6e755c3a0fe6964833a89015ad0be0f284b59759f4c80025091131683)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startEventIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startEventLabelId")
    def start_event_label_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startEventLabelId"))

    @start_event_label_id.setter
    def start_event_label_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e04926f7ffadd8943866181062321add26a0abf7ae5e8ff9244ad4dc3828ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startEventLabelId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ValueStreamAnalyticsStages]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ValueStreamAnalyticsStages]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ValueStreamAnalyticsStages]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8774a1ad795a37cfa6a44551aa785ba13848a950118ec5d017fc81a1da1a18ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ValueStreamAnalytics",
    "ValueStreamAnalyticsConfig",
    "ValueStreamAnalyticsStages",
    "ValueStreamAnalyticsStagesList",
    "ValueStreamAnalyticsStagesOutputReference",
]

publication.publish()

def _typecheckingstub__57e0acd6111a09cfa2060076c6b0bc12ace64d3ecc8f0bf1b526258c89a56d61(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    stages: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ValueStreamAnalyticsStages, typing.Dict[builtins.str, typing.Any]]]],
    group_full_path: typing.Optional[builtins.str] = None,
    project_full_path: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__e78ef38a0e9f3d86e1d03f8fc65b4b7129f6fa07271b532eb59ef58028e9aabf(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d190bbfbae0ca5e69eae687c69b7763c55653f1da2c63e633009aac84ef867c5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ValueStreamAnalyticsStages, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c169090aac50e32d5cb886bb5c24d7077c563c32ed6f2969849664b2fbbcdc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95c61313779a6347221cb7630d3b421716d461f0dc152a49b6cd65e3244d7b55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c8b206f40f0f99e377f8535f8c786cd92054d56c4688fdbc1a0720be5b45f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a074a05fa329189efe1af57541c86959699134568c83192d06420ff520898779(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    stages: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ValueStreamAnalyticsStages, typing.Dict[builtins.str, typing.Any]]]],
    group_full_path: typing.Optional[builtins.str] = None,
    project_full_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a4723ed0f5e3dded5a24d39ef47c1cacccdd68139bf42d6529b281dcbd899b(
    *,
    name: builtins.str,
    custom: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    end_event_identifier: typing.Optional[builtins.str] = None,
    end_event_label_id: typing.Optional[builtins.str] = None,
    hidden: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    start_event_identifier: typing.Optional[builtins.str] = None,
    start_event_label_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b66df318fac552356de5887505ac8c9e4ba5349728db192597491d73680717f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee50e59c5a3821277e66f7d1592f707553eaf1071a89dc33969f87116f48d1a4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b999426a187fede2bfbfad558e55f72ad955111ee008da7ad9f67fe697808e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d75884de977c56ff561e7a59abdb4af0b70cf776bf8cdaeef0253c88cc516df(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8085b82353aa9d4cd104bbe746fefd1091dde5cd6f3e4172dc26846fdbbc2f3d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e799d0216d08c1090bb1d1b0a7eee0a6ccbffc433f1528d6b9a64f6ca2b5d1e9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ValueStreamAnalyticsStages]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d19367f8bd6a92270d2ea8839b5b8f129395b9314f737b065256cae716497eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b925cdb419138f5354d681e0a9b9ee74e6ca0c363045eb1dca7ecdbd0cc521(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8466c5c9a4183fd6fadaaca904e9a09750b50d9fc6a49e0822e8325b8067d5b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae128bbdc4a5256883fa7ab891fb0b96d62ec73a4770b9cd313b08f0ce491f05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ddc0f5fb520d5b6363e3a98ec0d617de96197fa3057eda1d8ffddf668bd9f7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78bdecae1a1d0fd2b1ac123106484bec80507b044082e387280c89ab3a29663f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12c371a6e755c3a0fe6964833a89015ad0be0f284b59759f4c80025091131683(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e04926f7ffadd8943866181062321add26a0abf7ae5e8ff9244ad4dc3828ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8774a1ad795a37cfa6a44551aa785ba13848a950118ec5d017fc81a1da1a18ce(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ValueStreamAnalyticsStages]],
) -> None:
    """Type checking stubs"""
    pass
