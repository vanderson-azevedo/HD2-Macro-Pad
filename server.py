from flask import Flask, request, jsonify, send_from_directory
from waitress import serve
import pyautogui
import time
import threading
import logging
from datetime import datetime

app = Flask(__name__)
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('hd2')

@app.after_request
def log_request(response):
    now = datetime.now().strftime('%H:%M:%S')
    log.info(f'➡️ Comando Recebido | {request.remote_addr} | [{now}] "{request.method} {request.path}"')
    return response

STRATAGEMS = {
    # Eagle
    "eagle_airstrike":      ["ctrl", "w", "d", "w", "w"],
    "eagle_500kg":          ["ctrl", "w", "d", "d", "w", "d"],
    "eagle_cluster":        ["ctrl", "w", "d", "w", "w", "d"],
    "eagle_napalm":         ["ctrl", "w", "d", "s", "w"],
    "eagle_smoke":          ["ctrl", "w", "d", "w", "d"],
    "eagle_110mm":          ["ctrl", "w", "d", "w", "a"],
    "eagle_strafing":       ["ctrl", "w", "d", "d"],
    "eagle_rearm":          ["ctrl", "w", "w", "a", "w", "d"],
    # Orbital
    "orbital_precision":    ["ctrl", "d", "d", "w"],
    "orbital_laser":        ["ctrl", "d", "s", "w", "d", "s"],
    "orbital_railcannon":   ["ctrl", "d", "s", "w", "d", "w"],
    "orbital_gatling":      ["ctrl", "d", "s", "w", "a"],
    "orbital_airburst":     ["ctrl", "d", "d", "s"],
    "orbital_120mm":        ["ctrl", "d", "s", "a", "d", "s"],
    "orbital_380mm":        ["ctrl", "d", "s", "s", "a", "s", "d"],
    "orbital_ems":          ["ctrl", "d", "s", "w", "s"],
    "orbital_smoke":        ["ctrl", "d", "s", "s", "d"],
    "orbital_gas":          ["ctrl", "d", "s", "s", "a"],
    "orbital_napalm":       ["ctrl", "d", "s", "a", "a", "s"],
    "orbital_walking":      ["ctrl", "d", "s", "d", "s", "d", "s"],
    "orbital_illumination": ["ctrl", "d", "s", "s", "w"],
    # Sentinelas
    "machine_gun_sentry":   ["ctrl", "s", "w", "d", "d", "w"],
    "gatling_sentry":       ["ctrl", "s", "w", "d", "a"],
    "autocannon_sentry":    ["ctrl", "s", "w", "d", "w", "a", "w"],
    "mortar_sentry":        ["ctrl", "s", "w", "d", "d", "s"],
    "rocket_sentry":        ["ctrl", "s", "w", "d", "d", "a"],
    "tesla_tower":          ["ctrl", "s", "w", "d", "w", "a", "d"],
    "ems_mortar_sentry":    ["ctrl", "s", "w", "d", "s", "d"],
    "laser_sentry":         ["ctrl", "s", "w", "d", "s", "w", "d"],
    "flame_sentry":         ["ctrl", "s", "w", "d", "s", "w", "w"],
    "gas_mortar_sentry":    ["ctrl", "s", "w", "d", "s", "a"],
    # Defesa
    "hmg_emplacement":      ["ctrl", "s", "w", "a", "d", "d", "a"],
    "anti_tank_emplacement":["ctrl", "s", "w", "a", "d", "d", "d"],
    "grenadier_battlement": ["ctrl", "s", "d", "s", "a", "d"],
    "shield_relay":         ["ctrl", "s", "s", "a", "d", "a", "d"],
    "anti_personnel_mine":  ["ctrl", "s", "a", "w", "d"],
    "incendiary_mines":     ["ctrl", "s", "a", "a", "s"],
    "anti_tank_mines":      ["ctrl", "s", "a", "w", "w"],
    "gas_mines":            ["ctrl", "s", "a", "a", "d"],
    # Armas
    "machine_gun":          ["ctrl", "s", "a", "s", "w", "d"],
    "expendable_at":        ["ctrl", "s", "s", "a", "w", "d"],
    "stalwart":             ["ctrl", "s", "a", "s", "w", "w", "a"],
    "laser_cannon":         ["ctrl", "s", "a", "s", "w", "a"],
    "anti_materiel_rifle":  ["ctrl", "s", "a", "d", "w", "s"],
    "recoilless_rifle":     ["ctrl", "s", "a", "d", "d", "a"],
    "grenade_launcher":     ["ctrl", "s", "a", "w", "a", "s"],
    "flamethrower":         ["ctrl", "s", "a", "w", "s", "w"],
    "hmg":                  ["ctrl", "s", "a", "w", "s", "s"],
    "autocannon":           ["ctrl", "s", "a", "s", "w", "w", "d"],
    "arc_thrower":          ["ctrl", "s", "d", "s", "w", "a", "a"],
    "quasar":               ["ctrl", "s", "s", "w", "a", "d"],
    "airburst_launcher":    ["ctrl", "s", "w", "w", "a", "d"],
    "commando":             ["ctrl", "s", "a", "w", "s", "d"],
    "spear":                ["ctrl", "s", "s", "w", "s", "s"],
    "railgun":              ["ctrl", "s", "d", "s", "w", "a", "d"],
    "wasp_launcher":        ["ctrl", "s", "s", "w", "s", "d"],
    "breaching_hammer":     ["ctrl", "s", "a", "d", "a", "w"],
    "epoch":                ["ctrl", "s", "a", "w", "a", "d"],
    "bullet_storm":         ["ctrl", "s", "a", "s", "d", "w", "a"],
    "speargun":             ["ctrl", "s", "d", "s", "a", "w", "d"],
    "defoliation_tool":     ["ctrl", "s", "a", "d", "d", "s"],
    "de_escalator":         ["ctrl", "s", "d", "w", "a", "d"],
    "expendable_napalm":    ["ctrl", "s", "s", "a", "w", "a"],
    "sterilizer":           ["ctrl", "s", "a", "w", "s", "a"],
    "leveller":             ["ctrl", "s", "s", "a", "w", "s"],
    "belt_grenade_launcher":["ctrl", "s", "a", "w", "a", "w", "w"],
    "c4_pack":              ["ctrl", "s", "d", "w", "w", "d", "w"],
    "cremator":             ["ctrl", "s", "s", "d", "s", "w", "w"],
    "maxigun":              ["ctrl", "s", "a", "d", "s", "w", "w"],
    "one_true_flag":        ["ctrl", "s", "a", "d", "d", "w"],
    "meltagun":             ["ctrl", "s", "a", "w", "a", "a", "s"],
    "solo_silo":            ["ctrl", "s", "w", "d", "s", "s"],
    # Backpacks
    "supply_pack":          ["ctrl", "s", "a", "s", "w", "w", "s"],
    "jump_pack":            ["ctrl", "s", "w", "w", "s", "w"],
    "ballistic_shield":     ["ctrl", "s", "a", "s", "s", "w", "a"],
    "guard_dog":            ["ctrl", "s", "w", "a", "w", "d", "s"],
    "rover":                ["ctrl", "s", "w", "a", "w", "d", "d"],
    "shield_generator":     ["ctrl", "s", "w", "a", "d", "a", "d"],
    "directional_shield":   ["ctrl", "s", "w", "a", "d", "w", "w"],
    "hot_dog":              ["ctrl", "s", "w", "a", "w", "a", "a"],
    "k9":                   ["ctrl", "s", "w", "a", "w", "d", "a"],
    "hover_pack":           ["ctrl", "s", "w", "w", "s", "a", "d"],
    "dog_breath":           ["ctrl", "s", "w", "a", "w", "d", "w"],
    "warp_pack":            ["ctrl", "s", "a", "d", "s", "a", "d"],
    # Exosuits
    "patriot_exosuit":      ["ctrl", "a", "s", "d", "w", "a", "s", "s"],
    "emancipator_exosuit":  ["ctrl", "a", "s", "d", "w", "a", "s", "w"],
    "lumberer_exosuit":     ["ctrl", "a", "s", "d", "w", "d", "a", "w"],
    "breakthrough_exosuit": ["ctrl", "a", "s", "d", "a", "d", "s", "w"],
    "bastion_exosuit":      ["ctrl", "a", "s", "d", "s", "a", "s", "w", "s", "w"],
    # Veiculos
    "fast_recon_vehicle":   ["ctrl", "a", "s", "d", "s", "d", "s", "w"],
    "incinerator_frv":      ["ctrl", "a", "s", "d", "a", "s", "w", "w"],
    "supply_frv":           ["ctrl", "a", "s", "a", "a", "s", "w", "d"],
    # Missao
    "portable_hellbomb":    ["ctrl", "s", "d", "w", "w", "w"],
    "cargo_container":      ["ctrl", "w", "w", "s", "s", "d", "s"],
    "drill":                ["ctrl", "s", "s", "a", "d", "s", "s"],
    "seaf_artillery":       ["ctrl", "d", "w", "w", "s"],
    "seismic_probe":        ["ctrl", "w", "w", "a", "d", "s", "s"],
    "upload_data":          ["ctrl", "s", "s", "s", "s", "s", "w", "w"],
    "dark_fluid_vessel":    ["ctrl", "w", "a", "d", "s", "w", "w"],
    "call_super_destroyer": ["ctrl", "w", "w", "s", "s", "a", "d", "a", "d"],
    # Essenciais
    "reinforce":            ["ctrl", "w", "s", "d", "a", "w"],
    "resupply":             ["ctrl", "s", "s", "w", "d"],
    "sos_beacon":           ["ctrl", "w", "s", "d", "w"],
    "hellbomb":             ["ctrl", "s", "w", "a", "s", "w", "d", "s", "w"],
    "super_earth_flag":     ["ctrl", "s", "w", "s", "w"],
}

