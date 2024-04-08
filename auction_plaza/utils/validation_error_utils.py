
def get_error_message_in_serializer(serializer) -> str:
    """
    In django rest framework if exception true in is valid method than fetch error message for exception.
    :serializer: pass rest framework serializer object
    return: error message string
    """
    error_message = ''
    for flied_name, error in serializer.errors.items():
        name_field = "" if flied_name in ('non_field_errors', None) else f"{flied_name}: "
        error_message = f"{name_field}{error[0]} {error_message}"
    return error_message
