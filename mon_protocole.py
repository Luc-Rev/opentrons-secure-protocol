# mon_protocole.py
import os, hmac, hashlib, time
from opentrons import protocol_api


metadata = {
    "protocolName": "Secured Run",
    "author": "Luc",
    "description": "Protocol requiring authentication (env or signed token)",
}
requirements = {"robotType": "Flex", "apiLevel": "2.24"}

# La variable charge automatiquement le contenu du fichier
SECRET_KEY = b""
TOKEN_FILENAME = "auth_token.txt"
TOKEN_TTL_SECONDS = 86400  #
# ----------------------------------------------------------------

def _check_env_auth():
    """Local simulate guard: env flags set by the secure launcher."""
    return os.environ.get("OT_AUTH") == "OK"

def _check_bundled_token(protocol: protocol_api.ProtocolContext):
    """Robot guard: verify signed token bundled with the protocol."""
    data = getattr(protocol, "bundled_data", None)
    if not data or TOKEN_FILENAME not in data:
        return False
    try:
        raw = data[TOKEN_FILENAME].decode("utf-8").strip()
        # token format: username|ts|nonce|hmac_hex
        username, ts_s, nonce, sig_hex = raw.split("|", 3)
        ts = int(ts_s)
        if abs(time.time() - ts) > TOKEN_TTL_SECONDS:
            return False
        msg = f"{username}|{ts}|{nonce}".encode("utf-8")
        expected = hmac.new(SECRET_KEY, msg, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, sig_hex)
    except Exception:
        return False

def _require_auth(protocol: protocol_api.ProtocolContext):
    # Accept either env-based (local simulate) or bundled signed token (robot)
    if _check_env_auth():
        protocol.comment(f"[AUTH] Local simulate OK: user={os.environ.get('OT_USER','unknown')}")
        return
    if _check_bundled_token(protocol):
        protocol.comment("[AUTH] Robot token OK")
        return
    raise RuntimeError("Authentication required: set OT_AUTH/OT_USER (simulate) or provide signed token file.")


def run(protocol: protocol_api.ProtocolContext):
    _require_auth(protocol)
       # -------------------- Modules (sans adaptateur HS) --------------------
    tc = protocol.load_module("thermocyclerModuleV2", "B1")
    hs = protocol.load_module("heaterShakerModuleV1", "C1")      # sans adaptateur
    tempmod = protocol.load_module("temperatureModuleV2", "D1")  # non utilisé
    mag = protocol.load_module("magneticBlockV1", "D2")
    tip50 = protocol.load_labware('opentrons_flex_96_tiprack_50ul', 'C2')
    tip1k_A3 = protocol.load_labware("opentrons_flex_96_filtertiprack_1000ul", "C3")
    p50      = protocol.load_instrument("flex_8channel_50", "left",  tip_racks=[tip50])
    p1000    = protocol.load_instrument("flex_8channel_1000", "right", tip_racks=[tip1k_A3])

    waste_chute = protocol.load_waste_chute()

    # --- 3. AJOUT DE LA PLAQUE EN A2 ---
    # On charge une plaque PCR standard 96 puits
    plaque = protocol.load_labware("opentrons_96_wellplate_200ul_pcr_full_skirt", "A2")

    # --- 4. DÉPLACEMENT AVEC LE GRIPPER ---
    protocol.comment("🤖 Début du déplacement : Prise de la plaque en A2...")
    
    protocol.move_labware(
        labware=plaque,
        new_location="A3",
        use_gripper=True
    )

    protocol.comment("Run complete ✅")
