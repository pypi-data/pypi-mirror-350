from fastmcp import FastMCP, Context
import requests
from typing import Dict, Any, Optional, Annotated
from pydantic import Field

# Crear un servidor FastMCP
mcp = FastMCP(name="RequestsServer")

@mcp.tool()
async def http_get(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: Annotated[int, Field(description="Timeout in seconds", ge=1, le=60)] = 30,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Realiza una petición HTTP GET a la URL especificada.
    
    Args:
        url: La URL a la que hacer la petición
        params: Parámetros opcionales de la consulta (query parameters)
        headers: Headers HTTP opcionales
        timeout: Tiempo máximo de espera en segundos
    
    Returns:
        Un diccionario con 'status_code', 'headers', 'content' y 'elapsed_time'
    """
    if ctx:
        await ctx.info(f"Realizando GET a {url}")
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        
        # Intentamos convertir el contenido a texto, si no es posible devolvemos un mensaje
        try:
            content = response.text
        except:
            content = "[Contenido binario no mostrable]"
        
        result = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content": content,
            "elapsed_time": response.elapsed.total_seconds()
        }
        
        if ctx:
            await ctx.info(f"GET completado: status {response.status_code}")
        
        return result
    
    except Exception as e:
        if ctx:
            await ctx.error(f"Error en GET: {str(e)}")
        raise Exception(f"Error realizando la petición GET: {str(e)}")

@mcp.tool()
async def http_post(
    url: str,
    data: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: Annotated[int, Field(description="Timeout in seconds", ge=1, le=60)] = 30,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Realiza una petición HTTP POST a la URL especificada.
    
    Args:
        url: La URL a la que hacer la petición
        data: Datos a enviar en el cuerpo (form data)
        json: Datos JSON a enviar en el cuerpo
        params: Parámetros opcionales de la consulta (query parameters)
        headers: Headers HTTP opcionales
        timeout: Tiempo máximo de espera en segundos
    
    Returns:
        Un diccionario con 'status_code', 'headers', 'content' y 'elapsed_time'
    """
    if ctx:
        await ctx.info(f"Realizando POST a {url}")
    
    try:
        response = requests.post(
            url, 
            data=data, 
            json=json, 
            params=params, 
            headers=headers, 
            timeout=timeout
        )
        
        # Intentamos convertir el contenido a texto, si no es posible devolvemos un mensaje
        try:
            content = response.text
        except:
            content = "[Contenido binario no mostrable]"
        
        result = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content": content,
            "elapsed_time": response.elapsed.total_seconds()
        }
        
        if ctx:
            await ctx.info(f"POST completado: status {response.status_code}")
        
        return result
    
    except Exception as e:
        if ctx:
            await ctx.error(f"Error en POST: {str(e)}")
        raise Exception(f"Error realizando la petición POST: {str(e)}")

@mcp.tool()
async def http_put(
    url: str,
    data: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: Annotated[int, Field(description="Timeout in seconds", ge=1, le=60)] = 30,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Realiza una petición HTTP PUT a la URL especificada.
    
    Args:
        url: La URL a la que hacer la petición
        data: Datos a enviar en el cuerpo (form data)
        json: Datos JSON a enviar en el cuerpo
        params: Parámetros opcionales de la consulta (query parameters)
        headers: Headers HTTP opcionales
        timeout: Tiempo máximo de espera en segundos
    
    Returns:
        Un diccionario con 'status_code', 'headers', 'content' y 'elapsed_time'
    """
    if ctx:
        await ctx.info(f"Realizando PUT a {url}")
    
    try:
        response = requests.put(
            url, 
            data=data, 
            json=json, 
            params=params, 
            headers=headers, 
            timeout=timeout
        )
        
        # Intentamos convertir el contenido a texto, si no es posible devolvemos un mensaje
        try:
            content = response.text
        except:
            content = "[Contenido binario no mostrable]"
        
        result = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content": content,
            "elapsed_time": response.elapsed.total_seconds()
        }
        
        if ctx:
            await ctx.info(f"PUT completado: status {response.status_code}")
        
        return result
    
    except Exception as e:
        if ctx:
            await ctx.error(f"Error en PUT: {str(e)}")
        raise Exception(f"Error realizando la petición PUT: {str(e)}")

@mcp.tool()
async def http_delete(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: Annotated[int, Field(description="Timeout in seconds", ge=1, le=60)] = 30,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Realiza una petición HTTP DELETE a la URL especificada.
    
    Args:
        url: La URL a la que hacer la petición
        params: Parámetros opcionales de la consulta (query parameters)
        headers: Headers HTTP opcionales
        timeout: Tiempo máximo de espera en segundos
    
    Returns:
        Un diccionario con 'status_code', 'headers', 'content' y 'elapsed_time'
    """
    if ctx:
        await ctx.info(f"Realizando DELETE a {url}")
    
    try:
        response = requests.delete(url, params=params, headers=headers, timeout=timeout)
        
        # Intentamos convertir el contenido a texto, si no es posible devolvemos un mensaje
        try:
            content = response.text
        except:
            content = "[Contenido binario no mostrable]"
        
        result = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content": content,
            "elapsed_time": response.elapsed.total_seconds()
        }
        
        if ctx:
            await ctx.info(f"DELETE completado: status {response.status_code}")
        
        return result
    
    except Exception as e:
        if ctx:
            await ctx.error(f"Error en DELETE: {str(e)}")
        raise Exception(f"Error realizando la petición DELETE: {str(e)}")

# Punto de entrada para ejecutar el servidor
if __name__ == "__main__":
    mcp.run()