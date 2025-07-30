"""The endpoints for role objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""

import os
import typing as t

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from .. import parsers, utils

if t.TYPE_CHECKING or os.getenv("CG_EAGERIMPORT", False):
    import codegrade

    from ..models.patch_role_data import PatchRoleData
    from ..models.role_as_json_with_perms import RoleAsJSONWithPerms


_ClientT = t.TypeVar("_ClientT", bound="codegrade.client._BaseClient")


class RoleService(t.Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: _ClientT) -> None:
        self.__client = client

    def get_all(
        self: "RoleService[codegrade.client.AuthenticatedClient]",
        *,
        extra_parameters: t.Optional[
            t.Mapping[str, t.Union[str, bool, int, float]]
        ] = None,
    ) -> "t.Sequence[RoleAsJSONWithPerms]":
        """Get all global roles with their permissions

        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: An array of all global roles.
        """

        url = "/api/v1/roles/"
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.get(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.role_as_json_with_perms import RoleAsJSONWithPerms

            # fmt: on
            return parsers.JsonResponseParser(
                rqa.List(parsers.ParserFor.make(RoleAsJSONWithPerms))
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

    def patch(
        self: "RoleService[codegrade.client.AuthenticatedClient]",
        json_body: t.Union[dict, list, "PatchRoleData"],
        *,
        role_id: "int",
        extra_parameters: t.Optional[
            t.Mapping[str, t.Union[str, bool, int, float]]
        ] = None,
    ) -> "None":
        """Update the `Permission` of a given `Role`.

        :param json_body: The body of the request. See :class:`.PatchRoleData`
            for information about the possible fields. You can provide this
            data as a :class:`.PatchRoleData` or as a dictionary.
        :param role_id: The id of the global role.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: An empty response with return code 204.
        """

        url = "/api/v1/roles/{roleId}".format(roleId=role_id)
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.patch(
                url=url, json=utils.to_dict(json_body), params=params
            )
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
