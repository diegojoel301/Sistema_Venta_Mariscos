CREATE TABLE PROVEEDOR(
	id_prov	INTEGER PRIMARY KEY AUTOINCREMENT,
	nombre_prov VARCHAR2(50),
	numero_telefono VARCHAR2(50),
	ubicacion VARCHAR2(50),
	email VARCHAR2(50),
	pais VARCHAR2(50)
);

CREATE TABLE PRODUCTO(
	id_prod	INTEGER PRIMARY KEY AUTOINCREMENT,
	nombre 	VARCHAR2(50),
	stock	INTEGER NOT NULL,
	descripcion	VARCHAR2(50),
	foto_prod	VARCHAR2(50),
	fecha_venc	DATETIME NOT NULL,
	precio	INTEGER NOT NULL,
	pais_fabricacion	VARCHAR2(50),
	id_prov	INTEGER NOT NULL,
	ci_director_comercial INTEGER NOT NULL,
	FOREIGN KEY (id_prov) REFERENCES PROVEEDOR(id_prov),
	FOREIGN KEY (ci_director_comercial) REFERENCES DIRECTOR_COMERCIAL(ci_director_comercial)
);

CREATE TABLE CATEGORIA(
	id_cat INTEGER PRIMARY KEY AUTOINCREMENT,
	nombre_cat VARCHAR2(50),
	id_prod INTEGER NOT NULL,
	FOREIGN KEY (id_prod) REFERENCES PRODUCTO(id_prod)
);

CREATE TABLE CLIENTE(
	ci INTEGER PRIMARY KEY AUTOINCREMENT,
	nombre_completo VARCHAR2(100)
);

CREATE TABLE FACTURACION(
	nro_factura INTEGER NOT NULL PRIMARY KEY,
	nit INTEGER NOT NULL,
	nro_autorizacion INTEGER NOT NULL,
	fecha DATE NOT NULL
);

CREATE TABLE EMPLEADO(
	ci INTEGER PRIMARY KEY,
	nombres VARCHAR2(50),
	apellido_paterno VARCHAR2(50),
	apellido_materno VARCHAR2(50),
	fecha_nac DATETIME NOT NULL,
	celular	VARCHAR2(10),
	user VARCHAR2(20),
	password VARCHAR2(30),
	email VARCHAR2(20),
	salario INTEGER NOT NULL,
	foto_emp VARCHAR2(50)
);

CREATE TABLE ENTRADA(
	id_entrada INTEGER PRIMARY KEY AUTOINCREMENT,
	fecha DATETIME NOT NULL,
	hora TIME NOT NULL,
	ci INTEGER NOT NULL,
	FOREIGN KEY (ci) REFERENCES EMPLEADO(ci)
);

CREATE TABLE SALIDA(
	id_salida INTEGER PRIMARY KEY AUTOINCREMENT,
	fecha DATETIME NOT NULL,
	hora TIME NOT NULL,
	ci INTEGER NOT NULL,
	FOREIGN KEY (ci) REFERENCES EMPLEADO(ci)
);


CREATE TABLE ADMINISTRADOR(
	ci_administrador INTEGER PRIMARY KEY AUTOINCREMENT,
	FOREIGN KEY (ci_administrador) REFERENCES EMPLEADO(ci)
);

CREATE TABLE GERENTE(
	ci_gerente INTEGER PRIMARY KEY AUTOINCREMENT,
	FOREIGN KEY (ci_gerente) REFERENCES EMPLEADO(ci)
);

CREATE TABLE DIRECTOR_COMERCIAL(
	ci_director_comercial INTEGER PRIMARY KEY AUTOINCREMENT,
	FOREIGN KEY (ci_director_comercial) REFERENCES EMPLEADO(ci)
)

CREATE TABLE DELIVERY(
	ci_delivery INTEGER PRIMARY KEY AUTOINCREMENT,
	FOREIGN KEY (ci_delivery) REFERENCES EMPLEADO(ci)
);

CREATE TABLE VENDEDOR(
	ci_vendedor INTEGER PRIMARY KEY AUTOINCREMENT,
	FOREIGN KEY (ci_vendedor) REFERENCES EMPLEADO(ci)
);

