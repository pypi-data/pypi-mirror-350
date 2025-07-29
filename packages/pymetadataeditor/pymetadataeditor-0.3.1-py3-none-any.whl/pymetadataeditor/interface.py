"""The interface between pyMetadataEditor and the Metadata Editor API."""

import warnings
from io import BufferedReader
from json import JSONDecodeError
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable, Dict, Iterable, List, Optional, Tuple, Type, Union

import pandas as pd
import tiktoken
from markitdown import MarkItDown
from metadataschemas.metadata_manager import MetadataManager
from metadataschemas.utils.schema_base_model import SchemaBaseModel

# from metadataschemas.utils.quick_start import make_skeleton
from metadataschemas.utils.utils import merge_dicts, standardize_keys_in_dict
from openai import AzureOpenAI, OpenAI
from pydantic import BaseModel, ValidationError
from requests.exceptions import HTTPError
from urllib3.exceptions import InsecureRequestWarning

from pymetadataeditor.llm_helpers import (
    _iterated_validated_update_to_outline,
    _prepend_draft_drop_non_str,
    call_per_field,
    get_date_as_text,
    json_to_markdown,
)
from pymetadataeditor.requester import RequestsWithSpecificErrors
from pymetadataeditor.templates import pydantic_from_template

from .utils import remove_empty_from_dict, validate_json_patches

__all__ = ["MetadataEditor", "DeleteNotAppliedError", "TemplateError"]

DICT_MODES = ["dict", "dictionary"]
PYDANTIC_MODES = ["pydantic", "model", "basemodel", "object"]
EXCEL_MODES = ["excel"]

shown_insecure_request_warnings = set()


# Define a custom function to display warnings once only for unique InsecureRequestWarning messages
def custom_showwarning(message, category, filename, lineno, file=None, line=None):
    global shown_insecure_request_warnings
    # Only handle InsecureRequestWarning
    if category is InsecureRequestWarning:
        # Check if this message has already been shown
        warning_key = (str(message), filename, lineno)
        if warning_key not in shown_insecure_request_warnings:
            # Show the warning and add the message to the set
            warnings._showwarnmsg_impl(warnings.WarningMessage(message, category, filename, lineno, file, line))
            shown_insecure_request_warnings.add(warning_key)
    else:
        # Pass other warnings through without suppression
        warnings._showwarnmsg_impl(warnings.WarningMessage(message, category, filename, lineno, file, line))


# Set the warnings to always trigger, but filter them through custom_showwarning
warnings.simplefilter("always", InsecureRequestWarning)
warnings.showwarning = custom_showwarning


class DeleteNotAppliedError(Exception):
    """Exception raised when a delete request is not accepted by the system."""

    def __init__(self, message="Delete request not accepted by system.", response=None):
        """Initialize the error with a message and an optional response."""
        super().__init__(message)
        self.response = response


class TemplateError(Exception):
    """Exception raised when there is an error with a template."""

    def __init__(self, message="Error with template", response=None):
        """Initialize the error with a message and an optional response."""
        super().__init__(message)
        self.message = message
        self.response = response

    def __str__(self):
        """Customize the error message to include the response if available."""
        if self.response:
            return f"{self.response}\n\n{self.message}"
        else:
            return self.message