def execute_stratagem(keys):
    time.sleep(0.1)
    pyautogui.keyDown("ctrl")
    time.sleep(0.1)
    for key in keys[1:]:
        pyautogui.keyDown(key)
        time.sleep(0.1)
        pyautogui.keyUp(key)
        time.sleep(0.1)
    pyautogui.keyUp("ctrl")

@app.route("/ping")
def ping():
    return jsonify({"ok": True})

@app.route("/")
def index():
    return send_from_directory("web", "index.html")

@app.route("/icons/<path:filename>")
def icons(filename):
    return send_from_directory("web/icons", filename)

@app.route("/stratagem/<name>", methods=["POST"])
def stratagem(name):
    if name not in STRATAGEMS:
        print(f"[ERRO] Stratagem nao encontrado: {name}")
        return jsonify({"error": "Stratagem nao encontrado"}), 404
    # print(f"[DISPARO] {name}")
    threading.Thread(target=execute_stratagem, args=(STRATAGEMS[name],), daemon=True).start()
    return jsonify({"ok": True, "stratagem": name})

if __name__ == "__main__":
    print("==================================================================")
    print("🚀 ┊ HD2-Macro-Pad ATIVO E RODANDO!")
    print("==================================================================")
    print("🌐 ┊ Acesse pelo seu dispositivo : http://<SEU_IP_LOCAL>:5000")
    print("📌 ┊ Requisito: O dispositivo deve estar na MESMA REDE WI-FI DO PC.")
    print("------------------------------------------------------------------")
    print("⚠️ » ATENÇÃO: MANTENHA ESTA JANELA ABERTA ENQUANTO ESTIVER USANDO!")
    print("🛑 » Para encerrar o servidor com segurança, pressione: Ctrl + C")
    print("==================================================================\n")

    # O serve deve ser a ÚLTIMA linha, pois ele bloqueia a execução do script
    serve(app, host="0.0.0.0", port=5000)
