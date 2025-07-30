"""The endpoints for plagiarism objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""

import os
import typing as t

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from .. import parsers, utils

if t.TYPE_CHECKING or os.getenv("CG_EAGERIMPORT", False):
    import codegrade

    from ..models.plagiarism_case import PlagiarismCase
    from ..models.plagiarism_run import PlagiarismRun


_ClientT = t.TypeVar("_ClientT", bound="codegrade.client._BaseClient")


class PlagiarismService(t.Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: _ClientT) -> None:
        self.__client = client

    def get(
        self: "PlagiarismService[codegrade.client.AuthenticatedClient]",
        *,
        plagiarism_id: "int",
        extra_parameters: t.Optional[
            t.Mapping[str, t.Union[str, bool, int, float]]
        ] = None,
    ) -> "PlagiarismRun":
        """Get a `.models.PlagiarismRun`.

        :param plagiarism_id: The of the plagiarism run.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: An single plagiarism run.
        """

        url = "/api/v1/plagiarism/{plagiarismId}".format(
            plagiarismId=plagiarism_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.get(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.plagiarism_run import PlagiarismRun

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(PlagiarismRun)
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
        self: "PlagiarismService[codegrade.client.AuthenticatedClient]",
        *,
        plagiarism_id: "int",
        extra_parameters: t.Optional[
            t.Mapping[str, t.Union[str, bool, int, float]]
        ] = None,
    ) -> "None":
        """Delete a given plagiarism run and all its cases.

        This is irreversible, so make sure the user really wants this!

        :param plagiarism_id: The id of the run to delete.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: Nothing.
        """

        url = "/api/v1/plagiarism/{plagiarismId}".format(
            plagiarismId=plagiarism_id
        )
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

    def get_cases(
        self: "PlagiarismService[codegrade.client.AuthenticatedClient]",
        *,
        plagiarism_id: "int",
        offset: Maybe["int"] = Nothing,
        limit: "int" = 25,
        extra_parameters: t.Optional[
            t.Mapping[str, t.Union[str, bool, int, float]]
        ] = None,
    ) -> "t.Sequence[PlagiarismCase]":
        """Get all the `.models.PlagiarismCase`s for the given
        `.models.PlagiarismRun`.

        :param plagiarism_id: The of the plagiarism run.
        :param offset: The amount of cases that should be skipped, only used
            when limit is given. Defaults to 0.
        :param limit: The amount of cases to get. Defaults to infinity.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: An array of JSON serialized plagiarism cases.
        """

        url = "/api/v1/plagiarism/{plagiarismId}/cases/".format(
            plagiarismId=plagiarism_id
        )
        params: t.Dict[str, t.Any] = {
            **(extra_parameters or {}),
            "limit": utils.to_dict(limit),
        }
        maybe_from_nullable(t.cast(t.Any, offset)).if_just(
            lambda val: params.__setitem__("offset", val)
        )

        with self.__client as client:
            resp = client.http.get(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.plagiarism_case import PlagiarismCase

            # fmt: on
            return parsers.JsonResponseParser(
                rqa.List(parsers.ParserFor.make(PlagiarismCase))
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
