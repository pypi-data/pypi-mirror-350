r'''
# `data_gitlab_projects`

Refer to the Terraform Registry for docs: [`data_gitlab_projects`](https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects).
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


class DataGitlabProjects(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjects",
):
    '''Represents a {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects gitlab_projects}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        archived: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        group_id: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        include_subgroups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_queryable_pages: typing.Optional[jsii.Number] = None,
        membership: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        min_access_level: typing.Optional[jsii.Number] = None,
        order_by: typing.Optional[builtins.str] = None,
        owned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        page: typing.Optional[jsii.Number] = None,
        per_page: typing.Optional[jsii.Number] = None,
        search: typing.Optional[builtins.str] = None,
        simple: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sort: typing.Optional[builtins.str] = None,
        starred: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        statistics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        topic: typing.Optional[typing.Sequence[builtins.str]] = None,
        visibility: typing.Optional[builtins.str] = None,
        with_custom_attributes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        with_issues_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        with_merge_requests_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        with_programming_language: typing.Optional[builtins.str] = None,
        with_shared: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects gitlab_projects} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param archived: Limit by archived status. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#archived DataGitlabProjects#archived}
        :param group_id: The ID of the group owned by the authenticated user to look projects for within. Cannot be used with ``min_access_level``, ``with_programming_language`` or ``statistics``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#group_id DataGitlabProjects#group_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#id DataGitlabProjects#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_subgroups: Include projects in subgroups of this group. Default is ``false``. Needs ``group_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#include_subgroups DataGitlabProjects#include_subgroups}
        :param max_queryable_pages: The maximum number of project results pages that may be queried. Prevents overloading your Gitlab instance in case of a misconfiguration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#max_queryable_pages DataGitlabProjects#max_queryable_pages}
        :param membership: Limit by projects that the current user is a member of. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#membership DataGitlabProjects#membership}
        :param min_access_level: Limit to projects where current user has at least this access level, refer to the `official documentation <https://docs.gitlab.com/api/members/>`_ for values. Cannot be used with ``group_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#min_access_level DataGitlabProjects#min_access_level}
        :param order_by: Return projects ordered ordered by: ``id``, ``name``, ``path``, ``created_at``, ``updated_at``, ``last_activity_at``, ``similarity``, ``repository_size``, ``storage_size``, ``packages_size``, ``wiki_size``. Some values or only available in certain circumstances. See `upstream docs <https://docs.gitlab.com/api/projects/#list-all-projects>`_ for details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#order_by DataGitlabProjects#order_by}
        :param owned: Limit by projects owned by the current user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#owned DataGitlabProjects#owned}
        :param page: The first page to begin the query on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#page DataGitlabProjects#page}
        :param per_page: The number of results to return per page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#per_page DataGitlabProjects#per_page}
        :param search: Return list of authorized projects matching the search criteria. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#search DataGitlabProjects#search}
        :param simple: Return only the ID, URL, name, and path of each project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#simple DataGitlabProjects#simple}
        :param sort: Return projects sorted in ``asc`` or ``desc`` order. Default is ``desc``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#sort DataGitlabProjects#sort}
        :param starred: Limit by projects starred by the current user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#starred DataGitlabProjects#starred}
        :param statistics: Include project statistics. Cannot be used with ``group_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#statistics DataGitlabProjects#statistics}
        :param topic: Limit by projects that have all of the given topics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#topic DataGitlabProjects#topic}
        :param visibility: Limit by visibility ``public``, ``internal``, or ``private``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#visibility DataGitlabProjects#visibility}
        :param with_custom_attributes: Include custom attributes in response *(admins only)*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#with_custom_attributes DataGitlabProjects#with_custom_attributes}
        :param with_issues_enabled: Limit by projects with issues feature enabled. Default is ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#with_issues_enabled DataGitlabProjects#with_issues_enabled}
        :param with_merge_requests_enabled: Limit by projects with merge requests feature enabled. Default is ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#with_merge_requests_enabled DataGitlabProjects#with_merge_requests_enabled}
        :param with_programming_language: Limit by projects which use the given programming language. Cannot be used with ``group_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#with_programming_language DataGitlabProjects#with_programming_language}
        :param with_shared: Include projects shared to this group. Default is ``true``. Needs ``group_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#with_shared DataGitlabProjects#with_shared}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__993279bdb0d1ba395d8f49ee2bdc6676530aac6554fc359e0ed8694e08284e15)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataGitlabProjectsConfig(
            archived=archived,
            group_id=group_id,
            id=id,
            include_subgroups=include_subgroups,
            max_queryable_pages=max_queryable_pages,
            membership=membership,
            min_access_level=min_access_level,
            order_by=order_by,
            owned=owned,
            page=page,
            per_page=per_page,
            search=search,
            simple=simple,
            sort=sort,
            starred=starred,
            statistics=statistics,
            topic=topic,
            visibility=visibility,
            with_custom_attributes=with_custom_attributes,
            with_issues_enabled=with_issues_enabled,
            with_merge_requests_enabled=with_merge_requests_enabled,
            with_programming_language=with_programming_language,
            with_shared=with_shared,
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
        '''Generates CDKTF code for importing a DataGitlabProjects resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataGitlabProjects to import.
        :param import_from_id: The id of the existing DataGitlabProjects that should be imported. Refer to the {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataGitlabProjects to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17548a2ead63fa297bee57630363c7dfc3fcb868fbbb93327a057008fdc3f1f3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetArchived")
    def reset_archived(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchived", []))

    @jsii.member(jsii_name="resetGroupId")
    def reset_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIncludeSubgroups")
    def reset_include_subgroups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeSubgroups", []))

    @jsii.member(jsii_name="resetMaxQueryablePages")
    def reset_max_queryable_pages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxQueryablePages", []))

    @jsii.member(jsii_name="resetMembership")
    def reset_membership(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMembership", []))

    @jsii.member(jsii_name="resetMinAccessLevel")
    def reset_min_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinAccessLevel", []))

    @jsii.member(jsii_name="resetOrderBy")
    def reset_order_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrderBy", []))

    @jsii.member(jsii_name="resetOwned")
    def reset_owned(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwned", []))

    @jsii.member(jsii_name="resetPage")
    def reset_page(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPage", []))

    @jsii.member(jsii_name="resetPerPage")
    def reset_per_page(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerPage", []))

    @jsii.member(jsii_name="resetSearch")
    def reset_search(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearch", []))

    @jsii.member(jsii_name="resetSimple")
    def reset_simple(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSimple", []))

    @jsii.member(jsii_name="resetSort")
    def reset_sort(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSort", []))

    @jsii.member(jsii_name="resetStarred")
    def reset_starred(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStarred", []))

    @jsii.member(jsii_name="resetStatistics")
    def reset_statistics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatistics", []))

    @jsii.member(jsii_name="resetTopic")
    def reset_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopic", []))

    @jsii.member(jsii_name="resetVisibility")
    def reset_visibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisibility", []))

    @jsii.member(jsii_name="resetWithCustomAttributes")
    def reset_with_custom_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWithCustomAttributes", []))

    @jsii.member(jsii_name="resetWithIssuesEnabled")
    def reset_with_issues_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWithIssuesEnabled", []))

    @jsii.member(jsii_name="resetWithMergeRequestsEnabled")
    def reset_with_merge_requests_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWithMergeRequestsEnabled", []))

    @jsii.member(jsii_name="resetWithProgrammingLanguage")
    def reset_with_programming_language(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWithProgrammingLanguage", []))

    @jsii.member(jsii_name="resetWithShared")
    def reset_with_shared(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWithShared", []))

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
    @jsii.member(jsii_name="projects")
    def projects(self) -> "DataGitlabProjectsProjectsList":
        return typing.cast("DataGitlabProjectsProjectsList", jsii.get(self, "projects"))

    @builtins.property
    @jsii.member(jsii_name="archivedInput")
    def archived_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "archivedInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includeSubgroupsInput")
    def include_subgroups_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeSubgroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxQueryablePagesInput")
    def max_queryable_pages_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxQueryablePagesInput"))

    @builtins.property
    @jsii.member(jsii_name="membershipInput")
    def membership_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "membershipInput"))

    @builtins.property
    @jsii.member(jsii_name="minAccessLevelInput")
    def min_access_level_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minAccessLevelInput"))

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
    @jsii.member(jsii_name="pageInput")
    def page_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "pageInput"))

    @builtins.property
    @jsii.member(jsii_name="perPageInput")
    def per_page_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "perPageInput"))

    @builtins.property
    @jsii.member(jsii_name="searchInput")
    def search_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "searchInput"))

    @builtins.property
    @jsii.member(jsii_name="simpleInput")
    def simple_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "simpleInput"))

    @builtins.property
    @jsii.member(jsii_name="sortInput")
    def sort_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sortInput"))

    @builtins.property
    @jsii.member(jsii_name="starredInput")
    def starred_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "starredInput"))

    @builtins.property
    @jsii.member(jsii_name="statisticsInput")
    def statistics_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "statisticsInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="visibilityInput")
    def visibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "visibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="withCustomAttributesInput")
    def with_custom_attributes_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "withCustomAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="withIssuesEnabledInput")
    def with_issues_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "withIssuesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="withMergeRequestsEnabledInput")
    def with_merge_requests_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "withMergeRequestsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="withProgrammingLanguageInput")
    def with_programming_language_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "withProgrammingLanguageInput"))

    @builtins.property
    @jsii.member(jsii_name="withSharedInput")
    def with_shared_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "withSharedInput"))

    @builtins.property
    @jsii.member(jsii_name="archived")
    def archived(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "archived"))

    @archived.setter
    def archived(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dde07081449ab4c4a3f7db2823f6e331b53e2bc366dd473a32ad211084e67b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archived", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__600bbe88e991d2c73af35c710b5f51ef02527e5fdef185e68009035b874f8ed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d099d34a2e43d6b1469b8797f900e9bb4d9a5482f9c9b83ee8adca514f97885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeSubgroups")
    def include_subgroups(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeSubgroups"))

    @include_subgroups.setter
    def include_subgroups(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a4c3d4b4fc8dfa7cde46073c5c3d24cb911f02d641c2e12ee3b209b89973ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeSubgroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxQueryablePages")
    def max_queryable_pages(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxQueryablePages"))

    @max_queryable_pages.setter
    def max_queryable_pages(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac81e903034f7df8ffe7662a60d3fdaf1e0c8b5be5d9f894185701df78f38d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxQueryablePages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="membership")
    def membership(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "membership"))

    @membership.setter
    def membership(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9ca4fe113b3f7260e86dfbc9a35b85ae8622995107fb66e1f8a166dfbbfb9e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "membership", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minAccessLevel")
    def min_access_level(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minAccessLevel"))

    @min_access_level.setter
    def min_access_level(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd8b90a0c237397b46929e0822f1fb8f970926a6c41ed7380406e568ab18ec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orderBy")
    def order_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orderBy"))

    @order_by.setter
    def order_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7db14c905a3f6eaded4940b3d6d41bc8ce04888dcb6c0bfebe9cc5f435e37771)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4927db345addd4bcde7703610599fbe160c38000daf3d56c620344627d26dc92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "owned", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="page")
    def page(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "page"))

    @page.setter
    def page(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a189c6ac953f2ff8f8b648dcb6400984ace9737963653dc5573273caf40d76cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "page", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="perPage")
    def per_page(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "perPage"))

    @per_page.setter
    def per_page(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31771985c71c50cbbedec7b4f8efe670c1c3987bb9b160dc9018084bacb6607b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "perPage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="search")
    def search(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "search"))

    @search.setter
    def search(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54a6a48386b829c18cc980baaa848ffaf35bbe53ecc2248bd0e63874284f7354)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "search", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="simple")
    def simple(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "simple"))

    @simple.setter
    def simple(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd794144fd2b4d6bf35ee0bb6f91e1b1f9fa598d6434c61df9c7883d8237a4f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "simple", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sort")
    def sort(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sort"))

    @sort.setter
    def sort(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94f972661e27efbd489074dff3b67f98ef5270e3c30a361d7d12cca655acb3fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="starred")
    def starred(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "starred"))

    @starred.setter
    def starred(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d71025fab0cf51e83a4a27d483c356b1528acb09f31f4b42a32234ed7e6ddfa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "starred", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__bc364874d7548a0d3ccf3bbd3cade6a0f167a196ba066ef37595c98c4ab92a28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statistics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cc96579549159166800b38a3f8d6d37d5c3890bf203658635a0012ee8167bad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visibility")
    def visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibility"))

    @visibility.setter
    def visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c852665c70a28f4c642eeaf1a23537a525af0906852ece046df4badf85d4e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibility", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__8611409750fd8dbb46741deecc06f1a9c744a8bc0d976b39fde27a87bb8b2d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withCustomAttributes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="withIssuesEnabled")
    def with_issues_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "withIssuesEnabled"))

    @with_issues_enabled.setter
    def with_issues_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60715b5c5bb67e548467a0d141d57ba7d1572318390173ef79fa798d20f24598)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withIssuesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="withMergeRequestsEnabled")
    def with_merge_requests_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "withMergeRequestsEnabled"))

    @with_merge_requests_enabled.setter
    def with_merge_requests_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d5e10b9fa60da6853aba5900c84aa5bf35cf5e9955d182f7f6418302a2aebbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withMergeRequestsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="withProgrammingLanguage")
    def with_programming_language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "withProgrammingLanguage"))

    @with_programming_language.setter
    def with_programming_language(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c27d87413960ec276bc9a24bc384e444a410482b2e242f90cca954c0cad3e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withProgrammingLanguage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="withShared")
    def with_shared(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "withShared"))

    @with_shared.setter
    def with_shared(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2279de7e39ab30a1752ea5ede57433a01c1cc63a268f8a327c32d13d9a4aab2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withShared", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "archived": "archived",
        "group_id": "groupId",
        "id": "id",
        "include_subgroups": "includeSubgroups",
        "max_queryable_pages": "maxQueryablePages",
        "membership": "membership",
        "min_access_level": "minAccessLevel",
        "order_by": "orderBy",
        "owned": "owned",
        "page": "page",
        "per_page": "perPage",
        "search": "search",
        "simple": "simple",
        "sort": "sort",
        "starred": "starred",
        "statistics": "statistics",
        "topic": "topic",
        "visibility": "visibility",
        "with_custom_attributes": "withCustomAttributes",
        "with_issues_enabled": "withIssuesEnabled",
        "with_merge_requests_enabled": "withMergeRequestsEnabled",
        "with_programming_language": "withProgrammingLanguage",
        "with_shared": "withShared",
    },
)
class DataGitlabProjectsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        archived: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        group_id: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        include_subgroups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_queryable_pages: typing.Optional[jsii.Number] = None,
        membership: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        min_access_level: typing.Optional[jsii.Number] = None,
        order_by: typing.Optional[builtins.str] = None,
        owned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        page: typing.Optional[jsii.Number] = None,
        per_page: typing.Optional[jsii.Number] = None,
        search: typing.Optional[builtins.str] = None,
        simple: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sort: typing.Optional[builtins.str] = None,
        starred: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        statistics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        topic: typing.Optional[typing.Sequence[builtins.str]] = None,
        visibility: typing.Optional[builtins.str] = None,
        with_custom_attributes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        with_issues_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        with_merge_requests_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        with_programming_language: typing.Optional[builtins.str] = None,
        with_shared: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param archived: Limit by archived status. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#archived DataGitlabProjects#archived}
        :param group_id: The ID of the group owned by the authenticated user to look projects for within. Cannot be used with ``min_access_level``, ``with_programming_language`` or ``statistics``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#group_id DataGitlabProjects#group_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#id DataGitlabProjects#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_subgroups: Include projects in subgroups of this group. Default is ``false``. Needs ``group_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#include_subgroups DataGitlabProjects#include_subgroups}
        :param max_queryable_pages: The maximum number of project results pages that may be queried. Prevents overloading your Gitlab instance in case of a misconfiguration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#max_queryable_pages DataGitlabProjects#max_queryable_pages}
        :param membership: Limit by projects that the current user is a member of. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#membership DataGitlabProjects#membership}
        :param min_access_level: Limit to projects where current user has at least this access level, refer to the `official documentation <https://docs.gitlab.com/api/members/>`_ for values. Cannot be used with ``group_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#min_access_level DataGitlabProjects#min_access_level}
        :param order_by: Return projects ordered ordered by: ``id``, ``name``, ``path``, ``created_at``, ``updated_at``, ``last_activity_at``, ``similarity``, ``repository_size``, ``storage_size``, ``packages_size``, ``wiki_size``. Some values or only available in certain circumstances. See `upstream docs <https://docs.gitlab.com/api/projects/#list-all-projects>`_ for details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#order_by DataGitlabProjects#order_by}
        :param owned: Limit by projects owned by the current user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#owned DataGitlabProjects#owned}
        :param page: The first page to begin the query on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#page DataGitlabProjects#page}
        :param per_page: The number of results to return per page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#per_page DataGitlabProjects#per_page}
        :param search: Return list of authorized projects matching the search criteria. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#search DataGitlabProjects#search}
        :param simple: Return only the ID, URL, name, and path of each project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#simple DataGitlabProjects#simple}
        :param sort: Return projects sorted in ``asc`` or ``desc`` order. Default is ``desc``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#sort DataGitlabProjects#sort}
        :param starred: Limit by projects starred by the current user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#starred DataGitlabProjects#starred}
        :param statistics: Include project statistics. Cannot be used with ``group_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#statistics DataGitlabProjects#statistics}
        :param topic: Limit by projects that have all of the given topics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#topic DataGitlabProjects#topic}
        :param visibility: Limit by visibility ``public``, ``internal``, or ``private``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#visibility DataGitlabProjects#visibility}
        :param with_custom_attributes: Include custom attributes in response *(admins only)*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#with_custom_attributes DataGitlabProjects#with_custom_attributes}
        :param with_issues_enabled: Limit by projects with issues feature enabled. Default is ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#with_issues_enabled DataGitlabProjects#with_issues_enabled}
        :param with_merge_requests_enabled: Limit by projects with merge requests feature enabled. Default is ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#with_merge_requests_enabled DataGitlabProjects#with_merge_requests_enabled}
        :param with_programming_language: Limit by projects which use the given programming language. Cannot be used with ``group_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#with_programming_language DataGitlabProjects#with_programming_language}
        :param with_shared: Include projects shared to this group. Default is ``true``. Needs ``group_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#with_shared DataGitlabProjects#with_shared}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99f4ff5494815653fd2ddb374edfdee6ca2fdab397e2cdd3b99adf9781027678)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument archived", value=archived, expected_type=type_hints["archived"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument include_subgroups", value=include_subgroups, expected_type=type_hints["include_subgroups"])
            check_type(argname="argument max_queryable_pages", value=max_queryable_pages, expected_type=type_hints["max_queryable_pages"])
            check_type(argname="argument membership", value=membership, expected_type=type_hints["membership"])
            check_type(argname="argument min_access_level", value=min_access_level, expected_type=type_hints["min_access_level"])
            check_type(argname="argument order_by", value=order_by, expected_type=type_hints["order_by"])
            check_type(argname="argument owned", value=owned, expected_type=type_hints["owned"])
            check_type(argname="argument page", value=page, expected_type=type_hints["page"])
            check_type(argname="argument per_page", value=per_page, expected_type=type_hints["per_page"])
            check_type(argname="argument search", value=search, expected_type=type_hints["search"])
            check_type(argname="argument simple", value=simple, expected_type=type_hints["simple"])
            check_type(argname="argument sort", value=sort, expected_type=type_hints["sort"])
            check_type(argname="argument starred", value=starred, expected_type=type_hints["starred"])
            check_type(argname="argument statistics", value=statistics, expected_type=type_hints["statistics"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
            check_type(argname="argument with_custom_attributes", value=with_custom_attributes, expected_type=type_hints["with_custom_attributes"])
            check_type(argname="argument with_issues_enabled", value=with_issues_enabled, expected_type=type_hints["with_issues_enabled"])
            check_type(argname="argument with_merge_requests_enabled", value=with_merge_requests_enabled, expected_type=type_hints["with_merge_requests_enabled"])
            check_type(argname="argument with_programming_language", value=with_programming_language, expected_type=type_hints["with_programming_language"])
            check_type(argname="argument with_shared", value=with_shared, expected_type=type_hints["with_shared"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if archived is not None:
            self._values["archived"] = archived
        if group_id is not None:
            self._values["group_id"] = group_id
        if id is not None:
            self._values["id"] = id
        if include_subgroups is not None:
            self._values["include_subgroups"] = include_subgroups
        if max_queryable_pages is not None:
            self._values["max_queryable_pages"] = max_queryable_pages
        if membership is not None:
            self._values["membership"] = membership
        if min_access_level is not None:
            self._values["min_access_level"] = min_access_level
        if order_by is not None:
            self._values["order_by"] = order_by
        if owned is not None:
            self._values["owned"] = owned
        if page is not None:
            self._values["page"] = page
        if per_page is not None:
            self._values["per_page"] = per_page
        if search is not None:
            self._values["search"] = search
        if simple is not None:
            self._values["simple"] = simple
        if sort is not None:
            self._values["sort"] = sort
        if starred is not None:
            self._values["starred"] = starred
        if statistics is not None:
            self._values["statistics"] = statistics
        if topic is not None:
            self._values["topic"] = topic
        if visibility is not None:
            self._values["visibility"] = visibility
        if with_custom_attributes is not None:
            self._values["with_custom_attributes"] = with_custom_attributes
        if with_issues_enabled is not None:
            self._values["with_issues_enabled"] = with_issues_enabled
        if with_merge_requests_enabled is not None:
            self._values["with_merge_requests_enabled"] = with_merge_requests_enabled
        if with_programming_language is not None:
            self._values["with_programming_language"] = with_programming_language
        if with_shared is not None:
            self._values["with_shared"] = with_shared

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
    def archived(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Limit by archived status.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#archived DataGitlabProjects#archived}
        '''
        result = self._values.get("archived")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def group_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of the group owned by the authenticated user to look projects for within.

        Cannot be used with ``min_access_level``, ``with_programming_language`` or ``statistics``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#group_id DataGitlabProjects#group_id}
        '''
        result = self._values.get("group_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#id DataGitlabProjects#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_subgroups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Include projects in subgroups of this group. Default is ``false``. Needs ``group_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#include_subgroups DataGitlabProjects#include_subgroups}
        '''
        result = self._values.get("include_subgroups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_queryable_pages(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of project results pages that may be queried.

        Prevents overloading your Gitlab instance in case of a misconfiguration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#max_queryable_pages DataGitlabProjects#max_queryable_pages}
        '''
        result = self._values.get("max_queryable_pages")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def membership(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Limit by projects that the current user is a member of.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#membership DataGitlabProjects#membership}
        '''
        result = self._values.get("membership")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def min_access_level(self) -> typing.Optional[jsii.Number]:
        '''Limit to projects where current user has at least this access level, refer to the `official documentation <https://docs.gitlab.com/api/members/>`_ for values. Cannot be used with ``group_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#min_access_level DataGitlabProjects#min_access_level}
        '''
        result = self._values.get("min_access_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def order_by(self) -> typing.Optional[builtins.str]:
        '''Return projects ordered ordered by: ``id``, ``name``, ``path``, ``created_at``, ``updated_at``, ``last_activity_at``, ``similarity``, ``repository_size``, ``storage_size``, ``packages_size``, ``wiki_size``.

        Some values or only available in certain circumstances. See `upstream docs <https://docs.gitlab.com/api/projects/#list-all-projects>`_ for details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#order_by DataGitlabProjects#order_by}
        '''
        result = self._values.get("order_by")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owned(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Limit by projects owned by the current user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#owned DataGitlabProjects#owned}
        '''
        result = self._values.get("owned")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def page(self) -> typing.Optional[jsii.Number]:
        '''The first page to begin the query on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#page DataGitlabProjects#page}
        '''
        result = self._values.get("page")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def per_page(self) -> typing.Optional[jsii.Number]:
        '''The number of results to return per page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#per_page DataGitlabProjects#per_page}
        '''
        result = self._values.get("per_page")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def search(self) -> typing.Optional[builtins.str]:
        '''Return list of authorized projects matching the search criteria.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#search DataGitlabProjects#search}
        '''
        result = self._values.get("search")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def simple(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Return only the ID, URL, name, and path of each project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#simple DataGitlabProjects#simple}
        '''
        result = self._values.get("simple")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sort(self) -> typing.Optional[builtins.str]:
        '''Return projects sorted in ``asc`` or ``desc`` order. Default is ``desc``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#sort DataGitlabProjects#sort}
        '''
        result = self._values.get("sort")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def starred(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Limit by projects starred by the current user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#starred DataGitlabProjects#starred}
        '''
        result = self._values.get("starred")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def statistics(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Include project statistics. Cannot be used with ``group_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#statistics DataGitlabProjects#statistics}
        '''
        result = self._values.get("statistics")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def topic(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Limit by projects that have all of the given topics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#topic DataGitlabProjects#topic}
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def visibility(self) -> typing.Optional[builtins.str]:
        '''Limit by visibility ``public``, ``internal``, or ``private``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#visibility DataGitlabProjects#visibility}
        '''
        result = self._values.get("visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def with_custom_attributes(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Include custom attributes in response *(admins only)*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#with_custom_attributes DataGitlabProjects#with_custom_attributes}
        '''
        result = self._values.get("with_custom_attributes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def with_issues_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Limit by projects with issues feature enabled. Default is ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#with_issues_enabled DataGitlabProjects#with_issues_enabled}
        '''
        result = self._values.get("with_issues_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def with_merge_requests_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Limit by projects with merge requests feature enabled. Default is ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#with_merge_requests_enabled DataGitlabProjects#with_merge_requests_enabled}
        '''
        result = self._values.get("with_merge_requests_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def with_programming_language(self) -> typing.Optional[builtins.str]:
        '''Limit by projects which use the given programming language. Cannot be used with ``group_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#with_programming_language DataGitlabProjects#with_programming_language}
        '''
        result = self._values.get("with_programming_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def with_shared(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Include projects shared to this group. Default is ``true``. Needs ``group_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/data-sources/projects#with_shared DataGitlabProjects#with_shared}
        '''
        result = self._values.get("with_shared")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGitlabProjectsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsProjects",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGitlabProjectsProjects:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGitlabProjectsProjects(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsProjectsContainerExpirationPolicy",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGitlabProjectsProjectsContainerExpirationPolicy:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGitlabProjectsProjectsContainerExpirationPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGitlabProjectsProjectsContainerExpirationPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsProjectsContainerExpirationPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d968315069d70fcc08b1e273e530cc3840c6dd7e671f78555ac82bb0e277e526)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGitlabProjectsProjectsContainerExpirationPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9b17e180c9b526eddb5cb10d990c0f789d8a9cb50de3213ff1a19dd12405f63)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGitlabProjectsProjectsContainerExpirationPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__881af90724855aa7ff25f180079ab5b7a5dccb2acbb0230cd1c18edf6334eda6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f44bf929f85390d8a783811e3486b0d71aa32c5f636fb8c3e1fb65c1a6e06f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cce16fcbb926c42e88876fad26829f320a97c8199f2de02feea1bb626591642)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGitlabProjectsProjectsContainerExpirationPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsProjectsContainerExpirationPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__208f4ad63eee55c5fb15b83f8bf80762a24e635e52821cceb77abb29906ec040)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="cadence")
    def cadence(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cadence"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="keepN")
    def keep_n(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keepN"))

    @builtins.property
    @jsii.member(jsii_name="nameRegex")
    def name_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameRegex"))

    @builtins.property
    @jsii.member(jsii_name="nameRegexDelete")
    def name_regex_delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameRegexDelete"))

    @builtins.property
    @jsii.member(jsii_name="nameRegexKeep")
    def name_regex_keep(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameRegexKeep"))

    @builtins.property
    @jsii.member(jsii_name="nextRunAt")
    def next_run_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextRunAt"))

    @builtins.property
    @jsii.member(jsii_name="olderThan")
    def older_than(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "olderThan"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGitlabProjectsProjectsContainerExpirationPolicy]:
        return typing.cast(typing.Optional[DataGitlabProjectsProjectsContainerExpirationPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGitlabProjectsProjectsContainerExpirationPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdcce1c37f42800e20944854b6cb8b19236bf652ef63c5e888b13266c94fd813)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsProjectsForkedFromProject",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGitlabProjectsProjectsForkedFromProject:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGitlabProjectsProjectsForkedFromProject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGitlabProjectsProjectsForkedFromProjectList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsProjectsForkedFromProjectList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5cff5766a0d75771bb8729b7e030ea3b1ee6eeb247ccffa3f09bc6284e32d31)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGitlabProjectsProjectsForkedFromProjectOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__318fe0e652048e610200e65d4e6e11a4650e4d4d8ff98db152df5b2d73cfdb62)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGitlabProjectsProjectsForkedFromProjectOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e24ab2771939d7cb53e382177c0cc33dd9b04de262f6f13e52054e9eb01eac2c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__884f1a8f02f3627d3b891da92a05d3e8246cc7a5a0ccdef7e8e2c86ac2e19bb6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50639bdd48a47bba93c25dd616ac1d755481a58547c61bf99c0fe4e7ab3e452c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGitlabProjectsProjectsForkedFromProjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsProjectsForkedFromProjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ea2764a24f0cb7be49676755c7c56db391a5274291b03b6796eefde6e90daba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="httpUrlToRepo")
    def http_url_to_repo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpUrlToRepo"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="nameWithNamespace")
    def name_with_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameWithNamespace"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="pathWithNamespace")
    def path_with_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathWithNamespace"))

    @builtins.property
    @jsii.member(jsii_name="webUrl")
    def web_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webUrl"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGitlabProjectsProjectsForkedFromProject]:
        return typing.cast(typing.Optional[DataGitlabProjectsProjectsForkedFromProject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGitlabProjectsProjectsForkedFromProject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58a1b35226d9eb9eb82eb4bdaaaf46d00314b42dcf0b1fbf76dcdd4697778a6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataGitlabProjectsProjectsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsProjectsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9868ac8c3ae43156ef67dbe5177ec484ad4f9da354b77903ce21b71ddc568f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataGitlabProjectsProjectsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f4789a019408a5b9ca448085849e430a1b439a0752726054b882a0262b7b642)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGitlabProjectsProjectsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85e699a0296619c33d8e65613255f34ecf3fac15d31909bc811eefa0eb2c2725)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73e96d1c82fcf04a137dbe8e0bfa26ff4bd8144fbcd397d15a184f01a150a96b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b68f8218b227d742c3def21cec26c0837feb056c0ae555725838d3b8b4f3491c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsProjectsNamespace",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGitlabProjectsProjectsNamespace:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGitlabProjectsProjectsNamespace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGitlabProjectsProjectsNamespaceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsProjectsNamespaceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cd2b56e20fb872b94bfc1dc055bd6ed4a53dd526d9106360faede0bb0ad15f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGitlabProjectsProjectsNamespaceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35f87e75db6670ecdf95847bc88c12247594a11b4e671f30d7a87f3f238fa2b9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGitlabProjectsProjectsNamespaceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b72b893284dce2c6d6dbdf5e6e48b08090b1765dac907643193afcb2bf7bac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6604f9c50a6c7319f356ce4076092d13e5b87a79353863de205b5441563d8528)
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
            type_hints = typing.get_type_hints(_typecheckingstub__662d5691f8cb9c7d0a651069c6a2e9ff43a0edfa0e1f8d807d22ddcbf74abc8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGitlabProjectsProjectsNamespaceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsProjectsNamespaceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c210ac36f5587e83f4856f38a8e4e590fe39c01939accced374e471ad28122c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="fullPath")
    def full_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullPath"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataGitlabProjectsProjectsNamespace]:
        return typing.cast(typing.Optional[DataGitlabProjectsProjectsNamespace], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGitlabProjectsProjectsNamespace],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b416e777df02a08ecc0425a16f4bf9b66ad658830fdf298f082ae1aa253debaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataGitlabProjectsProjectsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsProjectsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f3a2e020e3f79cdde8ee4b20174880e7c8aadb2259b6f8d97a164e6295ce0e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allowMergeOnSkippedPipeline")
    def allow_merge_on_skipped_pipeline(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "allowMergeOnSkippedPipeline"))

    @builtins.property
    @jsii.member(jsii_name="allowPipelineTriggerApproveDeployment")
    def allow_pipeline_trigger_approve_deployment(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "allowPipelineTriggerApproveDeployment"))

    @builtins.property
    @jsii.member(jsii_name="analyticsAccessLevel")
    def analytics_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "analyticsAccessLevel"))

    @builtins.property
    @jsii.member(jsii_name="approvalsBeforeMerge")
    def approvals_before_merge(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "approvalsBeforeMerge"))

    @builtins.property
    @jsii.member(jsii_name="archived")
    def archived(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "archived"))

    @builtins.property
    @jsii.member(jsii_name="autoCancelPendingPipelines")
    def auto_cancel_pending_pipelines(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoCancelPendingPipelines"))

    @builtins.property
    @jsii.member(jsii_name="autocloseReferencedIssues")
    def autoclose_referenced_issues(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "autocloseReferencedIssues"))

    @builtins.property
    @jsii.member(jsii_name="autoDevopsDeployStrategy")
    def auto_devops_deploy_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoDevopsDeployStrategy"))

    @builtins.property
    @jsii.member(jsii_name="autoDevopsEnabled")
    def auto_devops_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "autoDevopsEnabled"))

    @builtins.property
    @jsii.member(jsii_name="avatarUrl")
    def avatar_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "avatarUrl"))

    @builtins.property
    @jsii.member(jsii_name="buildCoverageRegex")
    def build_coverage_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildCoverageRegex"))

    @builtins.property
    @jsii.member(jsii_name="buildGitStrategy")
    def build_git_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildGitStrategy"))

    @builtins.property
    @jsii.member(jsii_name="buildsAccessLevel")
    def builds_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildsAccessLevel"))

    @builtins.property
    @jsii.member(jsii_name="buildTimeout")
    def build_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "buildTimeout"))

    @builtins.property
    @jsii.member(jsii_name="ciConfigPath")
    def ci_config_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ciConfigPath"))

    @builtins.property
    @jsii.member(jsii_name="ciDefaultGitDepth")
    def ci_default_git_depth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ciDefaultGitDepth"))

    @builtins.property
    @jsii.member(jsii_name="ciDeletePipelinesInSeconds")
    def ci_delete_pipelines_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ciDeletePipelinesInSeconds"))

    @builtins.property
    @jsii.member(jsii_name="ciForwardDeploymentEnabled")
    def ci_forward_deployment_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "ciForwardDeploymentEnabled"))

    @builtins.property
    @jsii.member(jsii_name="ciIdTokenSubClaimComponents")
    def ci_id_token_sub_claim_components(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ciIdTokenSubClaimComponents"))

    @builtins.property
    @jsii.member(jsii_name="ciPipelineVariablesMinimumOverrideRole")
    def ci_pipeline_variables_minimum_override_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ciPipelineVariablesMinimumOverrideRole"))

    @builtins.property
    @jsii.member(jsii_name="ciRestrictPipelineCancellationRole")
    def ci_restrict_pipeline_cancellation_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ciRestrictPipelineCancellationRole"))

    @builtins.property
    @jsii.member(jsii_name="containerExpirationPolicy")
    def container_expiration_policy(
        self,
    ) -> DataGitlabProjectsProjectsContainerExpirationPolicyList:
        return typing.cast(DataGitlabProjectsProjectsContainerExpirationPolicyList, jsii.get(self, "containerExpirationPolicy"))

    @builtins.property
    @jsii.member(jsii_name="containerRegistryAccessLevel")
    def container_registry_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerRegistryAccessLevel"))

    @builtins.property
    @jsii.member(jsii_name="containerRegistryEnabled")
    def container_registry_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "containerRegistryEnabled"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="creatorId")
    def creator_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "creatorId"))

    @builtins.property
    @jsii.member(jsii_name="customAttributes")
    def custom_attributes(self) -> _cdktf_9a9027ec.StringMapList:
        return typing.cast(_cdktf_9a9027ec.StringMapList, jsii.get(self, "customAttributes"))

    @builtins.property
    @jsii.member(jsii_name="defaultBranch")
    def default_branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultBranch"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="emailsEnabled")
    def emails_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "emailsEnabled"))

    @builtins.property
    @jsii.member(jsii_name="emptyRepo")
    def empty_repo(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "emptyRepo"))

    @builtins.property
    @jsii.member(jsii_name="environmentsAccessLevel")
    def environments_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environmentsAccessLevel"))

    @builtins.property
    @jsii.member(jsii_name="externalAuthorizationClassificationLabel")
    def external_authorization_classification_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalAuthorizationClassificationLabel"))

    @builtins.property
    @jsii.member(jsii_name="featureFlagsAccessLevel")
    def feature_flags_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "featureFlagsAccessLevel"))

    @builtins.property
    @jsii.member(jsii_name="forkedFromProject")
    def forked_from_project(self) -> DataGitlabProjectsProjectsForkedFromProjectList:
        return typing.cast(DataGitlabProjectsProjectsForkedFromProjectList, jsii.get(self, "forkedFromProject"))

    @builtins.property
    @jsii.member(jsii_name="forkingAccessLevel")
    def forking_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forkingAccessLevel"))

    @builtins.property
    @jsii.member(jsii_name="forksCount")
    def forks_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "forksCount"))

    @builtins.property
    @jsii.member(jsii_name="groupRunnersEnabled")
    def group_runners_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "groupRunnersEnabled"))

    @builtins.property
    @jsii.member(jsii_name="httpUrlToRepo")
    def http_url_to_repo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpUrlToRepo"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="importError")
    def import_error(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "importError"))

    @builtins.property
    @jsii.member(jsii_name="importStatus")
    def import_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "importStatus"))

    @builtins.property
    @jsii.member(jsii_name="importUrl")
    def import_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "importUrl"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureAccessLevel")
    def infrastructure_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "infrastructureAccessLevel"))

    @builtins.property
    @jsii.member(jsii_name="issuesAccessLevel")
    def issues_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuesAccessLevel"))

    @builtins.property
    @jsii.member(jsii_name="issuesEnabled")
    def issues_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "issuesEnabled"))

    @builtins.property
    @jsii.member(jsii_name="jobsEnabled")
    def jobs_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "jobsEnabled"))

    @builtins.property
    @jsii.member(jsii_name="keepLatestArtifact")
    def keep_latest_artifact(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "keepLatestArtifact"))

    @builtins.property
    @jsii.member(jsii_name="lastActivityAt")
    def last_activity_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastActivityAt"))

    @builtins.property
    @jsii.member(jsii_name="lfsEnabled")
    def lfs_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "lfsEnabled"))

    @builtins.property
    @jsii.member(jsii_name="links")
    def links(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "links"))

    @builtins.property
    @jsii.member(jsii_name="mergeCommitTemplate")
    def merge_commit_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mergeCommitTemplate"))

    @builtins.property
    @jsii.member(jsii_name="mergeMethod")
    def merge_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mergeMethod"))

    @builtins.property
    @jsii.member(jsii_name="mergePipelinesEnabled")
    def merge_pipelines_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "mergePipelinesEnabled"))

    @builtins.property
    @jsii.member(jsii_name="mergeRequestsAccessLevel")
    def merge_requests_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mergeRequestsAccessLevel"))

    @builtins.property
    @jsii.member(jsii_name="mergeRequestsEnabled")
    def merge_requests_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "mergeRequestsEnabled"))

    @builtins.property
    @jsii.member(jsii_name="mergeTrainsEnabled")
    def merge_trains_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "mergeTrainsEnabled"))

    @builtins.property
    @jsii.member(jsii_name="mirror")
    def mirror(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "mirror"))

    @builtins.property
    @jsii.member(jsii_name="mirrorOverwritesDivergedBranches")
    def mirror_overwrites_diverged_branches(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "mirrorOverwritesDivergedBranches"))

    @builtins.property
    @jsii.member(jsii_name="mirrorTriggerBuilds")
    def mirror_trigger_builds(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "mirrorTriggerBuilds"))

    @builtins.property
    @jsii.member(jsii_name="mirrorUserId")
    def mirror_user_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mirrorUserId"))

    @builtins.property
    @jsii.member(jsii_name="modelExperimentsAccessLevel")
    def model_experiments_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelExperimentsAccessLevel"))

    @builtins.property
    @jsii.member(jsii_name="modelRegistryAccessLevel")
    def model_registry_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelRegistryAccessLevel"))

    @builtins.property
    @jsii.member(jsii_name="monitorAccessLevel")
    def monitor_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monitorAccessLevel"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> DataGitlabProjectsProjectsNamespaceList:
        return typing.cast(DataGitlabProjectsProjectsNamespaceList, jsii.get(self, "namespace"))

    @builtins.property
    @jsii.member(jsii_name="nameWithNamespace")
    def name_with_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameWithNamespace"))

    @builtins.property
    @jsii.member(jsii_name="onlyAllowMergeIfAllDiscussionsAreResolved")
    def only_allow_merge_if_all_discussions_are_resolved(
        self,
    ) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "onlyAllowMergeIfAllDiscussionsAreResolved"))

    @builtins.property
    @jsii.member(jsii_name="onlyAllowMergeIfPipelineSucceeds")
    def only_allow_merge_if_pipeline_succeeds(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "onlyAllowMergeIfPipelineSucceeds"))

    @builtins.property
    @jsii.member(jsii_name="onlyMirrorProtectedBranches")
    def only_mirror_protected_branches(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "onlyMirrorProtectedBranches"))

    @builtins.property
    @jsii.member(jsii_name="openIssuesCount")
    def open_issues_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "openIssuesCount"))

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> "DataGitlabProjectsProjectsOwnerList":
        return typing.cast("DataGitlabProjectsProjectsOwnerList", jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="packagesEnabled")
    def packages_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "packagesEnabled"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="pathWithNamespace")
    def path_with_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathWithNamespace"))

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> "DataGitlabProjectsProjectsPermissionsList":
        return typing.cast("DataGitlabProjectsProjectsPermissionsList", jsii.get(self, "permissions"))

    @builtins.property
    @jsii.member(jsii_name="preventMergeWithoutJiraIssue")
    def prevent_merge_without_jira_issue(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "preventMergeWithoutJiraIssue"))

    @builtins.property
    @jsii.member(jsii_name="publicBuilds")
    def public_builds(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "publicBuilds"))

    @builtins.property
    @jsii.member(jsii_name="readmeUrl")
    def readme_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "readmeUrl"))

    @builtins.property
    @jsii.member(jsii_name="releasesAccessLevel")
    def releases_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "releasesAccessLevel"))

    @builtins.property
    @jsii.member(jsii_name="repositoryAccessLevel")
    def repository_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryAccessLevel"))

    @builtins.property
    @jsii.member(jsii_name="repositoryStorage")
    def repository_storage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryStorage"))

    @builtins.property
    @jsii.member(jsii_name="requestAccessEnabled")
    def request_access_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "requestAccessEnabled"))

    @builtins.property
    @jsii.member(jsii_name="requirementsAccessLevel")
    def requirements_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requirementsAccessLevel"))

    @builtins.property
    @jsii.member(jsii_name="resolveOutdatedDiffDiscussions")
    def resolve_outdated_diff_discussions(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "resolveOutdatedDiffDiscussions"))

    @builtins.property
    @jsii.member(jsii_name="restrictUserDefinedVariables")
    def restrict_user_defined_variables(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "restrictUserDefinedVariables"))

    @builtins.property
    @jsii.member(jsii_name="runnersToken")
    def runners_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runnersToken"))

    @builtins.property
    @jsii.member(jsii_name="securityAndComplianceAccessLevel")
    def security_and_compliance_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityAndComplianceAccessLevel"))

    @builtins.property
    @jsii.member(jsii_name="sharedRunnersEnabled")
    def shared_runners_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "sharedRunnersEnabled"))

    @builtins.property
    @jsii.member(jsii_name="sharedWithGroups")
    def shared_with_groups(self) -> "DataGitlabProjectsProjectsSharedWithGroupsList":
        return typing.cast("DataGitlabProjectsProjectsSharedWithGroupsList", jsii.get(self, "sharedWithGroups"))

    @builtins.property
    @jsii.member(jsii_name="snippetsAccessLevel")
    def snippets_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snippetsAccessLevel"))

    @builtins.property
    @jsii.member(jsii_name="snippetsEnabled")
    def snippets_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "snippetsEnabled"))

    @builtins.property
    @jsii.member(jsii_name="squashCommitTemplate")
    def squash_commit_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "squashCommitTemplate"))

    @builtins.property
    @jsii.member(jsii_name="sshUrlToRepo")
    def ssh_url_to_repo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshUrlToRepo"))

    @builtins.property
    @jsii.member(jsii_name="starCount")
    def star_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "starCount"))

    @builtins.property
    @jsii.member(jsii_name="statistics")
    def statistics(self) -> _cdktf_9a9027ec.NumberMap:
        return typing.cast(_cdktf_9a9027ec.NumberMap, jsii.get(self, "statistics"))

    @builtins.property
    @jsii.member(jsii_name="suggestionCommitMessage")
    def suggestion_commit_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suggestionCommitMessage"))

    @builtins.property
    @jsii.member(jsii_name="tagList")
    def tag_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tagList"))

    @builtins.property
    @jsii.member(jsii_name="topics")
    def topics(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "topics"))

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
    @jsii.member(jsii_name="wikiEnabled")
    def wiki_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "wikiEnabled"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataGitlabProjectsProjects]:
        return typing.cast(typing.Optional[DataGitlabProjectsProjects], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGitlabProjectsProjects],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b2adb70664bceba5874a814c230aabe3cb1df3cbafb1c127449dfda4ff32553)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsProjectsOwner",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGitlabProjectsProjectsOwner:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGitlabProjectsProjectsOwner(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGitlabProjectsProjectsOwnerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsProjectsOwnerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__beb343792a481023eb7ab424e6f5778de9e0f8e338ea4c9759c06eecf1548450)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGitlabProjectsProjectsOwnerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3f844e405d29076d354dcddeb021808a8bbe407e2b9d845273d142aba8a090a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGitlabProjectsProjectsOwnerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d487220c1e88c4a469d3718f4491f74850987f978c26326835de2b2bc97ebe75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36e565febdf85fb660ce51f950f045a48a06b0b5dabd4a3847484b248cf5cb87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e58f55dac1914ed5684269558b2365572e96c6270296916f4f5a64cc9f726c3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGitlabProjectsProjectsOwnerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsProjectsOwnerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e1591041ff093a8bfe9103af3e3fbada8669742ca01ad2d404e9d92eb44df71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="avatarUrl")
    def avatar_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "avatarUrl"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @builtins.property
    @jsii.member(jsii_name="websiteUrl")
    def website_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "websiteUrl"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataGitlabProjectsProjectsOwner]:
        return typing.cast(typing.Optional[DataGitlabProjectsProjectsOwner], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGitlabProjectsProjectsOwner],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bef58a55765ad2f6954e5d01dd5bd90bdda28f5d1f91efe0327b9ca026eaf772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsProjectsPermissions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGitlabProjectsProjectsPermissions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGitlabProjectsProjectsPermissions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGitlabProjectsProjectsPermissionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsProjectsPermissionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8cffcc65be5e033241e4f30c2d6c2ba1190b9a3b3c362044aaa90a74a6578a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGitlabProjectsProjectsPermissionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__312ad3518002f255bd9aab81eb3c75afac9212e16940d5fa868c060529303398)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGitlabProjectsProjectsPermissionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4ba2aa27452cecb9a1e19698be185d7971e23006643af55475185054c897434)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9059027b2e437c1e7cf4bdf237f9059e51351d00397a004e50ae9ecf31e75005)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae493b9fbcdffdb38bc931273911fb00573bb8c957aed543240fec66c4204d7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGitlabProjectsProjectsPermissionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsProjectsPermissionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__776acf06dfdeb283967ada148b9c9b2ad6773d03b99b62525b757b9fd3b2fc33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="groupAccess")
    def group_access(self) -> _cdktf_9a9027ec.NumberMap:
        return typing.cast(_cdktf_9a9027ec.NumberMap, jsii.get(self, "groupAccess"))

    @builtins.property
    @jsii.member(jsii_name="projectAccess")
    def project_access(self) -> _cdktf_9a9027ec.NumberMap:
        return typing.cast(_cdktf_9a9027ec.NumberMap, jsii.get(self, "projectAccess"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataGitlabProjectsProjectsPermissions]:
        return typing.cast(typing.Optional[DataGitlabProjectsProjectsPermissions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGitlabProjectsProjectsPermissions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e05003d4f1bc54513744b5083efb68c1e49e8c26f489908593925d3a25f8d13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsProjectsSharedWithGroups",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGitlabProjectsProjectsSharedWithGroups:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGitlabProjectsProjectsSharedWithGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGitlabProjectsProjectsSharedWithGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsProjectsSharedWithGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c05b7101afbe966f68f50674752620afc57a593cc22c3bf457c3d142d420974b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGitlabProjectsProjectsSharedWithGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f24cb8c16b33e0a0698ed1d03311d5d6146e286b4ecbaa7f4a0dcf0627bc310f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGitlabProjectsProjectsSharedWithGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1966a5bcd1de18aa7862545fc56dc3f3f9b89fd19a2066b5a34c9ab45d62f20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61a6be624eef6dff5a49a269f680d36f160d23d55b00302beebf6f6c1bbee2d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d038272410e0e792acc02e02ef62e066d526a453f16f41689fcd65bba5ab5ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGitlabProjectsProjectsSharedWithGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.dataGitlabProjects.DataGitlabProjectsProjectsSharedWithGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__868e4bfeffc4366cbf9c372dacd264f28f342d56ad0c39089699b41ed3b3d666)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="groupAccessLevel")
    def group_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupAccessLevel"))

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "groupId"))

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupName"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGitlabProjectsProjectsSharedWithGroups]:
        return typing.cast(typing.Optional[DataGitlabProjectsProjectsSharedWithGroups], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGitlabProjectsProjectsSharedWithGroups],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57e05dd5da5228de72a213f44bcebe1b09d3a15749332df55bfaa1ca6a2ee422)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataGitlabProjects",
    "DataGitlabProjectsConfig",
    "DataGitlabProjectsProjects",
    "DataGitlabProjectsProjectsContainerExpirationPolicy",
    "DataGitlabProjectsProjectsContainerExpirationPolicyList",
    "DataGitlabProjectsProjectsContainerExpirationPolicyOutputReference",
    "DataGitlabProjectsProjectsForkedFromProject",
    "DataGitlabProjectsProjectsForkedFromProjectList",
    "DataGitlabProjectsProjectsForkedFromProjectOutputReference",
    "DataGitlabProjectsProjectsList",
    "DataGitlabProjectsProjectsNamespace",
    "DataGitlabProjectsProjectsNamespaceList",
    "DataGitlabProjectsProjectsNamespaceOutputReference",
    "DataGitlabProjectsProjectsOutputReference",
    "DataGitlabProjectsProjectsOwner",
    "DataGitlabProjectsProjectsOwnerList",
    "DataGitlabProjectsProjectsOwnerOutputReference",
    "DataGitlabProjectsProjectsPermissions",
    "DataGitlabProjectsProjectsPermissionsList",
    "DataGitlabProjectsProjectsPermissionsOutputReference",
    "DataGitlabProjectsProjectsSharedWithGroups",
    "DataGitlabProjectsProjectsSharedWithGroupsList",
    "DataGitlabProjectsProjectsSharedWithGroupsOutputReference",
]

