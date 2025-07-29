from grpc import RpcError, StatusCode
from radiens.utils.enums import ClientType
from radiens.utils.logging_config import logger


class RpcException(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.code_msg = ". Error code: {}".format(status_code.value[0])

    def __str__(self):
        return self.message + self.code_msg


def handle_grpc_error(ex: RpcError, client_type: ClientType):
    status_code = ex.code()
    try:
        logger.error("Error: code: %d (%s), details: %s",
                     status_code.value[0], status_code, ex.details())
    except Exception:
        pass
    if status_code == StatusCode.UNAVAILABLE:
        raise RpcException("Confirm {} is running".format(
            client_type), status_code) from None
    if status_code == StatusCode.UNAUTHENTICATED:
        raise RpcException("Invalid authentication", status_code) from None
    if status_code == StatusCode.RESOURCE_EXHAUSTED:
        raise RpcException("Data too big. Try smaller chunks",
                           status_code) from None
    if status_code == StatusCode.UNKNOWN:
        raise RpcException("Unknown error: {}".format(ex.details()),
                           status_code) from None
    else:
        raise RpcError(ex) from None
