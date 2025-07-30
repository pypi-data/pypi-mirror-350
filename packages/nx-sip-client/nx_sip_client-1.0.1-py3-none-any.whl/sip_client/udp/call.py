import re
import time
import ctypes
import random
import socket
import struct
import hashlib
import audioop
import logging
import platform
import threading
from collections import deque

from .call_fsm import CallState, CallEvent, CallFSM
from .utils import create_unique_tag, parse_rtp_packet, decode_g711a

logger = logging.getLogger('sip')

# 定義Call類來使用FSM管理呼叫狀態
class Call:
    def __init__(
            self,
            sc,
            sip_socket,
            domain=None,
            port=None,
            username=None,
            password=None,
            opp_username=None,
            sender_addr=None,
            rtp_port=None,
            rtcp_port=None
            ):
        self.sc = sc
        self.sip_socket = sip_socket
        self.domain = domain  # server domain
        self.port = port  # server port
        self.username = username
        self.password = password
        self.opp_username = opp_username
        self.sender_addr = sender_addr  # address of the nearest sender, used to append to Via header
        self.rtp_port = rtp_port
        self.rtcp_port = rtcp_port

        self.local_ip, self.local_port = sip_socket.getsockname()  # transport address

        self.fsm = CallFSM(self)
        self.recv_msg = ''
        self.invite_msg = ''  # backup for CANCEL
        self.call_id = None
        self.invite_branch = None
        self.invite_cseq = None
        self.cseq_num = 1
        self.transfer_username = None
        self.my_tag = None
        self.opp_tag = None

        # RTP parameters
        self.channels = 1
        self.rate = 8000
        self.interval = 0.02  # 20ms per frame
        self.stop_event = threading.Event()

        self.running = True
        self.audio_recv_buffer = deque(maxlen=1000)  # buffer for 20s audio
        self.audio_send_buffer = deque(maxlen=10000)  # 20ms per frame, buffer for 200s audio
        self.ssrc = random.randint(0, 0xFFFFFFFF)  # identifier for RTP stream
        self.cname = random.randint(0, 0xFFFFFFFF)  # identifier for RTCP to the same stream source
        self.rtp_socket = None
        self.rtcp_socket = None

    def bind_rtp_rtcp_sockets(self):
        # Create sockets for RTP and RTCP
        self.rtp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rtcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if self.rtp_port is not None:
            self.rtcp_port = self.rtcp_port if self.rtcp_port else self.rtp_port + 1
            try:
                self.rtp_socket.bind((self.local_ip, self.rtp_port))
                self.rtcp_socket.bind((self.local_ip, self.rtp_port + 1))
            except socket.error:
                logger.warning(f'Failed to bind specified ports {self.rtp_port} and {self.rtp_port + 1}')
                self.rtp_socket.close()
                self.rtcp_socket.close()
                self.rtp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.rtcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.bind_dynamic_ports()  # Fallback to dynamic port selection
        else:
            # If no port specified, directly bind to dynamic ports
            self.bind_dynamic_ports()
        
        self.rtp_socket.settimeout(1)
        self.rtcp_socket.settimeout(1)
        logger.info(f'RTP socket bound to {self.rtp_port}')
        logger.info(f'RTCP socket bound to {self.rtcp_port}')

    def bind_dynamic_ports(self):
        logger.debug('Binding RTP and RTCP to dynamic ports')
        while True:
            try:
                # Let the system select an available port for RTP
                self.rtp_socket.bind((self.local_ip, 0))
                self.rtp_port = self.rtp_socket.getsockname()[1]

                # Ensure RTP port is even
                if self.rtp_port % 2 == 0:
                    # Attempt to bind RTCP to the next port (odd)
                    self.rtcp_port = self.rtp_port + 1
                    self.rtcp_socket.bind((self.local_ip, self.rtcp_port))
                    break
                else:
                    # If RTP port is odd, reset sockets and try again
                    self.rtp_socket.close()
                    self.rtcp_socket.close()
                    self.rtp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    self.rtcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            except socket.error:
                # Retry in case of any binding errors
                self.rtp_socket.close()
                self.rtcp_socket.close()
                self.rtp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.rtcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def unbind_rtp_socket(self):
        if self.rtp_socket:
            self.rtp_socket.close()
            self.rtp_socket = None

    def start_audio(self):
        recv_thread = threading.Thread(target=self.receive_rtp_threading, daemon=True)
        recv_thread.start()
        send_thread = threading.Thread(target=self.send_rtp_threading, daemon=True)
        send_thread.start()
        
        # 發送一個假RTP封包以在NAT或防火牆打洞，否則將無法接收到對方的RTP封包
        self.send_dummy_rtp_packet()

    def send_dummy_rtp_packet(self):
        dummy_packet = self.create_rtp_packet(0, 0, 8, b'\x00' * 160)  # 創建一個假RTP封包，payload為160個0字節
        self.rtp_socket.sendto(dummy_packet, (self.opp_rtp_ip, self.opp_rtp_port))
        logger.debug(f'Sent dummy RTP packet to {self.opp_rtp_ip}:{self.opp_rtp_port}')

    def receive_rtp_threading(self):
        while self.running:
            # no need sleep since socket has timeout
            try:
                data, _ = self.rtp_socket.recvfrom(2048)
                if data:
                    rtp_packet = parse_rtp_packet(data)  # 解析RTP封包
                    raw_audio = decode_g711a(rtp_packet['payload'])  # 解碼RTP payload
                    self.audio_recv_buffer.append(raw_audio)  # 保存解碼的音頻數據
            except socket.timeout:
                continue
            except socket.error:
                if self.running:
                    logger.exception("RTP socket error")
                break

    def send_rtp_threading(self):
        # Change the default time resolution of Windows from 15ms to 1ms
        if platform.system() == 'Windows':
            ctypes.windll.winmm.timeBeginPeriod(1)
            
        seq_num = 0
        timestamp = 0
        payload_type = 8  # PCMA
        next_time = time.perf_counter() + self.interval
        while self.running:
            if len(self.audio_send_buffer) > 0:
                frame = self.audio_send_buffer.popleft()  # except raw_audio have 320 bytes
                raw_audio = audioop.lin2alaw(frame, 2)
                rtp_packet = self.create_rtp_packet(seq_num, timestamp, payload_type, raw_audio)
                self.rtp_socket.sendto(rtp_packet, (self.opp_rtp_ip, self.opp_rtp_port))
                timestamp += 160
                seq_num += 1

            # Calculate the next time to send the next frame
            next_time += self.interval
            delay = next_time - time.perf_counter()
            if delay > 0:
                self.stop_event.wait(delay)
            
        if platform.system() == 'Windows':
            ctypes.windll.winmm.timeEndPeriod(1)
    
    def create_rtp_packet(self, seq_num, timestamp, payload_type, payload):
        rtp_header = struct.pack('!BBHII',
                                 0x80,
                                 payload_type,
                                 seq_num,
                                 timestamp,
                                 self.ssrc)
        return rtp_header + payload
    
    def safe_sendto(self, data, addr, max_retries=5):
        """
        Re-package socket.sendto to do retry and exception handling
        """
        delay = 1  # initial delay time
        for retry in range(max_retries):
            try:
                self.sip_socket.sendto(data, addr)
                return True
            except OSError as e:
                logger.error(f"{retry+1} times failed to send data: {e}")
                time.sleep(delay)
                delay *= 2  # exponential backoff
        # exceed max retries
        logger.error("Reach max retries, failed to send data")
        return False

    #######################################
    # Make call operations
    #######################################
    def send_invite(self, retry_auth=False):
        sdp = (
            'v=0\r\n'
            f'o=- {int(time.time())} {int(time.time())} IN IP4 {self.local_ip}\r\n'
            's=pjmedia\r\n'
            'b=AS:84\r\n'
            't=0 0\r\n'
            'a=X-nat:0\r\n'
            f'm=audio {self.rtp_port} RTP/AVP 8 120\r\n'
            f'c=IN IP4 {self.local_ip}\r\n'
            'b=TIAS:64000\r\n'
            f'a=rtcp:{self.rtcp_port} IN IP4 {self.local_ip}\r\n'
            'a=sendrecv\r\n'
            'a=rtpmap:8 PCMA/8000\r\n'
            'a=rtpmap:120 telephone-event/8000\r\n'
            'a=fmtp:120 0-16\r\n'
            f'a=ssrc:{self.ssrc} cname:{self.cname}\r\n'
        )
        sdp_length = len(sdp)

        self.call_id = create_unique_tag()
        self.invite_branch = 'z9hG4bKPj' + create_unique_tag()
        self.invite_cseq = self.cseq_num
        self.cseq_num += 1
        self.my_tag = create_unique_tag()

        invite_msg = (
            f'INVITE sip:{self.opp_username}@{self.domain}:{self.port} SIP/2.0\r\n'
            f'Via: SIP/2.0/UDP {self.local_ip}:{self.local_port};rport;branch={self.invite_branch}\r\n'
            'Max-Forwards: 70\r\n'
            f'From: sip:{self.username}@{self.domain};tag={self.my_tag}\r\n'
            f'To: sip:{self.opp_username}@{self.domain}\r\n'
            f'Contact: <sip:{self.username}@{self.local_ip}:{self.local_port};ob>\r\n'
            f'Call-ID: {self.call_id}\r\n'
            f'CSeq: {self.invite_cseq} INVITE\r\n'
            'Allow: PRACK, INVITE, ACK, BYE, CANCEL, UPDATE, INFO, SUBSCRIBE, NOTIFY, REFER, MESSAGE, OPTIONS\r\n'
            'Supported: replaces, 100rel, timer, norefersub\r\n'
            'Session-Expires: 1800\r\n'
            'Min-SE: 90\r\n'
            'Content-Type: application/sdp\r\n'
            f'Content-Length: {sdp_length}\r\n\r\n'
        )
        invite_msg += sdp

        # Add Authorization header if retry_auth is True, this appears in Panasonic PBX
        if retry_auth:
            def _generate_auth_response(method, uri, nonce, realm, username, password):
                ha1 = hashlib.md5(f"{username}:{realm}:{password}".encode()).hexdigest()
                ha2 = hashlib.md5(f"{method}:{uri}".encode()).hexdigest()
                response = hashlib.md5(f"{ha1}:{nonce}:{ha2}".encode()).hexdigest()
                return response
            
            nonce = self.recv_msg.split('nonce="')[1].split('"')[0]
            realm = self.recv_msg.split('realm="')[1].split('"')[0]
            
            if nonce and realm:
                uri = f'sip:{self.opp_username}@{self.domain}:{self.port}'
                hdr = ('Proxy-Authorization'
                       if 'Proxy Authentication Required' in self.recv_msg
                       else 'Authorization')
                response = _generate_auth_response('INVITE', uri, nonce, realm, self.username, self.password)
                auth_header = (
                    f'{hdr}: Digest username="{self.username}", realm="{realm}", '
                    f'nonce="{nonce}", uri="{uri}", response="{response}", algorithm=MD5\r\n'
                )
                invite_msg = invite_msg.replace('Max-Forwards: 70\r\n', f'Max-Forwards: 70\r\n{auth_header}')

        logger.debug('############ Sending INVITE ############ ')
        logger.debug(invite_msg)
        logger.debug('############ end of INVITE ############')
        self.safe_sendto(invite_msg.encode(), (self.domain, self.port))
        self.invite_msg = invite_msg  # backup for CANCEL

    def send_ack_for_auth(self):  # make call in Panasonic PBX when auth is required
        call_id = self.recv_msg.split('Call-ID: ')[1].split('\r\n')[0]
        assert call_id == self.call_id

        via_header = self.recv_msg.split('Via: ')[1].split('\r\n')[0]
        from_header = self.recv_msg.split('From: ')[1].split('\r\n')[0]
        to_header = self.recv_msg.split('To: ')[1].split('\r\n')[0]
        cseq = self.recv_msg.split('CSeq: ')[1].split(' ')[0]

        ack = (
            f'ACK sip:{self.opp_username}@{self.domain}:{self.port} SIP/2.0\r\n'
            f'Via: {via_header}\r\n'
            f'From: {from_header}\r\n'
            f'To: {to_header}\r\n'
            f'Call-ID: {self.call_id}\r\n'
            f'CSeq: {cseq} ACK\r\n'
            'Content-Length: 0\r\n\r\n'
        )
        logger.debug('############ Sending ACK ############ ')
        logger.debug(ack)
        logger.debug('############ end of ACK ############')
        self.safe_sendto(ack.encode(), (self.domain, self.port))

    def handle_180_ringing(self):  # need to send PRACK in NEC PBX
        # Parse necessary headers
        self.contact_uri = self.recv_msg.split('Contact: <')[1].split('>\r\n')[0]
        self.opp_tag = self.recv_msg.split('To: ')[1].split('\r\n')[0].split('tag=')[1]
        # Update invite msg with opp_tag
        self._update_invite_msg_with_to_tag(self.opp_tag)

        # Check if 100rel is required, if yes, need to send PRACK
        if 'Require: 100rel' in self.recv_msg and 'RSeq: ' in self.recv_msg:
            logger.debug("Reliable provisional response received. Sending PRACK.")
            self.send_prack()
        else:
            logger.debug("Non-reliable provisional response. No PRACK required.")

    def send_prack(self):
        ring_call_id = self.recv_msg.split('Call-ID: ')[1].split('\r\n')[0]
        assert ring_call_id == self.call_id

        contact_uri = self.recv_msg.split('Contact: <')[1].split('>\r\n')[0]
        prack_branch = 'z9hG4bKPj' + create_unique_tag()
        
        prack_cseq = self.cseq_num
        self.cseq_num += 1
        rseq = self.recv_msg.split('RSeq: ')[1].split('\r\n')[0]
        
        prack = (
            f'PRACK {contact_uri} SIP/2.0\r\n'
            f'Via: SIP/2.0/UDP {self.local_ip}:{self.local_port};rport;branch={prack_branch}\r\n'
            'Max-Forwards: 70\r\n'
            f'From: sip:{self.username}@{self.domain};tag={self.my_tag}\r\n'
            f'To: sip:{self.opp_username}@{self.domain};tag={self.opp_tag}\r\n'
            f'Call-ID: {self.call_id}\r\n'
            f'CSeq: {prack_cseq} PRACK\r\n'
            f'RAck: {rseq} {self.invite_cseq} INVITE\r\n'
            'Content-Length: 0\r\n\r\n'
        )
        logger.debug('############ Sending PRACK ############ ')
        logger.debug(prack)
        logger.debug('############ end of PRACK ############')
        self.safe_sendto(prack.encode(), (self.domain, self.port))
        self.fsm.handle_event(CallEvent.PRACK_SENT)

    def send_ack_for_ok(self):
        ok_call_id = self.recv_msg.split('Call-ID: ')[1].split('\r\n')[0]
        assert ok_call_id == self.call_id
        ### 還要檢查fram_tag和to_tag是否正確

        contact_uri = self.recv_msg.split('Contact: <')[1].split('>\r\n')[0]
        ack_branch = 'z9hG4bKPj' + create_unique_tag()
        from_header = self.recv_msg.split('From: ')[1].split('\r\n')[0]
        to_header = self.recv_msg.split('To: ')[1].split('\r\n')[0]
        # self.call_id = self.recv_msg.split('Call-ID: ')[1].split('\r\n')[0]
        # cseq = self.recv_msg.split('CSeq: ')[1].split(' INVITE')[0]
        
        ack = (
            f'ACK {contact_uri} SIP/2.0\r\n'
            f'Via: SIP/2.0/UDP {self.local_ip}:{self.local_port};rport;branch={ack_branch}\r\n'
            'Max-Forwards: 70\r\n'
            f'From: {from_header}\r\n'
            f'To: {to_header}\r\n'
            f'Call-ID: {self.call_id}\r\n'
            f'CSeq: {self.invite_cseq} ACK\r\n'  # 原本寫的是cseq
            'Content-Length: 0\r\n\r\n'
        )
        logger.debug('############ Sending ACK ############ ')
        logger.debug(ack)
        logger.debug('############ end of ACK ############')
        self.safe_sendto(ack.encode(), (self.domain, self.port))
        self.fsm.handle_event(CallEvent.ACK_SENT)

    def send_ok_for_bye(self):
        via_header = self.recv_msg.split('Via: ')[1].split('\r\n')[0]
        from_header = self.recv_msg.split('From: ')[1].split('\r\n')[0]
        to_header = self.recv_msg.split('To: ')[1].split('\r\n')[0]
        bye_cseq = self.recv_msg.split('CSeq: ')[1].split(' BYE')[0]
        bye_ack = (
            f'SIP/2.0 200 OK\r\n'
            f'Via: {via_header};received={self.sender_addr[0]}\r\n'
            f'From: {from_header}\r\n'
            f'To: {to_header}\r\n'
            f'Call-ID: {self.call_id}\r\n'
            f'CSeq: {bye_cseq} BYE\r\n'
            'Content-Length: 0\r\n\r\n'
        )
        logger.debug('############ Sending 200 OK for BYE ############')
        logger.debug(bye_ack)
        logger.debug('############ end of 200 OK ############')
        self.safe_sendto(bye_ack.encode(), (self.domain, self.port))

    #######################################
    # Answer call operations
    # #####################################      
    def send_trying(self):
        # recv_msg must be the same as invite_msg at this point
        via_header = self.invite_msg.split('Via: ')[1].split('\r\n')[0]
        opp_uri = self.invite_msg.split('From: ')[1].split('\r\n')[0].split('<')[1].split('>')[0]
        from_header = self.invite_msg.split('From: ')[1].split('\r\n')[0]
        to_header = self.invite_msg.split('To: ')[1].split('\r\n')[0]

        self.opp_username = opp_uri.split('@')[0].split(':')[1]
        self.invite_branch = self.invite_msg.split('Via: ')[1].split('\r\n')[0].split('branch=')[1]
        self.call_id = self.invite_msg.split('Call-ID: ')[1].split('\r\n')[0]
        self.invite_cseq = int(self.invite_msg.split('CSeq: ')[1].split(' INVITE')[0])
        
        try_resp = (
            f"SIP/2.0 100 Trying\r\n"
            f"Via: {via_header};received={self.sender_addr[0]}\r\n"
            f'From: {from_header}\r\n'
            f"To: {to_header}\r\n"
            f"Call-ID: {self.call_id}\r\n"
            f"CSeq: {self.invite_cseq} INVITE\r\n"
            "Content-Length: 0\r\n\r\n"
        )

        self.safe_sendto(try_resp.encode(), (self.domain, self.port))
        logger.debug("############ Sending 100 Trying ############")
        logger.debug(try_resp)
        logger.debug('############ end of 100 Trying ############')

    def send_ringing(self):
        # recv_msg must be the same as invite_msg at this point
        via_header = self.invite_msg.split('Via: ')[1].split('\r\n')[0]
        from_header = self.invite_msg.split('From: ')[1].split('\r\n')[0]
        to_header = self.invite_msg.split('To: ')[1].split('\r\n')[0]
        self.opp_tag = self.invite_msg.split('From: ')[1].split('\r\n')[0].split('tag=')[1]
        self.my_tag = create_unique_tag()

        ring_resp = (
            f"SIP/2.0 180 Ringing\r\n"
            f"Via: {via_header};received={self.sender_addr[0]}\r\n"
            f'From: {from_header}\r\n'
            f"To: {to_header};tag={self.my_tag}\r\n"
            f"Call-ID: {self.call_id}\r\n"
            f"CSeq: {self.invite_cseq} INVITE\r\n"
            f"Contact: <sip:{self.username}@{self.local_ip}:{self.local_port};ob>\r\n"
            "Allow: PRACK, INVITE, ACK, BYE, CANCEL, UPDATE, INFO, SUBSCRIBE, NOTIFY, REFER, MESSAGE, OPTIONS\r\n"
            "Content-Length: 0\r\n\r\n"
        )
        self.safe_sendto(ring_resp.encode(), (self.domain, self.port))
        logger.debug("############ Sending 180 Ringing ############")
        logger.debug(ring_resp)
        logger.debug('############ end of 180 Ringing ############')

        # update invite msg with my_tag
        self._update_invite_msg_with_to_tag(self.my_tag)

    def send_ok_for_invite(self):
        sdp = (
            'v=0\r\n'
            f'o=- {int(time.time())} {int(time.time())} IN IP4 {self.local_ip}\r\n'
            's=pjmedia\r\n'
            'b=AS:84\r\n'
            't=0 0\r\n'
            'a=X-nat:0\r\n'
            f'm=audio {self.rtp_port} RTP/AVP 8 101\r\n'
            f'c=IN IP4 {self.local_ip}\r\n'
            'b=TIAS:64000\r\n'
            f'a=rtcp:{self.rtcp_port} IN IP4 {self.local_ip}\r\n'
            'a=sendrecv\r\n'
            'a=rtpmap:8 PCMA/8000\r\n'
            'a=rtpmap:101 telephone-event/8000\r\n'
            'a=fmtp:101 0-16\r\n'
            f'a=ssrc:{self.ssrc} cname:{self.cname}\r\n'
        )
        sdp_length = len(sdp)

        via_header = self.recv_msg.split('Via: ')[1].split('\r\n')[0]
        from_header = self.recv_msg.split('From: ')[1].split('\r\n')[0]
        to_header = self.recv_msg.split('To: ')[1].split('\r\n')[0]

        ok_resp = (
            f'SIP/2.0 200 OK\r\n'
            f"Via: {via_header};received={self.sender_addr[0]}\r\n"
            f'From: {from_header}\r\n'
            f"To: {to_header};tag={self.my_tag}\r\n"
            f"Call-ID: {self.call_id}\r\n"
            f"CSeq: {self.invite_cseq} INVITE\r\n"
            f"Contact: <sip:{self.username}@{self.local_ip}:{self.local_port};ob>\r\n"
            "Allow: PRACK, INVITE, ACK, BYE, CANCEL, UPDATE, INFO, SUBSCRIBE, NOTIFY, REFER, MESSAGE, OPTIONS\r\n"
            'Supported: replaces, 100rel, timer, norefersub\r\n'
            'User-Agent: My SIP Client\r\n'
            'Session-Expires: 1800;refresher=uac\r\n'
            'Require: timer\r\n'
            'Content-Type: application/sdp\r\n'
            f'Content-Length: {sdp_length}\r\n\r\n'
        )
        ok_resp += sdp

        logger.debug('############ Sending 200 OK ############')
        logger.debug(ok_resp)
        logger.debug('############ end of 200 OK ############')
        self.safe_sendto(ok_resp.encode(), (self.domain, self.port))

    #######################################
    # Transfer call operations
    #######################################
    def send_reinvite(self):
        sdp = (
            'v=0\r\n'
            f'o=- {int(time.time())} {int(time.time())} IN IP4 {self.local_ip}\r\n'
            's=pjmedia\r\n'
            'b=AS:84\r\n'
            't=0 0\r\n'
            'a=X-nat:0\r\n'
            f'm=audio {self.rtp_port} RTP/AVP 8 101\r\n'
            f'c=IN IP4 {self.local_ip}\r\n'
            'b=TIAS:64000\r\n'
            f'a=rtcp:{self.rtp_port + 1} IN IP4 {self.local_ip}\r\n'
            'a=sendonly\r\n'  # sendonly for hold
            'a=rtpmap:8 PCMA/8000\r\n'
            'a=rtpmap:101 telephone-event/8000\r\n'
            'a=fmtp:101 0-16\r\n'
            f'a=ssrc:{self.ssrc} cname:{self.cname}\r\n'
        )
        sdp_length = len(sdp)
        
        self.reinvite_branch = 'z9hG4bKPj' + create_unique_tag()
        self.reinvite_cseq = self.cseq_num
        self.cseq_num += 1
        reinvite_request = (
            f'INVITE sip:{self.domain}:{self.port} SIP/2.0\r\n'
            f'Via: SIP/2.0/UDP {self.local_ip}:{self.local_port};branch={self.reinvite_branch};rport\r\n'
            f'From: <sip:{self.username}@{self.local_ip}>;tag={self.my_tag}\r\n'
            f'To: <sip:{self.opp_username}@{self.domain}>;tag={self.opp_tag}\r\n'
            f'Call-ID: {self.call_id}\r\n'
            f'CSeq: {self.reinvite_cseq} INVITE\r\n'
            f'Contact: <sip:{self.username}@{self.local_ip}:{self.local_port}>\r\n'
            'Max-Forwards: 70\r\n'
            'Supported: replaces, path, timer\r\n'
            'User-Agent: My SIP Client\r\n'
            'Session-Expires: 180;refresher=uas\r\n'
            'Min-SE: 180\r\n'
            'Allow: INVITE, ACK, OPTIONS, CANCEL, BYE, SUBSCRIBE, NOTIFY, INFO, REFER, UPDATE, MESSAGE\r\n'
            'Content-Type: application/sdp\r\n'
            'Accept: application/sdp, application/dtmf-relay\r\n'
            f'Content-Length: {sdp_length}\r\n\r\n'
        )
        reinvite_request += sdp

        logger.debug("############ Sending RE-INVITE for Hold ############")
        logger.debug(reinvite_request)
        logger.debug("############ End of RE-INVITE ############")

        self.safe_sendto(reinvite_request.encode(), (self.domain, self.port))
        self.fsm.handle_event(CallEvent.REINVITE_SENT)

    def send_refer(self, target_username):
        self.refer_branch = 'z9hG4bKPj' + create_unique_tag()
        refer_cseq = self.cseq_num
        self.cseq_num += 1
        refer_to_header = f'Refer-To: <sip:{target_username}@{self.domain}:{self.port}>'
        regerred_by_header = f'Referred-By: <sip:{self.username}@{self.domain}:{self.port}>'
        refer_request = (
            f'REFER sip:{self.opp_username}@{self.domain}:{self.port} SIP/2.0\r\n'
            f'Via: SIP/2.0/UDP {self.local_ip}:{self.local_port};rport;branch={self.refer_branch}\r\n'
            f'From: <sip:{self.username}@{self.local_ip}>;tag={self.my_tag}\r\n'
            f'To: "{self.opp_username}" <sip:{self.opp_username}@{self.domain}>;tag={self.opp_tag}\r\n'
            f'Call-ID: {self.call_id}\r\n'
            f'CSeq: {refer_cseq} REFER\r\n'
            f'Contact: <sip:{self.username}@{self.local_ip}:{self.local_port}>\r\n'
            'Max-Forwards: 70\r\n'
            'Supported: replaces, path, timer\r\n'
            f'User-Agent: My SIP Client\r\n'
            'Allow: INVITE, ACK, OPTIONS, CANCEL, BYE, SUBSCRIBE, NOTIFY, INFO, REFER, UPDATE, MESSAGE\r\n'
            f'{refer_to_header}\r\n'
            f'{regerred_by_header}\r\n'
            f'Content-Length: 0\r\n\r\n'
        )
        
        logger.debug("############ Sending REFER ############")
        logger.debug(refer_request)
        logger.debug("############ End of REFER ############")
        
        self.safe_sendto(refer_request.encode(), (self.domain, self.port))
        self.fsm.handle_event(CallEvent.REFER_SENT)

    def send_ok_for_notify(self):
        via_header = self.recv_msg.split('Via: ')[1].split('\r\n')[0]
        from_header = self.recv_msg.split('From: ')[1].split('\r\n')[0]
        to_header = self.recv_msg.split('To: ')[1].split('\r\n')[0]
        notify_cseq = self.recv_msg.split('CSeq: ')[1].split(' NOTIFY')[0]

        notify_resp = (
            f'SIP/2.0 200 OK\r\n'
            f'Via: {via_header}\r\n'
            f'From: {from_header}\r\n'
            f'To: {to_header}\r\n'
            f'Call-ID: {self.call_id}\r\n'
            f'CSeq: {notify_cseq} NOTIFY\r\n'
            f'Contact: <sip:{self.username}@{self.local_ip}:{self.local_port}>\r\n'
            'Supported: replaces, path, timer\r\n'
            'User-Agent: My SIP Client\r\n'
            'Allow: INVITE, ACK, OPTIONS, CANCEL, BYE, SUBSCRIBE, NOTIFY, INFO, REFER, UPDATE, MESSAGE\r\n'
            'Content-Length: 0\r\n\r\n'
        )
        
        logger.debug("############ Sending NOTIFY OK ############")
        logger.debug(notify_resp)
        logger.debug("############ End of NOTIFY OK ############")
        
        self.safe_sendto(notify_resp.encode(), (self.domain, self.port))

    #######################################
    # Session Timer operations
    #######################################
    def send_ok_for_invite_check(self):
        ok_call_id = self.recv_msg.split('Call-ID: ')[1].split('\r\n')[0]
        assert ok_call_id == self.call_id

        via_header = self.recv_msg.split('Via: ')[1].split('\r\n')[0]
        contact_uri = self.recv_msg.split('Contact: <')[1].split('>\r\n')[0]
        from_header = self.recv_msg.split('From: ')[1].split('\r\n')[0]
        to_header = self.recv_msg.split('To: ')[1].split('\r\n')[0]
        self.call_id = self.recv_msg.split('Call-ID: ')[1].split('\r\n')[0]
        cseq = self.recv_msg.split('CSeq: ')[1].split(' INVITE')[0]

        # Adding and updating necessary headers
        ok_response = (
            f'SIP/2.0 200 OK\r\n'
            f'Via: {via_header};rport;received={self.sender_addr[0]}\r\n'
            f'From: {from_header}\r\n'
            f'To: {to_header}\r\n'
            f'Call-ID: {self.call_id}\r\n'
            f'CSeq: {cseq} INVITE\r\n'
            f'Contact: <{contact_uri}>\r\n'
            f'Supported: replaces, timer\r\n'
            f'Session-Expires: 1800;refresher=uas\r\n'
            'Content-Length: 0\r\n\r\n'
        )

        logger.debug('############ Sending 200 OK for INVITE Session Timer ############')
        logger.debug(ok_response)
        logger.debug('############ end of 200 OK ############')
        self.safe_sendto(ok_response.encode(), (self.domain, self.port))

    #######################################
    # Cancel call operations
    #######################################
    def send_cancel(self):
        """ (sender)
        Make call but cancel it before it is answered.
        """
        via_header = self.invite_msg.split('Via: ')[1].split('\r\n')[0]
        from_header = self.invite_msg.split('From: ')[1].split('\r\n')[0]
        to_header = self.invite_msg.split('To: ')[1].split('\r\n')[0]

        cancel_request = (
            f'CANCEL sip:{self.opp_username}@{self.domain}:{self.port} SIP/2.0\r\n'
            f'Via: {via_header}\r\n'
            f'From: {from_header}\r\n'
            f'To: {to_header}\r\n'
            f'Call-ID: {self.call_id}\r\n'
            f'CSeq: {self.invite_cseq} CANCEL\r\n'
            'Max-Forwards: 70\r\n'
            'Content-Length: 0\r\n\r\n'
        )

        logger.debug('############ Sending CANCEL ############')
        logger.debug(cancel_request)
        logger.debug('############ end of CANCEL ############')
        self.safe_sendto(cancel_request.encode(), (self.domain, self.port))

    def send_ok_for_cancel(self):
        """ (receiver)
        Send 200 OK for CANCEL request from caller.
        """
        via_header = self.recv_msg.split('Via: ')[1].split('\r\n')[0]
        from_header = self.recv_msg.split('From: ')[1].split('\r\n')[0]
        to_header = self.recv_msg.split('To: ')[1].split('\r\n')[0]
        call_id = self.recv_msg.split('Call-ID: ')[1].split('\r\n')[0]
        cseq_header = self.recv_msg.split('CSeq: ')[1].split('\r\n')[0]

        ok_resp = (
            f'SIP/2.0 200 OK\r\n'
            f'Via: {via_header}\r\n'
            f'From: {from_header}\r\n'
            f'To: {to_header}\r\n'
            f'Call-ID: {call_id}\r\n'
            f'CSeq: {cseq_header}\r\n'
            'Content-Length: 0\r\n\r\n'
        )

        logger.debug('############ Sending 200 OK to CANCEL ############')
        logger.debug(ok_resp)
        logger.debug('############ end of 200 OK ############')
        self.safe_sendto(ok_resp.encode(), (self.domain, self.port))

    def send_ack_for_487(self):
        """ (sender)
        Send ACK for 487 Request Terminated.
        This is used when the call is cancelled by the caller after making call, 
        and finally terminated by the callee.
        """
        via_header = self.recv_msg.split('Via: ')[1].split('\r\n')[0]
        from_header = self.recv_msg.split('From: ')[1].split('\r\n')[0]
        to_header = self.recv_msg.split('To: ')[1].split('\r\n')[0]
        call_id = self.recv_msg.split('Call-ID: ')[1].split('\r\n')[0]

        ack_resp = (
            f'ACK sip:{self.opp_username}@{self.domain}:{self.port} SIP/2.0\r\n'
            f'Via: {via_header}\r\n'
            f'From: {from_header}\r\n'
            f'To: {to_header}\r\n'
            f'Call-ID: {call_id}\r\n'
            f'CSeq: {self.invite_cseq} ACK\r\n'
            'Max-Forwards: 70\r\n'
            'Content-Length: 0\r\n\r\n'
        )

        logger.debug('############ Sending ACK for 487 Request Terminated ############')
        logger.debug(ack_resp)
        logger.debug('############ end of ACK ############')
        self.safe_sendto(ack_resp.encode(), (self.domain, self.port))

    def send_487_for_invite(self):
        """ (receiver)
        Send 487 Request Terminated for INVITE request.
        This is used when the call is cancelled by the caller after receiving call,
        and need to send 487 Request Terminated to the caller.
        """
        via_header = self.invite_msg.split('Via: ')[1].split('\r\n')[0]
        from_header = self.invite_msg.split('From: ')[1].split('\r\n')[0]
        to_header = self.invite_msg.split('To: ')[1].split('\r\n')[0]
        call_id = self.invite_msg.split('Call-ID: ')[1].split('\r\n')[0]
        cseq_header = self.invite_msg.split('CSeq: ')[1].split('\r\n')[0]

        resp_487 = (
            f'SIP/2.0 487 Request Terminated\r\n'
            f'Via: {via_header}\r\n'
            f'From: {from_header}\r\n'
            f'To: {to_header}\r\n'
            f'Call-ID: {call_id}\r\n'
            f'CSeq: {cseq_header}\r\n'
            'Content-Length: 0\r\n\r\n'
        )

        logger.debug('############ Sending 487 Request Terminated ############')
        logger.debug(resp_487)
        logger.debug('############ end of 487 ############')
        self.safe_sendto(resp_487.encode(), (self.domain, self.port))

    #######################################
    # Reject call operations
    #######################################
    def send_ack_for_486(self):
        """ (sender)
        Send ACK for 486 Busy Here.
        This is used when the call is rejected by the callee in EARLY state.
        """
        via_header = self.recv_msg.split('Via: ')[1].split('\r\n')[0]
        from_header = self.recv_msg.split('From: ')[1].split('\r\n')[0]
        to_header = self.recv_msg.split('To: ')[1].split('\r\n')[0]
        call_id = self.recv_msg.split('Call-ID: ')[1].split('\r\n')[0]

        ack_resp = (
            f'ACK sip:{self.opp_username}@{self.domain}:{self.port} SIP/2.0\r\n'
            f'Via: {via_header}\r\n'
            f'From: {from_header}\r\n'
            f'To: {to_header}\r\n'
            f'Call-ID: {call_id}\r\n'
            f'CSeq: {self.invite_cseq} ACK\r\n'
            'Max-Forwards: 70\r\n'
            'Content-Length: 0\r\n\r\n'
        )

        logger.debug('############ Sending ACK for 486 Busy Here ############')
        logger.debug(ack_resp)
        logger.debug('############ end of ACK ############')
        self.safe_sendto(ack_resp.encode(), (self.domain, self.port))

    def send_486(self):
        """ (receiver)
        Send 486 Busy Here for INVITE request.
        This is used when the user wants to reject the call.
        """
        via_header = self.invite_msg.split('Via: ')[1].split('\r\n')[0]
        from_header = self.invite_msg.split('From: ')[1].split('\r\n')[0]
        to_header = self.invite_msg.split('To: ')[1].split('\r\n')[0]

        resp_486 = (
            f'SIP/2.0 486 Busy Here\r\n'
            f'Via: {via_header}\r\n'
            f'From: {from_header}\r\n'
            f'To: {to_header}\r\n'
            f'Call-ID: {self.call_id}\r\n'
            f'CSeq: {self.invite_cseq} INVITE\r\n'
            'Content-Length: 0\r\n\r\n'
        )

        logger.debug('############ Sending 486 Busy Here ############')
        logger.debug(resp_486)
        logger.debug('############ end of 486 ############')
        self.safe_sendto(resp_486.encode(), (self.domain, self.port))

    #######################################
    # Others
    #######################################
    def send_bye(self):
        """
        Send BYE request to terminate the call.
        Active sending only works in CONFIRMED state.
        """
        bye_branch = 'z9hG4bKPj' + create_unique_tag()
        bye_cseq = self.cseq_num
        self.cseq_num += 1

        bye_request = (
            f'BYE sip:{self.opp_username}@{self.domain}:{self.port} SIP/2.0\r\n'
            f'Via: SIP/2.0/UDP {self.local_ip}:{self.local_port};rport;branch={bye_branch}\r\n'
            f'From: <sip:{self.username}@{self.local_ip}>;tag={self.my_tag}\r\n'
            f'To: "{self.opp_username}" <sip:{self.opp_username}@{self.domain}>;tag={self.opp_tag}\r\n'
            f'Call-ID: {self.call_id}\r\n'
            f'CSeq: {bye_cseq} BYE\r\n'
            'Max-Forwards: 70\r\n'
            'Content-Length: 0\r\n\r\n'
        )

        logger.debug('############ Sending BYE ############')
        logger.debug(bye_request)
        logger.debug('############ end of BYE ############')
        self.safe_sendto(bye_request.encode(), (self.domain, self.port))

    def parse_sdp(self):
        self.opp_rtp_ip = None
        self.opp_rtp_port = None

        sdp = self.recv_msg.split('Content-Length: ')[1].split('\r\n\r\n')[1].strip()
        
        # find ip address (c=IN IP4 x.x.x.x)
        c_line = re.search(r"c=IN IP4 (\d+\.\d+\.\d+\.\d+)", sdp)
        if c_line:
            self.opp_rtp_ip = c_line.group(1)

        # find audio port (m=audio x RTP/AVP ...)
        m_line = re.search(r"m=audio (\d+) RTP/AVP", sdp)
        if m_line:
            self.opp_rtp_port = int(m_line.group(1))

    def end_call(self):
        logger.info('Call ended')
        self.running = False
        time.sleep(0.5)
        self.unbind_rtp_socket()
        self.fsm.state = CallState.CLEARED

    def _update_invite_msg_with_to_tag(self, new_to_tag):
        lines = self.invite_msg.split("\r\n")

        for i in range(len(lines)):
            if lines[i].startswith("To:"):
                base_to = lines[i].split(";")[0]
                lines[i] = f"{base_to};tag={new_to_tag}"
                break

        self.invite_msg = "\r\n".join(lines)

    #######################################
    # User operations
    #######################################
    def make_call(self):
        self.fsm.handle_event(CallEvent.MAKE_CALL)

    def answer_call(self):
        self.fsm.handle_event(CallEvent.ANSWER_CALL)

    def reject_call(self):
        self.fsm.handle_event(CallEvent.REJECT_CALL)

    def hangup_call(self):
        self.fsm.handle_event(CallEvent.HANGUP_CALL)

    def getFrames(self):
        if len(self.audio_recv_buffer) > 0:
            return self.audio_recv_buffer.popleft()  # deque usage
        return b''
    
    def putFrame(self, frame):
        """
        Put received audio frames into buffer
        Args:
            frame (bytes): audio frame
        """
        self.audio_send_buffer.append(frame)