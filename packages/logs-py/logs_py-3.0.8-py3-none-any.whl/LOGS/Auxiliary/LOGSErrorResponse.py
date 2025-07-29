from typing import Any, List, Optional, cast


class LOGSErrorResponse:
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None
    type: Optional[str] = None

    errors: List[str] = []

    def __init__(self, ref=None, errors: Optional[List[str]] = None):
        if ref:
            self._fromRef(ref)

        if errors:
            self.errors = errors

    def override(self, ref=dict):
        self._fromRef(ref)

    def _fromRef(self, ref=None):
        if not isinstance(ref, dict):
            ref = {"title": str(ref)}

        errors: List[str] = []
        if "title" in ref:
            errors.append(str(ref["title"]))

        if "description" in ref:
            errors.extend(str(ref["description"]).split("\n"))

        if "error" in ref:
            errors = [f"({str(ref['error'])})"]

        if "errors" in ref and isinstance(ref["errors"], dict):
            for k, v in ref["errors"].items():
                errors.append(k + ": " + " ".join(v) if isinstance(v, list) else str(v))

        ref["errors"] = cast(Any, errors)

        for k in dir(self):
            if k in ref and hasattr(self, k) and not callable(getattr(self, k)):
                try:
                    setattr(self, k, ref[k])
                except AttributeError:
                    pass
