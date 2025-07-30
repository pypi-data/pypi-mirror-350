# SPDX-FileCopyrightText: © 2025 Evotis S.A.S.
# SPDX-License-Identifier: Elastic-2.0
# "Pipelex" is a trademark of Evotis S.A.S.

from typing import Any, Callable

from pydantic import BaseModel


class ActivityReport(BaseModel):
    content: Any


ActivityCallback = Callable[[ActivityReport], None]