class MetadataEditor:
    """pyMetadataEditor helps create and manage metadata in a Metadata Editor database.

    pyMetadataEditor allows you to list, create, update and delete projects, manage collections and list templates in
      a metadata database.

    You can save metadata to an Excel file. Or use OpenAI to draft metadata from files or web pages.

    First obtain an API key and pase it into a file called '.env' in the root of your project. The contents of the
        file should look like this:

        `METADATA_API_URL=https://<name_of_your_metadata_database>.org/index.php/api`

        `METADATA_API_KEY=your_api_key`


    Then in python run

    ```python
    from pymetadataeditor import MetadataEditor
    import os

    api_url = os.getenv("METADATA_API_URL")
    api_key = os.getenv("METADATA_API_KEY")
    me = MetadataEditor(api_url = api_url, api_key = api_key)
    ```

    Then you can list and create new projects like so:

    ```python
    me.list_projects(limit=100)
    indicator_metadata = me.make_metadata_outline("indicator", "pydantic")
    # update the indicator metadata as needed.

    # View nicely formatted metadata
    indicator_metadata.pretty_print()

    # Then log the metadata to the database
    me.create_project_log(dict_of_indicator, "indicator")
    ```
    """

    def __init__(self, api_url: str, api_key: str, allow_http: bool = False, verify_ssl: bool = True):
        """Create a new MetadataEditor object connected to an instance of a Metadata Editor database.

        Args:
            api_url (str): the URL typically looks like 'https://<name_of_your_metadata_database>.org/index.php/api'
            api_key (str): typically this is created through the web interface of the metadata system.
            allow_http (bool): whether to allow calls to the metadata system when the URL begins "http" instead of the
                more secure "https". Defaults to False.
            verify_ssl (bool): Although it is good practice for API requests to verify SSL, some systems do not allow
                this so setting verify_ssl=False may be required. Defaults to True.

        Example:
        ```python
        from pymetadataeditor import MetadataEditor
        import os

        api_url = os.getenv("METADATA_API_URL")
        api_key = os.getenv("METADATA_API_KEY")
        me = MetadataEditor(api_url = api_url, api_key = api_key)
        ```
        """
        self._apinterface = RequestsWithSpecificErrors(
            api_url=api_url, api_key=api_key, allow_http=allow_http, verify_ssl=verify_ssl
        )
        self._mm = MetadataManager()
        self._templates = {}
        self._default_templates = None

    ####################################################################################################################
    # PROJECTS
    ####################################################################################################################

    def count_projects(self) -> int:
        """Count the number of projects you have access to.

        Returns:
            int: The number of projects
        """
        list_projects_get_path = "/editor"
        params = {"offset": 0, "limit": 1}
        response = self._apinterface.get_request(pth=list_projects_get_path, params=params)
        return response["total"]

    def list_projects(
        self,
        limit: Union[int, str],
        keywords: Optional[Union[str, List[str]]] = None,
        metadata_type: Optional[str] = None,
        offset: int = 0,
        sort_by: Optional[str] = None,
    ) -> pd.DataFrame:
        """Lists all the projects associated with your API key.

        Args:
            limit (int or str): Page size e.g. 10 to show 10 records. If limit='All' then all records are retrieved.
            keywords (optional str or list of str): Keywords for filtering projects by title and/or idno.
            metadata_type (optional str): If given, only projects of this type are returned.
            offset (int): Offset for pagination e.g. 10 to skip first 10 records. Default is 0.
            sort_by (optional str): valid values: "title_asc", "title_desc", "updated_asc", "updated_desc".

        Returns:
            pd.DataFrame: Information about the projects
        """
        if isinstance(limit, str):
            assert limit.lower() == "all", f"Expected limit to be 'All' or a positive integer but got '{limit}'"
            new_offset = offset
            new_limit = 500
            dfs = []
            while True:
                df = self.list_projects(
                    keywords=keywords, metadata_type=metadata_type, offset=new_offset, limit=new_limit, sort_by=sort_by
                )
                dfs.append(df)
                if len(df) < new_limit:
                    break
                new_offset += new_limit
            return pd.concat(dfs)

        list_projects_get_path = "/editor"
        params = {"offset": offset, "limit": limit}
        if keywords is not None:
            if not isinstance(keywords, str) and isinstance(keywords, Iterable):
                keywords = "%".join(keywords)
            keywords = keywords.replace(" ", "%")
            params["keywords"] = keywords
        if metadata_type is not None:
            metadata_type = self._mm.standardize_metadata_name(metadata_type)
            params["type"] = metadata_type
        if sort_by is not None:
            sort_by = sort_by.lower()
            valid_sort_by = ["title_asc", "title_desc", "updated_asc", "updated_desc"]
            assert sort_by in valid_sort_by, f"{sort_by} not valid, must be one of {valid_sort_by}"
            params["sort_by"] = sort_by
        response = self._apinterface.get_request(pth=list_projects_get_path, params=params)
        try:
            projects = response["projects"]
            projects = pd.DataFrame.from_dict(projects).set_index("id")
        except KeyError:  # is this the best way to cope with times when there are no projects?
            return pd.DataFrame(columns=["id", "created"]).set_index("id")

        try:
            new_index = projects.index.astype(int)
        except ValueError:
            pass
        else:
            projects.index = new_index
        return projects

    def get_project_by_id(self, id: int) -> pd.Series:
        """Retrieve information about a project such as the title, creator, creation date and last updated date.

        Args:
            id (int): the id of the project, not to be confused with the idno.

        Returns:
            (pd.Series): project information

        Raises:
            Exception: You don't have permission to access this project - often this means the id is incorrect
        """
        #  todo(gblackadder) we could implement a get project by **idno** by using list projects and then filtering
        get_project_template = "/editor/{}"
        response = self._apinterface.get_request(get_project_template, id=id)
        return pd.Series(response["project"])

    ####################################################################################################################
    # Generic API requests
    ####################################################################################################################

    def generic_api_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json: Optional[Dict] = None,
        files: Optional[Dict[str, BufferedReader]] = None,
    ) -> Dict:
        """Make a generic API request to the Metadata Editor API.

        It's generally better to use the specific functions such as list_projects, create_project_log etc. but this
        function is provided for flexibility and to allow for future changes in the API.

        Args:
            method (str): Either 'POST' or 'GET'
            endpoint (str): The path appended to the API_URL to which a GET or POST request is sent.
            params (optional dict): additional parameters to send with a GET request.
            data (optional dict): The data to send with a POST request.
            json (optional dict): The JSON data to send with a POST request.
            files (optional dict[str, BufferedReader]): The files to send with a POST request in the form
                ```{"filename": open(filename, "rb")}```.

        Returns:
            Dict: The response from the API as a dictionary.
        """
        return self._apinterface._request(
            method=method,
            pth=endpoint,
            params=params,
            data=data,
            json=json,
            files=files,
        )

    ####################################################################################################################
    # METADATA Input and Output
    ####################################################################################################################

    def _process_metadata_input(
        self, metadata: Union[SchemaBaseModel, Dict, str], metadata_type_or_template_uid: Optional[str] = None
    ) -> Tuple[BaseModel, str, None | str]:
        """Internal function to process metadata input, converting it to a pydantic object if necessary.

        Args:
            metadata (Union[BaseModel, Dict, str]): The metadata to process.
            metadata_type_or_template_uid (Optional[str]): The metadata type or template UID. Required if metadata is a
                dictionary otherwise ignored.

        Returns:
            BaseModel: The metadata object.
            str: The metadata type.
            None | str: The template UID if the metadata is from a template, otherwise None.
        """
        if isinstance(metadata, BaseModel):
            metadata_type, uid = (
                metadata._metadata_type__
                if isinstance(metadata._metadata_type__, str)
                else metadata._metadata_type__.default,
                metadata._template_uid__
                if isinstance(metadata._template_uid__, str)
                else metadata._template_uid__.default
                if hasattr(metadata._template_uid__, "default")
                else None,
            )  # self._lookup_metadata_type_and_uid(metadata)
        elif isinstance(metadata, dict):
            if metadata_type_or_template_uid is None:
                raise ValueError("metadata_type_or_template_uid must be passed when metadata is a dictionary")
            klass, metadata_type, uid = self._get_metadata_class_and_type_and_UID(metadata_type_or_template_uid)
            metadata = klass.model_validate(metadata, strict=False)
        else:
            # if metadata_type_or_template_uid is None:
            metadata_info = self._mm.get_metadata_type_info_from_excel_file(metadata)
            metadata_type = metadata_info["metadata_type"]
            uid = metadata_info.get("template_uid", None)
            if uid is not None:
                klass = self._get_template_class_and_type_and_UID(uid)[0]
            else:
                klass = self._get_metadata_class_and_type_and_UID(metadata_type)[0]
            metadata = self._mm.read_metadata_from_excel(metadata, klass, verbose=False)
        return metadata, metadata_type, uid

    def _process_metadata_output(
        self,
        metadata_object: BaseModel,
        output_mode: str,
        filename: Optional[str] = None,
        title: Optional[str] = None,
        simplify: Optional[bool] = None,
    ) -> Union[BaseModel, Dict, str]:
        """Internal function to output metadata in a given format - dict, pydantic or excel.

        Args:
            metadata_object (BaseModel): The metadata object to output.
            output_mode (str): The output mode. Must be 'dict', 'pydantic' or 'excel'.
            filename (Optional[str]): If output_mode=='excel', the path to the Excel file.
                If None, defaults to {name of metadata type}_metadata.xlsx
            title (Optional[str]): If output_mode=='excel', the title for the Excel sheet.
                If None, defaults to '{name of metadata type} Metadata'
            simplify (Optional[bool]): If output_mode=='dict', then if simplify=True, only elements that were explicitly
                set with non-null, non-empty values are returned in the dictionary. Default behaviour is False

        Returns:
            Union[BaseModel, Dict, str]: The output metadata.
        """
        assert output_mode in DICT_MODES + EXCEL_MODES + PYDANTIC_MODES, (
            f"mode should be 'pydantic', 'dict' or 'excel' but found '{output_mode}'"
        )
        if output_mode in PYDANTIC_MODES:
            return metadata_object
        elif output_mode in DICT_MODES:
            if simplify is None:
                simplify = False
            metadata_dict = metadata_object.model_dump(mode="json", exclude_none=simplify, exclude_unset=simplify)
            if simplify:
                return remove_empty_from_dict(metadata_dict)
            else:
                return metadata_dict
        else:
            metadata_type = (
                metadata_object._metadata_type__
                if isinstance(metadata_object._metadata_type__, str)
                else metadata_object._metadata_type__.default
            )
            # metadata_type, _ = self._lookup_metadata_type_and_uid(metadata_object)
            return self._mm.save_metadata_to_excel(
                metadata_model=metadata_object,
                filename=filename,
                title=title,
                metadata_type=metadata_type,
            )

    ####################################################################################################################
    # Metadata Classes
    ####################################################################################################################

    def _get_template_class_and_type_and_UID(
        self, template_uid: str, apply_template_rules: bool = True
    ) -> Tuple[Type[BaseModel], str, str]:
        """Internal function to return the class of a given template UID, it's type and UID.

        Template rules are requirements on fields such as max_length of a string is 10 characters. We generally want
            such rules if they're specified, but OpenAI strucutured output doesn't allow for such rules so when making
            LLM calls we need to ignore rules.

        Args:
            template_uid (str): The UID of the template.
            apply_template_rules (bool): Whether to apply template rules. Defaults to True.

        Returns:
            Type[BaseModel]: The Pydantic class of the template.
            str: The metadata type, such as 'document', 'geospatial', or 'image'.
            str: The template UID.
        """
        if template_uid in self._templates and "class" in self._templates[template_uid] and apply_template_rules:
            return self._templates[template_uid]["class"], self._templates[template_uid]["metadata_type"], template_uid
        try:
            temp = self.get_template_by_uid(template_uid)
        except (KeyError, PermissionError) as e:
            # not a template either
            raise TemplateError(
                f"{template_uid} is not a known template uid - consider using an alternative template "
                f"from MetadataEditor.list_templates(limit='all')",
                response=e,
            )
        else:
            metadata_type = self._templates[template_uid]["metadata_type"]
            if "class" not in self._templates[template_uid] or apply_template_rules is False:
                try:
                    parent_schema = self._mm.metadata_class_from_name(metadata_type)
                except ValueError:
                    warnings.warn(
                        f"Could not find a metadata class for template type '{metadata_type}', UID '{template_uid}'. "
                        f"Building a class from the template without a parent schema."
                    )
                    parent_schema = SchemaBaseModel

                klass = pydantic_from_template(
                    temp.template,
                    parent_schema=parent_schema,
                    uid=template_uid,
                    name=temp.name,
                    metadata_type=metadata_type,
                    apply_rules=apply_template_rules,
                )
                if apply_template_rules:
                    self._templates[template_uid]["class"] = klass
            else:
                klass = self._templates[template_uid]["class"]
            return klass, metadata_type, template_uid

    def _get_metadata_class_and_type_and_UID(
        self, metadata_type_or_template_uid: str, apply_template_rules: bool = True
    ) -> Tuple[Type[BaseModel], str, None | str]:
        """Internal function to return the class of a given metadata type or template UID, it's type and UID.

        Template rules are requirements on fields such as max_length of a string is 10 characters. We generally want
            such rules if they're specified, but OpenAI strucutured output doesn't allow for such rules so when making
            LLM calls we need to ignore rules.

        Args:
            metadata_type_or_template_uid (str): The metadata type or template UID.
            apply_template_rules (bool): Whether to apply template rules. Defaults to True.

        Returns:
            Type[BaseModel]: The pydantic class of the metadata.
            str: The metadata type such as 'document', 'geospatial', 'image' etc.
            None | str: The template UID if the metadata is from a template, otherwise None.
        """
        try:
            metadata_type = self._mm.standardize_metadata_name(metadata_type_or_template_uid)
        except ValueError:
            # assume must be template
            return self._get_template_class_and_type_and_UID(
                metadata_type_or_template_uid, apply_template_rules=apply_template_rules
            )
        else:
            if self._default_templates is None:
                _ = self.list_templates()

            if (
                self._default_templates is not None
                and metadata_type in self._default_templates.data_type.values
                and self._default_templates[self._default_templates.data_type == metadata_type].iloc[0].uid != ""
            ):
                return self._get_template_class_and_type_and_UID(
                    self._default_templates[self._default_templates.data_type == metadata_type].iloc[0].uid,
                    apply_template_rules=apply_template_rules,
                )
            else:
                klass = self._mm.metadata_class_from_name(metadata_type)
                return klass, metadata_type, None

    def get_metadata_class(self, metadata_type_or_template_uid: str) -> Type[BaseModel]:
        """Create a pydantic class of a given metadata type or template UID.

        If a metadata type is passed then the class will be created from the default template of that type.

        Args:
            metadata_type_or_template_uid (str): The metadata type or template UID.

        Returns:
            Type[BaseModel]: The pydantic class of the metadata.

        Examples:
        ```python
        me = MetadataEditor(api_url=..., api_key=...)
        indicator_metadata_class = me.get_metadata_class("indicator")
        specific_metadata_class = me.get_metadata_class("timeseries-system-en")
        ```
        """
        return self._get_metadata_class_and_type_and_UID(
            metadata_type_or_template_uid.strip(), apply_template_rules=True
        )[0]

    def make_metadata_outline(
        self,
        metadata_type_or_template_uid: str,
        output_mode: str,
        filename: Optional[str] = None,
        title: Optional[str] = None,
    ) -> Union[Dict, BaseModel, Path]:
        """Creates a skeleton outline of a given metadata type.

        Since the metadata can be quite complex, it's useful to start with all the possible fields and their subfields.

        Args:
            metadata_type_or_template_uid (str):The type of a supported metadata type, currently:
                    document, geospatial, image, indicator, indicators_db, microdata, resource, script, table, video
                If passed as a template UID then this template is retreived and an outline created.
            output_mode (str): The type of output. Must be 'dict', 'pydantic' or 'excel'.
            filename (Optional[str]): If output_mode=='excel', the path to the Excel file.
                If None, defaults to {name of metadata type}_metadata.xlsx
            title (Optional[str]): If output_mode=='excel', the title for the Excel sheet.
                If None, defaults to '{name of metadata type} Metadata'

        Returns:
            `BaseModel` | `Dict` | `str`: If `output_mode == 'dict'`, a dictionary is returned.
                If `output_mode == 'pydantic'`, a pydantic model object is returned.
                If `output_mode == 'excel'`, the metadata was saved to a file and the filename is returned.

        Examples:
        ```python
        me = MetadataEditor(api_url=..., api_key=...)

        # using a metadata type will create an outline using the default template
        indicator_dict = me.make_metadata_outline("indicator", "dict")
        indicator_dict['metadata_information']['idno'] = "my_idno"

        # using a template uid
        indicator_pydantic = me.outline_metadata("timeseries-system-en", "pydantic")
        indicator_pydantic.metadata_information.idno = "my_idno"

        # an outline can also be written to an Excel file
        path_to_indicator_excel_file = me.outline_metadata("indicator", "excel", "indicator_outline_metadata.xlsx")
        ```
        """
        metadata_class = self.get_metadata_class(metadata_type_or_template_uid)
        # metadata_object = make_skeleton(metadata_class, debug=False)
        metadata_object = self._mm.create_metadata_outline(metadata_class)
        return self._process_metadata_output(
            metadata_object=metadata_object,
            output_mode=output_mode,
            filename=filename,
            title=title,
        )

    ####################################################################################################################
    # Retrieve Metadata
    ####################################################################################################################

    def get_project_metadata_by_id(
        self,
        id: int,
        output_mode: str,
        template_uid: Optional[str] = None,
        simplify: bool = True,
        filename: Optional[str] = None,
        title: Optional[str] = None,
        debug: bool = False,
    ) -> Union[BaseModel, Dict, str]:
        """Return the metadata as a dictionary, pydantic object or saved to an Excel file.

        Args:
            id (int): the id of the project, not to be confused with the idno.
            output_mode (str): The type of output. Must be 'dict', 'pydantic' or 'excel'.
            template_uid (Optional[str]): The UID of the template to be applied to the logged metadata if different from
                    the template already associated with the project.
                If None then the template listed in the logs will be used. And if the logs don't list a template then
                    the default template for that metadata type will be used.
                The special value 'default' can be used to apply the default template for the metadata type.
                When the output mode is 'dict' the special value 'none' can be used to remove the template from the
                    metadata and return whatever metadata was logged.
            simplify (bool): If output_mode=='dict', then if simplify=True, only elements that were explicitly set with
                non-null, non-empty values are returned in the dictionary. Default behaviour is True
            filename (Optional[str]): If output_mode=='excel' then this is the path to the Excel file.
                If None and output_mode=='excel', defaults to {name of metadata type}_metadata.xlsx
            title (Optional[str]): If output_mode=='excel' then the title for the Excel sheet.
                If None and mode=='excel', defaults to '{name of metadata type} Metadata'
            debug (bool): If True, then the function will print out some internal, intermediate output. Default False.

        Returns:
            (Union[BaseModel, Dict, str]): If mode == 'dict', a dictionary is returned. If mode == 'pydantic', a
                pydantic model object is returned. If mode == 'excel' then the metadata was saved to a file and the
                filename is returned.
        """
        output_mode = output_mode.lower().strip()
        assert output_mode in DICT_MODES + EXCEL_MODES + PYDANTIC_MODES, (
            f"mode should be 'pydantic', 'dict' or 'excel' but found '{output_mode}'"
        )

        template_uid = template_uid.lower().strip() if template_uid is not None else None
        if template_uid == "none" and output_mode not in DICT_MODES:
            raise ValueError("When template_uid='none' then output_mode must be 'dict'")

        project = self.get_project_by_id(id=id)

        if template_uid == "none":
            return project.metadata

        if template_uid == "default":
            _, _, template_uid = self._get_metadata_class_and_type_and_UID(project.type)
            if template_uid is None:
                raise ValueError(
                    f"Cannot apply default template to metadata type '{project.type}' as "
                    f"no default template is set for this type"
                )

            if template_uid == project.template_uid:
                template_uid = None

        if template_uid is not None:
            klass, _, uid = self._get_template_class_and_type_and_UID(template_uid)
            skeleton_object = self.make_metadata_outline(uid, output_mode="dict")
            validation_error_msg = (
                f"The stored metadata conflicts with the specified {project.type} template with UID '{uid}'"
            )
        elif "template_uid" in project and project.template_uid is not None and project.template_uid != "":
            assert project.template_uid.lower() != "none", (
                f"template_uid is 'none' but this should have been caught earlier, {project}"
            )
            klass, _, uid = self._get_template_class_and_type_and_UID(project.template_uid)
            skeleton_object = self.make_metadata_outline(uid, output_mode="dict")
            validation_error_msg = (
                f"The stored metadata conflicts with the assigned {project.type} template "
                f"with UID '{project.template_uid}'"
            )
        else:
            klass, metadata_type, uid = self._get_metadata_class_and_type_and_UID(project.type)
            skeleton_object = self.make_metadata_outline(metadata_type, output_mode="dict")
            validation_error_msg = f"The stored metadata conflicts with the default {project.type} template"
            if uid is not None:
                validation_error_msg += f" with UID '{uid}'"

            #### if unknown metadata type we should raise a warning and fall back to default template?
            ####   No - put the user in control - raise the error and tell them how to choose a new template.

        if debug:
            print(f"\nskeleton_object = {skeleton_object}\n")
            print(f"\nproject_metadata = {project['metadata']}\n")
        combined_dict = merge_dicts(
            skeleton_object,
            remove_empty_from_dict(project["metadata"]),
            skeleton_mode=True,
        )
        combined_dict = standardize_keys_in_dict(combined_dict)
        if debug:
            print(f"combined_dict = {combined_dict}\n")
        try:
            metadata_object = klass.model_validate(standardize_keys_in_dict(combined_dict), strict=False)
        except ValidationError as e:
            raise TemplateError(
                f"{validation_error_msg}, consider rerunning get_project_metadata_by_id with "
                f"output_mode='dict' and template_uid='none' or changing the assigned template",
                response=e,
            )

        return self._process_metadata_output(
            metadata_object=metadata_object,
            output_mode=output_mode,
            filename=filename,
            title=title,
            simplify=simplify,
        )

    ####################################################################################################################
    # Automatic Metadata Creation
    ####################################################################################################################

    def draft_metadata_from_files(
        self,
        llm_api_key: str,
        files: List[str] | str,
        output_mode: str,
        metadata_type_or_template_uid: str,
        metadata_producer_organization: Optional[str] = None,
        # prefix: Optional[str] = "?",
        filename: Optional[str] = None,
        title: Optional[str] = None,
        llm_model_name="gpt-4o",
        tokenizer_model="o200k_base",
        max_tokens=128_000,
        llm_base_url: Optional[str] = None,
        azure_llm_base_url: Optional[str] = None,
    ) -> Union[BaseModel, Dict, str]:
        """Automatically generate *draft* metadata for a project based on local files or web pages.

        The files can be:

        - PDF
        - PowerPoint
        - Word
        - Excel
        - Images
        - Audio
        - HTML
        - Text-based formats (CSV, XML)
        - ZIP files

        In the case of images and audio the files will first be passed to OpenAI for describing or transcribing.

        Args:
            llm_api_key (str): The API key for the LLM API.
            files (List[str] | str): The path to the file or a list of paths to the files from which to base metadata.
            output_mode (str): The type of output. Must be 'dict', 'pydantic' or 'excel'.
            metadata_type_or_template_uid (str): The type of metadata to create or the UID of a template to use.
            metadata_producer_organization (Optional[str]): The name of the organisation producing the metadata.
            filename (Optional[str]): If output_mode=='excel', the path to the Excel file.
                If None and output_mode=='excel', defaults to {name of metadata type}_metadata.xlsx
            title (Optional[str]): If output_mode=='excel', the title for the Excel sheet.
                If None and mode=='excel', defaults to '{name of metadata type} Metadata'
            llm_model_name (str): The model to use. Defaults to "gpt-4o". Note any model must accept a response
                format (also called structured output). Usually you should leave this to the default value.
                The option is provided in case OpenAI deprecated the 4o model.
            tokenizer_model (str): The tokenizer model to use. Defaults to "o200k_base". Note this should be the
                tokenizer corresponding to the OpenAI model used. Usually you should leave this to the default value.
                The option is provided in case OpenAI deprecated the 4o model.
            max_tokens (int): The maximum number of tokens to use when sending the content to OpenAI.
                Defaults to 128_000, which has been the typical maximum for the 4o model.
            llm_base_url (Optional[str]): The base URL for the LLM API. If None, the default URL is used which
                sends the request to OpenAI. This argument is ignored if an azure_llm_base_url is provided.
            azure_llm_base_url (Optional[str]): The base URL for the Azure LLM API. Typically used when an organization
                has its own deployment of an LLM model, possibly for privacy reasons. The Azure endpoint will be used
                even if a llm_base_url is provided. If None, then the llm_base_url endpoint is used. If
                that's also None, then OpenAI is used.

        Returns:
            (Union[BaseModel, Dict, str]): If mode == 'dict', a dictionary is returned. If mode == 'pydantic', a
                pydantic model object is returned. If mode == 'excel' then the metadata was saved to a file and the
                filename is returned.

        Example:
        ```python
        me = MetadataEditor(api_url = api_url, api_key = api_key)
        me.draft_metadata_from_files(
            llm_api_key="...",
            files=["/path/to/word_file1.docx", "http://www.example.com/report.pdf"],
            output_mode="pydantic",
            metadata_type_or_template_uid="indicator",
            metadata_producer_organization="My Organization",
            filename="output.xlsx",
            title="My Metadata",
        )

        # Example with a local model running on Ollama:
        me.draft_metadata_from_files(
            llm_api_key="ollama",  # pragma: allowlist secret
            files=["/path/to/word_file1.docx", "http://www.example.com/report.pdf"],
            output_mode="pydantic",
            metadata_type_or_template_uid="indicator",
            metadata_producer_organization="My Organization",
            filename="output.xlsx",
            title="My Metadata",
            llm_base_url="http://localhost:11434/v1/",
            llm_model_name="llama3.1"
        )

        # Example with an Azure instance of a Large Language Model:
        me.draft_metadata_from_files(
            llm_api_key="...",
            files=["/path/to/word_file1.docx", "http://www.example.com/report.pdf"],
            output_mode="pydantic",
            metadata_type_or_template_uid="indicator",
            metadata_producer_organization="My Organization",
            filename="output.xlsx",
            title="My Metadata",
            azure_llm_base_url="https://my-azure-openai-resource.openai.azure.com/",
        )
        ```
        """
        #  prefix (Optional[str]): A prefix to add to the metadata. Defaults to '?'. If None, no prefix is added.

        metadata_class_no_rules, metadata_type, _ = self._get_metadata_class_and_type_and_UID(
            metadata_type_or_template_uid, apply_template_rules=False
        )
        enc = tiktoken.get_encoding(tokenizer_model)
        if azure_llm_base_url is None:
            client = OpenAI(api_key=llm_api_key, base_url=llm_base_url)
        else:
            client = AzureOpenAI(api_key=llm_api_key, base_url=azure_llm_base_url, api_version="2024-10-01")

        system_prompt = f"You are an expert on producing {metadata_type} documentation. "
        system_prompt += (
            "Based on the user content, write project metadata. "
            "If you are unsure about the correct metadata values, leave them blank. "
            "Do not guess. Accuracy is more important than completeness. "
        )

        # "You are an expert on survey microdata documentation. Based on the user content alone, write project metadata.
        # If you are unsure about the correct metadata values, leave them blank. Do not guess. Accuracy is more
        # important than completeness."},

        messages = [
            {"role": "system", "content": system_prompt},
        ]

        md = MarkItDown(llm_client=client, llm_model=llm_model_name)

        if isinstance(files, str):
            files = [files]

        out = f"The metadata is being produced today, {get_date_as_text()}."
        if metadata_producer_organization is not None:
            out += f" The metadata is being produced by {metadata_producer_organization}.\n\n"
        for doc in files:
            out += "################################################\n\n"
            out += f"# {doc}\n\n"
            out += md.convert(doc).text_content + "\n\n"
            user_message = [{"role": "user", "content": out}]
            num_tokens = len(enc.encode(messages[0]["content"]) + enc.encode(user_message[0]["content"]))
            if num_tokens > max_tokens:
                warnings.warn(
                    f"Caution - after importing {doc} the token count will be {num_tokens} which exceeds the maximum of"
                    f" {max_tokens}, truncating the content and proceeding."
                )
            else:
                print(f"Reading {doc}, running token count is {num_tokens}")
        messages += user_message

        endpoint_name = (
            azure_llm_base_url if azure_llm_base_url is not None else "OpenAI" if llm_base_url is None else llm_base_url
        )
        print(f"Sending to {endpoint_name}, this may take a few minutes...")
        try:
            completion = client.beta.chat.completions.parse(
                model=llm_model_name,
                messages=messages,
                response_format=metadata_class_no_rules,
            )

            message = completion.choices[0].message
            if not message.parsed:
                raise ValueError(message.refusal)

            metadata_dict = message.parsed.model_dump(exclude_none=True, exclude_unset=True)
        except ValidationError:
            metadata_dict = call_per_field(metadata_class_no_rules, client, llm_model_name, messages).model_dump(
                exclude_none=True, exclude_unset=True
            )
        # if prefix:
        #     metadata_dict = self._prepend_draft_drop_non_str(metadata_dict, prefix)
        metadata_class_with_rules = self.get_metadata_class(metadata_type_or_template_uid)
        metadata_with_rules = _iterated_validated_update_to_outline(metadata_class_with_rules, metadata_dict)

        return self._process_metadata_output(
            metadata_object=metadata_with_rules,
            output_mode=output_mode,
            filename=filename,
            title=title,
        )

    def augment_metadata_from_files(
        self,
        input_metadata: Union[BaseModel, Dict, str],
        llm_api_key: str,
        files: List[str] | str,
        output_mode: str,
        metadata_type_or_template_uid: Optional[str] = None,
        metadata_producer_organization: Optional[str] = None,
        prefix: Optional[str] = None,
        filename: Optional[str] = None,
        title: Optional[str] = None,
        llm_model_name="gpt-4o",
        tokenizer_model="o200k_base",
        max_tokens=128_000,
        llm_base_url: Optional[str] = None,
        azure_llm_base_url: Optional[str] = None,
    ) -> Union[BaseModel, Dict, str]:
        """Augment existing metadata with information from files or web pages.

        Since the metadata is being augmented, the new metadata can be given a prefix to indicate it is new.

        Args:
            input_metadata (Union[BaseModel, Dict, str]): The existing metadata to augment. Can be a dictionary, a
                pydantic model or a path to an Excel file.
            llm_api_key (str): The API key for the LLM API.
            files (List[str] | str): The path to the file or a list of paths to the files from which to base metadata.
            output_mode (str): The type of output. Must be 'dict', 'pydantic' or 'excel'.
            metadata_type_or_template_uid (Optional[str]): The type of metadata to create or the UID of a template to
                use. If None then the type will be inferred from the input_metadata.
            metadata_producer_organization (Optional[str]): The name of the organisation producing the metadata.
            prefix (Optional[str]): A prefix to add to the new metadata. If None, no prefix is added.
            filename (Optional[str]): If output_mode=='excel', the path to the Excel file.
                If None and output_mode=='excel', defaults to {name of metadata type}_metadata.xlsx
            title (Optional[str]): If output_mode=='excel', the title for the Excel sheet.
                If None and mode=='excel', defaults to '{name of metadata type} Metadata'
            llm_model_name (str): The OpenAI model to use. Defaults to "gpt-4o". Note any model must accept a response
                format (also called structured output). Usually you should leave this to the default value.
                The option is provided in case OpenAI deprecated the 4o model.
            tokenizer_model (str): The tokenizer model to use. Defaults to "o200k_base". Note this should be the
                tokenizer corresponding to the OpenAI model used. Usually you should leave this to the default value.
                The option is provided in case OpenAI deprecated the 4o model.
            max_tokens (int): The maximum number of tokens to use when sending the content to OpenAI.
                Defaults to 128_000, which has been the typical maximum for the 4o model.
            llm_base_url (Optional[str]): The base URL for the LLM API. If None, the default URL is used which
                sends the request to OpenAI.
            azure_llm_base_url (Optional[str]): The base URL for the Azure LLM API. Typically used when an organization
                has its own deployment of an LLM model, possibly for privacy reasons. The Azure endpoint will be used
                even if a llm_base_url is provided. If None, then the llm_base_url endpoint is used. If
                that's also None, then OpenAI is used.

        Returns:
            Union[BaseModel, Dict, str]: The augmented metadata.

        Example:
        ```python
        me = MetadataEditor(api_url=..., api_key=...)

        # augment existing metadata with information from files
        me.augment_metadata_from_files(
            input_metadata=my_indicator_metadata,
            llm_api_key="...",
            files=["/path/to/word_file1.docx", "http://www.example.com/report.pdf"],
            output_mode="pydantic",
            metadata_producer_organization="My Organization",
            prefix="<AI>"
        )

        # Example with an Azure instance of a Large Language Model:
        me.augment_metadata_from_files(
            input_metadata=my_indicator_metadata,
            llm_api_key="...",
            files=["/path/to/word_file1.docx", "http://www.example.com/report.pdf"],
            output_mode="pydantic",
            metadata_producer_organization="My Organization",
            prefix="<AI>",
            azure_llm_base_url="https://my-azure-openai-resource.openai.azure.com/",
        )
        ```
        """
        #  prefix (Optional[str]): A prefix to add to the metadata. Defaults to '?'. If None, no prefix is added.

        if isinstance(input_metadata, str):
            input_metadata = pd.read_excel(input_metadata, sheet_name=0).to_dict(orient="records")[0]

        metadata_type_or_template_uid = self._process_metadata_input(input_metadata, metadata_type_or_template_uid)[2]

        if metadata_type_or_template_uid is None:
            raise ValueError("metadata_type_or_template_uid must be passed when input_metadata is a dictionary")

        old_metadata = self.change_mode_or_template(
            input_metadata, output_mode="dict", input_template_uid=metadata_type_or_template_uid, simplify=True
        )

        klass = self.get_metadata_class(metadata_type_or_template_uid)

        old_metadata = _iterated_validated_update_to_outline(klass, updates=old_metadata)

        old_metadata = self.change_mode_or_template(old_metadata, output_mode="dict", simplify=True)
        old_metadata_md = "# Previously written metadata\n\n"
        old_metadata_md += json_to_markdown(old_metadata, level=2)

        with NamedTemporaryFile(delete=True, suffix=".txt") as f:
            f.write(old_metadata_md.encode("utf-8"))
            f.flush()

        if metadata_type_or_template_uid is None:
            if isinstance(input_metadata, dict):
                raise ValueError("metadata_type_or_template_uid must be passed when input_metadata is a dictionary")

            _, _, metadata_type_or_template_uid = self._process_metadata_input(
                input_metadata, metadata_type_or_template_uid
            )

        old_metadata = self.change_mode_or_template(
            input_metadata, output_mode="dict", input_template_uid=metadata_type_or_template_uid, simplify=True
        )

        klass = self.get_metadata_class(metadata_type_or_template_uid)

        old_metadata = _iterated_validated_update_to_outline(klass, updates=old_metadata)

        old_metadata = self.change_mode_or_template(old_metadata, output_mode="dict", simplify=True)
        old_metadata_md = "# Prevsiouly written metadata\n\n"
        old_metadata_md += json_to_markdown(old_metadata, level=2)

        with NamedTemporaryFile(delete=True, suffix=".txt") as f:
            f.write(old_metadata_md.encode("utf-8"))
            f.flush()  # Ensure the content is written to disk
            file_path = f.name

            if isinstance(files, str):
                files = [files]
            files = [file_path] + files

            new_metadata = self.draft_metadata_from_files(
                llm_api_key=llm_api_key,
                files=files,
                metadata_type_or_template_uid=metadata_type_or_template_uid,
                metadata_producer_organization=metadata_producer_organization,
                output_mode="dict",
                # prefix=prefix,
                filename=None,
                title=None,
                llm_model_name=llm_model_name,
                tokenizer_model=tokenizer_model,
                max_tokens=max_tokens,
                llm_base_url=llm_base_url,
                azure_llm_base_url=azure_llm_base_url,
            )

        if new_metadata is None or len(new_metadata) == 0:
            raise ValueError("No metadata was generated from the files.")

        if prefix:
            new_metadata = _prepend_draft_drop_non_str(new_metadata, prefix=prefix)

        combined_metadata = merge_dicts(old_metadata, new_metadata)

        metadata_object = _iterated_validated_update_to_outline(klass, updates=combined_metadata)
        return self._process_metadata_output(
            metadata_object=metadata_object,
            output_mode=output_mode,
            filename=filename,
            title=title,
        )

    ####################################################################################################################
    # Log and Update Metadata
    ####################################################################################################################

    def create_project_log(
        self, metadata: Union[BaseModel, Dict, str], metadata_type_or_template_uid: Optional[str] = None
    ) -> int:
        """Validates and logs metadata which can be a dictionary, a pydantic model or a path to an Excel spreadsheet.

        Args:
            metadata (dictionary or BaseModel or str): If str, it's assumed this is a path to an appropriately
                formatted Excel file.
            metadata_type_or_template_uid (str): If passing in a simple type then the supported types are:
                    document, geospatial, image, indicator, indicators_db, microdata, resource, script, table, video
                In this case we will use the default template for that metadata type.
                Alternatively you can pass in the UID of a template. This is required if the metadata is a dictionary
                    otherwise the UID associated with the pydantic model or the Excel file will be used.

        Returns:
            int: The ID of the newly created document metadata
        """
        metadata, metadata_type, uid = self._process_metadata_input(metadata, metadata_type_or_template_uid)

        if metadata_type == "indicator":
            metadata_type = "timeseries"
        elif metadata_type == "indicators_db":
            metadata_type = "timeseries_db"
        elif metadata_type == "microdata":
            metadata_type = "survey"
        post_request_pth = f"/editor/create/{metadata_type.replace('_', '-')}"
        ret = self._apinterface.post_request(
            pth=post_request_pth,
            json=remove_empty_from_dict(metadata.model_dump(mode="json", exclude_none=True, exclude_unset=True)),
        )
        return ret["id"]

    # def log_project_admin_metadata(
    #         self, id: int, metadata: Union[BaseModel, Dict, str], metadata_type_or_template_uid: Optional[str] = None
    # ) -> int:
    #     """Validates and logs admin metadata which can be a dictionary, a pydantic model or a path to an Excel file.

    #     Args:
    #         id (int): The ID of the project to associate the metadata with.
    #         metadata (dictionary or BaseModel or str): If str, it's assumed this is a path to an appropriately
    #             formatted Excel file.
    #         admin_metadata_template_uid (str, optional): The UID of the admin metadata template to use.
    #             otherwise the UID associated with the pydantic model or the Excel file will be used.

    #     Returns:
    #         int: The ID of the newly created admin metadata
    #     """
    #     metadata, metadata_type, uid = self._process_metadata_input(metadata, metadata_type_or_template_uid)
    #     post_request_pth = "admin-metadata/data/"
    #     post_json = {
    #         "project_id": id,
    #         "template_uid": uid,
    #         "metadata": remove_empty_from_dict(metadata.model_dump(mode="json",
    #                                                                exclude_none=True,
    #                                                                exclude_unset=True)),
    #     }
    #     ret = self._apinterface.post_request(
    #         pth=post_request_pth,
    #         json=post_json,
    #         id=id,
    #     )
    #     return ret

    def update_project_log_by_id(self, id: int, new_metadata: Union[BaseModel, Dict, str]):
        """Updates the record of the metadata.

        If a dictionary is passed that only contains a subset of the possible keys then the remaining values not
        mentioned are left as is.

        Args:
            id (int): The ID of the metadata to update.
            new_metadata (dictionary, BaseModel or str): If str, it's assumed this is a path to an appropriately
                formatted Excel file
        """
        project_data = self.get_project_by_id(id)
        try:
            project_type = self._mm.standardize_metadata_name(project_data["type"])
        except ValueError as e:
            raise ValueError(
                f"Unknown metadata type {project_data['type']}. The metadata type is required to "
                f"set the metadata API endpoint path, therefore we cannot update the metadata."
            ) from e

        if (
            "template_uid" in project_data
            and project_data["template_uid"] is not None
            and project_data["template_uid"] != ""
        ):
            project_uid = project_data["template_uid"]
            metadata_type_or_template_uid = project_uid
        else:
            project_uid = None
            metadata_type_or_template_uid = project_type

        if not isinstance(new_metadata, dict):
            if isinstance(new_metadata, BaseModel):
                metadata_type = (
                    new_metadata._metadata_type__
                    if isinstance(new_metadata._metadata_type__, str)
                    else new_metadata._metadata_type__.default
                )
                uid = (
                    new_metadata._template_uid__
                    if isinstance(new_metadata._template_uid__, str)
                    else new_metadata._template_uid__.default
                    if hasattr(new_metadata._template_uid__, "default")
                    else None
                )
            else:
                metadata_info = self._mm.get_metadata_type_info_from_excel_file(new_metadata)
                metadata_type = metadata_info["metadata_type"]
                uid = metadata_info.get("template_uid", None)
            if uid is not None and project_uid != uid:
                raise ValueError(
                    f"The template UID of the existing project is {project_uid} but the template UID "
                    f"of the new metadata is {uid}.\n"
                    f"The template of the new metadata should be changed to match the existing project "
                    f"uid='{project_uid}' or change the template of the existing project to match the new metadata "
                    f"uid='{uid}'."
                )
            elif uid is None and metadata_type != project_type:
                raise ValueError(
                    f"The metadata type of the existing project is {project_type} but the metadata type "
                    f"of the new metadata is {metadata_type}."
                )

        metadata, metadata_type, uid = self._process_metadata_input(new_metadata, metadata_type_or_template_uid)

        if project_type != metadata_type:
            raise ValueError(
                f"The metadata type of the existing project is {project_type} but the metadata type "
                f"of the new metadata is {metadata_type}."
            )

        if uid is not None and project_uid is not None and project_uid != uid:
            raise ValueError(
                f"The template UID of the existing project is {project_uid} but the template UID "
                f"of the new metadata is {uid}.\n"
                "This could cause issues if the templates are incompatible.\n"
                f"You should change the template of the new metadata to match the existing project "
                f"uid='{project_uid}' or change the template of the existing project to match the new metadata "
                f"uid='{uid}'."
            )

        metadata = remove_empty_from_dict(metadata.model_dump(mode="json", exclude_none=True, exclude_unset=True))

        if metadata_type == "indicator":
            metadata_type = "timeseries"
        elif metadata_type == "indicators_db":
            metadata_type = "timeseries_db"
        elif metadata_type == "microdata":
            metadata_type = "survey"
        post_request_template_path = f"/editor/update/{metadata_type.replace('_', '-')}/" + "{}"
        self._apinterface.post_request(
            post_request_template_path,
            id=id,
            json=metadata,
        )

    def patch_update_project_log_by_id(self, id: int, op: str, path: str, value: Optional[str] = None):
        """Add, update, or remove parts of a project's metadata using a single JSON Patch operation.

        "JSON Patch is a format for describing changes to a JSON document. It can be used to avoid sending a whole
        document when only a part has changed." - https://jsonpatch.com/ accessed 2024-08-20

        This method applies a single JSON Patch operation to update the metadata of a project specified by its ID.

        JSON Patch Operations:

        - "add": Adds a value to the specified path. If the path already exists, the value is replaced.
        - "remove": Removes the value at the specified path.
        - "replace": Replaces the value at the specified path with a new value.
        - "test": Tests that the specified path contains the given value.

        The `path` is a string that uses a slash (`/`) notation to specify the location within the JSON document.
        For example, `/author` refers to the "author" field, and `/metadata/title` refers to the "title" field
        inside the "metadata" object. If the path does not start with a `/`, the method will automatically
        prepend it.

        Args:
            id (int): The unique identifier of the project whose metadata is to be updated.
            op (str): The JSON Patch operation to be applied. Valid operations are "add", "remove",
                "replace", and "test".
            path (str): The path in the project's metadata where the operation will be applied, using JSON
                Pointer notation.
            value (Optional[str]): The value to be added, replaced, or tested. Not required for "remove" operations.

        Raises:
            ValueError: If the provided operation, path, or value is invalid.

        Example:
        ```python
        me = MetadataEditor(api_url = api_url, api_key = api_key)

        # set the author of the project with ID 123 to "John Doe"
        me.patch_update_project_log_by_id(id=123, op="add", path="/author", value="John Doe")

        # test that the author is "John Doe"
        me.patch_update_project_log_by_id(id=123, op="test", path="/author", value="John Doe")

        # change the author to "Jane Doe"
        me.patch_update_project_log_by_id(id=123, op="replace", path="/author", value="Jane Doe")

        # remove the value of author
        me.patch_update_project_log_by_id(id=123, op="remove", path="/author")
        ```
        """
        project_data = self.get_project_by_id(id)
        metadata_name = project_data["type"]
        pth = f"editor/patch/{metadata_name}/"

        patches = {"op": op, "path": path}
        if value is not None:
            patches["value"] = value
        if isinstance(patches, dict):
            patches = [patches]
        patches = validate_json_patches(patches)  # could instead only depend on serverside validation...
        self._apinterface.post_request(pth=pth + "{}", id=id, json={"patches": patches, "validate": False})

    ####################################################################################################################
    # TEMPLATES
    ####################################################################################################################

    def list_templates(self) -> pd.DataFrame:
        """Retrieves templates, both standard and any custom templates.

        Returns:
            pd.DataFrame: A DataFrame containing the templates. If none are found, an empty DataFrame is returned.
        """
        response = self._apinterface.get_request("templates")
        if "templates" not in response or len(response["templates"]) == 0:
            return pd.DataFrame([], columns=["uid", "template_type", "name", "template"])
        else:
            templates = pd.DataFrame([v_item for _, v in response["templates"].items() for v_item in v])
            if "default" in templates and "uid" in templates and "data_type" in templates:
                self._default_templates = (
                    templates[templates.default].drop_duplicates("uid").drop_duplicates("data_type")
                )

                # in place replace each value of data_type with the standardised version
                def standardize(row):
                    try:
                        return self._mm.standardize_metadata_name(row["data_type"])
                    except ValueError:
                        return row["data_type"]

                self._default_templates["data_type"] = self._default_templates.apply(standardize, axis=1)

            try:
                new_index = templates.index.astype(int)
            except ValueError:
                pass
                templates.index = new_index
            return templates

    def get_template_by_uid(self, uid: str) -> pd.Series:
        """Retrieves given template by *UID*, not id.

        Args:
            uid (str): The Unique Identifier of the template to retrieve.

        Returns:
            pd.Series: A pandas Series containing the template details.
        """
        if uid in self._templates:
            return self._templates[uid]["template"]
        response = self._apinterface.get_request("templates/{}", uid)
        if "result" not in response:
            raise KeyError(f"No result returned.\nResponse: {response}")

        temp = pd.Series(response["result"], name=response["result"]["name"])
        try:
            standard_type_name = self._mm.standardize_metadata_name(temp.data_type)
        except ValueError:
            standard_type_name = temp.data_type
        self._templates[uid] = {"template": temp, "metadata_type": standard_type_name}
        try:
            try:
                parent_schema = self._mm.metadata_class_from_name(temp.data_type)
            except ValueError:
                warnings.warn(
                    f"Could not find a metadata class for template type '{standard_type_name}', UID '{uid}'. "
                    f"Building a class from the template without a parent schema."
                )
                parent_schema = SchemaBaseModel
            klass = pydantic_from_template(
                temp.template, parent_schema=parent_schema, uid=uid, name=temp.name, metadata_type=standard_type_name
            )
            self._templates[uid]["class"] = klass
        finally:
            return temp

    def change_mode_or_template(
        self,
        metadata: Union[BaseModel, Dict, str],
        output_mode: str,
        output_template_uid: Optional[str] = None,
        input_template_uid: Optional[str] = None,
        filename: Optional[str] = None,
        title: Optional[str] = None,
        simplify: Optional[bool] = None,
    ) -> Union[BaseModel, Dict, str]:
        """Change the mode or template of a metadata object.

        In terms of modes, you can convert
            - a dict to a pydantic model, or vice versa,
            - a dict to an Excel file, or vice versa,
            - a pydantic model to an Excel file, or vice versa

        And in terms of templates, you can convert a metadata object from one template to another.

        Args:
            metadata (Union[BaseModel, Dict, str]): The metadata to process.
            output_mode (str): The output mode. Must be 'dict', 'pydantic' or 'excel'.
            output_template_uid (Optional[str]): The UID of the new template. If None then the existing template is
                used.
            input_template_uid (Optional[str]): The UID of the input template. Required if the metadata is a dictionary.
                Ignored if metadata is a pydantic model or a path to an Excel file.
            filename (Optional[str]): If output_mode=='excel', the path to the Excel file.
                If None, defaults to {name of metadata type}_metadata.xlsx
            title (Optional[str]): If output_mode=='excel', the title for the Excel sheet.
                If None, defaults to '{name of metadata type} Metadata'
            simplify (Optional[bool]): If output_mode=='dict', then if simplify=True, only elements that were explicitly
                set with non-null, non-empty values are returned in the dictionary. Default behaviour is False

        Returns:
            Union[BaseModel, Dict, str]: The updated metadata object.
        """
        metadata, metadata_type, uid = self._process_metadata_input(metadata, input_template_uid)

        if not (output_template_uid is None or output_template_uid == uid):
            new_klass, new_type, _ = self._get_metadata_class_and_type_and_UID(output_template_uid)
            try:
                # metadata = new_klass.model_validate(
                #     remove_empty_from_dict(metadata.model_dump(mode="json", exclude_none=True, exclude_unset=True)),
                #     strict=False,
                # )
                metadata = _iterated_validated_update_to_outline(
                    new_klass, updates=metadata.model_dump(mode="json", exclude_none=True, exclude_unset=True)
                )
            except ValidationError as e:
                raise TemplateError(
                    f"Could not coerce metadata from the {metadata_type} template with UID "
                    f"'{input_template_uid}' to {new_type} template with UID '{output_template_uid}'",
                    e,
                )
            if metadata_type != new_type:
                warnings.warn(
                    f"The metadata type of the logged project is {metadata_type} but the metadata type "
                    f"of the new template is {new_type}, which could lead to data loss."
                )

        return self._process_metadata_output(
            metadata_object=metadata,
            output_mode=output_mode,
            filename=filename,
            title=title,
            simplify=simplify,
        )

    ####################################################################################################################
    # EXCEL INTERFACE
    ####################################################################################################################

    def save_metadata_to_excel(
        self,
        metadata_model: BaseModel | dict | str,
        metadata_type_or_template_uid: Optional[str] = None,
        filename: Optional[str] = None,
        title: Optional[str] = None,
    ) -> str:
        """Save a metadata object to an Excel file.

        Args:
            metadata_model (BaseModel|dict|str): The pydantic object, python dictionary or path to an Excel file.
            metadata_type_or_template_uid (Optional[str]): If the metadata is a dictionary, this is the UID of the
                template to use. Ignored if metadata is a pydantic model or a path to an Excel file.
            filename (Optional[str]): The path to the output Excel file. Defaults to {name}_metadata.xlsx
            title (Optional[str]): The title for the output Excel sheet. Defaults to '{name} Metadata'

        Returns:
            str: The path to the saved Excel file.
        """
        processed_model = self._process_metadata_input(
            metadata_model, metadata_type_or_template_uid=metadata_type_or_template_uid
        )[0]
        return self._process_metadata_output(
            metadata_object=processed_model, output_mode="excel", filename=filename, title=title
        )

    def read_metadata_from_excel(
        self,
        filename: str,
        output_mode: str = "pydantic",
        exclude_unset=True,
    ) -> Union[BaseModel, Dict]:
        """Read metadata from an Excel file.

        Args:
            filename (str): The path to the Excel file.
            output_mode (str): The output mode. Must be 'pydantic' or 'dict'.
            exclude_unset (bool): If mode=='dict', then if exclude_unset=True, only elements that were explicitly set
                with non-null, non-empty values are returned in the dictionary.

        Returns:
            Union[BaseModel, Dict]: The metadata object or dictionary.
        """
        assert output_mode not in EXCEL_MODES, (
            f"read_metadata_from_excel output_mode should be 'pydantic' or 'dict' but found '{output_mode}'"
        )
        object = self._process_metadata_input(filename)[0]
        return self._process_metadata_output(object, output_mode, simplify=exclude_unset)

    ####################################################################################################################
    # COLLECTION METHODS
    ####################################################################################################################

    def list_collections(self) -> pd.DataFrame:
        """Lists all the collections associated with your API key.

        Returns:
            pd.DataFrame: Collection information
        """
        response = self._apinterface.get_request("collections")
        if "collections" not in response or len(response["collections"]) == 0:
            return pd.DataFrame([], columns=["id", "title", "created"]).set_index("id")
        df = pd.DataFrame(response["collections"]).set_index("id")
        try:
            new_index = df.index.astype(int)
        except ValueError:
            pass
        else:
            df.index = new_index
        return df

    def get_collection_by_id(self, id: int) -> pd.Series:
        """Get information about a collection like title, description, created date.

        Args:
            id (int): the id of the collection.

        Returns:
            (pd.Series): a pandas series of the collection information

        Raises:
            Exception: You don't have permission to access this project - often this means the id is incorrect
        """
        collection_data = self._apinterface.get_request("collections/{}", id=id)
        if "collection" not in collection_data:
            raise ValueError(f"API call was good but collection data missing from: {collection_data}")
        return pd.Series(collection_data["collection"])

    def create_collection(self, title: str, description: str):
        """Creates a new collection with the specified title and description.

        Args:
            title (str): The title of the collection.
            description (str): The description of the collection.

        Returns:
            (int): The id of the newly created collection
        """
        assert title != "", "The collection must have a title but an empty string was passed"
        ret = self._apinterface.post_request("collections", json={"title": title, "description": description})
        return ret["collection"]

    def update_collection(self, id: int, title: Optional[str] = None, description: Optional[str] = None):
        """Updates the specified collection with a new title and/or description.

        Args:
            id (int): The unique identifier of the collection to update.
            title (Optional[str]): The new title of the collection. Defaults to None.
            description (Optional[str]): The new description of the collection. Defaults to None.

        Raises:
            Assertion Error: if both title and description are None, since we must update one or the other.
        """
        # Is it clear this updates title/description of the collection and not the data in the collection?
        assert title is not None or description is not None, "can update title or description or both, but not neither"
        metadata = {}
        if title is not None:
            metadata["title"] = title
        if description is not None:
            metadata["description"] = description
        self._apinterface.post_request("collections/update/{}", id=id, json=metadata)

    def copy_collection(self, source_id: int, target_id: int):
        """Copy projects and users from one collection to another.

        Args:
            source_id (int): The ID of the source collection.
            target_id (int): The ID of the target collection.

        """
        self._apinterface.post_request("collections/copy/", json={"source_id": source_id, "target_id": target_id})

    def move_collection(self, source_id, target_id):
        """Move source collection to be a sub-collection of the target collection.

        Args:
            source_id (int): The ID of the source collection.
            target_id (int): The ID of the target collection.

        """
        self._apinterface.post_request("collections/move/", json={"source_id": source_id, "target_id": target_id})

    def count_projects_in_collection(self, collection: int) -> int:
        """Count the number of projects you have access to.

        Args:
            collection (int):
                The id of the collection.

        Returns:
            int: The number of projects
        """
        params = {"offset": 0, "limit": 1}
        response = self._apinterface.get_request("editor?collection={}", id=collection, params=params)
        return response["total"]

    def list_projects_in_collection(
        self,
        collection: int,
        limit: Union[int, str],
        keywords: Optional[Union[str, List[str]]] = None,
        offset: int = 0,
        sort_by: Optional[str] = None,
    ) -> pd.DataFrame:
        """Retrieve projects that have been added to the given collection.

        Args:
            collection (int): The id of the collection.
            limit (int): The maximum number of projects to return. If limit='All' then all records are retrieved.
            keywords (optional str or list of str):  filter projects based on whether the project title or idno contains
                this keyword
            offset (int): Offset for pagination e.g. 10 to skip first 10 records. Default is 0.
            sort_by (optional str): valid values: "title_asc", "title_desc", "updated_asc", "updated_desc".

        Returns:
            pd.DataFrame: Information on the projects in the collection, such as id, idno, title and type.
        """
        if isinstance(limit, str):
            assert limit.lower() == "all", f"Expected limit to be 'all' or a positive integer but got '{limit}'"
            new_offset = offset
            new_limit = 500
            dfs = []
            while True:
                df = self.list_projects_in_collection(
                    collection=collection, keywords=keywords, offset=new_offset, limit=new_limit, sort_by=sort_by
                )
                dfs.append(df)
                if len(df) < new_limit:
                    break
                new_offset += new_limit
            return pd.concat(dfs)

        params = {"limit": limit, "offset": offset}
        if keywords is not None:
            if not isinstance(keywords, str) and isinstance(keywords, Iterable):
                keywords = "%".join(keywords)
            keywords = keywords.replace(" ", "%")
            params["keywords"] = keywords
        if sort_by is not None:
            sort_by = sort_by.lower()
            valid_sort_by = ["title_asc", "title_desc", "updated_asc", "updated_desc"]
            assert sort_by in valid_sort_by, f"{sort_by} not valid, must be one of {valid_sort_by}"
            params["sort_by"] = sort_by
        ret = self._apinterface.get_request("editor?collection={}", id=collection, params=params)
        if len(ret["projects"]) == 0:
            return pd.DataFrame([], columns=["id", "type", "idno", "title"]).set_index("id")
        df = pd.DataFrame(ret["projects"]).set_index("id")

        try:
            new_index = df.index.astype(int)
        except ValueError:
            pass
        else:
            df.index = new_index
        return df

    def add_projects_to_collection(
        self, collection: Union[int, List[int]], id_format: str, projects: Union[int, List[int], str, List[str]]
    ):
        """Adds project or projects to specified collection or collections.

        This method associates one or more projects with one or more collections. The `collection`
        parameter can be a single collection ID or a list of collection IDs. The `projects` parameter
        can be a single project ID, a single project ID number (idno), a list of project IDs, or a list
        of project idnos. The `id_format` parameter specifies whether the project identifiers
        are in the form of IDs (integer) or idno (string).

        Args:
            collection : Union[int, List[int]]
                A single collection ID or a list of collection IDs to which projects should be added.
            id_format : str
                Specifies the format of the project identifiers. Must be either 'id' or 'idno'.
            projects : Union[int, List[int], str, List[str]]
                A single project ID, a single project idno, a list of project IDs, or a list of
                project idnos to be added to the specified collection(s).

        Example:
        ```python
        me = MetadataEditor(api_url = api_url, api_key = api_key)
        me.add_projects_to_collection(collection=1, id_format='id', projects=[101, 102])
        me.add_projects_to_collection(collection=[1, 2], id_format='idno', projects=['A101', 'A102'])
        ```
        """
        assert id_format.lower() in ["id", "idno"], f"id_format must be either 'id' or 'idno' but got '{id_format}'"
        if not isinstance(collection, Iterable) or isinstance(collection, str):
            collection = [collection]

        if not isinstance(projects, Iterable) or isinstance(projects, str):
            projects = [projects]
        if id_format.lower() == "id":
            for proj in projects:
                assert isinstance(proj, int), f"When passing ids the projects must be ints, but found: {proj}"
        else:
            for proj in projects:
                assert isinstance(proj, str), f"While passing idnos the projects must be strs but found: {proj}"
        self._apinterface.post_request(
            "collections/add_projects",
            json={"collections": collection, "id_format": id_format, "projects": projects},
        )

    def remove_projects_from_collection(
        self, collection: Union[int, List[int]], id_format: str, projects: Union[int, List[int], str, List[str]]
    ):
        """Removes project or projects from specified collection or collections.

        This method dissociates one or more projects from one or more collections. The `collection`
        parameter can be a single collection ID or a list of collection IDs. The `projects` parameter
        can be a single project ID, a single project ID number (idno), a list of project IDs, or a list
        of project idnos. The `id_format` parameter specifies whether the project identifiers
        are in the form of IDs or idnos.

        Note that if the project(s) are not in the collection there is no error raised since either way the project
            will not be in the collection after this function executes

        Args:
            collection : Union[int, List[int]]
                A single collection ID or a list of collection IDs to which projects should be removed.

            id_format : str
                Specifies the format of the project identifiers. Must be either 'id' or 'idno'.

            projects : Union[int, List[int], str, List[str]]
                A single project ID, a single project idno, a list of project IDs, or a list of
                project idnos to be removed from the specified collection(s).

        Raises:
            AssertionError: If `id_format` is not 'id' or 'idno'.
                If a project ID is not an integer when `id_format` is 'id'.
                If a project ID number is not a string when `id_format` is 'idno'.


        Example:
        ```python
        me = MetadataEditor(api_url = api_url, api_key = api_key)
        me.remove_projects_from_collection(collection=1, id_format='id', projects=[101, 102])

        me.remove_projects_from_collection(collection=[1, 2], id_format='idno', projects=['A101', 'A102'])
        ```
        """
        assert id_format.lower() in ["id", "idno"], f"id_format must be either 'id' or 'idno' but got '{id_format}'"
        if not isinstance(projects, Iterable) or isinstance(projects, str):
            projects = [projects]
        if id_format.lower() == "id":
            for proj in projects:
                assert isinstance(proj, int), f"When passing ids the projects must be ints, but found: {proj}"
        else:
            for proj in projects:
                assert isinstance(proj, str), f"While passing idnos the projects must be strs but found: {proj}"

        self._apinterface.post_request(
            "collections/remove_projects",
            json={"collections": collection, "id_format": id_format, "projects": projects},
        )

    def set_template_for_collection(self, collection_id: int, template_uid: str):
        """Set the specified template to be used for all metadata of its type to a collection.

        Args:
            collection_id (int): the id of the collection.
            template_uid (str): The Unique Identifier of the template to apply to the collection.
        """
        # check collection exists
        self.get_collection_by_id(collection_id)
        template = self.get_template_by_uid(uid=template_uid)
        template_type = template["data_type"]
        self._apinterface.post_request(
            "collections/template",
            json={"collection_id": collection_id, "template_uid": template_uid, "project_type": template_type},
        )

    ####################################################################################################################
    # RESOURCE METHODS
    ####################################################################################################################

    def get_resources_by_id(self, id: int) -> pd.DataFrame:
        """List documentation (Reports, Questionnaires, Tables, etc.) for a project.

        Args:
            id (int): project id

        Returns:
            (pd.DataFrame): resource information including titles, subtitles, authors and file formats
        """
        response = self._apinterface.get_request("resources/{}", id=id)
        if "resources" in response and len(response["resources"]) > 0:
            df = pd.DataFrame(response["resources"])
            try:
                new_index = df.index.astype(int)
            except ValueError:
                pass
            else:
                df.index = new_index
            return df
        else:
            return pd.DataFrame(columns=["id", "sid", "dctype", "title", "subtitle", "author", "filename", "dcformat"])

    def log_resource(
        self,
        project_id: int,
        dctype: str,
        title: str,
        author: Optional[str] = None,
        dcdate: Optional[str] = None,
        country: Optional[str] = None,
        language: Optional[str] = None,
        contributor: Optional[str] = None,
        publisher: Optional[str] = None,
        rights: Optional[str] = None,
        description: Optional[str] = None,
        abstract: Optional[str] = None,
        toc: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> int:
        """Log a new resource associated with a project (Reports, Questionnaires, Tables, etc).

        If filename is provided then the file is uploaded and logged.

        Args:
            project_id (int): The project id the resource is associated with.
            dctype (str): The type of the resource (e.g., 'txt', 'pdf').
            title (str): The title of the resource.
            author (Optional[str]): The author of the resource. Defaults to None.
            dcdate (Optional[str]): The date of the resource. Defaults to None.
            country (Optional[str]): The country associated with the resource. Defaults to None.
            language (Optional[str]): The language of the resource. Defaults to None.
            contributor (Optional[str]): The contributor to the resource. Defaults to None.
            publisher (Optional[str]): The publisher of the resource. Defaults to None.
            rights (Optional[str]): The rights associated with the resource. Defaults to None.
            description (Optional[str]): A brief description of the resource. Defaults to None.
            abstract (Optional[str]): An abstract summarizing the resource. Defaults to None.
            toc (Optional[str]): The table of contents of the resource. Defaults to None.
            filename (Optional[str]): The filename of the resource which will be uploaded. Defaults to None.

        Returns:
            int: The unique identifier of the logged resource.
        """
        data = {
            "dctype": dctype,
            "title": title,
            "author": author,
            "dcdate": dcdate,
            "country": country,
            "language": language,
            "contributor": contributor,
            "publisher": publisher,
            "rights": rights,
            "description": description,
            "abstract": abstract,
            "toc": toc,
        }

        if filename is not None:
            files = {"file": open(filename, "rb")}
        else:
            files = None

        response = self._apinterface.post_request(pth="resources/{}", id=project_id, data=data, files=files)
        return int(response["resource"]["id"])

    def update_resource(
        self,
        project_id: int,
        resource_id: int,
        dctype: str,
        title: str,
        author: Optional[str] = None,
        dcdate: Optional[str] = None,
        country: Optional[str] = None,
        language: Optional[str] = None,
        contributor: Optional[str] = None,
        publisher: Optional[str] = None,
        rights: Optional[str] = None,
        description: Optional[str] = None,
        abstract: Optional[str] = None,
        toc: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> int:
        """Update the log of resource associated with a project (Reports, Questionnaires, Tables, etc).

        If filename is provided then the file is uploaded and logged.

        Args:
            project_id (int): The project id the resource is associated with.
            resource_id (int): The id of the resource.
            dctype (str): The type of the resource (e.g., 'txt', 'pdf').
            title (str): The title of the resource.
            author (Optional[str]): The author of the resource. Defaults to None.
            dcdate (Optional[str]): The date of the resource. Defaults to None.
            country (Optional[str]): The country associated with the resource. Defaults to None.
            language (Optional[str]): The language of the resource. Defaults to None.
            contributor (Optional[str]): The contributor to the resource. Defaults to None.
            publisher (Optional[str]): The publisher of the resource. Defaults to None.
            rights (Optional[str]): The rights associated with the resource. Defaults to None.
            description (Optional[str]): A brief description of the resource. Defaults to None.
            abstract (Optional[str]): An abstract summarizing the resource. Defaults to None.
            toc (Optional[str]): The table of contents of the resource. Defaults to None.
            filename (Optional[str]): The filename of the resource which will be uploaded. Defaults to None.
        """
        data = {
            "dctype": dctype,
            "title": title,
            "author": author,
            "dcdate": dcdate,
            "country": country,
            "language": language,
            "contributor": contributor,
            "publisher": publisher,
            "rights": rights,
            "description": description,
            "abstract": abstract,
            "toc": toc,
        }

        if filename is not None:
            files = {"file": open(filename, "rb")}
        else:
            files = None

        self._apinterface.post_request(pth="resources/{}/" + f"{resource_id}", id=project_id, data=data, files=files)

    ####################################################################################################################
    # DELETE METHODS
    ####################################################################################################################

    def delete_project_by_id(self, id: int):
        """If the project exists then delete it and check it was deleted.

        Args:
            id (int): the id of the project, not to be confused with the idno.

        Raises:
            DeleteNotAppliedError: This can be the result of system admins blocking data deletion
        """
        pth = "editor/delete/{}"
        self._delete_by_id(pth=pth, id=id, checker_fn=self.get_project_by_id)

    def delete_collection_by_id(self, id: int):
        """If the collection exists then deletes it and check it was deleted.

        Args:
            id (int): the id of the colection.

        Raises:
            DeleteNotAppliedError: This can be the result of system admins blocking data deletion
        """
        pth = "collections/delete/{}"
        self._delete_by_id(pth=pth, id=id, checker_fn=self.get_collection_by_id)

    def delete_resource_by_id(self, project_id, resource_id):
        """If the resource exists then deletes it and check it was deleted.

        Args:
            project_id (int): The project id the resource is associated with.
            resource_id (int): The id of the resource.

        Raises:
            DeleteNotAppliedError: This can be the result of system admins blocking data deletion
        """

        def check_exists(resource_id):
            resource_ids = self.get_resources_by_id(project_id)["id"].apply(int).values
            if resource_id not in resource_ids:
                raise IndexError(f"{resource_id} not in list of resources for project id {project_id}")

        pth = f"resources/delete/{project_id}/" + "{}"
        self._delete_by_id(pth, resource_id, checker_fn=check_exists)

    def delete_template(self, uid: str):
        """Deletes the given template.

        Args:
            uid (str): The Unique Identifier of the template to delete.

        """
        if uid in self._templates:
            self._templates.pop(uid, None)
        self._delete_by_id("templates/delete/{}", id=uid, checker_fn=self.get_template_by_uid)

    def _delete_by_id(self, pth: str, id: Union[int, str], checker_fn: Callable[[int], pd.Series]):
        """Internal, generic method for deleting either collections or projects or similar."""
        # # first check that the project/collection is there to be deleted
        # checker_fn(id)
        try:
            self._apinterface.post_request(pth=pth, id=id)
        except JSONDecodeError:
            pass

        # check that the entity was deleted
        try:
            checker_fn(id)
        except (PermissionError, JSONDecodeError, IndexError, HTTPError):
            pass  # evidently the entity was deleted because now it can't be found
        else:
            raise DeleteNotAppliedError()
