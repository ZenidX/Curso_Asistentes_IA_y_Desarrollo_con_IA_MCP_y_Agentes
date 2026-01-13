# Firebase MCP

## Información

| | |
|---|---|
| **Duración** | 30 minutos |
| **Nivel** | Intermedio |
| **Requisitos** | Proyecto Firebase, Service Account Key |
| **Tipo de BD** | NoSQL (Firestore) |

---

## Objetivos de Aprendizaje

Al completar esta sección podrás:

- [ ] Generar y configurar Service Account Key
- [ ] Gestionar usuarios con Authentication
- [ ] Crear y consultar documentos en Firestore
- [ ] Subir y descargar archivos de Storage
- [ ] Diseñar estructura de datos para Firestore

---

Firebase ofrece un **backend completo sin servidor**:
- Autenticación de usuarios
- Base de datos en tiempo real (Firestore)
- Almacenamiento de archivos
- Hosting

---

## Configuración

```json
{
  "mcpServers": {
    "firebase": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/firebase-mcp"],
      "env": {
        "SERVICE_ACCOUNT_KEY_PATH": "/path/to/serviceAccountKey.json",
        "FIREBASE_STORAGE_BUCKET": "tu-proyecto.firebasestorage.app"
      }
    }
  }
}
```

---

## Obtener Service Account Key

1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Selecciona tu proyecto (o crea uno nuevo)
3. Settings (engranaje) → Service Accounts
4. Click en "Generate New Private Key"
5. Guarda el archivo JSON en ubicación segura
6. Actualiza `SERVICE_ACCOUNT_KEY_PATH`

> ⚠️ **NUNCA** commits el archivo `serviceAccountKey.json`. Añádelo a `.gitignore`.

---

## Tools Disponibles

### Authentication

| Tool | Función | Ejemplo |
|------|---------|---------|
| `auth_get_user` | Obtener usuario por UID | Verificar si existe |
| `auth_get_user_by_email` | Obtener usuario por email | Buscar usuario |
| `auth_list_users` | Listar usuarios | Ver todos |
| `auth_create_user` | Crear usuario | Registrar nuevo |
| `auth_update_user` | Actualizar usuario | Cambiar datos |
| `auth_delete_user` | Eliminar usuario | Dar de baja |

### Firestore

| Tool | Función | Ejemplo |
|------|---------|---------|
| `firestore_add_document` | Crear documento | Crear nueva tarea |
| `firestore_get_document` | Obtener documento | Leer tarea |
| `firestore_update_document` | Actualizar documento | Marcar completada |
| `firestore_delete_document` | Eliminar documento | Borrar tarea |
| `firestore_query` | Consultar colección | Buscar por estado |
| `firestore_list_collections` | Listar colecciones | Ver estructura |

### Storage

| Tool | Función | Ejemplo |
|------|---------|---------|
| `storage_list_files` | Listar archivos | Ver adjuntos |
| `storage_upload` | Subir archivo | Adjuntar documento |
| `storage_download` | Descargar archivo | Obtener adjunto |
| `storage_delete` | Eliminar archivo | Borrar adjunto |
| `storage_get_metadata` | Obtener metadata | Ver tamaño y tipo |

---

## Ejemplo Completo para TaskFlow

```
Usuario: "Crea un usuario para pruebas"
Claude: auth_create_user(email="test@taskflow.com", password="...")

Usuario: "Guarda una tarea en Firestore"
Claude: firestore_add_document(
  collection="tareas",
  data={
    titulo: "Completar módulo MCP",
    estado: "pendiente",
    prioridad: "alta",
    asignado_a: "test@taskflow.com"
  }
)

Usuario: "Busca tareas de alta prioridad"
Claude: firestore_query(
  collection="tareas",
  where=[["prioridad", "==", "alta"]]
)
```

---

## Estructura de datos recomendada

```
firestore/
├── usuarios/
│   └── {userId}/
│       ├── email
│       ├── nombre
│       └── preferencias
├── proyectos/
│   └── {projectId}/
│       ├── nombre
│       ├── owner
│       └── miembros[]
└── tareas/
    └── {taskId}/
        ├── titulo
        ├── descripcion
        ├── estado
        ├── proyecto_id
        └── asignado_a
```

---

## 📍 Checkpoint

Verifica que puedes:
- [ ] Generar Service Account Key desde Firebase Console
- [ ] Configurar el MCP con la ruta correcta al archivo JSON
- [ ] Crear un documento en Firestore desde Claude
- [ ] Listar usuarios de Authentication

---

## Resumen

| Aspecto | Firebase MCP |
|---------|--------------|
| **Mejor para** | Apps móviles/web con backend completo |
| **Ventaja clave** | Ecosistema integrado (Auth + DB + Storage) |
| **Precaución** | NUNCA commitear serviceAccountKey.json |
| **Tipo de BD** | NoSQL (Firestore) - documentos anidados |

---

## Recursos

- [Firebase Console](https://console.firebase.google.com/)
- [Firestore Documentation](https://firebase.google.com/docs/firestore)
- [Firebase Auth](https://firebase.google.com/docs/auth)
