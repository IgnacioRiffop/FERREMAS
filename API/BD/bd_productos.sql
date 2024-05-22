DROP TABLE producto CASCADE CONSTRAINTS;
DROP TABLE marca CASCADE CONSTRAINTS;

CREATE TABLE producto(
    id_producto NUMBER PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    id_marca NUMBER NOT NULL,
    precio NUMBER NOT NULL,
    stock NUMBER NOT NULL,
    imagen VARCHAR2(255)
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
INSERT INTO producto VALUES(1,'Martillo',1,1990,17,'martillo.jpg');
INSERT INTO producto VALUES(2,'LLave',1,990,12,'llave.jpg');
INSERT INTO producto VALUES(3,'Taladro Percutor',1,21990,6,'taladro.jpg');
INSERT INTO producto VALUES(4,'Caja de Herramientas',1,14990,5,'caja.jpg');
INSERT INTO producto VALUES(7,'Pala Punta Huevo',1,5990,9,'pala.jpg');
INSERT INTO producto VALUES(8,'Sierra Circular',1,18990,13,'sierra.jpg');
INSERT INTO producto VALUES(10,'Escuadra Carpintero',1,1290,20,'escuadra.jpg');
INSERT INTO producto VALUES(11,'LLave Punta Corona',1,890,10,'llavepc.jpg');
INSERT INTO producto VALUES(12,'Atornillador',1,1590,19,'atornillador.jpg');
INSERT INTO producto VALUES(9,'Set de brocas',1,7990,2,'brocas.jpg');
INSERT INTO producto VALUES(5,'Escalera',1,12990,11,'escalera.png');
INSERT INTO producto VALUES(6,'Esmeril Angular',1,16990,21,'esmeril.jpg');


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
                           p.stock,
                           p.imagen
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
                           p.stock,
                           p.imagen
                      FROM producto p
                      WHERE p.id_producto = p_id;
    p_out := 1;
    
    EXCEPTION
    WHEN OTHERS THEN
        p_out := 0;
END sp_get_producto;
/
CREATE OR REPLACE PROCEDURE sp_post_producto(p_id NUMBER, p_nombre VARCHAR2, p_id_marca NUMBER,
                                           p_precio NUMBER, p_stock NUMBER, p_imagen VARCHAR2,
                                          p_out OUT NUMBER)
IS
BEGIN
    INSERT INTO producto VALUES(p_id, p_nombre, p_id_marca, p_precio, p_stock, p_imagen);
    p_out := 1;
    
    EXCEPTION
    WHEN OTHERS THEN
        p_out := 0;
END sp_post_producto;
/
CREATE OR REPLACE PROCEDURE sp_put_producto(p_id NUMBER, p_nombre VARCHAR2, p_id_marca NUMBER,
                                         p_precio NUMBER, p_stock NUMBER, p_imagen VARCHAR2,
                                         p_out OUT NUMBER)
IS
BEGIN
    UPDATE producto
    SET nombre = p_nombre,
        id_marca = p_id_marca,
        precio = p_precio,
        stock = p_stock,
        imagen = p_imagen
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
                                          p_precio NUMBER, p_stock NUMBER, p_imagen VARCHAR2,
                                          p_out OUT NUMBER)
IS
BEGIN
    INSERT INTO producto VALUES(p_id, p_nombre, p_id_marca, p_precio, p_stock, p_imagen);
    p_out := 1;
    
    EXCEPTION
    WHEN DUP_VAL_ON_INDEX THEN
        UPDATE producto
        SET nombre = p_nombre,
            id_marca = p_id_marca,
            precio = p_precio,
            stock = p_stock,
            imagen = p_imagen
        WHERE id_producto = p_id;
        p_out := 1;
    WHEN OTHERS THEN
        p_out := 0;
END sp_patch_producto;
/
COMMIT;