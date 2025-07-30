#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import http
import pathlib
import typing

import httpx
import pydantic
import rich
import typer

from pendingai import config
from pendingai.api import ApiClient
from pendingai.commands.retro.batch.models import (
    Batch,
    BatchJobResult,
    BatchPage,
    BatchStatus,
)
from pendingai.context import Context

console = rich.console.Console(theme=config.RICH_CONSOLE_THEME, soft_wrap=True)


class RetroBatchController:
    """
    Controller for `pendingai retro batch` subcommands. Controls batch
    retrosynthesis operations for captured named commands in the app
    like providing CRUD methods.

    Args:
        context (Context): App runtime context.
    """

    def __init__(self, context: Context) -> None:
        self.context: Context = context
        self.api: ApiClient = ApiClient(
            base_url=config.API_BASE_URLS[self.context.obj.environment],
            subdomain=config.RETRO_SUBDOMAIN,
            bearer_token=self.context.obj.cache.access_token,
        )

    def check_batch_exists(self, batch_id: str) -> bool:
        """
        Check a batch exists by the batch resource id.

        Args:
            batch_id (str): Batch resource id.

        Returns:
            bool: Batch exists.
        """
        with console.status(f"Checking batch exists: {batch_id}"):
            r: httpx.Response = self.api.get(f"/batches/{batch_id}", skip_errors=True)
        return r.status_code == 200

    # region create ----------------------------------------------------

    def create_batch(
        self,
        input_file: pathlib.Path,
        retrosynthesis_engine: str,
        building_block_libraries: list[str],
        number_of_routes: int,
        processing_time: int,
        reaction_limit: int,
        building_block_limit: int,
        filename: str | None = None,
    ) -> Batch:
        """
        Create a batch of retrosynthesis jobs from an input file and set
        of job parameters by calling the api layer. Parse the response
        into the batch object and handle submission failures.

        Args:
            input_file (pathlib.Path): File containing line-delimited
                smiles strings for each requested job.
            retrosynthesis_engine (str): Retrosynthesis engine id.
            building_block_libraries (list[str]): Building block library
                ids.
            number_of_routes (int): Maximum number of retrosynthetic
                routes to generate.
            processing_time (int): Maximum processing time in seconds.
            reaction_limit (int): Maximum number of times a specific
                reaction can appear in generated retrosynthetic routes.
            building_block_limit (int): Maximum number of times a
                building block can appear in a retrosynthetic route.
            filename (str, optional): Sanitized filename used for the
                batch submission as added metadata.

        Raises:
            typer.Exit: Failed to submit the batch request with an
                unexpected status code or invalid response data.

        Returns:
            Batch: Submitted batch object.
        """
        # build parameter dict for the request, note that job parameters
        # are not nested and are currently given as snake-case keys.
        params: dict = {
            "engine": retrosynthesis_engine,
            "libraries": building_block_libraries,
            "max-routes": number_of_routes,
            "processing-time": processing_time,
            "reaction-limit": reaction_limit,
            "building-block-limit": building_block_limit,
            "filename": filename,
        }

        # request the batch submission by sending the input file bytes
        # and the endpoint will automatically de-duplicate and repeated
        # smiles strings in the request; set content-type header.
        with console.status(f"Submitting batch file: {input_file}"):
            r: httpx.Response = self.api.post(
                "/batches",
                data=input_file.read_bytes(),
                params=params,
                headers={"Content-Type": "text/plain"},
            )
        if r.status_code == http.HTTPStatus.OK:
            try:
                return Batch.model_validate(r.json())
            except pydantic.ValidationError:
                pass

        # error otherwise if the batch submission failed in any way like
        # the response was malformed or the status code was unexpected.
        console.print("[fail]Failed to submit batch request, please try again.")
        raise typer.Exit(1)

    # region retrieve --------------------------------------------------

    def retrieve_batch_list(
        self,
        page: int = 1,
        page_size: int = 50,
    ) -> BatchPage | None:
        """
        Retrieve a page of batch results using the api layer and input
        query parameters given on the command line by the user. Coerce
        the result into a batch page response.

        Args:
            pagination_key (str, optional): Batch resource id that gives
                the next page lookup location for more batch resources.
            page_size (int, optional): Page size parameter sets how many
                results are returned by the api layer.

        Raises:
            typer.Exit: Batch response contains unexpected data or an
                unhandled status code.

        Returns:
            BatchPage: Paginated batch resource data.
        """
        # request page of batches from the api, only respond on success
        # with valid paginated response, else return non-zero status.
        with console.status(f"Retrieving page {page} of batches..."):
            r: httpx.Response = self.api.get(
                "/batches",
                params={"page-size": page_size, "page": page},
                skip_errors=True,
            )
        if r.status_code == http.HTTPStatus.OK:
            try:
                return BatchPage.model_validate(r.json())
            except pydantic.ValidationError:
                pass
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            return None
        console.print("[fail]Unable to retrieve page of batches.")
        raise typer.Exit(1)

    def retrieve_batch_result_by_batch_id(self, batch_id: str) -> list[BatchJobResult]:
        """
        Retrieves a list of individual batch job results. Handles edge
        conditions of when a batch is still in progress or a batch does
        not exist.

        Args:
            batch_id (str): Batch resource id.

        Raises:
            typer.Exit: Batch does not exist or is still processing.

        Returns:
            list[BatchJobResult]: Batch results for each job.
        """
        # retrieve the batch results from the api with a console status
        # spinner in case the api call is hanging or times out for being
        # too slow.
        with console.status(f"Retrieving results for {batch_id}"):
            r: httpx.Response = self.api.get(
                f"/batches/{batch_id}/result",
                skip_errors=True,
            )

        if r.status_code == http.HTTPStatus.OK:
            # parse a completed result for the batch iterating over each
            # job result and constructing a set of response objects.
            result: list[BatchJobResult] = []
            for x in r.json():
                try:
                    result.append(BatchJobResult.model_validate(x))
                except pydantic.ValidationError:
                    continue
            return result

        console.print("[warn]! Batch was not found.")
        raise typer.Exit(1)

    def retrieve_batch_status_by_batch_id(self, batch_id: str) -> BatchStatus:
        """
        Retrieve the status of a batch by its batch resource id. Handles
        if a batch does not exist or the status is not valid for a user.

        Args:
            batch_id (str): Batch resource id for retrieving the status.

        Raises:
            typer.Exit: Batch resource id was not found or an invalid
                status response was received from the api layer.

        Returns:
            BatchStatus: Batch status flag.
        """
        # request the status of the batch from the api layer; request is
        # quite slow since it inspects status of all jobs; return the
        # result and only return if the status is provided and valid,.
        with console.status(f"Retrieving status for batch: {batch_id}"):
            r: httpx.Response = self.api.get(
                f"/batches/{batch_id}/status",
                skip_errors=True,
            )
        if r.status_code == http.HTTPStatus.OK:
            if status := r.json().get("status", None):
                try:
                    return BatchStatus(status)  # Convert string to enum instance
                except ValueError:
                    # exit here; below chunk handles this conditon.
                    pass

        # treat all failed requests as if the status was not found to
        # make responses easier for the user.
        console.print("[warn]! Batch status was not found.")
        raise typer.Exit(1)

    # region update ----------------------------------------------------

    # region delete ----------------------------------------------------

    def delete_batch(self, batch_id: str) -> typing.Literal[True]:
        """
        Delete a batch resource by id. Call the rest api with the batch
        id to initiate the delete operation; handle the different codes
        from the response.

        Args:
            batch_id (str): Batch resource id.

        Raises:
            typer.Exit: Delete operation responded with an unexpected
                status code from the rest api.

        Returns:
            bool: Delete operation request was successful.
        """
        with console.status(f"Deleting batch: {batch_id}"):
            r: httpx.Response = self.api.delete(f"/batches/{batch_id}", skip_errors=True)

        # parse the status code to know the state of the delete api
        # request; handle when it is still in progress, does not exist
        # or completes as expected.
        if r.status_code == http.HTTPStatus.NO_CONTENT:
            console.print("[success]✓ Batch was deleted successfully.")
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            console.print("[warn]! Batch was not found.")
        elif r.status_code == http.HTTPStatus.CONFLICT:
            console.print("[warn]! Batch is still in progress.")
        else:
            console.print("[fail]Failed to delete batch, please try again.")
            raise typer.Exit(1)
        return True
