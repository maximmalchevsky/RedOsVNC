import tkinter as tk
from tkinter import messagebox
import subprocess
import netifaces
import signal
import os

VNC_PORT = 5900
vnc_process = None


def get_primary_ip():
    gateways = netifaces.gateways()
    default_gw = gateways.get('default', {})
    if netifaces.AF_INET not in default_gw:
        return None
    iface = default_gw[netifaces.AF_INET][1]
    addrs = netifaces.ifaddresses(iface)
    if netifaces.AF_INET in addrs:
        return addrs[netifaces.AF_INET][0]['addr']
    return None


def start_vnc():
    global vnc_process
    try:
        if vnc_process is None:
            display_env = os.environ.get("DISPLAY", ":0")
            vnc_process = subprocess.Popen([
                "x11vnc",
                "-display", display_env,
                "-rfbport", str(VNC_PORT),
                "-auth", "guess",
                "-shared",
                "-nopw"
            ])
            log(f"[INFO] VNC запущен на {get_primary_ip()}:{VNC_PORT} (DISPLAY={display_env})")
        else:
            log("[WARN] VNC уже запущен")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить VNC:\n{e}")
        log(f"[ERROR] {e}")


def stop_vnc():
    global vnc_process
    try:
        if vnc_process:
            os.kill(vnc_process.pid, signal.SIGTERM)
            vnc_process.wait()
            vnc_process = None
            log("[INFO] VNC сервер остановлен (доступ отозван)")
        else:
            log("[WARN] VNC не был запущен")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось остановить VNC:\n{e}")
        log(f"[ERROR] {e}")


def log(msg):
    log_box.configure(state="normal")
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)
    log_box.configure(state="disabled")


def on_close():
    stop_vnc()
    root.destroy()



root = tk.Tk()
root.title("Техподдержка")
root.geometry("750x550")
root.configure(bg="#2e3440")

primary_bg = "#2e3440"
secondary_bg = "#3b4252"
primary_text = "#eceff4"
accent = "#88c0d0"
danger = "#bf616a"


header = tk.Label(
    root,
    text="Удалённый доступ для техподдержки",
    font=("Arial", 20, "bold"),
    bg=primary_bg,
    fg=accent
)
header.pack(pady=(20, 10))


ip = get_primary_ip()
ip_label = tk.Label(
    root,
    text=f"Сообщите ваш IP сотруднику поддержки: \n{ip if ip else 'Не найден'}\nПорт: {VNC_PORT}",
    font=("Arial", 16),
    bg=primary_bg,
    fg=primary_text,
    justify="center"
)
ip_label.pack(pady=(10, 20))



def create_rounded_button(parent, text, command, width=200, height=50, radius=15, bg_color=danger, fg_color="white"):
    canvas = tk.Canvas(parent, width=width, height=height, bg=primary_bg, highlightthickness=0)
    canvas.pack(pady=10)
    rect = canvas.create_rectangle(2, 2, width - 2, height - 2, fill=bg_color, outline=bg_color)
    label = canvas.create_text(width // 2, height // 2, text=text, fill=fg_color, font=("Arial", 14, "bold"))

    def click(event):
        command()

    canvas.tag_bind(rect, "<Button-1>", click)
    canvas.tag_bind(label, "<Button-1>", click)
    return canvas


btn_stop = create_rounded_button(root, "Отозвать доступ", stop_vnc, width=250, height=50, radius=15, bg_color=danger)


log_frame = tk.Canvas(root, bg=primary_bg, bd=0, highlightthickness=0, width=700, height=200)
log_frame.pack(pady=10)
log_bg = log_frame.create_rectangle(0, 0, 700, 200, fill=secondary_bg, outline=secondary_bg, width=0)
log_box = tk.Text(log_frame,
                  height=10,
                  width=82,
                  bg=secondary_bg,
                  fg=primary_text,
                  font=("Consolas", 11),
                  bd=0,
                  highlightthickness=0,
                  wrap="word")
log_box.place(x=5, y=5, width=690, height=190)
log_box.configure(state="disabled")


root.after(1000, start_vnc)
root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
