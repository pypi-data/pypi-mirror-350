import logging
from enum import Enum, auto

logger = logging.getLogger('sip')


# 定義通話狀態
class CallState(Enum):
    INITIAL = auto()
    CALLING = auto()
    AUTHENTICATING = auto()
    INCOMING = auto()
    EARLY = auto()
    CONNECTING = auto()
    CONFIRMED = auto()
    DISCONNECTED = auto()
    CANCELLED = auto()
    WAIT_REINVIET = auto()
    REFER = auto()
    ACCEPTED = auto()
    WAIT_REFER = auto()
    REFER_COMPLETED = auto()
    CLEARED = auto()


# 定義呼叫事件
class CallEvent(Enum):
    MAKE_CALL = auto()
    ANSWER_CALL = auto()
    HANGUP_CALL = auto()
    REJECT_CALL = auto()
    # INVITE_SENT = auto()
    INVITE_RECEIVED = auto()
    AUTH_REQUIRED = auto()
    # TRYING_SENT = auto()
    TRYING_RECEIVED = auto()
    RINGING_SENT = auto()
    RINGING_RECEIVED = auto()
    PRACK_SENT = auto()
    PRACK_RECEIVED = auto()
    # OK_SENT = auto()
    OK_RECEIVED = auto()
    ACK_SENT = auto()
    ACK_RECEIVED = auto()
    # BYE_SENT = auto()
    BYE_RECEIVED = auto()
    REINVITE_SENT = auto()
    REFER_SENT = auto()
    ACCEPTED_RECEIVED = auto()
    NOTIFY_RECEIVED = auto()
    CANCEL_RECEIVED = auto()
    _480_RECEIVED = auto()
    _486_RECEIVED = auto()
    _487_RECEIVED = auto()


class CallRole(Enum):
    UNDEFINED = auto()
    SENDER = auto()
    RECEIVER = auto()


