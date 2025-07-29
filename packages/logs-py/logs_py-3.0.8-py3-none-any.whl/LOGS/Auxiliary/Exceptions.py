from typing import TYPE_CHECKING, Any, List, Optional, TypeVar, Union, cast

from LOGS.Auxiliary.Constants import Constants
from LOGS.Auxiliary.LOGSErrorResponse import LOGSErrorResponse
from LOGS.Auxiliary.Tools import Tools

if TYPE_CHECKING:
    from LOGS.Converter.Conversion import Conversion
    from LOGS.Entity.ConnectedEntity import ConnectedEntity
    from LOGS.Entity.Entity import Entity


def formatErrorMessage(errors: List[str], indent: str = " " * 2):
    indent *= 2
    if len(errors) == 1:
        return errors[0]
    if len(errors) > 1:
        return "\n" + indent + ("\n" + indent).join(errors)
        # return ("\n" + indent).join(errors)
    else:
        return ""


class LOGSException(Exception):
    title: Optional[str] = None
    details: Optional[str] = None
    status: Optional[int] = None
    type: Optional[str] = None

    def __init__(
        self,
        message: Optional[Union[List[str], str]] = None,
        responseError: Optional[LOGSErrorResponse] = None,
    ):
        if responseError:
            self._fromResponse(responseError)
            if not message:
                message = responseError.errors

        if message:
            if isinstance(message, list):
                message = formatErrorMessage(message)
            message = cast(str, message)
            super().__init__(Tools.convertToNativeNewline(message))
        else:
            super().__init__()

    def _fromResponse(self, response: LOGSErrorResponse):
        self.title = response.title
        self.details = response.description
        self.status = response.status
        self.type = response.type

    @classmethod
    def gerundVerb(cls, verb: str):
        if verb.endswith("ing"):
            return verb
        elif verb.endswith("e"):
            verb = verb[:-1]

        return verb + "ing"


TEntity = TypeVar("TEntity", bound="Entity")


class LOGSMultilineException(LOGSException):
    def __init__(
        self,
        errors: Optional[List[str]] = None,
        responseError: Optional[LOGSErrorResponse] = None,
    ):
        if not errors and responseError:
            errors = responseError.errors

        super().__init__(
            self._createMessage(errors=errors), responseError=responseError
        )

    @classmethod
    def _createMessage(
        cls,
        errors: Optional[List[str]] = None,
    ):
        pass

        indent = " " * 4
        message = ""

        indent *= 2

        if errors:
            message = errors.pop(0)

        if errors:
            message += "\n" + indent + ("\n" + indent).join(errors)

        return message


class EntityIncompleteException(LOGSException):
    def __init__(
        self,
        entity: Union["Entity", "ConnectedEntity"],
        errors: Optional[List[str]] = None,
        parameterName: Optional[str] = None,
        functionName: Optional[str] = None,
        responseError: Optional[LOGSErrorResponse] = None,
        hasFetchFull: bool = True,
    ):
        if not errors and responseError:
            errors = responseError.errors

        super().__init__(
            self._createMessage(
                entity=entity,
                errors=errors,
                functionName=functionName,
                parameterName=parameterName,
                hasFetchFull=hasFetchFull,
            ),
            responseError=responseError,
        )

    def _createMessage(
        self,
        entity: Union["Entity", "ConnectedEntity"],
        errors: Optional[List[str]] = None,
        parameterName: Optional[str] = None,
        functionName: Optional[str] = None,
        hasFetchFull: bool = True,
    ):
        indent = " " * 2
        message = ""

        name = f" '{parameterName}' " if parameterName else " "
        func = []
        if functionName:
            func.append(f"'{functionName}'")

        if hasFetchFull:
            func.append(f"'fetchFull()'")

        message = f"Additional field{name}of entity {entity.identifier} was not fetched for efficiency reasons. Use {' or '.join(func)} method to fetch this parameter"

        indent *= 2
        if errors:
            message += formatErrorMessage(errors=errors, indent=indent)
            # lines = errors.split("\n")
            # if len(lines) > 1:
            #     message += ":\n" + indent + ("\n" + indent).join(lines)
            # else:
            #     message += ": " + errors
        else:
            message += "."

        return message


