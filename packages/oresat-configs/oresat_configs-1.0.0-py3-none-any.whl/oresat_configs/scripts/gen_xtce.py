from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from canopen.objectdictionary import ObjectDictionary, Variable

from .._yaml_to_od import DataType, get_beacon_def, load_od_configs, load_od_db
from ..configs.cards_config import CardsConfig
from ..configs.mission_config import MissionConfig

CANOPEN_TO_XTCE_DT = {
    DataType.BOOL: "bool",
    DataType.INT8: "int8",
    DataType.INT16: "int16",
    DataType.INT32: "int32",
    DataType.INT64: "int64",
    DataType.UINT8: "uint8",
    DataType.UINT16: "uint16",
    DataType.UINT32: "uint32",
    DataType.UINT64: "uint64",
    DataType.STR: "string",
    DataType.FLOAT32: "float",
    DataType.FLOAT64: "double",
}


def make_obj_name(obj: Variable) -> str:
    """get obj name."""

    name = ""
    if obj.index < 0x5000:
        name += "c3_"

    if isinstance(obj.parent, ObjectDictionary):
        name += obj.name
    else:
        name += f"{obj.parent.name}_{obj.name}"

    return name


def make_dt_name(obj: Variable) -> str:
    """Make xtce data type name."""

    type_name = CANOPEN_TO_XTCE_DT[DataType(obj.data_type)]
    if obj.name in ["unix_time", "updater_status"]:
        type_name = obj.name
    elif obj.value_descriptions:
        if isinstance(obj.parent, ObjectDictionary):
            type_name += f"_c3_{obj.name}"
        else:
            type_name += f"_{obj.parent.name}_{obj.name}"
    elif obj.data_type == DataType.STR:
        type_name += f"{len(obj.default) * 8}"
    elif obj.unit:
        type_name += f"_{obj.unit}"
    type_name = type_name.replace("/", "p").replace("%", "percent")

    type_name += "_type"

    return type_name


