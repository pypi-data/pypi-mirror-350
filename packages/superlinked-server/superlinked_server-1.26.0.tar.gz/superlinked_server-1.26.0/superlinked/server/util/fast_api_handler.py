# Copyright 2024 Superlinked, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import structlog
from beartype.typing import Any
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import Field
from superlinked.framework.common.util.immutable_model import ImmutableBaseModel
from superlinked.framework.dsl.executor.rest.rest_handler import RestHandler

logger = structlog.getLogger(__name__)


class QueryResponse(ImmutableBaseModel):
    schema_: str = Field(..., alias="schema")
    results: list[dict[str, Any]]
    metadata: dict[str, Any] | None


class FastApiHandler:
    def __init__(self, rest_handler: RestHandler) -> None:
        self.__rest_handler = rest_handler

    async def ingest(self, request: Request) -> Response:
        payload = await request.json()
        self.__rest_handler._ingest_handler(payload, request.url.path)
        logger.debug("ingested data", path=request.url.path, pii_payload=payload)
        return Response(status_code=status.HTTP_202_ACCEPTED)

    async def query(self, request: Request) -> Response:
        payload = await request.json()
        include_metadata = request.headers.get("x-include-metadata", "false").lower() == "true"
        query_result = self.__rest_handler._query_handler(payload, request.url.path, include_metadata)
        logger.debug(
            "queried data",
            path=request.url.path,
            include_metadata=include_metadata,
            result_entity_count=len(query_result.entries),
            pii_payload=payload,
            pii_result=query_result,
        )

        return JSONResponse(
            content=(query_result.model_dump() if include_metadata else query_result.model_dump(exclude={"metadata"})),
            status_code=status.HTTP_200_OK,
        )
