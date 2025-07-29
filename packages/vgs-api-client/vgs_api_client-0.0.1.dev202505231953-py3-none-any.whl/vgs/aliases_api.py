import logging

import vgs_api_client
from vgs_api_client import Configuration
from vgs_api_client.api import aliases_api
from vgs_api_client.exceptions import (
    ApiException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
)
from vgs_api_client.model.alias_format import AliasFormat
from vgs_api_client.model.create_aliases_request import CreateAliasesRequest
from vgs_api_client.model.create_aliases_request_new import CreateAliasesRequestNew
from vgs_api_client.model.update_alias_request import UpdateAliasRequest
from vgs_api_client.model.update_alias_request_data import UpdateAliasRequestData

import vgs.exceptions
from vgs.configuration import VGSConfiguration


def _map_exception(message, e):
    error_message = message
    if isinstance(e, ApiException):
        error_message += f". Details: {e}"
    if isinstance(e, NotFoundException):
        return vgs.exceptions.NotFoundException(error_message)
    if isinstance(e, UnauthorizedException):
        return vgs.exceptions.UnauthorizedException(error_message)
    if isinstance(e, ForbiddenException):
        return vgs.exceptions.ForbiddenException(error_message)
    return vgs.exceptions.VgsApiException(error_message)


class Aliases:
    def __init__(self, config: Configuration):
        if not config:
            raise ValueError

        self._api = aliases_api.AliasesApi(
            vgs_api_client.ApiClient(
                VGSConfiguration(username=config.username, password=config.password, host=config.host)
            )
        )

    def redact(self, data):
        # TODO: validate data and raise meaningful exception on validation error
        try:
            requests = []
            for item in data:
                requests.append(
                    CreateAliasesRequestNew(
                        format=AliasFormat(item.get("format", "UUID")),
                        value=item.get("value"),
                        classifiers=item.get("classifiers", []),
                        storage=item.get("storage", "PERSISTENT"),
                    )
                )
            create_aliases_request = CreateAliasesRequest(data=requests)

            api_response = self._api.create_aliases(create_aliases_request=create_aliases_request)
            return api_response["data"]
        except Exception as e:
            logging.exception(e)
            ex = _map_exception(f"Failed to redact data ${data}", e)
            raise ex

    def reveal(self, aliases):
        # TODO: validate data and raise meaningful exception on validation error
        try:
            query = ",".join(aliases) if isinstance(aliases, list) else aliases
            api_response = self._api.reveal_multiple_aliases(aliases=query)
            return api_response["data"]
        except Exception as e:
            logging.exception(e)
            ex = _map_exception(f"Failed to reveal aliases ${aliases}", e)
            raise ex

    def delete(self, alias):
        try:
            self._api.delete_alias(alias=alias)
        except Exception as e:
            logging.exception(e)
            ex = _map_exception(f"Failed to reveal delete ${alias}", e)
            raise ex

    def update(self, alias, data):
        try:
            self._api.update_alias(
                alias=alias,
                update_alias_request=UpdateAliasRequest(UpdateAliasRequestData(data["classifiers"])),
            )
        except Exception as e:
            logging.exception(e)
            ex = _map_exception(f"Failed to update alias ${alias}.", e)
            raise ex
