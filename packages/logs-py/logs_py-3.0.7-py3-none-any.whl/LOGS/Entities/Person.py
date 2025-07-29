from enum import Enum
from typing import List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.PersonCategory import PersonCategory
from LOGS.Entities.PersonRelations import PersonRelations
from LOGS.Entities.Role import Role
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.ICreationRecord import ICreationRecord
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IPermissionedEntity import GenericPermissionEntity
from LOGS.Interfaces.IRelatedEntity import IRelatedEntity
from LOGS.Interfaces.ISoftDeletable import ISoftDeletable
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.LOGSConnection import LOGSConnection


class PersonAccountState(Enum):
    NoAccount = "NoAccount"
    Enabled = "Enabled"
    Disabled = "Disabled"


@Endpoint("persons")
class Person(
    IEntityWithIntId,
    IRelatedEntity[PersonRelations],
    INamedEntity,
    IUniqueEntity,
    ISoftDeletable,
    ICreationRecord,
    IModificationRecord,
    GenericPermissionEntity,
):
    _firstName: Optional[str]
    _lastName: Optional[str]
    _login: Optional[str]
    _accountState: Optional[PersonAccountState]
    _salutation: Optional[str]
    _notes: Optional[str]
    _officePhone: Optional[str]
    _email: Optional[str]
    _privateAddress: Optional[str]
    _phone: Optional[str]
    _web: Optional[str]
    _categories: Optional[List[PersonCategory]]
    _relations: Optional[PersonRelations]
    _roles: Optional[List[Role]]
    _password: Optional[str]

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
    ):
        self._firstName = None
        self._lastName = None
        self._login = None
        self._accountState = None
        self._salutation = None
        self._notes = None
        self._officePhone = None
        self._email = None
        self._privateAddress = None
        self._phone = None
        self._web = None
        self._categories = None
        self._relations = None
        self._roles = None
        self._password = None

        super().__init__(ref=ref, id=id, connection=connection)

    @property
    def login(self) -> Optional[str]:
        return self._login

    @login.setter
    def login(self, value):
        self._login = self.checkAndConvertNullable(value, str, "login")

    @property
    def accountState(self) -> Optional[PersonAccountState]:
        return self._accountState

    @accountState.setter
    def accountState(self, value):
        self._accountState = self.checkAndConvertNullable(
            value, PersonAccountState, "accountState"
        )

    @property
    def firstName(self) -> Optional[str]:
        return self._firstName

    @firstName.setter
    def firstName(self, value):
        self._firstName = self.checkAndConvertNullable(value, str, "firstName")

    @property
    def lastName(self) -> Optional[str]:
        return self._lastName

    @lastName.setter
    def lastName(self, value):
        self._lastName = self.checkAndConvertNullable(value, str, "lastName")

    @property
    def salutation(self) -> Optional[str]:
        return self._salutation

    @salutation.setter
    def salutation(self, value):
        self._salutation = self.checkAndConvertNullable(value, str, "salutation")

    @property
    def notes(self) -> Optional[str]:
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = self.checkAndConvertNullable(value, str, "notes")

    @property
    def officePhone(self) -> Optional[str]:
        return self._officePhone

    @officePhone.setter
    def officePhone(self, value):
        self._officePhone = self.checkAndConvertNullable(value, str, "officePhone")

    @property
    def email(self) -> Optional[str]:
        return self._email

    @email.setter
    def email(self, value):
        self._email = self.checkAndConvertNullable(value, str, "email")

    @property
    def privateAddress(self) -> Optional[str]:
        return self._privateAddress

    @privateAddress.setter
    def privateAddress(self, value):
        self._privateAddress = self.checkAndConvertNullable(
            value, str, "privateAddress"
        )

    @property
    def phone(self) -> Optional[str]:
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = self.checkAndConvertNullable(value, str, "phone")

    @property
    def web(self) -> Optional[str]:
        return self._web

    @web.setter
    def web(self, value):
        self._web = self.checkAndConvertNullable(value, str, "web")

    @property
    def categories(self) -> Optional[List[PersonCategory]]:
        return self._categories

    @categories.setter
    def categories(self, value):
        self._categories = self.checkListAndConvertNullable(
            value, PersonCategory, "categories"
        )

    @property
    def relations(self) -> Optional[PersonRelations]:
        return self._relations

    @relations.setter
    def relations(self, value):
        self._relations = self.checkAndConvertNullable(
            value, PersonRelations, "relations"
        )

    @property
    def roles(self) -> Optional[List[Role]]:
        return self._roles

    @roles.setter
    def roles(self, value):
        if value is None:
            self._roles = None
        else:
            self._roles = self.checkListAndConvertNullable(value, Role, "roles")

    @property
    def password(self) -> Optional[str]:
        return self._password

    @password.setter
    def password(self, value):
        self._password = self.checkAndConvertNullable(value, str, "password")
