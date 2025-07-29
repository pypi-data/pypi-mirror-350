from __future__ import annotations

import json
import logging
import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Union, TypeAlias, Optional, Iterable

from pydantic import StrictStr

from .api.client_api import ClientApi
from .api_client import ApiClient
from .configuration import Configuration, ConfigurationError
from .models.artifact import Artifact
from .models.comment import Comment
from .models.control_tag import ControlTag
from .models.control_tagging_object_type import ControlTaggingObjectType
from .models.file import File
from .models.function_auth_secret import FunctionAuthSecret
from .models.function_auth_type import FunctionAuthType
from .models.job import Job
from .models.model import Model
from .models.new_function_auth_secret import NewFunctionAuthSecret
from .models.new_source import NewSource
from .models.patch_op import PatchOp
from .models.resource_control_tagging import ResourceControlTagging
from .models.user import User
from .models.user_control_tagging import UserControlTagging

logger = logging.getLogger("istari-digital-client.client")

PathLike = Union[str, os.PathLike, Path]
JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None


class Client(ClientApi):
    """Create a new instance of the Istari client

    Args:
        config (Configuration | None): The configuration for the client

    Returns:
        Client: The Istari client instance
    """

    def __init__(
        self,
        config: Configuration | None = None,
    ) -> None:
        config = config or Configuration()

        if not config.registry_url:
            raise ConfigurationError(
                "Registry URL not set! Must be specified, either via ISTART_REGISTRY_URL env or by explicitly setting "
                "in  'registry_url' parameter in (optional) configuration parameter on client initialization"
            )
        if not config.registry_auth_token:
            logger.warning("registry auth token not set!")

        self.configuration: Configuration = config

        self._api_client = ApiClient(config)

        super().__init__(self.configuration, self._api_client)

    def __del__(self):
        if (
            self.configuration.filesystem_cache_enabled
            and self.configuration.filesystem_cache_clean_on_exit
            and self.configuration.filesystem_cache_root.exists()
            and self.configuration.filesystem_cache_root.is_dir()
        ):
            logger.debug("Cleaning up cache contents for client exit")
            for child in self.configuration.filesystem_cache_root.iterdir():
                if child.is_dir():
                    logger.debug("deleting cache directory - %s", child)
                    shutil.rmtree(
                        self.configuration.filesystem_cache_root, ignore_errors=True
                    )
                elif child.is_file() and not child.is_symlink():
                    logger.debug("deleting cache file - %s", child)
                    child.unlink(missing_ok=True)
                else:
                    logger.debug(
                        "not deleting cache item (is neither a directory nor a regular file) -  %s",
                        child,
                    )

    def add_artifact(
        self,
        model_id: str,
        path: PathLike,
        sources: list[NewSource | str] | None = None,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
    ) -> Artifact:
        """Add an artifact

        Args:
            model_id (str): The model to add the artifact to
            path (PathLike): The path to the artifact
            sources (List[NewSource]): The sources of the artifact
            description (str | None): The description of the artifact
            version_name (str | None): The version name of the artifact
            external_identifier (str | None): The external identifier of the artifact
            display_name (str | None): The display name of the artifact

        Returns:
            Artifact: The added artifact

        """
        file_revision = self.create_revision(
            file_path=path,
            sources=sources,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )

        return self._create_artifact(
            model_id=model_id,
            file_revision=file_revision,
        )

    def update_artifact(
        self,
        artifact_id: str,
        path: PathLike,
        sources: list[NewSource | str] | None = None,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
    ) -> Artifact:
        salt = self.get_artifact(artifact_id=artifact_id).revision.content_token.salt

        file_revision = self.update_revision_content(
            file_path=path,
            salt=salt,
            sources=sources,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )

        return self._update_artifact(
            artifact_id=artifact_id,
            file_revision=file_revision,
        )

    def add_comment(
        self,
        resource_id: str,
        path: PathLike,
        description: str | None = None,
    ) -> Comment:
        """Add a comment to a resource

        Args:
            resource_id (str): The resource to add the comment to
            path (PathLike): The path to the comment
            description (str | None): The description of the comment

        Returns:
            Comment: The added comment

        """
        file_revision = self.create_revision(
            file_path=path,
            sources=None,
            display_name=None,
            description=description,
            version_name=None,
            external_identifier=None,
        )

        return self._create_comment(
            resource_id=resource_id,
            file_revision=file_revision,
        )

    def update_comment(
        self,
            comment_id: str,
        path: PathLike,
        description: str | None = None,
    ) -> Comment:
        """Update a comment

        Args:
            comment_id (str | UUID | Comment): The comment to update
            path (PathLike): The path to the comment
            description (str | None): The description of the comment

        Returns:
            Comment: The updated comment

        """

        salt = self.get_comment(comment_id=comment_id).revision.content_token.salt

        file_revision = self.update_revision_content(
            file_path=path,
            salt=salt,
            sources=None,
            display_name=None,
            description=description,
            version_name=None,
            external_identifier=None,
        )

        return self._update_comment(
            comment_id=comment_id,
            file_revision=file_revision,
        )

    def add_file(
        self,
        path: PathLike,
        sources: list[NewSource | str] | None = None,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
    ) -> File:
        """Add a file

        Args:
            path (PathLike): The path to the file
            sources (List[NewSource] | None): The sources of the file
            description (str | None): The description of the file
            version_name (str | None): The version name of the file
            external_identifier (str | None): The external identifier of the file
            display_name (str | None): The display name of the file

        Returns:
            File: The added file

        """
        file_revision = self.create_revision(
            file_path=path,
            sources=sources,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )

        return self._create_file(
            file_revision=file_revision,
        )

    def update_file(
        self,
        file_id: str,
        path: PathLike | str,
        sources: list[NewSource | str] | None = None,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
    ) -> File:
        """Update a file

        Args:
            file_id (str): The file to update
            path (PathLike): The path to the file
            sources (List[NewSource] | None): The sources of the file
            description (str | None): The description of the file
            version_name (str | None): The version name of the file
            external_identifier (str | None): The external identifier of the file
            display_name (str | None): The display name of the file

        Returns:
            File: The updated file

        """
        salt = self.get_file(file_id=file_id).revision.content_token.salt

        file_revision = self.update_revision_content(
            file_path=path,
            salt=salt,
            sources=sources,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )

        return self._update_file(
            file_id=file_id,
            file_revision=file_revision,
        )

    def update_file_properties(
        self,
        file: File,
        display_name: str | None = None,
        description: str | None = None,
        external_identifier: str | None = None,
        version_name: str | None = None,
    ) -> File:
        """Update file properties

        Args:
            file (File): The file to update
            display_name (str | None): The display name of the file
            description (str | None): The description of the file

        Returns:
            File: The updated file

        """
        return self.update_revision_properties(
            file_revision=file.revision,
            display_name=display_name,
            description=description,
            external_identifier=external_identifier,
            version_name=version_name,
        )

    def add_job(
        self,
        model_id: str,
        function: str,
        *,
        parameters: JSON | None = None,
        parameters_file: PathLike | None = None,
        tool_name: str | None = None,
        tool_version: str | None = None,
        operating_system: str | None = None,
        agent_identifier: str | None = None,
        sources: list[NewSource | str] | None = None,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
        **kwargs,
    ) -> "Job":
        """Add a job

        Args:
            model_id (str): The model to add the job to
            function (str): The function of the job
            parameters (JSON | None): The parameters of the job
            parameters_file (PathLike | None): The path to the parameters file
            tool_name (str | None): The name of the tool
            tool_version (str | None): The version of the tool
            operating_system (str | None): The operating system of the agent
            agent_identifier (str | None): The identifier of the agent
            sources (List[NewSource] | None): The sources of the job
            description (str | None): The description of the job
            version_name (str | None): The version name of the job
            external_identifier (str | None): The external identifier of the job
            display_name (str | None): The display name of the job

        Returns:
            Job: The added job

        """
        parameters_file_is_temp = False
        if parameters_file and (parameters or kwargs):
            raise ValueError(
                "Can't combine a parameters file with explicit parameters or parameter kwargs"
            )
        if not parameters_file:
            if parameters and kwargs:
                raise ValueError(
                    "Can't combine explicit parameters with parameters kwargs"
                )
            parameters = parameters or kwargs
            parameters_file = Path(
                tempfile.NamedTemporaryFile(
                    prefix="parameters", suffix=".json", delete=False
                ).name
            )
            parameters_file.write_text(json.dumps(parameters, indent=4))
            parameters_file_is_temp = True
        parameters_file = Path(parameters_file)
        try:
            file_revision = self.create_revision(
                file_path=str(parameters_file),
                sources=sources,
                display_name=display_name,
                description=description,
                version_name=version_name,
                external_identifier=external_identifier,
            )

            openapi_job = self._create_model_job(
                model_id=model_id,
                function_name=function,
                file_revision=file_revision,
                tool_name=tool_name,
                tool_version=tool_version,
                operating_system=operating_system,
                agent_identifier=agent_identifier,
            )
        finally:
            if parameters_file_is_temp:
                if parameters_file.exists():
                    parameters_file.unlink(missing_ok=True)

        return openapi_job

    def update_job(
        self,
        job_id: str,
        path: PathLike,
        sources: list[NewSource | str] | None = None,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
    ) -> Job:
        """Update a job

        Args:
            job_id (str): The job to update
            path (PathLike): The path to the job
            sources (List[NewSource] | None): The sources of the job
            description (str | None): The description of the job
            version_name (str | None): The version name of the job
            external_identifier (str | None): The external identifier of the job
            display_name (str | None): The display name of the job

        Returns:
            Job: The updated job

        """
        salt = self.get_job(job_id=job_id).revision.content_token.salt

        file_revision = self.update_revision_content(
            file_path=path,
            salt=salt,
            sources=sources,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )

        return self._update_job(
            job_id=job_id,
            file_revision=file_revision,
        )

    def add_model(
        self,
        path: PathLike,
        sources: list[NewSource | str] | None = None,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
    ) -> Model:
        """Add a model

        Args:
            path (PathLike): The path to the model
            sources (List[NewSource] | None): The sources of the model
            description (str | None): The description of the model
            version_name (str | None): The version name of the model
            external_identifier (str | None): The external identifier of the model
            display_name (str | None): The display name of the model

        Returns:
            model: The added model

        """
        file_revision = self.create_revision(
            file_path=path,
            sources=sources,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )
        return self._create_model(
            file_revision=file_revision,
        )

    def update_model(
        self,
        model_id: str,
        path: PathLike,
        sources: list[NewSource | str] | None = None,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
    ) -> Model:
        """Update a model

        Args:
            model_id (str): The model to update
            path (PathLike): The path to the model
            sources (List[NewSource] | None): The sources of the model
            description (str | None): The description of the model
            version_name (str | None): The version name of the model
            external_identifier (str | None): The external identifier of the model
            display_name (str | None): The display name of the model

        Returns:
            model: The updated model

        """
        salt = self.get_model(model_id=model_id).revision.content_token.salt

        file_revision = self.update_revision_content(
            file_path=path,
            salt=salt,
            sources=sources,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )

        return self._update_model(
            model_id=model_id,
            file_revision=file_revision,
        )

    def add_function_auth_secret(
        self,
        auth_provider_name: str,
        function_auth_type: FunctionAuthType,
        path: PathLike,
        expiration: Optional[datetime] = None,
    ) -> FunctionAuthSecret:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(path)

        file_revision = self.create_revision(
            file_path=path,
        )

        secret = NewFunctionAuthSecret(
            auth_provider_name=auth_provider_name,
            revision=file_revision,
            function_auth_type=function_auth_type,
            expiration=expiration,
        )

        return self._create_function_auth_secret(secret)

    def add_user_control_taggings(
        self,
        user_id: StrictStr,
        control_tag_ids: Iterable[StrictStr],
        reason: Optional[StrictStr] = None,
    ) -> list[UserControlTagging]:
        """Assign one or more control tags to a model

         Args:
             user_id (str): The id of the user to assign control tag access.
             control_tag_id Iterable[str]:  The ids of the control tags to assign access to.
             reason (Optional[str]) The reson for the assignment (optionsl).

         Returns:
             list[UserControlTagging]: A list of UserControlTagging objects, one for each tag assignment made.

        The list resource control taggings returned may be more than the number of control tags assigned,
        as when a tag is applied to a model, the tagging is applied to each of its child artifacts as well.

        Note: The calling user must be a customer admin on the tenant the target user is a member of or the operation
        will fail with a permission denied error.

        """

        return self.patch_user_control_taggings(
            user_id, list(control_tag_ids), patch_op=PatchOp.SET, reason=reason
        )

    def remove_user_control_taggings(
        self,
        user_id: StrictStr,
        control_tag_ids: Iterable[StrictStr],
        reason: Optional[StrictStr] = None,
    ) -> list[UserControlTagging]:
        """Remove (archive) one or more control tag access assignments from a user.

         Args:
             user_id (str): The id of the user to remove control tag access from.
             control_tag_id Iterable[str]:  The ids of the control tags to remove access assignments fro
             reason (Optional[str]) The reson for the assignment (optionsl).

         Returns:
             list[UserControlTagging]: A list of UserControlTagging objects, one for each tag assignment made.

        Note: The calling user must be a customer admin on the tenant the target user is a member of or the operation
        will fail with a permission denied error.

        """

        return self.patch_user_control_taggings(
            user_id, list(control_tag_ids), patch_op=PatchOp.DELETE, reason=reason
        )

    def add_model_control_taggings(
        self,
        model_id: StrictStr,
        control_tag_ids: Iterable[StrictStr],
        reason: Optional[StrictStr] = None,
    ) -> list[ResourceControlTagging]:
        """Assign one or more control tags to a model

         Args:
             model_id (str): The model to assign the control tag to.
             control_tag_id Iterable[str]:  The ids of the control tags to assign.
             reason (Optional[str]) The reson for the assignment (optionsl).

         Returns:
             list[ResourceControlTagging]: A list of ResourceControlTagging objects, one for each tag assignment made.

        The list resource control taggings returned may be more than the number of control tags assigned,
        as when a tag is applied to a model, the tagging is applied to each of its child artifacts as well.

        Note: Owner or administrator access to the model is required to modify control tag assignments.

        """

        return self.patch_model_control_taggings(
            model_id, list(control_tag_ids), patch_op=PatchOp.SET, reason=reason
        )

    def remove_model_control_taggings(
        self,
        model_id: StrictStr,
        control_tag_ids: Iterable[StrictStr],
        reason: Optional[StrictStr] = None,
    ) -> list[ResourceControlTagging]:
        """Remove (archive) one or more control tag assignments from a model.

        Args:
            model_id (str): The id of the model to remove the control tag assignment from.
            control_tag_id Iterable[str]:  The ids of the control tags to assign.
            reason (Optional[str]) The reson for the assignment (optionsl).

        Returns:
            list[ResourceControlTagging]: A list of ResourceControlTagging objects,one for each tagging archived.

        Note: Owner or administrator access to the model its parent model is required to modify control tag
        assignments.

        """

        return self.patch_model_control_taggings(
            model_id, list(control_tag_ids), patch_op=PatchOp.DELETE, reason=reason
        )

    def add_artifact_control_taggings(
        self,
        artifact_id: StrictStr,
        control_tag_ids: Iterable[StrictStr],
        reason: Optional[StrictStr] = None,
    ) -> list[ResourceControlTagging]:
        """Assign one or more control tags to an artifact,

        Args:
            artifact_id (str): The id of the artifact to assign the control tag to.
            control_tag_id Iterable[str]:  The ids of the control tags to assign.
            reason (Optional[str]) The reson for the assignment (optionsl).

        Returns:
            list[ResourceControlTagging]: A list of ResourceControlTagging objects, one for each tag assignment made.

        Note: Owner or administrator access to the artifactits parent model is required to modify control tag
        assignments.

        """

        return self.patch_artifact_control_taggings(
            artifact_id, list(control_tag_ids), patch_op=PatchOp.SET, reason=reason
        )

    def remove_artifact_control_taggings(
        self,
        artifact_id: StrictStr,
        control_tag_ids: Iterable[StrictStr],
        reason: Optional[StrictStr] = None,
    ) -> list[ResourceControlTagging]:
        """Archive one or more control tagings on  amodel

        Args:
            artifact_id (str): The id of the artifact to remove the control tag assignment from.
            control_tag_id Iterable[str]:  The ids of the control tags to assign.
            reason (Optional[str]) The reson for the assignment (optionsl).

        Returns:
            list[ResourceControlTagging]: A list of ResourceControlTagging objects, one for each resulting taggging applied.

        Note: Owner or administrator access to the artifactits parent model is required to modify control tag
        assignments.

        """

        return self.patch_artifact_control_taggings(
            artifact_id, list(control_tag_ids), patch_op=PatchOp.DELETE, reason=reason
        )

    def get_model_control_tags(self, model_id: StrictStr) -> list[ControlTag]:
        """Get list of control tags for the active control taggings on a model.
        Args:
            model_id (str): The id of the model to get the assigned control tags for.

        Returns:
             list[ControlTag};  The list of control tags assigned to the model.

        """

        return self.get_object_control_tags(ControlTaggingObjectType.MODEL, model_id)

    def get_artifact_control_tags(self, artifact_id: StrictStr) -> list[ControlTag]:
        """Get list of control tags for the active control taggings on a model.
        Args:
            artifact_id (str): The id of the model to get the assigned control tags for.

        Returns:
             list[ControlTag};  The list of control tags assigned to the model.

        """

        return self.get_object_control_tags(
            ControlTaggingObjectType.ARTIFACT, artifact_id
        )

    def get_user_control_tags(self, user_id: StrictStr) -> list[ControlTag]:
        """Get list of control tags a user has been assigned access to.
        Args:
            user_id (str): The id of the user to get the assigned control tags for.

        Returns:
             list[ControlTag};  The list of control tags the user has been assigned access to.

        """

        return self.get_object_control_tags(ControlTaggingObjectType.USER, user_id)

    def get_user(self, user_id: StrictStr) -> User:
        """Get a user from the registry
        Args:
            user_id (str): The id of the user to get the assigned control tags for.

        Returns:
             list[ControlTag};  The list of control tags the user has been assigned access to.

        This method simply a convenience wrapper for "get_user_by_id" added for
        "get" method naming convention consistency (get_model, get_artifact, etc...)
        """

        return self.get_user_by_id(user_id)
