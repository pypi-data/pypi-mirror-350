# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from datetime import datetime

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.system import (
    ExternalJobStatus,
    matching_job_submit_params,
    matching_job_error_task_params,
    matching_job_complete_task_params,
)
from ...types.system.matching_job_read import MatchingJobRead
from ...types.system.matching_task_read import MatchingTaskRead
from ...types.system.external_job_status import ExternalJobStatus
from ...types.criteria_instance_create_param import CriteriaInstanceCreateParam

__all__ = ["MatchingJobsResource", "AsyncMatchingJobsResource"]


class MatchingJobsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MatchingJobsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#accessing-raw-response-data-eg-headers
        """
        return MatchingJobsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MatchingJobsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#with_streaming_response
        """
        return MatchingJobsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        matching_job_id: int,
        *,
        tenant_db_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MatchingJobRead:
        """
        Get Matching Job

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tenant_db_name:
            raise ValueError(f"Expected a non-empty value for `tenant_db_name` but received {tenant_db_name!r}")
        return self._get(
            f"/system/{tenant_db_name}/matching_jobs/{matching_job_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MatchingJobRead,
        )

    def cancel(
        self,
        matching_job_id: int,
        *,
        tenant_db_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MatchingJobRead:
        """
        Cancel a matching job and its pending tasks.

        This will:

        - Delete tasks from the queue
        - Mark tasks as CANCELLED in the database
        - Mark the job as CANCELLED

        If the job is already in a final state (SUCCESS, ERROR, CANCELLED), it will not
        be modified.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tenant_db_name:
            raise ValueError(f"Expected a non-empty value for `tenant_db_name` but received {tenant_db_name!r}")
        return self._post(
            f"/system/{tenant_db_name}/matching_jobs/{matching_job_id}/cancel",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MatchingJobRead,
        )

    def complete_task(
        self,
        path_tenant_db_name: str,
        *,
        criteria_instances: Iterable[CriteriaInstanceCreateParam],
        task_id: int,
        task_name: str,
        body_tenant_db_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MatchingTaskRead:
        """
        Complete a matching task

        Args:
          task_id: The ID of the task as it exists in the database

          task_name: The name of the task

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_tenant_db_name:
            raise ValueError(
                f"Expected a non-empty value for `path_tenant_db_name` but received {path_tenant_db_name!r}"
            )
        return self._post(
            f"/system/{path_tenant_db_name}/matching_jobs/complete_task",
            body=maybe_transform(
                {
                    "criteria_instances": criteria_instances,
                    "task_id": task_id,
                    "task_name": task_name,
                    "body_tenant_db_name": body_tenant_db_name,
                },
                matching_job_complete_task_params.MatchingJobCompleteTaskParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MatchingTaskRead,
        )

    def error_task(
        self,
        path_tenant_db_name: str,
        *,
        error_message: str,
        task_id: int,
        task_name: str,
        body_tenant_db_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MatchingTaskRead:
        """
        Error a matching task

        Args:
          task_id: The ID of the task as it exists in the database

          task_name: The name of the task

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_tenant_db_name:
            raise ValueError(
                f"Expected a non-empty value for `path_tenant_db_name` but received {path_tenant_db_name!r}"
            )
        return self._post(
            f"/system/{path_tenant_db_name}/matching_jobs/error_task",
            body=maybe_transform(
                {
                    "error_message": error_message,
                    "task_id": task_id,
                    "task_name": task_name,
                    "body_tenant_db_name": body_tenant_db_name,
                },
                matching_job_error_task_params.MatchingJobErrorTaskParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MatchingTaskRead,
        )

    def submit(
        self,
        tenant_db_name: str,
        *,
        criteria_id: int,
        site_id: int,
        batch_size: Optional[int] | NotGiven = NOT_GIVEN,
        cancelled_at: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        completed_at: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        created_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        status: ExternalJobStatus | NotGiven = NOT_GIVEN,
        updated_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MatchingJobRead:
        """
        Submit a new matching job for processing

        Args:
          batch_size: Number of patients to process in each batch

          status: Enum for the status of an external job.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tenant_db_name:
            raise ValueError(f"Expected a non-empty value for `tenant_db_name` but received {tenant_db_name!r}")
        return self._post(
            f"/system/{tenant_db_name}/matching_jobs",
            body=maybe_transform(
                {
                    "criteria_id": criteria_id,
                    "site_id": site_id,
                    "cancelled_at": cancelled_at,
                    "completed_at": completed_at,
                    "created_at": created_at,
                    "status": status,
                    "updated_at": updated_at,
                },
                matching_job_submit_params.MatchingJobSubmitParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"batch_size": batch_size}, matching_job_submit_params.MatchingJobSubmitParams),
            ),
            cast_to=MatchingJobRead,
        )


class AsyncMatchingJobsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMatchingJobsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncMatchingJobsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMatchingJobsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#with_streaming_response
        """
        return AsyncMatchingJobsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        matching_job_id: int,
        *,
        tenant_db_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MatchingJobRead:
        """
        Get Matching Job

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tenant_db_name:
            raise ValueError(f"Expected a non-empty value for `tenant_db_name` but received {tenant_db_name!r}")
        return await self._get(
            f"/system/{tenant_db_name}/matching_jobs/{matching_job_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MatchingJobRead,
        )

    async def cancel(
        self,
        matching_job_id: int,
        *,
        tenant_db_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MatchingJobRead:
        """
        Cancel a matching job and its pending tasks.

        This will:

        - Delete tasks from the queue
        - Mark tasks as CANCELLED in the database
        - Mark the job as CANCELLED

        If the job is already in a final state (SUCCESS, ERROR, CANCELLED), it will not
        be modified.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tenant_db_name:
            raise ValueError(f"Expected a non-empty value for `tenant_db_name` but received {tenant_db_name!r}")
        return await self._post(
            f"/system/{tenant_db_name}/matching_jobs/{matching_job_id}/cancel",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MatchingJobRead,
        )

    async def complete_task(
        self,
        path_tenant_db_name: str,
        *,
        criteria_instances: Iterable[CriteriaInstanceCreateParam],
        task_id: int,
        task_name: str,
        body_tenant_db_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MatchingTaskRead:
        """
        Complete a matching task

        Args:
          task_id: The ID of the task as it exists in the database

          task_name: The name of the task

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_tenant_db_name:
            raise ValueError(
                f"Expected a non-empty value for `path_tenant_db_name` but received {path_tenant_db_name!r}"
            )
        return await self._post(
            f"/system/{path_tenant_db_name}/matching_jobs/complete_task",
            body=await async_maybe_transform(
                {
                    "criteria_instances": criteria_instances,
                    "task_id": task_id,
                    "task_name": task_name,
                    "body_tenant_db_name": body_tenant_db_name,
                },
                matching_job_complete_task_params.MatchingJobCompleteTaskParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MatchingTaskRead,
        )

    async def error_task(
        self,
        path_tenant_db_name: str,
        *,
        error_message: str,
        task_id: int,
        task_name: str,
        body_tenant_db_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MatchingTaskRead:
        """
        Error a matching task

        Args:
          task_id: The ID of the task as it exists in the database

          task_name: The name of the task

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_tenant_db_name:
            raise ValueError(
                f"Expected a non-empty value for `path_tenant_db_name` but received {path_tenant_db_name!r}"
            )
        return await self._post(
            f"/system/{path_tenant_db_name}/matching_jobs/error_task",
            body=await async_maybe_transform(
                {
                    "error_message": error_message,
                    "task_id": task_id,
                    "task_name": task_name,
                    "body_tenant_db_name": body_tenant_db_name,
                },
                matching_job_error_task_params.MatchingJobErrorTaskParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MatchingTaskRead,
        )

    async def submit(
        self,
        tenant_db_name: str,
        *,
        criteria_id: int,
        site_id: int,
        batch_size: Optional[int] | NotGiven = NOT_GIVEN,
        cancelled_at: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        completed_at: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        created_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        status: ExternalJobStatus | NotGiven = NOT_GIVEN,
        updated_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MatchingJobRead:
        """
        Submit a new matching job for processing

        Args:
          batch_size: Number of patients to process in each batch

          status: Enum for the status of an external job.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tenant_db_name:
            raise ValueError(f"Expected a non-empty value for `tenant_db_name` but received {tenant_db_name!r}")
        return await self._post(
            f"/system/{tenant_db_name}/matching_jobs",
            body=await async_maybe_transform(
                {
                    "criteria_id": criteria_id,
                    "site_id": site_id,
                    "cancelled_at": cancelled_at,
                    "completed_at": completed_at,
                    "created_at": created_at,
                    "status": status,
                    "updated_at": updated_at,
                },
                matching_job_submit_params.MatchingJobSubmitParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"batch_size": batch_size}, matching_job_submit_params.MatchingJobSubmitParams
                ),
            ),
            cast_to=MatchingJobRead,
        )


class MatchingJobsResourceWithRawResponse:
    def __init__(self, matching_jobs: MatchingJobsResource) -> None:
        self._matching_jobs = matching_jobs

        self.retrieve = to_raw_response_wrapper(
            matching_jobs.retrieve,
        )
        self.cancel = to_raw_response_wrapper(
            matching_jobs.cancel,
        )
        self.complete_task = to_raw_response_wrapper(
            matching_jobs.complete_task,
        )
        self.error_task = to_raw_response_wrapper(
            matching_jobs.error_task,
        )
        self.submit = to_raw_response_wrapper(
            matching_jobs.submit,
        )


class AsyncMatchingJobsResourceWithRawResponse:
    def __init__(self, matching_jobs: AsyncMatchingJobsResource) -> None:
        self._matching_jobs = matching_jobs

        self.retrieve = async_to_raw_response_wrapper(
            matching_jobs.retrieve,
        )
        self.cancel = async_to_raw_response_wrapper(
            matching_jobs.cancel,
        )
        self.complete_task = async_to_raw_response_wrapper(
            matching_jobs.complete_task,
        )
        self.error_task = async_to_raw_response_wrapper(
            matching_jobs.error_task,
        )
        self.submit = async_to_raw_response_wrapper(
            matching_jobs.submit,
        )


class MatchingJobsResourceWithStreamingResponse:
    def __init__(self, matching_jobs: MatchingJobsResource) -> None:
        self._matching_jobs = matching_jobs

        self.retrieve = to_streamed_response_wrapper(
            matching_jobs.retrieve,
        )
        self.cancel = to_streamed_response_wrapper(
            matching_jobs.cancel,
        )
        self.complete_task = to_streamed_response_wrapper(
            matching_jobs.complete_task,
        )
        self.error_task = to_streamed_response_wrapper(
            matching_jobs.error_task,
        )
        self.submit = to_streamed_response_wrapper(
            matching_jobs.submit,
        )


class AsyncMatchingJobsResourceWithStreamingResponse:
    def __init__(self, matching_jobs: AsyncMatchingJobsResource) -> None:
        self._matching_jobs = matching_jobs

        self.retrieve = async_to_streamed_response_wrapper(
            matching_jobs.retrieve,
        )
        self.cancel = async_to_streamed_response_wrapper(
            matching_jobs.cancel,
        )
        self.complete_task = async_to_streamed_response_wrapper(
            matching_jobs.complete_task,
        )
        self.error_task = async_to_streamed_response_wrapper(
            matching_jobs.error_task,
        )
        self.submit = async_to_streamed_response_wrapper(
            matching_jobs.submit,
        )
