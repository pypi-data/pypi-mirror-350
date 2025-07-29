from __future__ import annotations

import dataclasses

from typing import TYPE_CHECKING

from pubtools.sign.operations.base import SignOperation
from pubtools.sign.results import SignerResults
from pubtools.sign.results.operation_result import OperationResult

if TYPE_CHECKING:  # pragma: no cover
    from pubtools.sign.signers import Signer


@dataclasses.dataclass
class SigningResults:
    """SigningResults model."""

    signer: Signer
    operation: SignOperation
    signer_results: SignerResults
    operation_result: OperationResult
