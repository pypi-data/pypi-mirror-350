from typing import TYPE_CHECKING, Any, List, Optional, Type, TypeVar, Union, cast

from LOGS.Auxiliary.Constants import Constants
from LOGS.Auxiliary.Tools import Tools

if TYPE_CHECKING:
    from LOGS.LOGSConnection import LOGSConnection

# from LOGS.Entities.SampleMinimal import SampleMinimal


def _typeByTypename(fieldType):
    switcher = {
        "Bridge": BridgeMinimalFromDict,
        "BridgeMinimal": BridgeMinimalFromDict,
        "CustomType": CustomTypeMinimalFromDict,
        "CustomTypeMinimal": CustomTypeMinimalFromDict,
        "Dataset": DatasetMinimalFromDict,
        "DatasetMinimal": DatasetMinimalFromDict,
        "Equipment": EquipmentMinimalFromDict,
        "EquipmentMinimal": EquipmentMinimalFromDict,
        "Experiment": ExperimentMinimalFromDict,
        "ExperimentMinimal": ExperimentMinimalFromDict,
        "FormatFormat": FormatFormatMinimalFromDict,
        "FormatFormatMinimal": FormatFormatMinimalFromDict,
        "Format": FormatMinimalFromDict,
        "FormatInstrument": FormatInstrumentMinimalFromDict,
        "FormatInstrumentMinimal": FormatInstrumentMinimalFromDict,
        "FormatMethod": FormatMethodMinimalFromDict,
        "FormatMethodMinimal": FormatMethodMinimalFromDict,
        "FormatMinimal": FormatMinimalFromDict,
        "FormatVendor": FormatVendorMinimalFromDict,
        "FormatVendorMinimal": FormatVendorMinimalFromDict,
        "InstrumentFacility": InstrumentMinimalFromDict,
        "InstrumentFacilityMinimal": InstrumentMinimalFromDict,
        "Instrument": InstrumentMinimalFromDict,
        "InstrumentMinimal": InstrumentMinimalFromDict,
        "LabNotebook": LabNotebookMinimalFromDict,
        "LabNotebookMinimal": LabNotebookMinimalFromDict,
        "LabNotebookExperiment": LabNotebookExperimentMinimalFromDict,
        "LabNotebookExperimentMinimal": LabNotebookExperimentMinimalFromDict,
        "LabNotebookEntry": LabNotebookEntryMinimalFromDict,
        "LabNotebookEntryMinimal": LabNotebookEntryMinimalFromDict,
        "Method": MethodMinimalFromDict,
        "MethodMinimal": MethodMinimalFromDict,
        "OriginMinimal": OriginMinimalFromDict,
        "Origin": OriginMinimalFromDict,
        "PersonMinimal": PersonMinimalFromDict,
        "Person": PersonMinimalFromDict,
        "ProjectMinimal": ProjectMinimalFromDict,
        "Project": ProjectMinimalFromDict,
        "SampleMinimal": SampleMinimalFromDict,
        "Sample": SampleMinimalFromDict,
        "InventoryMinimal": InventoryMinimalFromDict,
        "Inventory": InventoryMinimalFromDict,
        "CustomTypeMinimal": CustomTypeMinimalFromDict,
        "CustomType": CustomTypeMinimalFromDict,
        "CustomFieldMinimal": CustomFieldMinimalFromDict,
        "CustomField": CustomFieldMinimalFromDict,
    }
    return switcher.get(fieldType, lambda ref: None)


def MinimalFromSingle(
    value: Any,
    fieldType: str,
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
) -> Any:
    from LOGS.Entity.ConnectedEntity import ConnectedEntity

    result = cast(
        Any,
        Tools.checkAndConvert(
            value,
            fieldType=str,
            fieldName=fieldName,
            converter=_typeByTypename(fieldType),
            allowNone=True,
        ),
    )

    if connection:
        if isinstance(result, ConnectedEntity):
            result.connection = connection

    return result


def MinimalFromList(
    value: Any,
    fieldType: str,
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
) -> Any:
    from LOGS.Entity.ConnectedEntity import ConnectedEntity

    if isinstance(value, (int, str)):
        value = {"id": value}

    if isinstance(value, list):
        l = []
        for v in value:
            if isinstance(v, (int, str)):
                l.append({"id": v})
            else:
                l.append(v)
        value = l

    l = Tools.checkListAndConvert(
        value,
        fieldType=str,
        fieldName=fieldName,
        converter=_typeByTypename(fieldType),
        allowNone=True,
    )
    result = list([a for a in l if a])

    if connection:
        for f in result:
            if isinstance(f, ConnectedEntity):
                f.connection = connection

    if len(result) < 1:
        return None

    return result


