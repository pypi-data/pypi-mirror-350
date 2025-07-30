"""The endpoints for sso_provider objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""

import os
import typing as t

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from .. import parsers, utils

if t.TYPE_CHECKING or os.getenv("CG_EAGERIMPORT", False):
    import codegrade

    from ..models.create_sso_provider_data import CreateSSOProviderData
    from ..models.saml2_provider_json import Saml2ProviderJSON


_ClientT = t.TypeVar("_ClientT", bound="codegrade.client._BaseClient")


class SSOProviderService(t.Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: _ClientT) -> None:
        self.__client = client

    def create(
        self: "SSOProviderService[codegrade.client.AuthenticatedClient]",
        json_body: t.Union[dict, list, "CreateSSOProviderData"],
        *,
        extra_parameters: t.Optional[
            t.Mapping[str, t.Union[str, bool, int, float]]
        ] = None,
    ) -> "Saml2ProviderJSON":
        """Register a new SSO Provider in this instance.

        Users will be able to login using the registered provider.

        The request should contain two files. One named `json` containing the
        json data explained below and one named `logo` containing the backup
        logo.

        :param json_body: The body of the request. See
            :class:`.CreateSSOProviderData` for information about the possible
            fields. You can provide this data as a
            :class:`.CreateSSOProviderData` or as a dictionary.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The just created provider.
        """

        url = "/api/v1/sso_providers/"
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.post(
                url=url, json=utils.to_dict(json_body), params=params
            )
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.saml2_provider_json import Saml2ProviderJSON

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(Saml2ProviderJSON)
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
