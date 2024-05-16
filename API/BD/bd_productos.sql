DROP TABLE producto CASCADE CONSTRAINTS;
DROP TABLE marca CASCADE CONSTRAINTS;

CREATE TABLE producto(
    id_producto NUMBER PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    id_marca NUMBER NOT NULL,
    precio NUMBER NOT NULL,
    stock NUMBER NOT NULL
);

CREATE TABLE marca(
    id_marca NUMBER PRIMARY KEY,
    nombre_marca VARCHAR2(60) NOT NULL
);

ALTER TABLE producto ADD(
     CONSTRAINT fk_marca_libro FOREIGN KEY (id_marca) REFERENCES marca(id_marca)
);

--marcas de libros:
INSERT INTO marca VALUES(1,'Bosch');

--insertar 3 libros:
INSERT INTO producto VALUES(1,'martillo',1,30000,100);
INSERT INTO producto VALUES(2,'llave',1,20000,12);
INSERT INTO producto VALUES(3,'taladro',1,30000,30);

COMMIT;
/
--PROCEDIMIENTOS ALMACENADOS PARA EL CONSUMO DE MI API:
CREATE OR REPLACE PROCEDURE sp_get_productos(p_cursor OUT SYS_REFCURSOR, p_out OUT NUMBER)
IS
BEGIN
    OPEN p_cursor FOR SELECT p.id_producto,
                           p.nombre,
                           p.id_marca,
                           (SELECT nombre_marca FROM marca m WHERE p.id_marca = m.id_marca) AS marca,
                           p.precio,
                           p.stock
                      FROM producto p;
    p_out := 1;
    
    EXCEPTION
    WHEN OTHERS THEN
        p_out := 0;
END sp_get_productos;
/
CREATE OR REPLACE PROCEDURE sp_get_producto(p_id NUMBER,p_cursor OUT SYS_REFCURSOR, p_out OUT NUMBER)
IS
BEGIN
    OPEN p_cursor FOR SELECT p.id_producto,
                           p.nombre,
                           p.id_marca,
                           (SELECT nombre_marca FROM marca m WHERE p.id_marca = m.id_marca) AS marca,
                           p.precio,
                           p.stock
                      FROM producto p
                      WHERE p.id_producto = p_id;
    p_out := 1;
    
    EXCEPTION
    WHEN OTHERS THEN
        p_out := 0;
END sp_get_producto;
/
CREATE OR REPLACE PROCEDURE sp_post_producto(p_id NUMBER, p_nombre VARCHAR2, p_id_marca NUMBER,
                                           p_precio NUMBER, p_stock NUMBER,
                                          p_out OUT NUMBER)
IS
BEGIN
    INSERT INTO producto VALUES(p_id, p_nombre, p_id_marca, p_precio, p_stock);
    p_out := 1;
    
    EXCEPTION
    WHEN OTHERS THEN
        p_out := 0;
END sp_post_producto;
/
CREATE OR REPLACE PROCEDURE sp_put_producto(p_id NUMBER, p_nombre VARCHAR2, p_id_marca NUMBER,
                                         p_precio NUMBER, p_stock NUMBER,
                                         p_out OUT NUMBER)
IS
BEGIN
    UPDATE producto
    SET nombre = p_nombre,
        id_marca = p_id_marca,
        precio = p_precio,
        stock = p_stock
    WHERE id_producto = p_id;
    p_out := 1;
    
    EXCEPTION
    WHEN OTHERS THEN
        p_out := 0;
END sp_put_producto;
/
CREATE OR REPLACE PROCEDURE sp_delete_producto(p_id NUMBER, p_out OUT NUMBER)
IS
BEGIN
    DELETE FROM producto
    WHERE id_producto = p_id;
    p_out := 1;
    
    EXCEPTION
    WHEN OTHERS THEN
        p_out := 0;
END sp_delete_producto;
/
CREATE OR REPLACE PROCEDURE sp_patch_producto(p_id NUMBER, p_nombre VARCHAR2, p_id_marca NUMBER,
                                          p_precio NUMBER, p_stock NUMBER,
                                          p_out OUT NUMBER)
IS
BEGIN
    INSERT INTO producto VALUES(p_id, p_nombre, p_id_marca, p_precio, p_stock);
    p_out := 1;
    
    EXCEPTION
    WHEN DUP_VAL_ON_INDEX THEN
        UPDATE producto
        SET nombre = p_nombre,
            id_marca = p_id_marca,
            precio = p_precio,
            stock = p_stock
        WHERE id_producto = p_id;
        p_out := 1;
    WHEN OTHERS THEN
        p_out := 0;
END sp_patch_producto;
/
COMMIT;