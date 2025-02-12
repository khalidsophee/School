def create_response(status="success", data=None, message=None):
    """ Standardizes API responses """
    return {
        "status": status,
        "data": data,
        "message": message
    }
