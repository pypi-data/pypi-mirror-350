from httpx import Response,HTTPStatusError
class CustomResponse(Response):
    def raise_for_status(self) -> None:
        """
        Raise the `HTTPStatusError` if one occurred.
        """
        request = self._request
        if request is None:
            raise RuntimeError(
                "Cannot call `raise_for_status` as the request "
                "instance has not been set on this response."
            )

        if self.is_success:
            return

        if self.has_redirect_location:
            message = (
                "Custom error message for redirect:\n"
                "Status code: {0.status_code}\n"
                "Reason phrase: {0.reason_phrase}\n"
                "URL: {0.url}\n"
                "Redirect location: {0.headers['location']}\n"
                "For more information check: https://httpstatuses.com/{0.status_code}"
            )
        else:
            message = (
                "Custom error message for non-redirect:\n"
                "Status code: {0.status_code}\n"
                "Reason phrase: {0.reason_phrase}\n"
                "URL: {0.url}\n"
                "For more information check: https://httpstatuses.com/{0.status_code}"
            )

        status_class = self.status_code // 100
        error_types = {
            1: "Informational response",
            3: "Redirect response",
            4: "Client error",
            5: "Server error",
        }
        error_type = error_types.get(status_class, "Invalid status code")
        message = message.format(self, error_type=error_type)
        print(message)
        raise HTTPStatusError(message, request=request, response=self)