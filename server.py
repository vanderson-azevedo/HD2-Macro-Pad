from flask import Flask, request, jsonify, send_from_directory
from waitress import serve
import pyautogui
import time
import threading
import logging
import sys
import os
import socket
from datetime import datetime

def resource_path(relative):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)

app = Flask(__name__)
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

logging.disable(logging.CRITICAL)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

# Callbacks injetados pela GUI
_gui_log_cb    = None
_gui_status_cb = None
_connected_ips = {}

def _notify_log(msg):
    if _gui_log_cb:
        _gui_log_cb(msg)

def _notify_status():
    if _gui_status_cb:
        _gui_status_cb(_connected_ips)

@app.after_request
def track_request(response):
    ip = request.remote_addr
    if ip != "127.0.0.1":
        _connected_ips[ip] = datetime.now()
        _notify_status()
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
    return send_from_directory(resource_path("web"), "index.html")

@app.route("/icons/<path:filename>")
def icons(filename):
    return send_from_directory(resource_path("web/icons"), filename)

@app.route("/stratagem/<name>", methods=["POST"])
def stratagem(name):
    if name not in STRATAGEMS:
        return jsonify({"error": "Stratagem nao encontrado"}), 404
    now   = datetime.now().strftime("%H:%M:%S")
    label = name.replace("_", " ").title()
    _notify_log(f"🕗 [{now}] | 🌐 {request.remote_addr} | 📲 {label}")
    threading.Thread(target=execute_stratagem, args=(STRATAGEMS[name],), daemon=True).start()
    return jsonify({"ok": True, "stratagem": name})

if __name__ == "__main__":
    import tkinter as tk
    from PIL import Image, ImageTk

    BG     = "#090b0e"
    YELLOW = "#ffe800"
    DIM    = "#3a3a2a"
    GREEN  = "#39ff14"
    FONT   = "Courier"

    local_ip = get_local_ip()

    root = tk.Tk()
    root.title("HD2 Macro-Pad")
    root.configure(bg=BG)
    root.resizable(False, False)
    root.geometry("460x580")

    try:
        root.iconbitmap(resource_path("icon.ico"))
    except Exception:
        pass

    # Logo
    try:
        pil_img  = Image.open(resource_path(os.path.join("hd2_macropad_glow.png")))
        pil_img = pil_img.resize(
            (int(pil_img.width * 0.15), int(pil_img.height * 0.15)),
            Image.LANCZOS
        )
        logo_img = ImageTk.PhotoImage(pil_img)
        lbl_logo = tk.Label(root, image=logo_img, bg=BG)
        lbl_logo.image = logo_img
        lbl_logo.pack(pady=(28, 6))
    except Exception:
        tk.Label(root, text="⚙", font=(FONT, 48), bg=BG, fg=YELLOW).pack(pady=(28, 6))

    # tk.Label(root, text="HD2 MACRO-PAD",
    #          font=(FONT, 15, "bold"), bg=BG, fg=YELLOW).pack()
    tk.Label(root, text=f"ENDEREÇO DE CONEXÃO: {local_ip}:5000",
             font=(FONT, 9), bg=BG, fg=DIM).pack(pady=(2, 14))

    # Status
    status_var = tk.StringVar(value="🟠 | Aguardando conexão do dispositivo...")
    status_lbl = tk.Label(root, textvariable=status_var,
                          font=(FONT, 10, "bold"), bg=BG, fg=DIM)
    status_lbl.pack()

    tk.Frame(root, bg="#2a2a1a", height=1).pack(fill="x", padx=24, pady=12)

    # Log
    tk.Label(root, text="📜 | LOG DE DISPAROS",
             font=(FONT, 8), bg=BG, fg=DIM).pack(anchor="w", padx=24)

    log_frame = tk.Frame(root, bg="#0d1117")
    log_frame.pack(fill="both", expand=True, padx=24, pady=(4, 24))

    log_text = tk.Text(log_frame, bg="#0d1117", fg="#b8b890",
                       font=(FONT, 9), state="disabled",
                       relief="flat", bd=0, wrap="word")
    sb = tk.Scrollbar(log_frame, command=log_text.yview, bg=BG, troughcolor=BG)
    log_text.configure(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y")
    log_text.pack(fill="both", expand=True, padx=6, pady=6)

    # Callbacks
    def on_log(msg):
        def _do():
            log_text.configure(state="normal")
            log_text.insert("end", msg + "\n")
            log_text.see("end")
            log_text.configure(state="disabled")
        root.after(0, _do)

    def on_status(ips):
        def _do():
            if not ips:
                status_var.set("⬤  Aguardando dispositivo...")
                status_lbl.configure(fg=DIM)
            else:
                latest = max(ips, key=ips.get)
                status_var.set(f"⬤  Dispositivo conectado: {latest}")
                status_lbl.configure(fg=GREEN)
        root.after(0, _do)

    _gui_log_cb    = on_log
    _gui_status_cb = on_status

    threading.Thread(
        target=lambda: serve(app, host="0.0.0.0", port=5000),
        daemon=True
    ).start()

    root.mainloop()
