import streamlit as st
import socket
from datetime import datetime
import threading
from queue import Queue

# =========================
# 🎨 HACKER UI STYLE
# =========================
st.set_page_config(page_title="Cyber Scanner", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #0d0d0d; color: #00ff9f; }
h1, h2, h3 { color: #00ff9f; }
.stButton>button {
    background-color: #111;
    color: #00ff9f;
    border: 1px solid #00ff9f;
}
</style>
""", unsafe_allow_html=True)

st.title("⚡ CYBER PORT SCANNER")

tab1, tab2 = st.tabs(["🛠 Scanner", "📊 Results"])

if "results" not in st.session_state:
    st.session_state.results = []

common_ports = {
    21: "FTP", 22: "SSH", 23: "TELNET", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 3306: "MySQL", 8080: "HTTP-ALT"
}

# =========================
# THREAD WORKER
# =========================
def scan_worker(target_ip, queue, results, timeout, counter, lock):
    while True:
        try:
            port = queue.get_nowait()
        except:
            return

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)

            result = sock.connect_ex((target_ip, port))

            if result == 0:
                service = common_ports.get(port, "Unknown")

                try:
                    banner = sock.recv(1024).decode().strip()
                except:
                    banner = "No banner"

                with lock:
                    results.append(f"[OPEN] Port {port} | {service} | {banner}")

            sock.close()
        except:
            pass

        # 🔥 SAFE COUNTER UPDATE
        with lock:
            counter[0] += 1

        queue.task_done()


# =========================
# TAB 1 - SCANNER
# =========================
with tab1:
    target = st.text_input("Target (IP or Domain)")

    scan_type = st.selectbox("Scan Type", [
        "Quick Scan (1-1024)",
        "Full Scan (1-65535)",
        "Custom"
    ])

    if scan_type == "Quick Scan (1-1024)":
        start_port, end_port = 1, 1024
    elif scan_type == "Full Scan (1-65535)":
        start_port, end_port = 1, 65535
    else:
        start_port = st.number_input("Start Port", 1, 65535, 1)
        end_port = st.number_input("End Port", 1, 65535, 1024)

    timeout = st.slider("Timeout", 0.1, 3.0, 1.0)
    thread_count = st.slider("Threads", 10, 300, 100)

    scan_button = st.button("🚀 Start Scan")

    if scan_button:
        st.session_state.results = []

        try:
            target_ip = socket.gethostbyname(target)
        except:
            st.error("Invalid target")
            st.stop()

        st.info(f"Scanning {target_ip}")

        start_time = datetime.now()

        queue = Queue()
        for port in range(start_port, end_port + 1):
            queue.put(port)

        total_ports = end_port - start_port + 1
        counter = [0]
        lock = threading.Lock()

        # 🔥 UI placeholders
        progress_bar = st.progress(0)
        live_output = st.empty()

        threads = []

        for _ in range(thread_count):
            t = threading.Thread(
                target=scan_worker,
                args=(target_ip, queue, st.session_state.results, timeout, counter, lock)
            )
            t.daemon = True
            t.start()
            threads.append(t)

        # 🔥 REAL-TIME LOOP
        while any(t.is_alive() for t in threads):
            with lock:
                progress = counter[0] / total_ports
                progress_bar.progress(progress)

                # Show last few results (live feed style)
                latest = st.session_state.results[-10:]
                live_output.code("\n".join(latest) if latest else "Scanning...")

        for t in threads:
            t.join()

        end_time = datetime.now()
        duration = end_time - start_time

        progress_bar.progress(1.0)

        st.success(f"Scan completed in {duration}")

# =========================
# TAB 2 - RESULTS
# =========================
with tab2:
    st.subheader("Scan Results")

    if st.session_state.results:
        st.code("\n".join(st.session_state.results))

        st.download_button(
            "📥 Download Results",
            "\n".join(st.session_state.results),
            file_name="scan_results.txt"
        )
    else:
        st.warning("No results yet.")