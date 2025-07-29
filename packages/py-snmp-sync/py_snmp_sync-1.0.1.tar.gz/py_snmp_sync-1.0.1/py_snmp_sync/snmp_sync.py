import socket

from pysnmp import error
from pysnmp.hlapi.v1arch import CommunityData

from pysnmp.proto.api import v1
from pyasn1.codec.ber import encoder, decoder

from pysnmp.smi import builder, view
from pysnmp.smi.rfc1902 import ObjectIdentity

# Create MIB builder and view
mib_builder = builder.MibBuilder()
mib_view = view.MibViewController(mib_builder)
# Load required MIBs
mib_builder.load_modules('SNMPv2-MIB')


class SyncUdpTransportTarget:
    """Synchronous UDP transport target for SNMP operations"""
    
    def __init__(self, transport_addr, timeout=1, retries=3, tag_list=()):
        if not (isinstance(transport_addr, tuple) and len(transport_addr) == 2):
            raise ValueError("transport_addr must be a tuple (host, port)")
        self.transport_addr = transport_addr
        self.timeout = timeout
        self.retries = retries
        self.tag_list = tag_list
        self.socket = None
        self._domain_name = 'udpv4'
    
    def get_transport_info(self):
        return self._domain_name, self.transport_addr
    
    def open_socket(self):
        if self.socket is None:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.socket.settimeout(self.timeout)
                self.socket.connect(self.transport_addr)
            except Exception as e:
                raise error.PySnmpError(f"Failed to create socket: {e}")
    
    def close_socket(self):
        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass
            self.socket = None
    
    def send_and_receive(self, message):
        self.open_socket()
        
        last_error = None
        for attempt in range(self.retries + 1):
            try:
                # Send the message
                bytes_sent = self.socket.send(message)
                if bytes_sent != len(message):
                    raise error.PySnmpError("Failed to send complete message")

                # Receive response
                response = self.socket.recv(65535)
                return response

            except socket.timeout as e:
                last_error = e
                if attempt == self.retries:
                    raise error.PySnmpError(
                        f"SNMP timeout after {self.retries + 1} tries"
                    )
            except Exception as e:
                self.close_socket()
                raise error.PySnmpError(f"Socket error: {e}")
        
        # Should not reach here, but just in case
        raise error.PySnmpError(f"All retries failed. Last error: {last_error}")
    
    def __enter__(self):
        self.open_socket()
        return self
    
    def __exit__(self, *exc_info):
        self.close_socket()


def sync_get_cmd(community, transport_target, *var_names):
    """
    Synchronous SNMP GET command implementation
    Args:
        community: SNMP community. E.g., CommunityData("public", mpModel=0)
        transport_target: SyncUdpTransportTarget instance
        *var_names: Variable names (ObjectIdentity or OID strings)
    Returns: (error_indication, error_status, error_index, var_binds)
    """
    try:
        # Build PDU
        proto = v1
        pdu = proto.GetRequestPDU()
        proto.apiPDU.set_defaults(pdu)
        request_id = proto.apiPDU.get_request_id(pdu)
        proto.apiPDU.set_request_id(pdu, request_id)
        varbinds = []
        for i in var_names:
            if isinstance(i, str):
                varbinds.append((i, proto.Null()))
            else:
                i.resolve_with_mib(mib_view)
                varbinds.append((i.get_oid(), proto.Null()))
        proto.apiPDU.set_varbinds(pdu, varbinds)
        
        # Build message
        msg = proto.Message()
        proto.apiMessage.set_defaults(msg)
        proto.apiMessage.set_community(
            msg,
            community if isinstance(community, str) else community.communityName
        )
        proto.apiMessage.set_pdu(msg, pdu)
        
        # Encode message
        msg_bytes = encoder.encode(msg)
        
        # Send message using our custom transport
        try:
            response_bytes = transport_target.send_and_receive(msg_bytes)
        except Exception as e:
            return str(e), None, None, []
        
        # Decode response using the tested approach
        rsp_msg, _ = decoder.decode(response_bytes, asn1Spec=proto.Message())
        rsp_pdu = proto.apiMessage.get_pdu(rsp_msg)
        error_status = proto.apiPDU.get_error_status(rsp_pdu)
        error_index = proto.apiPDU.get_error_index(rsp_pdu)
        var_binds = proto.apiPDU.get_varbinds(rsp_pdu)
        
        # Return in a format similar to get_cmd
        if error_status:
            return None, error_status, error_index, []
        else:
            return None, None, None, var_binds
        
    except Exception as e:
        return str(e), None, None, []
