"""Fold sequences using Arcadia's folding server.

Usage:
    $ apb-fold --help
"""

from __future__ import annotations
import asyncio
import logging
import random
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Any

import aiohttp
import attrs
import biotite.sequence.io.fasta as fasta
import cattrs
import pandas as pd
import typer
import yaml
from dateutil.parser import isoparse
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    ProgressColumn,
    TaskID,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.prompt import Prompt
from slugify import slugify

from apb.config import CONFIG_DIR, ensure_config_dir_exists

app = typer.Typer(
    help="Fold protein sequences using Arcadia's folding server.",
    add_completion=False,
    pretty_exceptions_show_locals=False,
)
console = Console()

logging.basicConfig(level="INFO", format="%(message)s", handlers=[RichHandler(console=console)])
logger = logging.getLogger("rich")

# Create a converter and register a structure hook for datetime
converter = cattrs.Converter()
converter.register_structure_hook(datetime, lambda dt_str, _: isoparse(dt_str) if dt_str else None)

FOLD_CONFIG_DIR = CONFIG_DIR / "fold_server"
FOLD_CREDENTIALS = FOLD_CONFIG_DIR / "credentials.yaml"

FETCH_TIMEOUT: int = 60 * 60 * 10  # Total time to keep retrying (in seconds)
INITIAL_RETRY_DELAY: float = 10  # Initial delay in seconds
BACKOFF_FACTOR: float = 1.03  # Exponential backoff factor


def get_url_and_token() -> tuple[str, str]:
    ensure_config_dir_exists()

    if not FOLD_CREDENTIALS.exists():
        console.print(
            Panel(
                "[red]Credentials not found![/red]\n\n"
                "Please run [bold]apb-fold setup[/bold] first to configure your API credentials.",
                title="Configuration Required",
                border_style="red",
            )
        )
        raise typer.Exit(code=1)

    with open(FOLD_CREDENTIALS) as f:
        config = yaml.safe_load(f)

    api_url = config.get("api_url")
    bearer_token = config.get("bearer_token")

    if not api_url or not bearer_token:
        console.print(
            Panel(
                f"[red]api_url and/or bearer_token missing[/red]\n\n"
                f"Run [bold]apb-fold setup[/bold] or update {FOLD_CREDENTIALS} manually.",
                title="Configuration Error",
                border_style="red",
            )
        )
        raise typer.Exit(code=1)

    return api_url, bearer_token


@attrs.define
class Response:
    # Present in /fold and /result responses
    job_id: str
    sequence: str
    pdb_uri: str | None
    status: str
    device_type: str
    failure_reason: str | None
    created_at: datetime
    updated_at: datetime
    folding_model: str

    # Present in /result resonses
    pdb_content: str | None = None

    @property
    def runtime(self) -> float:
        """Number of sequences between updated_at and created_at"""
        return (self.updated_at - self.created_at).total_seconds()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Response:
        return converter.structure(data, Response)


async def submit_job(
    session: aiohttp.ClientSession, sequence: str, api_url: str, headers: dict[str, str]
) -> Response | None:
    url: str = f"{api_url}/fold"
    data: dict[str, str] = {"protein_sequence": sequence}

    async with session.post(url, json=data, headers=headers) as response:
        if response.status == 200:
            response_json = await response.json()
            return Response.from_dict(response_json)

    console.print(
        f"[bold]Failed[/bold] submission for '{sequence}'. Response: {response.status}", style="red"
    )

    return None


def _get_most_recently_succeeded(results: list[Response]) -> Response | None:
    succeeded_results = [result for result in results if result.status == "SUCCEEDED"]
    if succeeded_results:
        return max(succeeded_results, key=lambda r: r.updated_at)

    return None


async def fetch_result(
    session: aiohttp.ClientSession, job_id: str | None, api_url: str, headers: dict[str, str]
) -> Response | None:
    if job_id is None:
        return None

    url: str = f"{api_url}/result/{job_id}"

    attempt: int = 0
    delay: float = INITIAL_RETRY_DELAY
    cumulative_delay: float = 0

    while cumulative_delay + delay < FETCH_TIMEOUT:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                response_json = await response.json()

                # /result endpoint always returns a list of jobs
                results = [Response.from_dict(job_json) for job_json in response_json]
                result = _get_most_recently_succeeded(results)

                if result is not None:
                    msg = (
                        f"[bold]Folded[/bold] {result.job_id} "
                        f"({result.updated_at}) "
                        f"[bold][magenta]{result.sequence}"
                    )
                    console.print(msg, style="green")
                    return result
            else:
                console.print(
                    f"Error fetching job {job_id}. Status code: {response.status}. "
                    f"Attempt {attempt + 1}.",
                    style="red",
                )

        logger.debug(f"Job {job_id}: attempt {attempt} failed. Trying again in {delay} seconds.")
        jitter = random.uniform(0, delay * 0.1)
        await asyncio.sleep(delay + jitter)

        cumulative_delay += delay
        attempt += 1
        delay = INITIAL_RETRY_DELAY * (BACKOFF_FACTOR**attempt)

    console.print(
        f"Failed to fetch result for job {job_id} after exceeding the timeout of "
        f"{FETCH_TIMEOUT} seconds.",
        style="red",
    )

    return None


def _update_progress(task: asyncio.Task, progress: Progress, progress_task_id: TaskID) -> None:
    assert task.done()
    progress.advance(progress_task_id)


