import uuid
import struct
import audioop

def create_unique_tag():
    return str(uuid.uuid4())


# /////////////////////////////////////////////////////////////////////////////
# RTP related functions
# /////////////////////////////////////////////////////////////////////////////
def parse_rtp_packet(packet):
    # RTP 頭部長度應該是 12 字節
    header = packet[:12]
    payload = packet[12:]
    
    # 正確解析 RTP 頭部的 12 字節
    rtp_header = struct.unpack('!BBHII', header)
    version = (rtp_header[0] >> 6) & 0x03
    padding = (rtp_header[0] >> 5) & 0x01
    extension = (rtp_header[0] >> 4) & 0x01
    csrc_count = rtp_header[0] & 0x0F
    marker = (rtp_header[1] >> 7) & 0x01
    payload_type = rtp_header[1] & 0x7F
    seq_num = rtp_header[2]
    timestamp = rtp_header[3]
    ssrc = rtp_header[4]
    
    return {
        'version': version,
        'padding': padding,
        'extension': extension,
        'csrc_count': csrc_count,
        'marker': marker,
        'payload_type': payload_type,
        'seq_num': seq_num,
        'timestamp': timestamp,
        'ssrc': ssrc,
        'payload': payload
    }


def decode_g711a(payload):
    # 使用G.711A-law解碼
    return audioop.alaw2lin(payload, 2)