def write_xtce(mission_config: MissionConfig, od: ObjectDictionary) -> None:
    root = ET.Element(
        "SpaceSystem",
        attrib={
            "name": mission_config.nice_name,
            "xmlns": "http://www.omg.org/spec/XTCE/20180204",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:schemaLocation": (
                "http://www.omg.org/spec/XTCE/20180204 "
                "https://www.omg.org/spec/XTCE/20180204/SpaceSystem.xsd"
            ),
        },
    )

    header = ET.SubElement(
        root,
        "Header",
        attrib={
            "validationStatus": "Working",
            "classification": "NotClassified",
            "version": "0.0",
            "date": datetime.now().strftime("%Y-%m-%d"),
        },
    )
    author_set = ET.SubElement(header, "AuthorSet")
    author = ET.SubElement(author_set, "Author")
    author.text = "PSAS (Portland State Aerospace Society)"

    tm_meta = ET.SubElement(root, "TelemetryMetaData")
    tm_meta_para = ET.SubElement(tm_meta, "ParameterTypeSet")

    # hard-code the unitless uint32 type for the crc32
    uint32_type = ET.SubElement(
        tm_meta_para,
        "IntegerParameterType",
        attrib={
            "name": "uint32_type",
        },
    )
    ET.SubElement(uint32_type, "UnitSet")
    bin_data_enc = ET.SubElement(
        uint32_type,
        "IntegerDataEncoding",
        attrib={
            "bitOrder": "leastSignificantBitFirst",
            "encoding": "unsigned",
            "sizeInBits": "32",
        },
    )

    # hard-code the 128b type for the AX.25 parameter
    uint128_type = ET.SubElement(
        tm_meta_para,
        "BinaryParameterType",
        attrib={
            "name": "b128_type",
            "shortDescription": "128 bitfield",
        },
    )
    ET.SubElement(uint128_type, "UnitSet")
    bin_data_enc = ET.SubElement(
        uint128_type,
        "BinaryDataEncoding",
        attrib={"bitOrder": "leastSignificantBitFirst"},
    )
    bin_data_enc_size = ET.SubElement(
        bin_data_enc,
        "SizeInBits",
    )
    bin_data_enc_size_fixed = ET.SubElement(
        bin_data_enc_size,
        "FixedValue",
    )
    bin_data_enc_size_fixed.text = "128"

    # hard-code the unix time type
    para_type = ET.SubElement(
        tm_meta_para,
        "AbsoluteTimeParameterType",
        attrib={
            "name": "unix_time",
            "shortDescription": "Unix coarse timestamp",
        },
    )
    enc = ET.SubElement(para_type, "Encoding")
    ET.SubElement(
        enc,
        "IntegerDataEncoding",
        attrib={
            "byteOrder": "leastSignificantByteFirst",
            "sizeInBits": "32",
        },
    )
    ref_time = ET.SubElement(para_type, "ReferenceTime")
    epoch = ET.SubElement(ref_time, "Epoch")
    epoch.text = "1970-01-01T00:00:00.000"

    beacon_def = get_beacon_def(od, mission_config)

    para_types = ["unix_time", "b128_type", "uint32_type"]
    for obj in beacon_def:
        name = make_dt_name(obj)
        if name in para_types:
            continue
        para_types.append(name)

        data_type = DataType(obj.data_type)
        if data_type == DataType.BOOL:
            para_type = ET.SubElement(
                tm_meta_para,
                "BooleanParameterType",
                attrib={
                    "name": name,
                    "zeroStringValue": "0",
                    "oneStringValue": "1",
                },
            )
        elif data_type.name.startswith("UINT") and obj.value_descriptions:
            para_type = ET.SubElement(
                tm_meta_para,
                "EnumeratedParameterType",
                attrib={
                    "name": name,
                },
            )
            enum_list = ET.SubElement(para_type, "EnumerationList")
            for value, name in obj.value_descriptions.items():
                ET.SubElement(
                    enum_list,
                    "Enumeration",
                    attrib={
                        "value": str(value),
                        "label": name,
                    },
                )
        elif data_type.is_int:
            if data_type.name.startswith("UINT"):
                signed = False
                encoding = "unsigned"
            else:
                signed = True
                encoding = "twosComplement"

            para_type = ET.SubElement(
                tm_meta_para,
                "IntegerParameterType",
                attrib={
                    "name": name,
                    "signed": str(signed).lower(),
                },
            )

            para_unit_set = ET.SubElement(para_type, "UnitSet")
            if obj.unit:
                para_unit = ET.SubElement(
                    para_unit_set,
                    "Unit",
                    attrib={
                        "description": obj.unit,
                    },
                )
                para_unit.text = obj.unit

            data_enc = ET.SubElement(
                para_type,
                "IntegerDataEncoding",
                attrib={
                    "byteOrder": "leastSignificantByteFirst",
                    "encoding": encoding,
                    "sizeInBits": str(data_type.size),
                },
            )
            if obj.factor != 1:
                def_cal = ET.SubElement(data_enc, "DefaultCalibrator")
                poly_cal = ET.SubElement(def_cal, "PolynomialCalibrator")
                ET.SubElement(
                    poly_cal,
                    "Term",
                    attrib={
                        "exponent": "1",
                        "coefficient": str(obj.factor),
                    },
                )
        elif data_type == DataType.STR:
            para_type = ET.SubElement(
                tm_meta_para,
                "StringParameterType",
                attrib={
                    "name": name,
                },
            )
            str_para_type = ET.SubElement(
                para_type,
                "StringDataEncoding",
                attrib={
                    "encoding": "UTF-8",
                },
            )
            size_in_bits = ET.SubElement(str_para_type, "SizeInBits")
            fixed = ET.SubElement(size_in_bits, "Fixed")
            fixed_value = ET.SubElement(fixed, "FixedValue")
            fixed_value.text = str(len(obj.default) * 8)

    para_set = ET.SubElement(tm_meta, "ParameterSet")

    # hard-code the AX.25 headers as a Binary128 type
    ET.SubElement(
        para_set,
        "Parameter",
        attrib={
            "name": "ax25_header",
            "parameterTypeRef": "b128_type",
            "shortDescription": "AX.25 Header",
        },
    )
    for obj in beacon_def:
        ET.SubElement(
            para_set,
            "Parameter",
            attrib={
                "name": make_obj_name(obj),
                "parameterTypeRef": make_dt_name(obj),
                "shortDescription": obj.description,
            },
        )
    ET.SubElement(
        para_set,
        "Parameter",
        attrib={
            "name": "crc32",
            "parameterTypeRef": "uint32_type",
            "shortDescription": "crc check for beacon",
        },
    )

    cont_set = ET.SubElement(tm_meta, "ContainerSet")
    seq_cont = ET.SubElement(
        cont_set,
        "SequenceContainer",
        attrib={
            "name": "Beacon",
        },
    )
    entry_list = ET.SubElement(seq_cont, "EntryList")
    ET.SubElement(
        entry_list,
        "ParameterRefEntry",
        attrib={"parameterRef": "ax25_header"},
    )
    for obj in beacon_def:
        ET.SubElement(
            entry_list,
            "ParameterRefEntry",
            attrib={
                "parameterRef": make_obj_name(obj),
            },
        )
    ET.SubElement(
        entry_list,
        "ParameterRefEntry",
        attrib={
            "parameterRef": "crc32",
        },
    )

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    file_name = f"{mission_config.name}.xtce"
    tree.write(file_name, encoding="utf-8", xml_declaration=True)


def gen_xtce(
    cards_config_path: str | Path, mission_config_paths: str | Path | list[str | Path]
) -> None:
    if isinstance(cards_config_path, str):
        cards_config_path = Path(cards_config_path)
    cards_config = CardsConfig.from_yaml(cards_config_path)

    if isinstance(mission_config_paths, (str, Path)):
        mission_config_paths = [mission_config_paths]
    mission_configs = [MissionConfig.from_yaml(m) for m in mission_config_paths]

    config_dir = cards_config_path.parent
    od_configs = load_od_configs(cards_config, config_dir)
    od_db = load_od_db(cards_config, od_configs)
    for mission_config in mission_configs:
        write_xtce(mission_config, od_db[cards_config.manager.name])
