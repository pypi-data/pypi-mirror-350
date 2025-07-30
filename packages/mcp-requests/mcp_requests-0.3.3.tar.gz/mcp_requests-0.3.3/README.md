LIMPIO

Un servidor MCP (Model Context Protocol) que proporciona herramientas para realizar peticiones HTTP de manera segura y eficiente.

## 🚀 Características

- ✅ Soporte completo para métodos HTTP: GET, POST, PUT, DELETE
- ✅ Manejo robusto de errores y timeouts configurables
- ✅ Soporte para headers personalizados y parámetros de consulta
- ✅ Capacidad para enviar datos JSON y form-data
- ✅ Logging contextual integrado
- ✅ Manejo seguro de contenido binario
- ✅ Validación de parámetros con Pydantic

## 📦 Instalación

### Desde PyPI (próximamente)
```

### `http_put`
Realiza peticiones HTTP PUT.

**Parámetros:** (Igual que `http_post`)

**Ejemplo:**
```python
result = await http_put(
    url="https://api.ejemplo.com/actualizar/123",
    json={"nombre": "Nuevo nombre"}
)
```

### `http_delete`
Realiza peticiones HTTP DELETE.

**Parámetros:**
- `url` (str): URL de destino
- `params` (dict, opcional): Parámetros de consulta
- `headers` (dict, opcional): Headers HTTP personalizados
- `timeout` (int, opcional): Timeout en segundos (1-60, default: 30)

**Ejemplo:**
```python
result = await http_delete(
    url="https://api.ejemplo.com/eliminar/123",
    headers={"Authorization": "Bearer token"}
)
```

## 📊 Formato de Respuesta

Todas las herramientas devuelven un diccionario con la siguiente estructura:

```python
{
    "status_code": 200,                    # Código de estado HTTP
    "headers": {                           # Headers de respuesta
        "content-type": "application/json",
        "content-length": "150"
    },
    "content": "...",                      # Contenido de la respuesta
    "elapsed_time": 0.234                  # Tiempo de respuesta en segundos
}
```

**Notas sobre el contenido:**
- Para contenido de texto: se devuelve como string
- Para contenido binario: se muestra como `"[Contenido binario no mostrable]"`

## ⚠️ Manejo de Errores

El servidor maneja los siguientes tipos de errores:

- **Timeout**: Cuando la petición excede el tiempo límite
- **Conexión**: Cuando no se puede conectar al servidor
- **HTTP**: Errores de estado HTTP (4xx, 5xx)
- **Formato**: Cuando el contenido no se puede procesar

Todos los errores se capturan y se reportan con mensajes descriptivos.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENCE` para detalles.

## 👨‍💻 Autor

**Alejandro Cuartas**
- Email: alejandro.cuartas@yahoo.com
- GitHub: [@alejandrocuartas](https://github.com/alejandrocuartas)

---

⭐ Si este proyecto te es útil, no olvides darle una estrella en GitHub!bash
