
```
██████╗  ██████╗ ██████╗ ████████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗
██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
██████╔╝██║   ██║██████╔╝   ██║       ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
██╔═══╝ ██║   ██║██╔══██╗   ██║       ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
██║     ╚██████╔╝██║  ██║   ██║       ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
```

<h1 align="center">PORT SCANNER</h1>
<p align="center">A multithreaded TCP port scanner for network reconnaissance — real-time service detection, banner grabbing, and open port discovery.</p>

---

═══════════════════════════════
OVERVIEW
═══════════════════════════════

## Overview

Port Scanner is a Python-based network reconnaissance tool built with Streamlit. It allows users to scan a target host for open TCP ports across a configurable range, with real-time feedback, multithreaded execution, and service banner grabbing. The interface adopts a dark terminal aesthetic designed for clarity and focus during active scans.

---

═══════════════════════════════
OBJECTIVES
═══════════════════════════════

## Objectives

- Provide a fast, multithreaded port scanning engine capable of covering the full 65535 port range
- Display live scan progress and open port results in real time within the browser UI
- Identify common services by port number and attempt to retrieve service banners
- Allow flexible scan configuration including port range, timeout, and thread count
- Export discovered results as a plain-text report for further analysis

---

═══════════════════════════════
TOOLS & TECHNOLOGIES
═══════════════════════════════

## Tools & Technologies

![Python](https://img.shields.io/badge/Python-3.x-black?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-black?style=flat&logo=streamlit&logoColor=white)
![Socket](https://img.shields.io/badge/Socket-Networking-black?style=flat)
![Threading](https://img.shields.io/badge/Threading-Concurrency-black?style=flat)

---

═══════════════════════════════
PROJECT STRUCTURE
═══════════════════════════════

## Project Structure

```
Port_Scanner/
│── app.py
│── README.md
│── Screenshots/
│   │── scanner.png
│   │── scan_results.png
│   │── timestamp.png
```

---

═══════════════════════════════
METHODOLOGY
═══════════════════════════════

## Methodology

### Target Resolution

The tool accepts either an IP address or a domain name as the scan target. It resolves the hostname to an IP using Python's `socket.gethostbyname()` before initiating any connection attempts, ensuring compatibility with both formats.

### Multithreaded Scanning Engine

Ports are distributed across worker threads via a shared thread-safe queue. Each thread independently attempts a TCP connection to its assigned port using `socket.connect_ex()`. A configurable timeout and thread count allow the user to balance scan speed against network stability. A shared lock ensures safe concurrent updates to the result list and progress counter.

### Service Identification & Banner Grabbing

After a successful connection, the scanner cross-references the port number against a dictionary of well-known services (FTP, SSH, HTTP, MySQL, etc.). It then attempts to receive a banner from the open socket, which may reveal server software and version information.

### Real-Time UI Feedback

A live progress bar and scrolling result feed update continuously while threads are running. Once all threads complete, the final result set is written to the Results tab and made available for download.

---

═══════════════════════════════
RESULTS & SCREENSHOTS
═══════════════════════════════

## Results & Screenshots

### Scanner Interface

![scanner](Screenshots/scanner.png)

The main scan interface showing target input, scan type selection, timeout slider, thread count configuration, and the live output terminal feed during an active scan.

---

### Scan Results

![scan_results](Screenshots/scan_results.png)

The Results tab displaying discovered open ports along with their associated service names and any captured banners. Results can be downloaded as a `.txt` file directly from this view.

---

### Timestamp & Completion

![timestamp](Screenshots/timestamp.png)

Scan completion summary showing the elapsed duration and a fully populated results log, confirming successful end-to-end execution.

---

═══════════════════════════════
COMMANDS & CODE
═══════════════════════════════

## Commands & Code

**Install dependencies:**

```bash
pip install streamlit
```

**Run the application:**

```bash
streamlit run app.py
```

**Core scan logic:**

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(timeout)
result = sock.connect_ex((target_ip, port))

if result == 0:
    service = common_ports.get(port, "Unknown")
    banner = sock.recv(1024).decode().strip()
```

---

═══════════════════════════════
CONCLUSION
═══════════════════════════════

## Conclusion

Port Scanner demonstrates the practical application of multithreaded network programming within a polished, browser-based interface. The project reinforces core concepts in socket programming, thread synchronization, and real-time UI rendering. It delivers a functional and extensible reconnaissance tool with a strong emphasis on usability and visual clarity.

---

<p align="center">Developed as a personal cybersecurity tooling project</p>
