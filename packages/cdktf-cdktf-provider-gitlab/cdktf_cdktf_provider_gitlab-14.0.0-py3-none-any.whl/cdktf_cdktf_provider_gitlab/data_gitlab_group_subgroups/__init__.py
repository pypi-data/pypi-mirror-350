r'''
# `data_gitlab_group_subgroups`

Refer to the Terraform Registry for docs: [`data_gitlab_group_subgroups`](https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups).
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


class DataGitlabGroupSubgroups(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabGroupSubgroups.DataGitlabGroupSubgroups",
):
    '''Represents a {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups gitlab_group_subgroups}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        group_id: jsii.Number,
        all_available: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        min_access_level: typing.Optional[builtins.str] = None,
        order_by: typing.Optional[builtins.str] = None,
        owned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        search: typing.Optional[builtins.str] = None,
        skip_groups: typing.Optional[typing.Sequence[jsii.Number]] = None,
        sort: typing.Optional[builtins.str] = None,
        statistics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        with_custom_attributes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups gitlab_group_subgroups} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param group_id: The ID of the group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#group_id DataGitlabGroupSubgroups#group_id}
        :param all_available: Show all the groups you have access to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#all_available DataGitlabGroupSubgroups#all_available}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#id DataGitlabGroupSubgroups#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param min_access_level: Limit to groups where current user has at least this access level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#min_access_level DataGitlabGroupSubgroups#min_access_level}
        :param order_by: Order groups by name, path or id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#order_by DataGitlabGroupSubgroups#order_by}
        :param owned: Limit to groups explicitly owned by the current user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#owned DataGitlabGroupSubgroups#owned}
        :param search: Return the list of authorized groups matching the search criteria. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#search DataGitlabGroupSubgroups#search}
        :param skip_groups: Skip the group IDs passed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#skip_groups DataGitlabGroupSubgroups#skip_groups}
        :param sort: Order groups in asc or desc order. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#sort DataGitlabGroupSubgroups#sort}
        :param statistics: Include group statistics (administrators only). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#statistics DataGitlabGroupSubgroups#statistics}
        :param with_custom_attributes: Include custom attributes in response (administrators only). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#with_custom_attributes DataGitlabGroupSubgroups#with_custom_attributes}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af0876c2a7d0672b0e25d8ceb2bfdbc3785dc65ecdcd45114975a9291d1ad3c5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataGitlabGroupSubgroupsConfig(
            group_id=group_id,
            all_available=all_available,
            id=id,
            min_access_level=min_access_level,
            order_by=order_by,
            owned=owned,
            search=search,
            skip_groups=skip_groups,
            sort=sort,
            statistics=statistics,
            with_custom_attributes=with_custom_attributes,
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
        '''Generates CDKTF code for importing a DataGitlabGroupSubgroups resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataGitlabGroupSubgroups to import.
        :param import_from_id: The id of the existing DataGitlabGroupSubgroups that should be imported. Refer to the {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataGitlabGroupSubgroups to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bba1dfc0da76130313f808c10b12e68a269efcf9b490f3b078de4209155ad32b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAllAvailable")
    def reset_all_available(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllAvailable", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMinAccessLevel")
    def reset_min_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinAccessLevel", []))

    @jsii.member(jsii_name="resetOrderBy")
    def reset_order_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrderBy", []))

    @jsii.member(jsii_name="resetOwned")
    def reset_owned(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwned", []))

    @jsii.member(jsii_name="resetSearch")
    def reset_search(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearch", []))

    @jsii.member(jsii_name="resetSkipGroups")
    def reset_skip_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipGroups", []))

    @jsii.member(jsii_name="resetSort")
    def reset_sort(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSort", []))

    @jsii.member(jsii_name="resetStatistics")
    def reset_statistics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatistics", []))

    @jsii.member(jsii_name="resetWithCustomAttributes")
    def reset_with_custom_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWithCustomAttributes", []))

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
    @jsii.member(jsii_name="subgroups")
    def subgroups(self) -> "DataGitlabGroupSubgroupsSubgroupsList":
        return typing.cast("DataGitlabGroupSubgroupsSubgroupsList", jsii.get(self, "subgroups"))

    @builtins.property
    @jsii.member(jsii_name="allAvailableInput")
    def all_available_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allAvailableInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="minAccessLevelInput")
    def min_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="orderByInput")
    def order_by_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orderByInput"))

    @builtins.property
    @jsii.member(jsii_name="ownedInput")
    def owned_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ownedInput"))

    @builtins.property
    @jsii.member(jsii_name="searchInput")
    def search_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "searchInput"))

    @builtins.property
    @jsii.member(jsii_name="skipGroupsInput")
    def skip_groups_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "skipGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="sortInput")
    def sort_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sortInput"))

    @builtins.property
    @jsii.member(jsii_name="statisticsInput")
    def statistics_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "statisticsInput"))

    @builtins.property
    @jsii.member(jsii_name="withCustomAttributesInput")
    def with_custom_attributes_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "withCustomAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="allAvailable")
    def all_available(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allAvailable"))

    @all_available.setter
    def all_available(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f61deb0ece11ccc204e583766bcfd49e2ced304219116c60280186c3e0391ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allAvailable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2003711be90fdd3931a6191caa2b7a85bd5439e4192ed1928183a4f4845214cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aaae0f01fa1a9fbb871f95fadc65d60d8cdccf93a863b516343d0c85bc12c64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minAccessLevel")
    def min_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minAccessLevel"))

    @min_access_level.setter
    def min_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e5bddabff2b2e85154d86b284d031c7fd06a9270917651749f1bec53067b7a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orderBy")
    def order_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orderBy"))

    @order_by.setter
    def order_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__738f41dcda9e857d9a3d87e0245a539714ebb7b4c5cb972cf89b3146a5056ade)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orderBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="owned")
    def owned(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "owned"))

    @owned.setter
    def owned(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c81a69b35031ae2511b2d55949f2d3c85f764c77cbcc4d6a600ac780a5d67ee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "owned", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="search")
    def search(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "search"))

    @search.setter
    def search(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b339ce47f9252b4dc09a9dd6ff6d5798e899364971b8cbe0125b0471337b2617)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "search", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipGroups")
    def skip_groups(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "skipGroups"))

    @skip_groups.setter
    def skip_groups(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__364c02a8fa00befadf09df471bded0d506953c4701130601e34a84395c95e7a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sort")
    def sort(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sort"))

    @sort.setter
    def sort(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3dae05844229fac12003f1d9e38bd597686eb289055708a925de18dd4c58c0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statistics")
    def statistics(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "statistics"))

    @statistics.setter
    def statistics(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fa3a68a4117009f5a4c88cea049d0df23d9cce2e89339f6e4c2d42dcb4031cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statistics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="withCustomAttributes")
    def with_custom_attributes(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "withCustomAttributes"))

    @with_custom_attributes.setter
    def with_custom_attributes(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a04c7fb6588e6f64593d8c6e3369fb10ee925be84265d4194ab94aede8bc6bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withCustomAttributes", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.dataGitlabGroupSubgroups.DataGitlabGroupSubgroupsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "group_id": "groupId",
        "all_available": "allAvailable",
        "id": "id",
        "min_access_level": "minAccessLevel",
        "order_by": "orderBy",
        "owned": "owned",
        "search": "search",
        "skip_groups": "skipGroups",
        "sort": "sort",
        "statistics": "statistics",
        "with_custom_attributes": "withCustomAttributes",
    },
)
class DataGitlabGroupSubgroupsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        group_id: jsii.Number,
        all_available: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        min_access_level: typing.Optional[builtins.str] = None,
        order_by: typing.Optional[builtins.str] = None,
        owned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        search: typing.Optional[builtins.str] = None,
        skip_groups: typing.Optional[typing.Sequence[jsii.Number]] = None,
        sort: typing.Optional[builtins.str] = None,
        statistics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        with_custom_attributes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param group_id: The ID of the group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#group_id DataGitlabGroupSubgroups#group_id}
        :param all_available: Show all the groups you have access to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#all_available DataGitlabGroupSubgroups#all_available}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#id DataGitlabGroupSubgroups#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param min_access_level: Limit to groups where current user has at least this access level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#min_access_level DataGitlabGroupSubgroups#min_access_level}
        :param order_by: Order groups by name, path or id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#order_by DataGitlabGroupSubgroups#order_by}
        :param owned: Limit to groups explicitly owned by the current user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#owned DataGitlabGroupSubgroups#owned}
        :param search: Return the list of authorized groups matching the search criteria. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#search DataGitlabGroupSubgroups#search}
        :param skip_groups: Skip the group IDs passed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#skip_groups DataGitlabGroupSubgroups#skip_groups}
        :param sort: Order groups in asc or desc order. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#sort DataGitlabGroupSubgroups#sort}
        :param statistics: Include group statistics (administrators only). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#statistics DataGitlabGroupSubgroups#statistics}
        :param with_custom_attributes: Include custom attributes in response (administrators only). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#with_custom_attributes DataGitlabGroupSubgroups#with_custom_attributes}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e342cf71f778dc14a03716d693be61bcbfb93a3758654f64f567077c6e5129ae)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument all_available", value=all_available, expected_type=type_hints["all_available"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument min_access_level", value=min_access_level, expected_type=type_hints["min_access_level"])
            check_type(argname="argument order_by", value=order_by, expected_type=type_hints["order_by"])
            check_type(argname="argument owned", value=owned, expected_type=type_hints["owned"])
            check_type(argname="argument search", value=search, expected_type=type_hints["search"])
            check_type(argname="argument skip_groups", value=skip_groups, expected_type=type_hints["skip_groups"])
            check_type(argname="argument sort", value=sort, expected_type=type_hints["sort"])
            check_type(argname="argument statistics", value=statistics, expected_type=type_hints["statistics"])
            check_type(argname="argument with_custom_attributes", value=with_custom_attributes, expected_type=type_hints["with_custom_attributes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_id": group_id,
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
        if all_available is not None:
            self._values["all_available"] = all_available
        if id is not None:
            self._values["id"] = id
        if min_access_level is not None:
            self._values["min_access_level"] = min_access_level
        if order_by is not None:
            self._values["order_by"] = order_by
        if owned is not None:
            self._values["owned"] = owned
        if search is not None:
            self._values["search"] = search
        if skip_groups is not None:
            self._values["skip_groups"] = skip_groups
        if sort is not None:
            self._values["sort"] = sort
        if statistics is not None:
            self._values["statistics"] = statistics
        if with_custom_attributes is not None:
            self._values["with_custom_attributes"] = with_custom_attributes

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
    def group_id(self) -> jsii.Number:
        '''The ID of the group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#group_id DataGitlabGroupSubgroups#group_id}
        '''
        result = self._values.get("group_id")
        assert result is not None, "Required property 'group_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def all_available(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Show all the groups you have access to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#all_available DataGitlabGroupSubgroups#all_available}
        '''
        result = self._values.get("all_available")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#id DataGitlabGroupSubgroups#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_access_level(self) -> typing.Optional[builtins.str]:
        '''Limit to groups where current user has at least this access level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#min_access_level DataGitlabGroupSubgroups#min_access_level}
        '''
        result = self._values.get("min_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def order_by(self) -> typing.Optional[builtins.str]:
        '''Order groups by name, path or id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#order_by DataGitlabGroupSubgroups#order_by}
        '''
        result = self._values.get("order_by")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owned(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Limit to groups explicitly owned by the current user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#owned DataGitlabGroupSubgroups#owned}
        '''
        result = self._values.get("owned")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def search(self) -> typing.Optional[builtins.str]:
        '''Return the list of authorized groups matching the search criteria.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#search DataGitlabGroupSubgroups#search}
        '''
        result = self._values.get("search")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_groups(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Skip the group IDs passed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#skip_groups DataGitlabGroupSubgroups#skip_groups}
        '''
        result = self._values.get("skip_groups")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def sort(self) -> typing.Optional[builtins.str]:
        '''Order groups in asc or desc order.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#sort DataGitlabGroupSubgroups#sort}
        '''
        result = self._values.get("sort")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statistics(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Include group statistics (administrators only).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#statistics DataGitlabGroupSubgroups#statistics}
        '''
        result = self._values.get("statistics")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def with_custom_attributes(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Include custom attributes in response (administrators only).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/group_subgroups#with_custom_attributes DataGitlabGroupSubgroups#with_custom_attributes}
        '''
        result = self._values.get("with_custom_attributes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGitlabGroupSubgroupsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.dataGitlabGroupSubgroups.DataGitlabGroupSubgroupsSubgroups",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGitlabGroupSubgroupsSubgroups:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGitlabGroupSubgroupsSubgroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGitlabGroupSubgroupsSubgroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabGroupSubgroups.DataGitlabGroupSubgroupsSubgroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9782d9ba0a94811bb0210a6d2b6a0c707146d45a858da56084abfbe4ddf7fbe0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGitlabGroupSubgroupsSubgroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b8f4b0981c1eae2214da049956a2f4a299568cd72c0f0e72fec031358d23e5e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGitlabGroupSubgroupsSubgroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__308a09243b8a93dff406c83a1c95cfecbfee5b003535f7dbd74e8b0f7eaa8f6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__056314ba0d7e24da3bd794ec5afb721a35d51ab8bdfc7e42caec4b95effb4353)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02dd6d3ba4f6839ada3fca6e79420105e647510ef763da97857b89d190a1ed25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGitlabGroupSubgroupsSubgroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabGroupSubgroups.DataGitlabGroupSubgroupsSubgroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bee053ba74c878cb1f760364120f75b03c61edfb2f35e4059a58e9f09179a89)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allowedEmailDomainsList")
    def allowed_email_domains_list(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allowedEmailDomainsList"))

    @builtins.property
    @jsii.member(jsii_name="autoDevopsEnabled")
    def auto_devops_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "autoDevopsEnabled"))

    @builtins.property
    @jsii.member(jsii_name="avatarUrl")
    def avatar_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "avatarUrl"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="defaultBranchProtection")
    def default_branch_protection(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultBranchProtection"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="emailsEnabled")
    def emails_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "emailsEnabled"))

    @builtins.property
    @jsii.member(jsii_name="fileTemplateProjectId")
    def file_template_project_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fileTemplateProjectId"))

    @builtins.property
    @jsii.member(jsii_name="fullName")
    def full_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullName"))

    @builtins.property
    @jsii.member(jsii_name="fullPath")
    def full_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullPath"))

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "groupId"))

    @builtins.property
    @jsii.member(jsii_name="ipRestrictionRanges")
    def ip_restriction_ranges(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipRestrictionRanges"))

    @builtins.property
    @jsii.member(jsii_name="lfsEnabled")
    def lfs_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "lfsEnabled"))

    @builtins.property
    @jsii.member(jsii_name="mentionsDisabled")
    def mentions_disabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "mentionsDisabled"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="parentId")
    def parent_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parentId"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="projectCreationLevel")
    def project_creation_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectCreationLevel"))

    @builtins.property
    @jsii.member(jsii_name="requestAccessEnabled")
    def request_access_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "requestAccessEnabled"))

    @builtins.property
    @jsii.member(jsii_name="requireTwoFactorAuthentication")
    def require_two_factor_authentication(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "requireTwoFactorAuthentication"))

    @builtins.property
    @jsii.member(jsii_name="sharedRunnersSetting")
    def shared_runners_setting(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharedRunnersSetting"))

    @builtins.property
    @jsii.member(jsii_name="shareWithGroupLock")
    def share_with_group_lock(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "shareWithGroupLock"))

    @builtins.property
    @jsii.member(jsii_name="statistics")
    def statistics(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "statistics"))

    @builtins.property
    @jsii.member(jsii_name="subgroupCreationLevel")
    def subgroup_creation_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subgroupCreationLevel"))

    @builtins.property
    @jsii.member(jsii_name="twoFactorGracePeriod")
    def two_factor_grace_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "twoFactorGracePeriod"))

    @builtins.property
    @jsii.member(jsii_name="visibility")
    def visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibility"))

    @builtins.property
    @jsii.member(jsii_name="webUrl")
    def web_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webUrl"))

    @builtins.property
    @jsii.member(jsii_name="wikiAccessLevel")
    def wiki_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "wikiAccessLevel"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataGitlabGroupSubgroupsSubgroups]:
        return typing.cast(typing.Optional[DataGitlabGroupSubgroupsSubgroups], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGitlabGroupSubgroupsSubgroups],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bfe80e26029574b78b5b5039a060ee54d7601ef762251d43cc83f037a089dc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataGitlabGroupSubgroups",
    "DataGitlabGroupSubgroupsConfig",
    "DataGitlabGroupSubgroupsSubgroups",
    "DataGitlabGroupSubgroupsSubgroupsList",
    "DataGitlabGroupSubgroupsSubgroupsOutputReference",
]

