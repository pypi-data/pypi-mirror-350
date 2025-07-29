r'''
# `gitlab_project`

Refer to the Terraform Registry for docs: [`gitlab_project`](https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project).
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


class Project(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.project.Project",
):
    '''Represents a {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project gitlab_project}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        allow_merge_on_skipped_pipeline: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_pipeline_trigger_approve_deployment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        analytics_access_level: typing.Optional[builtins.str] = None,
        approvals_before_merge: typing.Optional[jsii.Number] = None,
        archived: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        archive_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_cancel_pending_pipelines: typing.Optional[builtins.str] = None,
        autoclose_referenced_issues: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_devops_deploy_strategy: typing.Optional[builtins.str] = None,
        auto_devops_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        avatar: typing.Optional[builtins.str] = None,
        avatar_hash: typing.Optional[builtins.str] = None,
        build_coverage_regex: typing.Optional[builtins.str] = None,
        build_git_strategy: typing.Optional[builtins.str] = None,
        builds_access_level: typing.Optional[builtins.str] = None,
        build_timeout: typing.Optional[jsii.Number] = None,
        ci_config_path: typing.Optional[builtins.str] = None,
        ci_default_git_depth: typing.Optional[jsii.Number] = None,
        ci_delete_pipelines_in_seconds: typing.Optional[jsii.Number] = None,
        ci_forward_deployment_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ci_id_token_sub_claim_components: typing.Optional[typing.Sequence[builtins.str]] = None,
        ci_pipeline_variables_minimum_override_role: typing.Optional[builtins.str] = None,
        ci_restrict_pipeline_cancellation_role: typing.Optional[builtins.str] = None,
        ci_separated_caches: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        container_expiration_policy: typing.Optional[typing.Union["ProjectContainerExpirationPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        container_registry_access_level: typing.Optional[builtins.str] = None,
        container_registry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_branch: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        emails_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        environments_access_level: typing.Optional[builtins.str] = None,
        external_authorization_classification_label: typing.Optional[builtins.str] = None,
        feature_flags_access_level: typing.Optional[builtins.str] = None,
        forked_from_project_id: typing.Optional[jsii.Number] = None,
        forking_access_level: typing.Optional[builtins.str] = None,
        group_runners_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        group_with_project_templates_id: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        import_url: typing.Optional[builtins.str] = None,
        import_url_password: typing.Optional[builtins.str] = None,
        import_url_username: typing.Optional[builtins.str] = None,
        infrastructure_access_level: typing.Optional[builtins.str] = None,
        initialize_with_readme: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        issues_access_level: typing.Optional[builtins.str] = None,
        issues_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        issues_template: typing.Optional[builtins.str] = None,
        keep_latest_artifact: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lfs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        merge_commit_template: typing.Optional[builtins.str] = None,
        merge_method: typing.Optional[builtins.str] = None,
        merge_pipelines_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        merge_requests_access_level: typing.Optional[builtins.str] = None,
        merge_requests_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        merge_requests_template: typing.Optional[builtins.str] = None,
        merge_trains_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mirror: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mirror_overwrites_diverged_branches: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mirror_trigger_builds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        model_experiments_access_level: typing.Optional[builtins.str] = None,
        model_registry_access_level: typing.Optional[builtins.str] = None,
        monitor_access_level: typing.Optional[builtins.str] = None,
        mr_default_target_self: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        namespace_id: typing.Optional[jsii.Number] = None,
        only_allow_merge_if_all_discussions_are_resolved: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        only_allow_merge_if_pipeline_succeeds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        only_mirror_protected_branches: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        packages_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pages_access_level: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        permanently_delete_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pipelines_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pre_receive_secret_detection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prevent_merge_without_jira_issue: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        printing_merge_request_link_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_builds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_jobs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        push_rules: typing.Optional[typing.Union["ProjectPushRules", typing.Dict[builtins.str, typing.Any]]] = None,
        releases_access_level: typing.Optional[builtins.str] = None,
        remove_source_branch_after_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        repository_access_level: typing.Optional[builtins.str] = None,
        repository_storage: typing.Optional[builtins.str] = None,
        request_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        requirements_access_level: typing.Optional[builtins.str] = None,
        resolve_outdated_diff_discussions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restrict_user_defined_variables: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_and_compliance_access_level: typing.Optional[builtins.str] = None,
        shared_runners_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_wait_for_default_branch_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        snippets_access_level: typing.Optional[builtins.str] = None,
        snippets_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        squash_commit_template: typing.Optional[builtins.str] = None,
        squash_option: typing.Optional[builtins.str] = None,
        suggestion_commit_message: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        template_name: typing.Optional[builtins.str] = None,
        template_project_id: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["ProjectTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        topics: typing.Optional[typing.Sequence[builtins.str]] = None,
        use_custom_template: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        visibility_level: typing.Optional[builtins.str] = None,
        wiki_access_level: typing.Optional[builtins.str] = None,
        wiki_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project gitlab_project} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#name Project#name}
        :param allow_merge_on_skipped_pipeline: Set to true if you want to treat skipped pipelines as if they finished with success. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#allow_merge_on_skipped_pipeline Project#allow_merge_on_skipped_pipeline}
        :param allow_pipeline_trigger_approve_deployment: Set whether or not a pipeline triggerer is allowed to approve deployments. Premium and Ultimate only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#allow_pipeline_trigger_approve_deployment Project#allow_pipeline_trigger_approve_deployment}
        :param analytics_access_level: Set the analytics access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#analytics_access_level Project#analytics_access_level}
        :param approvals_before_merge: Number of merge request approvals required for merging. Default is 0. This field **does not** work well in combination with the ``gitlab_project_approval_rule`` resource and is most likely gonna be deprecated in a future GitLab version (see `this upstream epic <https://gitlab.com/groups/gitlab-org/-/epics/7572>`_). In the meantime we recommend against using this attribute and use ``gitlab_project_approval_rule`` instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#approvals_before_merge Project#approvals_before_merge}
        :param archived: Whether the project is in read-only mode (archived). Repositories can be archived/unarchived by toggling this parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#archived Project#archived}
        :param archive_on_destroy: Set to ``true`` to archive the project instead of deleting on destroy. If set to ``true`` it will entire omit the ``DELETE`` operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#archive_on_destroy Project#archive_on_destroy}
        :param auto_cancel_pending_pipelines: Auto-cancel pending pipelines. This isn’t a boolean, but enabled/disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#auto_cancel_pending_pipelines Project#auto_cancel_pending_pipelines}
        :param autoclose_referenced_issues: Set whether auto-closing referenced issues on default branch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#autoclose_referenced_issues Project#autoclose_referenced_issues}
        :param auto_devops_deploy_strategy: Auto Deploy strategy. Valid values are ``continuous``, ``manual``, ``timed_incremental``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#auto_devops_deploy_strategy Project#auto_devops_deploy_strategy}
        :param auto_devops_enabled: Enable Auto DevOps for this project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#auto_devops_enabled Project#auto_devops_enabled}
        :param avatar: A local path to the avatar image to upload. **Note**: not available for imported resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#avatar Project#avatar}
        :param avatar_hash: The hash of the avatar image. Use ``filesha256("path/to/avatar.png")`` whenever possible. **Note**: this is used to trigger an update of the avatar. If it's not given, but an avatar is given, the avatar will be updated each time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#avatar_hash Project#avatar_hash}
        :param build_coverage_regex: Test coverage parsing for the project. This is deprecated feature in GitLab 15.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#build_coverage_regex Project#build_coverage_regex}
        :param build_git_strategy: The Git strategy. Defaults to fetch. Valid values are ``clone``, ``fetch``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#build_git_strategy Project#build_git_strategy}
        :param builds_access_level: Set the builds access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#builds_access_level Project#builds_access_level}
        :param build_timeout: The maximum amount of time, in seconds, that a job can run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#build_timeout Project#build_timeout}
        :param ci_config_path: Custom Path to CI config file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_config_path Project#ci_config_path}
        :param ci_default_git_depth: Default number of revisions for shallow cloning. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_default_git_depth Project#ci_default_git_depth}
        :param ci_delete_pipelines_in_seconds: Pipelines older than the configured time are deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_delete_pipelines_in_seconds Project#ci_delete_pipelines_in_seconds}
        :param ci_forward_deployment_enabled: When a new deployment job starts, skip older deployment jobs that are still pending. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_forward_deployment_enabled Project#ci_forward_deployment_enabled}
        :param ci_id_token_sub_claim_components: Fields included in the sub claim of the ID Token. Accepts an array starting with project_path. The array might also include ref_type and ref. Defaults to ["project_path", "ref_type", "ref"]. Introduced in GitLab 17.10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_id_token_sub_claim_components Project#ci_id_token_sub_claim_components}
        :param ci_pipeline_variables_minimum_override_role: The minimum role required to set variables when running pipelines and jobs. Introduced in GitLab 17.1. Valid values are ``developer``, ``maintainer``, ``owner``, ``no_one_allowed`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_pipeline_variables_minimum_override_role Project#ci_pipeline_variables_minimum_override_role}
        :param ci_restrict_pipeline_cancellation_role: The role required to cancel a pipeline or job. Premium and Ultimate only. Valid values are ``developer``, ``maintainer``, ``no one`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_restrict_pipeline_cancellation_role Project#ci_restrict_pipeline_cancellation_role}
        :param ci_separated_caches: Use separate caches for protected branches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_separated_caches Project#ci_separated_caches}
        :param container_expiration_policy: container_expiration_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#container_expiration_policy Project#container_expiration_policy}
        :param container_registry_access_level: Set visibility of container registry, for this project. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#container_registry_access_level Project#container_registry_access_level}
        :param container_registry_enabled: Enable container registry for the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#container_registry_enabled Project#container_registry_enabled}
        :param default_branch: The default branch for the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#default_branch Project#default_branch}
        :param description: A description of the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#description Project#description}
        :param emails_enabled: Enable email notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#emails_enabled Project#emails_enabled}
        :param environments_access_level: Set the environments access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#environments_access_level Project#environments_access_level}
        :param external_authorization_classification_label: The classification label for the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#external_authorization_classification_label Project#external_authorization_classification_label}
        :param feature_flags_access_level: Set the feature flags access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#feature_flags_access_level Project#feature_flags_access_level}
        :param forked_from_project_id: The id of the project to fork. During create the project is forked and during an update the fork relation is changed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#forked_from_project_id Project#forked_from_project_id}
        :param forking_access_level: Set the forking access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#forking_access_level Project#forking_access_level}
        :param group_runners_enabled: Enable group runners for this project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#group_runners_enabled Project#group_runners_enabled}
        :param group_with_project_templates_id: For group-level custom templates, specifies ID of group from which all the custom project templates are sourced. Leave empty for instance-level templates. Requires use_custom_template to be true (enterprise edition). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#group_with_project_templates_id Project#group_with_project_templates_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#id Project#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param import_url: Git URL to a repository to be imported. Together with ``mirror = true`` it will setup a Pull Mirror. This can also be used together with ``forked_from_project_id`` to setup a Pull Mirror for a fork. The fork takes precedence over the import. Make sure to provide the credentials in ``import_url_username`` and ``import_url_password``. GitLab never returns the credentials, thus the provider cannot detect configuration drift in the credentials. They can also not be imported using ``terraform import``. See the examples section for how to properly use it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#import_url Project#import_url}
        :param import_url_password: The password for the ``import_url``. The value of this field is used to construct a valid ``import_url`` and is only related to the provider. This field cannot be imported using ``terraform import``. See the examples section for how to properly use it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#import_url_password Project#import_url_password}
        :param import_url_username: The username for the ``import_url``. The value of this field is used to construct a valid ``import_url`` and is only related to the provider. This field cannot be imported using ``terraform import``. See the examples section for how to properly use it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#import_url_username Project#import_url_username}
        :param infrastructure_access_level: Set the infrastructure access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#infrastructure_access_level Project#infrastructure_access_level}
        :param initialize_with_readme: Create main branch with first commit containing a README.md file. Must be set to ``true`` if importing an uninitialized project with a different ``default_branch``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#initialize_with_readme Project#initialize_with_readme}
        :param issues_access_level: Set the issues access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#issues_access_level Project#issues_access_level}
        :param issues_enabled: Enable issue tracking for the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#issues_enabled Project#issues_enabled}
        :param issues_template: Sets the template for new issues in the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#issues_template Project#issues_template}
        :param keep_latest_artifact: Disable or enable the ability to keep the latest artifact for this project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#keep_latest_artifact Project#keep_latest_artifact}
        :param lfs_enabled: Enable LFS for the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#lfs_enabled Project#lfs_enabled}
        :param merge_commit_template: Template used to create merge commit message in merge requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#merge_commit_template Project#merge_commit_template}
        :param merge_method: Set the merge method. Valid values are ``merge``, ``rebase_merge``, ``ff``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#merge_method Project#merge_method}
        :param merge_pipelines_enabled: Enable or disable merge pipelines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#merge_pipelines_enabled Project#merge_pipelines_enabled}
        :param merge_requests_access_level: Set the merge requests access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#merge_requests_access_level Project#merge_requests_access_level}
        :param merge_requests_enabled: Enable merge requests for the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#merge_requests_enabled Project#merge_requests_enabled}
        :param merge_requests_template: Sets the template for new merge requests in the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#merge_requests_template Project#merge_requests_template}
        :param merge_trains_enabled: Enable or disable merge trains. Requires ``merge_pipelines_enabled`` to be set to ``true`` to take effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#merge_trains_enabled Project#merge_trains_enabled}
        :param mirror: Enable project pull mirror. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#mirror Project#mirror}
        :param mirror_overwrites_diverged_branches: Enable overwrite diverged branches for a mirrored project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#mirror_overwrites_diverged_branches Project#mirror_overwrites_diverged_branches}
        :param mirror_trigger_builds: Enable trigger builds on pushes for a mirrored project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#mirror_trigger_builds Project#mirror_trigger_builds}
        :param model_experiments_access_level: Set visibility of machine learning model experiments. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#model_experiments_access_level Project#model_experiments_access_level}
        :param model_registry_access_level: Set visibility of machine learning model registry. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#model_registry_access_level Project#model_registry_access_level}
        :param monitor_access_level: Set the monitor access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#monitor_access_level Project#monitor_access_level}
        :param mr_default_target_self: For forked projects, target merge requests to this project. If false, the target will be the upstream project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#mr_default_target_self Project#mr_default_target_self}
        :param namespace_id: The namespace (group or user) of the project. Defaults to your user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#namespace_id Project#namespace_id}
        :param only_allow_merge_if_all_discussions_are_resolved: Set to true if you want allow merges only if all discussions are resolved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#only_allow_merge_if_all_discussions_are_resolved Project#only_allow_merge_if_all_discussions_are_resolved}
        :param only_allow_merge_if_pipeline_succeeds: Set to true if you want allow merges only if a pipeline succeeds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#only_allow_merge_if_pipeline_succeeds Project#only_allow_merge_if_pipeline_succeeds}
        :param only_mirror_protected_branches: Enable only mirror protected branches for a mirrored project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#only_mirror_protected_branches Project#only_mirror_protected_branches}
        :param packages_enabled: Enable packages repository for the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#packages_enabled Project#packages_enabled}
        :param pages_access_level: Enable pages access control. Valid values are ``public``, ``private``, ``enabled``, ``disabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#pages_access_level Project#pages_access_level}
        :param path: The path of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#path Project#path}
        :param permanently_delete_on_destroy: Set to ``true`` to immediately permanently delete the project instead of scheduling a delete for Premium and Ultimate tiers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#permanently_delete_on_destroy Project#permanently_delete_on_destroy}
        :param pipelines_enabled: Enable pipelines for the project. The ``pipelines_enabled`` field is being sent as ``jobs_enabled`` in the GitLab API calls. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#pipelines_enabled Project#pipelines_enabled}
        :param pre_receive_secret_detection_enabled: Whether Secret Push Detection is enabled. Requires GitLab Ultimate and at least GitLab 17.3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#pre_receive_secret_detection_enabled Project#pre_receive_secret_detection_enabled}
        :param prevent_merge_without_jira_issue: Set whether merge requests require an associated issue from Jira. Premium and Ultimate only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#prevent_merge_without_jira_issue Project#prevent_merge_without_jira_issue}
        :param printing_merge_request_link_enabled: Show link to create/view merge request when pushing from the command line. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#printing_merge_request_link_enabled Project#printing_merge_request_link_enabled}
        :param public_builds: If true, jobs can be viewed by non-project members. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#public_builds Project#public_builds}
        :param public_jobs: If true, jobs can be viewed by non-project members. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#public_jobs Project#public_jobs}
        :param push_rules: push_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#push_rules Project#push_rules}
        :param releases_access_level: Set the releases access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#releases_access_level Project#releases_access_level}
        :param remove_source_branch_after_merge: Enable ``Delete source branch`` option by default for all new merge requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#remove_source_branch_after_merge Project#remove_source_branch_after_merge}
        :param repository_access_level: Set the repository access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#repository_access_level Project#repository_access_level}
        :param repository_storage: Which storage shard the repository is on. (administrator only). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#repository_storage Project#repository_storage}
        :param request_access_enabled: Allow users to request member access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#request_access_enabled Project#request_access_enabled}
        :param requirements_access_level: Set the requirements access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#requirements_access_level Project#requirements_access_level}
        :param resolve_outdated_diff_discussions: Automatically resolve merge request diffs discussions on lines changed with a push. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#resolve_outdated_diff_discussions Project#resolve_outdated_diff_discussions}
        :param restrict_user_defined_variables: Allow only users with the Maintainer role to pass user-defined variables when triggering a pipeline. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#restrict_user_defined_variables Project#restrict_user_defined_variables}
        :param security_and_compliance_access_level: Set the security and compliance access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#security_and_compliance_access_level Project#security_and_compliance_access_level}
        :param shared_runners_enabled: Enable shared runners for this project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#shared_runners_enabled Project#shared_runners_enabled}
        :param skip_wait_for_default_branch_protection: If ``true``, the default behavior to wait for the default branch protection to be created is skipped. This is necessary if the current user is not an admin and the default branch protection is disabled on an instance-level. There is currently no known way to determine if the default branch protection is disabled on an instance-level for non-admin users. This attribute is only used during resource creation, thus changes are suppressed and the attribute cannot be imported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#skip_wait_for_default_branch_protection Project#skip_wait_for_default_branch_protection}
        :param snippets_access_level: Set the snippets access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#snippets_access_level Project#snippets_access_level}
        :param snippets_enabled: Enable snippets for the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#snippets_enabled Project#snippets_enabled}
        :param squash_commit_template: Template used to create squash commit message in merge requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#squash_commit_template Project#squash_commit_template}
        :param squash_option: Squash commits when merge request is merged. Valid values are ``never`` (Do not allow), ``always`` (Require), ``default_on`` (Encourage), or ``default_off`` (Allow). The default value is ``default_off`` (Allow). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#squash_option Project#squash_option}
        :param suggestion_commit_message: The commit message used to apply merge request suggestions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#suggestion_commit_message Project#suggestion_commit_message}
        :param tags: The list of tags for a project; put array of tags, that should be finally assigned to a project. Use topics instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#tags Project#tags}
        :param template_name: When used without use_custom_template, name of a built-in project template. When used with use_custom_template, name of a custom project template. This option is mutually exclusive with ``template_project_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#template_name Project#template_name}
        :param template_project_id: When used with use_custom_template, project ID of a custom project template. This is preferable to using template_name since template_name may be ambiguous (enterprise edition). This option is mutually exclusive with ``template_name``. See ``gitlab_group_project_file_template`` to set a project as a template project. If a project has not been set as a template, using it here will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#template_project_id Project#template_project_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#timeouts Project#timeouts}
        :param topics: The list of topics for the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#topics Project#topics}
        :param use_custom_template: Use either custom instance or group (with group_with_project_templates_id) project template (enterprise edition). ~> When using a custom template, `Group Tokens won't work <https://docs.gitlab.com/15.7/ee/user/project/settings/import_export_troubleshooting/#import-using-the-rest-api-fails-when-using-a-group-access-token>`_. You must use a real user's Personal Access Token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#use_custom_template Project#use_custom_template}
        :param visibility_level: Set to ``public`` to create a public project. Valid values are ``private``, ``internal``, ``public``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#visibility_level Project#visibility_level}
        :param wiki_access_level: Set the wiki access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#wiki_access_level Project#wiki_access_level}
        :param wiki_enabled: Enable wiki for the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#wiki_enabled Project#wiki_enabled}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2173b0bb50322800875b29c7030755fe97cc1d30816c7d87b42f0013c7d5580)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ProjectConfig(
            name=name,
            allow_merge_on_skipped_pipeline=allow_merge_on_skipped_pipeline,
            allow_pipeline_trigger_approve_deployment=allow_pipeline_trigger_approve_deployment,
            analytics_access_level=analytics_access_level,
            approvals_before_merge=approvals_before_merge,
            archived=archived,
            archive_on_destroy=archive_on_destroy,
            auto_cancel_pending_pipelines=auto_cancel_pending_pipelines,
            autoclose_referenced_issues=autoclose_referenced_issues,
            auto_devops_deploy_strategy=auto_devops_deploy_strategy,
            auto_devops_enabled=auto_devops_enabled,
            avatar=avatar,
            avatar_hash=avatar_hash,
            build_coverage_regex=build_coverage_regex,
            build_git_strategy=build_git_strategy,
            builds_access_level=builds_access_level,
            build_timeout=build_timeout,
            ci_config_path=ci_config_path,
            ci_default_git_depth=ci_default_git_depth,
            ci_delete_pipelines_in_seconds=ci_delete_pipelines_in_seconds,
            ci_forward_deployment_enabled=ci_forward_deployment_enabled,
            ci_id_token_sub_claim_components=ci_id_token_sub_claim_components,
            ci_pipeline_variables_minimum_override_role=ci_pipeline_variables_minimum_override_role,
            ci_restrict_pipeline_cancellation_role=ci_restrict_pipeline_cancellation_role,
            ci_separated_caches=ci_separated_caches,
            container_expiration_policy=container_expiration_policy,
            container_registry_access_level=container_registry_access_level,
            container_registry_enabled=container_registry_enabled,
            default_branch=default_branch,
            description=description,
            emails_enabled=emails_enabled,
            environments_access_level=environments_access_level,
            external_authorization_classification_label=external_authorization_classification_label,
            feature_flags_access_level=feature_flags_access_level,
            forked_from_project_id=forked_from_project_id,
            forking_access_level=forking_access_level,
            group_runners_enabled=group_runners_enabled,
            group_with_project_templates_id=group_with_project_templates_id,
            id=id,
            import_url=import_url,
            import_url_password=import_url_password,
            import_url_username=import_url_username,
            infrastructure_access_level=infrastructure_access_level,
            initialize_with_readme=initialize_with_readme,
            issues_access_level=issues_access_level,
            issues_enabled=issues_enabled,
            issues_template=issues_template,
            keep_latest_artifact=keep_latest_artifact,
            lfs_enabled=lfs_enabled,
            merge_commit_template=merge_commit_template,
            merge_method=merge_method,
            merge_pipelines_enabled=merge_pipelines_enabled,
            merge_requests_access_level=merge_requests_access_level,
            merge_requests_enabled=merge_requests_enabled,
            merge_requests_template=merge_requests_template,
            merge_trains_enabled=merge_trains_enabled,
            mirror=mirror,
            mirror_overwrites_diverged_branches=mirror_overwrites_diverged_branches,
            mirror_trigger_builds=mirror_trigger_builds,
            model_experiments_access_level=model_experiments_access_level,
            model_registry_access_level=model_registry_access_level,
            monitor_access_level=monitor_access_level,
            mr_default_target_self=mr_default_target_self,
            namespace_id=namespace_id,
            only_allow_merge_if_all_discussions_are_resolved=only_allow_merge_if_all_discussions_are_resolved,
            only_allow_merge_if_pipeline_succeeds=only_allow_merge_if_pipeline_succeeds,
            only_mirror_protected_branches=only_mirror_protected_branches,
            packages_enabled=packages_enabled,
            pages_access_level=pages_access_level,
            path=path,
            permanently_delete_on_destroy=permanently_delete_on_destroy,
            pipelines_enabled=pipelines_enabled,
            pre_receive_secret_detection_enabled=pre_receive_secret_detection_enabled,
            prevent_merge_without_jira_issue=prevent_merge_without_jira_issue,
            printing_merge_request_link_enabled=printing_merge_request_link_enabled,
            public_builds=public_builds,
            public_jobs=public_jobs,
            push_rules=push_rules,
            releases_access_level=releases_access_level,
            remove_source_branch_after_merge=remove_source_branch_after_merge,
            repository_access_level=repository_access_level,
            repository_storage=repository_storage,
            request_access_enabled=request_access_enabled,
            requirements_access_level=requirements_access_level,
            resolve_outdated_diff_discussions=resolve_outdated_diff_discussions,
            restrict_user_defined_variables=restrict_user_defined_variables,
            security_and_compliance_access_level=security_and_compliance_access_level,
            shared_runners_enabled=shared_runners_enabled,
            skip_wait_for_default_branch_protection=skip_wait_for_default_branch_protection,
            snippets_access_level=snippets_access_level,
            snippets_enabled=snippets_enabled,
            squash_commit_template=squash_commit_template,
            squash_option=squash_option,
            suggestion_commit_message=suggestion_commit_message,
            tags=tags,
            template_name=template_name,
            template_project_id=template_project_id,
            timeouts=timeouts,
            topics=topics,
            use_custom_template=use_custom_template,
            visibility_level=visibility_level,
            wiki_access_level=wiki_access_level,
            wiki_enabled=wiki_enabled,
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
        '''Generates CDKTF code for importing a Project resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Project to import.
        :param import_from_id: The id of the existing Project that should be imported. Refer to the {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Project to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cc5d19d006568564a2a3cfd20f7ee36be0475e29a083408063121c8dc35acf7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putContainerExpirationPolicy")
    def put_container_expiration_policy(
        self,
        *,
        cadence: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        keep_n: typing.Optional[jsii.Number] = None,
        name_regex: typing.Optional[builtins.str] = None,
        name_regex_delete: typing.Optional[builtins.str] = None,
        name_regex_keep: typing.Optional[builtins.str] = None,
        older_than: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cadence: The cadence of the policy. Valid values are: ``1d``, ``7d``, ``14d``, ``1month``, ``3month``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#cadence Project#cadence}
        :param enabled: If true, the policy is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#enabled Project#enabled}
        :param keep_n: The number of images to keep. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#keep_n Project#keep_n}
        :param name_regex: The regular expression to match image names to delete. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#name_regex Project#name_regex}
        :param name_regex_delete: The regular expression to match image names to delete. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#name_regex_delete Project#name_regex_delete}
        :param name_regex_keep: The regular expression to match image names to keep. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#name_regex_keep Project#name_regex_keep}
        :param older_than: The number of days to keep images. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#older_than Project#older_than}
        '''
        value = ProjectContainerExpirationPolicy(
            cadence=cadence,
            enabled=enabled,
            keep_n=keep_n,
            name_regex=name_regex,
            name_regex_delete=name_regex_delete,
            name_regex_keep=name_regex_keep,
            older_than=older_than,
        )

        return typing.cast(None, jsii.invoke(self, "putContainerExpirationPolicy", [value]))

    @jsii.member(jsii_name="putPushRules")
    def put_push_rules(
        self,
        *,
        author_email_regex: typing.Optional[builtins.str] = None,
        branch_name_regex: typing.Optional[builtins.str] = None,
        commit_committer_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        commit_committer_name_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        commit_message_negative_regex: typing.Optional[builtins.str] = None,
        commit_message_regex: typing.Optional[builtins.str] = None,
        deny_delete_tag: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        file_name_regex: typing.Optional[builtins.str] = None,
        max_file_size: typing.Optional[jsii.Number] = None,
        member_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prevent_secrets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reject_non_dco_commits: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reject_unsigned_commits: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param author_email_regex: All commit author emails must match this regex, e.g. ``@my-company.com$``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#author_email_regex Project#author_email_regex}
        :param branch_name_regex: All branch names must match this regex, e.g. ``(feature|hotfix)\\/*``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#branch_name_regex Project#branch_name_regex}
        :param commit_committer_check: Users can only push commits to this repository that were committed with one of their own verified emails. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#commit_committer_check Project#commit_committer_check}
        :param commit_committer_name_check: Users can only push commits to this repository if the commit author name is consistent with their GitLab account name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#commit_committer_name_check Project#commit_committer_name_check}
        :param commit_message_negative_regex: No commit message is allowed to match this regex, e.g. ``ssh\\:\\/\\/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#commit_message_negative_regex Project#commit_message_negative_regex}
        :param commit_message_regex: All commit messages must match this regex, e.g. ``Fixed \\d+\\..*``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#commit_message_regex Project#commit_message_regex}
        :param deny_delete_tag: Deny deleting a tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#deny_delete_tag Project#deny_delete_tag}
        :param file_name_regex: All committed filenames must not match this regex, e.g. ``(jar|exe)$``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#file_name_regex Project#file_name_regex}
        :param max_file_size: Maximum file size (MB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#max_file_size Project#max_file_size}
        :param member_check: Restrict commits by author (email) to existing GitLab users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#member_check Project#member_check}
        :param prevent_secrets: GitLab will reject any files that are likely to contain secrets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#prevent_secrets Project#prevent_secrets}
        :param reject_non_dco_commits: Reject commit when it’s not DCO certified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#reject_non_dco_commits Project#reject_non_dco_commits}
        :param reject_unsigned_commits: Reject commit when it’s not signed through GPG. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#reject_unsigned_commits Project#reject_unsigned_commits}
        '''
        value = ProjectPushRules(
            author_email_regex=author_email_regex,
            branch_name_regex=branch_name_regex,
            commit_committer_check=commit_committer_check,
            commit_committer_name_check=commit_committer_name_check,
            commit_message_negative_regex=commit_message_negative_regex,
            commit_message_regex=commit_message_regex,
            deny_delete_tag=deny_delete_tag,
            file_name_regex=file_name_regex,
            max_file_size=max_file_size,
            member_check=member_check,
            prevent_secrets=prevent_secrets,
            reject_non_dco_commits=reject_non_dco_commits,
            reject_unsigned_commits=reject_unsigned_commits,
        )

        return typing.cast(None, jsii.invoke(self, "putPushRules", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#create Project#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#delete Project#delete}.
        '''
        value = ProjectTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAllowMergeOnSkippedPipeline")
    def reset_allow_merge_on_skipped_pipeline(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowMergeOnSkippedPipeline", []))

    @jsii.member(jsii_name="resetAllowPipelineTriggerApproveDeployment")
    def reset_allow_pipeline_trigger_approve_deployment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowPipelineTriggerApproveDeployment", []))

    @jsii.member(jsii_name="resetAnalyticsAccessLevel")
    def reset_analytics_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnalyticsAccessLevel", []))

    @jsii.member(jsii_name="resetApprovalsBeforeMerge")
    def reset_approvals_before_merge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApprovalsBeforeMerge", []))

    @jsii.member(jsii_name="resetArchived")
    def reset_archived(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchived", []))

    @jsii.member(jsii_name="resetArchiveOnDestroy")
    def reset_archive_on_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchiveOnDestroy", []))

    @jsii.member(jsii_name="resetAutoCancelPendingPipelines")
    def reset_auto_cancel_pending_pipelines(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoCancelPendingPipelines", []))

    @jsii.member(jsii_name="resetAutocloseReferencedIssues")
    def reset_autoclose_referenced_issues(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutocloseReferencedIssues", []))

    @jsii.member(jsii_name="resetAutoDevopsDeployStrategy")
    def reset_auto_devops_deploy_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDevopsDeployStrategy", []))

    @jsii.member(jsii_name="resetAutoDevopsEnabled")
    def reset_auto_devops_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDevopsEnabled", []))

    @jsii.member(jsii_name="resetAvatar")
    def reset_avatar(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvatar", []))

    @jsii.member(jsii_name="resetAvatarHash")
    def reset_avatar_hash(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvatarHash", []))

    @jsii.member(jsii_name="resetBuildCoverageRegex")
    def reset_build_coverage_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildCoverageRegex", []))

    @jsii.member(jsii_name="resetBuildGitStrategy")
    def reset_build_git_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildGitStrategy", []))

    @jsii.member(jsii_name="resetBuildsAccessLevel")
    def reset_builds_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildsAccessLevel", []))

    @jsii.member(jsii_name="resetBuildTimeout")
    def reset_build_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildTimeout", []))

    @jsii.member(jsii_name="resetCiConfigPath")
    def reset_ci_config_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCiConfigPath", []))

    @jsii.member(jsii_name="resetCiDefaultGitDepth")
    def reset_ci_default_git_depth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCiDefaultGitDepth", []))

    @jsii.member(jsii_name="resetCiDeletePipelinesInSeconds")
    def reset_ci_delete_pipelines_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCiDeletePipelinesInSeconds", []))

    @jsii.member(jsii_name="resetCiForwardDeploymentEnabled")
    def reset_ci_forward_deployment_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCiForwardDeploymentEnabled", []))

    @jsii.member(jsii_name="resetCiIdTokenSubClaimComponents")
    def reset_ci_id_token_sub_claim_components(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCiIdTokenSubClaimComponents", []))

    @jsii.member(jsii_name="resetCiPipelineVariablesMinimumOverrideRole")
    def reset_ci_pipeline_variables_minimum_override_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCiPipelineVariablesMinimumOverrideRole", []))

    @jsii.member(jsii_name="resetCiRestrictPipelineCancellationRole")
    def reset_ci_restrict_pipeline_cancellation_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCiRestrictPipelineCancellationRole", []))

    @jsii.member(jsii_name="resetCiSeparatedCaches")
    def reset_ci_separated_caches(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCiSeparatedCaches", []))

    @jsii.member(jsii_name="resetContainerExpirationPolicy")
    def reset_container_expiration_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerExpirationPolicy", []))

    @jsii.member(jsii_name="resetContainerRegistryAccessLevel")
    def reset_container_registry_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerRegistryAccessLevel", []))

    @jsii.member(jsii_name="resetContainerRegistryEnabled")
    def reset_container_registry_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerRegistryEnabled", []))

    @jsii.member(jsii_name="resetDefaultBranch")
    def reset_default_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultBranch", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEmailsEnabled")
    def reset_emails_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailsEnabled", []))

    @jsii.member(jsii_name="resetEnvironmentsAccessLevel")
    def reset_environments_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironmentsAccessLevel", []))

    @jsii.member(jsii_name="resetExternalAuthorizationClassificationLabel")
    def reset_external_authorization_classification_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalAuthorizationClassificationLabel", []))

    @jsii.member(jsii_name="resetFeatureFlagsAccessLevel")
    def reset_feature_flags_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeatureFlagsAccessLevel", []))

    @jsii.member(jsii_name="resetForkedFromProjectId")
    def reset_forked_from_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForkedFromProjectId", []))

    @jsii.member(jsii_name="resetForkingAccessLevel")
    def reset_forking_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForkingAccessLevel", []))

    @jsii.member(jsii_name="resetGroupRunnersEnabled")
    def reset_group_runners_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupRunnersEnabled", []))

    @jsii.member(jsii_name="resetGroupWithProjectTemplatesId")
    def reset_group_with_project_templates_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupWithProjectTemplatesId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImportUrl")
    def reset_import_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImportUrl", []))

    @jsii.member(jsii_name="resetImportUrlPassword")
    def reset_import_url_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImportUrlPassword", []))

    @jsii.member(jsii_name="resetImportUrlUsername")
    def reset_import_url_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImportUrlUsername", []))

    @jsii.member(jsii_name="resetInfrastructureAccessLevel")
    def reset_infrastructure_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInfrastructureAccessLevel", []))

    @jsii.member(jsii_name="resetInitializeWithReadme")
    def reset_initialize_with_readme(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitializeWithReadme", []))

    @jsii.member(jsii_name="resetIssuesAccessLevel")
    def reset_issues_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuesAccessLevel", []))

    @jsii.member(jsii_name="resetIssuesEnabled")
    def reset_issues_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuesEnabled", []))

    @jsii.member(jsii_name="resetIssuesTemplate")
    def reset_issues_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuesTemplate", []))

    @jsii.member(jsii_name="resetKeepLatestArtifact")
    def reset_keep_latest_artifact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepLatestArtifact", []))

    @jsii.member(jsii_name="resetLfsEnabled")
    def reset_lfs_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLfsEnabled", []))

    @jsii.member(jsii_name="resetMergeCommitTemplate")
    def reset_merge_commit_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergeCommitTemplate", []))

    @jsii.member(jsii_name="resetMergeMethod")
    def reset_merge_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergeMethod", []))

    @jsii.member(jsii_name="resetMergePipelinesEnabled")
    def reset_merge_pipelines_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergePipelinesEnabled", []))

    @jsii.member(jsii_name="resetMergeRequestsAccessLevel")
    def reset_merge_requests_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergeRequestsAccessLevel", []))

    @jsii.member(jsii_name="resetMergeRequestsEnabled")
    def reset_merge_requests_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergeRequestsEnabled", []))

    @jsii.member(jsii_name="resetMergeRequestsTemplate")
    def reset_merge_requests_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergeRequestsTemplate", []))

    @jsii.member(jsii_name="resetMergeTrainsEnabled")
    def reset_merge_trains_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergeTrainsEnabled", []))

    @jsii.member(jsii_name="resetMirror")
    def reset_mirror(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMirror", []))

    @jsii.member(jsii_name="resetMirrorOverwritesDivergedBranches")
    def reset_mirror_overwrites_diverged_branches(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMirrorOverwritesDivergedBranches", []))

    @jsii.member(jsii_name="resetMirrorTriggerBuilds")
    def reset_mirror_trigger_builds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMirrorTriggerBuilds", []))

    @jsii.member(jsii_name="resetModelExperimentsAccessLevel")
    def reset_model_experiments_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelExperimentsAccessLevel", []))

    @jsii.member(jsii_name="resetModelRegistryAccessLevel")
    def reset_model_registry_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelRegistryAccessLevel", []))

    @jsii.member(jsii_name="resetMonitorAccessLevel")
    def reset_monitor_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitorAccessLevel", []))

    @jsii.member(jsii_name="resetMrDefaultTargetSelf")
    def reset_mr_default_target_self(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMrDefaultTargetSelf", []))

    @jsii.member(jsii_name="resetNamespaceId")
    def reset_namespace_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespaceId", []))

    @jsii.member(jsii_name="resetOnlyAllowMergeIfAllDiscussionsAreResolved")
    def reset_only_allow_merge_if_all_discussions_are_resolved(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnlyAllowMergeIfAllDiscussionsAreResolved", []))

    @jsii.member(jsii_name="resetOnlyAllowMergeIfPipelineSucceeds")
    def reset_only_allow_merge_if_pipeline_succeeds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnlyAllowMergeIfPipelineSucceeds", []))

    @jsii.member(jsii_name="resetOnlyMirrorProtectedBranches")
    def reset_only_mirror_protected_branches(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnlyMirrorProtectedBranches", []))

    @jsii.member(jsii_name="resetPackagesEnabled")
    def reset_packages_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPackagesEnabled", []))

    @jsii.member(jsii_name="resetPagesAccessLevel")
    def reset_pages_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPagesAccessLevel", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPermanentlyDeleteOnDestroy")
    def reset_permanently_delete_on_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermanentlyDeleteOnDestroy", []))

    @jsii.member(jsii_name="resetPipelinesEnabled")
    def reset_pipelines_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPipelinesEnabled", []))

    @jsii.member(jsii_name="resetPreReceiveSecretDetectionEnabled")
    def reset_pre_receive_secret_detection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreReceiveSecretDetectionEnabled", []))

    @jsii.member(jsii_name="resetPreventMergeWithoutJiraIssue")
    def reset_prevent_merge_without_jira_issue(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreventMergeWithoutJiraIssue", []))

    @jsii.member(jsii_name="resetPrintingMergeRequestLinkEnabled")
    def reset_printing_merge_request_link_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrintingMergeRequestLinkEnabled", []))

    @jsii.member(jsii_name="resetPublicBuilds")
    def reset_public_builds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicBuilds", []))

    @jsii.member(jsii_name="resetPublicJobs")
    def reset_public_jobs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicJobs", []))

    @jsii.member(jsii_name="resetPushRules")
    def reset_push_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPushRules", []))

    @jsii.member(jsii_name="resetReleasesAccessLevel")
    def reset_releases_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReleasesAccessLevel", []))

    @jsii.member(jsii_name="resetRemoveSourceBranchAfterMerge")
    def reset_remove_source_branch_after_merge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoveSourceBranchAfterMerge", []))

    @jsii.member(jsii_name="resetRepositoryAccessLevel")
    def reset_repository_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositoryAccessLevel", []))

    @jsii.member(jsii_name="resetRepositoryStorage")
    def reset_repository_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositoryStorage", []))

    @jsii.member(jsii_name="resetRequestAccessEnabled")
    def reset_request_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestAccessEnabled", []))

    @jsii.member(jsii_name="resetRequirementsAccessLevel")
    def reset_requirements_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequirementsAccessLevel", []))

    @jsii.member(jsii_name="resetResolveOutdatedDiffDiscussions")
    def reset_resolve_outdated_diff_discussions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResolveOutdatedDiffDiscussions", []))

    @jsii.member(jsii_name="resetRestrictUserDefinedVariables")
    def reset_restrict_user_defined_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestrictUserDefinedVariables", []))

    @jsii.member(jsii_name="resetSecurityAndComplianceAccessLevel")
    def reset_security_and_compliance_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityAndComplianceAccessLevel", []))

    @jsii.member(jsii_name="resetSharedRunnersEnabled")
    def reset_shared_runners_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedRunnersEnabled", []))

    @jsii.member(jsii_name="resetSkipWaitForDefaultBranchProtection")
    def reset_skip_wait_for_default_branch_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipWaitForDefaultBranchProtection", []))

    @jsii.member(jsii_name="resetSnippetsAccessLevel")
    def reset_snippets_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnippetsAccessLevel", []))

    @jsii.member(jsii_name="resetSnippetsEnabled")
    def reset_snippets_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnippetsEnabled", []))

    @jsii.member(jsii_name="resetSquashCommitTemplate")
    def reset_squash_commit_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSquashCommitTemplate", []))

    @jsii.member(jsii_name="resetSquashOption")
    def reset_squash_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSquashOption", []))

    @jsii.member(jsii_name="resetSuggestionCommitMessage")
    def reset_suggestion_commit_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuggestionCommitMessage", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTemplateName")
    def reset_template_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemplateName", []))

    @jsii.member(jsii_name="resetTemplateProjectId")
    def reset_template_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemplateProjectId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTopics")
    def reset_topics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopics", []))

    @jsii.member(jsii_name="resetUseCustomTemplate")
    def reset_use_custom_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseCustomTemplate", []))

    @jsii.member(jsii_name="resetVisibilityLevel")
    def reset_visibility_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisibilityLevel", []))

    @jsii.member(jsii_name="resetWikiAccessLevel")
    def reset_wiki_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWikiAccessLevel", []))

    @jsii.member(jsii_name="resetWikiEnabled")
    def reset_wiki_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWikiEnabled", []))

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
    @jsii.member(jsii_name="avatarUrl")
    def avatar_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "avatarUrl"))

    @builtins.property
    @jsii.member(jsii_name="containerExpirationPolicy")
    def container_expiration_policy(
        self,
    ) -> "ProjectContainerExpirationPolicyOutputReference":
        return typing.cast("ProjectContainerExpirationPolicyOutputReference", jsii.get(self, "containerExpirationPolicy"))

    @builtins.property
    @jsii.member(jsii_name="emptyRepo")
    def empty_repo(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "emptyRepo"))

    @builtins.property
    @jsii.member(jsii_name="httpUrlToRepo")
    def http_url_to_repo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpUrlToRepo"))

    @builtins.property
    @jsii.member(jsii_name="pathWithNamespace")
    def path_with_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathWithNamespace"))

    @builtins.property
    @jsii.member(jsii_name="pushRules")
    def push_rules(self) -> "ProjectPushRulesOutputReference":
        return typing.cast("ProjectPushRulesOutputReference", jsii.get(self, "pushRules"))

    @builtins.property
    @jsii.member(jsii_name="runnersToken")
    def runners_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runnersToken"))

    @builtins.property
    @jsii.member(jsii_name="sshUrlToRepo")
    def ssh_url_to_repo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshUrlToRepo"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ProjectTimeoutsOutputReference":
        return typing.cast("ProjectTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="webUrl")
    def web_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webUrl"))

    @builtins.property
    @jsii.member(jsii_name="allowMergeOnSkippedPipelineInput")
    def allow_merge_on_skipped_pipeline_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowMergeOnSkippedPipelineInput"))

    @builtins.property
    @jsii.member(jsii_name="allowPipelineTriggerApproveDeploymentInput")
    def allow_pipeline_trigger_approve_deployment_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowPipelineTriggerApproveDeploymentInput"))

    @builtins.property
    @jsii.member(jsii_name="analyticsAccessLevelInput")
    def analytics_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "analyticsAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="approvalsBeforeMergeInput")
    def approvals_before_merge_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "approvalsBeforeMergeInput"))

    @builtins.property
    @jsii.member(jsii_name="archivedInput")
    def archived_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "archivedInput"))

    @builtins.property
    @jsii.member(jsii_name="archiveOnDestroyInput")
    def archive_on_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "archiveOnDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="autoCancelPendingPipelinesInput")
    def auto_cancel_pending_pipelines_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoCancelPendingPipelinesInput"))

    @builtins.property
    @jsii.member(jsii_name="autocloseReferencedIssuesInput")
    def autoclose_referenced_issues_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autocloseReferencedIssuesInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDevopsDeployStrategyInput")
    def auto_devops_deploy_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoDevopsDeployStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDevopsEnabledInput")
    def auto_devops_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoDevopsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="avatarHashInput")
    def avatar_hash_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "avatarHashInput"))

    @builtins.property
    @jsii.member(jsii_name="avatarInput")
    def avatar_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "avatarInput"))

    @builtins.property
    @jsii.member(jsii_name="buildCoverageRegexInput")
    def build_coverage_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildCoverageRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="buildGitStrategyInput")
    def build_git_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildGitStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="buildsAccessLevelInput")
    def builds_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildsAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="buildTimeoutInput")
    def build_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "buildTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="ciConfigPathInput")
    def ci_config_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ciConfigPathInput"))

    @builtins.property
    @jsii.member(jsii_name="ciDefaultGitDepthInput")
    def ci_default_git_depth_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ciDefaultGitDepthInput"))

    @builtins.property
    @jsii.member(jsii_name="ciDeletePipelinesInSecondsInput")
    def ci_delete_pipelines_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ciDeletePipelinesInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="ciForwardDeploymentEnabledInput")
    def ci_forward_deployment_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ciForwardDeploymentEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="ciIdTokenSubClaimComponentsInput")
    def ci_id_token_sub_claim_components_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ciIdTokenSubClaimComponentsInput"))

    @builtins.property
    @jsii.member(jsii_name="ciPipelineVariablesMinimumOverrideRoleInput")
    def ci_pipeline_variables_minimum_override_role_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ciPipelineVariablesMinimumOverrideRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="ciRestrictPipelineCancellationRoleInput")
    def ci_restrict_pipeline_cancellation_role_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ciRestrictPipelineCancellationRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="ciSeparatedCachesInput")
    def ci_separated_caches_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ciSeparatedCachesInput"))

    @builtins.property
    @jsii.member(jsii_name="containerExpirationPolicyInput")
    def container_expiration_policy_input(
        self,
    ) -> typing.Optional["ProjectContainerExpirationPolicy"]:
        return typing.cast(typing.Optional["ProjectContainerExpirationPolicy"], jsii.get(self, "containerExpirationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="containerRegistryAccessLevelInput")
    def container_registry_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerRegistryAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="containerRegistryEnabledInput")
    def container_registry_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "containerRegistryEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultBranchInput")
    def default_branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultBranchInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="emailsEnabledInput")
    def emails_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "emailsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentsAccessLevelInput")
    def environments_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentsAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="externalAuthorizationClassificationLabelInput")
    def external_authorization_classification_label_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalAuthorizationClassificationLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="featureFlagsAccessLevelInput")
    def feature_flags_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "featureFlagsAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="forkedFromProjectIdInput")
    def forked_from_project_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "forkedFromProjectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="forkingAccessLevelInput")
    def forking_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forkingAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="groupRunnersEnabledInput")
    def group_runners_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "groupRunnersEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="groupWithProjectTemplatesIdInput")
    def group_with_project_templates_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "groupWithProjectTemplatesIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="importUrlInput")
    def import_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "importUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="importUrlPasswordInput")
    def import_url_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "importUrlPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="importUrlUsernameInput")
    def import_url_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "importUrlUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureAccessLevelInput")
    def infrastructure_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "infrastructureAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="initializeWithReadmeInput")
    def initialize_with_readme_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "initializeWithReadmeInput"))

    @builtins.property
    @jsii.member(jsii_name="issuesAccessLevelInput")
    def issues_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuesAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="issuesEnabledInput")
    def issues_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "issuesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="issuesTemplateInput")
    def issues_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuesTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="keepLatestArtifactInput")
    def keep_latest_artifact_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "keepLatestArtifactInput"))

    @builtins.property
    @jsii.member(jsii_name="lfsEnabledInput")
    def lfs_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "lfsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="mergeCommitTemplateInput")
    def merge_commit_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mergeCommitTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="mergeMethodInput")
    def merge_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mergeMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="mergePipelinesEnabledInput")
    def merge_pipelines_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mergePipelinesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="mergeRequestsAccessLevelInput")
    def merge_requests_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mergeRequestsAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="mergeRequestsEnabledInput")
    def merge_requests_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mergeRequestsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="mergeRequestsTemplateInput")
    def merge_requests_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mergeRequestsTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="mergeTrainsEnabledInput")
    def merge_trains_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mergeTrainsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="mirrorInput")
    def mirror_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mirrorInput"))

    @builtins.property
    @jsii.member(jsii_name="mirrorOverwritesDivergedBranchesInput")
    def mirror_overwrites_diverged_branches_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mirrorOverwritesDivergedBranchesInput"))

    @builtins.property
    @jsii.member(jsii_name="mirrorTriggerBuildsInput")
    def mirror_trigger_builds_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mirrorTriggerBuildsInput"))

    @builtins.property
    @jsii.member(jsii_name="modelExperimentsAccessLevelInput")
    def model_experiments_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelExperimentsAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="modelRegistryAccessLevelInput")
    def model_registry_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelRegistryAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorAccessLevelInput")
    def monitor_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "monitorAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="mrDefaultTargetSelfInput")
    def mr_default_target_self_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mrDefaultTargetSelfInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceIdInput")
    def namespace_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "namespaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="onlyAllowMergeIfAllDiscussionsAreResolvedInput")
    def only_allow_merge_if_all_discussions_are_resolved_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "onlyAllowMergeIfAllDiscussionsAreResolvedInput"))

    @builtins.property
    @jsii.member(jsii_name="onlyAllowMergeIfPipelineSucceedsInput")
    def only_allow_merge_if_pipeline_succeeds_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "onlyAllowMergeIfPipelineSucceedsInput"))

    @builtins.property
    @jsii.member(jsii_name="onlyMirrorProtectedBranchesInput")
    def only_mirror_protected_branches_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "onlyMirrorProtectedBranchesInput"))

    @builtins.property
    @jsii.member(jsii_name="packagesEnabledInput")
    def packages_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "packagesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="pagesAccessLevelInput")
    def pages_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pagesAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="permanentlyDeleteOnDestroyInput")
    def permanently_delete_on_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "permanentlyDeleteOnDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="pipelinesEnabledInput")
    def pipelines_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pipelinesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="preReceiveSecretDetectionEnabledInput")
    def pre_receive_secret_detection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preReceiveSecretDetectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="preventMergeWithoutJiraIssueInput")
    def prevent_merge_without_jira_issue_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preventMergeWithoutJiraIssueInput"))

    @builtins.property
    @jsii.member(jsii_name="printingMergeRequestLinkEnabledInput")
    def printing_merge_request_link_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "printingMergeRequestLinkEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="publicBuildsInput")
    def public_builds_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicBuildsInput"))

    @builtins.property
    @jsii.member(jsii_name="publicJobsInput")
    def public_jobs_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicJobsInput"))

    @builtins.property
    @jsii.member(jsii_name="pushRulesInput")
    def push_rules_input(self) -> typing.Optional["ProjectPushRules"]:
        return typing.cast(typing.Optional["ProjectPushRules"], jsii.get(self, "pushRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="releasesAccessLevelInput")
    def releases_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "releasesAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="removeSourceBranchAfterMergeInput")
    def remove_source_branch_after_merge_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "removeSourceBranchAfterMergeInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryAccessLevelInput")
    def repository_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryStorageInput")
    def repository_storage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="requestAccessEnabledInput")
    def request_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requestAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="requirementsAccessLevelInput")
    def requirements_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requirementsAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="resolveOutdatedDiffDiscussionsInput")
    def resolve_outdated_diff_discussions_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "resolveOutdatedDiffDiscussionsInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictUserDefinedVariablesInput")
    def restrict_user_defined_variables_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "restrictUserDefinedVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="securityAndComplianceAccessLevelInput")
    def security_and_compliance_access_level_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityAndComplianceAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedRunnersEnabledInput")
    def shared_runners_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sharedRunnersEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="skipWaitForDefaultBranchProtectionInput")
    def skip_wait_for_default_branch_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipWaitForDefaultBranchProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="snippetsAccessLevelInput")
    def snippets_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snippetsAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="snippetsEnabledInput")
    def snippets_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "snippetsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="squashCommitTemplateInput")
    def squash_commit_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "squashCommitTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="squashOptionInput")
    def squash_option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "squashOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="suggestionCommitMessageInput")
    def suggestion_commit_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suggestionCommitMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="templateNameInput")
    def template_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateNameInput"))

    @builtins.property
    @jsii.member(jsii_name="templateProjectIdInput")
    def template_project_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "templateProjectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ProjectTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ProjectTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="topicsInput")
    def topics_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "topicsInput"))

    @builtins.property
    @jsii.member(jsii_name="useCustomTemplateInput")
    def use_custom_template_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useCustomTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="visibilityLevelInput")
    def visibility_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "visibilityLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="wikiAccessLevelInput")
    def wiki_access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "wikiAccessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="wikiEnabledInput")
    def wiki_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "wikiEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="allowMergeOnSkippedPipeline")
    def allow_merge_on_skipped_pipeline(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowMergeOnSkippedPipeline"))

    @allow_merge_on_skipped_pipeline.setter
    def allow_merge_on_skipped_pipeline(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7720953023af4e9a324f9b83458c1d9a993975d5bd799b0bf21ec0e3250c4dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowMergeOnSkippedPipeline", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowPipelineTriggerApproveDeployment")
    def allow_pipeline_trigger_approve_deployment(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowPipelineTriggerApproveDeployment"))

    @allow_pipeline_trigger_approve_deployment.setter
    def allow_pipeline_trigger_approve_deployment(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f20a2f8753eb02f5996962c7dc586b4c9e6cae1d3db31e578e8ff3e5fe60fd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowPipelineTriggerApproveDeployment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="analyticsAccessLevel")
    def analytics_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "analyticsAccessLevel"))

    @analytics_access_level.setter
    def analytics_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b63e479e2a2e67a7b2701403b44d71606eece0833b43826d92466343de6ae2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "analyticsAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="approvalsBeforeMerge")
    def approvals_before_merge(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "approvalsBeforeMerge"))

    @approvals_before_merge.setter
    def approvals_before_merge(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50463079233251631937821546249b0c6416caecb354cbfba5f8a4126bc0aaab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "approvalsBeforeMerge", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__ce5fceba4cce9233297b3939cf3ce983d05903d1d7374cacb2453e9f9e007dc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archived", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="archiveOnDestroy")
    def archive_on_destroy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "archiveOnDestroy"))

    @archive_on_destroy.setter
    def archive_on_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d69f98caacbd79d12802d55c25c646f2860a4608f58d4b93629881784b86dc5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveOnDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoCancelPendingPipelines")
    def auto_cancel_pending_pipelines(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoCancelPendingPipelines"))

    @auto_cancel_pending_pipelines.setter
    def auto_cancel_pending_pipelines(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15b3ce900b8b5f9808388ef66c978415a6f2102764b1b73216c539c72314c4bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoCancelPendingPipelines", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autocloseReferencedIssues")
    def autoclose_referenced_issues(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autocloseReferencedIssues"))

    @autoclose_referenced_issues.setter
    def autoclose_referenced_issues(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2815dd42610c310f2a6afe4412d8a32dae0633ef15e2a45af4492cf26c3032a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autocloseReferencedIssues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoDevopsDeployStrategy")
    def auto_devops_deploy_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoDevopsDeployStrategy"))

    @auto_devops_deploy_strategy.setter
    def auto_devops_deploy_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__618de3cff3633b2ccab7c63d7cd494a4ffdde1168718aa097612081bebee674a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDevopsDeployStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoDevopsEnabled")
    def auto_devops_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoDevopsEnabled"))

    @auto_devops_enabled.setter
    def auto_devops_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9284ed85e2e0ea9617223e16b4fcd3ba507fd9ceb2092b5799f233674d0eed7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDevopsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="avatar")
    def avatar(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "avatar"))

    @avatar.setter
    def avatar(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28e759bbd484eb31f3bb75433427ea379be520f22d49e5f6ad3937f5d6142583)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "avatar", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="avatarHash")
    def avatar_hash(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "avatarHash"))

    @avatar_hash.setter
    def avatar_hash(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1257c74a1e43481413c1feb3d5001aedec9828b6d5b8b03f3443557a858e4737)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "avatarHash", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="buildCoverageRegex")
    def build_coverage_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildCoverageRegex"))

    @build_coverage_regex.setter
    def build_coverage_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c47413678c8932dd842b5b790aa22ce2ec89bde2e61f7b809ac62428ec17af0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildCoverageRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="buildGitStrategy")
    def build_git_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildGitStrategy"))

    @build_git_strategy.setter
    def build_git_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2762d906019fdeffd60048d8bd847fd44675d624ada12ddf20a9f36406f4beb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildGitStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="buildsAccessLevel")
    def builds_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildsAccessLevel"))

    @builds_access_level.setter
    def builds_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__599a4629b0752678f346673f118eab7cd897571562f3d31f3fe697ad9cd86579)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildsAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="buildTimeout")
    def build_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "buildTimeout"))

    @build_timeout.setter
    def build_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f745441f0a34dcf878662e649b32fbeaa6a10836856b3ec3f2b1c8ca271d047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ciConfigPath")
    def ci_config_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ciConfigPath"))

    @ci_config_path.setter
    def ci_config_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93b40184dd6b51f071d3210a3a7b13f9e740df9c1b253a6ea2ddd01dde780ae6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ciConfigPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ciDefaultGitDepth")
    def ci_default_git_depth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ciDefaultGitDepth"))

    @ci_default_git_depth.setter
    def ci_default_git_depth(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a86511b3970b7ac819e7a0586dfdc12fb21b7c31dc97573427c09c3e1218ea1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ciDefaultGitDepth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ciDeletePipelinesInSeconds")
    def ci_delete_pipelines_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ciDeletePipelinesInSeconds"))

    @ci_delete_pipelines_in_seconds.setter
    def ci_delete_pipelines_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4775d75147f6e136dc035cd8f64317b27e0b235832aa65c5c3301de6b0209a30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ciDeletePipelinesInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ciForwardDeploymentEnabled")
    def ci_forward_deployment_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ciForwardDeploymentEnabled"))

    @ci_forward_deployment_enabled.setter
    def ci_forward_deployment_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7650d35b8fd0580ff2e0df59e0854f23713e9e4a1b0062f211d0a242ee819703)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ciForwardDeploymentEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ciIdTokenSubClaimComponents")
    def ci_id_token_sub_claim_components(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ciIdTokenSubClaimComponents"))

    @ci_id_token_sub_claim_components.setter
    def ci_id_token_sub_claim_components(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ed6f0134a541ec09572ce91aed5061c1cb07a17e84f2754d57c0c2e038b90f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ciIdTokenSubClaimComponents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ciPipelineVariablesMinimumOverrideRole")
    def ci_pipeline_variables_minimum_override_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ciPipelineVariablesMinimumOverrideRole"))

    @ci_pipeline_variables_minimum_override_role.setter
    def ci_pipeline_variables_minimum_override_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bd6f7bbe3ad16bc73b8bbb181292c84e6ae13f253f26bd5778b3e8397d0a55b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ciPipelineVariablesMinimumOverrideRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ciRestrictPipelineCancellationRole")
    def ci_restrict_pipeline_cancellation_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ciRestrictPipelineCancellationRole"))

    @ci_restrict_pipeline_cancellation_role.setter
    def ci_restrict_pipeline_cancellation_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a87736c2bea32c96e5e0868709cd3e9a86e9a9cbefdd4474c4991d519360e5a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ciRestrictPipelineCancellationRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ciSeparatedCaches")
    def ci_separated_caches(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ciSeparatedCaches"))

    @ci_separated_caches.setter
    def ci_separated_caches(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03b41dab6c5c58a2ad3b77370c008e30a460414aa8adc6cf566378dc61cf8158)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ciSeparatedCaches", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerRegistryAccessLevel")
    def container_registry_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerRegistryAccessLevel"))

    @container_registry_access_level.setter
    def container_registry_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5db40d9a0ef7dcc1912a12fe88d0d1bc91f4776ff2fd2012d93318a0e537c1a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerRegistryAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerRegistryEnabled")
    def container_registry_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "containerRegistryEnabled"))

    @container_registry_enabled.setter
    def container_registry_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc779dceb7b8d00ee010c0cc760845775c915b4bc4ab9253a0eeb4f17ef8fa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerRegistryEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultBranch")
    def default_branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultBranch"))

    @default_branch.setter
    def default_branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__492dde2baafa69396d477930efffb6ba89d2213cae2b0cfb3479e9e32d277c7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultBranch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fb6d0cdd4255a769e976bcb3bc878be0ba6e29bd9d2d765c6e229854ea92ee3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailsEnabled")
    def emails_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "emailsEnabled"))

    @emails_enabled.setter
    def emails_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__876b224f773bd1d500f4ac6bf2fb0e1d25ccc999c7f77a2d6bbf227e32cbaf6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environmentsAccessLevel")
    def environments_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environmentsAccessLevel"))

    @environments_access_level.setter
    def environments_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbff0b897676ff143b34e6ee490c9d26aae11b99eac93c9bfb53d89494432f54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentsAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalAuthorizationClassificationLabel")
    def external_authorization_classification_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalAuthorizationClassificationLabel"))

    @external_authorization_classification_label.setter
    def external_authorization_classification_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5301348d3ea99c18c7b3c79bc8929be85044849e36d0c3c3769fc7914f7d2a17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalAuthorizationClassificationLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="featureFlagsAccessLevel")
    def feature_flags_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "featureFlagsAccessLevel"))

    @feature_flags_access_level.setter
    def feature_flags_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f365a7d3032fee5168227e39f870d1989e35034c46c04f127a776b73a5e67f9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featureFlagsAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forkedFromProjectId")
    def forked_from_project_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "forkedFromProjectId"))

    @forked_from_project_id.setter
    def forked_from_project_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9f9542ff4ec6e2dc282d33a9e45e2d5cef29865875239790fe3f2cf763a772f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forkedFromProjectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forkingAccessLevel")
    def forking_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forkingAccessLevel"))

    @forking_access_level.setter
    def forking_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0360cb384a360c4c3fce95e8976223252da3b4f8d4d61cff8ca416675a28221)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forkingAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupRunnersEnabled")
    def group_runners_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "groupRunnersEnabled"))

    @group_runners_enabled.setter
    def group_runners_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0166083d46b7cc1c136a32fef50a9ad7df545edf1de6bc48c83450d8174cc848)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupRunnersEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupWithProjectTemplatesId")
    def group_with_project_templates_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "groupWithProjectTemplatesId"))

    @group_with_project_templates_id.setter
    def group_with_project_templates_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2344b0f84ecbad1dd7bda33d68cac69caedb27f4672e3ac8adcd52157fc5b266)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupWithProjectTemplatesId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__391e59e752248192b195825a881e1abb207ae32841ab8c634a168d93d2599016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="importUrl")
    def import_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "importUrl"))

    @import_url.setter
    def import_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c0ada320871e88cdbc2d83a83e8e3fa4ab7e4546da98f9e3ee1e85ec2b55406)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="importUrlPassword")
    def import_url_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "importUrlPassword"))

    @import_url_password.setter
    def import_url_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__085f6adb0eede64b94af40382f2aa9e52ef3180ad64b9db1952801c12aa336fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importUrlPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="importUrlUsername")
    def import_url_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "importUrlUsername"))

    @import_url_username.setter
    def import_url_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac3b79e43e8e550c10510efbd2d96c423e4c74cd28cc5e314f901ca66594d10b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importUrlUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="infrastructureAccessLevel")
    def infrastructure_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "infrastructureAccessLevel"))

    @infrastructure_access_level.setter
    def infrastructure_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4583e76e277b53c054ac08a0715ac2636fec0a9c5dfeed9584c27be54a15d00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "infrastructureAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initializeWithReadme")
    def initialize_with_readme(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "initializeWithReadme"))

    @initialize_with_readme.setter
    def initialize_with_readme(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f365eabdf77d2437c4ce7d12bedeb78368985dc9362440d9907828b18a5284f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initializeWithReadme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuesAccessLevel")
    def issues_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuesAccessLevel"))

    @issues_access_level.setter
    def issues_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__961d059d1b52f5cb577dcfa5fdd0b1723e7484c72ef43200600a7c20f6b039b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuesAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuesEnabled")
    def issues_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "issuesEnabled"))

    @issues_enabled.setter
    def issues_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ca288aee588c70082fff179787b08045491fbd5a3d3f598fc41531ce23023e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuesTemplate")
    def issues_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuesTemplate"))

    @issues_template.setter
    def issues_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b801cc53a73f6d3abaad0b099323a134fc4dd6a82bfb0e23a4a57df8ffbe026c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuesTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keepLatestArtifact")
    def keep_latest_artifact(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "keepLatestArtifact"))

    @keep_latest_artifact.setter
    def keep_latest_artifact(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3769adc0ba16bd78c545aa019135d42ed874ee57c217db73bee73c975344dcfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepLatestArtifact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lfsEnabled")
    def lfs_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "lfsEnabled"))

    @lfs_enabled.setter
    def lfs_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f71d99a7a3f9e42f96b8e9ebfbcd99cd660132b9004c853a7c9df493b9fb0ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lfsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mergeCommitTemplate")
    def merge_commit_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mergeCommitTemplate"))

    @merge_commit_template.setter
    def merge_commit_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__807a0c19cc8e6d11627c375fb6e4a37b67348b1ca38332f865a471399b1d3b1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mergeCommitTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mergeMethod")
    def merge_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mergeMethod"))

    @merge_method.setter
    def merge_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c35e3966cb22c86168b62e5477829a3080cf0be773ac232a79426bafbe1c7f98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mergeMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mergePipelinesEnabled")
    def merge_pipelines_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mergePipelinesEnabled"))

    @merge_pipelines_enabled.setter
    def merge_pipelines_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__216deebc496425c752d80670209cb6d2e8bc5d24342793d9461e8bac5b8ff944)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mergePipelinesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mergeRequestsAccessLevel")
    def merge_requests_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mergeRequestsAccessLevel"))

    @merge_requests_access_level.setter
    def merge_requests_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28edbd395755370de227b620571a95e688cf290532c080160c0f595896cf563a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mergeRequestsAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mergeRequestsEnabled")
    def merge_requests_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mergeRequestsEnabled"))

    @merge_requests_enabled.setter
    def merge_requests_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3538e1a91bd84cd99395599a447f384a07f34f0be3aa0ca5c7954bb06310a76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mergeRequestsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mergeRequestsTemplate")
    def merge_requests_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mergeRequestsTemplate"))

    @merge_requests_template.setter
    def merge_requests_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65fbf0b38939ded6b2c74f532b1855bd660c98b821388ff140738afe8f46a279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mergeRequestsTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mergeTrainsEnabled")
    def merge_trains_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mergeTrainsEnabled"))

    @merge_trains_enabled.setter
    def merge_trains_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19dc42d2760288cc84f1f93ac2280d9ea807f65c8856cae47d0c51e6677d45f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mergeTrainsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mirror")
    def mirror(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mirror"))

    @mirror.setter
    def mirror(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f6892b08f576f7be0fda65cba031d8b6efcc54296965591a3e9ee8d7f6b5232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mirror", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mirrorOverwritesDivergedBranches")
    def mirror_overwrites_diverged_branches(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mirrorOverwritesDivergedBranches"))

    @mirror_overwrites_diverged_branches.setter
    def mirror_overwrites_diverged_branches(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcbdea53b7bbb6a16bfdac864b3058129139c6fa76e089c5c5579b95515010d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mirrorOverwritesDivergedBranches", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mirrorTriggerBuilds")
    def mirror_trigger_builds(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mirrorTriggerBuilds"))

    @mirror_trigger_builds.setter
    def mirror_trigger_builds(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25c667ad7dfb5114afaf82f8250c5a709c0c7b80e0eef0b963668ab56e4fe67b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mirrorTriggerBuilds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelExperimentsAccessLevel")
    def model_experiments_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelExperimentsAccessLevel"))

    @model_experiments_access_level.setter
    def model_experiments_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd50df7c617ed8af0561205440168a8bd741b80f71ee40014113a48b52006ca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelExperimentsAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelRegistryAccessLevel")
    def model_registry_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelRegistryAccessLevel"))

    @model_registry_access_level.setter
    def model_registry_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85312fdd83ff00e5f418d3a02111a493d9b0e48efa487149bfa35cf3772ea388)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelRegistryAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monitorAccessLevel")
    def monitor_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monitorAccessLevel"))

    @monitor_access_level.setter
    def monitor_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5029ebe9cf78a0ce2a9e81189b27c01a7705a114eb756512b9fe4b7ac4b2ed9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitorAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mrDefaultTargetSelf")
    def mr_default_target_self(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mrDefaultTargetSelf"))

    @mr_default_target_self.setter
    def mr_default_target_self(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59273e9ff19fb4854698988e9aa58241e9ca822b6e8ac29d20ab4144f975fb53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mrDefaultTargetSelf", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fe03191df7018c3fba732187b9038e8f4fccf70e7de45d0010e20af4e8cbaf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "namespaceId"))

    @namespace_id.setter
    def namespace_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c729a1ea7a441913e553f92587c61220e9b766530c8e9ff4b3e234de11d241)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onlyAllowMergeIfAllDiscussionsAreResolved")
    def only_allow_merge_if_all_discussions_are_resolved(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "onlyAllowMergeIfAllDiscussionsAreResolved"))

    @only_allow_merge_if_all_discussions_are_resolved.setter
    def only_allow_merge_if_all_discussions_are_resolved(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bd4fb866305ee70afa162ec6625153065028d64445e4672dd13c65e69794cdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onlyAllowMergeIfAllDiscussionsAreResolved", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onlyAllowMergeIfPipelineSucceeds")
    def only_allow_merge_if_pipeline_succeeds(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "onlyAllowMergeIfPipelineSucceeds"))

    @only_allow_merge_if_pipeline_succeeds.setter
    def only_allow_merge_if_pipeline_succeeds(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04bc734a522fd8dea632af021fcf98a65ba97a614dbce827ec40e1f6ce48a01e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onlyAllowMergeIfPipelineSucceeds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onlyMirrorProtectedBranches")
    def only_mirror_protected_branches(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "onlyMirrorProtectedBranches"))

    @only_mirror_protected_branches.setter
    def only_mirror_protected_branches(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef1232b53bc8d11118fc976db5aa1aa66a4a02aeeb72724908f9d37d17df770b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onlyMirrorProtectedBranches", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="packagesEnabled")
    def packages_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "packagesEnabled"))

    @packages_enabled.setter
    def packages_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81d8f09149c1bdf9df31a77779d693ac195471bb9af67f36f3466483799a8aec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packagesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pagesAccessLevel")
    def pages_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pagesAccessLevel"))

    @pages_access_level.setter
    def pages_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0648bc69a76a430e2e7e7c0755e263cca0e765e542f92e9bcd78d0b375849d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pagesAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__377be5d79e807f244068fd9277e04ccbad92dda8d73101853f4b5c6737bdc40c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permanentlyDeleteOnDestroy")
    def permanently_delete_on_destroy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "permanentlyDeleteOnDestroy"))

    @permanently_delete_on_destroy.setter
    def permanently_delete_on_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6f8f919087e719e4d2b6ce712258dac9d4fc104dd2423aca6207c758a13dd8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permanentlyDeleteOnDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pipelinesEnabled")
    def pipelines_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pipelinesEnabled"))

    @pipelines_enabled.setter
    def pipelines_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7c14219bd1444855a494bf1e70ee2e756c2983fbe85c2c1b82a8ee75582cc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pipelinesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preReceiveSecretDetectionEnabled")
    def pre_receive_secret_detection_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preReceiveSecretDetectionEnabled"))

    @pre_receive_secret_detection_enabled.setter
    def pre_receive_secret_detection_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f16afb98921b2fea618f023f0786c760f5b6f7c97716da0dbc961bc3dd67b328)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preReceiveSecretDetectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preventMergeWithoutJiraIssue")
    def prevent_merge_without_jira_issue(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preventMergeWithoutJiraIssue"))

    @prevent_merge_without_jira_issue.setter
    def prevent_merge_without_jira_issue(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81f2cc0b438b62cde5f4b79f3434b245dbae76ba15e9d576dfd91782a4c6b2e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preventMergeWithoutJiraIssue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="printingMergeRequestLinkEnabled")
    def printing_merge_request_link_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "printingMergeRequestLinkEnabled"))

    @printing_merge_request_link_enabled.setter
    def printing_merge_request_link_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35be9e2abc1c8fe52ab7dde656a07ac62fc88cf75d37dc7cca65773fd62c8610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "printingMergeRequestLinkEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicBuilds")
    def public_builds(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publicBuilds"))

    @public_builds.setter
    def public_builds(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e080aff4eeb5c856f75ea07fe760527c5122e49383939b428668e2f940939536)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicBuilds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicJobs")
    def public_jobs(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publicJobs"))

    @public_jobs.setter
    def public_jobs(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d002f034e319569568f3e5ec835ba0d145b60b1caee7ecd37aed11429859f65a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicJobs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="releasesAccessLevel")
    def releases_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "releasesAccessLevel"))

    @releases_access_level.setter
    def releases_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16af67f6205a368a583e39305e287827497af4eb9cf5ceaf9cdd1112903329d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "releasesAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="removeSourceBranchAfterMerge")
    def remove_source_branch_after_merge(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "removeSourceBranchAfterMerge"))

    @remove_source_branch_after_merge.setter
    def remove_source_branch_after_merge(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b377615606c8ba5a32679029843541aa633183f9780441d9fa9dad9e2986d422)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "removeSourceBranchAfterMerge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryAccessLevel")
    def repository_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryAccessLevel"))

    @repository_access_level.setter
    def repository_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a6645d6afc8062aa440727b5ffa1a26087c18826d9d9a2db439aa31d1ea843)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryStorage")
    def repository_storage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryStorage"))

    @repository_storage.setter
    def repository_storage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16212c2e5baae9c569df56996300e476c2fd47180fc8e3c0b0c1394f351c265f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryStorage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestAccessEnabled")
    def request_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requestAccessEnabled"))

    @request_access_enabled.setter
    def request_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ddd9f7ec538b2c71b0bb82cb85db6ec209f484f4718533c785da8084ea5d970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requirementsAccessLevel")
    def requirements_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requirementsAccessLevel"))

    @requirements_access_level.setter
    def requirements_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ee3e507cd3dfa5fe67519ff1300271bb29fa878636f0969564408a90b518170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requirementsAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resolveOutdatedDiffDiscussions")
    def resolve_outdated_diff_discussions(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "resolveOutdatedDiffDiscussions"))

    @resolve_outdated_diff_discussions.setter
    def resolve_outdated_diff_discussions(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbf428cca7b3d41eead73b3de4b3816d28aa426991c5362a07e92755ed06a041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resolveOutdatedDiffDiscussions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restrictUserDefinedVariables")
    def restrict_user_defined_variables(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "restrictUserDefinedVariables"))

    @restrict_user_defined_variables.setter
    def restrict_user_defined_variables(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58ef947f89a0a66660346a8d6865cafb067ee82e63dd48a67af64e310ca15ec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restrictUserDefinedVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityAndComplianceAccessLevel")
    def security_and_compliance_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityAndComplianceAccessLevel"))

    @security_and_compliance_access_level.setter
    def security_and_compliance_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1643543e2f32823446517da824f9c39ed66e7c3508c1a6c74856e97f4f351fea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityAndComplianceAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sharedRunnersEnabled")
    def shared_runners_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sharedRunnersEnabled"))

    @shared_runners_enabled.setter
    def shared_runners_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff5a9c9a3fc2a8e366c93e75dabb5ef345c7fee7200a4d4fcf444d064f38fcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedRunnersEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipWaitForDefaultBranchProtection")
    def skip_wait_for_default_branch_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipWaitForDefaultBranchProtection"))

    @skip_wait_for_default_branch_protection.setter
    def skip_wait_for_default_branch_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28b864416593aed0d3d9ebf0efd84985e815203c92278b69778e4bc5bd7fd7c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipWaitForDefaultBranchProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snippetsAccessLevel")
    def snippets_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snippetsAccessLevel"))

    @snippets_access_level.setter
    def snippets_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f7becac67df745ba9b200bcae9c6f9d48b6247a9e5fb217c9441027f6f3be23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snippetsAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snippetsEnabled")
    def snippets_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "snippetsEnabled"))

    @snippets_enabled.setter
    def snippets_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6726fc26ce61f1fccf04e8a4fd15326334e70850a5984c52ed4f8bc1c69a6d4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snippetsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="squashCommitTemplate")
    def squash_commit_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "squashCommitTemplate"))

    @squash_commit_template.setter
    def squash_commit_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__062cae4af9a002ccffc3b292bf579f19bf648acaf47f3ca95a7b114d45b1a749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "squashCommitTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="squashOption")
    def squash_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "squashOption"))

    @squash_option.setter
    def squash_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37db4feb5e1e379087e07b556a604ff8ace30ce05f5076c2c62f914d44960960)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "squashOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suggestionCommitMessage")
    def suggestion_commit_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suggestionCommitMessage"))

    @suggestion_commit_message.setter
    def suggestion_commit_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33def3fb4e82a4ac9bdebf5caa77376811703f8542591fefd6660a869826686e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suggestionCommitMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__395930ac24bda9ce44f7b4fc001ba815af5167c42ed6ef94d0446395ebb5c463)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "templateName"))

    @template_name.setter
    def template_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a974616584f3ddca0989c9c17343d580e23cc76a6532d42cfb8e83dc6f387eaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="templateProjectId")
    def template_project_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "templateProjectId"))

    @template_project_id.setter
    def template_project_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e6f27f4ad4895e7022c0306369344a2c3837d669cd317f3e74feed5c954e36a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateProjectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topics")
    def topics(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "topics"))

    @topics.setter
    def topics(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__717788577432e647953afa83c2a5275a7fdabfa3cb7d7954d9750fa01f39ce4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useCustomTemplate")
    def use_custom_template(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useCustomTemplate"))

    @use_custom_template.setter
    def use_custom_template(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb2f90fac3851cd716edbeec477216976ab7fa90ddadf6fa17db0c5f3cf4085f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useCustomTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visibilityLevel")
    def visibility_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibilityLevel"))

    @visibility_level.setter
    def visibility_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0ca540dde10854c71011ebd382cd4818e02380a3728ba2359a3d71c1c763ff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibilityLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wikiAccessLevel")
    def wiki_access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "wikiAccessLevel"))

    @wiki_access_level.setter
    def wiki_access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7242aa4a23953bff60de74ba06a9182344f538db264f1c0cdc43085ab3de60c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wikiAccessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wikiEnabled")
    def wiki_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "wikiEnabled"))

    @wiki_enabled.setter
    def wiki_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__649074350ece8bf58f2ca799e281aaa440d4f8185669bfe963223812e67b2c6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wikiEnabled", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.project.ProjectConfig",
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
        "allow_merge_on_skipped_pipeline": "allowMergeOnSkippedPipeline",
        "allow_pipeline_trigger_approve_deployment": "allowPipelineTriggerApproveDeployment",
        "analytics_access_level": "analyticsAccessLevel",
        "approvals_before_merge": "approvalsBeforeMerge",
        "archived": "archived",
        "archive_on_destroy": "archiveOnDestroy",
        "auto_cancel_pending_pipelines": "autoCancelPendingPipelines",
        "autoclose_referenced_issues": "autocloseReferencedIssues",
        "auto_devops_deploy_strategy": "autoDevopsDeployStrategy",
        "auto_devops_enabled": "autoDevopsEnabled",
        "avatar": "avatar",
        "avatar_hash": "avatarHash",
        "build_coverage_regex": "buildCoverageRegex",
        "build_git_strategy": "buildGitStrategy",
        "builds_access_level": "buildsAccessLevel",
        "build_timeout": "buildTimeout",
        "ci_config_path": "ciConfigPath",
        "ci_default_git_depth": "ciDefaultGitDepth",
        "ci_delete_pipelines_in_seconds": "ciDeletePipelinesInSeconds",
        "ci_forward_deployment_enabled": "ciForwardDeploymentEnabled",
        "ci_id_token_sub_claim_components": "ciIdTokenSubClaimComponents",
        "ci_pipeline_variables_minimum_override_role": "ciPipelineVariablesMinimumOverrideRole",
        "ci_restrict_pipeline_cancellation_role": "ciRestrictPipelineCancellationRole",
        "ci_separated_caches": "ciSeparatedCaches",
        "container_expiration_policy": "containerExpirationPolicy",
        "container_registry_access_level": "containerRegistryAccessLevel",
        "container_registry_enabled": "containerRegistryEnabled",
        "default_branch": "defaultBranch",
        "description": "description",
        "emails_enabled": "emailsEnabled",
        "environments_access_level": "environmentsAccessLevel",
        "external_authorization_classification_label": "externalAuthorizationClassificationLabel",
        "feature_flags_access_level": "featureFlagsAccessLevel",
        "forked_from_project_id": "forkedFromProjectId",
        "forking_access_level": "forkingAccessLevel",
        "group_runners_enabled": "groupRunnersEnabled",
        "group_with_project_templates_id": "groupWithProjectTemplatesId",
        "id": "id",
        "import_url": "importUrl",
        "import_url_password": "importUrlPassword",
        "import_url_username": "importUrlUsername",
        "infrastructure_access_level": "infrastructureAccessLevel",
        "initialize_with_readme": "initializeWithReadme",
        "issues_access_level": "issuesAccessLevel",
        "issues_enabled": "issuesEnabled",
        "issues_template": "issuesTemplate",
        "keep_latest_artifact": "keepLatestArtifact",
        "lfs_enabled": "lfsEnabled",
        "merge_commit_template": "mergeCommitTemplate",
        "merge_method": "mergeMethod",
        "merge_pipelines_enabled": "mergePipelinesEnabled",
        "merge_requests_access_level": "mergeRequestsAccessLevel",
        "merge_requests_enabled": "mergeRequestsEnabled",
        "merge_requests_template": "mergeRequestsTemplate",
        "merge_trains_enabled": "mergeTrainsEnabled",
        "mirror": "mirror",
        "mirror_overwrites_diverged_branches": "mirrorOverwritesDivergedBranches",
        "mirror_trigger_builds": "mirrorTriggerBuilds",
        "model_experiments_access_level": "modelExperimentsAccessLevel",
        "model_registry_access_level": "modelRegistryAccessLevel",
        "monitor_access_level": "monitorAccessLevel",
        "mr_default_target_self": "mrDefaultTargetSelf",
        "namespace_id": "namespaceId",
        "only_allow_merge_if_all_discussions_are_resolved": "onlyAllowMergeIfAllDiscussionsAreResolved",
        "only_allow_merge_if_pipeline_succeeds": "onlyAllowMergeIfPipelineSucceeds",
        "only_mirror_protected_branches": "onlyMirrorProtectedBranches",
        "packages_enabled": "packagesEnabled",
        "pages_access_level": "pagesAccessLevel",
        "path": "path",
        "permanently_delete_on_destroy": "permanentlyDeleteOnDestroy",
        "pipelines_enabled": "pipelinesEnabled",
        "pre_receive_secret_detection_enabled": "preReceiveSecretDetectionEnabled",
        "prevent_merge_without_jira_issue": "preventMergeWithoutJiraIssue",
        "printing_merge_request_link_enabled": "printingMergeRequestLinkEnabled",
        "public_builds": "publicBuilds",
        "public_jobs": "publicJobs",
        "push_rules": "pushRules",
        "releases_access_level": "releasesAccessLevel",
        "remove_source_branch_after_merge": "removeSourceBranchAfterMerge",
        "repository_access_level": "repositoryAccessLevel",
        "repository_storage": "repositoryStorage",
        "request_access_enabled": "requestAccessEnabled",
        "requirements_access_level": "requirementsAccessLevel",
        "resolve_outdated_diff_discussions": "resolveOutdatedDiffDiscussions",
        "restrict_user_defined_variables": "restrictUserDefinedVariables",
        "security_and_compliance_access_level": "securityAndComplianceAccessLevel",
        "shared_runners_enabled": "sharedRunnersEnabled",
        "skip_wait_for_default_branch_protection": "skipWaitForDefaultBranchProtection",
        "snippets_access_level": "snippetsAccessLevel",
        "snippets_enabled": "snippetsEnabled",
        "squash_commit_template": "squashCommitTemplate",
        "squash_option": "squashOption",
        "suggestion_commit_message": "suggestionCommitMessage",
        "tags": "tags",
        "template_name": "templateName",
        "template_project_id": "templateProjectId",
        "timeouts": "timeouts",
        "topics": "topics",
        "use_custom_template": "useCustomTemplate",
        "visibility_level": "visibilityLevel",
        "wiki_access_level": "wikiAccessLevel",
        "wiki_enabled": "wikiEnabled",
    },
)
class ProjectConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        allow_merge_on_skipped_pipeline: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_pipeline_trigger_approve_deployment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        analytics_access_level: typing.Optional[builtins.str] = None,
        approvals_before_merge: typing.Optional[jsii.Number] = None,
        archived: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        archive_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_cancel_pending_pipelines: typing.Optional[builtins.str] = None,
        autoclose_referenced_issues: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_devops_deploy_strategy: typing.Optional[builtins.str] = None,
        auto_devops_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        avatar: typing.Optional[builtins.str] = None,
        avatar_hash: typing.Optional[builtins.str] = None,
        build_coverage_regex: typing.Optional[builtins.str] = None,
        build_git_strategy: typing.Optional[builtins.str] = None,
        builds_access_level: typing.Optional[builtins.str] = None,
        build_timeout: typing.Optional[jsii.Number] = None,
        ci_config_path: typing.Optional[builtins.str] = None,
        ci_default_git_depth: typing.Optional[jsii.Number] = None,
        ci_delete_pipelines_in_seconds: typing.Optional[jsii.Number] = None,
        ci_forward_deployment_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ci_id_token_sub_claim_components: typing.Optional[typing.Sequence[builtins.str]] = None,
        ci_pipeline_variables_minimum_override_role: typing.Optional[builtins.str] = None,
        ci_restrict_pipeline_cancellation_role: typing.Optional[builtins.str] = None,
        ci_separated_caches: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        container_expiration_policy: typing.Optional[typing.Union["ProjectContainerExpirationPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        container_registry_access_level: typing.Optional[builtins.str] = None,
        container_registry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_branch: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        emails_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        environments_access_level: typing.Optional[builtins.str] = None,
        external_authorization_classification_label: typing.Optional[builtins.str] = None,
        feature_flags_access_level: typing.Optional[builtins.str] = None,
        forked_from_project_id: typing.Optional[jsii.Number] = None,
        forking_access_level: typing.Optional[builtins.str] = None,
        group_runners_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        group_with_project_templates_id: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        import_url: typing.Optional[builtins.str] = None,
        import_url_password: typing.Optional[builtins.str] = None,
        import_url_username: typing.Optional[builtins.str] = None,
        infrastructure_access_level: typing.Optional[builtins.str] = None,
        initialize_with_readme: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        issues_access_level: typing.Optional[builtins.str] = None,
        issues_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        issues_template: typing.Optional[builtins.str] = None,
        keep_latest_artifact: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lfs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        merge_commit_template: typing.Optional[builtins.str] = None,
        merge_method: typing.Optional[builtins.str] = None,
        merge_pipelines_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        merge_requests_access_level: typing.Optional[builtins.str] = None,
        merge_requests_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        merge_requests_template: typing.Optional[builtins.str] = None,
        merge_trains_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mirror: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mirror_overwrites_diverged_branches: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mirror_trigger_builds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        model_experiments_access_level: typing.Optional[builtins.str] = None,
        model_registry_access_level: typing.Optional[builtins.str] = None,
        monitor_access_level: typing.Optional[builtins.str] = None,
        mr_default_target_self: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        namespace_id: typing.Optional[jsii.Number] = None,
        only_allow_merge_if_all_discussions_are_resolved: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        only_allow_merge_if_pipeline_succeeds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        only_mirror_protected_branches: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        packages_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pages_access_level: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        permanently_delete_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pipelines_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pre_receive_secret_detection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prevent_merge_without_jira_issue: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        printing_merge_request_link_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_builds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_jobs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        push_rules: typing.Optional[typing.Union["ProjectPushRules", typing.Dict[builtins.str, typing.Any]]] = None,
        releases_access_level: typing.Optional[builtins.str] = None,
        remove_source_branch_after_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        repository_access_level: typing.Optional[builtins.str] = None,
        repository_storage: typing.Optional[builtins.str] = None,
        request_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        requirements_access_level: typing.Optional[builtins.str] = None,
        resolve_outdated_diff_discussions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restrict_user_defined_variables: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_and_compliance_access_level: typing.Optional[builtins.str] = None,
        shared_runners_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_wait_for_default_branch_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        snippets_access_level: typing.Optional[builtins.str] = None,
        snippets_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        squash_commit_template: typing.Optional[builtins.str] = None,
        squash_option: typing.Optional[builtins.str] = None,
        suggestion_commit_message: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        template_name: typing.Optional[builtins.str] = None,
        template_project_id: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["ProjectTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        topics: typing.Optional[typing.Sequence[builtins.str]] = None,
        use_custom_template: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        visibility_level: typing.Optional[builtins.str] = None,
        wiki_access_level: typing.Optional[builtins.str] = None,
        wiki_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#name Project#name}
        :param allow_merge_on_skipped_pipeline: Set to true if you want to treat skipped pipelines as if they finished with success. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#allow_merge_on_skipped_pipeline Project#allow_merge_on_skipped_pipeline}
        :param allow_pipeline_trigger_approve_deployment: Set whether or not a pipeline triggerer is allowed to approve deployments. Premium and Ultimate only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#allow_pipeline_trigger_approve_deployment Project#allow_pipeline_trigger_approve_deployment}
        :param analytics_access_level: Set the analytics access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#analytics_access_level Project#analytics_access_level}
        :param approvals_before_merge: Number of merge request approvals required for merging. Default is 0. This field **does not** work well in combination with the ``gitlab_project_approval_rule`` resource and is most likely gonna be deprecated in a future GitLab version (see `this upstream epic <https://gitlab.com/groups/gitlab-org/-/epics/7572>`_). In the meantime we recommend against using this attribute and use ``gitlab_project_approval_rule`` instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#approvals_before_merge Project#approvals_before_merge}
        :param archived: Whether the project is in read-only mode (archived). Repositories can be archived/unarchived by toggling this parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#archived Project#archived}
        :param archive_on_destroy: Set to ``true`` to archive the project instead of deleting on destroy. If set to ``true`` it will entire omit the ``DELETE`` operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#archive_on_destroy Project#archive_on_destroy}
        :param auto_cancel_pending_pipelines: Auto-cancel pending pipelines. This isn’t a boolean, but enabled/disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#auto_cancel_pending_pipelines Project#auto_cancel_pending_pipelines}
        :param autoclose_referenced_issues: Set whether auto-closing referenced issues on default branch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#autoclose_referenced_issues Project#autoclose_referenced_issues}
        :param auto_devops_deploy_strategy: Auto Deploy strategy. Valid values are ``continuous``, ``manual``, ``timed_incremental``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#auto_devops_deploy_strategy Project#auto_devops_deploy_strategy}
        :param auto_devops_enabled: Enable Auto DevOps for this project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#auto_devops_enabled Project#auto_devops_enabled}
        :param avatar: A local path to the avatar image to upload. **Note**: not available for imported resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#avatar Project#avatar}
        :param avatar_hash: The hash of the avatar image. Use ``filesha256("path/to/avatar.png")`` whenever possible. **Note**: this is used to trigger an update of the avatar. If it's not given, but an avatar is given, the avatar will be updated each time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#avatar_hash Project#avatar_hash}
        :param build_coverage_regex: Test coverage parsing for the project. This is deprecated feature in GitLab 15.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#build_coverage_regex Project#build_coverage_regex}
        :param build_git_strategy: The Git strategy. Defaults to fetch. Valid values are ``clone``, ``fetch``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#build_git_strategy Project#build_git_strategy}
        :param builds_access_level: Set the builds access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#builds_access_level Project#builds_access_level}
        :param build_timeout: The maximum amount of time, in seconds, that a job can run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#build_timeout Project#build_timeout}
        :param ci_config_path: Custom Path to CI config file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_config_path Project#ci_config_path}
        :param ci_default_git_depth: Default number of revisions for shallow cloning. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_default_git_depth Project#ci_default_git_depth}
        :param ci_delete_pipelines_in_seconds: Pipelines older than the configured time are deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_delete_pipelines_in_seconds Project#ci_delete_pipelines_in_seconds}
        :param ci_forward_deployment_enabled: When a new deployment job starts, skip older deployment jobs that are still pending. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_forward_deployment_enabled Project#ci_forward_deployment_enabled}
        :param ci_id_token_sub_claim_components: Fields included in the sub claim of the ID Token. Accepts an array starting with project_path. The array might also include ref_type and ref. Defaults to ["project_path", "ref_type", "ref"]. Introduced in GitLab 17.10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_id_token_sub_claim_components Project#ci_id_token_sub_claim_components}
        :param ci_pipeline_variables_minimum_override_role: The minimum role required to set variables when running pipelines and jobs. Introduced in GitLab 17.1. Valid values are ``developer``, ``maintainer``, ``owner``, ``no_one_allowed`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_pipeline_variables_minimum_override_role Project#ci_pipeline_variables_minimum_override_role}
        :param ci_restrict_pipeline_cancellation_role: The role required to cancel a pipeline or job. Premium and Ultimate only. Valid values are ``developer``, ``maintainer``, ``no one`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_restrict_pipeline_cancellation_role Project#ci_restrict_pipeline_cancellation_role}
        :param ci_separated_caches: Use separate caches for protected branches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_separated_caches Project#ci_separated_caches}
        :param container_expiration_policy: container_expiration_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#container_expiration_policy Project#container_expiration_policy}
        :param container_registry_access_level: Set visibility of container registry, for this project. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#container_registry_access_level Project#container_registry_access_level}
        :param container_registry_enabled: Enable container registry for the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#container_registry_enabled Project#container_registry_enabled}
        :param default_branch: The default branch for the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#default_branch Project#default_branch}
        :param description: A description of the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#description Project#description}
        :param emails_enabled: Enable email notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#emails_enabled Project#emails_enabled}
        :param environments_access_level: Set the environments access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#environments_access_level Project#environments_access_level}
        :param external_authorization_classification_label: The classification label for the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#external_authorization_classification_label Project#external_authorization_classification_label}
        :param feature_flags_access_level: Set the feature flags access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#feature_flags_access_level Project#feature_flags_access_level}
        :param forked_from_project_id: The id of the project to fork. During create the project is forked and during an update the fork relation is changed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#forked_from_project_id Project#forked_from_project_id}
        :param forking_access_level: Set the forking access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#forking_access_level Project#forking_access_level}
        :param group_runners_enabled: Enable group runners for this project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#group_runners_enabled Project#group_runners_enabled}
        :param group_with_project_templates_id: For group-level custom templates, specifies ID of group from which all the custom project templates are sourced. Leave empty for instance-level templates. Requires use_custom_template to be true (enterprise edition). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#group_with_project_templates_id Project#group_with_project_templates_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#id Project#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param import_url: Git URL to a repository to be imported. Together with ``mirror = true`` it will setup a Pull Mirror. This can also be used together with ``forked_from_project_id`` to setup a Pull Mirror for a fork. The fork takes precedence over the import. Make sure to provide the credentials in ``import_url_username`` and ``import_url_password``. GitLab never returns the credentials, thus the provider cannot detect configuration drift in the credentials. They can also not be imported using ``terraform import``. See the examples section for how to properly use it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#import_url Project#import_url}
        :param import_url_password: The password for the ``import_url``. The value of this field is used to construct a valid ``import_url`` and is only related to the provider. This field cannot be imported using ``terraform import``. See the examples section for how to properly use it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#import_url_password Project#import_url_password}
        :param import_url_username: The username for the ``import_url``. The value of this field is used to construct a valid ``import_url`` and is only related to the provider. This field cannot be imported using ``terraform import``. See the examples section for how to properly use it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#import_url_username Project#import_url_username}
        :param infrastructure_access_level: Set the infrastructure access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#infrastructure_access_level Project#infrastructure_access_level}
        :param initialize_with_readme: Create main branch with first commit containing a README.md file. Must be set to ``true`` if importing an uninitialized project with a different ``default_branch``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#initialize_with_readme Project#initialize_with_readme}
        :param issues_access_level: Set the issues access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#issues_access_level Project#issues_access_level}
        :param issues_enabled: Enable issue tracking for the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#issues_enabled Project#issues_enabled}
        :param issues_template: Sets the template for new issues in the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#issues_template Project#issues_template}
        :param keep_latest_artifact: Disable or enable the ability to keep the latest artifact for this project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#keep_latest_artifact Project#keep_latest_artifact}
        :param lfs_enabled: Enable LFS for the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#lfs_enabled Project#lfs_enabled}
        :param merge_commit_template: Template used to create merge commit message in merge requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#merge_commit_template Project#merge_commit_template}
        :param merge_method: Set the merge method. Valid values are ``merge``, ``rebase_merge``, ``ff``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#merge_method Project#merge_method}
        :param merge_pipelines_enabled: Enable or disable merge pipelines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#merge_pipelines_enabled Project#merge_pipelines_enabled}
        :param merge_requests_access_level: Set the merge requests access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#merge_requests_access_level Project#merge_requests_access_level}
        :param merge_requests_enabled: Enable merge requests for the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#merge_requests_enabled Project#merge_requests_enabled}
        :param merge_requests_template: Sets the template for new merge requests in the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#merge_requests_template Project#merge_requests_template}
        :param merge_trains_enabled: Enable or disable merge trains. Requires ``merge_pipelines_enabled`` to be set to ``true`` to take effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#merge_trains_enabled Project#merge_trains_enabled}
        :param mirror: Enable project pull mirror. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#mirror Project#mirror}
        :param mirror_overwrites_diverged_branches: Enable overwrite diverged branches for a mirrored project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#mirror_overwrites_diverged_branches Project#mirror_overwrites_diverged_branches}
        :param mirror_trigger_builds: Enable trigger builds on pushes for a mirrored project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#mirror_trigger_builds Project#mirror_trigger_builds}
        :param model_experiments_access_level: Set visibility of machine learning model experiments. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#model_experiments_access_level Project#model_experiments_access_level}
        :param model_registry_access_level: Set visibility of machine learning model registry. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#model_registry_access_level Project#model_registry_access_level}
        :param monitor_access_level: Set the monitor access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#monitor_access_level Project#monitor_access_level}
        :param mr_default_target_self: For forked projects, target merge requests to this project. If false, the target will be the upstream project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#mr_default_target_self Project#mr_default_target_self}
        :param namespace_id: The namespace (group or user) of the project. Defaults to your user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#namespace_id Project#namespace_id}
        :param only_allow_merge_if_all_discussions_are_resolved: Set to true if you want allow merges only if all discussions are resolved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#only_allow_merge_if_all_discussions_are_resolved Project#only_allow_merge_if_all_discussions_are_resolved}
        :param only_allow_merge_if_pipeline_succeeds: Set to true if you want allow merges only if a pipeline succeeds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#only_allow_merge_if_pipeline_succeeds Project#only_allow_merge_if_pipeline_succeeds}
        :param only_mirror_protected_branches: Enable only mirror protected branches for a mirrored project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#only_mirror_protected_branches Project#only_mirror_protected_branches}
        :param packages_enabled: Enable packages repository for the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#packages_enabled Project#packages_enabled}
        :param pages_access_level: Enable pages access control. Valid values are ``public``, ``private``, ``enabled``, ``disabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#pages_access_level Project#pages_access_level}
        :param path: The path of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#path Project#path}
        :param permanently_delete_on_destroy: Set to ``true`` to immediately permanently delete the project instead of scheduling a delete for Premium and Ultimate tiers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#permanently_delete_on_destroy Project#permanently_delete_on_destroy}
        :param pipelines_enabled: Enable pipelines for the project. The ``pipelines_enabled`` field is being sent as ``jobs_enabled`` in the GitLab API calls. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#pipelines_enabled Project#pipelines_enabled}
        :param pre_receive_secret_detection_enabled: Whether Secret Push Detection is enabled. Requires GitLab Ultimate and at least GitLab 17.3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#pre_receive_secret_detection_enabled Project#pre_receive_secret_detection_enabled}
        :param prevent_merge_without_jira_issue: Set whether merge requests require an associated issue from Jira. Premium and Ultimate only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#prevent_merge_without_jira_issue Project#prevent_merge_without_jira_issue}
        :param printing_merge_request_link_enabled: Show link to create/view merge request when pushing from the command line. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#printing_merge_request_link_enabled Project#printing_merge_request_link_enabled}
        :param public_builds: If true, jobs can be viewed by non-project members. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#public_builds Project#public_builds}
        :param public_jobs: If true, jobs can be viewed by non-project members. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#public_jobs Project#public_jobs}
        :param push_rules: push_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#push_rules Project#push_rules}
        :param releases_access_level: Set the releases access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#releases_access_level Project#releases_access_level}
        :param remove_source_branch_after_merge: Enable ``Delete source branch`` option by default for all new merge requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#remove_source_branch_after_merge Project#remove_source_branch_after_merge}
        :param repository_access_level: Set the repository access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#repository_access_level Project#repository_access_level}
        :param repository_storage: Which storage shard the repository is on. (administrator only). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#repository_storage Project#repository_storage}
        :param request_access_enabled: Allow users to request member access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#request_access_enabled Project#request_access_enabled}
        :param requirements_access_level: Set the requirements access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#requirements_access_level Project#requirements_access_level}
        :param resolve_outdated_diff_discussions: Automatically resolve merge request diffs discussions on lines changed with a push. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#resolve_outdated_diff_discussions Project#resolve_outdated_diff_discussions}
        :param restrict_user_defined_variables: Allow only users with the Maintainer role to pass user-defined variables when triggering a pipeline. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#restrict_user_defined_variables Project#restrict_user_defined_variables}
        :param security_and_compliance_access_level: Set the security and compliance access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#security_and_compliance_access_level Project#security_and_compliance_access_level}
        :param shared_runners_enabled: Enable shared runners for this project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#shared_runners_enabled Project#shared_runners_enabled}
        :param skip_wait_for_default_branch_protection: If ``true``, the default behavior to wait for the default branch protection to be created is skipped. This is necessary if the current user is not an admin and the default branch protection is disabled on an instance-level. There is currently no known way to determine if the default branch protection is disabled on an instance-level for non-admin users. This attribute is only used during resource creation, thus changes are suppressed and the attribute cannot be imported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#skip_wait_for_default_branch_protection Project#skip_wait_for_default_branch_protection}
        :param snippets_access_level: Set the snippets access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#snippets_access_level Project#snippets_access_level}
        :param snippets_enabled: Enable snippets for the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#snippets_enabled Project#snippets_enabled}
        :param squash_commit_template: Template used to create squash commit message in merge requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#squash_commit_template Project#squash_commit_template}
        :param squash_option: Squash commits when merge request is merged. Valid values are ``never`` (Do not allow), ``always`` (Require), ``default_on`` (Encourage), or ``default_off`` (Allow). The default value is ``default_off`` (Allow). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#squash_option Project#squash_option}
        :param suggestion_commit_message: The commit message used to apply merge request suggestions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#suggestion_commit_message Project#suggestion_commit_message}
        :param tags: The list of tags for a project; put array of tags, that should be finally assigned to a project. Use topics instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#tags Project#tags}
        :param template_name: When used without use_custom_template, name of a built-in project template. When used with use_custom_template, name of a custom project template. This option is mutually exclusive with ``template_project_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#template_name Project#template_name}
        :param template_project_id: When used with use_custom_template, project ID of a custom project template. This is preferable to using template_name since template_name may be ambiguous (enterprise edition). This option is mutually exclusive with ``template_name``. See ``gitlab_group_project_file_template`` to set a project as a template project. If a project has not been set as a template, using it here will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#template_project_id Project#template_project_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#timeouts Project#timeouts}
        :param topics: The list of topics for the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#topics Project#topics}
        :param use_custom_template: Use either custom instance or group (with group_with_project_templates_id) project template (enterprise edition). ~> When using a custom template, `Group Tokens won't work <https://docs.gitlab.com/15.7/ee/user/project/settings/import_export_troubleshooting/#import-using-the-rest-api-fails-when-using-a-group-access-token>`_. You must use a real user's Personal Access Token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#use_custom_template Project#use_custom_template}
        :param visibility_level: Set to ``public`` to create a public project. Valid values are ``private``, ``internal``, ``public``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#visibility_level Project#visibility_level}
        :param wiki_access_level: Set the wiki access level. Valid values are ``disabled``, ``private``, ``enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#wiki_access_level Project#wiki_access_level}
        :param wiki_enabled: Enable wiki for the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#wiki_enabled Project#wiki_enabled}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(container_expiration_policy, dict):
            container_expiration_policy = ProjectContainerExpirationPolicy(**container_expiration_policy)
        if isinstance(push_rules, dict):
            push_rules = ProjectPushRules(**push_rules)
        if isinstance(timeouts, dict):
            timeouts = ProjectTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bddaf370c13119f237b3d2249ec2a22de82ad4f858153da4a356830c5bd5c5dc)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allow_merge_on_skipped_pipeline", value=allow_merge_on_skipped_pipeline, expected_type=type_hints["allow_merge_on_skipped_pipeline"])
            check_type(argname="argument allow_pipeline_trigger_approve_deployment", value=allow_pipeline_trigger_approve_deployment, expected_type=type_hints["allow_pipeline_trigger_approve_deployment"])
            check_type(argname="argument analytics_access_level", value=analytics_access_level, expected_type=type_hints["analytics_access_level"])
            check_type(argname="argument approvals_before_merge", value=approvals_before_merge, expected_type=type_hints["approvals_before_merge"])
            check_type(argname="argument archived", value=archived, expected_type=type_hints["archived"])
            check_type(argname="argument archive_on_destroy", value=archive_on_destroy, expected_type=type_hints["archive_on_destroy"])
            check_type(argname="argument auto_cancel_pending_pipelines", value=auto_cancel_pending_pipelines, expected_type=type_hints["auto_cancel_pending_pipelines"])
            check_type(argname="argument autoclose_referenced_issues", value=autoclose_referenced_issues, expected_type=type_hints["autoclose_referenced_issues"])
            check_type(argname="argument auto_devops_deploy_strategy", value=auto_devops_deploy_strategy, expected_type=type_hints["auto_devops_deploy_strategy"])
            check_type(argname="argument auto_devops_enabled", value=auto_devops_enabled, expected_type=type_hints["auto_devops_enabled"])
            check_type(argname="argument avatar", value=avatar, expected_type=type_hints["avatar"])
            check_type(argname="argument avatar_hash", value=avatar_hash, expected_type=type_hints["avatar_hash"])
            check_type(argname="argument build_coverage_regex", value=build_coverage_regex, expected_type=type_hints["build_coverage_regex"])
            check_type(argname="argument build_git_strategy", value=build_git_strategy, expected_type=type_hints["build_git_strategy"])
            check_type(argname="argument builds_access_level", value=builds_access_level, expected_type=type_hints["builds_access_level"])
            check_type(argname="argument build_timeout", value=build_timeout, expected_type=type_hints["build_timeout"])
            check_type(argname="argument ci_config_path", value=ci_config_path, expected_type=type_hints["ci_config_path"])
            check_type(argname="argument ci_default_git_depth", value=ci_default_git_depth, expected_type=type_hints["ci_default_git_depth"])
            check_type(argname="argument ci_delete_pipelines_in_seconds", value=ci_delete_pipelines_in_seconds, expected_type=type_hints["ci_delete_pipelines_in_seconds"])
            check_type(argname="argument ci_forward_deployment_enabled", value=ci_forward_deployment_enabled, expected_type=type_hints["ci_forward_deployment_enabled"])
            check_type(argname="argument ci_id_token_sub_claim_components", value=ci_id_token_sub_claim_components, expected_type=type_hints["ci_id_token_sub_claim_components"])
            check_type(argname="argument ci_pipeline_variables_minimum_override_role", value=ci_pipeline_variables_minimum_override_role, expected_type=type_hints["ci_pipeline_variables_minimum_override_role"])
            check_type(argname="argument ci_restrict_pipeline_cancellation_role", value=ci_restrict_pipeline_cancellation_role, expected_type=type_hints["ci_restrict_pipeline_cancellation_role"])
            check_type(argname="argument ci_separated_caches", value=ci_separated_caches, expected_type=type_hints["ci_separated_caches"])
            check_type(argname="argument container_expiration_policy", value=container_expiration_policy, expected_type=type_hints["container_expiration_policy"])
            check_type(argname="argument container_registry_access_level", value=container_registry_access_level, expected_type=type_hints["container_registry_access_level"])
            check_type(argname="argument container_registry_enabled", value=container_registry_enabled, expected_type=type_hints["container_registry_enabled"])
            check_type(argname="argument default_branch", value=default_branch, expected_type=type_hints["default_branch"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument emails_enabled", value=emails_enabled, expected_type=type_hints["emails_enabled"])
            check_type(argname="argument environments_access_level", value=environments_access_level, expected_type=type_hints["environments_access_level"])
            check_type(argname="argument external_authorization_classification_label", value=external_authorization_classification_label, expected_type=type_hints["external_authorization_classification_label"])
            check_type(argname="argument feature_flags_access_level", value=feature_flags_access_level, expected_type=type_hints["feature_flags_access_level"])
            check_type(argname="argument forked_from_project_id", value=forked_from_project_id, expected_type=type_hints["forked_from_project_id"])
            check_type(argname="argument forking_access_level", value=forking_access_level, expected_type=type_hints["forking_access_level"])
            check_type(argname="argument group_runners_enabled", value=group_runners_enabled, expected_type=type_hints["group_runners_enabled"])
            check_type(argname="argument group_with_project_templates_id", value=group_with_project_templates_id, expected_type=type_hints["group_with_project_templates_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument import_url", value=import_url, expected_type=type_hints["import_url"])
            check_type(argname="argument import_url_password", value=import_url_password, expected_type=type_hints["import_url_password"])
            check_type(argname="argument import_url_username", value=import_url_username, expected_type=type_hints["import_url_username"])
            check_type(argname="argument infrastructure_access_level", value=infrastructure_access_level, expected_type=type_hints["infrastructure_access_level"])
            check_type(argname="argument initialize_with_readme", value=initialize_with_readme, expected_type=type_hints["initialize_with_readme"])
            check_type(argname="argument issues_access_level", value=issues_access_level, expected_type=type_hints["issues_access_level"])
            check_type(argname="argument issues_enabled", value=issues_enabled, expected_type=type_hints["issues_enabled"])
            check_type(argname="argument issues_template", value=issues_template, expected_type=type_hints["issues_template"])
            check_type(argname="argument keep_latest_artifact", value=keep_latest_artifact, expected_type=type_hints["keep_latest_artifact"])
            check_type(argname="argument lfs_enabled", value=lfs_enabled, expected_type=type_hints["lfs_enabled"])
            check_type(argname="argument merge_commit_template", value=merge_commit_template, expected_type=type_hints["merge_commit_template"])
            check_type(argname="argument merge_method", value=merge_method, expected_type=type_hints["merge_method"])
            check_type(argname="argument merge_pipelines_enabled", value=merge_pipelines_enabled, expected_type=type_hints["merge_pipelines_enabled"])
            check_type(argname="argument merge_requests_access_level", value=merge_requests_access_level, expected_type=type_hints["merge_requests_access_level"])
            check_type(argname="argument merge_requests_enabled", value=merge_requests_enabled, expected_type=type_hints["merge_requests_enabled"])
            check_type(argname="argument merge_requests_template", value=merge_requests_template, expected_type=type_hints["merge_requests_template"])
            check_type(argname="argument merge_trains_enabled", value=merge_trains_enabled, expected_type=type_hints["merge_trains_enabled"])
            check_type(argname="argument mirror", value=mirror, expected_type=type_hints["mirror"])
            check_type(argname="argument mirror_overwrites_diverged_branches", value=mirror_overwrites_diverged_branches, expected_type=type_hints["mirror_overwrites_diverged_branches"])
            check_type(argname="argument mirror_trigger_builds", value=mirror_trigger_builds, expected_type=type_hints["mirror_trigger_builds"])
            check_type(argname="argument model_experiments_access_level", value=model_experiments_access_level, expected_type=type_hints["model_experiments_access_level"])
            check_type(argname="argument model_registry_access_level", value=model_registry_access_level, expected_type=type_hints["model_registry_access_level"])
            check_type(argname="argument monitor_access_level", value=monitor_access_level, expected_type=type_hints["monitor_access_level"])
            check_type(argname="argument mr_default_target_self", value=mr_default_target_self, expected_type=type_hints["mr_default_target_self"])
            check_type(argname="argument namespace_id", value=namespace_id, expected_type=type_hints["namespace_id"])
            check_type(argname="argument only_allow_merge_if_all_discussions_are_resolved", value=only_allow_merge_if_all_discussions_are_resolved, expected_type=type_hints["only_allow_merge_if_all_discussions_are_resolved"])
            check_type(argname="argument only_allow_merge_if_pipeline_succeeds", value=only_allow_merge_if_pipeline_succeeds, expected_type=type_hints["only_allow_merge_if_pipeline_succeeds"])
            check_type(argname="argument only_mirror_protected_branches", value=only_mirror_protected_branches, expected_type=type_hints["only_mirror_protected_branches"])
            check_type(argname="argument packages_enabled", value=packages_enabled, expected_type=type_hints["packages_enabled"])
            check_type(argname="argument pages_access_level", value=pages_access_level, expected_type=type_hints["pages_access_level"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument permanently_delete_on_destroy", value=permanently_delete_on_destroy, expected_type=type_hints["permanently_delete_on_destroy"])
            check_type(argname="argument pipelines_enabled", value=pipelines_enabled, expected_type=type_hints["pipelines_enabled"])
            check_type(argname="argument pre_receive_secret_detection_enabled", value=pre_receive_secret_detection_enabled, expected_type=type_hints["pre_receive_secret_detection_enabled"])
            check_type(argname="argument prevent_merge_without_jira_issue", value=prevent_merge_without_jira_issue, expected_type=type_hints["prevent_merge_without_jira_issue"])
            check_type(argname="argument printing_merge_request_link_enabled", value=printing_merge_request_link_enabled, expected_type=type_hints["printing_merge_request_link_enabled"])
            check_type(argname="argument public_builds", value=public_builds, expected_type=type_hints["public_builds"])
            check_type(argname="argument public_jobs", value=public_jobs, expected_type=type_hints["public_jobs"])
            check_type(argname="argument push_rules", value=push_rules, expected_type=type_hints["push_rules"])
            check_type(argname="argument releases_access_level", value=releases_access_level, expected_type=type_hints["releases_access_level"])
            check_type(argname="argument remove_source_branch_after_merge", value=remove_source_branch_after_merge, expected_type=type_hints["remove_source_branch_after_merge"])
            check_type(argname="argument repository_access_level", value=repository_access_level, expected_type=type_hints["repository_access_level"])
            check_type(argname="argument repository_storage", value=repository_storage, expected_type=type_hints["repository_storage"])
            check_type(argname="argument request_access_enabled", value=request_access_enabled, expected_type=type_hints["request_access_enabled"])
            check_type(argname="argument requirements_access_level", value=requirements_access_level, expected_type=type_hints["requirements_access_level"])
            check_type(argname="argument resolve_outdated_diff_discussions", value=resolve_outdated_diff_discussions, expected_type=type_hints["resolve_outdated_diff_discussions"])
            check_type(argname="argument restrict_user_defined_variables", value=restrict_user_defined_variables, expected_type=type_hints["restrict_user_defined_variables"])
            check_type(argname="argument security_and_compliance_access_level", value=security_and_compliance_access_level, expected_type=type_hints["security_and_compliance_access_level"])
            check_type(argname="argument shared_runners_enabled", value=shared_runners_enabled, expected_type=type_hints["shared_runners_enabled"])
            check_type(argname="argument skip_wait_for_default_branch_protection", value=skip_wait_for_default_branch_protection, expected_type=type_hints["skip_wait_for_default_branch_protection"])
            check_type(argname="argument snippets_access_level", value=snippets_access_level, expected_type=type_hints["snippets_access_level"])
            check_type(argname="argument snippets_enabled", value=snippets_enabled, expected_type=type_hints["snippets_enabled"])
            check_type(argname="argument squash_commit_template", value=squash_commit_template, expected_type=type_hints["squash_commit_template"])
            check_type(argname="argument squash_option", value=squash_option, expected_type=type_hints["squash_option"])
            check_type(argname="argument suggestion_commit_message", value=suggestion_commit_message, expected_type=type_hints["suggestion_commit_message"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
            check_type(argname="argument template_project_id", value=template_project_id, expected_type=type_hints["template_project_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument topics", value=topics, expected_type=type_hints["topics"])
            check_type(argname="argument use_custom_template", value=use_custom_template, expected_type=type_hints["use_custom_template"])
            check_type(argname="argument visibility_level", value=visibility_level, expected_type=type_hints["visibility_level"])
            check_type(argname="argument wiki_access_level", value=wiki_access_level, expected_type=type_hints["wiki_access_level"])
            check_type(argname="argument wiki_enabled", value=wiki_enabled, expected_type=type_hints["wiki_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if allow_merge_on_skipped_pipeline is not None:
            self._values["allow_merge_on_skipped_pipeline"] = allow_merge_on_skipped_pipeline
        if allow_pipeline_trigger_approve_deployment is not None:
            self._values["allow_pipeline_trigger_approve_deployment"] = allow_pipeline_trigger_approve_deployment
        if analytics_access_level is not None:
            self._values["analytics_access_level"] = analytics_access_level
        if approvals_before_merge is not None:
            self._values["approvals_before_merge"] = approvals_before_merge
        if archived is not None:
            self._values["archived"] = archived
        if archive_on_destroy is not None:
            self._values["archive_on_destroy"] = archive_on_destroy
        if auto_cancel_pending_pipelines is not None:
            self._values["auto_cancel_pending_pipelines"] = auto_cancel_pending_pipelines
        if autoclose_referenced_issues is not None:
            self._values["autoclose_referenced_issues"] = autoclose_referenced_issues
        if auto_devops_deploy_strategy is not None:
            self._values["auto_devops_deploy_strategy"] = auto_devops_deploy_strategy
        if auto_devops_enabled is not None:
            self._values["auto_devops_enabled"] = auto_devops_enabled
        if avatar is not None:
            self._values["avatar"] = avatar
        if avatar_hash is not None:
            self._values["avatar_hash"] = avatar_hash
        if build_coverage_regex is not None:
            self._values["build_coverage_regex"] = build_coverage_regex
        if build_git_strategy is not None:
            self._values["build_git_strategy"] = build_git_strategy
        if builds_access_level is not None:
            self._values["builds_access_level"] = builds_access_level
        if build_timeout is not None:
            self._values["build_timeout"] = build_timeout
        if ci_config_path is not None:
            self._values["ci_config_path"] = ci_config_path
        if ci_default_git_depth is not None:
            self._values["ci_default_git_depth"] = ci_default_git_depth
        if ci_delete_pipelines_in_seconds is not None:
            self._values["ci_delete_pipelines_in_seconds"] = ci_delete_pipelines_in_seconds
        if ci_forward_deployment_enabled is not None:
            self._values["ci_forward_deployment_enabled"] = ci_forward_deployment_enabled
        if ci_id_token_sub_claim_components is not None:
            self._values["ci_id_token_sub_claim_components"] = ci_id_token_sub_claim_components
        if ci_pipeline_variables_minimum_override_role is not None:
            self._values["ci_pipeline_variables_minimum_override_role"] = ci_pipeline_variables_minimum_override_role
        if ci_restrict_pipeline_cancellation_role is not None:
            self._values["ci_restrict_pipeline_cancellation_role"] = ci_restrict_pipeline_cancellation_role
        if ci_separated_caches is not None:
            self._values["ci_separated_caches"] = ci_separated_caches
        if container_expiration_policy is not None:
            self._values["container_expiration_policy"] = container_expiration_policy
        if container_registry_access_level is not None:
            self._values["container_registry_access_level"] = container_registry_access_level
        if container_registry_enabled is not None:
            self._values["container_registry_enabled"] = container_registry_enabled
        if default_branch is not None:
            self._values["default_branch"] = default_branch
        if description is not None:
            self._values["description"] = description
        if emails_enabled is not None:
            self._values["emails_enabled"] = emails_enabled
        if environments_access_level is not None:
            self._values["environments_access_level"] = environments_access_level
        if external_authorization_classification_label is not None:
            self._values["external_authorization_classification_label"] = external_authorization_classification_label
        if feature_flags_access_level is not None:
            self._values["feature_flags_access_level"] = feature_flags_access_level
        if forked_from_project_id is not None:
            self._values["forked_from_project_id"] = forked_from_project_id
        if forking_access_level is not None:
            self._values["forking_access_level"] = forking_access_level
        if group_runners_enabled is not None:
            self._values["group_runners_enabled"] = group_runners_enabled
        if group_with_project_templates_id is not None:
            self._values["group_with_project_templates_id"] = group_with_project_templates_id
        if id is not None:
            self._values["id"] = id
        if import_url is not None:
            self._values["import_url"] = import_url
        if import_url_password is not None:
            self._values["import_url_password"] = import_url_password
        if import_url_username is not None:
            self._values["import_url_username"] = import_url_username
        if infrastructure_access_level is not None:
            self._values["infrastructure_access_level"] = infrastructure_access_level
        if initialize_with_readme is not None:
            self._values["initialize_with_readme"] = initialize_with_readme
        if issues_access_level is not None:
            self._values["issues_access_level"] = issues_access_level
        if issues_enabled is not None:
            self._values["issues_enabled"] = issues_enabled
        if issues_template is not None:
            self._values["issues_template"] = issues_template
        if keep_latest_artifact is not None:
            self._values["keep_latest_artifact"] = keep_latest_artifact
        if lfs_enabled is not None:
            self._values["lfs_enabled"] = lfs_enabled
        if merge_commit_template is not None:
            self._values["merge_commit_template"] = merge_commit_template
        if merge_method is not None:
            self._values["merge_method"] = merge_method
        if merge_pipelines_enabled is not None:
            self._values["merge_pipelines_enabled"] = merge_pipelines_enabled
        if merge_requests_access_level is not None:
            self._values["merge_requests_access_level"] = merge_requests_access_level
        if merge_requests_enabled is not None:
            self._values["merge_requests_enabled"] = merge_requests_enabled
        if merge_requests_template is not None:
            self._values["merge_requests_template"] = merge_requests_template
        if merge_trains_enabled is not None:
            self._values["merge_trains_enabled"] = merge_trains_enabled
        if mirror is not None:
            self._values["mirror"] = mirror
        if mirror_overwrites_diverged_branches is not None:
            self._values["mirror_overwrites_diverged_branches"] = mirror_overwrites_diverged_branches
        if mirror_trigger_builds is not None:
            self._values["mirror_trigger_builds"] = mirror_trigger_builds
        if model_experiments_access_level is not None:
            self._values["model_experiments_access_level"] = model_experiments_access_level
        if model_registry_access_level is not None:
            self._values["model_registry_access_level"] = model_registry_access_level
        if monitor_access_level is not None:
            self._values["monitor_access_level"] = monitor_access_level
        if mr_default_target_self is not None:
            self._values["mr_default_target_self"] = mr_default_target_self
        if namespace_id is not None:
            self._values["namespace_id"] = namespace_id
        if only_allow_merge_if_all_discussions_are_resolved is not None:
            self._values["only_allow_merge_if_all_discussions_are_resolved"] = only_allow_merge_if_all_discussions_are_resolved
        if only_allow_merge_if_pipeline_succeeds is not None:
            self._values["only_allow_merge_if_pipeline_succeeds"] = only_allow_merge_if_pipeline_succeeds
        if only_mirror_protected_branches is not None:
            self._values["only_mirror_protected_branches"] = only_mirror_protected_branches
        if packages_enabled is not None:
            self._values["packages_enabled"] = packages_enabled
        if pages_access_level is not None:
            self._values["pages_access_level"] = pages_access_level
        if path is not None:
            self._values["path"] = path
        if permanently_delete_on_destroy is not None:
            self._values["permanently_delete_on_destroy"] = permanently_delete_on_destroy
        if pipelines_enabled is not None:
            self._values["pipelines_enabled"] = pipelines_enabled
        if pre_receive_secret_detection_enabled is not None:
            self._values["pre_receive_secret_detection_enabled"] = pre_receive_secret_detection_enabled
        if prevent_merge_without_jira_issue is not None:
            self._values["prevent_merge_without_jira_issue"] = prevent_merge_without_jira_issue
        if printing_merge_request_link_enabled is not None:
            self._values["printing_merge_request_link_enabled"] = printing_merge_request_link_enabled
        if public_builds is not None:
            self._values["public_builds"] = public_builds
        if public_jobs is not None:
            self._values["public_jobs"] = public_jobs
        if push_rules is not None:
            self._values["push_rules"] = push_rules
        if releases_access_level is not None:
            self._values["releases_access_level"] = releases_access_level
        if remove_source_branch_after_merge is not None:
            self._values["remove_source_branch_after_merge"] = remove_source_branch_after_merge
        if repository_access_level is not None:
            self._values["repository_access_level"] = repository_access_level
        if repository_storage is not None:
            self._values["repository_storage"] = repository_storage
        if request_access_enabled is not None:
            self._values["request_access_enabled"] = request_access_enabled
        if requirements_access_level is not None:
            self._values["requirements_access_level"] = requirements_access_level
        if resolve_outdated_diff_discussions is not None:
            self._values["resolve_outdated_diff_discussions"] = resolve_outdated_diff_discussions
        if restrict_user_defined_variables is not None:
            self._values["restrict_user_defined_variables"] = restrict_user_defined_variables
        if security_and_compliance_access_level is not None:
            self._values["security_and_compliance_access_level"] = security_and_compliance_access_level
        if shared_runners_enabled is not None:
            self._values["shared_runners_enabled"] = shared_runners_enabled
        if skip_wait_for_default_branch_protection is not None:
            self._values["skip_wait_for_default_branch_protection"] = skip_wait_for_default_branch_protection
        if snippets_access_level is not None:
            self._values["snippets_access_level"] = snippets_access_level
        if snippets_enabled is not None:
            self._values["snippets_enabled"] = snippets_enabled
        if squash_commit_template is not None:
            self._values["squash_commit_template"] = squash_commit_template
        if squash_option is not None:
            self._values["squash_option"] = squash_option
        if suggestion_commit_message is not None:
            self._values["suggestion_commit_message"] = suggestion_commit_message
        if tags is not None:
            self._values["tags"] = tags
        if template_name is not None:
            self._values["template_name"] = template_name
        if template_project_id is not None:
            self._values["template_project_id"] = template_project_id
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if topics is not None:
            self._values["topics"] = topics
        if use_custom_template is not None:
            self._values["use_custom_template"] = use_custom_template
        if visibility_level is not None:
            self._values["visibility_level"] = visibility_level
        if wiki_access_level is not None:
            self._values["wiki_access_level"] = wiki_access_level
        if wiki_enabled is not None:
            self._values["wiki_enabled"] = wiki_enabled

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
        '''The name of the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#name Project#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_merge_on_skipped_pipeline(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true if you want to treat skipped pipelines as if they finished with success.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#allow_merge_on_skipped_pipeline Project#allow_merge_on_skipped_pipeline}
        '''
        result = self._values.get("allow_merge_on_skipped_pipeline")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_pipeline_trigger_approve_deployment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set whether or not a pipeline triggerer is allowed to approve deployments. Premium and Ultimate only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#allow_pipeline_trigger_approve_deployment Project#allow_pipeline_trigger_approve_deployment}
        '''
        result = self._values.get("allow_pipeline_trigger_approve_deployment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def analytics_access_level(self) -> typing.Optional[builtins.str]:
        '''Set the analytics access level. Valid values are ``disabled``, ``private``, ``enabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#analytics_access_level Project#analytics_access_level}
        '''
        result = self._values.get("analytics_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def approvals_before_merge(self) -> typing.Optional[jsii.Number]:
        '''Number of merge request approvals required for merging.

        Default is 0.
        This field **does not** work well in combination with the ``gitlab_project_approval_rule`` resource
        and is most likely gonna be deprecated in a future GitLab version (see `this upstream epic <https://gitlab.com/groups/gitlab-org/-/epics/7572>`_).
        In the meantime we recommend against using this attribute and use ``gitlab_project_approval_rule`` instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#approvals_before_merge Project#approvals_before_merge}
        '''
        result = self._values.get("approvals_before_merge")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def archived(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the project is in read-only mode (archived). Repositories can be archived/unarchived by toggling this parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#archived Project#archived}
        '''
        result = self._values.get("archived")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def archive_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to ``true`` to archive the project instead of deleting on destroy.

        If set to ``true`` it will entire omit the ``DELETE`` operation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#archive_on_destroy Project#archive_on_destroy}
        '''
        result = self._values.get("archive_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auto_cancel_pending_pipelines(self) -> typing.Optional[builtins.str]:
        '''Auto-cancel pending pipelines. This isn’t a boolean, but enabled/disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#auto_cancel_pending_pipelines Project#auto_cancel_pending_pipelines}
        '''
        result = self._values.get("auto_cancel_pending_pipelines")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def autoclose_referenced_issues(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set whether auto-closing referenced issues on default branch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#autoclose_referenced_issues Project#autoclose_referenced_issues}
        '''
        result = self._values.get("autoclose_referenced_issues")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auto_devops_deploy_strategy(self) -> typing.Optional[builtins.str]:
        '''Auto Deploy strategy. Valid values are ``continuous``, ``manual``, ``timed_incremental``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#auto_devops_deploy_strategy Project#auto_devops_deploy_strategy}
        '''
        result = self._values.get("auto_devops_deploy_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_devops_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable Auto DevOps for this project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#auto_devops_enabled Project#auto_devops_enabled}
        '''
        result = self._values.get("auto_devops_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def avatar(self) -> typing.Optional[builtins.str]:
        '''A local path to the avatar image to upload. **Note**: not available for imported resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#avatar Project#avatar}
        '''
        result = self._values.get("avatar")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def avatar_hash(self) -> typing.Optional[builtins.str]:
        '''The hash of the avatar image.

        Use ``filesha256("path/to/avatar.png")`` whenever possible. **Note**: this is used to trigger an update of the avatar. If it's not given, but an avatar is given, the avatar will be updated each time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#avatar_hash Project#avatar_hash}
        '''
        result = self._values.get("avatar_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_coverage_regex(self) -> typing.Optional[builtins.str]:
        '''Test coverage parsing for the project. This is deprecated feature in GitLab 15.0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#build_coverage_regex Project#build_coverage_regex}
        '''
        result = self._values.get("build_coverage_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_git_strategy(self) -> typing.Optional[builtins.str]:
        '''The Git strategy. Defaults to fetch. Valid values are ``clone``, ``fetch``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#build_git_strategy Project#build_git_strategy}
        '''
        result = self._values.get("build_git_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def builds_access_level(self) -> typing.Optional[builtins.str]:
        '''Set the builds access level. Valid values are ``disabled``, ``private``, ``enabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#builds_access_level Project#builds_access_level}
        '''
        result = self._values.get("builds_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_timeout(self) -> typing.Optional[jsii.Number]:
        '''The maximum amount of time, in seconds, that a job can run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#build_timeout Project#build_timeout}
        '''
        result = self._values.get("build_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ci_config_path(self) -> typing.Optional[builtins.str]:
        '''Custom Path to CI config file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_config_path Project#ci_config_path}
        '''
        result = self._values.get("ci_config_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ci_default_git_depth(self) -> typing.Optional[jsii.Number]:
        '''Default number of revisions for shallow cloning.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_default_git_depth Project#ci_default_git_depth}
        '''
        result = self._values.get("ci_default_git_depth")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ci_delete_pipelines_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Pipelines older than the configured time are deleted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_delete_pipelines_in_seconds Project#ci_delete_pipelines_in_seconds}
        '''
        result = self._values.get("ci_delete_pipelines_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ci_forward_deployment_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When a new deployment job starts, skip older deployment jobs that are still pending.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_forward_deployment_enabled Project#ci_forward_deployment_enabled}
        '''
        result = self._values.get("ci_forward_deployment_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ci_id_token_sub_claim_components(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Fields included in the sub claim of the ID Token.

        Accepts an array starting with project_path. The array might also include ref_type and ref. Defaults to ["project_path", "ref_type", "ref"]. Introduced in GitLab 17.10.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_id_token_sub_claim_components Project#ci_id_token_sub_claim_components}
        '''
        result = self._values.get("ci_id_token_sub_claim_components")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ci_pipeline_variables_minimum_override_role(
        self,
    ) -> typing.Optional[builtins.str]:
        '''The minimum role required to set variables when running pipelines and jobs.

        Introduced in GitLab 17.1. Valid values are ``developer``, ``maintainer``, ``owner``, ``no_one_allowed``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_pipeline_variables_minimum_override_role Project#ci_pipeline_variables_minimum_override_role}
        '''
        result = self._values.get("ci_pipeline_variables_minimum_override_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ci_restrict_pipeline_cancellation_role(self) -> typing.Optional[builtins.str]:
        '''The role required to cancel a pipeline or job.

        Premium and Ultimate only. Valid values are ``developer``, ``maintainer``, ``no one``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_restrict_pipeline_cancellation_role Project#ci_restrict_pipeline_cancellation_role}
        '''
        result = self._values.get("ci_restrict_pipeline_cancellation_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ci_separated_caches(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use separate caches for protected branches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#ci_separated_caches Project#ci_separated_caches}
        '''
        result = self._values.get("ci_separated_caches")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def container_expiration_policy(
        self,
    ) -> typing.Optional["ProjectContainerExpirationPolicy"]:
        '''container_expiration_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#container_expiration_policy Project#container_expiration_policy}
        '''
        result = self._values.get("container_expiration_policy")
        return typing.cast(typing.Optional["ProjectContainerExpirationPolicy"], result)

    @builtins.property
    def container_registry_access_level(self) -> typing.Optional[builtins.str]:
        '''Set visibility of container registry, for this project. Valid values are ``disabled``, ``private``, ``enabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#container_registry_access_level Project#container_registry_access_level}
        '''
        result = self._values.get("container_registry_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_registry_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable container registry for the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#container_registry_enabled Project#container_registry_enabled}
        '''
        result = self._values.get("container_registry_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def default_branch(self) -> typing.Optional[builtins.str]:
        '''The default branch for the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#default_branch Project#default_branch}
        '''
        result = self._values.get("default_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#description Project#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def emails_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable email notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#emails_enabled Project#emails_enabled}
        '''
        result = self._values.get("emails_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def environments_access_level(self) -> typing.Optional[builtins.str]:
        '''Set the environments access level. Valid values are ``disabled``, ``private``, ``enabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#environments_access_level Project#environments_access_level}
        '''
        result = self._values.get("environments_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_authorization_classification_label(
        self,
    ) -> typing.Optional[builtins.str]:
        '''The classification label for the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#external_authorization_classification_label Project#external_authorization_classification_label}
        '''
        result = self._values.get("external_authorization_classification_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def feature_flags_access_level(self) -> typing.Optional[builtins.str]:
        '''Set the feature flags access level. Valid values are ``disabled``, ``private``, ``enabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#feature_flags_access_level Project#feature_flags_access_level}
        '''
        result = self._values.get("feature_flags_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forked_from_project_id(self) -> typing.Optional[jsii.Number]:
        '''The id of the project to fork.

        During create the project is forked and during an update the fork relation is changed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#forked_from_project_id Project#forked_from_project_id}
        '''
        result = self._values.get("forked_from_project_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def forking_access_level(self) -> typing.Optional[builtins.str]:
        '''Set the forking access level. Valid values are ``disabled``, ``private``, ``enabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#forking_access_level Project#forking_access_level}
        '''
        result = self._values.get("forking_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_runners_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable group runners for this project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#group_runners_enabled Project#group_runners_enabled}
        '''
        result = self._values.get("group_runners_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def group_with_project_templates_id(self) -> typing.Optional[jsii.Number]:
        '''For group-level custom templates, specifies ID of group from which all the custom project templates are sourced.

        Leave empty for instance-level templates. Requires use_custom_template to be true (enterprise edition).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#group_with_project_templates_id Project#group_with_project_templates_id}
        '''
        result = self._values.get("group_with_project_templates_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#id Project#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def import_url(self) -> typing.Optional[builtins.str]:
        '''Git URL to a repository to be imported.

        Together with ``mirror = true`` it will setup a Pull Mirror. This can also be used together with ``forked_from_project_id`` to setup a Pull Mirror for a fork. The fork takes precedence over the import. Make sure to provide the credentials in ``import_url_username`` and ``import_url_password``. GitLab never returns the credentials, thus the provider cannot detect configuration drift in the credentials. They can also not be imported using ``terraform import``. See the examples section for how to properly use it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#import_url Project#import_url}
        '''
        result = self._values.get("import_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def import_url_password(self) -> typing.Optional[builtins.str]:
        '''The password for the ``import_url``.

        The value of this field is used to construct a valid ``import_url`` and is only related to the provider. This field cannot be imported using ``terraform import``. See the examples section for how to properly use it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#import_url_password Project#import_url_password}
        '''
        result = self._values.get("import_url_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def import_url_username(self) -> typing.Optional[builtins.str]:
        '''The username for the ``import_url``.

        The value of this field is used to construct a valid ``import_url`` and is only related to the provider. This field cannot be imported using ``terraform import``.  See the examples section for how to properly use it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#import_url_username Project#import_url_username}
        '''
        result = self._values.get("import_url_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def infrastructure_access_level(self) -> typing.Optional[builtins.str]:
        '''Set the infrastructure access level. Valid values are ``disabled``, ``private``, ``enabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#infrastructure_access_level Project#infrastructure_access_level}
        '''
        result = self._values.get("infrastructure_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initialize_with_readme(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Create main branch with first commit containing a README.md file. Must be set to ``true`` if importing an uninitialized project with a different ``default_branch``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#initialize_with_readme Project#initialize_with_readme}
        '''
        result = self._values.get("initialize_with_readme")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def issues_access_level(self) -> typing.Optional[builtins.str]:
        '''Set the issues access level. Valid values are ``disabled``, ``private``, ``enabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#issues_access_level Project#issues_access_level}
        '''
        result = self._values.get("issues_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issues_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable issue tracking for the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#issues_enabled Project#issues_enabled}
        '''
        result = self._values.get("issues_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def issues_template(self) -> typing.Optional[builtins.str]:
        '''Sets the template for new issues in the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#issues_template Project#issues_template}
        '''
        result = self._values.get("issues_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keep_latest_artifact(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable or enable the ability to keep the latest artifact for this project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#keep_latest_artifact Project#keep_latest_artifact}
        '''
        result = self._values.get("keep_latest_artifact")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def lfs_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable LFS for the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#lfs_enabled Project#lfs_enabled}
        '''
        result = self._values.get("lfs_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def merge_commit_template(self) -> typing.Optional[builtins.str]:
        '''Template used to create merge commit message in merge requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#merge_commit_template Project#merge_commit_template}
        '''
        result = self._values.get("merge_commit_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def merge_method(self) -> typing.Optional[builtins.str]:
        '''Set the merge method. Valid values are ``merge``, ``rebase_merge``, ``ff``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#merge_method Project#merge_method}
        '''
        result = self._values.get("merge_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def merge_pipelines_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable or disable merge pipelines.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#merge_pipelines_enabled Project#merge_pipelines_enabled}
        '''
        result = self._values.get("merge_pipelines_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def merge_requests_access_level(self) -> typing.Optional[builtins.str]:
        '''Set the merge requests access level. Valid values are ``disabled``, ``private``, ``enabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#merge_requests_access_level Project#merge_requests_access_level}
        '''
        result = self._values.get("merge_requests_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def merge_requests_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable merge requests for the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#merge_requests_enabled Project#merge_requests_enabled}
        '''
        result = self._values.get("merge_requests_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def merge_requests_template(self) -> typing.Optional[builtins.str]:
        '''Sets the template for new merge requests in the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#merge_requests_template Project#merge_requests_template}
        '''
        result = self._values.get("merge_requests_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def merge_trains_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable or disable merge trains. Requires ``merge_pipelines_enabled`` to be set to ``true`` to take effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#merge_trains_enabled Project#merge_trains_enabled}
        '''
        result = self._values.get("merge_trains_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def mirror(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable project pull mirror.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#mirror Project#mirror}
        '''
        result = self._values.get("mirror")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def mirror_overwrites_diverged_branches(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable overwrite diverged branches for a mirrored project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#mirror_overwrites_diverged_branches Project#mirror_overwrites_diverged_branches}
        '''
        result = self._values.get("mirror_overwrites_diverged_branches")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def mirror_trigger_builds(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable trigger builds on pushes for a mirrored project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#mirror_trigger_builds Project#mirror_trigger_builds}
        '''
        result = self._values.get("mirror_trigger_builds")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def model_experiments_access_level(self) -> typing.Optional[builtins.str]:
        '''Set visibility of machine learning model experiments. Valid values are ``disabled``, ``private``, ``enabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#model_experiments_access_level Project#model_experiments_access_level}
        '''
        result = self._values.get("model_experiments_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model_registry_access_level(self) -> typing.Optional[builtins.str]:
        '''Set visibility of machine learning model registry. Valid values are ``disabled``, ``private``, ``enabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#model_registry_access_level Project#model_registry_access_level}
        '''
        result = self._values.get("model_registry_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitor_access_level(self) -> typing.Optional[builtins.str]:
        '''Set the monitor access level. Valid values are ``disabled``, ``private``, ``enabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#monitor_access_level Project#monitor_access_level}
        '''
        result = self._values.get("monitor_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mr_default_target_self(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''For forked projects, target merge requests to this project. If false, the target will be the upstream project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#mr_default_target_self Project#mr_default_target_self}
        '''
        result = self._values.get("mr_default_target_self")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def namespace_id(self) -> typing.Optional[jsii.Number]:
        '''The namespace (group or user) of the project. Defaults to your user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#namespace_id Project#namespace_id}
        '''
        result = self._values.get("namespace_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def only_allow_merge_if_all_discussions_are_resolved(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true if you want allow merges only if all discussions are resolved.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#only_allow_merge_if_all_discussions_are_resolved Project#only_allow_merge_if_all_discussions_are_resolved}
        '''
        result = self._values.get("only_allow_merge_if_all_discussions_are_resolved")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def only_allow_merge_if_pipeline_succeeds(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true if you want allow merges only if a pipeline succeeds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#only_allow_merge_if_pipeline_succeeds Project#only_allow_merge_if_pipeline_succeeds}
        '''
        result = self._values.get("only_allow_merge_if_pipeline_succeeds")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def only_mirror_protected_branches(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable only mirror protected branches for a mirrored project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#only_mirror_protected_branches Project#only_mirror_protected_branches}
        '''
        result = self._values.get("only_mirror_protected_branches")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def packages_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable packages repository for the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#packages_enabled Project#packages_enabled}
        '''
        result = self._values.get("packages_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def pages_access_level(self) -> typing.Optional[builtins.str]:
        '''Enable pages access control. Valid values are ``public``, ``private``, ``enabled``, ``disabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#pages_access_level Project#pages_access_level}
        '''
        result = self._values.get("pages_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#path Project#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permanently_delete_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to ``true`` to immediately permanently delete the project instead of scheduling a delete for Premium and Ultimate tiers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#permanently_delete_on_destroy Project#permanently_delete_on_destroy}
        '''
        result = self._values.get("permanently_delete_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def pipelines_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable pipelines for the project. The ``pipelines_enabled`` field is being sent as ``jobs_enabled`` in the GitLab API calls.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#pipelines_enabled Project#pipelines_enabled}
        '''
        result = self._values.get("pipelines_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def pre_receive_secret_detection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Secret Push Detection is enabled. Requires GitLab Ultimate and at least GitLab 17.3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#pre_receive_secret_detection_enabled Project#pre_receive_secret_detection_enabled}
        '''
        result = self._values.get("pre_receive_secret_detection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prevent_merge_without_jira_issue(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set whether merge requests require an associated issue from Jira. Premium and Ultimate only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#prevent_merge_without_jira_issue Project#prevent_merge_without_jira_issue}
        '''
        result = self._values.get("prevent_merge_without_jira_issue")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def printing_merge_request_link_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Show link to create/view merge request when pushing from the command line.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#printing_merge_request_link_enabled Project#printing_merge_request_link_enabled}
        '''
        result = self._values.get("printing_merge_request_link_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def public_builds(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, jobs can be viewed by non-project members.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#public_builds Project#public_builds}
        '''
        result = self._values.get("public_builds")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def public_jobs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, jobs can be viewed by non-project members.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#public_jobs Project#public_jobs}
        '''
        result = self._values.get("public_jobs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def push_rules(self) -> typing.Optional["ProjectPushRules"]:
        '''push_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#push_rules Project#push_rules}
        '''
        result = self._values.get("push_rules")
        return typing.cast(typing.Optional["ProjectPushRules"], result)

    @builtins.property
    def releases_access_level(self) -> typing.Optional[builtins.str]:
        '''Set the releases access level. Valid values are ``disabled``, ``private``, ``enabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#releases_access_level Project#releases_access_level}
        '''
        result = self._values.get("releases_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remove_source_branch_after_merge(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable ``Delete source branch`` option by default for all new merge requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#remove_source_branch_after_merge Project#remove_source_branch_after_merge}
        '''
        result = self._values.get("remove_source_branch_after_merge")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def repository_access_level(self) -> typing.Optional[builtins.str]:
        '''Set the repository access level. Valid values are ``disabled``, ``private``, ``enabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#repository_access_level Project#repository_access_level}
        '''
        result = self._values.get("repository_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_storage(self) -> typing.Optional[builtins.str]:
        '''Which storage shard the repository is on. (administrator only).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#repository_storage Project#repository_storage}
        '''
        result = self._values.get("repository_storage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow users to request member access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#request_access_enabled Project#request_access_enabled}
        '''
        result = self._values.get("request_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def requirements_access_level(self) -> typing.Optional[builtins.str]:
        '''Set the requirements access level. Valid values are ``disabled``, ``private``, ``enabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#requirements_access_level Project#requirements_access_level}
        '''
        result = self._values.get("requirements_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resolve_outdated_diff_discussions(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Automatically resolve merge request diffs discussions on lines changed with a push.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#resolve_outdated_diff_discussions Project#resolve_outdated_diff_discussions}
        '''
        result = self._values.get("resolve_outdated_diff_discussions")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def restrict_user_defined_variables(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow only users with the Maintainer role to pass user-defined variables when triggering a pipeline.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#restrict_user_defined_variables Project#restrict_user_defined_variables}
        '''
        result = self._values.get("restrict_user_defined_variables")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def security_and_compliance_access_level(self) -> typing.Optional[builtins.str]:
        '''Set the security and compliance access level. Valid values are ``disabled``, ``private``, ``enabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#security_and_compliance_access_level Project#security_and_compliance_access_level}
        '''
        result = self._values.get("security_and_compliance_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shared_runners_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable shared runners for this project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#shared_runners_enabled Project#shared_runners_enabled}
        '''
        result = self._values.get("shared_runners_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def skip_wait_for_default_branch_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If ``true``, the default behavior to wait for the default branch protection to be created is skipped.

        This is necessary if the current user is not an admin and the default branch protection is disabled on an instance-level.
        There is currently no known way to determine if the default branch protection is disabled on an instance-level for non-admin users.
        This attribute is only used during resource creation, thus changes are suppressed and the attribute cannot be imported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#skip_wait_for_default_branch_protection Project#skip_wait_for_default_branch_protection}
        '''
        result = self._values.get("skip_wait_for_default_branch_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def snippets_access_level(self) -> typing.Optional[builtins.str]:
        '''Set the snippets access level. Valid values are ``disabled``, ``private``, ``enabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#snippets_access_level Project#snippets_access_level}
        '''
        result = self._values.get("snippets_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snippets_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable snippets for the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#snippets_enabled Project#snippets_enabled}
        '''
        result = self._values.get("snippets_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def squash_commit_template(self) -> typing.Optional[builtins.str]:
        '''Template used to create squash commit message in merge requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#squash_commit_template Project#squash_commit_template}
        '''
        result = self._values.get("squash_commit_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def squash_option(self) -> typing.Optional[builtins.str]:
        '''Squash commits when merge request is merged.

        Valid values are ``never`` (Do not allow), ``always`` (Require), ``default_on`` (Encourage), or ``default_off`` (Allow). The default value is ``default_off`` (Allow).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#squash_option Project#squash_option}
        '''
        result = self._values.get("squash_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suggestion_commit_message(self) -> typing.Optional[builtins.str]:
        '''The commit message used to apply merge request suggestions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#suggestion_commit_message Project#suggestion_commit_message}
        '''
        result = self._values.get("suggestion_commit_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of tags for a project;

        put array of tags, that should be finally assigned to a project. Use topics instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#tags Project#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def template_name(self) -> typing.Optional[builtins.str]:
        '''When used without use_custom_template, name of a built-in project template.

        When used with use_custom_template, name of a custom project template. This option is mutually exclusive with ``template_project_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#template_name Project#template_name}
        '''
        result = self._values.get("template_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_project_id(self) -> typing.Optional[jsii.Number]:
        '''When used with use_custom_template, project ID of a custom project template.

        This is preferable to using template_name since template_name may be ambiguous (enterprise edition). This option is mutually exclusive with ``template_name``. See ``gitlab_group_project_file_template`` to set a project as a template project. If a project has not been set as a template, using it here will result in an error.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#template_project_id Project#template_project_id}
        '''
        result = self._values.get("template_project_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ProjectTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#timeouts Project#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ProjectTimeouts"], result)

    @builtins.property
    def topics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of topics for the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#topics Project#topics}
        '''
        result = self._values.get("topics")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def use_custom_template(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use either custom instance or group (with group_with_project_templates_id) project template (enterprise edition).

        ~> When using a custom template, `Group Tokens won't work <https://docs.gitlab.com/15.7/ee/user/project/settings/import_export_troubleshooting/#import-using-the-rest-api-fails-when-using-a-group-access-token>`_. You must use a real user's Personal Access Token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#use_custom_template Project#use_custom_template}
        '''
        result = self._values.get("use_custom_template")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def visibility_level(self) -> typing.Optional[builtins.str]:
        '''Set to ``public`` to create a public project. Valid values are ``private``, ``internal``, ``public``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#visibility_level Project#visibility_level}
        '''
        result = self._values.get("visibility_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wiki_access_level(self) -> typing.Optional[builtins.str]:
        '''Set the wiki access level. Valid values are ``disabled``, ``private``, ``enabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#wiki_access_level Project#wiki_access_level}
        '''
        result = self._values.get("wiki_access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wiki_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable wiki for the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#wiki_enabled Project#wiki_enabled}
        '''
        result = self._values.get("wiki_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.project.ProjectContainerExpirationPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "cadence": "cadence",
        "enabled": "enabled",
        "keep_n": "keepN",
        "name_regex": "nameRegex",
        "name_regex_delete": "nameRegexDelete",
        "name_regex_keep": "nameRegexKeep",
        "older_than": "olderThan",
    },
)
class ProjectContainerExpirationPolicy:
    def __init__(
        self,
        *,
        cadence: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        keep_n: typing.Optional[jsii.Number] = None,
        name_regex: typing.Optional[builtins.str] = None,
        name_regex_delete: typing.Optional[builtins.str] = None,
        name_regex_keep: typing.Optional[builtins.str] = None,
        older_than: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cadence: The cadence of the policy. Valid values are: ``1d``, ``7d``, ``14d``, ``1month``, ``3month``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#cadence Project#cadence}
        :param enabled: If true, the policy is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#enabled Project#enabled}
        :param keep_n: The number of images to keep. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#keep_n Project#keep_n}
        :param name_regex: The regular expression to match image names to delete. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#name_regex Project#name_regex}
        :param name_regex_delete: The regular expression to match image names to delete. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#name_regex_delete Project#name_regex_delete}
        :param name_regex_keep: The regular expression to match image names to keep. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#name_regex_keep Project#name_regex_keep}
        :param older_than: The number of days to keep images. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#older_than Project#older_than}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c134465d2f19253cf8263d41a482769fcea91f99876deed9c1639157c39cbbdd)
            check_type(argname="argument cadence", value=cadence, expected_type=type_hints["cadence"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument keep_n", value=keep_n, expected_type=type_hints["keep_n"])
            check_type(argname="argument name_regex", value=name_regex, expected_type=type_hints["name_regex"])
            check_type(argname="argument name_regex_delete", value=name_regex_delete, expected_type=type_hints["name_regex_delete"])
            check_type(argname="argument name_regex_keep", value=name_regex_keep, expected_type=type_hints["name_regex_keep"])
            check_type(argname="argument older_than", value=older_than, expected_type=type_hints["older_than"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cadence is not None:
            self._values["cadence"] = cadence
        if enabled is not None:
            self._values["enabled"] = enabled
        if keep_n is not None:
            self._values["keep_n"] = keep_n
        if name_regex is not None:
            self._values["name_regex"] = name_regex
        if name_regex_delete is not None:
            self._values["name_regex_delete"] = name_regex_delete
        if name_regex_keep is not None:
            self._values["name_regex_keep"] = name_regex_keep
        if older_than is not None:
            self._values["older_than"] = older_than

    @builtins.property
    def cadence(self) -> typing.Optional[builtins.str]:
        '''The cadence of the policy. Valid values are: ``1d``, ``7d``, ``14d``, ``1month``, ``3month``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#cadence Project#cadence}
        '''
        result = self._values.get("cadence")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the policy is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#enabled Project#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def keep_n(self) -> typing.Optional[jsii.Number]:
        '''The number of images to keep.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#keep_n Project#keep_n}
        '''
        result = self._values.get("keep_n")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name_regex(self) -> typing.Optional[builtins.str]:
        '''The regular expression to match image names to delete.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#name_regex Project#name_regex}
        '''
        result = self._values.get("name_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_regex_delete(self) -> typing.Optional[builtins.str]:
        '''The regular expression to match image names to delete.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#name_regex_delete Project#name_regex_delete}
        '''
        result = self._values.get("name_regex_delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_regex_keep(self) -> typing.Optional[builtins.str]:
        '''The regular expression to match image names to keep.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#name_regex_keep Project#name_regex_keep}
        '''
        result = self._values.get("name_regex_keep")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def older_than(self) -> typing.Optional[builtins.str]:
        '''The number of days to keep images.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#older_than Project#older_than}
        '''
        result = self._values.get("older_than")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectContainerExpirationPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectContainerExpirationPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.project.ProjectContainerExpirationPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0de4753bbf69e900422fb46e2ca806925eecd4882b541522d14dd4fcc827b3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCadence")
    def reset_cadence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCadence", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetKeepN")
    def reset_keep_n(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepN", []))

    @jsii.member(jsii_name="resetNameRegex")
    def reset_name_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNameRegex", []))

    @jsii.member(jsii_name="resetNameRegexDelete")
    def reset_name_regex_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNameRegexDelete", []))

    @jsii.member(jsii_name="resetNameRegexKeep")
    def reset_name_regex_keep(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNameRegexKeep", []))

    @jsii.member(jsii_name="resetOlderThan")
    def reset_older_than(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOlderThan", []))

    @builtins.property
    @jsii.member(jsii_name="nextRunAt")
    def next_run_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextRunAt"))

    @builtins.property
    @jsii.member(jsii_name="cadenceInput")
    def cadence_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cadenceInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="keepNInput")
    def keep_n_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keepNInput"))

    @builtins.property
    @jsii.member(jsii_name="nameRegexDeleteInput")
    def name_regex_delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameRegexDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="nameRegexInput")
    def name_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="nameRegexKeepInput")
    def name_regex_keep_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameRegexKeepInput"))

    @builtins.property
    @jsii.member(jsii_name="olderThanInput")
    def older_than_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "olderThanInput"))

    @builtins.property
    @jsii.member(jsii_name="cadence")
    def cadence(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cadence"))

    @cadence.setter
    def cadence(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__481878a2b02a6662df25d3b20a64635a2f2996628641b1ba47965dfa8eac20fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cadence", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eeeae9492fec5d77433118546c0fbd53fd5510ae46535a048602e9bd145bc79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keepN")
    def keep_n(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keepN"))

    @keep_n.setter
    def keep_n(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ee71d8112b55ce54a9f60cf5d3a2811eec1c96420284addacd145f1aba1d2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepN", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nameRegex")
    def name_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameRegex"))

    @name_regex.setter
    def name_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__032cee01373b66e9067d9cf031ccb876465cfb43f3a1d9123554d35aeeedc85a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nameRegexDelete")
    def name_regex_delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameRegexDelete"))

    @name_regex_delete.setter
    def name_regex_delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef59396557624da8549c22f3e310b7cb7eabc33fcdbc1617552cbbfd3e319950)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameRegexDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nameRegexKeep")
    def name_regex_keep(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameRegexKeep"))

    @name_regex_keep.setter
    def name_regex_keep(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d20de45d369a47cd0b6868d4779724f55228763fa72acb44c6d3058407eee36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameRegexKeep", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="olderThan")
    def older_than(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "olderThan"))

    @older_than.setter
    def older_than(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0419624816ae54d9371de7800af0c3155b7cb06e62659892a050e5663d855c42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "olderThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ProjectContainerExpirationPolicy]:
        return typing.cast(typing.Optional[ProjectContainerExpirationPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ProjectContainerExpirationPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__505a8dea72c5e5c15331ac448ccf11ffac738d81bcce98f9f43fedbadb33849c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.project.ProjectPushRules",
    jsii_struct_bases=[],
    name_mapping={
        "author_email_regex": "authorEmailRegex",
        "branch_name_regex": "branchNameRegex",
        "commit_committer_check": "commitCommitterCheck",
        "commit_committer_name_check": "commitCommitterNameCheck",
        "commit_message_negative_regex": "commitMessageNegativeRegex",
        "commit_message_regex": "commitMessageRegex",
        "deny_delete_tag": "denyDeleteTag",
        "file_name_regex": "fileNameRegex",
        "max_file_size": "maxFileSize",
        "member_check": "memberCheck",
        "prevent_secrets": "preventSecrets",
        "reject_non_dco_commits": "rejectNonDcoCommits",
        "reject_unsigned_commits": "rejectUnsignedCommits",
    },
)
class ProjectPushRules:
    def __init__(
        self,
        *,
        author_email_regex: typing.Optional[builtins.str] = None,
        branch_name_regex: typing.Optional[builtins.str] = None,
        commit_committer_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        commit_committer_name_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        commit_message_negative_regex: typing.Optional[builtins.str] = None,
        commit_message_regex: typing.Optional[builtins.str] = None,
        deny_delete_tag: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        file_name_regex: typing.Optional[builtins.str] = None,
        max_file_size: typing.Optional[jsii.Number] = None,
        member_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prevent_secrets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reject_non_dco_commits: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reject_unsigned_commits: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param author_email_regex: All commit author emails must match this regex, e.g. ``@my-company.com$``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#author_email_regex Project#author_email_regex}
        :param branch_name_regex: All branch names must match this regex, e.g. ``(feature|hotfix)\\/*``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#branch_name_regex Project#branch_name_regex}
        :param commit_committer_check: Users can only push commits to this repository that were committed with one of their own verified emails. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#commit_committer_check Project#commit_committer_check}
        :param commit_committer_name_check: Users can only push commits to this repository if the commit author name is consistent with their GitLab account name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#commit_committer_name_check Project#commit_committer_name_check}
        :param commit_message_negative_regex: No commit message is allowed to match this regex, e.g. ``ssh\\:\\/\\/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#commit_message_negative_regex Project#commit_message_negative_regex}
        :param commit_message_regex: All commit messages must match this regex, e.g. ``Fixed \\d+\\..*``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#commit_message_regex Project#commit_message_regex}
        :param deny_delete_tag: Deny deleting a tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#deny_delete_tag Project#deny_delete_tag}
        :param file_name_regex: All committed filenames must not match this regex, e.g. ``(jar|exe)$``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#file_name_regex Project#file_name_regex}
        :param max_file_size: Maximum file size (MB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#max_file_size Project#max_file_size}
        :param member_check: Restrict commits by author (email) to existing GitLab users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#member_check Project#member_check}
        :param prevent_secrets: GitLab will reject any files that are likely to contain secrets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#prevent_secrets Project#prevent_secrets}
        :param reject_non_dco_commits: Reject commit when it’s not DCO certified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#reject_non_dco_commits Project#reject_non_dco_commits}
        :param reject_unsigned_commits: Reject commit when it’s not signed through GPG. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#reject_unsigned_commits Project#reject_unsigned_commits}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff35d95b8340935ce7a6171d3b4e31a36394558b658b7707fe11a5630ce5c23)
            check_type(argname="argument author_email_regex", value=author_email_regex, expected_type=type_hints["author_email_regex"])
            check_type(argname="argument branch_name_regex", value=branch_name_regex, expected_type=type_hints["branch_name_regex"])
            check_type(argname="argument commit_committer_check", value=commit_committer_check, expected_type=type_hints["commit_committer_check"])
            check_type(argname="argument commit_committer_name_check", value=commit_committer_name_check, expected_type=type_hints["commit_committer_name_check"])
            check_type(argname="argument commit_message_negative_regex", value=commit_message_negative_regex, expected_type=type_hints["commit_message_negative_regex"])
            check_type(argname="argument commit_message_regex", value=commit_message_regex, expected_type=type_hints["commit_message_regex"])
            check_type(argname="argument deny_delete_tag", value=deny_delete_tag, expected_type=type_hints["deny_delete_tag"])
            check_type(argname="argument file_name_regex", value=file_name_regex, expected_type=type_hints["file_name_regex"])
            check_type(argname="argument max_file_size", value=max_file_size, expected_type=type_hints["max_file_size"])
            check_type(argname="argument member_check", value=member_check, expected_type=type_hints["member_check"])
            check_type(argname="argument prevent_secrets", value=prevent_secrets, expected_type=type_hints["prevent_secrets"])
            check_type(argname="argument reject_non_dco_commits", value=reject_non_dco_commits, expected_type=type_hints["reject_non_dco_commits"])
            check_type(argname="argument reject_unsigned_commits", value=reject_unsigned_commits, expected_type=type_hints["reject_unsigned_commits"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if author_email_regex is not None:
            self._values["author_email_regex"] = author_email_regex
        if branch_name_regex is not None:
            self._values["branch_name_regex"] = branch_name_regex
        if commit_committer_check is not None:
            self._values["commit_committer_check"] = commit_committer_check
        if commit_committer_name_check is not None:
            self._values["commit_committer_name_check"] = commit_committer_name_check
        if commit_message_negative_regex is not None:
            self._values["commit_message_negative_regex"] = commit_message_negative_regex
        if commit_message_regex is not None:
            self._values["commit_message_regex"] = commit_message_regex
        if deny_delete_tag is not None:
            self._values["deny_delete_tag"] = deny_delete_tag
        if file_name_regex is not None:
            self._values["file_name_regex"] = file_name_regex
        if max_file_size is not None:
            self._values["max_file_size"] = max_file_size
        if member_check is not None:
            self._values["member_check"] = member_check
        if prevent_secrets is not None:
            self._values["prevent_secrets"] = prevent_secrets
        if reject_non_dco_commits is not None:
            self._values["reject_non_dco_commits"] = reject_non_dco_commits
        if reject_unsigned_commits is not None:
            self._values["reject_unsigned_commits"] = reject_unsigned_commits

    @builtins.property
    def author_email_regex(self) -> typing.Optional[builtins.str]:
        '''All commit author emails must match this regex, e.g. ``@my-company.com$``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#author_email_regex Project#author_email_regex}
        '''
        result = self._values.get("author_email_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def branch_name_regex(self) -> typing.Optional[builtins.str]:
        '''All branch names must match this regex, e.g. ``(feature|hotfix)\\/*``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#branch_name_regex Project#branch_name_regex}
        '''
        result = self._values.get("branch_name_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def commit_committer_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Users can only push commits to this repository that were committed with one of their own verified emails.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#commit_committer_check Project#commit_committer_check}
        '''
        result = self._values.get("commit_committer_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def commit_committer_name_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Users can only push commits to this repository if the commit author name is consistent with their GitLab account name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#commit_committer_name_check Project#commit_committer_name_check}
        '''
        result = self._values.get("commit_committer_name_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def commit_message_negative_regex(self) -> typing.Optional[builtins.str]:
        '''No commit message is allowed to match this regex, e.g. ``ssh\\:\\/\\/``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#commit_message_negative_regex Project#commit_message_negative_regex}
        '''
        result = self._values.get("commit_message_negative_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def commit_message_regex(self) -> typing.Optional[builtins.str]:
        '''All commit messages must match this regex, e.g. ``Fixed \\d+\\..*``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#commit_message_regex Project#commit_message_regex}
        '''
        result = self._values.get("commit_message_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deny_delete_tag(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Deny deleting a tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#deny_delete_tag Project#deny_delete_tag}
        '''
        result = self._values.get("deny_delete_tag")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def file_name_regex(self) -> typing.Optional[builtins.str]:
        '''All committed filenames must not match this regex, e.g. ``(jar|exe)$``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#file_name_regex Project#file_name_regex}
        '''
        result = self._values.get("file_name_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_file_size(self) -> typing.Optional[jsii.Number]:
        '''Maximum file size (MB).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#max_file_size Project#max_file_size}
        '''
        result = self._values.get("max_file_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def member_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Restrict commits by author (email) to existing GitLab users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#member_check Project#member_check}
        '''
        result = self._values.get("member_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prevent_secrets(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''GitLab will reject any files that are likely to contain secrets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#prevent_secrets Project#prevent_secrets}
        '''
        result = self._values.get("prevent_secrets")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reject_non_dco_commits(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Reject commit when it’s not DCO certified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#reject_non_dco_commits Project#reject_non_dco_commits}
        '''
        result = self._values.get("reject_non_dco_commits")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reject_unsigned_commits(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Reject commit when it’s not signed through GPG.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#reject_unsigned_commits Project#reject_unsigned_commits}
        '''
        result = self._values.get("reject_unsigned_commits")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectPushRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectPushRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.project.ProjectPushRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d1eca75e285e467e1010e303e6795d2944e0bb7c05343036f7a83efb5d5cf91)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthorEmailRegex")
    def reset_author_email_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorEmailRegex", []))

    @jsii.member(jsii_name="resetBranchNameRegex")
    def reset_branch_name_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBranchNameRegex", []))

    @jsii.member(jsii_name="resetCommitCommitterCheck")
    def reset_commit_committer_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitCommitterCheck", []))

    @jsii.member(jsii_name="resetCommitCommitterNameCheck")
    def reset_commit_committer_name_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitCommitterNameCheck", []))

    @jsii.member(jsii_name="resetCommitMessageNegativeRegex")
    def reset_commit_message_negative_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitMessageNegativeRegex", []))

    @jsii.member(jsii_name="resetCommitMessageRegex")
    def reset_commit_message_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitMessageRegex", []))

    @jsii.member(jsii_name="resetDenyDeleteTag")
    def reset_deny_delete_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDenyDeleteTag", []))

    @jsii.member(jsii_name="resetFileNameRegex")
    def reset_file_name_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileNameRegex", []))

    @jsii.member(jsii_name="resetMaxFileSize")
    def reset_max_file_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxFileSize", []))

    @jsii.member(jsii_name="resetMemberCheck")
    def reset_member_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemberCheck", []))

    @jsii.member(jsii_name="resetPreventSecrets")
    def reset_prevent_secrets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreventSecrets", []))

    @jsii.member(jsii_name="resetRejectNonDcoCommits")
    def reset_reject_non_dco_commits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRejectNonDcoCommits", []))

    @jsii.member(jsii_name="resetRejectUnsignedCommits")
    def reset_reject_unsigned_commits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRejectUnsignedCommits", []))

    @builtins.property
    @jsii.member(jsii_name="authorEmailRegexInput")
    def author_email_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorEmailRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="branchNameRegexInput")
    def branch_name_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchNameRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="commitCommitterCheckInput")
    def commit_committer_check_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "commitCommitterCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="commitCommitterNameCheckInput")
    def commit_committer_name_check_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "commitCommitterNameCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="commitMessageNegativeRegexInput")
    def commit_message_negative_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitMessageNegativeRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="commitMessageRegexInput")
    def commit_message_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitMessageRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="denyDeleteTagInput")
    def deny_delete_tag_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "denyDeleteTagInput"))

    @builtins.property
    @jsii.member(jsii_name="fileNameRegexInput")
    def file_name_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileNameRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFileSizeInput")
    def max_file_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxFileSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="memberCheckInput")
    def member_check_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "memberCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="preventSecretsInput")
    def prevent_secrets_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preventSecretsInput"))

    @builtins.property
    @jsii.member(jsii_name="rejectNonDcoCommitsInput")
    def reject_non_dco_commits_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rejectNonDcoCommitsInput"))

    @builtins.property
    @jsii.member(jsii_name="rejectUnsignedCommitsInput")
    def reject_unsigned_commits_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rejectUnsignedCommitsInput"))

    @builtins.property
    @jsii.member(jsii_name="authorEmailRegex")
    def author_email_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorEmailRegex"))

    @author_email_regex.setter
    def author_email_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22ff21ead0ff0446c39cec7ca79f56a287aee3af7af54d753d8aae392463e22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorEmailRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="branchNameRegex")
    def branch_name_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branchNameRegex"))

    @branch_name_regex.setter
    def branch_name_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5081b23ac1ba41414072d60ade6124d3953098630b49fc0f86fb1e00b9a9adc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branchNameRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commitCommitterCheck")
    def commit_committer_check(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "commitCommitterCheck"))

    @commit_committer_check.setter
    def commit_committer_check(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf8b78d01a2a421f0fb34f83296907b52a0636df033d1dc36dbb7cd0869cc839)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitCommitterCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commitCommitterNameCheck")
    def commit_committer_name_check(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "commitCommitterNameCheck"))

    @commit_committer_name_check.setter
    def commit_committer_name_check(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__398266693f11b80332cc48292fc471da3d13c151b2d924535a2310ca04397c5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitCommitterNameCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commitMessageNegativeRegex")
    def commit_message_negative_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitMessageNegativeRegex"))

    @commit_message_negative_regex.setter
    def commit_message_negative_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a2e1c20a1832f777ea4c577a7efdf2c574c2dd9c213f4962dc3de5ddf7a30f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitMessageNegativeRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commitMessageRegex")
    def commit_message_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitMessageRegex"))

    @commit_message_regex.setter
    def commit_message_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ec9863a3daf8bc5afd71d2d2fe573af94398152b791af8a8c7678b36c3b0bb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitMessageRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="denyDeleteTag")
    def deny_delete_tag(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "denyDeleteTag"))

    @deny_delete_tag.setter
    def deny_delete_tag(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae90c4c818f25d9dc47ee320bd36b759abc88153be8a56e216ea07dde2e29320)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "denyDeleteTag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileNameRegex")
    def file_name_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileNameRegex"))

    @file_name_regex.setter
    def file_name_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e95e259dfef9d36d21837149e0a355dd257d87073b510db482e85561bd72d6e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileNameRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxFileSize")
    def max_file_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxFileSize"))

    @max_file_size.setter
    def max_file_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40ecb83e97acdd4540b0a5a2aefcb8f47e1f8fb1b31dbbdbb2758bb0b6efd30e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFileSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memberCheck")
    def member_check(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "memberCheck"))

    @member_check.setter
    def member_check(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44aedf81a599572dc6717ff3a81ba9fa30b8c0aa5974bf5503b2ac9f382aedb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preventSecrets")
    def prevent_secrets(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preventSecrets"))

    @prevent_secrets.setter
    def prevent_secrets(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e39fc476c06596d9ff239f90762ef1d62a490caa6474f7fb3c7de077f81a9016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preventSecrets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rejectNonDcoCommits")
    def reject_non_dco_commits(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rejectNonDcoCommits"))

    @reject_non_dco_commits.setter
    def reject_non_dco_commits(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__338d6b366690f6cd24a0f2ac41b171a8d736a82dee585335c13764cc233e3c21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rejectNonDcoCommits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rejectUnsignedCommits")
    def reject_unsigned_commits(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rejectUnsignedCommits"))

    @reject_unsigned_commits.setter
    def reject_unsigned_commits(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e0d89b9b94ef6c16029b13128e2ecc5d77cd808ed5cfea436fca9b4b9d2d0de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rejectUnsignedCommits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ProjectPushRules]:
        return typing.cast(typing.Optional[ProjectPushRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ProjectPushRules]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac2e1390c9f2ad9d57c002b8e10430fadcb10fd19eefc83e4864c256c720ec39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.project.ProjectTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class ProjectTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#create Project#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#delete Project#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8e6b1af361a5d01b9ec6257a3a2472a47fe48a9e2898c92b767d001d44d8216)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#create Project#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/17.11.0/docs/resources/project#delete Project#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.project.ProjectTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d84d5f074cf05cf4a8fb8106a509529d28bfa42f51871a72022143928f345640)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d73b80202ba4f5e3fb5188a25dda1ff9a4783e315e72268a6dd33241c9301714)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25dfcafd62176637fd9bece9cf6a2283bcec03d2f92f34e857cbf9cdbcd12e64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__484d28eb08adeb7795775c6fcb9756df73cb31a6598d82525e7eee5125790218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Project",
    "ProjectConfig",
    "ProjectContainerExpirationPolicy",
    "ProjectContainerExpirationPolicyOutputReference",
    "ProjectPushRules",
    "ProjectPushRulesOutputReference",
    "ProjectTimeouts",
    "ProjectTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d2173b0bb50322800875b29c7030755fe97cc1d30816c7d87b42f0013c7d5580(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    allow_merge_on_skipped_pipeline: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_pipeline_trigger_approve_deployment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    analytics_access_level: typing.Optional[builtins.str] = None,
    approvals_before_merge: typing.Optional[jsii.Number] = None,
    archived: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    archive_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_cancel_pending_pipelines: typing.Optional[builtins.str] = None,
    autoclose_referenced_issues: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_devops_deploy_strategy: typing.Optional[builtins.str] = None,
    auto_devops_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    avatar: typing.Optional[builtins.str] = None,
    avatar_hash: typing.Optional[builtins.str] = None,
    build_coverage_regex: typing.Optional[builtins.str] = None,
    build_git_strategy: typing.Optional[builtins.str] = None,
    builds_access_level: typing.Optional[builtins.str] = None,
    build_timeout: typing.Optional[jsii.Number] = None,
    ci_config_path: typing.Optional[builtins.str] = None,
    ci_default_git_depth: typing.Optional[jsii.Number] = None,
    ci_delete_pipelines_in_seconds: typing.Optional[jsii.Number] = None,
    ci_forward_deployment_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ci_id_token_sub_claim_components: typing.Optional[typing.Sequence[builtins.str]] = None,
    ci_pipeline_variables_minimum_override_role: typing.Optional[builtins.str] = None,
    ci_restrict_pipeline_cancellation_role: typing.Optional[builtins.str] = None,
    ci_separated_caches: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    container_expiration_policy: typing.Optional[typing.Union[ProjectContainerExpirationPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    container_registry_access_level: typing.Optional[builtins.str] = None,
    container_registry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_branch: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    emails_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    environments_access_level: typing.Optional[builtins.str] = None,
    external_authorization_classification_label: typing.Optional[builtins.str] = None,
    feature_flags_access_level: typing.Optional[builtins.str] = None,
    forked_from_project_id: typing.Optional[jsii.Number] = None,
    forking_access_level: typing.Optional[builtins.str] = None,
    group_runners_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    group_with_project_templates_id: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    import_url: typing.Optional[builtins.str] = None,
    import_url_password: typing.Optional[builtins.str] = None,
    import_url_username: typing.Optional[builtins.str] = None,
    infrastructure_access_level: typing.Optional[builtins.str] = None,
    initialize_with_readme: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    issues_access_level: typing.Optional[builtins.str] = None,
    issues_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    issues_template: typing.Optional[builtins.str] = None,
    keep_latest_artifact: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    lfs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    merge_commit_template: typing.Optional[builtins.str] = None,
    merge_method: typing.Optional[builtins.str] = None,
    merge_pipelines_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    merge_requests_access_level: typing.Optional[builtins.str] = None,
    merge_requests_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    merge_requests_template: typing.Optional[builtins.str] = None,
    merge_trains_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mirror: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mirror_overwrites_diverged_branches: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mirror_trigger_builds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    model_experiments_access_level: typing.Optional[builtins.str] = None,
    model_registry_access_level: typing.Optional[builtins.str] = None,
    monitor_access_level: typing.Optional[builtins.str] = None,
    mr_default_target_self: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    namespace_id: typing.Optional[jsii.Number] = None,
    only_allow_merge_if_all_discussions_are_resolved: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    only_allow_merge_if_pipeline_succeeds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    only_mirror_protected_branches: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    packages_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pages_access_level: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    permanently_delete_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pipelines_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pre_receive_secret_detection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prevent_merge_without_jira_issue: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    printing_merge_request_link_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_builds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_jobs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    push_rules: typing.Optional[typing.Union[ProjectPushRules, typing.Dict[builtins.str, typing.Any]]] = None,
    releases_access_level: typing.Optional[builtins.str] = None,
    remove_source_branch_after_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    repository_access_level: typing.Optional[builtins.str] = None,
    repository_storage: typing.Optional[builtins.str] = None,
    request_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    requirements_access_level: typing.Optional[builtins.str] = None,
    resolve_outdated_diff_discussions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restrict_user_defined_variables: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security_and_compliance_access_level: typing.Optional[builtins.str] = None,
    shared_runners_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_wait_for_default_branch_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    snippets_access_level: typing.Optional[builtins.str] = None,
    snippets_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    squash_commit_template: typing.Optional[builtins.str] = None,
    squash_option: typing.Optional[builtins.str] = None,
    suggestion_commit_message: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    template_name: typing.Optional[builtins.str] = None,
    template_project_id: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[ProjectTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    topics: typing.Optional[typing.Sequence[builtins.str]] = None,
    use_custom_template: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    visibility_level: typing.Optional[builtins.str] = None,
    wiki_access_level: typing.Optional[builtins.str] = None,
    wiki_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__4cc5d19d006568564a2a3cfd20f7ee36be0475e29a083408063121c8dc35acf7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7720953023af4e9a324f9b83458c1d9a993975d5bd799b0bf21ec0e3250c4dd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f20a2f8753eb02f5996962c7dc586b4c9e6cae1d3db31e578e8ff3e5fe60fd0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b63e479e2a2e67a7b2701403b44d71606eece0833b43826d92466343de6ae2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50463079233251631937821546249b0c6416caecb354cbfba5f8a4126bc0aaab(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce5fceba4cce9233297b3939cf3ce983d05903d1d7374cacb2453e9f9e007dc3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d69f98caacbd79d12802d55c25c646f2860a4608f58d4b93629881784b86dc5b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b3ce900b8b5f9808388ef66c978415a6f2102764b1b73216c539c72314c4bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2815dd42610c310f2a6afe4412d8a32dae0633ef15e2a45af4492cf26c3032a8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__618de3cff3633b2ccab7c63d7cd494a4ffdde1168718aa097612081bebee674a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9284ed85e2e0ea9617223e16b4fcd3ba507fd9ceb2092b5799f233674d0eed7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e759bbd484eb31f3bb75433427ea379be520f22d49e5f6ad3937f5d6142583(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1257c74a1e43481413c1feb3d5001aedec9828b6d5b8b03f3443557a858e4737(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c47413678c8932dd842b5b790aa22ce2ec89bde2e61f7b809ac62428ec17af0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2762d906019fdeffd60048d8bd847fd44675d624ada12ddf20a9f36406f4beb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__599a4629b0752678f346673f118eab7cd897571562f3d31f3fe697ad9cd86579(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f745441f0a34dcf878662e649b32fbeaa6a10836856b3ec3f2b1c8ca271d047(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b40184dd6b51f071d3210a3a7b13f9e740df9c1b253a6ea2ddd01dde780ae6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a86511b3970b7ac819e7a0586dfdc12fb21b7c31dc97573427c09c3e1218ea1d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4775d75147f6e136dc035cd8f64317b27e0b235832aa65c5c3301de6b0209a30(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7650d35b8fd0580ff2e0df59e0854f23713e9e4a1b0062f211d0a242ee819703(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ed6f0134a541ec09572ce91aed5061c1cb07a17e84f2754d57c0c2e038b90f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd6f7bbe3ad16bc73b8bbb181292c84e6ae13f253f26bd5778b3e8397d0a55b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87736c2bea32c96e5e0868709cd3e9a86e9a9cbefdd4474c4991d519360e5a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b41dab6c5c58a2ad3b77370c008e30a460414aa8adc6cf566378dc61cf8158(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db40d9a0ef7dcc1912a12fe88d0d1bc91f4776ff2fd2012d93318a0e537c1a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc779dceb7b8d00ee010c0cc760845775c915b4bc4ab9253a0eeb4f17ef8fa6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492dde2baafa69396d477930efffb6ba89d2213cae2b0cfb3479e9e32d277c7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb6d0cdd4255a769e976bcb3bc878be0ba6e29bd9d2d765c6e229854ea92ee3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876b224f773bd1d500f4ac6bf2fb0e1d25ccc999c7f77a2d6bbf227e32cbaf6e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbff0b897676ff143b34e6ee490c9d26aae11b99eac93c9bfb53d89494432f54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5301348d3ea99c18c7b3c79bc8929be85044849e36d0c3c3769fc7914f7d2a17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f365a7d3032fee5168227e39f870d1989e35034c46c04f127a776b73a5e67f9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f9542ff4ec6e2dc282d33a9e45e2d5cef29865875239790fe3f2cf763a772f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0360cb384a360c4c3fce95e8976223252da3b4f8d4d61cff8ca416675a28221(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0166083d46b7cc1c136a32fef50a9ad7df545edf1de6bc48c83450d8174cc848(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2344b0f84ecbad1dd7bda33d68cac69caedb27f4672e3ac8adcd52157fc5b266(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__391e59e752248192b195825a881e1abb207ae32841ab8c634a168d93d2599016(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0ada320871e88cdbc2d83a83e8e3fa4ab7e4546da98f9e3ee1e85ec2b55406(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085f6adb0eede64b94af40382f2aa9e52ef3180ad64b9db1952801c12aa336fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac3b79e43e8e550c10510efbd2d96c423e4c74cd28cc5e314f901ca66594d10b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4583e76e277b53c054ac08a0715ac2636fec0a9c5dfeed9584c27be54a15d00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f365eabdf77d2437c4ce7d12bedeb78368985dc9362440d9907828b18a5284f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961d059d1b52f5cb577dcfa5fdd0b1723e7484c72ef43200600a7c20f6b039b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca288aee588c70082fff179787b08045491fbd5a3d3f598fc41531ce23023e3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b801cc53a73f6d3abaad0b099323a134fc4dd6a82bfb0e23a4a57df8ffbe026c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3769adc0ba16bd78c545aa019135d42ed874ee57c217db73bee73c975344dcfa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f71d99a7a3f9e42f96b8e9ebfbcd99cd660132b9004c853a7c9df493b9fb0ff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__807a0c19cc8e6d11627c375fb6e4a37b67348b1ca38332f865a471399b1d3b1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c35e3966cb22c86168b62e5477829a3080cf0be773ac232a79426bafbe1c7f98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__216deebc496425c752d80670209cb6d2e8bc5d24342793d9461e8bac5b8ff944(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28edbd395755370de227b620571a95e688cf290532c080160c0f595896cf563a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3538e1a91bd84cd99395599a447f384a07f34f0be3aa0ca5c7954bb06310a76(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65fbf0b38939ded6b2c74f532b1855bd660c98b821388ff140738afe8f46a279(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19dc42d2760288cc84f1f93ac2280d9ea807f65c8856cae47d0c51e6677d45f9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f6892b08f576f7be0fda65cba031d8b6efcc54296965591a3e9ee8d7f6b5232(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcbdea53b7bbb6a16bfdac864b3058129139c6fa76e089c5c5579b95515010d8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c667ad7dfb5114afaf82f8250c5a709c0c7b80e0eef0b963668ab56e4fe67b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd50df7c617ed8af0561205440168a8bd741b80f71ee40014113a48b52006ca4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85312fdd83ff00e5f418d3a02111a493d9b0e48efa487149bfa35cf3772ea388(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5029ebe9cf78a0ce2a9e81189b27c01a7705a114eb756512b9fe4b7ac4b2ed9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59273e9ff19fb4854698988e9aa58241e9ca822b6e8ac29d20ab4144f975fb53(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe03191df7018c3fba732187b9038e8f4fccf70e7de45d0010e20af4e8cbaf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c729a1ea7a441913e553f92587c61220e9b766530c8e9ff4b3e234de11d241(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd4fb866305ee70afa162ec6625153065028d64445e4672dd13c65e69794cdf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04bc734a522fd8dea632af021fcf98a65ba97a614dbce827ec40e1f6ce48a01e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef1232b53bc8d11118fc976db5aa1aa66a4a02aeeb72724908f9d37d17df770b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81d8f09149c1bdf9df31a77779d693ac195471bb9af67f36f3466483799a8aec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0648bc69a76a430e2e7e7c0755e263cca0e765e542f92e9bcd78d0b375849d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377be5d79e807f244068fd9277e04ccbad92dda8d73101853f4b5c6737bdc40c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f8f919087e719e4d2b6ce712258dac9d4fc104dd2423aca6207c758a13dd8d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7c14219bd1444855a494bf1e70ee2e756c2983fbe85c2c1b82a8ee75582cc5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f16afb98921b2fea618f023f0786c760f5b6f7c97716da0dbc961bc3dd67b328(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f2cc0b438b62cde5f4b79f3434b245dbae76ba15e9d576dfd91782a4c6b2e3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35be9e2abc1c8fe52ab7dde656a07ac62fc88cf75d37dc7cca65773fd62c8610(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e080aff4eeb5c856f75ea07fe760527c5122e49383939b428668e2f940939536(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d002f034e319569568f3e5ec835ba0d145b60b1caee7ecd37aed11429859f65a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16af67f6205a368a583e39305e287827497af4eb9cf5ceaf9cdd1112903329d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b377615606c8ba5a32679029843541aa633183f9780441d9fa9dad9e2986d422(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a6645d6afc8062aa440727b5ffa1a26087c18826d9d9a2db439aa31d1ea843(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16212c2e5baae9c569df56996300e476c2fd47180fc8e3c0b0c1394f351c265f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ddd9f7ec538b2c71b0bb82cb85db6ec209f484f4718533c785da8084ea5d970(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ee3e507cd3dfa5fe67519ff1300271bb29fa878636f0969564408a90b518170(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbf428cca7b3d41eead73b3de4b3816d28aa426991c5362a07e92755ed06a041(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58ef947f89a0a66660346a8d6865cafb067ee82e63dd48a67af64e310ca15ec5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1643543e2f32823446517da824f9c39ed66e7c3508c1a6c74856e97f4f351fea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff5a9c9a3fc2a8e366c93e75dabb5ef345c7fee7200a4d4fcf444d064f38fcd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b864416593aed0d3d9ebf0efd84985e815203c92278b69778e4bc5bd7fd7c3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f7becac67df745ba9b200bcae9c6f9d48b6247a9e5fb217c9441027f6f3be23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6726fc26ce61f1fccf04e8a4fd15326334e70850a5984c52ed4f8bc1c69a6d4d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__062cae4af9a002ccffc3b292bf579f19bf648acaf47f3ca95a7b114d45b1a749(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37db4feb5e1e379087e07b556a604ff8ace30ce05f5076c2c62f914d44960960(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33def3fb4e82a4ac9bdebf5caa77376811703f8542591fefd6660a869826686e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395930ac24bda9ce44f7b4fc001ba815af5167c42ed6ef94d0446395ebb5c463(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a974616584f3ddca0989c9c17343d580e23cc76a6532d42cfb8e83dc6f387eaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6f27f4ad4895e7022c0306369344a2c3837d669cd317f3e74feed5c954e36a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__717788577432e647953afa83c2a5275a7fdabfa3cb7d7954d9750fa01f39ce4c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2f90fac3851cd716edbeec477216976ab7fa90ddadf6fa17db0c5f3cf4085f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ca540dde10854c71011ebd382cd4818e02380a3728ba2359a3d71c1c763ff5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7242aa4a23953bff60de74ba06a9182344f538db264f1c0cdc43085ab3de60c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__649074350ece8bf58f2ca799e281aaa440d4f8185669bfe963223812e67b2c6b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bddaf370c13119f237b3d2249ec2a22de82ad4f858153da4a356830c5bd5c5dc(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    allow_merge_on_skipped_pipeline: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_pipeline_trigger_approve_deployment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    analytics_access_level: typing.Optional[builtins.str] = None,
    approvals_before_merge: typing.Optional[jsii.Number] = None,
    archived: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    archive_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_cancel_pending_pipelines: typing.Optional[builtins.str] = None,
    autoclose_referenced_issues: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_devops_deploy_strategy: typing.Optional[builtins.str] = None,
    auto_devops_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    avatar: typing.Optional[builtins.str] = None,
    avatar_hash: typing.Optional[builtins.str] = None,
    build_coverage_regex: typing.Optional[builtins.str] = None,
    build_git_strategy: typing.Optional[builtins.str] = None,
    builds_access_level: typing.Optional[builtins.str] = None,
    build_timeout: typing.Optional[jsii.Number] = None,
    ci_config_path: typing.Optional[builtins.str] = None,
    ci_default_git_depth: typing.Optional[jsii.Number] = None,
    ci_delete_pipelines_in_seconds: typing.Optional[jsii.Number] = None,
    ci_forward_deployment_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ci_id_token_sub_claim_components: typing.Optional[typing.Sequence[builtins.str]] = None,
    ci_pipeline_variables_minimum_override_role: typing.Optional[builtins.str] = None,
    ci_restrict_pipeline_cancellation_role: typing.Optional[builtins.str] = None,
    ci_separated_caches: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    container_expiration_policy: typing.Optional[typing.Union[ProjectContainerExpirationPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    container_registry_access_level: typing.Optional[builtins.str] = None,
    container_registry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_branch: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    emails_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    environments_access_level: typing.Optional[builtins.str] = None,
    external_authorization_classification_label: typing.Optional[builtins.str] = None,
    feature_flags_access_level: typing.Optional[builtins.str] = None,
    forked_from_project_id: typing.Optional[jsii.Number] = None,
    forking_access_level: typing.Optional[builtins.str] = None,
    group_runners_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    group_with_project_templates_id: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    import_url: typing.Optional[builtins.str] = None,
    import_url_password: typing.Optional[builtins.str] = None,
    import_url_username: typing.Optional[builtins.str] = None,
    infrastructure_access_level: typing.Optional[builtins.str] = None,
    initialize_with_readme: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    issues_access_level: typing.Optional[builtins.str] = None,
    issues_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    issues_template: typing.Optional[builtins.str] = None,
    keep_latest_artifact: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    lfs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    merge_commit_template: typing.Optional[builtins.str] = None,
    merge_method: typing.Optional[builtins.str] = None,
    merge_pipelines_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    merge_requests_access_level: typing.Optional[builtins.str] = None,
    merge_requests_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    merge_requests_template: typing.Optional[builtins.str] = None,
    merge_trains_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mirror: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mirror_overwrites_diverged_branches: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mirror_trigger_builds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    model_experiments_access_level: typing.Optional[builtins.str] = None,
    model_registry_access_level: typing.Optional[builtins.str] = None,
    monitor_access_level: typing.Optional[builtins.str] = None,
    mr_default_target_self: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    namespace_id: typing.Optional[jsii.Number] = None,
    only_allow_merge_if_all_discussions_are_resolved: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    only_allow_merge_if_pipeline_succeeds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    only_mirror_protected_branches: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    packages_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pages_access_level: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    permanently_delete_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pipelines_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pre_receive_secret_detection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prevent_merge_without_jira_issue: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    printing_merge_request_link_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_builds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_jobs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    push_rules: typing.Optional[typing.Union[ProjectPushRules, typing.Dict[builtins.str, typing.Any]]] = None,
    releases_access_level: typing.Optional[builtins.str] = None,
    remove_source_branch_after_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    repository_access_level: typing.Optional[builtins.str] = None,
    repository_storage: typing.Optional[builtins.str] = None,
    request_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    requirements_access_level: typing.Optional[builtins.str] = None,
    resolve_outdated_diff_discussions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restrict_user_defined_variables: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security_and_compliance_access_level: typing.Optional[builtins.str] = None,
    shared_runners_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_wait_for_default_branch_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    snippets_access_level: typing.Optional[builtins.str] = None,
    snippets_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    squash_commit_template: typing.Optional[builtins.str] = None,
    squash_option: typing.Optional[builtins.str] = None,
    suggestion_commit_message: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    template_name: typing.Optional[builtins.str] = None,
    template_project_id: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[ProjectTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    topics: typing.Optional[typing.Sequence[builtins.str]] = None,
    use_custom_template: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    visibility_level: typing.Optional[builtins.str] = None,
    wiki_access_level: typing.Optional[builtins.str] = None,
    wiki_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c134465d2f19253cf8263d41a482769fcea91f99876deed9c1639157c39cbbdd(
    *,
    cadence: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    keep_n: typing.Optional[jsii.Number] = None,
    name_regex: typing.Optional[builtins.str] = None,
    name_regex_delete: typing.Optional[builtins.str] = None,
    name_regex_keep: typing.Optional[builtins.str] = None,
    older_than: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0de4753bbf69e900422fb46e2ca806925eecd4882b541522d14dd4fcc827b3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__481878a2b02a6662df25d3b20a64635a2f2996628641b1ba47965dfa8eac20fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eeeae9492fec5d77433118546c0fbd53fd5510ae46535a048602e9bd145bc79(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ee71d8112b55ce54a9f60cf5d3a2811eec1c96420284addacd145f1aba1d2f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032cee01373b66e9067d9cf031ccb876465cfb43f3a1d9123554d35aeeedc85a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef59396557624da8549c22f3e310b7cb7eabc33fcdbc1617552cbbfd3e319950(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d20de45d369a47cd0b6868d4779724f55228763fa72acb44c6d3058407eee36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0419624816ae54d9371de7800af0c3155b7cb06e62659892a050e5663d855c42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__505a8dea72c5e5c15331ac448ccf11ffac738d81bcce98f9f43fedbadb33849c(
    value: typing.Optional[ProjectContainerExpirationPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff35d95b8340935ce7a6171d3b4e31a36394558b658b7707fe11a5630ce5c23(
    *,
    author_email_regex: typing.Optional[builtins.str] = None,
    branch_name_regex: typing.Optional[builtins.str] = None,
    commit_committer_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    commit_committer_name_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    commit_message_negative_regex: typing.Optional[builtins.str] = None,
    commit_message_regex: typing.Optional[builtins.str] = None,
    deny_delete_tag: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    file_name_regex: typing.Optional[builtins.str] = None,
    max_file_size: typing.Optional[jsii.Number] = None,
    member_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prevent_secrets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reject_non_dco_commits: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reject_unsigned_commits: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d1eca75e285e467e1010e303e6795d2944e0bb7c05343036f7a83efb5d5cf91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22ff21ead0ff0446c39cec7ca79f56a287aee3af7af54d753d8aae392463e22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5081b23ac1ba41414072d60ade6124d3953098630b49fc0f86fb1e00b9a9adc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf8b78d01a2a421f0fb34f83296907b52a0636df033d1dc36dbb7cd0869cc839(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398266693f11b80332cc48292fc471da3d13c151b2d924535a2310ca04397c5e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a2e1c20a1832f777ea4c577a7efdf2c574c2dd9c213f4962dc3de5ddf7a30f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec9863a3daf8bc5afd71d2d2fe573af94398152b791af8a8c7678b36c3b0bb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae90c4c818f25d9dc47ee320bd36b759abc88153be8a56e216ea07dde2e29320(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e95e259dfef9d36d21837149e0a355dd257d87073b510db482e85561bd72d6e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ecb83e97acdd4540b0a5a2aefcb8f47e1f8fb1b31dbbdbb2758bb0b6efd30e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44aedf81a599572dc6717ff3a81ba9fa30b8c0aa5974bf5503b2ac9f382aedb4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e39fc476c06596d9ff239f90762ef1d62a490caa6474f7fb3c7de077f81a9016(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__338d6b366690f6cd24a0f2ac41b171a8d736a82dee585335c13764cc233e3c21(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0d89b9b94ef6c16029b13128e2ecc5d77cd808ed5cfea436fca9b4b9d2d0de(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac2e1390c9f2ad9d57c002b8e10430fadcb10fd19eefc83e4864c256c720ec39(
    value: typing.Optional[ProjectPushRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e6b1af361a5d01b9ec6257a3a2472a47fe48a9e2898c92b767d001d44d8216(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d84d5f074cf05cf4a8fb8106a509529d28bfa42f51871a72022143928f345640(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73b80202ba4f5e3fb5188a25dda1ff9a4783e315e72268a6dd33241c9301714(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25dfcafd62176637fd9bece9cf6a2283bcec03d2f92f34e857cbf9cdbcd12e64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__484d28eb08adeb7795775c6fcb9756df73cb31a6598d82525e7eee5125790218(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
