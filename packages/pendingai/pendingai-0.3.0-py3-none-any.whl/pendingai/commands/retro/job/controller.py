#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import base64
import http
import pathlib

import httpx
import pydantic
import rich
import typer

from pendingai import config
from pendingai.api import ApiClient
from pendingai.commands.retro.job.models import JobPage
from pendingai.context import Context
from pendingai.utils.formatters import format_filesize

console = rich.console.Console(theme=config.RICH_CONSOLE_THEME, soft_wrap=True)


class RetroJobController:
    """
    Controller for `pendingai retro job` subcommands. Controls specific
    retrosynthesis job operations for CRUD-like commands against single
    jobs with a provided retrosynthesis engine.

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

    def create_job(
        self,
        smiles: str,
        retrosynthesis_engine: str | None,
        building_block_libraries: list[str] | None,
        number_of_routes: int,
        processing_time: int,
        reaction_limit: int,
        building_block_limit: int,
    ) -> str:
        """
        Submit a single retrosynthesis job and retrieve the newly created
        job id returned by the api layer.

        Args:
            context (Context): App runtime context.
            smiles (str): Smiles query molecule.
            retrosynthesis_engine (str, optional): Retrosynthesis engine
                id. Defaults to primary engine.
            building_block_libraries (list[str], optional): Building block
                library ids. Defaults to all available libraries.
            number_of_routes (int, optional): Maximum number of
                retrosynthetic routes to generate. Defaults to 20.
            processing_time (int, optional): Maximum processing time in
                seconds. Defaults to 300.
            reaction_limit (int, optional): Maximum number of times a
                specific reaction can appear in generated retrosynthetic
                routes. Defaults to 3.
            building_block_limit (int, optional): Maximum number of times a
                building block can appear in a single retrosynthetic route.
                Default to 3.
            render_json (bool, optional): Render output as json.

        Raises:
            typer.Exit: Failed to submit retrosynthesis job.

        Returns:
            str: Retrosynthesis job id.
        """
        # build out the input json body and parameters nested field from
        # input parameters, add a single smiles and optional
        # engines and libraries.
        body: dict = {
            "query": smiles,
            "parameters": {
                "number_of_routes": number_of_routes,
                "processing_time": processing_time,
                "reaction_limit": reaction_limit,
                "building_block_limit": building_block_limit,
            },
        }
        if retrosynthesis_engine:
            body["parameters"]["retrosynthesis_engine"] = retrosynthesis_engine
        if building_block_libraries:
            body["parameters"]["building_block_libraries"] = building_block_libraries

        # request to submit the job, process only the 202 status code on
        # completion and pull the result from the location header; exit
        # with non-zero status on failure.
        with console.status("Submitting query molecule..."):
            r: httpx.Response = self.api.post("/queries", json=body)
        if r.status_code == http.HTTPStatus.ACCEPTED:
            try:
                return r.headers.get("Location").split("/")[-2]
            except Exception:
                pass

        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            console.print("[warn]! Unable to find requested engine or libraries.")
            raise typer.Exit(1)
        elif r.status_code == http.HTTPStatus.SERVICE_UNAVAILABLE:
            console.print("[warn]! There are not available engine or libraries.")
            console.print("[warn]! Please contact support to resolve the issue.")
            raise typer.Exit(1)
        elif r.status_code == http.HTTPStatus.PAYMENT_REQUIRED:
            console.print("[warn]! Failed to process the payment, try again shortly.")
            raise typer.Exit(1)

        console.print("[warn]! Failed to submit retrosynthesis job, try again shorty.")
        raise typer.Exit(1)

    def retrieve_jobs(
        self,
        page: int,
        page_size: int,
        filter_status: str | None = None,
    ) -> JobPage:
        """
        Retrieve a paginated collection of retrosynthesis jobs for a set
        of optional filter conditions and page lookup parameters.

        Args:
            page (int): Page number being fetched.
            page_size (int): Page size for the paginated response.
            filter_status (str, optional): Filter value for status.

        Raises:
            typer.Exit: No retrosynthesis page data was returned; the
                page data was invalid or an unexpected http status code
                was received from the api layer.

        Returns:
            JobPage: Paginated retrosynthesis jobs.
        """
        # build the parameters for the http request based on the page
        # filtering options given as arguments.
        params: dict = {"page-number": page, "page-size": page_size}
        if filter_status is not None:
            params["status"] = filter_status

        # make the request with a spinner status since it can take a
        # while filtering many jobs with the optional status filter.
        with console.status(f"Retrieving page {page} of jobs..."):
            r: httpx.Response = self.api.get("/queries", params=params, skip_errors=True)

        # process json response body into the jobs page data model; if
        # the model validation fails return a non-zero exit status.
        if r.status_code == 200:
            try:
                page_data: JobPage = JobPage.model_validate(r.json())
                page_data.data.sort(key=lambda x: x.created)
                return page_data
            except pydantic.ValidationError:
                console.print("[warn]! Unexpected data from server, contact support.")
                raise typer.Exit(1)
        # capture the error conditions where no jobs page is returned by
        # the api layer or that a different status code is received that
        # was unexpected.
        elif r.status_code == 404:
            console.print("[warn]! No results found for the given filter.")
            raise typer.Exit(0)
        console.print("[fail]Failed retrieving jobs, try again shortly.")
        raise typer.Exit(1)

    def retrieve_job_status(self, job_id: str) -> str:
        """
        Retrieve the status of a single retrosynthesis job by id.

        Args:
            job_id (str): Retrosynthesis job id.

        Raises:
            typer.Exit: Requested job id does not exist or was invalid.

        Returns:
            str: Retrosynthesis job status.
        """
        # give a spinner status while retrieving the job status from the
        # api on a given job id, skip errors to handle edge cases like
        # when the job is not found.
        with console.status("Retrieving job status..."):
            r: httpx.Response = self.api.request(
                "GET", f"/queries/{job_id}/status", skip_errors=True
            )

        if r.status_code == http.HTTPStatus.OK:
            return r.json().get("status", "submitted")
        elif r.status_code == http.HTTPStatus.SEE_OTHER:
            return "completed"
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            console.print(f"[warn]! Retrosynthesis job not found: [not b]{job_id}")
        elif r.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY:
            console.print(f"[warn]! Invalid retrosynthesis job ID: [not b]{job_id}")
        raise typer.Exit(1)

    def retrieve_job_result(self, job_id: str) -> dict | None:
        """
        Retrieve a single retrosynthesis job result by id.

        Args:
            job_id (str): Retrosynthesis job id.

        Returns:
            dict: Retrosynthesis job result if it exists and is done.
        """
        r: httpx.Response = self.api.request(
            "GET", f"/queries/{job_id}", skip_errors=True
        )
        if r.status_code == http.HTTPStatus.OK:
            if r.json().get("status", "failed") == "completed":
                return r.json()
        return None

    def delete_job(self, job_id: str) -> bool:
        """
        Delete a retrosynthesis job by id.

        Args:
            job_id (str): Retrosynthesis job id.

        Raises:
            typer.Exit: Retrosynthesis job does not exist.

        Returns:
            bool: Success of the delete operation.
        """
        # give a spinner status while deleting the job using the api on
        # a given job id, skip errors to handle edge cases like when the
        # job is not found.
        with console.status("Deleting job..."):
            r: httpx.Response = self.api.request(
                "DELETE", f"/queries/{job_id}", skip_errors=True
            )

        if r.status_code == http.HTTPStatus.NO_CONTENT:
            return True
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            console.print(f"[warn]! Retrosynthesis job not found: [not b]{job_id}")
            raise typer.Exit(1)
        elif r.status_code == http.HTTPStatus.CONFLICT:
            console.print(f"[warn]! Retrosynthesis job is in progress: [not b]{job_id}")
            raise typer.Exit(1)
        return False

    def retrieve_job_pdf(self, job_id: str, path: pathlib.Path) -> None:
        """
        Process a retrosynthesis route pdf generation request for a
        single job id and output filepath; parse base64 encoded response
        body data and report on the size of the file, otherwise give
        feedback on the error i.e., that the job does not exist.

        Args:
            job_id (str): Retrosynthesis job id.
            path (pathlib.Path): Save path for the generated job result.

        Raises:
            typer.Exit: Pdf generation failed when parsing response data
                or an unknown error occurred when creating the file.
        """
        with console.status(f"Generating PDF for job: {job_id}"):
            r: httpx.Response = self.api.request(
                "GET", f"/queries/{job_id}/depict", skip_errors=True
            )

        # check response status code to determine the status of the job
        # where a 204 means no job routes exist and 200 has valid routes
        # to store as a pdf document.
        if r.status_code == http.HTTPStatus.OK:
            with open(path, "wb") as fp:
                try:
                    content: bytes = base64.decodebytes(r.json().encode())
                    filesize: str = format_filesize(len(content))
                    fp.write(content)
                except Exception:
                    console.print(f"[warn]! Failed saving job PDF, try again: {job_id}")
                    raise typer.Exit(1)
            console.print(f"[success][not b]✓ Job results saved: {path} ({filesize})")

        # edge cases can exit normally since the outer function may be
        # processing a mini-batch, this method will only fail if unknown
        # status is given by the api.
        elif r.status_code == http.HTTPStatus.CONFLICT:
            console.print(f"[warn]! Job is in progress: {job_id}")
        elif r.status_code == http.HTTPStatus.NO_CONTENT:
            console.print(f"[warn]! Job has no routes: {job_id}")
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            console.print(f"[warn]! Job was not found: {job_id}")
        else:
            console.print(f"[warn]! Failed saving job PDF, try again: {job_id}")
            raise typer.Exit(1)
