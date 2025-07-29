#!/usr/bin/env python3

import shlex
from collections.abc import Sequence
from pathlib import PurePath, PurePosixPath

from attrs import define, evolve, field

from .checks import (
    check_is_darwin,
    check_is_debian,
    check_is_debian_10,
    check_is_debian_11,
    check_is_debian_12,
    check_is_debian_13,
    check_is_debian_14,
    check_is_debian_15,
    check_is_debian_like,
    check_is_linux,
    check_is_windows,
    check_is_windows7,
    check_is_windows8,
    check_is_windows10,
    check_is_windows11,
    check_is_windows12,
)
from .common import run, run_bg
from .linux_methods import (
    linux_get_cpu_cores,
    linux_list_processes,
    linux_pgrep,
    linux_setup_deb_node,
    linux_setup_node,
)
from .protocol import (
    GetCPUCoresCallable,
    ListProcessesCallable,
    PgrepCallable,
    QuoteCallable,
    RunBgCallable,
    RunCallable,
    SetupNodeCallable,
    SSHCheck,
)
from .windows_methods import (
    MyPureWindowsPath,
    windows_get_cpu_cores,
    windows_list_processes,
    windows_pgrep,
    windows_quote,
    windows_setup_node,
)


@define(frozen=True)
class RemoteMachineAdapter:
    "Remote machine adapter"

    platform: str = field()
    path: type[PurePath] = field()

    quote: QuoteCallable = field()
    run: RunCallable = field()
    run_bg: RunBgCallable = field()
    get_cpu_cores: GetCPUCoresCallable = field()
    list_processes: ListProcessesCallable = field()
    pgrep: PgrepCallable = field()
    setup_node: SetupNodeCallable = field()

    checks: Sequence[SSHCheck] = field(factory=tuple)


linux_adapter = RemoteMachineAdapter(
    platform="linux",
    path=PurePosixPath,
    quote=shlex.quote,
    run=run,
    run_bg=run_bg,
    get_cpu_cores=linux_get_cpu_cores,
    list_processes=linux_list_processes,
    pgrep=linux_pgrep,
    setup_node=linux_setup_node,
    checks=(check_is_linux,),
)

debian_like_adapter = evolve(
    linux_adapter,
    platform="debian-like",
    setup_node=linux_setup_deb_node,
    checks=(*linux_adapter.checks, check_is_debian_like),
)

debian_adapter = evolve(
    debian_like_adapter,
    platform="debian",
    checks=(*debian_like_adapter.checks, check_is_debian),
)

debian_10_adapter = evolve(
    debian_adapter,
    platform="debian-10",
    checks=(*debian_adapter.checks, check_is_debian_10),
)

debian_11_adapter = evolve(
    debian_adapter,
    platform="debian-11",
    checks=(*debian_adapter.checks, check_is_debian_11),
)

debian_12_adapter = evolve(
    debian_adapter,
    platform="debian-12",
    checks=(*debian_adapter.checks, check_is_debian_12),
)

debian_13_adapter = evolve(
    debian_adapter,
    platform="debian-13",
    checks=(*debian_adapter.checks, check_is_debian_13),
)

debian_14_adapter = evolve(
    debian_adapter,
    platform="debian-14",
    checks=(*debian_adapter.checks, check_is_debian_14),
)

debian_15_adapter = evolve(
    debian_adapter,
    platform="debian-15",
    checks=(*debian_adapter.checks, check_is_debian_15),
)

darwin_adapter = evolve(
    linux_adapter,
    platform="darwin",
    checks=(check_is_darwin,),
)

windows_adapter = RemoteMachineAdapter(
    platform="windows",
    path=MyPureWindowsPath,
    quote=windows_quote,
    run=run,
    run_bg=run_bg,
    get_cpu_cores=windows_get_cpu_cores,
    list_processes=windows_list_processes,
    pgrep=windows_pgrep,
    setup_node=windows_setup_node,
    checks=(check_is_windows,),
)

windows7_adapter = evolve(
    windows_adapter,
    platform="windows-8",
    checks=(*windows_adapter.checks, check_is_windows7),
)

windows8_adapter = evolve(
    windows_adapter,
    platform="windows-8",
    checks=(*windows_adapter.checks, check_is_windows8),
)

windows10_adapter = evolve(
    windows_adapter,
    platform="windows-10",
    checks=(*windows_adapter.checks, check_is_windows10),
)

windows11_adapter = evolve(
    windows_adapter,
    platform="windows-11",
    checks=(*windows_adapter.checks, check_is_windows11),
)

windows12_adapter = evolve(
    windows_adapter,
    platform="windows-12",
    checks=(*windows_adapter.checks, check_is_windows12),
)