class EntityAPIException(LOGSException):
    _action = "communicate"

    def __init__(
        self,
        entity: Optional[Union[TEntity, List[TEntity]]] = None,
        errors: Optional[List[str]] = None,
        responseError: Optional[LOGSErrorResponse] = None,
    ):
        if not errors and responseError:
            errors = responseError.errors

        super().__init__(
            self._createMessage(entity=entity, errors=errors),
            responseError=responseError,
        )

    def _createMessage(
        self,
        entity: Optional[Union[TEntity, List[TEntity]]],
        errors: Optional[List[str]] = None,
    ):
        from LOGS.Entity.Entity import Entity

        indent = " " * 2
        message = ""
        if isinstance(entity, list):
            message = "%sCould not %s %s %a" % (
                "\n" + indent if errors and len(errors) > 1 else "",
                self._action,
                Tools.plural("entity", entity),
                Tools.eclipsesJoin(", ", [e.identifier for e in entity]),
            )
        elif isinstance(entity, Entity):
            message = "Could not %s entity %a" % (self._action, entity.identifier)
        else:
            message = "%s entity failed" % self.gerundVerb(self._action.capitalize())

        # indent *= 2
        if errors:
            message += ": " + formatErrorMessage(errors=errors, indent=indent)
            # lines = error.split("\n")
            # if len(lines) > 1:
            #     message += ":\n" + indent + ("\n" + indent).join(lines)
            # else:
            #     message += ": " + error
        else:
            message += "."

        return message


class EntityFetchingException(EntityAPIException):
    _action = "fetch"


class EntityUpdatingException(EntityAPIException):
    _action = "update"


class EntityCreatingException(EntityAPIException):
    _action = "create"


class EntityDeletingException(LOGSException):
    _action = "delete"

    def __init__(
        self,
        entityIds: Optional[Union[Constants.ID_TYPE, List[Constants.ID_TYPE]]] = None,
        errors: Optional[List[str]] = None,
        responseError: Optional[LOGSErrorResponse] = None,
    ):
        if not errors and responseError:
            errors = responseError.errors

        super().__init__(
            self._createMessage(entityIds=entityIds, errors=errors),
            responseError=responseError,
        )

    def _createMessage(
        self,
        entityIds: Optional[Union[Constants.ID_TYPE, List[Constants.ID_TYPE]]],
        errors: Optional[List[str]] = None,
    ):
        from LOGS.Entity.Entity import Entity

        indent = " " * 2
        message = ""
        if isinstance(entityIds, list):
            message = "%sCould not %s %s %a" % (
                "\n" + indent if errors and len(errors) > 1 else "",
                self._action,
                Tools.plural("entity", entityIds),
                Tools.eclipsesJoin(", ", [str(id) for id in entityIds]),
            )
        elif isinstance(entityIds, Entity):
            message = "Could not %s entity %a" % (self._action, entityIds.identifier)
        else:
            message = "%s entity failed" % (self.gerundVerb(self._action.capitalize()))

        indent *= 2
        if errors:
            message += ": " + formatErrorMessage(errors=errors, indent=indent)
            # lines = error.split("\n")
            # if len(lines) > 1:
            #     message += ":\n" + indent + ("\n" + indent).join(lines)
            # else:
            #     message += ": " + error
        else:
            message += "."

        return message


class EntityNotFoundException(LOGSException):
    def __init__(self, entity=None):
        ident = ""
        if entity:
            ident = " " + str(entity.id)
            name = entity.name
            if name:
                ident += " " + name
            ident += " (id:%s)" % str(entity.id)

        super().__init__("%s%s is not connected." % (type(entity).__name__, ident))


class NotConnectedException(LOGSException):
    def __init__(self, message: Optional[str] = None):
        if message:
            super().__init__(message=message)
        else:
            super().__init__("Not connected.")


class EntityNotConnectedException(NotConnectedException):
    def __init__(
        self,
        entity: Optional["ConnectedEntity"] = None,
        identifier: Optional[str] = None,
    ):
        if entity:
            super().__init__("Entity %a is not connected." % (entity.identifier))
        elif identifier:
            super().__init__("Entity %a is not connected." % (identifier))
        else:
            super().__init__("Entity is not connected.")


class IllegalFieldValueException(LOGSException):

    def __init__(
        self,
        entityType: Any,
        fieldName: str,
        value: Any,
        errorMessage: Optional[str] = None,
    ):
        if isinstance(entityType, object):
            t = type(entityType).__name__
        elif isinstance(entityType, type) and issubclass(entityType, Entity):
            t = entityType.__name__

        m = f"Illegal value for field '{t}.{fieldName} = {value}'"
        if errorMessage:
            m += ":" + errorMessage
        super().__init__(m)


class UnfinishedConversionException(LOGSException):
    def __init__(self, conversion: "Conversion"):
        super().__init__(
            f"Conversion for dataset {conversion.datasetId} from format '{conversion.datasetFormat}' to format '{conversion.exportFormat}' is not finished yet."
        )