# 定義FSM類來管理呼叫狀態
class CallFSM:
    def __init__(self, call):
        self.call = call
        self.role = CallRole.UNDEFINED
        self.state = CallState.INITIAL
        self.flags = {}

    def handle_event(self, event):
        logger.info(f'Handling event {event} in state {self.state}')

        if self.state == CallState.INITIAL:
            if event == CallEvent.MAKE_CALL:  # sender
                self.role = CallRole.SENDER
                self.call.bind_rtp_rtcp_sockets()
                self.call.send_invite()
                self.transition(CallState.CALLING)
            elif event == CallEvent.INVITE_RECEIVED:  # receiver
                self.role = CallRole.RECEIVER
                self.call.invite_msg = self.call.recv_msg
                self.call.parse_sdp()
                self.transition(CallState.INCOMING)

        elif self.state == CallState.CALLING:  # sender
            if event == CallEvent.TRYING_RECEIVED:
                pass
            elif event == CallEvent.RINGING_RECEIVED:
                self.call.handle_180_ringing()
                self.transition(CallState.EARLY)
            elif event == CallEvent.AUTH_REQUIRED:  # NEC PBX no need auth
                self.call.send_ack_for_auth()
                self.transition(CallState.AUTHENTICATING)
            elif event == CallEvent.HANGUP_CALL:
                self.call.send_cancel()
                self.transition(CallState.CANCELLED)     

        elif self.state == CallState.AUTHENTICATING:
            pass
        
        elif self.state == CallState.INCOMING:  # receiver
            if event == CallEvent.RINGING_SENT:
                self.transition(CallState.EARLY)

        elif self.state == CallState.EARLY:
            if event == CallEvent.RINGING_RECEIVED:  # sender
                self.call.handle_180_ringing()  ### could be 183
                self.transition(CallState.EARLY)
            if event == CallEvent.OK_RECEIVED:  # sender
                self.call.parse_sdp()
                self.transition(CallState.CONNECTING)
            elif event == CallEvent.ANSWER_CALL:  # receiver
                if self.role == CallRole.RECEIVER:
                    self.call.bind_rtp_rtcp_sockets()
                    self.call.send_ok_for_invite()
                    self.transition(CallState.CONNECTING)
            elif event == CallEvent.HANGUP_CALL:  # sender
                if self.role == CallRole.SENDER:
                    self.call.send_cancel()
                    self.transition(CallState.CANCELLED)
            if event == CallEvent.CANCEL_RECEIVED:  # receiver
                self.call.send_ok_for_cancel()
                self.call.send_487_for_invite()
                self.transition(CallState.DISCONNECTED)
            elif event == CallEvent._486_RECEIVED:  # sender be rejected
                self.call.send_ack_for_486()
                self.transition(CallState.DISCONNECTED)
            elif event == CallEvent.REJECT_CALL:  # receiver to reject
                if self.role == CallRole.RECEIVER:
                    self.call.send_486()
                    self.transition(CallState.DISCONNECTED)

        elif self.state == CallState.CONNECTING:
            if event == CallEvent.ACK_SENT:  # sender
                self.transition(CallState.CONFIRMED)
            elif event == CallEvent.ACK_RECEIVED:  # receiver
                self.transition(CallState.CONFIRMED)

        elif self.state == CallState.CONFIRMED:
            if event == CallEvent.HANGUP_CALL:
                self.call.send_bye()
                self.transition(CallState.DISCONNECTED)
            elif event == CallEvent.BYE_RECEIVED:
                self.call.send_ok_for_bye()
                self.transition(CallState.DISCONNECTED)
            elif event == CallEvent.REINVITE_SENT:  # transfer call
                self.transition(CallState.WAIT_REINVIET)
            elif event == CallEvent.INVITE_RECEIVED:  # prevent timeout for server
                self.call.send_ok_for_invite_check()

        elif self.state == CallState.CANCELLED:  # sender
            if event == CallEvent.OK_RECEIVED:
                self.flags['cancel_ok_received'] = True
            elif event == CallEvent._487_RECEIVED:
                self.flags['cancel_487_received'] = True
                self.call.send_ack_for_487()

            if self.flags.get('cancel_ok_received') and self.flags.get('cancel_487_received'):
                self.transition(CallState.DISCONNECTED)

        elif self.state == CallState.WAIT_REINVIET:
            if event == CallEvent.OK_RECEIVED:  # transfer call
                self.call.send_ack_for_ok()
                self.transition(CallState.REFER)
            elif event == CallEvent.BYE_RECEIVED:  # transfer call
                self.call.send_ok_for_bye()
                self.transition(CallState.DISCONNECTED)

        elif self.state == CallState.REFER:
            if event == CallEvent.REFER_SENT:  # transfer call
                self.transition(CallState.WAIT_REFER)
            elif event == CallEvent.BYE_RECEIVED:  # transfer call
                self.call.send_ok_for_bye()
                self.transition(CallState.DISCONNECTED)

        elif self.state == CallState.WAIT_REFER:
            if event == CallEvent.ACCEPTED_RECEIVED:  # transfer call
                self.transition(CallState.ACCEPTED)
            elif event == CallEvent.BYE_RECEIVED:  # transfer call
                self.call.send_ok_for_bye()
                self.transition(CallState.DISCONNECTED)
            elif event == CallEvent._480_RECEIVED:
                self.call.send_bye()
                self.transition(CallState.DISCONNECTED)

        elif self.state == CallState.ACCEPTED:
            if event == CallEvent.NOTIFY_RECEIVED:  # transfer call
                self.transition(CallState.REFER_COMPLETED)
                self.call.send_ok_for_notify()
            elif event == CallEvent.BYE_RECEIVED:  # transfer call
                self.call.send_ok_for_bye()
                self.transition(CallState.DISCONNECTED)

        elif self.state == CallState.REFER_COMPLETED:
            if event == CallEvent.BYE_RECEIVED:  # transfer call
                self.call.send_ok_for_bye()
                self.transition(CallState.DISCONNECTED)

        elif self.state == CallState.DISCONNECTED:
            pass

    def transition(self, new_state):
        logger.info(f'Transitioning from {self.state} to {new_state}')
        self.exit_action(self.state)
        self.transition_action(self.state, new_state)
        # need to update state before entry_action to prevent infinite loop
        self.state = new_state
        self.call.sc.state = new_state  # update state in sip client instance
        self.entry_action(new_state)

    def exit_action(self, state):
        if state == CallState.CONFIRMED:
            # release audio resources
            pass

    def transition_action(self, old_state, new_state):
        pass

    def entry_action(self, state):
        if state == CallState.AUTHENTICATING:
            self.call.send_invite(retry_auth=True)
            self.transition(CallState.CALLING)
        elif state == CallState.INCOMING:
            self.call.send_trying()
            self.call.send_ringing()
            self.handle_event(CallEvent.RINGING_SENT)
        elif state == CallState.CONNECTING:
            if self.role == CallRole.SENDER:
                self.call.send_ack_for_ok()
        elif state == CallState.CONFIRMED:
            self.call.start_audio()
        elif state == CallState.DISCONNECTED:
            self.call.end_call()
        elif state == CallState.REFER:
            self.call.send_refer(self.call.transfer_username)