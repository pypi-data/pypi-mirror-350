from fastmcp import FastMCP, Context
import requests
import json
from typing import Dict, Any, Optional, Annotated, Union
from pydantic import Field

# Crear un servidor FastMCP
mcp = FastMCP(name="RequestsServer")

def parse_json_if_string(data):
    """Convierte string JSON a dict si es necesario"""
    if isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return data
    return data

@mcp.tool()
async def http_get(
    url: str,
    ctx: Context,
    params: Annotated[
        Optional[Union[Dict[str, Any], str]], 
        Field(description="Parámetros de consulta (JSON string o dict)")
    ] = None,
    headers: Annotated[
        Optional[Union[Dict[str, str], str]], 
        Field(description="Headers HTTP (JSON string o dict)")
    ] = None,
    timeout: Annotated[int, Field(description="Timeout en segundos", ge=1, le=60)] = 30
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
    await ctx.info(f"Realizando GET a {url}")
    
    try:
        # Convertir strings JSON a diccionarios si es necesario
        if params is not None:
            params = parse_json_if_string(params)
            
        if headers is not None:
            headers = parse_json_if_string(headers)
        
        await ctx.debug(f"Parámetros: {params}")
        await ctx.debug(f"Headers: {headers}")
        
        response = requests.get(
            url, 
            params=params, 
            headers=headers, 
            timeout=timeout
        )
        
        # Intentamos convertir el contenido a texto
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
        
        await ctx.info(f"GET completado: status {response.status_code}")
        return result
    
    except Exception as e:
        await ctx.error(f"Error en GET: {str(e)}")
        raise Exception(f"Error realizando la petición GET: {str(e)}")

@mcp.tool()
async def http_post(
    url: str,
    ctx: Context,
    data: Annotated[
        Optional[Union[Dict[str, Any], str]], 
        Field(description="Datos para enviar como form data (JSON string o dict)")
    ] = None,
    json_data: Annotated[
        Optional[Union[Dict[str, Any], str]], 
        Field(description="Datos para enviar como JSON (JSON string o dict)")
    ] = None,
    params: Annotated[
        Optional[Union[Dict[str, Any], str]], 
        Field(description="Parámetros de consulta (JSON string o dict)")
    ] = None,
    headers: Annotated[
        Optional[Union[Dict[str, str], str]], 
        Field(description="Headers HTTP (JSON string o dict)")
    ] = None,
    timeout: Annotated[int, Field(description="Timeout en segundos", ge=1, le=60)] = 30
) -> Dict[str, Any]:
    """
    Realiza una petición HTTP POST a la URL especificada.
    
    Args:
        url: La URL a la que hacer la petición
        data: Datos a enviar en el cuerpo (form data)
        json_data: Datos JSON a enviar en el cuerpo
        params: Parámetros opcionales de la consulta (query parameters)
        headers: Headers HTTP opcionales
        timeout: Tiempo máximo de espera en segundos
    
    Returns:
        Un diccionario con 'status_code', 'headers', 'content' y 'elapsed_time'
    """
    await ctx.info(f"Realizando POST a {url}")
    
    try:
        # Convertir strings JSON a diccionarios si es necesario
        if data is not None:
            data = parse_json_if_string(data)
            
        if json_data is not None:
            json_data = parse_json_if_string(json_data)
            
        if params is not None:
            params = parse_json_if_string(params)
            
        if headers is not None:
            headers = parse_json_if_string(headers)
        
        # Validar que solo se use uno de los parámetros de cuerpo
        if data is not None and json_data is not None:
            error_msg = "No se pueden usar 'data' y 'json_data' simultáneamente. Usa solo uno."
            await ctx.error(error_msg)
            raise ValueError(error_msg)
        
        await ctx.debug(f"Data: {data}")
        await ctx.debug(f"JSON data: {json_data}")
        await ctx.debug(f"Parámetros: {params}")
        await ctx.debug(f"Headers: {headers}")
        
        # Realizar la petición según el tipo de datos
        if json_data is not None:
            await ctx.info(f"Enviando datos JSON")
            response = requests.post(
                url, 
                json=json_data,
                params=params, 
                headers=headers, 
                timeout=timeout
            )
        elif data is not None:
            await ctx.info(f"Enviando datos form")
            response = requests.post(
                url, 
                data=data,
                params=params, 
                headers=headers, 
                timeout=timeout
            )
        else:
            await ctx.info("Enviando POST sin cuerpo")
            response = requests.post(
                url,
                params=params, 
                headers=headers, 
                timeout=timeout
            )
        
        # Procesar respuesta
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
        
        await ctx.info(f"POST completado: status {response.status_code}")
        return result
    
    except Exception as e:
        await ctx.error(f"Error en POST: {str(e)}")
        raise Exception(f"Error realizando la petición POST: {str(e)}")

@mcp.tool()
async def http_put(
    url: str,
    ctx: Context,
    data: Annotated[
        Optional[Union[Dict[str, Any], str]], 
        Field(description="Datos para enviar como form data (JSON string o dict)")
    ] = None,
    json_data: Annotated[
        Optional[Union[Dict[str, Any], str]], 
        Field(description="Datos para enviar como JSON (JSON string o dict)")
    ] = None,
    params: Annotated[
        Optional[Union[Dict[str, Any], str]], 
        Field(description="Parámetros de consulta (JSON string o dict)")
    ] = None,
    headers: Annotated[
        Optional[Union[Dict[str, str], str]], 
        Field(description="Headers HTTP (JSON string o dict)")
    ] = None,
    timeout: Annotated[int, Field(description="Timeout en segundos", ge=1, le=60)] = 30
) -> Dict[str, Any]:
    """
    Realiza una petición HTTP PUT a la URL especificada.
    
    Args:
        url: La URL a la que hacer la petición
        data: Datos a enviar en el cuerpo (form data)
        json_data: Datos JSON a enviar en el cuerpo
        params: Parámetros opcionales de la consulta (query parameters)
        headers: Headers HTTP opcionales
        timeout: Tiempo máximo de espera en segundos
    
    Returns:
        Un diccionario con 'status_code', 'headers', 'content' y 'elapsed_time'
    """
    await ctx.info(f"Realizando PUT a {url}")
    
    try:
        # Convertir strings JSON a diccionarios si es necesario
        if data is not None:
            data = parse_json_if_string(data)
            
        if json_data is not None:
            json_data = parse_json_if_string(json_data)
            
        if params is not None:
            params = parse_json_if_string(params)
            
        if headers is not None:
            headers = parse_json_if_string(headers)
        
        # Validar que solo se use uno de los parámetros de cuerpo
        if data is not None and json_data is not None:
            error_msg = "No se pueden usar 'data' y 'json_data' simultáneamente. Usa solo uno."
            await ctx.error(error_msg)
            raise ValueError(error_msg)
        
        await ctx.debug(f"Data: {data}")
        await ctx.debug(f"JSON data: {json_data}")
        await ctx.debug(f"Parámetros: {params}")
        await ctx.debug(f"Headers: {headers}")
        
        # Realizar la petición según el tipo de datos
        if json_data is not None:
            await ctx.info(f"Enviando datos JSON")
            response = requests.put(
                url, 
                json=json_data,
                params=params, 
                headers=headers, 
                timeout=timeout
            )
        elif data is not None:
            await ctx.info(f"Enviando datos form")
            response = requests.put(
                url, 
                data=data,
                params=params, 
                headers=headers, 
                timeout=timeout
            )
        else:
            await ctx.info("Enviando PUT sin cuerpo")
            response = requests.put(
                url,
                params=params, 
                headers=headers, 
                timeout=timeout
            )
        
        # Procesar respuesta
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
        
        await ctx.info(f"PUT completado: status {response.status_code}")
        return result
    
    except Exception as e:
        await ctx.error(f"Error en PUT: {str(e)}")
        raise Exception(f"Error realizando la petición PUT: {str(e)}")

@mcp.tool()
async def http_delete(
    url: str,
    ctx: Context,
    params: Annotated[
        Optional[Union[Dict[str, Any], str]], 
        Field(description="Parámetros de consulta (JSON string o dict)")
    ] = None,
    headers: Annotated[
        Optional[Union[Dict[str, str], str]], 
        Field(description="Headers HTTP (JSON string o dict)")
    ] = None,
    timeout: Annotated[int, Field(description="Timeout en segundos", ge=1, le=60)] = 30
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
    await ctx.info(f"Realizando DELETE a {url}")
    
    try:
        # Convertir strings JSON a diccionarios si es necesario
        if params is not None:
            params = parse_json_if_string(params)
            
        if headers is not None:
            headers = parse_json_if_string(headers)
        
        await ctx.debug(f"Parámetros: {params}")
        await ctx.debug(f"Headers: {headers}")
        
        response = requests.delete(
            url, 
            params=params, 
            headers=headers, 
            timeout=timeout
        )
        
        # Procesar respuesta
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
        
        await ctx.info(f"DELETE completado: status {response.status_code}")
        return result
    
    except Exception as e:
        await ctx.error(f"Error en DELETE: {str(e)}")
        raise Exception(f"Error realizando la petición DELETE: {str(e)}")

def main():
    """Función principal para ejecutar el servidor MCP"""
    mcp.run()

# Punto de entrada para ejecutar el servidor
if __name__ == "__main__":
    main()