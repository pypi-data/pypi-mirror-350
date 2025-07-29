from pygeai.core.base.mappers import ErrorMapper


class ErrorHandler:

    @classmethod
    def has_errors(cls, response):
        error_found = False
        if "errors" in response or "error" in response:
            error_found = True

        return error_found

    @classmethod
    def extract_error(cls, response):
        if "errors" in response:
            result = ErrorMapper.map_to_error_list_response(response)
        elif "error" in response:
            result = ErrorMapper.map_to_error(response.get('error'))
        else:
            result = response

        return result
