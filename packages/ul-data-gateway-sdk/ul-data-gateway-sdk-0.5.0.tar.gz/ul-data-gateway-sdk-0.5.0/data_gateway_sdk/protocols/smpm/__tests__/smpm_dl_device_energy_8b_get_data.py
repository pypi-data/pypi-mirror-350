from data_gateway_sdk.protocols.smpm.smpm_dl_device_energy_8b_get_data import SmpmDlDeviceEnergy8BGetDataData, SmpmDlDeviceEnergy8bGetDataDataRequestMonth, \
    SmpmDlDeviceEnergy8bGetDataDataRequestId
from data_gateway_sdk.utils.buf_ref import BufRef


def test_smpm_dl_device_energy_8b_get_data() -> None:
    case_serialized = bytes.fromhex("8001c5db09000000")
    assert SmpmDlDeviceEnergy8BGetDataData(year=2032, month=SmpmDlDeviceEnergy8bGetDataDataRequestMonth.JAN, day=15, request_data_pack_ids=(SmpmDlDeviceEnergy8bGetDataDataRequestId.UL_DATA_16B__ENERGY, SmpmDlDeviceEnergy8bGetDataDataRequestId.UNDEFINED)) == SmpmDlDeviceEnergy8BGetDataData.parse(BufRef(case_serialized))  # noqa: E501
    assert case_serialized == SmpmDlDeviceEnergy8BGetDataData.serialize(SmpmDlDeviceEnergy8BGetDataData(year=2032, month=SmpmDlDeviceEnergy8bGetDataDataRequestMonth.JAN, day=15, request_data_pack_ids=(SmpmDlDeviceEnergy8bGetDataDataRequestId.UL_DATA_16B__ENERGY, SmpmDlDeviceEnergy8bGetDataDataRequestId.UNDEFINED)))  # noqa: E501
    case_serialized = bytes.fromhex("800130d809000000")  # overflow
    assert SmpmDlDeviceEnergy8BGetDataData(year=2000, month=SmpmDlDeviceEnergy8bGetDataDataRequestMonth.DEC, day=0, request_data_pack_ids=(SmpmDlDeviceEnergy8bGetDataDataRequestId.UL_DATA_16B__ENERGY, SmpmDlDeviceEnergy8bGetDataDataRequestId.UNDEFINED)) == SmpmDlDeviceEnergy8BGetDataData.parse(BufRef(case_serialized))  # noqa: E501
    assert case_serialized == SmpmDlDeviceEnergy8BGetDataData.serialize(SmpmDlDeviceEnergy8BGetDataData(day=0, month=SmpmDlDeviceEnergy8bGetDataDataRequestMonth.DEC, request_data_pack_ids=(SmpmDlDeviceEnergy8bGetDataDataRequestId.UL_DATA_16B__ENERGY, SmpmDlDeviceEnergy8bGetDataDataRequestId.UNDEFINED), year=2000))  # noqa: E501
    case_serialized = bytes.fromhex("80f933d809000000")  # overflow
    assert SmpmDlDeviceEnergy8BGetDataData(year=2127, month=SmpmDlDeviceEnergy8bGetDataDataRequestMonth.DEC, day=0, request_data_pack_ids=(SmpmDlDeviceEnergy8bGetDataDataRequestId.UL_DATA_16B__ENERGY, SmpmDlDeviceEnergy8bGetDataDataRequestId.UNDEFINED)) == SmpmDlDeviceEnergy8BGetDataData.parse(BufRef(case_serialized))  # noqa: E501
    assert case_serialized == SmpmDlDeviceEnergy8BGetDataData.serialize(SmpmDlDeviceEnergy8BGetDataData(day=0, month=SmpmDlDeviceEnergy8bGetDataDataRequestMonth.DEC, request_data_pack_ids=(SmpmDlDeviceEnergy8bGetDataDataRequestId.UL_DATA_16B__ENERGY, SmpmDlDeviceEnergy8bGetDataDataRequestId.UNDEFINED), year=2127))  # noqa: E501
    case_serialized = bytes.fromhex("8001f0df09000000")  # overflow
    assert SmpmDlDeviceEnergy8BGetDataData(year=2000, month=SmpmDlDeviceEnergy8bGetDataDataRequestMonth.DEC, day=31, request_data_pack_ids=(SmpmDlDeviceEnergy8bGetDataDataRequestId.UL_DATA_16B__ENERGY, SmpmDlDeviceEnergy8bGetDataDataRequestId.UNDEFINED)) == SmpmDlDeviceEnergy8BGetDataData.parse(BufRef(case_serialized))  # noqa: E501
    assert case_serialized == SmpmDlDeviceEnergy8BGetDataData.serialize(SmpmDlDeviceEnergy8BGetDataData(day=31, month=SmpmDlDeviceEnergy8bGetDataDataRequestMonth.DEC, request_data_pack_ids=(SmpmDlDeviceEnergy8bGetDataDataRequestId.UL_DATA_16B__ENERGY, SmpmDlDeviceEnergy8bGetDataDataRequestId.UNDEFINED), year=2000))  # noqa: E501
    case_serialized = bytes.fromhex("80f9f3df09000000")  # overflow
    assert SmpmDlDeviceEnergy8BGetDataData(year=2127, month=SmpmDlDeviceEnergy8bGetDataDataRequestMonth.DEC, day=31, request_data_pack_ids=(SmpmDlDeviceEnergy8bGetDataDataRequestId.UL_DATA_16B__ENERGY, SmpmDlDeviceEnergy8bGetDataDataRequestId.UNDEFINED)) == SmpmDlDeviceEnergy8BGetDataData.parse(BufRef(case_serialized))  # noqa: E501
    assert case_serialized == SmpmDlDeviceEnergy8BGetDataData.serialize(SmpmDlDeviceEnergy8BGetDataData(day=31, month=SmpmDlDeviceEnergy8bGetDataDataRequestMonth.DEC, request_data_pack_ids=(SmpmDlDeviceEnergy8bGetDataDataRequestId.UL_DATA_16B__ENERGY, SmpmDlDeviceEnergy8bGetDataDataRequestId.UNDEFINED), year=2127))  # noqa: E501
