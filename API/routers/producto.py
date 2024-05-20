from fastapi import APIRouter, HTTPException
from models.producto import Producto

#Vamos a conectar con oracle:
import oracledb
cone = oracledb.connect(user="ferremas_db",
                        password="ferremas_db",
                        host="127.0.0.1",
                        port=1521,
                        service_name="orcl")

router = APIRouter()

@router.get("/productos")
async def get_productos():
    try:
        cursor = cone.cursor() #conexión con oracle
        out = cursor.var(int) #variable numérica 0-1
        cursor_productos = cursor.var(oracledb.CURSOR) #variable sys_refcursor: select...
        cursor.callproc("SP_GET_PRODUCTOS", [cursor_productos,out]) #ejecuta el procedimiento
        if out.getvalue() == 1:
            lista = []
            for fila in cursor_productos.getvalue():
                json = {}
                json['id_producto'] = fila[0]
                json['nombre'] = fila[1]
                json['id_marca'] = fila[2]
                json['nombre_marca'] = fila[3]
                json['precio'] = fila[4]
                json['stock'] = fila[5]
                json['imagen'] = fila[6]
                lista.append(json)
            return lista
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()


@router.get("/productos/{id_producto}")
async def get_producto(id_producto:int):
    try:
        cursor = cone.cursor() #conexión con oracle
        out = cursor.var(int) #variable numérica 0-1
        cursor_productos = cursor.var(oracledb.CURSOR) #variable sys_refcursor: select...
        cursor.callproc("SP_GET_PRODUCTOS", [cursor_productos,out])
        if out.getvalue() == 1:
            json = {}
            for fila in cursor_productos.getvalue():
                if id_producto==fila[0]:
                    json['id_producto'] = fila[0]
                    json['nombre'] = fila[1]
                    json['id_marca'] = fila[2]
                    json['nombre_marca'] = fila[3]
                    json['precio'] = fila[4]
                    json['stock'] = fila[5]
                    json['imagen'] = fila[6]
                    break
            return json
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()


@router.post("/productos")
async def post_producto(producto: Producto):
    try:
        cursor = cone.cursor()
        out = cursor.var(int)
        cursor.callproc("SP_POST_PRODUCTO", [producto.id_producto,
                                          producto.nombre,
                                          producto.id_marca,
                                          producto.precio,
                                          producto.stock,
                                          producto.imagen,
                                          out])
        if out.getvalue()==1:
            cone.commit()
            return producto
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()


@router.put("/productos/{id_producto}")
async def put_producto(id_producto:int, producto:Producto):
    try:
        cursor = cone.cursor()
        out = cursor.var(int)
        cursor.callproc("SP_PUT_PRODUCTO", [id_producto,
                                          producto.nombre,
                                          producto.id_marca,
                                          producto.precio,
                                          producto.stock,
                                          producto.imagen,
                                          out])
        if out.getvalue()==1:
            cone.commit()
            return producto
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@router.delete("/productos/{id_producto}")
async def delete_producto(id_producto:int):
    try:
        cursor = cone.cursor()
        out = cursor.var(int)
        cursor.callproc("SP_DELETE_PRODUCTO", [id_producto, out])
        if out.getvalue()==1:
            cone.commit()
            return {"mensaje": "producto eliminado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()


@router.patch("/productos/{id_producto}")
async def patch_producto(id_producto:int, producto:Producto):
    try:
        cursor = cone.cursor()
        out = cursor.var(int)
        cursor.callproc("SP_PATCH_PRODUCTO", [id_producto,
                                          producto.nombre,
                                          producto.id_marca,
                                          producto.precio,
                                          producto.stock,
                                          producto.imagen,
                                          out])
        if out.getvalue()==1:
            cone.commit()
            return producto
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
