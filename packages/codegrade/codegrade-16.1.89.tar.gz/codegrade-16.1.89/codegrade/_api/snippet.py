"""The endpoints for snippet objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""

import os
import typing as t

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from .. import parsers, utils

if t.TYPE_CHECKING or os.getenv("CG_EAGERIMPORT", False):
    import codegrade

    from ..models.create_snippet_data import CreateSnippetData
    from ..models.patch_snippet_data import PatchSnippetData
    from ..models.snippet import Snippet


_ClientT = t.TypeVar("_ClientT", bound="codegrade.client._BaseClient")


class SnippetService(t.Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: _ClientT) -> None:
        self.__client = client

    def create(
        self: "SnippetService[codegrade.client.AuthenticatedClient]",
        json_body: t.Union[dict, list, "CreateSnippetData"],
        *,
        extra_parameters: t.Optional[
            t.Mapping[str, t.Union[str, bool, int, float]]
        ] = None,
    ) -> "Snippet":
        """Add or modify a `Snippet` by key.

        :param json_body: The body of the request. See
            :class:`.CreateSnippetData` for information about the possible
            fields. You can provide this data as a :class:`.CreateSnippetData`
            or as a dictionary.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A response containing the JSON serialized snippet and return
                  code 201.
        """

        url = "/api/v1/snippet"
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.put(
                url=url, json=utils.to_dict(json_body), params=params
            )
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.snippet import Snippet

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(Snippet)
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
        self: "SnippetService[codegrade.client.AuthenticatedClient]",
        *,
        snippet_id: "int",
        extra_parameters: t.Optional[
            t.Mapping[str, t.Union[str, bool, int, float]]
        ] = None,
    ) -> "None":
        """Delete the `Snippet` with the given id.

        :param snippet_id: The id of the snippet
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: An empty response with return code 204
        """

        url = "/api/v1/snippets/{snippetId}".format(snippetId=snippet_id)
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
        self: "SnippetService[codegrade.client.AuthenticatedClient]",
        json_body: t.Union[dict, list, "PatchSnippetData"],
        *,
        snippet_id: "int",
        extra_parameters: t.Optional[
            t.Mapping[str, t.Union[str, bool, int, float]]
        ] = None,
    ) -> "None":
        """Modify the `Snippet` with the given id.

        :param json_body: The body of the request. See
            :class:`.PatchSnippetData` for information about the possible
            fields. You can provide this data as a :class:`.PatchSnippetData`
            or as a dictionary.
        :param snippet_id: The id of the snippet to change.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: An empty response with return code 204.
        """

        url = "/api/v1/snippets/{snippetId}".format(snippetId=snippet_id)
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

    def get_all(
        self: "SnippetService[codegrade.client.AuthenticatedClient]",
        *,
        extra_parameters: t.Optional[
            t.Mapping[str, t.Union[str, bool, int, float]]
        ] = None,
    ) -> "t.Sequence[Snippet]":
        """Get all snippets of the current user.

        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: An array containing all snippets for the currently logged in
                  user.
        """

        url = "/api/v1/snippets/"
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.get(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.snippet import Snippet

            # fmt: on
            return parsers.JsonResponseParser(
                rqa.List(parsers.ParserFor.make(Snippet))
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