_T = TypeVar("_T")


def _checkAndConvert(
    value: Any,
    fieldType: Union[Type[_T], List[Type[_T]]],
    fieldName: Optional[str] = None,
    allowNone=False,
    connection: Optional["LOGSConnection"] = None,
) -> _T:
    from LOGS.Entity.ConnectedEntity import ConnectedEntity

    if isinstance(value, (int, str)):
        value = {"id": value}

    result = Tools.checkAndConvert(
        value, fieldType=fieldType, fieldName=fieldName, allowNone=allowNone
    )

    if connection:
        if isinstance(result, ConnectedEntity):
            result.connection = connection

    return result


def BridgeMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.BridgeMinimal import BridgeMinimal

    return _checkAndConvert(
        ref,
        BridgeMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def CustomTypeMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.CustomTypeMinimal import CustomTypeMinimal

    return _checkAndConvert(
        ref,
        CustomTypeMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def CustomFieldMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.CustomFieldMinimal import CustomFieldMinimal

    return _checkAndConvert(
        ref,
        CustomFieldMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def DatasetMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.DatasetMinimal import DatasetMinimal

    return _checkAndConvert(
        ref, DatasetMinimal, fieldName=fieldName, allowNone=True, connection=connection
    )


def EquipmentMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.EquipmentMinimal import EquipmentMinimal

    return _checkAndConvert(
        ref,
        EquipmentMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def ExperimentMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.ExperimentMinimal import ExperimentMinimal

    return _checkAndConvert(
        ref,
        ExperimentMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def InstrumentMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.InstrumentMinimal import InstrumentMinimal

    return _checkAndConvert(
        ref,
        InstrumentMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def MethodMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.MethodMinimal import MethodMinimal

    return _checkAndConvert(
        ref, MethodMinimal, fieldName=fieldName, allowNone=True, connection=connection
    )


def PersonMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.PersonMinimal import PersonMinimal

    return _checkAndConvert(
        ref, PersonMinimal, fieldName=fieldName, allowNone=True, connection=connection
    )


def ProjectMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.ProjectMinimal import ProjectMinimal

    return _checkAndConvert(
        ref, ProjectMinimal, fieldName=fieldName, allowNone=True, connection=connection
    )


def SampleMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.SampleMinimal import SampleMinimal

    return _checkAndConvert(
        ref, SampleMinimal, fieldName=fieldName, allowNone=True, connection=connection
    )


def InventoryMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.InventoryMinimal import InventoryMinimal

    return _checkAndConvert(
        ref,
        InventoryMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def LabNotebookMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.LabNotebookMinimal import LabNotebookMinimal

    return _checkAndConvert(
        ref,
        LabNotebookMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def LabNotebookExperimentMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.LabNotebookExperimentMinimal import LabNotebookExperimentMinimal

    return _checkAndConvert(
        ref,
        LabNotebookExperimentMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def LabNotebookEntryMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.LabNotebookEntryMinimal import LabNotebookEntryMinimal

    return _checkAndConvert(
        ref,
        LabNotebookEntryMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def OriginMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.OriginMinimal import OriginMinimal

    return _checkAndConvert(
        ref, OriginMinimal, fieldName=fieldName, allowNone=True, connection=connection
    )


def FormatMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.FormatMinimal import FormatMinimal

    return _checkAndConvert(
        ref, FormatMinimal, fieldName=fieldName, allowNone=True, connection=connection
    )


def FormatVendorMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.FormatVendorMinimal import FormatVendorMinimal

    return _checkAndConvert(
        ref,
        FormatVendorMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def FormatMethodMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.FormatMethodMinimal import FormatMethodMinimal

    return _checkAndConvert(
        ref,
        FormatMethodMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def FormatInstrumentMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.FormatInstrumentMinimal import FormatInstrumentMinimal

    return _checkAndConvert(
        ref,
        FormatInstrumentMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def FormatFormatMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.FormatFormatMinimal import FormatFormatMinimal

    return _checkAndConvert(
        ref,
        FormatFormatMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def EntityMinimalWithStrIdFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entity.EntityMinimalWithStrId import EntityMinimalWithStrId

    return _checkAndConvert(
        ref,
        EntityMinimalWithStrId,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )
