from __future__ import annotations

from pathlib import Path

from canopen.objectdictionary import REAL32, REAL64, UNSIGNED_TYPES, ObjectDictionary, Variable

from .. import __version__
from .._yaml_to_od import gen_od, load_od_configs, load_od_db, set_od_node_id
from ..configs.cards_config import CardsConfig
from ..configs.od_config import OdConfig
from . import INDENT3, INDENT4

DEFAULT_NODE_ID = 0x7C

VECTOR = "Vector__XXX"  # flag for default, any, all devices

HB_STATES = {
    0x00: "boot_up",
    0x04: "stopped",
    0x05: "operational",
    0x7F: "pre_operational",
}

EMCY_ERROR_CODES = {
    0x0000: "no_error",
    0x1000: "generic_error",
    0x2000: "current_error",
    0x2100: "current_device_input_error",
    0x2200: "current_inside_device_error",
    0x2300: "current_device output_error",
    0x3000: "voltage_error",
    0x3100: "mains_voltage_error",
    0x3200: "voltage_inside_device_error",
    0x3300: "output_voltage_error",
    0x4000: "temperature_error",
    0x4100: "ambient_temperature_error",
    0x4200: "device_temperature_error",
    0x5000: "device_hardware_error",
    0x6000: "device_software_error",
    0x6100: "internal_software_error",
    0x6200: "user_software_error",
    0x6300: "data_set_error",
    0x7000: "additional_modules_error",
    0x8000: "monitoring_error",
    0x8100: "communication_error",
    0x8110: "can_overrun_error",
    0x8120: "passive_mode_error",
    0x8130: "heartbeat_error",
    0x8140: "recovered_bus_error",
    0x8150: "can_id_collision_error",
    0x8200: "protocol_error",
    0x8210: "pdo_not_processed_due_to_length_error",
    0x8220: "pdo_length_exceeded_error",
    0x8230: "mpdo_not_processed_error",
    0x8240: "sync_data_length_error",
    0x8250: "rpdo_timeout_error",
    0x9000: "external_error",
    0xF000: "additional_function_error",
    0xFF00: "device_specific_error",
}

SDO_CSS = {
    0: "download_segment_request",
    1: "initiate_download_request",
    2: "initiate_upload_request",
    3: "upload_segment_request",
    4: "abort_transfer",
    5: "block_upload",
    6: "block_download",
}

SDO_SCS = {
    0: "upload_segment_response",
    1: "download_segment_respone",
    2: "initiate_upload_response",
    3: "initiate_download_response",
    4: "abort_transfer",
    5: "block_download",
    6: "block_upload",
}

SDO_ABORT_CODES = {
    0x0503_0000: "toggle_bit_not_alternated",
    0x0504_0000: "timed_out",
    0x0504_0001: "invalid_command_specifier",
    0x0504_0002: "invalid_block_size",
    0x0504_0003: "invalid_sequence_number",
    0x0504_0004: "crc_error",
    0x0504_0005: "out_of_memory",
    0x0601_0000: "unsupported_access_to_object",
    0x0601_0001: "write_only_object",
    0x0601_0002: "read_only_object",
    0x0602_0000: "object_does_not_exist",
    0x0604_0041: "object_cannot_be_mapped",
    0x0604_0042: "exceed_pdo_length",
    0x0604_0043: "general_parameter_incompatibility",
    0x0604_0047: "general_internal_incompatibility_in_device",
    0x0606_0000: "hardware_error",
    0x0607_0010: "parameter_type_does_not_match",
    0x0607_0012: "parameter_too_high",
    0x0607_0013: "parameter_too_low",
    0x0609_0011: "subindex_does_not_exist",
    0x0609_0030: "invalid_parameter_value",
    0x0609_0031: "write_value_too_high",
    0x0609_0032: "write_value_too_low",
    0x0609_0036: "maximum_less_than_minimum",
    0x060A_0023: "resource_not_available",
    0x0800_0000: "general_error",
    0x0800_0020: "data_cannot_be_transferred",
    0x0800_0021: "data_cannot_be_transferred_local_control",
    0x0800_0022: "data_cannot_be_transferred_device_state",
    0x0800_0023: "no_object_dictionary",
    0x0800_0024: "no_data_available",
}

RPDO_COMMS_INDEX_START = 0x1400
RPDO_MAP_INDEX_START = 0x1600
TPDO_COMMS_INDEX_START = 0x1800
TPDO_MAP_INDEX_START = 0x1A00


def write_dbc(name: str, od_db: dict[str, ObjectDictionary], manager: str = VECTOR):
    lines: list[str] = [
        f'VERSION "{__version__}"',
        "",
        "NS_ :",
        f"{INDENT4}NS_DESC_",
        f"{INDENT4}CM_",
        f"{INDENT4}BA_DEF_",
        f"{INDENT4}BA_",
        f"{INDENT4}VAL_",
        f"{INDENT4}CAT_DEF_",
        f"{INDENT4}CAT_",
        f"{INDENT4}FILTER",
        f"{INDENT4}BA_DEF_DEF_",
        f"{INDENT4}EV_DATA_",
        f"{INDENT4}ENVVAR_DATA_",
        f"{INDENT4}SGTYPE_",
        f"{INDENT4}SGTYPE_VAL_",
        f"{INDENT4}BA_DEF_SGTYPE_",
        f"{INDENT4}BA_SGTYPE_",
        f"{INDENT4}SIG_TYPE_REF_",
        f"{INDENT4}VAL_TABLE_",
        f"{INDENT4}SIG_GROUP_",
        f"{INDENT4}SIG_VALTYPE_",
        f"{INDENT4}SIGTYPE_VALTYPE_",
        f"{INDENT4}BO_TX_BU_",
        f"{INDENT4}BA_DEF_REL_",
        f"{INDENT4}BA_REL_",
        f"{INDENT4}BA_DEF_DEF_REL_",
        f"{INDENT4}BU_SG_REL_",
        f"{INDENT4}BU_EV_REL_",
        f"{INDENT4}BU_BO_REL_",
        f"{INDENT4}SG_MUL_VAL_",
        "",
        "BS_: 1000",  # bus speed in kbps
        "",
    ]

    # list nodes on the network
    lines.append("BU_: " + " ".join(list(od_db)) + " ")
    lines.append("")

    # general comments
    lines.append(f'CM_: "Generated by oresat-config {__version__}"')
    lines.append("")

    # SYNC
    lines.append(f"BO_ {0x80} sync: 0 {manager}")
    lines.append("")

    # TIME
    lines.append(f"BO_ {0x100} time: 6 {manager}")
    lines.append(f'{INDENT3}SG_ time_since_midnight : 0|28@1+ (1,0) [0|0] "ms" {VECTOR}')
    lines.append(f'{INDENT3}SG_ days_since_january_1_1984 : 32|16@1+ (1,0) [0|0] "days" {VECTOR}')
    lines.append("")

    enums: list[tuple[int, str, dict[int, str]]] = []
    signal_comments: list[tuple[int, str, str]] = []
    node_comments: list[tuple[int, str]] = []
    floats: list[tuple[int, str, int]] = []
    for node_name, od in od_db.items():
        node_comments.append((od.node_id, node_name))
        consumer = manager if node_name != manager else VECTOR

        # EMCYs
        cob_id = 0x80 + od.node_id
        lines.append(f"BO_ {cob_id} {node_name}_emcy: 8 {node_name}")
        lines.append(f'{INDENT3}SG_ emcy_error_code : 0|16@1+ (1,0) [0|0] "" {consumer}')
        lines.append(f'{INDENT3}SG_ error_reg_generic : 16|1@1+ (1,0) [0|0] "" {consumer}')
        lines.append(f'{INDENT3}SG_ error_reg_current : 17|1@1+ (1,0) [0|0] "" {consumer}')
        lines.append(f'{INDENT3}SG_ error_reg_voltage : 18|1@1+ (1,0) [0|0] "" {consumer}')
        lines.append(f'{INDENT3}SG_ error_reg_temperature : 19|1@1+ (1,0) [0|0] "" {consumer}')
        lines.append(f'{INDENT3}SG_ error_reg_communication : 20|1@1+ (1,0) [0|0] "" {consumer}')
        signal = "error_reg_device_profile_specific"
        lines.append(f'{INDENT3}SG_ {signal} : 21|1@1+ (1,0) [0|0] "" {consumer}')
        signal = "error_reg_manufacturer_specific"
        lines.append(f'{INDENT3}SG_ {signal} : 23|1@1+ (1,0) [0|0] "" {consumer}')
        lines.append(f'{INDENT3}SG_ emcy_data : 24|40@1+ (1,0) [0|0] "" {consumer}')
        lines.append("")
        enums.append((cob_id, "emcy_error_code", EMCY_ERROR_CODES))

        # PDOs
        for param_index in od:
            if param_index >= RPDO_COMMS_INDEX_START and param_index < RPDO_MAP_INDEX_START:
                pdo = "rpdo"
                comms_index_start = RPDO_COMMS_INDEX_START
                pdo_producer = consumer
                pdo_consumer = node_name
            elif param_index >= TPDO_COMMS_INDEX_START and param_index < TPDO_MAP_INDEX_START:
                pdo = "tpdo"
                comms_index_start = TPDO_COMMS_INDEX_START
                pdo_producer = node_name
                pdo_consumer = consumer
            else:
                continue

            pdo_lines = []
            mapping_index = param_index + 0x200
            num = param_index - comms_index_start + 1
            cob_id = od[param_index][1].value & 0x7FF
            sb = 0

            pdos = 12 if node_name == manager else 16
            if cob_id & 0x7F not in [od.node_id + i for i in range(pdos // 4)]:
                continue  # PDO for another node

            for subindex in od[mapping_index].subindices:
                if subindex == 0:
                    continue

                val = od[mapping_index][subindex].default
                mapped_index = (val >> 16) & 0xFFFF
                mapped_subindex = (val >> 8) & 0xFF
                mapped_size = val & 0xFF

                if isinstance(od[mapped_index], Variable):
                    obj = od[mapped_index]
                    signal = obj.name
                else:
                    obj = od[mapped_index][mapped_subindex]
                    signal = obj.parent.name + "_" + obj.name

                # value fields
                if not obj.bit_definitions:
                    sign = "+" if obj.data_type in UNSIGNED_TYPES else "-"
                    low = obj.min if obj.min is not None else 0
                    high = obj.max if obj.max is not None else 0
                    pdo_lines.append(
                        f"{INDENT3}SG_ {signal} : {sb}|{mapped_size}@1{sign} ({obj.factor},0) "
                        f'[{low}|{high}] "{obj.unit}" {pdo_consumer}'
                    )

                    if obj.description:
                        signal_comments.append((cob_id, signal, obj.description))

                    if obj.data_type == REAL32:
                        floats.append((cob_id, signal, 1))
                    elif obj.data_type == REAL64:
                        floats.append((cob_id, signal, 2))

                # bit fields
                for n, bits in obj.bit_definitions.items():
                    n_signal = f"{signal}_{n.lower()}"
                    bits = [bits] if isinstance(bits, int) else bits
                    pdo_lines.append(
                        f"{INDENT3}SG_ {n_signal} : {sb + max(bits)}|{len(bits)}@1+ (1,0) "
                        f'[0|0] "" {pdo_consumer}'
                    )

                sb += mapped_size
                if obj.value_descriptions:
                    enums.append((cob_id, signal, obj.value_descriptions))

            size = sb // 8
            lines.append(f"BO_ {cob_id} {node_name}_{pdo}_{num}: {size} {pdo_producer}")
            lines += pdo_lines
            lines.append("")

        # SDOs (useless for block SDO transfers)
        if node_name != manager:
            # client / tx
            cob_id = 0x580 + od.node_id
            lines.append(f"BO_ {cob_id} {node_name}_sdo_tx: 8 {node_name}")
            lines.append(f'{INDENT3}SG_ ccs M : 5|3@1+ (1,0) [0|0] "" {consumer}')  # multiplexor
            # ccs = 0
            lines.append(f'{INDENT3}SG_ more_segments m0 : 0|1@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ data_padding m0 : 1|3@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ toggle_bit m0 : 4|1@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ segment_data m0 : 8|56@1+ (1,0) [0|0] "" {consumer}')
            # ccs = 1
            lines.append(f'{INDENT3}SG_ size_indicated m1 : 0|1@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ expedited m1 : 1|1@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ data_padding m1 : 2|2@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ index m1 : 8|16@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ subindex m1 : 24|8@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ data m1 : 32|32@1+ (1,0) [0|0] "" {consumer}')
            # ccs = 2
            lines.append(f'{INDENT3}SG_ index m2 : 8|16@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ subindex m2 : 24|8@1+ (1,0) [0|0] "" {consumer}')
            # css = 3
            lines.append(f'{INDENT3}SG_ toggle_bit m3 : 4|1@1+ (1,0) [0|0] "" {consumer}')
            # ccs = 4
            lines.append(f'{INDENT3}SG_ index m4 : 8|16@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ subindex m4 : 24|8@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ abort_code m4 : 32|32@1+ (1,0) [0|0] "" {consumer}')
            # css = 5 & 6 have sub commands/multiplexor...
            lines.append("")
            enums.append((cob_id, "ccs", SDO_CSS))
            enums.append((cob_id, "abort_code", SDO_ABORT_CODES))

            # server / rx
            cob_id = 0x600 + od.node_id
            lines.append(f"BO_ {cob_id} {node_name}_sdo_rx: 8 {node_name}")
            lines.append(f'{INDENT3}SG_ scs M : 5|3@1+ (1,0) [0|0] "" {consumer}')  # multiplexor
            # scs = 0
            lines.append(f'{INDENT3}SG_ toggle_bit m0 : 4|1@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ data_padding m0 : 1|3@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ last_segment m0 : 0|1@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ segment_data m0 : 8|56@1+ (1,0) [0|0] "" {consumer}')
            # scs = 1
            lines.append(f'{INDENT3}SG_ toggle_bit m1 : 4|1@1+ (1,0) [0|0] "" {consumer}')
            # scs =2
            lines.append(f'{INDENT3}SG_ size_indicated m2 : 0|1@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ expedited m2 : 1|1@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ data_padding m2 : 2|2@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ index m2 : 8|16@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ subindex m2 : 24|8@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ data m2 : 32|32@1+ (1,0) [0|0] "" {consumer}')
            # scs = 3
            lines.append(f'{INDENT3}SG_ index m3 : 8|16@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ subindex m3 : 24|8@1+ (1,0) [0|0] "" {consumer}')
            # scs = 4
            lines.append(f'{INDENT3}SG_ index m4 : 8|16@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ subindex m4 : 24|8@1+ (1,0) [0|0] "" {consumer}')
            lines.append(f'{INDENT3}SG_ abort_code m4 : 32|32@1+ (1,0) [0|0] "" {consumer}')
            # scs = 5 & 6 have sub commands/multiplexor...
            lines.append("")
            enums.append((cob_id, "scs", SDO_SCS))
            enums.append((cob_id, "abort_code", SDO_ABORT_CODES))

        # heartbeats
        cob_id = 0x700 + od.node_id
        lines.append(f"BO_ {cob_id} {node_name}_heartbeat: 1 {node_name}")
        lines.append(f'{INDENT3}SG_ state : 0|7@1+ (1,0) [0|0] "" {consumer}')  # bit 7 is reserved
        enums.append((cob_id, "state", HB_STATES))
        lines.append("")
    lines.append("")

    # node comments
    for node_id, desc in node_comments:
        lines.append(f'CM_ BU_ {node_id} "{desc}";')
    lines.append("")

    # signal comments
    for cob_id, signal, desc in signal_comments:
        lines.append(f'CM_ SG_ {cob_id} {signal} "{desc}";')
    lines.append("")

    # signal enums
    for cob_id, signal, value_defs in enums:
        values = " ".join(f'{v} "{n}"' for v, n in value_defs.items())
        lines.append(f"VAL_ {cob_id} {signal} {values};")
    lines.append("")

    # signal floats
    for cob_id, signal, value in floats:
        lines.append(f"SIG_VALTYPE_ {cob_id} {signal} : {value};")

    with Path(f"{name}.dbc").open("w") as f:
        for line in lines:
            f.write(line + "\n")


def gen_dbc_node(
    card_od_config_path: str | Path,
    common_od_config_path: str | Path | None = None,
    node_id: int = DEFAULT_NODE_ID,
) -> None:
    if isinstance(card_od_config_path, str):
        card_od_config_path = Path(card_od_config_path)
    if isinstance(common_od_config_path, str):
        common_od_config_path = Path(common_od_config_path)

    card_od_config = OdConfig.from_yaml(card_od_config_path)
    if common_od_config_path is not None:
        common_od_config = OdConfig.from_yaml(common_od_config_path)
        od = gen_od([card_od_config, common_od_config])
    else:
        od = gen_od([card_od_config])
    set_od_node_id(od, node_id)
    write_dbc(card_od_config.name, {card_od_config.name: od})


def gen_dbc(cards_config_path: str | Path) -> None:
    if isinstance(cards_config_path, str):
        cards_config_path = Path(cards_config_path)

    cards_config = CardsConfig.from_yaml(cards_config_path)
    config_dir = cards_config_path.parent
    od_configs = load_od_configs(cards_config, config_dir)
    od_db = load_od_db(cards_config, od_configs)
    write_dbc("oresat", od_db, cards_config.manager.name)