publication.publish()

def _typecheckingstub__af0876c2a7d0672b0e25d8ceb2bfdbc3785dc65ecdcd45114975a9291d1ad3c5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    group_id: jsii.Number,
    all_available: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    min_access_level: typing.Optional[builtins.str] = None,
    order_by: typing.Optional[builtins.str] = None,
    owned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    search: typing.Optional[builtins.str] = None,
    skip_groups: typing.Optional[typing.Sequence[jsii.Number]] = None,
    sort: typing.Optional[builtins.str] = None,
    statistics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    with_custom_attributes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__bba1dfc0da76130313f808c10b12e68a269efcf9b490f3b078de4209155ad32b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f61deb0ece11ccc204e583766bcfd49e2ced304219116c60280186c3e0391ac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2003711be90fdd3931a6191caa2b7a85bd5439e4192ed1928183a4f4845214cc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aaae0f01fa1a9fbb871f95fadc65d60d8cdccf93a863b516343d0c85bc12c64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e5bddabff2b2e85154d86b284d031c7fd06a9270917651749f1bec53067b7a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__738f41dcda9e857d9a3d87e0245a539714ebb7b4c5cb972cf89b3146a5056ade(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c81a69b35031ae2511b2d55949f2d3c85f764c77cbcc4d6a600ac780a5d67ee6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b339ce47f9252b4dc09a9dd6ff6d5798e899364971b8cbe0125b0471337b2617(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__364c02a8fa00befadf09df471bded0d506953c4701130601e34a84395c95e7a2(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3dae05844229fac12003f1d9e38bd597686eb289055708a925de18dd4c58c0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fa3a68a4117009f5a4c88cea049d0df23d9cce2e89339f6e4c2d42dcb4031cb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a04c7fb6588e6f64593d8c6e3369fb10ee925be84265d4194ab94aede8bc6bd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e342cf71f778dc14a03716d693be61bcbfb93a3758654f64f567077c6e5129ae(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    group_id: jsii.Number,
    all_available: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    min_access_level: typing.Optional[builtins.str] = None,
    order_by: typing.Optional[builtins.str] = None,
    owned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    search: typing.Optional[builtins.str] = None,
    skip_groups: typing.Optional[typing.Sequence[jsii.Number]] = None,
    sort: typing.Optional[builtins.str] = None,
    statistics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    with_custom_attributes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9782d9ba0a94811bb0210a6d2b6a0c707146d45a858da56084abfbe4ddf7fbe0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b8f4b0981c1eae2214da049956a2f4a299568cd72c0f0e72fec031358d23e5e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__308a09243b8a93dff406c83a1c95cfecbfee5b003535f7dbd74e8b0f7eaa8f6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056314ba0d7e24da3bd794ec5afb721a35d51ab8bdfc7e42caec4b95effb4353(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02dd6d3ba4f6839ada3fca6e79420105e647510ef763da97857b89d190a1ed25(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bee053ba74c878cb1f760364120f75b03c61edfb2f35e4059a58e9f09179a89(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bfe80e26029574b78b5b5039a060ee54d7601ef762251d43cc83f037a089dc7(
    value: typing.Optional[DataGitlabGroupSubgroupsSubgroups],
) -> None:
    """Type checking stubs"""
    pass
