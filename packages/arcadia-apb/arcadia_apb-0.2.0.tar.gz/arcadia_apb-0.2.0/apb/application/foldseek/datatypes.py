from pathlib import Path

import attrs


@attrs.define(frozen=True)
class FoldseekOutputFileNotFoundError(Exception):
    path: Path
    command: list[str]

    @property
    def command_string(self) -> str:
        return " ".join(self.command)

    def __str__(self) -> str:
        return (
            f"Expected foldseek (`{self.command_string}`) to produce file '{self.path}', "
            "but it doesn't exist."
        )


@attrs.define(frozen=True)
class FoldSeekSearchConfig:
    """Parameter structuring for foldseek's search subcommand

    See `foldseek search -h` for details.
    """

    backtrace: bool | None = attrs.field(default=None)
    prefilter_mode: int | None = attrs.field(default=None)
    alignment_type: int | None = attrs.field(default=None)
    tmalign_fast: int | None = attrs.field(default=None)
    exact_tmscore: int | None = attrs.field(default=None)

    def parameters(self) -> list[str]:
        flag_strings = []

        if self.backtrace:
            flag_strings.append("-a")

        if self.prefilter_mode is not None:
            flag_strings.extend(["--prefilter-mode", str(self.prefilter_mode)])

        if self.alignment_type is not None:
            flag_strings.extend(["--alignment-type", str(self.alignment_type)])

        if self.tmalign_fast is not None:
            flag_strings.extend(["--tmalign-fast", str(int(self.tmalign_fast))])

        if self.exact_tmscore is not None:
            flag_strings.extend(["--exact-tmscore", str(int(self.exact_tmscore))])

        return flag_strings


@attrs.define(frozen=True)
class FoldSeekConvertalisConfig:
    """Parameter structuring for foldseek's convertalis subcommand

    See `foldseek convertalis -h` for details.
    """

    format_output: str | None = attrs.field(default=None)
    exact_tmscore: int | None = attrs.field(default=None)

    def parameters(self) -> list[str]:
        flag_strings = []

        if self.format_output is not None:
            flag_strings.extend(["--format-output", self.format_output])

        if self.exact_tmscore is not None:
            flag_strings.extend(["--exact-tmscore", str(int(self.exact_tmscore))])

        return flag_strings
