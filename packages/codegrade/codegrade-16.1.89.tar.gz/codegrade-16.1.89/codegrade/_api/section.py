"""The endpoints for section objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""

import os
import typing as t

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from .. import parsers, utils

if t.TYPE_CHECKING or os.getenv("CG_EAGERIMPORT", False):
    import codegrade

    from ..models.add_users_section_data import AddUsersSectionData
    from ..models.create_division_section_data import CreateDivisionSectionData
    from ..models.extended_course_section import ExtendedCourseSection
    from ..models.patch_section_data import PatchSectionData
    from ..models.result_data_post_section_create_division import (
        ResultDataPostSectionCreateDivision,
    )


_ClientT = t.TypeVar("_ClientT", bound="codegrade.client._BaseClient")


class SectionService(t.Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: _ClientT) -> None:
        self.__client = client

    def add_users(
        self: "SectionService[codegrade.client.AuthenticatedClient]",
        json_body: t.Union[dict, list, "AddUsersSectionData"],
        *,
        section_id: "str",
        extra_parameters: t.Optional[
            t.Mapping[str, t.Union[str, bool, int, float]]
        ] = None,
    ) -> "ExtendedCourseSection":
        """Add users to a course section.

        :param json_body: The body of the request. See
            :class:`.AddUsersSectionData` for information about the possible
            fields. You can provide this data as a
            :class:`.AddUsersSectionData` or as a dictionary.
        :param section_id: The id of the course section to add a user to.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The updated course section.
        """

        url = "/api/v1/sections/{sectionId}/members/".format(
            sectionId=section_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.put(
                url=url, json=utils.to_dict(json_body), params=params
            )
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.extended_course_section import ExtendedCourseSection

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(ExtendedCourseSection)
            ).try_parse(resp)

        from ..models.any_error import AnyError

        raise utils.get_error(
            resp,
            (
                (
                    (400, 409, 401, 403, 404, 429, 500),
                    utils.unpack_union(AnyError),
                ),
            ),
        )

    def create_division(
        self: "SectionService[codegrade.client.AuthenticatedClient]",
        json_body: t.Union[dict, list, "CreateDivisionSectionData"],
        *,
        section_id: "str",
        extra_parameters: t.Optional[
            t.Mapping[str, t.Union[str, bool, int, float]]
        ] = None,
    ) -> "ResultDataPostSectionCreateDivision":
        """Connect users to a course section.

        Users that are already enrolled in the course connected to this section
        are immediately added to the course section. Other users will be added
        to the section as soon as they enroll in the course.

        :param json_body: The body of the request. See
            :class:`.CreateDivisionSectionData` for information about the
            possible fields. You can provide this data as a
            :class:`.CreateDivisionSectionData` or as a dictionary.
        :param section_id: The id of the course section to connect users to.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The new division containing the users that were not
                  immediately added to the course section.
        """

        url = "/api/v1/sections/{sectionId}/division".format(
            sectionId=section_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.post(
                url=url, json=utils.to_dict(json_body), params=params
            )
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.result_data_post_section_create_division import (
                ResultDataPostSectionCreateDivision,
            )

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(ResultDataPostSectionCreateDivision)
            ).try_parse(resp)

        from ..models.any_error import AnyError

        raise utils.get_error(
            resp,
            (
                (
                    (400, 409, 401, 403, 404, 429, 500),
                    utils.unpack_union(AnyError),
                ),
            ),
        )

    def get(
        self: "SectionService[codegrade.client.AuthenticatedClient]",
        *,
        section_id: "str",
        extra_parameters: t.Optional[
            t.Mapping[str, t.Union[str, bool, int, float]]
        ] = None,
    ) -> "ExtendedCourseSection":
        """Get a course section.

        :param section_id: The id of the course section to get.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The requested course section.
        """

        url = "/api/v1/sections/{sectionId}".format(sectionId=section_id)
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.get(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.extended_course_section import ExtendedCourseSection

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(ExtendedCourseSection)
            ).try_parse(resp)

        from ..models.any_error import AnyError

        raise utils.get_error(
            resp,
            (
                (
                    (400, 409, 401, 403, 404, 429, 500),
                    utils.unpack_union(AnyError),
                ),
            ),
        )

    def delete(
        self: "SectionService[codegrade.client.AuthenticatedClient]",
        *,
        section_id: "str",
        extra_parameters: t.Optional[
            t.Mapping[str, t.Union[str, bool, int, float]]
        ] = None,
    ) -> "None":
        """Delete a course section.

        :param section_id: The id of the section to delete.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: Nothing.
        """

        url = "/api/v1/sections/{sectionId}".format(sectionId=section_id)
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.delete(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 204):
            # fmt: off
            # fmt: on
            return parsers.ConstantlyParser(None).try_parse(resp)

        from ..models.any_error import AnyError

        raise utils.get_error(
            resp,
            (
                (
                    (400, 409, 401, 403, 404, 429, 500),
                    utils.unpack_union(AnyError),
                ),
            ),
        )

    def patch(
        self: "SectionService[codegrade.client.AuthenticatedClient]",
        json_body: t.Union[dict, list, "PatchSectionData"],
        *,
        section_id: "str",
        extra_parameters: t.Optional[
            t.Mapping[str, t.Union[str, bool, int, float]]
        ] = None,
    ) -> "ExtendedCourseSection":
        """Update a course section.

        :param json_body: The body of the request. See
            :class:`.PatchSectionData` for information about the possible
            fields. You can provide this data as a :class:`.PatchSectionData`
            or as a dictionary.
        :param section_id: The id of the course section to update.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The updated course section.
        """

        url = "/api/v1/sections/{sectionId}".format(sectionId=section_id)
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.patch(
                url=url, json=utils.to_dict(json_body), params=params
            )
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.extended_course_section import ExtendedCourseSection

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(ExtendedCourseSection)
            ).try_parse(resp)

        from ..models.any_error import AnyError

        raise utils.get_error(
            resp,
            (
                (
                    (400, 409, 401, 403, 404, 429, 500),
                    utils.unpack_union(AnyError),
                ),
            ),
        )

    def delete_user(
        self: "SectionService[codegrade.client.AuthenticatedClient]",
        *,
        section_id: "str",
        user_id: "int",
        extra_parameters: t.Optional[
            t.Mapping[str, t.Union[str, bool, int, float]]
        ] = None,
    ) -> "ExtendedCourseSection":
        """Remove a user from a course section.

        :param section_id: The id of the course section to remove the user
            from.
        :param user_id: The id of the user to remove from the course section.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The updated course section.
        """

        url = "/api/v1/sections/{sectionId}/members/{userId}".format(
            sectionId=section_id, userId=user_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.delete(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.extended_course_section import ExtendedCourseSection

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(ExtendedCourseSection)
            ).try_parse(resp)

        from ..models.any_error import AnyError

        raise utils.get_error(
            resp,
            (
                (
                    (400, 409, 401, 403, 404, 429, 500),
                    utils.unpack_union(AnyError),
                ),
            ),
        )