async def fold(sequences: dict[str, str], output: Path | str, quiet: bool = False) -> Path:
    console.quiet = quiet

    api_url, token = get_url_and_token()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    output = Path(output)
    output.mkdir(exist_ok=True)

    progress_columns: list[ProgressColumn] = [
        TextColumn("{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn("[progress.percentage]{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
    ]

    if not quiet:
        msg = (
            "[green][bold] Job Information[/bold]\n"
            "• Once all jobs have submitted, they will continue running on the server even\n"
            "  if you close this terminal\n"
            "• At that point you can safely cancel this command or close your laptop - your\n"
            "  jobs will keep processing\n"
            "• To retrieve results later, simply run this same command again - previously\n"
            "  completed jobs are cached and won't be re-folded\n"
            "• Once all jobs are finished, this command will download the results to your local"
            "[/green]"
        )
        console.print(
            Panel(
                msg,
                border_style="green",
                title="[bold]Fold Server Jobs[/bold]",
                expand=False,
            )
        )

    with Progress(*progress_columns, console=console) as progress:
        submitting_progress_id = progress.add_task("[cyan]Submitting...", total=len(sequences))
        fetching_progress_id = progress.add_task("[cyan]Fetching...", total=len(sequences))

        update_submit = partial(
            _update_progress, progress=progress, progress_task_id=submitting_progress_id
        )
        update_fetch = partial(
            _update_progress, progress=progress, progress_task_id=fetching_progress_id
        )

        async with aiohttp.ClientSession() as session:
            submission_tasks: list[asyncio.Task] = []
            for sequence in sequences.values():
                task = asyncio.create_task(submit_job(session, sequence, api_url, headers))
                task.add_done_callback(update_submit)
                submission_tasks.append(task)

            submission_responses: list[Response | None] = await asyncio.gather(*submission_tasks)

            fetch_tasks: list[asyncio.Task] = []
            for job in submission_responses:
                task = asyncio.create_task(
                    fetch_result(session, job.job_id if job else None, api_url, headers)
                )
                task.add_done_callback(update_fetch)
                fetch_tasks.append(task)

            fold_results: list[Response | None] = await asyncio.gather(*fetch_tasks)

        progress.refresh()

    failures: list[dict[str, str | None]] = []

    for (seq_id, seq), fold_request, fold_result in zip(
        sequences.items(), submission_responses, fold_results, strict=True
    ):
        if fold_request is None:
            # Failed request
            failures.append(
                {"seq_id": seq_id, "failure": "submission", "job_id": None, "sequence": seq}
            )
        elif fold_result is None:
            # Failed fold / timeout
            failures.append(
                {
                    "seq_id": seq_id,
                    "failure": "fetch",
                    "job_id": fold_request.job_id,
                    "sequence": seq,
                }
            )
        else:
            # Success
            assert fold_result.status == "SUCCEEDED"
            assert fold_result.pdb_content is not None
            filename_safe_seq_id = slugify(seq_id)
            output_path = output / f"{filename_safe_seq_id}.pdb"
            with open(output_path, "w") as fp:
                fp.write(fold_result.pdb_content)

    if failures:
        failure_df = pd.DataFrame(failures)
        failure_path = output / "_failures.tsv"
        failure_df.to_csv(failure_path, sep="\t", index=False)

    console.print(f"Results saved in [bold]{output}[/bold]", style="green")

    return output


def setup_credentials() -> None:
    """Setup API credentials for the fold server."""
    ensure_config_dir_exists()

    console.print(
        Panel(
            "[bold cyan]Arcadia's Folding Server Setup[/bold cyan]\n\n"
            "This will configure your API credentials for Arcadia's folding server.\n"
            "You'll need to provide your API URL and Bearer Token. Please ping the \n"
            "Software Team for these two pieces of information.",
            title="Welcome",
            border_style="cyan",
        )
    )

    FOLD_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    api_url = Prompt.ask("[bold]API URL[/bold]").rstrip("/")
    bearer_token = Prompt.ask("[bold]Bearer Token[/bold]", password=True)

    if not api_url or not bearer_token:
        console.print("[red]Both API URL and Bearer Token are required![/red]")
        raise typer.Exit(code=1)

    credentials = {"api_url": api_url, "bearer_token": bearer_token}

    with open(FOLD_CREDENTIALS, "w") as f:
        yaml.safe_dump(credentials, f, default_flow_style=False)

    console.print(
        Panel(
            f"[green]✓ Credentials saved successfully![/green]\n\n"
            f"Configuration saved to: [dim]{FOLD_CREDENTIALS}[/dim]\n\n"
            "You can now use [bold]apb-fold run[/bold] to submit folding jobs.",
            title="Setup Complete",
            border_style="green",
        )
    )


@app.command()
def setup() -> None:
    """Configure API credentials for the fold server."""
    setup_credentials()


@app.command()
def run(
    fasta_file: Path = typer.Option(  # noqa: B008
        ...,
        "--fasta-file",
        "-f",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help="Path to FASTA file containing sequences to fold.",
    ),
    output_dir: Path = typer.Option(  # noqa: B008
        ...,
        "--output-dir",
        "-o",
        file_okay=False,
        dir_okay=True,
        writable=True,
        help="Directory where folded structures (.pdb) will be written.",
    ),
    quiet: bool = typer.Option(  # noqa: B008
        False,
        "--quiet",
        "-q",
        help="Suppress progress output.",
    ),
) -> None:
    """Fold protein sequences from a FASTA file."""
    sequences = dict(fasta.FastaFile.read(fasta_file).items())
    asyncio.run(fold(sequences, output_dir, quiet=quiet))


if __name__ == "__main__":
    app()
