import re
import logging
import pjsua2 as pj

logger = logging.getLogger("pjsip")

# ---------------- enum fallback ---------------------
try:
    ROLE_UAC = pj.pjsip_role_e.PJSIP_ROLE_UAC  # 標準寫法
except AttributeError:  # 舊版無列舉
    ROLE_UAC = 0  # According to PJSIP: 0 = UAC, 1 = UAS

# ---------------- helpers ---------------------------
USER_RE = re.compile(r"sip:([^@;>]+)")  # 擷取 sip:user@domain 中的 user

def parse_user(uri):
    m = USER_RE.search(uri)
    return m.group(1) if m else None


class AccountConfig:
    def __init__(self, domain, port, username, password, transport_ip, transport_port=5060):
        self._domain = domain
        self._port = port
        self._username = username
        self._password = password
        self._transport_ip = transport_ip
        self._transport_port = transport_port

    def getIdUri(self):
        return f"sip:{self._username}@{self._domain}"

    def getRegistrarUri(self):
        return f"sip:{self._domain}:{self._port}"

    def getDestinationUri(self, dest_username, domain=None):
        if domain is None:
            domain = self._domain
        return f"sip:{dest_username}@{domain}:{self._port}"

    def getTransportIp(self):
        return self._transport_ip

    def getTransportPort(self):
        return self._transport_port

    def getInfo(self):
        return {
            "domain": self._domain,
            "port": self._port,
            "username": self._username,
            "password": self._password,
            "transport_ip": self._transport_ip,
            "transport_port": self._transport_port,
        }


class Call(pj.Call):
    """擴充原 Call：加入 *hold‑then‑REFER* 轉接機制。其餘功能保持原狀。"""

    def __init__(self, acc, call_id=pj.PJSUA_INVALID_ID):
        super().__init__(acc, call_id)
        self.acc = acc
        self.call_id = call_id
        self.remote_uri = None
        self.remote_user = None

        # audio buffers
        self.pcm_capture = None
        self.pcm_stream = None

        self._hold_sent = False  # 是否已送出 hold re‑INVITE
        self._pending_xfer_uri = None  # hold 完成後要 REFER 的目標

    # -------------------- callbacks --------------------
    def onCallState(self, prm):  # noqa: N802
        ci = self.getInfo()
        self.remote_uri = ci.remoteUri
        self.remote_user = parse_user(ci.remoteUri)
        logger.debug("[SIP] state=%s (%s) code=%s", ci.state, ci.stateText, ci.lastStatusCode)

        # -------------------------------------------------------------
        # 1. 立即處理「提早以 183 Busy 音拒接」的 PBX
        # -------------------------------------------------------------
        # NEC SL2100 會在使用者按下拒接鍵時先送 183 Session Progress
        # 並播放 Busy Tone （需 100rel/PRACK），最後才送 486 Busy Here。
        # 我們偵測到 183 後先送 CANCEL，加速釋放通話。
        if (
            getattr(ci, "role", ROLE_UAC) == ROLE_UAC
            and ci.state == pj.PJSIP_INV_STATE_EARLY
            and ci.lastStatusCode == 183
        ):
            logger.info("[SIP] Got 183 Session Progress — treat as busy, sending CANCEL …")
            try:
                self.hangup(pj.CallOpParam())  # CANCEL
            except pj.Error:
                pass
            self.acc.sc.clear()
            return  # 直接結束 callback

        # 2. 撥出被拒 / 4xx‑6xx 最終回應
        if (
            getattr(ci, "role", ROLE_UAC) == ROLE_UAC
            and ci.lastStatusCode >= 300
            and ci.state not in (
                pj.PJSIP_INV_STATE_CONFIRMED,
                pj.PJSIP_INV_STATE_DISCONNECTED,
            )
        ):
            logger.info("[SIP] Remote rejected/failed (%s) – auto clear", ci.lastStatusCode)
            try:
                self.hangup(pj.CallOpParam())
            except pj.Error:
                pass
            self.acc.sc.clear()

        # 3. 正常斷線
        elif ci.state == pj.PJSIP_INV_STATE_DISCONNECTED:
            logger.debug("[SIP] Call disconnected")
            self.acc.sc.clear()

    def onCallMediaState(self, prm):
        ci = self.getInfo()
        aud_med = self.getAudioMedia(-1)
        if not self.pcm_capture and aud_med:
            self.pcm_capture = pj.AudioMediaCapture()
            self.pcm_capture.createMediaCapture(ci.id)
            aud_med.startTransmit(self.pcm_capture)
        if not self.pcm_stream and aud_med:
            self.pcm_stream = pj.AudioMediaStream()
            self.pcm_stream.createMediaStream(ci.id)
            self.pcm_stream.startTransmit(aud_med)

        # 若剛剛送過 hold，這 callback 表示 re‑INVITE 已結束
        if self._hold_sent and self._pending_xfer_uri:
            logger.debug("[SIP] Hold confirmed, sending REFER to %s", self._pending_xfer_uri)
            call_prm = pj.CallOpParam(True)
            self.xfer(self._pending_xfer_uri, call_prm)
            # 重置旗標避免重複
            self._hold_sent = False
            self._pending_xfer_uri = None

    def onCallTransferStatus(self, prm):
        logger.debug("Call transfer status: %s", prm.statusCode)
        if prm.statusCode // 100 == 2 and prm.finalNotify:
            logger.debug("Call transfer successful — hanging up local leg")
            self.hangup(pj.CallOpParam())
            self.acc.sc.clear()
        elif prm.finalNotify:
            logger.debug("Call transfer failed with status: %s", prm.statusCode)

    # -------------------- helpers --------------------
    def getFrames(self):
        return self.pcm_capture.getFrames() if self.pcm_capture else b""

    def putFrame(self, chunk):
        if self.pcm_stream:
            self.pcm_stream.putFrame(chunk)
        else:
            logger.warning("[SIP] Failed to putFrame to call")

    def transfer(self, dest):
        """Hold the call and then transfer it using REFER."""
        if self._hold_sent:
            logger.warning("[SIP] Transfer already in progress")
            return

        self._hold_sent = True
        self._pending_xfer_uri = dest
        logger.info("[SIP] Initiating transfer to %s (re‑INVITE hold → REFER)", dest)
        self.hold()  # 送 re‑INVITE (a=sendonly)

    def hold(self):
        """Put the call on hold by sending a re‑INVITE with sendonly."""
        logger.debug("[SIP] Sending setHold() to put call on hold")
        call_prm = pj.CallOpParam(True)
        self.setHold(call_prm)


