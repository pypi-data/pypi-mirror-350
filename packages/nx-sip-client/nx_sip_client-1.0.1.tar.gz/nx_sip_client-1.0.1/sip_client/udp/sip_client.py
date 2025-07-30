import time
import socket
import hashlib
import logging
import threading

from .call import Call
from .call_fsm import CallState, CallEvent
from .utils import create_unique_tag

logger = logging.getLogger('sip')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
formatter.datefmt = '%Y-%m-%d %H:%M:%S'
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)


class SipClient():
    """
    Attributes:
        domain (str): SIP server domain
        port (int): SIP server port
        username (str): SIP username
        password (str): SIP password
        realm (str): SIP server realm, default to domain
        transport_ip (str): IP address to bind the SIP socket
        transport_port (int): Port to bind the SIP socket
        rtp_port (int): Port to bind the RTP socket
        rtcp_port (int): Port to bind the RTCP socket
        sip_socket (socket): SIP socket
        register_call_id (str): Call-ID for REGISTER, need to keep the same for re-register
        register_cseq (int): Cseq number for REGISTER, need to increase for re-register
        register_expires (int): Expiration time for REGISTER, need to re-register before expiration
        current_call (Call): Current active call, None if no call
        state (CallState): Current state of the SIP client, reference to the current call state
    """

    def __init__(
        self,
        domain,
        port,
        username,
        password,
        transport_ip,
        transport_port,
        rtp_port=None,
        rtcp_port=None
    ):
        """
        Args:
            domain (str): SIP server domain
            port (int): SIP server port
            username (str): SIP username
            password (str): SIP password
            transport_ip (str): IP address to bind the SIP socket
            transport_port (int): Port to bind the SIP socket
            rtp_port (int): Port to bind the RTP socket, None will use random port
            rtcp_port (int): Port to bind the RTCP socket, None will use random port
        """
        self.domain = domain
        self.port = port
        self.username = username
        self.password = password
        self.realm = domain
        self.transport_ip = transport_ip
        self.transport_port = transport_port
        self.rtp_port = rtp_port
        self.rtcp_port = rtcp_port

        self.sip_socket = self._create_sip_socket(transport_ip, transport_port)
        self.register_call_id = create_unique_tag()
        self.register_cseq = 1
        self.register_expires = 300
        self.current_call = None
        self.state = CallState.INITIAL
        self.regIsActive = False

        threading.Thread(target=self.listen_sip_packet, daemon=True).start()
        threading.Thread(target=self.check_state, daemon=True).start()
        threading.Thread(target=self.periodic_register, daemon=True).start()
    
    def _create_sip_socket(self, ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((ip, port))
        s.settimeout(2)
        return s
    
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
    
    ########################################
    # Main threadings
    ########################################
    def listen_sip_packet(self):
        """Listen to incoming SIP packets"""
        while True:
            try:
                data, addr = self.sip_socket.recvfrom(4096)
                if data:
                    self.handle_sip_packet(data, addr)
            except socket.timeout:
                # logger.debug(f'socket timeout')
                pass

    def check_state(self):
        """Check current call state, clear the call when it is cleared"""
        while True:
            if self.current_call:
                if self.current_call.fsm.state == CallState.CLEARED:
                    self.current_call = None
                    self.state = CallState.INITIAL
            time.sleep(0.1)

    def periodic_register(self):
        """Periodically send REGISTER to keep the registration alive"""
        while True:
            if self.current_call is None:
                self._send_register()
            time.sleep(self.register_expires / 3)

    ########################################
    # SIP packet handling
    ########################################
    def handle_sip_packet(self, data, addr):
        """Handle incoming SIP packet"""
        message = data.decode(errors='replace')
        start_line = message.split("\r\n")[0]
        logger.debug(f'Received:\n{message}')

        pkg_call_id = message.split('Call-ID: ')[1].split('\r\n')[0]

        if self.current_call:
            # check if the incoming message belongs to the current call
            if pkg_call_id != self.current_call.call_id:
                self._send_481(message, addr)
                return
            
            # update the current call with the incoming message
            self.current_call.recv_msg = message
            self.current_call.sender_addr = addr
            
            if 'INVITE' in start_line:
                self.current_call.fsm.handle_event(CallEvent.INVITE_RECEIVED)

            elif 'Trying' in start_line:
                self.current_call.fsm.handle_event(CallEvent.TRYING_RECEIVED)

            elif '180 Ringing' in start_line:
                self.current_call.fsm.handle_event(CallEvent.RINGING_RECEIVED)

            elif '183 Session Progress' in start_line:
                self.current_call.fsm.handle_event(CallEvent.RINGING_RECEIVED)

            elif '200 OK' in start_line:
                if 'PRACK' in message.split('CSeq: ')[1].split('\r\n')[0]:
                    pass
                else:
                    self.current_call.fsm.handle_event(CallEvent.OK_RECEIVED)

            elif 'BYE' in start_line:
                self.current_call.fsm.handle_event(CallEvent.BYE_RECEIVED)

            elif 'ACK' in start_line:
                self.current_call.fsm.handle_event(CallEvent.ACK_RECEIVED)

            elif 'Accepted' in start_line:  # 202 Accepted for transfer call
                self.current_call.fsm.handle_event(CallEvent.ACCEPTED_RECEIVED)

            elif 'NOTIFY' in start_line:
                self.current_call.fsm.handle_event(CallEvent.NOTIFY_RECEIVED)

            elif '407 Proxy Authentication Required' in start_line:  # make call in Panasonic PBX
                self.current_call.fsm.handle_event(CallEvent.AUTH_REQUIRED)

            elif 'CANCEL' in start_line:
                # self._handle_cancel(message, addr)
                self.current_call.fsm.handle_event(CallEvent.CANCEL_RECEIVED)
            
            elif '480 Temporarily Unavailable' in start_line:
                self.current_call.fsm.handle_event(CallEvent._480_RECEIVED)

            elif '486 Busy Here' in start_line:
                self.current_call.fsm.handle_event(CallEvent._486_RECEIVED)

            elif '487 Request Terminated' in start_line:
                self.current_call.fsm.handle_event(CallEvent._487_RECEIVED)
                
        else:  # current call is None
            if 'INVITE' in start_line:
                # create a new call
                self.current_call = Call(
                    sc=self,
                    sip_socket=self.sip_socket,
                    domain=self.domain, 
                    port=self.port, 
                    username=self.username,
                    password=self.password,
                    rtp_port=self.rtp_port,
                    rtcp_port=self.rtcp_port
                )
                self.current_call.recv_msg = message
                self.current_call.sender_addr = addr
                self.current_call.fsm.handle_event(CallEvent.INVITE_RECEIVED)

            elif '200 OK' in start_line:
                # get the CSeq method to determine the response
                cseq_method = message.split('CSeq: ')[1].split(' ')[1].split('\r\n')[0]
                if cseq_method == 'REGISTER':
                    self.regIsActive = True
                    logger.info('Registration successful')
                elif cseq_method == 'INVITE':  # 200 OK for the previous call
                    self._send_ack_for_ok(message, addr)

            elif '401 Unauthorized' in start_line:
                # means the server requires authentication
                cseq_method = message.split('CSeq: ')[1].split(' ')[1].split('\r\n')[0]
                if cseq_method == 'REGISTER':
                    nonce = message.split('nonce="')[1].split('"')[0]
                    self._send_register(nonce=nonce, challenge_msg=message)
                elif cseq_method == 'INVITE':
                    self.current_call.fsm.handle_event(CallEvent.AUTH_REQUIRED)

            elif '423 Interval Too Brief' in start_line:
                # means the server requires a longer registration interval
                cseq_method = message.split('CSeq: ')[1].split(' ')[1].split('\r\n')[0]
                if cseq_method == 'REGISTER':
                    min_expires = int(message.split('Min-Expires: ')[1].split('\r\n')[0])
                    self._send_register(min_expires=min_expires)

            elif 'ACK' in start_line:
                pass

            else:  # other messages
                self._send_481(message, addr)

    def _send_register(self, min_expires=None, nonce=None, challenge_msg=None):
        """Send REGISTER packet to the SIP server"""
        def generate_md5_response(username, realm, password, nonce, uri):
            """Generate MD5 response for REGISTER"""
            ha1 = hashlib.md5(f'{username}:{realm}:{password}'.encode()).hexdigest()
            ha2 = hashlib.md5(f'REGISTER:{uri}'.encode()).hexdigest()
            return hashlib.md5(f'{ha1}:{nonce}:{ha2}'.encode()).hexdigest()
        
        branch = 'z9hG4bKPj' + create_unique_tag()  # need to create a new branch for each REGISTER
        call_id = self.register_call_id
        cseq = self.register_cseq
        self.register_cseq += 1
        self.register_expires = min_expires or self.register_expires

        register = f'REGISTER sip:{self.domain} SIP/2.0\r\n'
        register += f'Via: SIP/2.0/UDP {self.transport_ip}:{self.transport_port};rport;branch={branch}\r\n'
        register += 'Max-Forwards: 70\r\n'
        register += f'From: <sip:{self.username}@{self.domain}>;tag={create_unique_tag()}\r\n'
        register += f'To: <sip:{self.username}@{self.domain}>\r\n'
        register += f'Call-ID: {call_id}\r\n'
        register += f'CSeq: {cseq} REGISTER\r\n'
        register += f'Contact: <sip:{self.username}@{self.transport_ip}:{self.transport_port};ob>\r\n'
        register += f'Expires: {self.register_expires}\r\n'
        register += 'Allow: PRACK, INVITE, ACK, BYE, CANCEL, UPDATE, INFO, SUBSCRIBE, NOTIFY, REFER, MESSAGE, OPTIONS\r\n'
        register += 'Supported: replaces, 100rel, timer, norefersub\r\n'
        
        # add Authorization header if nonce is provided
        if nonce:
            hdr = ('Proxy-Authorization'
                    if 'Proxy Authentication Required' in challenge_msg
                    else 'Authorization')
            response = generate_md5_response(self.username, self.realm, self.password, nonce, f'sip:{self.domain}')
            register += (
                f'{hdr}: Digest username="{self.username}", '
                f'realm="{self.realm}", nonce="{nonce}", '
                f'uri="sip:{self.domain}", response="{response}", algorithm=MD5\r\n'
            )
        
        register += 'Content-Length: 0\r\n\r\n'
        logger.debug(f'Sending REGISTER:\n{register}')
        self.safe_sendto(register.encode(), (self.domain, self.port))
        self.regIsActive = False

    def _send_ack_for_ok(self, recv_msg, addr):
        """Send ACK packet for 200 OK"""
        contact_uri = recv_msg.split('Contact: <')[1].split('>\r\n')[0]
        ack_branch = 'z9hG4bKPj' + create_unique_tag()  # need to create a new branch for each ACK
        from_header = recv_msg.split('From: ')[1].split('\r\n')[0]
        to_header = recv_msg.split('To: ')[1].split('\r\n')[0]
        call_id = recv_msg.split('Call-ID: ')[1].split('\r\n')[0]
        cseq = recv_msg.split('CSeq: ')[1].split(' INVITE')[0]

        ack = (
            f'ACK {contact_uri} SIP/2.0\r\n'
            f'Via: SIP/2.0/UDP {self.transport_ip}:{self.transport_port};rport;branch={ack_branch}\r\n'
            'Max-Forwards: 70\r\n'
            f'From: {from_header}\r\n'
            f'To: {to_header}\r\n'
            f'Call-ID: {call_id}\r\n'
            f'CSeq: {cseq} ACK\r\n'
            'Content-Length: 0\r\n\r\n'
        )

        logger.debug('############ Sending 200 OK ACK ############')
        logger.debug(ack)
        logger.debug('############ end of 200 OK ACK ############')
        self.safe_sendto(ack.encode(), addr)
    
    def _send_481(self, recv_msg, addr):
        """Send 481 to tell the client that the call leg/transaction does not exist"""
        via_header = recv_msg.split('Via: ')[1].split('\r\n')[0]
        from_header = recv_msg.split('From: ')[1].split('\r\n')[0]
        to_header = recv_msg.split('To: ')[1].split('\r\n')[0]
        call_id = recv_msg.split('Call-ID: ')[1].split('\r\n')[0]
        cseq_header = recv_msg.split('CSeq: ')[1].split('\r\n')[0]

        not_exist_resp = (
            f'SIP/2.0 481 Call Leg/Transaction Does Not Exist\r\n'
            f'Via: {via_header}\r\n'
            f'From: {from_header}\r\n'
            f'To: {to_header}\r\n'
            f'Call-ID: {call_id}\r\n'
            f'CSeq: {cseq_header}\r\n'
            'Content-Length: 0\r\n\r\n'
        )

        logger.debug('############ Sending 481 Call Leg/Transaction Does Not Exist ############')
        logger.debug(not_exist_resp)
        logger.debug('############ end of 481 ############')
        self.safe_sendto(not_exist_resp.encode(), addr)

    ########################################
    # User operations
    ########################################
    def make_call(self, opp_username):
        if self.current_call:
            logger.warning("Call already in progress")
        else:
            self.current_call = Call(
                sc=self,
                sip_socket=self.sip_socket,
                domain=self.domain,
                port=self.port,
                username=self.username,
                password=self.password,
                opp_username=opp_username,
                rtp_port=self.rtp_port,
                rtcp_port=self.rtcp_port
            )
            self.current_call.make_call()

    def answer_call(self):
        if self.current_call:
            self.current_call.answer_call()
        else:
            logger.warning("No incoming call to answer")

    def reject_call(self):
        if self.current_call:
            self.current_call.reject_call()
        else:
            logger.warning("No incoming call to reject")

    def hangup_call(self):
        if self.current_call:
            self.current_call.hangup_call()
        else:
            logger.warning("No active call to hang up")

    def transfer_call(self, target_username):
        if self.current_call:
            self.current_call.transfer_username = target_username
            self.current_call.send_reinvite()
        else:
            logger.warning("No active call to transfer")