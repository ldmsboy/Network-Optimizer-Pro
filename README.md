<div align="center">

# 🌐 Network Optimizer Pro
**A modern, interactive web system for network scanning and topology mapping.**<br>
**Un sistema avanzado con interfaz web interactiva para el escaneo, mapeo y optimización de topologías de red en tiempo real.**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![License](https://img.shields.io/badge/License-Copyright%20(All%20Rights%20Reserved)-red?style=for-the-badge)

<br>
<a href="https://www.linkedin.com/in/ldmsboy"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
<a href="https://peerlist.io/ldmsboy"><img src="https://img.shields.io/badge/Peerlist-00CA51?style=for-the-badge&logo=peerlist&logoColor=white" alt="Peerlist"></a>
<a href="https://x.com/LuisDaniel38815"><img src="https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white" alt="X"></a>
<a href="https://www.instagram.com/ldmsboy/"><img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram"></a>
<a href="https://www.facebook.com/ldmsboy/"><img src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook"></a>
<br><br>

[🇪🇸 Español](#-español) | [🇬🇧 English](#-english)

---
</div>

## 🇪🇸 Español

Construido con Python y Flask en el backend, utiliza `scapy` para la captura y análisis de paquetes de red a bajo nivel.

### 🚀 Características Principales

*   **Escaneo Activo de Red:** Utiliza peticiones ARP (`scapy`) para descubrir dispositivos activos en la red local.
*   **Identificación de Dispositivos:** Resuelve direcciones MAC a fabricantes (OUI lookup) para adivinar inteligentemente el tipo de dispositivo (móvil, servidor, TV, router, PC).
*   **Topología Dinámica:** Genera un grafo interactivo de la red en tiempo real en la interfaz web.
*   **Optimización de Redes:** Calcula el Árbol de Expansión Mínima (Minimum Spanning Tree) y la ruta más corta (Shortest Path) mediante la librería matemática `networkx`.
*   **Modo Demostración Automático:** Si no se detectan permisos de administrador, el sistema realiza una simulación generando dispositivos virtuales. Esto asegura que la interfaz web pueda probarse y visualizarse sin errores ni bloqueos por falta de permisos.
*   **Escaneo de Puertos:** Herramienta manual adicional para revisar puertos comunes abiertos en dispositivos específicos.

---

### ⚙️ ¿Cómo funciona el Sistema?

El sistema está dividido en dos capas principales:

1.  **Backend (Python + Flask):** Actúa como el motor del sistema. Expone un servidor web ligero y una API RESTful. Cuando el usuario solicita un escaneo, el backend llama a las rutinas de `scapy` para inyectar paquetes ARP en la red, escucha las respuestas, y procesa las IPs y direcciones MAC resultantes. También mantiene el estado de la topología en memoria usando la librería `networkx`.
2.  **Frontend (HTML + JS):** Una interfaz intuitiva y moderna que consume las rutas `/api/*`. Recibe la lista de nodos y conexiones calculadas y los dibuja gráficamente. Permite a los usuarios interactuar, realizar nuevos escaneos o aplicar algoritmos de optimización de manera gráfica.

---

### 🛠️ Arquitectura y Cómo Desarrollar

El proyecto sigue el patrón de diseño de **Separación de Responsabilidades (SoC)**, asegurando que la lógica matemática y de red sea completamente independiente de la interfaz gráfica.

La estructura de archivos (Arquitectura Modular Profesional) es:

*   **`network_optimizer/`:** Paquete principal del código fuente.
    *   **`core/`:** Lógica de negocio (Independiente de la UI).
        *   `graph.py`: Define la estructura base de la red (`NetworkGraph`).
        *   `algorithms.py`: Tus implementaciones matemáticas puras (Kruskal, Dijkstra, TSP).
        *   `scanner.py`: Aísla la lógica de bajo nivel (peticiones ARP de `scapy`, escaneo de puertos, resolución MAC).
    *   **`web/`:** Capa de presentación Web.
        *   `server.py`: Actúa como controlador de API usando Flask.
        *   `templates/` y `static/`: Archivos HTML, CSS y JS del frontend.
    *   **`gui/`:** Capa de presentación de Escritorio.
        *   `desktop_app.py`: Interfaz gráfica interactiva utilizando Tkinter y Matplotlib.
*   **`run_web.py`:** Punto de entrada (entry-point) principal para arrancar el entorno web.
*   **`run_gui.py`:** Punto de entrada para arrancar la herramienta de escritorio.

**Flujo de Desarrollo Recomendado:**
1.  Aplica tus cambios lógicos en la carpeta `network_optimizer/` correspondiente.
2.  Flask arranca por defecto en `debug mode`, reiniciándose automáticamente al guardar cualquier cambio en los archivos (Hot Reloading).
3.  Puedes desarrollar el frontend (HTML/CSS/JS) sin necesidad de ser root aprovechando el "Modo Demostración" inteligente del escaneo.
4.  Si cambias la lógica de paquetes (`scapy`), prueba el sistema ejecutando la aplicación con permisos completos.

---

### 📦 Dependencias Requeridas

El sistema utiliza paquetes modernos de Python. Las dependencias exactas se encuentran en el archivo `requirements.txt`.

*   **[Flask](https://flask.palletsprojects.com/):** Framework web ligero utilizado para levantar la API RESTful y servir la interfaz HTML.
*   **[Scapy](https://scapy.net/):** Herramienta de manipulación interactiva de paquetes. Es el motor principal para enviar las peticiones ARP a la capa de red.
*   **[NetworkX](https://networkx.org/):** Librería especializada en la creación, manipulación y estudio dinámico de la estructura, dinámicas y funciones de grafos complejos.
*   **[Matplotlib](https://matplotlib.org/):** Utilizada exclusivamente por la interfaz de escritorio (`gui`) para renderizar el lienzo del mapa de red.
*   **[Requests](https://requests.readthedocs.io/):** Para llamadas HTTP a APIs externas (ej. OUI Lookup si se expande en el futuro).

---

### 📥 Guía de Instalación Paso a Paso

Te recomendamos usar un **entorno virtual** para no generar conflictos con otras librerías de Python en tu sistema. Sigue estos pasos en tu terminal:

1. **Clona el repositorio** y entra a la carpeta:
   ```bash
   git clone <tu-repositorio>
   cd "6 - Analisisdeted"
   ```

2. **Crea un entorno virtual** (opcional pero muy recomendado):
   ```bash
   python3 -m venv venv
   ```

3. **Activa el entorno virtual**:
   * **En Windows (CMD o PowerShell):**
     ```powershell
     .\venv\Scripts\activate
     ```
   * **En Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```

4. **Instala TODAS las dependencias de una vez:**
   Ejecuta el siguiente comando maestro para instalar Flask, Scapy, NetworkX y todo lo necesario en un solo paso:
   ```bash
   pip install -r requirements.txt
   ```

---

### 🖥️ Compilación y Ejecución (Windows & Linux)

Dado que el software hace inyección de paquetes crudos (RAW Sockets) en la capa de enlace de datos, la ejecución varía e impone ciertas dependencias de sistema dependiendo del Sistema Operativo.

#### Para Sistemas Unix (Kali Linux, Ubuntu, Debian)

En Linux, la captura de paquetes a bajo nivel se administra a través de la librería C `libpcap`. Debes tener las utilidades de desarrollo instaladas en tu sistema:

1.  **Instalar dependencias del S.O.:**
    Abre tu terminal y ejecuta:
    ```bash
    sudo apt-get update
    sudo apt-get install -y tcpdump libpcap-dev
    ```
2.  **Ejecutar el programa con privilegios:** 
    Los Sockets Crudos requieren, innegociablemente, permisos de superusuario. Para que tu aplicación escanee la red real, arráncala con `sudo`:
    ```bash
    sudo python3 run_web.py
    ```

#### Para Microsoft Windows

Windows no posee capacidades de Sockets Crudos habilitadas por defecto para software de terceros de esta manera. `scapy` requiere del motor `Npcap` para capturar e inyectar el tráfico:

1.  **Instalar Npcap:**
    Descarga e instala la última versión estable del controlador oficial Npcap desde su página web: [https://npcap.com/](https://npcap.com/). Se recomienda dejar las opciones de instalación por defecto.
2.  **Ejecutar el programa con privilegios:**
    Abre el Símbolo del Sistema (CMD) o una ventana de PowerShell **ejecutándolos como Administrador**. Luego sitúate en la carpeta y escribe:
    ```powershell
    python run_web.py
    ```

---
#### 💡 Fallback / Modo Demostración
Si el proyecto se ejecuta simplemente como `python3 run_web.py` (sin permisos de Administrador ni `sudo`), no colapsará. Automáticamente pasará a operar en un entorno simulado para propósitos de demostración y prototipado visual en la interfaz de la aplicación web.

Una vez iniciada la app (ya sea en modo Demo o Administrador), abre tu navegador y accede a: **`http://127.0.0.1:5000`** para comenzar.

---

<div align="center"><br><br></div>

## 🇬🇧 English

Built with Python and Flask in the backend, it uses `scapy` for low-level network packet capture and analysis.

### 🚀 Main Features

*   **Active Network Scanning:** Uses ARP requests (`scapy`) to discover active devices on the local network.
*   **Device Identification:** Resolves MAC addresses to manufacturers (OUI lookup) to intelligently guess the device type (mobile, server, TV, router, PC).
*   **Dynamic Topology:** Generates an interactive real-time network graph on the web interface.
*   **Network Optimization:** Calculates the Minimum Spanning Tree and the Shortest Path using the mathematical library `networkx`.
*   **Automatic Demonstration Mode:** If administrator privileges are not detected, the system performs a simulation generating virtual devices. This ensures the web interface can be tested and visualized without errors or crashes due to lack of permissions.
*   **Port Scanning:** Additional manual tool to check common open ports on specific devices.

---

### ⚙️ How does the System work?

The system is divided into two main layers:

1.  **Backend (Python + Flask):** Acts as the system engine. It exposes a lightweight web server and a RESTful API. When the user requests a scan, the backend calls the `scapy` routines to inject ARP packets into the network, listens for responses, and processes the resulting IPs and MAC addresses. It also maintains the topology state in memory using the `networkx` library.
2.  **Frontend (HTML + JS):** An intuitive and modern interface that consumes the `/api/*` routes. It receives the list of calculated nodes and connections and draws them graphically. It allows users to interact, perform new scans, or apply optimization algorithms graphically.

---

### 🛠️ Architecture and How to Develop

The project follows the **Separation of Concerns (SoC)** design pattern, ensuring that the mathematical and network logic is completely independent of the graphical interface.

The file structure (Professional Modular Architecture) is:

*   **`network_optimizer/`:** Main source code package.
    *   **`core/`:** Business logic (UI independent).
        *   `graph.py`: Defines the base network structure (`NetworkGraph`).
        *   `algorithms.py`: Pure mathematical implementations (Kruskal, Dijkstra, TSP).
        *   `scanner.py`: Isolates low-level logic (ARP requests from `scapy`, port scanning, MAC resolution).
    *   **`web/`:** Web Presentation Layer.
        *   `server.py`: Acts as an API controller using Flask.
        *   `templates/` and `static/`: HTML, CSS, and JS frontend files.
    *   **`gui/`:** Desktop Presentation Layer.
        *   `desktop_app.py`: Interactive graphical interface using Tkinter and Matplotlib.
*   **`run_web.py`:** Main entry point to start the web environment.
*   **`run_gui.py`:** Entry point to start the desktop tool.

**Recommended Development Workflow:**
1.  Apply your logic changes in the corresponding `network_optimizer/` folder.
2.  Flask starts by default in `debug mode`, automatically restarting when saving any changes to the files (Hot Reloading).
3.  You can develop the frontend (HTML/CSS/JS) without needing to be root by taking advantage of the smart "Demonstration Mode" of the scan.
4.  If you change the packet logic (`scapy`), test the system by running the application with full privileges.

---

### 📦 Required Dependencies

The system uses modern Python packages. The exact dependencies are listed in the `requirements.txt` file.

*   **[Flask](https://flask.palletsprojects.com/):** Lightweight web framework used to host the RESTful API and serve the HTML interface.
*   **[Scapy](https://scapy.net/):** Interactive packet manipulation program. It is the core engine for sending ARP requests to the network layer.
*   **[NetworkX](https://networkx.org/):** Specialized library for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.
*   **[Matplotlib](https://matplotlib.org/):** Used exclusively by the desktop interface (`gui`) to render the network map canvas.
*   **[Requests](https://requests.readthedocs.io/):** For HTTP calls to external APIs (e.g., OUI Lookup if expanded in the future).

---

### 📥 Step-by-Step Installation Guide

We highly recommend using a **virtual environment** to avoid conflicts with other Python libraries on your system. Follow these steps in your terminal:

1. **Clone the repository** and enter the folder:
   ```bash
   git clone <your-repository>
   cd "6 - Analisisdeted"
   ```

2. **Create a virtual environment** (optional but highly recommended):
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**:
   * **On Windows (CMD or PowerShell):**
     ```powershell
     .\venv\Scripts\activate
     ```
   * **On Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```

4. **Install ALL dependencies at once:**
   Run the following master command to seamlessly install Flask, Scapy, NetworkX, and everything else required in one step:
   ```bash
   pip install -r requirements.txt
   ```

---

### 🖥️ Compilation and Execution (Windows & Linux)

Since the software performs raw packet injection (RAW Sockets) in the data link layer, execution varies and imposes certain underlying system dependencies depending on the Operating System.

#### For Unix Systems (Kali Linux, Ubuntu, Debian)

In Linux, low-level packet capture is managed through the C library `libpcap`. You must have the development utilities installed on your system:

1.  **Install OS dependencies:**
    Open your terminal and run:
    ```bash
    sudo apt-get update
    sudo apt-get install -y tcpdump libpcap-dev
    ```
2.  **Run the program with privileges:** 
    Raw Sockets strictly require superuser permissions. For your application to scan the real network, start it with `sudo`:
    ```bash
    sudo python3 run_web.py
    ```

#### For Microsoft Windows

Windows does not have Raw Sockets capabilities enabled by default for third-party software in this way. `scapy` requires the `Npcap` engine to capture and inject traffic:

1.  **Install Npcap:**
    Download and install the latest stable version of the official Npcap driver from its website: [https://npcap.com/](https://npcap.com/). It is recommended to leave the default installation options.
2.  **Run the program with privileges:**
    Open the Command Prompt (CMD) or a PowerShell window **running them as Administrator**. Then navigate to the folder and type:
    ```powershell
    python run_web.py
    ```

---
#### 💡 Fallback / Demonstration Mode
If the project is simply executed as `python3 run_web.py` (without Administrator permissions or `sudo`), it will not crash. It will automatically switch to operate in a simulated environment for demonstration purposes and visual prototyping in the web application interface.

Once the app has started (either in Demo or Administrator mode), open your browser and access: **`http://127.0.0.1:5000`** to start.
