# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable

import httpx

from .bulk import (
    BulkResource,
    AsyncBulkResource,
    BulkResourceWithRawResponse,
    AsyncBulkResourceWithRawResponse,
    BulkResourceWithStreamingResponse,
    AsyncBulkResourceWithStreamingResponse,
)
from .cache import (
    CacheResource,
    AsyncCacheResource,
    CacheResourceWithRawResponse,
    AsyncCacheResourceWithRawResponse,
    CacheResourceWithStreamingResponse,
    AsyncCacheResourceWithStreamingResponse,
)
from ...types import (
    ExportStatus,
    system_patch_patient_export_params,
    system_get_patient_match_data_params,
)
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import maybe_transform, async_maybe_transform
from .criteria import (
    CriteriaResource,
    AsyncCriteriaResource,
    CriteriaResourceWithRawResponse,
    AsyncCriteriaResourceWithRawResponse,
    CriteriaResourceWithStreamingResponse,
    AsyncCriteriaResourceWithStreamingResponse,
)
from ..._compat import cached_property
from .protocols import (
    ProtocolsResource,
    AsyncProtocolsResource,
    ProtocolsResourceWithRawResponse,
    AsyncProtocolsResourceWithRawResponse,
    ProtocolsResourceWithStreamingResponse,
    AsyncProtocolsResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .sites.sites import (
    SitesResource,
    AsyncSitesResource,
    SitesResourceWithRawResponse,
    AsyncSitesResourceWithRawResponse,
    SitesResourceWithStreamingResponse,
    AsyncSitesResourceWithStreamingResponse,
)
from .appointments import (
    AppointmentsResource,
    AsyncAppointmentsResource,
    AppointmentsResourceWithRawResponse,
    AsyncAppointmentsResourceWithRawResponse,
    AppointmentsResourceWithStreamingResponse,
    AsyncAppointmentsResourceWithStreamingResponse,
)
from .matching_jobs import (
    MatchingJobsResource,
    AsyncMatchingJobsResource,
    MatchingJobsResourceWithRawResponse,
    AsyncMatchingJobsResourceWithRawResponse,
    MatchingJobsResourceWithStreamingResponse,
    AsyncMatchingJobsResourceWithStreamingResponse,
)
from ..._base_client import make_request_options
from .custom_searches import (
    CustomSearchesResource,
    AsyncCustomSearchesResource,
    CustomSearchesResourceWithRawResponse,
    AsyncCustomSearchesResourceWithRawResponse,
    CustomSearchesResourceWithStreamingResponse,
    AsyncCustomSearchesResourceWithStreamingResponse,
)
from .protocol_parsing import (
    ProtocolParsingResource,
    AsyncProtocolParsingResource,
    ProtocolParsingResourceWithRawResponse,
    AsyncProtocolParsingResourceWithRawResponse,
    ProtocolParsingResourceWithStreamingResponse,
    AsyncProtocolParsingResourceWithStreamingResponse,
)
from .patients.patients import (
    PatientsResource,
    AsyncPatientsResource,
    PatientsResourceWithRawResponse,
    AsyncPatientsResourceWithRawResponse,
    PatientsResourceWithStreamingResponse,
    AsyncPatientsResourceWithStreamingResponse,
)
from ...types.export_status import ExportStatus
from ...types.criteria_instance_create_param import CriteriaInstanceCreateParam
from ...types.system_patch_patient_export_response import SystemPatchPatientExportResponse
from ...types.system_get_patient_match_data_response import SystemGetPatientMatchDataResponse
from ...types.system_create_criteria_instance_response import SystemCreateCriteriaInstanceResponse

__all__ = ["SystemResource", "AsyncSystemResource"]


class SystemResource(SyncAPIResource):
    @cached_property
    def protocols(self) -> ProtocolsResource:
        return ProtocolsResource(self._client)

    @cached_property
    def criteria(self) -> CriteriaResource:
        return CriteriaResource(self._client)

    @cached_property
    def protocol_parsing(self) -> ProtocolParsingResource:
        return ProtocolParsingResource(self._client)

    @cached_property
    def sites(self) -> SitesResource:
        return SitesResource(self._client)

    @cached_property
    def patients(self) -> PatientsResource:
        return PatientsResource(self._client)

    @cached_property
    def appointments(self) -> AppointmentsResource:
        return AppointmentsResource(self._client)

    @cached_property
    def bulk(self) -> BulkResource:
        return BulkResource(self._client)

    @cached_property
    def matching_jobs(self) -> MatchingJobsResource:
        return MatchingJobsResource(self._client)

    @cached_property
    def cache(self) -> CacheResource:
        return CacheResource(self._client)

    @cached_property
    def custom_searches(self) -> CustomSearchesResource:
        return CustomSearchesResource(self._client)

    @cached_property
    def with_raw_response(self) -> SystemResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#accessing-raw-response-data-eg-headers
        """
        return SystemResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SystemResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#with_streaming_response
        """
        return SystemResourceWithStreamingResponse(self)

    def create_criteria_instance(
        self,
        tenant_db_name: str,
        *,
        body: Iterable[CriteriaInstanceCreateParam],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SystemCreateCriteriaInstanceResponse:
        """
        Create Criteria Instances

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tenant_db_name:
            raise ValueError(f"Expected a non-empty value for `tenant_db_name` but received {tenant_db_name!r}")
        return self._post(
            f"/system/{tenant_db_name}/criteria_instances",
            body=maybe_transform(body, Iterable[CriteriaInstanceCreateParam]),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SystemCreateCriteriaInstanceResponse,
        )

    def get_patient_match_data(
        self,
        tenant_db_name: str,
        *,
        criteria_id: int,
        patient_ids: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SystemGetPatientMatchDataResponse:
        """
        Get patient match data based on a list of patient IDs and a criteria ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tenant_db_name:
            raise ValueError(f"Expected a non-empty value for `tenant_db_name` but received {tenant_db_name!r}")
        return self._post(
            f"/system/{tenant_db_name}/patient-match-data",
            body=maybe_transform(
                {
                    "criteria_id": criteria_id,
                    "patient_ids": patient_ids,
                },
                system_get_patient_match_data_params.SystemGetPatientMatchDataParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SystemGetPatientMatchDataResponse,
        )

    def patch_patient_export(
        self,
        patient_ctms_export_id: int,
        *,
        tenant_db_name: str,
        status: ExportStatus,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SystemPatchPatientExportResponse:
        """
        Update a patient CTMS export's status

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tenant_db_name:
            raise ValueError(f"Expected a non-empty value for `tenant_db_name` but received {tenant_db_name!r}")
        return self._patch(
            f"/system/{tenant_db_name}/patient-ctms-exports/{patient_ctms_export_id}",
            body=maybe_transform({"status": status}, system_patch_patient_export_params.SystemPatchPatientExportParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SystemPatchPatientExportResponse,
        )

    def ping(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Simple health check endpoint to verify the API is running"""
        return self._get(
            "/system/ping",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncSystemResource(AsyncAPIResource):
    @cached_property
    def protocols(self) -> AsyncProtocolsResource:
        return AsyncProtocolsResource(self._client)

    @cached_property
    def criteria(self) -> AsyncCriteriaResource:
        return AsyncCriteriaResource(self._client)

    @cached_property
    def protocol_parsing(self) -> AsyncProtocolParsingResource:
        return AsyncProtocolParsingResource(self._client)

    @cached_property
    def sites(self) -> AsyncSitesResource:
        return AsyncSitesResource(self._client)

    @cached_property
    def patients(self) -> AsyncPatientsResource:
        return AsyncPatientsResource(self._client)

    @cached_property
    def appointments(self) -> AsyncAppointmentsResource:
        return AsyncAppointmentsResource(self._client)

    @cached_property
    def bulk(self) -> AsyncBulkResource:
        return AsyncBulkResource(self._client)

    @cached_property
    def matching_jobs(self) -> AsyncMatchingJobsResource:
        return AsyncMatchingJobsResource(self._client)

    @cached_property
    def cache(self) -> AsyncCacheResource:
        return AsyncCacheResource(self._client)

    @cached_property
    def custom_searches(self) -> AsyncCustomSearchesResource:
        return AsyncCustomSearchesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSystemResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncSystemResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSystemResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#with_streaming_response
        """
        return AsyncSystemResourceWithStreamingResponse(self)

    async def create_criteria_instance(
        self,
        tenant_db_name: str,
        *,
        body: Iterable[CriteriaInstanceCreateParam],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SystemCreateCriteriaInstanceResponse:
        """
        Create Criteria Instances

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tenant_db_name:
            raise ValueError(f"Expected a non-empty value for `tenant_db_name` but received {tenant_db_name!r}")
        return await self._post(
            f"/system/{tenant_db_name}/criteria_instances",
            body=await async_maybe_transform(body, Iterable[CriteriaInstanceCreateParam]),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SystemCreateCriteriaInstanceResponse,
        )

    async def get_patient_match_data(
        self,
        tenant_db_name: str,
        *,
        criteria_id: int,
        patient_ids: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SystemGetPatientMatchDataResponse:
        """
        Get patient match data based on a list of patient IDs and a criteria ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tenant_db_name:
            raise ValueError(f"Expected a non-empty value for `tenant_db_name` but received {tenant_db_name!r}")
        return await self._post(
            f"/system/{tenant_db_name}/patient-match-data",
            body=await async_maybe_transform(
                {
                    "criteria_id": criteria_id,
                    "patient_ids": patient_ids,
                },
                system_get_patient_match_data_params.SystemGetPatientMatchDataParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SystemGetPatientMatchDataResponse,
        )

    async def patch_patient_export(
        self,
        patient_ctms_export_id: int,
        *,
        tenant_db_name: str,
        status: ExportStatus,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SystemPatchPatientExportResponse:
        """
        Update a patient CTMS export's status

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tenant_db_name:
            raise ValueError(f"Expected a non-empty value for `tenant_db_name` but received {tenant_db_name!r}")
        return await self._patch(
            f"/system/{tenant_db_name}/patient-ctms-exports/{patient_ctms_export_id}",
            body=await async_maybe_transform(
                {"status": status}, system_patch_patient_export_params.SystemPatchPatientExportParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SystemPatchPatientExportResponse,
        )

    async def ping(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Simple health check endpoint to verify the API is running"""
        return await self._get(
            "/system/ping",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class SystemResourceWithRawResponse:
    def __init__(self, system: SystemResource) -> None:
        self._system = system

        self.create_criteria_instance = to_raw_response_wrapper(
            system.create_criteria_instance,
        )
        self.get_patient_match_data = to_raw_response_wrapper(
            system.get_patient_match_data,
        )
        self.patch_patient_export = to_raw_response_wrapper(
            system.patch_patient_export,
        )
        self.ping = to_raw_response_wrapper(
            system.ping,
        )

    @cached_property
    def protocols(self) -> ProtocolsResourceWithRawResponse:
        return ProtocolsResourceWithRawResponse(self._system.protocols)

    @cached_property
    def criteria(self) -> CriteriaResourceWithRawResponse:
        return CriteriaResourceWithRawResponse(self._system.criteria)

    @cached_property
    def protocol_parsing(self) -> ProtocolParsingResourceWithRawResponse:
        return ProtocolParsingResourceWithRawResponse(self._system.protocol_parsing)

    @cached_property
    def sites(self) -> SitesResourceWithRawResponse:
        return SitesResourceWithRawResponse(self._system.sites)

    @cached_property
    def patients(self) -> PatientsResourceWithRawResponse:
        return PatientsResourceWithRawResponse(self._system.patients)

    @cached_property
    def appointments(self) -> AppointmentsResourceWithRawResponse:
        return AppointmentsResourceWithRawResponse(self._system.appointments)

    @cached_property
    def bulk(self) -> BulkResourceWithRawResponse:
        return BulkResourceWithRawResponse(self._system.bulk)

    @cached_property
    def matching_jobs(self) -> MatchingJobsResourceWithRawResponse:
        return MatchingJobsResourceWithRawResponse(self._system.matching_jobs)

    @cached_property
    def cache(self) -> CacheResourceWithRawResponse:
        return CacheResourceWithRawResponse(self._system.cache)

    @cached_property
    def custom_searches(self) -> CustomSearchesResourceWithRawResponse:
        return CustomSearchesResourceWithRawResponse(self._system.custom_searches)


class AsyncSystemResourceWithRawResponse:
    def __init__(self, system: AsyncSystemResource) -> None:
        self._system = system

        self.create_criteria_instance = async_to_raw_response_wrapper(
            system.create_criteria_instance,
        )
        self.get_patient_match_data = async_to_raw_response_wrapper(
            system.get_patient_match_data,
        )
        self.patch_patient_export = async_to_raw_response_wrapper(
            system.patch_patient_export,
        )
        self.ping = async_to_raw_response_wrapper(
            system.ping,
        )

    @cached_property
    def protocols(self) -> AsyncProtocolsResourceWithRawResponse:
        return AsyncProtocolsResourceWithRawResponse(self._system.protocols)

    @cached_property
    def criteria(self) -> AsyncCriteriaResourceWithRawResponse:
        return AsyncCriteriaResourceWithRawResponse(self._system.criteria)

    @cached_property
    def protocol_parsing(self) -> AsyncProtocolParsingResourceWithRawResponse:
        return AsyncProtocolParsingResourceWithRawResponse(self._system.protocol_parsing)

    @cached_property
    def sites(self) -> AsyncSitesResourceWithRawResponse:
        return AsyncSitesResourceWithRawResponse(self._system.sites)

    @cached_property
    def patients(self) -> AsyncPatientsResourceWithRawResponse:
        return AsyncPatientsResourceWithRawResponse(self._system.patients)

    @cached_property
    def appointments(self) -> AsyncAppointmentsResourceWithRawResponse:
        return AsyncAppointmentsResourceWithRawResponse(self._system.appointments)

    @cached_property
    def bulk(self) -> AsyncBulkResourceWithRawResponse:
        return AsyncBulkResourceWithRawResponse(self._system.bulk)

    @cached_property
    def matching_jobs(self) -> AsyncMatchingJobsResourceWithRawResponse:
        return AsyncMatchingJobsResourceWithRawResponse(self._system.matching_jobs)

    @cached_property
    def cache(self) -> AsyncCacheResourceWithRawResponse:
        return AsyncCacheResourceWithRawResponse(self._system.cache)

    @cached_property
    def custom_searches(self) -> AsyncCustomSearchesResourceWithRawResponse:
        return AsyncCustomSearchesResourceWithRawResponse(self._system.custom_searches)


class SystemResourceWithStreamingResponse:
    def __init__(self, system: SystemResource) -> None:
        self._system = system

        self.create_criteria_instance = to_streamed_response_wrapper(
            system.create_criteria_instance,
        )
        self.get_patient_match_data = to_streamed_response_wrapper(
            system.get_patient_match_data,
        )
        self.patch_patient_export = to_streamed_response_wrapper(
            system.patch_patient_export,
        )
        self.ping = to_streamed_response_wrapper(
            system.ping,
        )

    @cached_property
    def protocols(self) -> ProtocolsResourceWithStreamingResponse:
        return ProtocolsResourceWithStreamingResponse(self._system.protocols)

    @cached_property
    def criteria(self) -> CriteriaResourceWithStreamingResponse:
        return CriteriaResourceWithStreamingResponse(self._system.criteria)

    @cached_property
    def protocol_parsing(self) -> ProtocolParsingResourceWithStreamingResponse:
        return ProtocolParsingResourceWithStreamingResponse(self._system.protocol_parsing)

    @cached_property
    def sites(self) -> SitesResourceWithStreamingResponse:
        return SitesResourceWithStreamingResponse(self._system.sites)

    @cached_property
    def patients(self) -> PatientsResourceWithStreamingResponse:
        return PatientsResourceWithStreamingResponse(self._system.patients)

    @cached_property
    def appointments(self) -> AppointmentsResourceWithStreamingResponse:
        return AppointmentsResourceWithStreamingResponse(self._system.appointments)

    @cached_property
    def bulk(self) -> BulkResourceWithStreamingResponse:
        return BulkResourceWithStreamingResponse(self._system.bulk)

    @cached_property
    def matching_jobs(self) -> MatchingJobsResourceWithStreamingResponse:
        return MatchingJobsResourceWithStreamingResponse(self._system.matching_jobs)

    @cached_property
    def cache(self) -> CacheResourceWithStreamingResponse:
        return CacheResourceWithStreamingResponse(self._system.cache)

    @cached_property
    def custom_searches(self) -> CustomSearchesResourceWithStreamingResponse:
        return CustomSearchesResourceWithStreamingResponse(self._system.custom_searches)


class AsyncSystemResourceWithStreamingResponse:
    def __init__(self, system: AsyncSystemResource) -> None:
        self._system = system

        self.create_criteria_instance = async_to_streamed_response_wrapper(
            system.create_criteria_instance,
        )
        self.get_patient_match_data = async_to_streamed_response_wrapper(
            system.get_patient_match_data,
        )
        self.patch_patient_export = async_to_streamed_response_wrapper(
            system.patch_patient_export,
        )
        self.ping = async_to_streamed_response_wrapper(
            system.ping,
        )

    @cached_property
    def protocols(self) -> AsyncProtocolsResourceWithStreamingResponse:
        return AsyncProtocolsResourceWithStreamingResponse(self._system.protocols)

    @cached_property
    def criteria(self) -> AsyncCriteriaResourceWithStreamingResponse:
        return AsyncCriteriaResourceWithStreamingResponse(self._system.criteria)

    @cached_property
    def protocol_parsing(self) -> AsyncProtocolParsingResourceWithStreamingResponse:
        return AsyncProtocolParsingResourceWithStreamingResponse(self._system.protocol_parsing)

    @cached_property
    def sites(self) -> AsyncSitesResourceWithStreamingResponse:
        return AsyncSitesResourceWithStreamingResponse(self._system.sites)

    @cached_property
    def patients(self) -> AsyncPatientsResourceWithStreamingResponse:
        return AsyncPatientsResourceWithStreamingResponse(self._system.patients)

    @cached_property
    def appointments(self) -> AsyncAppointmentsResourceWithStreamingResponse:
        return AsyncAppointmentsResourceWithStreamingResponse(self._system.appointments)

    @cached_property
    def bulk(self) -> AsyncBulkResourceWithStreamingResponse:
        return AsyncBulkResourceWithStreamingResponse(self._system.bulk)

    @cached_property
    def matching_jobs(self) -> AsyncMatchingJobsResourceWithStreamingResponse:
        return AsyncMatchingJobsResourceWithStreamingResponse(self._system.matching_jobs)

    @cached_property
    def cache(self) -> AsyncCacheResourceWithStreamingResponse:
        return AsyncCacheResourceWithStreamingResponse(self._system.cache)

    @cached_property
    def custom_searches(self) -> AsyncCustomSearchesResourceWithStreamingResponse:
        return AsyncCustomSearchesResourceWithStreamingResponse(self._system.custom_searches)
