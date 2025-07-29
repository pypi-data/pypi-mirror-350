import inspect
from base64 import urlsafe_b64encode
from collections.abc import Callable
from typing import Awaitable, ParamSpec

from atlantiscore.hash.ecdsa import EIP712Signer
from atlantiscore.types import EVMAddress
from fastapi import Depends, Response

from atlantisfastapi.lib.signature import copy_parameters

P = ParamSpec("P")


class HTTPBodySigner:
    signer: EIP712Signer

    def __init__(self, signer: EIP712Signer) -> None:
        self.signer = signer

    def create_signature_headers(
        self,
        body: dict,
        primary_type: str,
        additional_types: dict = {},
    ) -> dict[str, str]:
        key_id = self._signing_public_address
        signature = self._sign_body(body, primary_type, additional_types)
        return {
            "Signature-Input": f'signature=();alg="keccak";keyId="{key_id}"',
            "Signature": f"signature=:{signature}:",
        }

    @property
    def _signing_public_address(self) -> EVMAddress:
        return self.signer.private_key.public_address

    def _sign_body(self, body: dict, primary_type: str, additional_types: dict) -> str:
        """Creates recoverable ECDSA signature of the given body using EIP712 encoding.

        Returns the base64 encoded signature.
        """
        return urlsafe_b64encode(
            self.signer.sign(body, primary_type, additional_types)
        ).decode()


def with_response_body_signature(
    http_body_signer_dependency: Callable[[], HTTPBodySigner],
    primary_type: str,
    additional_types: dict = {},
) -> Callable[
    [Callable[P, Awaitable[dict] | dict]],
    Callable[[Response, HTTPBodySigner, P], Awaitable[dict]],
]:
    """Creates an HTTP signature for the EIP-712 encoded response body of a handler.

    The recoverable ECDSA signature is attached as described by the HTTP Message
    Signatures draft.
    """

    def decorate(
        func: Callable[[P], Awaitable[dict] | dict],
    ) -> Callable[[Response, HTTPBodySigner, P], Awaitable[dict]]:
        async def wrapped(
            response: Response,
            http_body_signer: HTTPBodySigner = Depends(http_body_signer_dependency),
            *args,
            **kwargs,
        ) -> dict:
            response_body = func(*args, **kwargs)
            if inspect.iscoroutine(response_body):
                response_body = await response_body
            signature_headers = http_body_signer.create_signature_headers(
                response_body,
                primary_type,
                additional_types,
            )
            response.headers.update(signature_headers)
            return response_body

        wrapped_signature = inspect.signature(wrapped)
        func_signature = inspect.signature(func)
        wrapped.__signature__ = copy_parameters(
            wrapped_signature, func_signature, ["response", "http_body_signer"]
        )
        return wrapped

    return decorate
