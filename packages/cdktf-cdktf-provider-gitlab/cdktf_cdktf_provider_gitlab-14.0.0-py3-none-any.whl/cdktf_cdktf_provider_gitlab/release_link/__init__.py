r'''
# `gitlab_release_link`

Refer to the Terraform Registry for docs: [`gitlab_release_link`](https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link).
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


class ReleaseLink(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.releaseLink.ReleaseLink",
):
    '''Represents a {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link gitlab_release_link}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        project: builtins.str,
        tag_name: builtins.str,
        url: builtins.str,
        filepath: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        link_type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link gitlab_release_link} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the link. Link names must be unique within the release. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#name ReleaseLink#name}
        :param project: The ID or `URL-encoded path of the project <https://docs.gitlab.com/api/index/#namespaced-path-encoding>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#project ReleaseLink#project}
        :param tag_name: The tag associated with the Release. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#tag_name ReleaseLink#tag_name}
        :param url: The URL of the link. Link URLs must be unique within the release. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#url ReleaseLink#url}
        :param filepath: Relative path for a `Direct Asset link <https://docs.gitlab.com/user/project/releases/index/#permanent-links-to-release-assets>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#filepath ReleaseLink#filepath}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#id ReleaseLink#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param link_type: The type of the link. Valid values are ``other``, ``runbook``, ``image``, ``package``. Defaults to other. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#link_type ReleaseLink#link_type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e6639a22963e6f2b8d0ef1b8571ea33a6dbeac16bd058d240637eb71e1a35f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ReleaseLinkConfig(
            name=name,
            project=project,
            tag_name=tag_name,
            url=url,
            filepath=filepath,
            id=id,
            link_type=link_type,
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
        '''Generates CDKTF code for importing a ReleaseLink resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ReleaseLink to import.
        :param import_from_id: The id of the existing ReleaseLink that should be imported. Refer to the {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ReleaseLink to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48efd47c076332da833ff61a4c2c007031f4a9ae11dd2b8b88569ce15c54e06b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetFilepath")
    def reset_filepath(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilepath", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLinkType")
    def reset_link_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinkType", []))

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
    @jsii.member(jsii_name="directAssetUrl")
    def direct_asset_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "directAssetUrl"))

    @builtins.property
    @jsii.member(jsii_name="external")
    def external(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "external"))

    @builtins.property
    @jsii.member(jsii_name="linkId")
    def link_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "linkId"))

    @builtins.property
    @jsii.member(jsii_name="filepathInput")
    def filepath_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filepathInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="linkTypeInput")
    def link_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "linkTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="tagNameInput")
    def tag_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagNameInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="filepath")
    def filepath(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filepath"))

    @filepath.setter
    def filepath(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd46b2d79ab73356c9eaae790ac2304a041ccb3bf9011d4727eccfcb63c7346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filepath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d650202cdc426a34706cc3556620dac36a6e494f126d16f44a6474edc6ce4a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="linkType")
    def link_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "linkType"))

    @link_type.setter
    def link_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__086aa1db02308fa0c983d8c0627783991bcecad459a97d52b4957b0ccc9130fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f2278464fe788472af5ae97771110d555583b3180a1e07abbb6857bf208e39a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c039944d7620a390bb2a166c06f0e3adfaeb35f41700d344c41f8f4a8b843af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagName")
    def tag_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagName"))

    @tag_name.setter
    def tag_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bec78b27770c22ba88075577aef74b922a629fe9359dc70ea7fbb815da2eb3ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__965bf276017cdac093ff723815649261f3aa062e4a604ac29b4a570cbc895fda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.releaseLink.ReleaseLinkConfig",
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
        "tag_name": "tagName",
        "url": "url",
        "filepath": "filepath",
        "id": "id",
        "link_type": "linkType",
    },
)
class ReleaseLinkConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        tag_name: builtins.str,
        url: builtins.str,
        filepath: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        link_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the link. Link names must be unique within the release. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#name ReleaseLink#name}
        :param project: The ID or `URL-encoded path of the project <https://docs.gitlab.com/api/index/#namespaced-path-encoding>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#project ReleaseLink#project}
        :param tag_name: The tag associated with the Release. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#tag_name ReleaseLink#tag_name}
        :param url: The URL of the link. Link URLs must be unique within the release. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#url ReleaseLink#url}
        :param filepath: Relative path for a `Direct Asset link <https://docs.gitlab.com/user/project/releases/index/#permanent-links-to-release-assets>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#filepath ReleaseLink#filepath}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#id ReleaseLink#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param link_type: The type of the link. Valid values are ``other``, ``runbook``, ``image``, ``package``. Defaults to other. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#link_type ReleaseLink#link_type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e57a918cf6b7bf9e2ea75fa23c6d3773d5d335bbd2f988c6aceda43ac4c9444)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument filepath", value=filepath, expected_type=type_hints["filepath"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument link_type", value=link_type, expected_type=type_hints["link_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "project": project,
            "tag_name": tag_name,
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
        if filepath is not None:
            self._values["filepath"] = filepath
        if id is not None:
            self._values["id"] = id
        if link_type is not None:
            self._values["link_type"] = link_type

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
        '''The name of the link. Link names must be unique within the release.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#name ReleaseLink#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''The ID or `URL-encoded path of the project <https://docs.gitlab.com/api/index/#namespaced-path-encoding>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#project ReleaseLink#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag_name(self) -> builtins.str:
        '''The tag associated with the Release.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#tag_name ReleaseLink#tag_name}
        '''
        result = self._values.get("tag_name")
        assert result is not None, "Required property 'tag_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''The URL of the link. Link URLs must be unique within the release.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#url ReleaseLink#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filepath(self) -> typing.Optional[builtins.str]:
        '''Relative path for a `Direct Asset link <https://docs.gitlab.com/user/project/releases/index/#permanent-links-to-release-assets>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#filepath ReleaseLink#filepath}
        '''
        result = self._values.get("filepath")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#id ReleaseLink#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def link_type(self) -> typing.Optional[builtins.str]:
        '''The type of the link. Valid values are ``other``, ``runbook``, ``image``, ``package``. Defaults to other.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release_link#link_type ReleaseLink#link_type}
        '''
        result = self._values.get("link_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseLinkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ReleaseLink",
    "ReleaseLinkConfig",
]

publication.publish()

def _typecheckingstub__90e6639a22963e6f2b8d0ef1b8571ea33a6dbeac16bd058d240637eb71e1a35f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    project: builtins.str,
    tag_name: builtins.str,
    url: builtins.str,
    filepath: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    link_type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__48efd47c076332da833ff61a4c2c007031f4a9ae11dd2b8b88569ce15c54e06b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd46b2d79ab73356c9eaae790ac2304a041ccb3bf9011d4727eccfcb63c7346(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d650202cdc426a34706cc3556620dac36a6e494f126d16f44a6474edc6ce4a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__086aa1db02308fa0c983d8c0627783991bcecad459a97d52b4957b0ccc9130fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2278464fe788472af5ae97771110d555583b3180a1e07abbb6857bf208e39a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c039944d7620a390bb2a166c06f0e3adfaeb35f41700d344c41f8f4a8b843af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec78b27770c22ba88075577aef74b922a629fe9359dc70ea7fbb815da2eb3ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__965bf276017cdac093ff723815649261f3aa062e4a604ac29b4a570cbc895fda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e57a918cf6b7bf9e2ea75fa23c6d3773d5d335bbd2f988c6aceda43ac4c9444(
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
    tag_name: builtins.str,
    url: builtins.str,
    filepath: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    link_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
