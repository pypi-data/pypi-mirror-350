# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from asktable import Asktable, AsyncAsktable
from tests.utils import assert_matches_type
from asktable.types.sys.projects import (
    APIKeyListResponse,
    APIKeyCreateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAPIKeys:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Asktable) -> None:
        api_key = client.sys.projects.api_keys.create(
            project_id="project_id",
            ak_role="admin",
        )
        assert_matches_type(APIKeyCreateResponse, api_key, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Asktable) -> None:
        response = client.sys.projects.api_keys.with_raw_response.create(
            project_id="project_id",
            ak_role="admin",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = response.parse()
        assert_matches_type(APIKeyCreateResponse, api_key, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Asktable) -> None:
        with client.sys.projects.api_keys.with_streaming_response.create(
            project_id="project_id",
            ak_role="admin",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = response.parse()
            assert_matches_type(APIKeyCreateResponse, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Asktable) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            client.sys.projects.api_keys.with_raw_response.create(
                project_id="",
                ak_role="admin",
            )

    @parametrize
    def test_method_list(self, client: Asktable) -> None:
        api_key = client.sys.projects.api_keys.list(
            "project_id",
        )
        assert_matches_type(APIKeyListResponse, api_key, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Asktable) -> None:
        response = client.sys.projects.api_keys.with_raw_response.list(
            "project_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = response.parse()
        assert_matches_type(APIKeyListResponse, api_key, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Asktable) -> None:
        with client.sys.projects.api_keys.with_streaming_response.list(
            "project_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = response.parse()
            assert_matches_type(APIKeyListResponse, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Asktable) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            client.sys.projects.api_keys.with_raw_response.list(
                "",
            )

    @parametrize
    def test_method_delete(self, client: Asktable) -> None:
        api_key = client.sys.projects.api_keys.delete(
            key_id="key_id",
            project_id="project_id",
        )
        assert api_key is None

    @parametrize
    def test_raw_response_delete(self, client: Asktable) -> None:
        response = client.sys.projects.api_keys.with_raw_response.delete(
            key_id="key_id",
            project_id="project_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = response.parse()
        assert api_key is None

    @parametrize
    def test_streaming_response_delete(self, client: Asktable) -> None:
        with client.sys.projects.api_keys.with_streaming_response.delete(
            key_id="key_id",
            project_id="project_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = response.parse()
            assert api_key is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Asktable) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            client.sys.projects.api_keys.with_raw_response.delete(
                key_id="key_id",
                project_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key_id` but received ''"):
            client.sys.projects.api_keys.with_raw_response.delete(
                key_id="",
                project_id="project_id",
            )

    @parametrize
    def test_method_create_token(self, client: Asktable) -> None:
        api_key = client.sys.projects.api_keys.create_token(
            project_id="project_id",
        )
        assert_matches_type(object, api_key, path=["response"])

    @parametrize
    def test_method_create_token_with_all_params(self, client: Asktable) -> None:
        api_key = client.sys.projects.api_keys.create_token(
            project_id="project_id",
            ak_role="asker",
            chat_role={
                "role_id": "1",
                "role_variables": {"id": "42"},
            },
            token_ttl=900,
            user_profile={"name": "张三"},
        )
        assert_matches_type(object, api_key, path=["response"])

    @parametrize
    def test_raw_response_create_token(self, client: Asktable) -> None:
        response = client.sys.projects.api_keys.with_raw_response.create_token(
            project_id="project_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = response.parse()
        assert_matches_type(object, api_key, path=["response"])

    @parametrize
    def test_streaming_response_create_token(self, client: Asktable) -> None:
        with client.sys.projects.api_keys.with_streaming_response.create_token(
            project_id="project_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = response.parse()
            assert_matches_type(object, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create_token(self, client: Asktable) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            client.sys.projects.api_keys.with_raw_response.create_token(
                project_id="",
            )


class TestAsyncAPIKeys:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncAsktable) -> None:
        api_key = await async_client.sys.projects.api_keys.create(
            project_id="project_id",
            ak_role="admin",
        )
        assert_matches_type(APIKeyCreateResponse, api_key, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAsktable) -> None:
        response = await async_client.sys.projects.api_keys.with_raw_response.create(
            project_id="project_id",
            ak_role="admin",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = await response.parse()
        assert_matches_type(APIKeyCreateResponse, api_key, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAsktable) -> None:
        async with async_client.sys.projects.api_keys.with_streaming_response.create(
            project_id="project_id",
            ak_role="admin",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = await response.parse()
            assert_matches_type(APIKeyCreateResponse, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncAsktable) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            await async_client.sys.projects.api_keys.with_raw_response.create(
                project_id="",
                ak_role="admin",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAsktable) -> None:
        api_key = await async_client.sys.projects.api_keys.list(
            "project_id",
        )
        assert_matches_type(APIKeyListResponse, api_key, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAsktable) -> None:
        response = await async_client.sys.projects.api_keys.with_raw_response.list(
            "project_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = await response.parse()
        assert_matches_type(APIKeyListResponse, api_key, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAsktable) -> None:
        async with async_client.sys.projects.api_keys.with_streaming_response.list(
            "project_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = await response.parse()
            assert_matches_type(APIKeyListResponse, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncAsktable) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            await async_client.sys.projects.api_keys.with_raw_response.list(
                "",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncAsktable) -> None:
        api_key = await async_client.sys.projects.api_keys.delete(
            key_id="key_id",
            project_id="project_id",
        )
        assert api_key is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAsktable) -> None:
        response = await async_client.sys.projects.api_keys.with_raw_response.delete(
            key_id="key_id",
            project_id="project_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = await response.parse()
        assert api_key is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAsktable) -> None:
        async with async_client.sys.projects.api_keys.with_streaming_response.delete(
            key_id="key_id",
            project_id="project_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = await response.parse()
            assert api_key is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAsktable) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            await async_client.sys.projects.api_keys.with_raw_response.delete(
                key_id="key_id",
                project_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key_id` but received ''"):
            await async_client.sys.projects.api_keys.with_raw_response.delete(
                key_id="",
                project_id="project_id",
            )

    @parametrize
    async def test_method_create_token(self, async_client: AsyncAsktable) -> None:
        api_key = await async_client.sys.projects.api_keys.create_token(
            project_id="project_id",
        )
        assert_matches_type(object, api_key, path=["response"])

    @parametrize
    async def test_method_create_token_with_all_params(self, async_client: AsyncAsktable) -> None:
        api_key = await async_client.sys.projects.api_keys.create_token(
            project_id="project_id",
            ak_role="asker",
            chat_role={
                "role_id": "1",
                "role_variables": {"id": "42"},
            },
            token_ttl=900,
            user_profile={"name": "张三"},
        )
        assert_matches_type(object, api_key, path=["response"])

    @parametrize
    async def test_raw_response_create_token(self, async_client: AsyncAsktable) -> None:
        response = await async_client.sys.projects.api_keys.with_raw_response.create_token(
            project_id="project_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = await response.parse()
        assert_matches_type(object, api_key, path=["response"])

    @parametrize
    async def test_streaming_response_create_token(self, async_client: AsyncAsktable) -> None:
        async with async_client.sys.projects.api_keys.with_streaming_response.create_token(
            project_id="project_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = await response.parse()
            assert_matches_type(object, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create_token(self, async_client: AsyncAsktable) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            await async_client.sys.projects.api_keys.with_raw_response.create_token(
                project_id="",
            )
