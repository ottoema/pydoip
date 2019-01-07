#!/usr/bin/python3

from doip.doip import DoIP_Header, DoIP_protocol_version, DoIP_payload_type, DoIP_Protocol, Generic_DoIP_NACK_codes, DoIP_VA_VIR

class VA_VIR_Handler(object):
    def decode(self,data):

        import struct
        vin = str(data[0:17])
        logical_address = str(data[17:19])
        eid =  str(data[19:25])
        gid = str(data[25:31])
        far =  str(data[31:32])
        if (len(data)==33):
            vin_gid_sync_status = str(data[32:])
            va_vir = DoIP_VA_VIR(vin,logical_address,eid,gid,far,vin_gid_sync_status)
        else:
            va_vir = DoIP_VA_VIR(vin,logical_address,eid,gid,far)
        return va_vir