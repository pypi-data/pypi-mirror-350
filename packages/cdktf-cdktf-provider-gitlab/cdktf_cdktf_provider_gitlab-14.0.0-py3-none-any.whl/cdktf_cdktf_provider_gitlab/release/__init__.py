r'''
# `gitlab_release`

Refer to the Terraform Registry for docs: [`gitlab_release`](https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release).
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


class Release(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.release.Release",
):
    '''Represents a {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release gitlab_release}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        project: builtins.str,
        tag_name: builtins.str,
        assets: typing.Optional[typing.Union["ReleaseAssets", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        milestones: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        ref: typing.Optional[builtins.str] = None,
        released_at: typing.Optional[builtins.str] = None,
        tag_message: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release gitlab_release} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param project: The ID or full path of the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#project Release#project}
        :param tag_name: The tag where the release is created from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#tag_name Release#tag_name}
        :param assets: The release assets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#assets Release#assets}
        :param description: The description of the release. You can use Markdown. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#description Release#description}
        :param milestones: The title of each milestone the release is associated with. GitLab Premium customers can specify group milestones. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#milestones Release#milestones}
        :param name: The name of the release. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#name Release#name}
        :param ref: If a tag specified in tag_name doesn't exist, the release is created from ref and tagged with tag_name. It can be a commit SHA, another tag name, or a branch name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#ref Release#ref}
        :param released_at: Date and time for the release. Defaults to the current time. Expected in ISO 8601 format (2019-03-15T08:00:00Z). Only provide this field if creating an upcoming or historical release. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#released_at Release#released_at}
        :param tag_message: Message to use if creating a new annotated tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#tag_message Release#tag_message}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b564bd914e99a603573e3ad0df9b8fe29db6fccbd2c45c6f0b2d3a6b60b51def)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ReleaseConfig(
            project=project,
            tag_name=tag_name,
            assets=assets,
            description=description,
            milestones=milestones,
            name=name,
            ref=ref,
            released_at=released_at,
            tag_message=tag_message,
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
        '''Generates CDKTF code for importing a Release resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Release to import.
        :param import_from_id: The id of the existing Release that should be imported. Refer to the {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Release to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f24bff3299d4a53c0eb5994dbebc3264c8dfdeeadf8d50bcb333796031fba3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAssets")
    def put_assets(self) -> None:
        value = ReleaseAssets()

        return typing.cast(None, jsii.invoke(self, "putAssets", [value]))

    @jsii.member(jsii_name="resetAssets")
    def reset_assets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssets", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetMilestones")
    def reset_milestones(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMilestones", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetRef")
    def reset_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRef", []))

    @jsii.member(jsii_name="resetReleasedAt")
    def reset_released_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReleasedAt", []))

    @jsii.member(jsii_name="resetTagMessage")
    def reset_tag_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagMessage", []))

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
    @jsii.member(jsii_name="assets")
    def assets(self) -> "ReleaseAssetsOutputReference":
        return typing.cast("ReleaseAssetsOutputReference", jsii.get(self, "assets"))

    @builtins.property
    @jsii.member(jsii_name="author")
    def author(self) -> "ReleaseAuthorOutputReference":
        return typing.cast("ReleaseAuthorOutputReference", jsii.get(self, "author"))

    @builtins.property
    @jsii.member(jsii_name="commit")
    def commit(self) -> "ReleaseCommitOutputReference":
        return typing.cast("ReleaseCommitOutputReference", jsii.get(self, "commit"))

    @builtins.property
    @jsii.member(jsii_name="commitPath")
    def commit_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitPath"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="descriptionHtml")
    def description_html(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "descriptionHtml"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="links")
    def links(self) -> "ReleaseLinksOutputReference":
        return typing.cast("ReleaseLinksOutputReference", jsii.get(self, "links"))

    @builtins.property
    @jsii.member(jsii_name="tagPath")
    def tag_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagPath"))

    @builtins.property
    @jsii.member(jsii_name="upcomingRelease")
    def upcoming_release(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "upcomingRelease"))

    @builtins.property
    @jsii.member(jsii_name="assetsInput")
    def assets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ReleaseAssets"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ReleaseAssets"]], jsii.get(self, "assetsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="milestonesInput")
    def milestones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "milestonesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="refInput")
    def ref_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "refInput"))

    @builtins.property
    @jsii.member(jsii_name="releasedAtInput")
    def released_at_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "releasedAtInput"))

    @builtins.property
    @jsii.member(jsii_name="tagMessageInput")
    def tag_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="tagNameInput")
    def tag_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagNameInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7930060644c1500e1731305fed93831fbd58acc7ed6083c63b400871fb781888)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="milestones")
    def milestones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "milestones"))

    @milestones.setter
    def milestones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba075b78c5f9efd85b304939b849d37d0f32b85ebbe09ee959b4f5bdd240891e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "milestones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__656667d2ecede2eac038475d777961f4007a807b89d11d5abb28d564843454df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__882de39eaadb3a6cda38226835228750373e09d67daa7f59913f070bd74f5dfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ref")
    def ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ref"))

    @ref.setter
    def ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa25093e42830bcdc8f1e79070b37772be87864e90321caa1873540275b3bd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ref", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="releasedAt")
    def released_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "releasedAt"))

    @released_at.setter
    def released_at(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3eac672bf94189680fa7b0e96d778671be9f83a85d42fe9865c2e61c7ca4713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "releasedAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagMessage")
    def tag_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagMessage"))

    @tag_message.setter
    def tag_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ddbee2892ae55e745e4dd591fe316966740807b40ae5ec69df2f7438b1f526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagName")
    def tag_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagName"))

    @tag_name.setter
    def tag_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12218af224c0f7b0a6de2db98dab1c1690c2a9085d015cf2670b0af773189051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.release.ReleaseAssets",
    jsii_struct_bases=[],
    name_mapping={},
)
class ReleaseAssets:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseAssets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReleaseAssetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.release.ReleaseAssetsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f5a33ef1587ff7c70a55d24d3a3452eb00e10d2dd308cf925e8de6662f4506b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleaseAssets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleaseAssets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleaseAssets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95228f125da5f3a31addd5dd763e0b864e030f84e0ad8f26135c49d50e56a088)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.release.ReleaseAuthor",
    jsii_struct_bases=[],
    name_mapping={},
)
class ReleaseAuthor:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseAuthor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReleaseAuthorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.release.ReleaseAuthorOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcca1eefcc13090b301123b76de340333c6701cac06015c501db601ee872280a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
    @jsii.member(jsii_name="webUrl")
    def web_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webUrl"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ReleaseAuthor]:
        return typing.cast(typing.Optional[ReleaseAuthor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ReleaseAuthor]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0acba86261777ea0523607580003d3bb4a3a37ac6a33a48ef8b252c286dc5cd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.release.ReleaseCommit",
    jsii_struct_bases=[],
    name_mapping={},
)
class ReleaseCommit:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseCommit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReleaseCommitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.release.ReleaseCommitOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b91d841397024d7f369f62016ef0df08e42cb3ae6657898370f9b8fab00ec5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="authoredDate")
    def authored_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authoredDate"))

    @builtins.property
    @jsii.member(jsii_name="authorEmail")
    def author_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorEmail"))

    @builtins.property
    @jsii.member(jsii_name="authorName")
    def author_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorName"))

    @builtins.property
    @jsii.member(jsii_name="committedDate")
    def committed_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "committedDate"))

    @builtins.property
    @jsii.member(jsii_name="committerEmail")
    def committer_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "committerEmail"))

    @builtins.property
    @jsii.member(jsii_name="committerName")
    def committer_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "committerName"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="parentIds")
    def parent_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "parentIds"))

    @builtins.property
    @jsii.member(jsii_name="shortId")
    def short_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shortId"))

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ReleaseCommit]:
        return typing.cast(typing.Optional[ReleaseCommit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ReleaseCommit]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97cb2a95dbb863c263c718cde6267e6eb1d69ef1bfdbb130d5653d16d06f6737)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.release.ReleaseConfig",
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
        "tag_name": "tagName",
        "assets": "assets",
        "description": "description",
        "milestones": "milestones",
        "name": "name",
        "ref": "ref",
        "released_at": "releasedAt",
        "tag_message": "tagMessage",
    },
)
class ReleaseConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        tag_name: builtins.str,
        assets: typing.Optional[typing.Union[ReleaseAssets, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        milestones: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        ref: typing.Optional[builtins.str] = None,
        released_at: typing.Optional[builtins.str] = None,
        tag_message: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param project: The ID or full path of the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#project Release#project}
        :param tag_name: The tag where the release is created from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#tag_name Release#tag_name}
        :param assets: The release assets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#assets Release#assets}
        :param description: The description of the release. You can use Markdown. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#description Release#description}
        :param milestones: The title of each milestone the release is associated with. GitLab Premium customers can specify group milestones. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#milestones Release#milestones}
        :param name: The name of the release. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#name Release#name}
        :param ref: If a tag specified in tag_name doesn't exist, the release is created from ref and tagged with tag_name. It can be a commit SHA, another tag name, or a branch name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#ref Release#ref}
        :param released_at: Date and time for the release. Defaults to the current time. Expected in ISO 8601 format (2019-03-15T08:00:00Z). Only provide this field if creating an upcoming or historical release. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#released_at Release#released_at}
        :param tag_message: Message to use if creating a new annotated tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#tag_message Release#tag_message}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(assets, dict):
            assets = ReleaseAssets(**assets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f12608c6970ca975d0d231928dbc848fac26089477ca0e01037dedbe336f6037)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
            check_type(argname="argument assets", value=assets, expected_type=type_hints["assets"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument milestones", value=milestones, expected_type=type_hints["milestones"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
            check_type(argname="argument released_at", value=released_at, expected_type=type_hints["released_at"])
            check_type(argname="argument tag_message", value=tag_message, expected_type=type_hints["tag_message"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project": project,
            "tag_name": tag_name,
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
        if assets is not None:
            self._values["assets"] = assets
        if description is not None:
            self._values["description"] = description
        if milestones is not None:
            self._values["milestones"] = milestones
        if name is not None:
            self._values["name"] = name
        if ref is not None:
            self._values["ref"] = ref
        if released_at is not None:
            self._values["released_at"] = released_at
        if tag_message is not None:
            self._values["tag_message"] = tag_message

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
        '''The ID or full path of the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#project Release#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag_name(self) -> builtins.str:
        '''The tag where the release is created from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#tag_name Release#tag_name}
        '''
        result = self._values.get("tag_name")
        assert result is not None, "Required property 'tag_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def assets(self) -> typing.Optional[ReleaseAssets]:
        '''The release assets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#assets Release#assets}
        '''
        result = self._values.get("assets")
        return typing.cast(typing.Optional[ReleaseAssets], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the release. You can use Markdown.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#description Release#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def milestones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The title of each milestone the release is associated with. GitLab Premium customers can specify group milestones.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#milestones Release#milestones}
        '''
        result = self._values.get("milestones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the release.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#name Release#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ref(self) -> typing.Optional[builtins.str]:
        '''If a tag specified in tag_name doesn't exist, the release is created from ref and tagged with tag_name.

        It can be a commit SHA, another tag name, or a branch name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#ref Release#ref}
        '''
        result = self._values.get("ref")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def released_at(self) -> typing.Optional[builtins.str]:
        '''Date and time for the release.

        Defaults to the current time. Expected in ISO 8601 format (2019-03-15T08:00:00Z). Only provide this field if creating an upcoming or historical release.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#released_at Release#released_at}
        '''
        result = self._values.get("released_at")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_message(self) -> typing.Optional[builtins.str]:
        '''Message to use if creating a new annotated tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/release#tag_message Release#tag_message}
        '''
        result = self._values.get("tag_message")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.release.ReleaseLinks",
    jsii_struct_bases=[],
    name_mapping={},
)
class ReleaseLinks:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseLinks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReleaseLinksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.release.ReleaseLinksOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e4079cf0758e4a1d1ae80ffb1dd70e27f9ddb4d32078896fb56d493c7b4f0d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="closedIssuesUrl")
    def closed_issues_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "closedIssuesUrl"))

    @builtins.property
    @jsii.member(jsii_name="closedMergeRequestsUrl")
    def closed_merge_requests_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "closedMergeRequestsUrl"))

    @builtins.property
    @jsii.member(jsii_name="editUrl")
    def edit_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "editUrl"))

    @builtins.property
    @jsii.member(jsii_name="mergedMergeRequestsUrl")
    def merged_merge_requests_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mergedMergeRequestsUrl"))

    @builtins.property
    @jsii.member(jsii_name="openedIssuesUrl")
    def opened_issues_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "openedIssuesUrl"))

    @builtins.property
    @jsii.member(jsii_name="openedMergeRequestsUrl")
    def opened_merge_requests_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "openedMergeRequestsUrl"))

    @builtins.property
    @jsii.member(jsii_name="selfAttribute")
    def self_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfAttribute"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ReleaseLinks]:
        return typing.cast(typing.Optional[ReleaseLinks], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ReleaseLinks]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccbd9ae533d86f0dd7092a3111c30ad73308ffb666d76473624467b39b59aeaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Release",
    "ReleaseAssets",
    "ReleaseAssetsOutputReference",
    "ReleaseAuthor",
    "ReleaseAuthorOutputReference",
    "ReleaseCommit",
    "ReleaseCommitOutputReference",
    "ReleaseConfig",
    "ReleaseLinks",
    "ReleaseLinksOutputReference",
]

publication.publish()

def _typecheckingstub__b564bd914e99a603573e3ad0df9b8fe29db6fccbd2c45c6f0b2d3a6b60b51def(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    project: builtins.str,
    tag_name: builtins.str,
    assets: typing.Optional[typing.Union[ReleaseAssets, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    milestones: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    ref: typing.Optional[builtins.str] = None,
    released_at: typing.Optional[builtins.str] = None,
    tag_message: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__d1f24bff3299d4a53c0eb5994dbebc3264c8dfdeeadf8d50bcb333796031fba3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7930060644c1500e1731305fed93831fbd58acc7ed6083c63b400871fb781888(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba075b78c5f9efd85b304939b849d37d0f32b85ebbe09ee959b4f5bdd240891e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__656667d2ecede2eac038475d777961f4007a807b89d11d5abb28d564843454df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882de39eaadb3a6cda38226835228750373e09d67daa7f59913f070bd74f5dfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa25093e42830bcdc8f1e79070b37772be87864e90321caa1873540275b3bd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3eac672bf94189680fa7b0e96d778671be9f83a85d42fe9865c2e61c7ca4713(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ddbee2892ae55e745e4dd591fe316966740807b40ae5ec69df2f7438b1f526(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12218af224c0f7b0a6de2db98dab1c1690c2a9085d015cf2670b0af773189051(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f5a33ef1587ff7c70a55d24d3a3452eb00e10d2dd308cf925e8de6662f4506b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95228f125da5f3a31addd5dd763e0b864e030f84e0ad8f26135c49d50e56a088(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleaseAssets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcca1eefcc13090b301123b76de340333c6701cac06015c501db601ee872280a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0acba86261777ea0523607580003d3bb4a3a37ac6a33a48ef8b252c286dc5cd6(
    value: typing.Optional[ReleaseAuthor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b91d841397024d7f369f62016ef0df08e42cb3ae6657898370f9b8fab00ec5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97cb2a95dbb863c263c718cde6267e6eb1d69ef1bfdbb130d5653d16d06f6737(
    value: typing.Optional[ReleaseCommit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f12608c6970ca975d0d231928dbc848fac26089477ca0e01037dedbe336f6037(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: builtins.str,
    tag_name: builtins.str,
    assets: typing.Optional[typing.Union[ReleaseAssets, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    milestones: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    ref: typing.Optional[builtins.str] = None,
    released_at: typing.Optional[builtins.str] = None,
    tag_message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e4079cf0758e4a1d1ae80ffb1dd70e27f9ddb4d32078896fb56d493c7b4f0d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccbd9ae533d86f0dd7092a3111c30ad73308ffb666d76473624467b39b59aeaf(
    value: typing.Optional[ReleaseLinks],
) -> None:
    """Type checking stubs"""
    pass
