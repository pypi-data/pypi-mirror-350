from typing import TYPE_CHECKING, List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.MinimalModelGenerator import MinimalFromList, MinimalFromSingle
from LOGS.Entities.CustomField import CustomField
from LOGS.Entities.CustomTypeEntityType import CustomTypeEntityType
from LOGS.Entities.CustomTypeRelations import CustomTypeRelations
from LOGS.Entities.CustomTypeSection import CustomTypeSection
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.ICreationRecord import ICreationRecord
from LOGS.Interfaces.IHierarchyType import IHierarchyType
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IPermissionedEntity import GenericPermissionEntity
from LOGS.Interfaces.IRelatedEntity import IRelatedEntity
from LOGS.Interfaces.ISoftDeletable import ISoftDeletable
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity

if TYPE_CHECKING:
    from LOGS.Entities.CustomTypeMinimal import CustomTypeMinimal


@Endpoint("types")
class CustomType(
    IEntityWithIntId,
    GenericPermissionEntity,
    INamedEntity,
    IUniqueEntity,
    ICreationRecord,
    IModificationRecord,
    ISoftDeletable,
    IRelatedEntity[CustomTypeRelations],
    IHierarchyType,
):
    _relationType = CustomTypeRelations
    _noSerialize = ["customFields"]

    _description: Optional[str] = None
    _entityType: Optional[CustomTypeEntityType] = None
    _hasRestrictedAddPermission: Optional[bool] = None
    _hasRestrictedEditPermission: Optional[bool] = None
    _hasRestrictedReadPermission: Optional[bool] = None
    _sections: Optional[List[CustomTypeSection]] = None
    _isEnabled: Optional[bool] = None
    _relations: Optional[CustomTypeRelations] = None
    _inventoryName: Optional[str] = None
    _inventoryDescription: Optional[str] = None
    _isHierarchyRoot: Optional[bool] = None
    _rootHierarchy: Optional["CustomTypeMinimal"] = None
    _parentTypes: Optional[List["CustomTypeMinimal"]] = None

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value):
        self._description = self.checkAndConvertNullable(value, str, "description")

    @property
    def entityType(self) -> Optional[CustomTypeEntityType]:
        return self._entityType

    @entityType.setter
    def entityType(self, value):
        self._entityType = self.checkAndConvertNullable(
            value, CustomTypeEntityType, "entityType"
        )

    @property
    def hasRestrictedAddPermission(self) -> Optional[bool]:
        return self._hasRestrictedAddPermission

    @hasRestrictedAddPermission.setter
    def hasRestrictedAddPermission(self, value):
        self._hasRestrictedAddPermission = self.checkAndConvertNullable(
            value, bool, "hasRestrictedAddPermission"
        )

    @property
    def hasRestrictedEditPermission(self) -> Optional[bool]:
        return self._hasRestrictedEditPermission

    @hasRestrictedEditPermission.setter
    def hasRestrictedEditPermission(self, value):
        self._hasRestrictedEditPermission = self.checkAndConvertNullable(
            value, bool, "hasRestrictedEditPermission"
        )

    @property
    def hasRestrictedReadPermission(self) -> Optional[bool]:
        return self._hasRestrictedReadPermission

    @hasRestrictedReadPermission.setter
    def hasRestrictedReadPermission(self, value):
        self._hasRestrictedReadPermission = self.checkAndConvertNullable(
            value, bool, "hasRestrictedReadPermission"
        )

    @property
    def sections(self) -> Optional[List[CustomTypeSection]]:
        return self._sections

    @sections.setter
    def sections(self, value):
        self._sections = self.checkListAndConvertNullable(
            value, CustomTypeSection, "sections"
        )

    @property
    def isEnabled(self) -> Optional[bool]:
        return self._isEnabled

    @isEnabled.setter
    def isEnabled(self, value):
        self._isEnabled = self.checkAndConvertNullable(value, bool, "isEnabled")

    @property
    def relations(self) -> Optional[CustomTypeRelations]:
        return self._relations

    @relations.setter
    def relations(self, value):
        self._relations = self.checkAndConvertNullable(
            value, CustomTypeRelations, "relations"
        )

    @property
    def inventoryName(self) -> Optional[str]:
        return self._inventoryName

    @inventoryName.setter
    def inventoryName(self, value):
        self._inventoryName = self.checkAndConvertNullable(value, str, "inventoryName")

    @property
    def inventoryDescription(self) -> Optional[str]:
        return self._inventoryDescription

    @inventoryDescription.setter
    def inventoryDescription(self, value):
        self._inventoryDescription = self.checkAndConvertNullable(
            value, str, "inventoryDescription"
        )

    @property
    def isHierarchyRoot(self) -> Optional[bool]:
        return self._isHierarchyRoot

    @isHierarchyRoot.setter
    def isHierarchyRoot(self, value):
        self._isHierarchyRoot = self.checkAndConvertNullable(
            value, bool, "isHierarchyRoot"
        )

    @property
    def rootHierarchy(self) -> Optional["CustomTypeMinimal"]:
        return self._rootHierarchy

    @rootHierarchy.setter
    def rootHierarchy(self, value):
        self._rootHierarchy = MinimalFromSingle(
            value, "CustomTypeMinimal", "rootHierarchy", self.connection
        )

    @property
    def parentTypes(self) -> Optional[List["CustomTypeMinimal"]]:
        return self._parentTypes

    @parentTypes.setter
    def parentTypes(self, value):
        self._parentTypes = MinimalFromList(
            value, "CustomTypeMinimal", "parentTypes", self.connection
        )

    @property
    def customFields(self) -> List[CustomField]:
        if self.sections is None:
            return []

        return [
            field
            for section in self.sections
            if section.customFields is not None
            for field in section.customFields
            if field is not None
        ]