publication.publish()

def _typecheckingstub__993279bdb0d1ba395d8f49ee2bdc6676530aac6554fc359e0ed8694e08284e15(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    archived: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    group_id: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    include_subgroups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_queryable_pages: typing.Optional[jsii.Number] = None,
    membership: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    min_access_level: typing.Optional[jsii.Number] = None,
    order_by: typing.Optional[builtins.str] = None,
    owned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    page: typing.Optional[jsii.Number] = None,
    per_page: typing.Optional[jsii.Number] = None,
    search: typing.Optional[builtins.str] = None,
    simple: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sort: typing.Optional[builtins.str] = None,
    starred: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    statistics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    topic: typing.Optional[typing.Sequence[builtins.str]] = None,
    visibility: typing.Optional[builtins.str] = None,
    with_custom_attributes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    with_issues_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    with_merge_requests_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    with_programming_language: typing.Optional[builtins.str] = None,
    with_shared: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__17548a2ead63fa297bee57630363c7dfc3fcb868fbbb93327a057008fdc3f1f3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dde07081449ab4c4a3f7db2823f6e331b53e2bc366dd473a32ad211084e67b2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__600bbe88e991d2c73af35c710b5f51ef02527e5fdef185e68009035b874f8ed0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d099d34a2e43d6b1469b8797f900e9bb4d9a5482f9c9b83ee8adca514f97885(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a4c3d4b4fc8dfa7cde46073c5c3d24cb911f02d641c2e12ee3b209b89973ce(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac81e903034f7df8ffe7662a60d3fdaf1e0c8b5be5d9f894185701df78f38d7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ca4fe113b3f7260e86dfbc9a35b85ae8622995107fb66e1f8a166dfbbfb9e5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd8b90a0c237397b46929e0822f1fb8f970926a6c41ed7380406e568ab18ec5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7db14c905a3f6eaded4940b3d6d41bc8ce04888dcb6c0bfebe9cc5f435e37771(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4927db345addd4bcde7703610599fbe160c38000daf3d56c620344627d26dc92(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a189c6ac953f2ff8f8b648dcb6400984ace9737963653dc5573273caf40d76cc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31771985c71c50cbbedec7b4f8efe670c1c3987bb9b160dc9018084bacb6607b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a6a48386b829c18cc980baaa848ffaf35bbe53ecc2248bd0e63874284f7354(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd794144fd2b4d6bf35ee0bb6f91e1b1f9fa598d6434c61df9c7883d8237a4f3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94f972661e27efbd489074dff3b67f98ef5270e3c30a361d7d12cca655acb3fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d71025fab0cf51e83a4a27d483c356b1528acb09f31f4b42a32234ed7e6ddfa5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc364874d7548a0d3ccf3bbd3cade6a0f167a196ba066ef37595c98c4ab92a28(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc96579549159166800b38a3f8d6d37d5c3890bf203658635a0012ee8167bad(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c852665c70a28f4c642eeaf1a23537a525af0906852ece046df4badf85d4e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8611409750fd8dbb46741deecc06f1a9c744a8bc0d976b39fde27a87bb8b2d5e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60715b5c5bb67e548467a0d141d57ba7d1572318390173ef79fa798d20f24598(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d5e10b9fa60da6853aba5900c84aa5bf35cf5e9955d182f7f6418302a2aebbb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c27d87413960ec276bc9a24bc384e444a410482b2e242f90cca954c0cad3e95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2279de7e39ab30a1752ea5ede57433a01c1cc63a268f8a327c32d13d9a4aab2c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99f4ff5494815653fd2ddb374edfdee6ca2fdab397e2cdd3b99adf9781027678(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    archived: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    group_id: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    include_subgroups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_queryable_pages: typing.Optional[jsii.Number] = None,
    membership: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    min_access_level: typing.Optional[jsii.Number] = None,
    order_by: typing.Optional[builtins.str] = None,
    owned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    page: typing.Optional[jsii.Number] = None,
    per_page: typing.Optional[jsii.Number] = None,
    search: typing.Optional[builtins.str] = None,
    simple: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sort: typing.Optional[builtins.str] = None,
    starred: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    statistics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    topic: typing.Optional[typing.Sequence[builtins.str]] = None,
    visibility: typing.Optional[builtins.str] = None,
    with_custom_attributes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    with_issues_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    with_merge_requests_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    with_programming_language: typing.Optional[builtins.str] = None,
    with_shared: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d968315069d70fcc08b1e273e530cc3840c6dd7e671f78555ac82bb0e277e526(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b17e180c9b526eddb5cb10d990c0f789d8a9cb50de3213ff1a19dd12405f63(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__881af90724855aa7ff25f180079ab5b7a5dccb2acbb0230cd1c18edf6334eda6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f44bf929f85390d8a783811e3486b0d71aa32c5f636fb8c3e1fb65c1a6e06f2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cce16fcbb926c42e88876fad26829f320a97c8199f2de02feea1bb626591642(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__208f4ad63eee55c5fb15b83f8bf80762a24e635e52821cceb77abb29906ec040(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdcce1c37f42800e20944854b6cb8b19236bf652ef63c5e888b13266c94fd813(
    value: typing.Optional[DataGitlabProjectsProjectsContainerExpirationPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5cff5766a0d75771bb8729b7e030ea3b1ee6eeb247ccffa3f09bc6284e32d31(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__318fe0e652048e610200e65d4e6e11a4650e4d4d8ff98db152df5b2d73cfdb62(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e24ab2771939d7cb53e382177c0cc33dd9b04de262f6f13e52054e9eb01eac2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__884f1a8f02f3627d3b891da92a05d3e8246cc7a5a0ccdef7e8e2c86ac2e19bb6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50639bdd48a47bba93c25dd616ac1d755481a58547c61bf99c0fe4e7ab3e452c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea2764a24f0cb7be49676755c7c56db391a5274291b03b6796eefde6e90daba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58a1b35226d9eb9eb82eb4bdaaaf46d00314b42dcf0b1fbf76dcdd4697778a6e(
    value: typing.Optional[DataGitlabProjectsProjectsForkedFromProject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9868ac8c3ae43156ef67dbe5177ec484ad4f9da354b77903ce21b71ddc568f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4789a019408a5b9ca448085849e430a1b439a0752726054b882a0262b7b642(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e699a0296619c33d8e65613255f34ecf3fac15d31909bc811eefa0eb2c2725(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e96d1c82fcf04a137dbe8e0bfa26ff4bd8144fbcd397d15a184f01a150a96b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68f8218b227d742c3def21cec26c0837feb056c0ae555725838d3b8b4f3491c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd2b56e20fb872b94bfc1dc055bd6ed4a53dd526d9106360faede0bb0ad15f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35f87e75db6670ecdf95847bc88c12247594a11b4e671f30d7a87f3f238fa2b9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b72b893284dce2c6d6dbdf5e6e48b08090b1765dac907643193afcb2bf7bac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6604f9c50a6c7319f356ce4076092d13e5b87a79353863de205b5441563d8528(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662d5691f8cb9c7d0a651069c6a2e9ff43a0edfa0e1f8d807d22ddcbf74abc8d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c210ac36f5587e83f4856f38a8e4e590fe39c01939accced374e471ad28122c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b416e777df02a08ecc0425a16f4bf9b66ad658830fdf298f082ae1aa253debaa(
    value: typing.Optional[DataGitlabProjectsProjectsNamespace],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f3a2e020e3f79cdde8ee4b20174880e7c8aadb2259b6f8d97a164e6295ce0e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2adb70664bceba5874a814c230aabe3cb1df3cbafb1c127449dfda4ff32553(
    value: typing.Optional[DataGitlabProjectsProjects],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb343792a481023eb7ab424e6f5778de9e0f8e338ea4c9759c06eecf1548450(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f844e405d29076d354dcddeb021808a8bbe407e2b9d845273d142aba8a090a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d487220c1e88c4a469d3718f4491f74850987f978c26326835de2b2bc97ebe75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36e565febdf85fb660ce51f950f045a48a06b0b5dabd4a3847484b248cf5cb87(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58f55dac1914ed5684269558b2365572e96c6270296916f4f5a64cc9f726c3c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1591041ff093a8bfe9103af3e3fbada8669742ca01ad2d404e9d92eb44df71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef58a55765ad2f6954e5d01dd5bd90bdda28f5d1f91efe0327b9ca026eaf772(
    value: typing.Optional[DataGitlabProjectsProjectsOwner],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8cffcc65be5e033241e4f30c2d6c2ba1190b9a3b3c362044aaa90a74a6578a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312ad3518002f255bd9aab81eb3c75afac9212e16940d5fa868c060529303398(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ba2aa27452cecb9a1e19698be185d7971e23006643af55475185054c897434(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9059027b2e437c1e7cf4bdf237f9059e51351d00397a004e50ae9ecf31e75005(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae493b9fbcdffdb38bc931273911fb00573bb8c957aed543240fec66c4204d7a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__776acf06dfdeb283967ada148b9c9b2ad6773d03b99b62525b757b9fd3b2fc33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e05003d4f1bc54513744b5083efb68c1e49e8c26f489908593925d3a25f8d13(
    value: typing.Optional[DataGitlabProjectsProjectsPermissions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05b7101afbe966f68f50674752620afc57a593cc22c3bf457c3d142d420974b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f24cb8c16b33e0a0698ed1d03311d5d6146e286b4ecbaa7f4a0dcf0627bc310f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1966a5bcd1de18aa7862545fc56dc3f3f9b89fd19a2066b5a34c9ab45d62f20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a6be624eef6dff5a49a269f680d36f160d23d55b00302beebf6f6c1bbee2d9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d038272410e0e792acc02e02ef62e066d526a453f16f41689fcd65bba5ab5ab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868e4bfeffc4366cbf9c372dacd264f28f342d56ad0c39089699b41ed3b3d666(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57e05dd5da5228de72a213f44bcebe1b09d3a15749332df55bfaa1ca6a2ee422(
    value: typing.Optional[DataGitlabProjectsProjectsSharedWithGroups],
) -> None:
    """Type checking stubs"""
    pass
