# Urban Flow Apparel - E-Commerce Backend 🛒🔥

Una plataforma de comercio electrónico moderna, rápida y escalable. Este proyecto implementa un CRUD completo de productos utilizando una arquitectura desacoplada donde Django actúa como motor de enrutamiento y renderizado, interactuando directamente con una base de datos NoSQL en tiempo real en la nube.

## 🚀 Tecnologías Utilizadas

* **Backend:** Python 3, Django (Enrutamiento y Vistas)
* **Base de Datos:** Firebase Firestore (NoSQL)
* **Almacenamiento:** Firebase Storage (Gestión de imágenes en la nube)
* **Frontend:** HTML5, Tailwind CSS (CDN)

## ⚙️ Arquitectura del Proyecto

El sistema omite el ORM tradicional relacional de Django en favor del Firebase Admin SDK. Esto permite:
* Lectura y escritura en tiempo real.
* Almacenamiento directo de assets en Buckets de Google Cloud.
* Interfaces de usuario limpias y responsivas inyectadas desde el servidor.

## 🛠️ Instalación y Configuración Local

Sigue estos pasos para ejecutar el proyecto en tu máquina local:

**1. Clonar el repositorio:**
\`\`\`bash
git clone https://github.com/TU-USUARIO/urban-flow-ecommerce.git
cd urban-flow-ecommerce
\`\`\`

**2. Crear y activar el entorno virtual:**
\`\`\`bash
# Windows
python -m venv venv -
venv\Scripts\activate


**3. Instalar dependencias:**
\`\`\`bash
pip install django firebase-admin requests
\`\`\`

**4. Configurar Credenciales de Firebase:**
* Genera una clave privada desde la Consola de Firebase (Cuentas de Servicio).
* Renombra el archivo a `firebase-key.json`.
* Colócalo en la raíz del proyecto (al mismo nivel que `manage.py`).
* *Nota: Este archivo está en el `.gitignore` por seguridad y no debe ser subido al repositorio.*

**5. Ejecutar el servidor de desarrollo:**
\`\`\`bash
python manage.py runserver
\`\`\`

Visita `http://127.0.0.1:8000/` en tu navegador para ver la aplicación.