CREATE TABLE COMPRA(
	-- - Claves:
	ci INTEGER NOT NULL,
	id_prod INTEGER NOT NULL,
	nro_factura INTEGER NOT NULL,
	ci_vendedor INTEGER NOT NULL,
	-- - Atributos de Relacion:
	fecha DATETIME NOT NULL,
	-- - PRIMARY KEY (ci, id_prod, nit)
	FOREIGN KEY (id_prod) REFERENCES PRODUCTO(id_prod)
	FOREIGN KEY (ci) REFERENCES CLIENTE(ci)
	FOREIGN KEY (nro_factura) REFERENCES FACTURACION(nro_factura)
	FOREIGN KEY (ci_vendedor) REFERENCES VENDEDOR(ci_vendedor)
);

CREATE TABLE COMPRA_DELIVERY(
	-- - Claves:
	ci INTEGER NOT NULL,
	id_prod INTEGER NOT NULL,
	nro_factura INTEGER NOT NULL,
	-- - Atributos de relacion
	entregado INT NOT NULL,
	ubicacion_cliente VARCHAR2(50),
	fecha DATETIME NOT NULL,
	telefono INTEGER NOT NULL,

	-- -PRIMARY KEY (ci, id_prod, nit)
	FOREIGN KEY (id_prod) REFERENCES PRODUCTO(id_prod)
	FOREIGN KEY (ci) REFERENCES CLIENTE(ci)
	FOREIGN KEY (nro_factura) REFERENCES FACTURACION(nro_factura)
);

INSERT INTO VENDEDOR(ci_vendedor)
VALUES (9768787);

-- - Proveedores

INSERT INTO PROVEEDOR(nombre_prov, numero_telefono, ubicacion)
VALUES ('Proveedor 1', '74646456', 'Calle #13 A');

INSERT INTO PROVEEDOR(nombre_prov, numero_telefono, ubicacion)
VALUES ('Proveedor 2', '74646455', 'Calle #13 B');

INSERT INTO PROVEEDOR(nombre_prov, numero_telefono, ubicacion)
VALUES ('Proveedor 3', '74646453', 'Calle #13 C');

INSERT INTO PROVEEDOR(nombre_prov, numero_telefono, ubicacion)
VALUES ('Proveedor 4', '74646451', 'Calle #13 D');

-- - Para los empleados

INSERT INTO EMPLEADO(ci, nombres, apellido_paterno, apellido_materno, fecha_nac, celular, user, password, email, salario, foto_emp)
VALUES (7346623, 'Jose', 'Chauca', 'Genaro', '11-09-2002', 3734645, 'chiqui', 'chauca', 'chiquichauca@gmail.com', 1500, '/home/diegojoel301/inf_162/fotos/2.png');

INSERT INTO EMPLEADO(ci, nombres, apellido_paterno, apellido_materno, fecha_nac, celular, user, password, email, salario, foto_emp)
VALUES (6768787, 'Juan Pablo', 'Andrade', 'Cock', '11-09-2002', 3744646, 'jp', 'revollex', 'juanpablosegundo@gmail.com', 2000, '/home/diegojoel301/inf_162/fotos/3.png');

INSERT INTO EMPLEADO(ci, nombres, apellido_paterno, apellido_materno, fecha_nac, celular, user, password, email, salario, foto_emp)
VALUES (9768787, 'Victor', 'Andrade', 'Huiza', '11-09-2002', 6744646, 'victor', 'andrade', 'chipsahoole@gmail.com', 1000, '/home/diegojoel301/inf_162/fotos/4.png');

-- - Para los directores comerciales

INSERT INTO DIRECTOR_COMERCIAL(ci_director_comercial)
VALUES (6768787);

INSERT INTO DIRECTOR_COMERCIAL(ci_director_comercial)
VALUES (9768787);

-- - Verificar si (user, password) es un director comercial




4|test1|34|gergregerg||2022-11-09|45|dfbfdb|4|9768787
5|test2|34|gergregerg||2022-11-09|45|dfbfdb|4|9768787
6|test3|34|gergregerg||2022-11-09|45|dfbfdb|4|9768787
7|test4|34|gergregerg||2022-11-09|45|dfbfdb|4|9768787
8|test5|34|gergregerg||2022-11-09|45|dfbfdb|4|9768787
9|test6|34|gergregerg||2022-11-09|45|dfbfdb|4|9768787