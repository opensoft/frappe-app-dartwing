"""Utility helpers for Dartwing APIs."""

def ok(message: str, data=None):
    return {"success": True, "message": message, "data": data}


def fail(message: str, data=None):
    return {"success": False, "message": message, "data": data}