class Account(pj.Account):
    def __init__(self, sip_client):
        super().__init__()
        self.sc = sip_client

    def onIncomingCall(self, prm):
        logger.debug("[SIP] Inside Incoming Call Handler")
        call = Call(self, call_id=prm.callId)
        logger.debug("[SIP] call id: %s", prm.callId)
        ci = call.getInfo()
        logger.info("[SIP] Incoming call from %s", ci.remoteUri)
        self.sc.current_call = call
        self.sc.current_call_id = prm.callId

        # return 180 Ringing
        call_prm = pj.CallOpParam()
        call_prm.statusCode = pj.PJSIP_SC_RINGING  # 180
        call.answer(call_prm)


class SipClient:
    ENDPOINT = None

    def __init__(
        self,
        domain,
        port,
        username,
        password,
        transport_ip,
        transport_port,
        sip_log_level=0,
    ):
        self.acc_config = AccountConfig(
            domain, port, username, password, transport_ip, transport_port
        )
        self.account = None
        self.current_call = None
        self.current_call_id = None

        if not SipClient.ENDPOINT:
            SipClient.ENDPOINT = self.init_endpoint(sip_log_level)

    @classmethod
    def init_endpoint(cls, sip_log_level):
        ep_cfg = pj.EpConfig()
        ep_cfg.logConfig.level = sip_log_level
        ep = pj.Endpoint()
        ep.libCreate()
        ep.libInit(ep_cfg)
        ep.audDevManager().setNullDev()
        for codec in ep.codecEnum2():
            priority = 255 if "PCMA/8000" in codec.codecId else 0
            ep.codecSetPriority(codec.codecId, priority)
        ep.libStart()
        return ep

    def init(self):
        sipTpConfig = pj.TransportConfig()
        sipTpConfig.boundAddress = self.acc_config.getTransportIp()
        sipTpConfig.port = self.acc_config.getTransportPort()
        self.transport = SipClient.ENDPOINT.transportCreate(
            pj.PJSIP_TRANSPORT_UDP, sipTpConfig
        )

        acfg = pj.AccountConfig()
        acfg.idUri = self.acc_config.getIdUri()
        acfg.regConfig.registrarUri = self.acc_config.getRegistrarUri()
        cred = pj.AuthCredInfo(
            "digest", "*", self.acc_config._username, 0, self.acc_config._password
        )
        acfg.sipConfig.authCreds.append(cred)

        self.account = Account(self)
        self.account.create(acfg)

    def make_call(self, dest_username):
        if self.current_call:
            logger.info("Already in a call. Hang up first.")
            return
        
        dest_uri = self.acc_config.getDestinationUri(dest_username)
        logger.info("[SIP] Making call to %s", dest_uri)

        call = Call(self.account)
        prm = pj.CallOpParam(True)
        prm.opt.audioCount = 1
        prm.opt.videoCount = 0
        call.makeCall(dest_uri, prm)
        self.current_call = call
        self.current_call_id = call.getInfo().id

    def answer_call(self):
        if self.current_call:
            call_prm = pj.CallOpParam()
            call_prm.statusCode = 200
            self.current_call.answer(call_prm)
            logger.debug("Call answered")
        else:
            logger.debug("No incoming call to answer")

    def safe_answer_call(self):
        try:
            SipClient.ENDPOINT.libRegisterThread("answer_thread")
            self.answer_call()
        except Exception as e:
            logger.exception("Error in safe_answer_call: %s", str(e))
        finally:
            try:
                if hasattr(SipClient.ENDPOINT, "libUnregisterThread"):
                    SipClient.ENDPOINT.libUnregisterThread()
            except Exception as e:
                logger.exception("Error unregistering thread: %s", str(e))

    def hangup_call(self):
        if self.current_call:
            try:
                call_prm = pj.CallOpParam()
                self.current_call.hangup(call_prm)
                logger.info("Call hung up")
            except pj.Error as e:
                logger.exception("Failed to hang up call: %s", str(e))
        else:
            logger.info("No active call to hang up")

    def reject_call(self):
        if self.current_call:
            call_prm = pj.CallOpParam()
            call_prm.statusCode = 486  # Busy Here
            self.current_call.hangup(call_prm)
            logger.info("Call rejected")
        else:
            logger.info("No incoming call to reject")

    def transfer_call(self, dest_username):
        if self.current_call:
            dest_uri = self.acc_config.getDestinationUri(dest_username)
            self.current_call.transfer(dest_uri)
        else:
            logger.info("No active call to transfer")

    def hold_call(self):
        if self.current_call:
            self.current_call.hold()
        else:
            logger.info("No active call to hold")

    def clear(self):
        self.current_call = None
        self.current_call_id = None

    def get_remote_username(self):
        return self.current_call.remote_user if self.current_call else None
    
    def get_call_state(self):
        if self.current_call:
            return self.current_call.getInfo().state
        return pj.PJSIP_INV_STATE_DISCONNECTED

    @staticmethod
    def register_external_thread():
        SipClient.ENDPOINT.libRegisterThread("external_thread")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    sc = SipClient(
        domain="10.0.0.108",
        port=5070,
        username="106",
        password="Kk106106",
        transport_ip="10.0.0.122",
        transport_port=5066,
        sip_log_level=4,
    )

    # sc = SipClient(
    #     domain='211.21.33.57',
    #     port=19064,
    #     username='1172',
    #     password='dodohome1172',
    #     transport_ip='10.0.0.122',
    #     transport_port=5060,
    #     sip_log_level=4
    # )

    sc.init()

    while True:
        if sc.account.getInfo().regIsActive:
            print("SIP Register Succeed")
            break

    while True:
        sc.ENDPOINT.libHandleEvents(10)
        command = input(
            "Enter command (c: call, h: hangup, a: answer, r: reject, t: transfer, q: quit): "
        ).lower()
        if command == "c":
            sc.make_call("104")
        elif command == "h":
            sc.hangup_call()
        elif command == "a":
            sc.answer_call()
        elif command == "r":
            sc.reject_call()
        elif command == "t":
            sc.transfer_call("105")
        elif command == "hold":
            sc.hold_call()
        elif command == "q":
            break
        else:
            print("Invalid command")
