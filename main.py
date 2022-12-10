import random
from flask import Flask, render_template, request, redirect, jsonify, make_response, flash, url_for
import sqlite3
from jwt import encode, decode, exceptions
from datetime import datetime, timedelta, date
from flask_cachecontrol import cache
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
# Generacion de usuarios de la base de datos
con = sqlite3.connect("database.db")
cur = con.cursor()
cur.execute("SELECT user, password, ci FROM EMPLEADO") # hacemos una query de todos los usuarios de la base de datos
usuarios = cur.fetchall() # de la query la salida lo convertimos en un vector de tuplas
filtro_productos = False
dict_users = dict()
cliente = ['', '', '', '', '', '', '', '']
cliente_delivery = ['', '', '', '', '', '', '', '', '', '']
#productos_imprimir = ['', '', '', '', '', '', '', '', '']
productos_imprimir = list()
for users in usuarios:
	dict_users[(users[0], users[1])] = users[2]
	
v_productos_facturacion = list()
v_productos_facturacion_del = list()



print(dict_users)

v_productos_facturacion.append((1, 10, 'Producto Interesante', 10, 5))
v_productos_facturacion.append((2, 10, 'Producto Interesante', 10, 5))
v_productos_facturacion.append((3, 10, 'Producto Interesante', 10, 5))
v_productos_facturacion.append((4, 10, 'Producto Interesante', 10, 5))
v_productos_facturacion.append((5, 10, 'Producto Interesante', 10, 5))
v_productos_facturacion.append((6, 10, 'Producto Interesante', 10, 5))


v_productos_facturacion_del.append((1, 10, 'Producto Interesante', 10, 5))
v_productos_facturacion_del.append((2, 10, 'Producto Interesante', 10, 5))
v_productos_facturacion_del.append((3, 10, 'Producto Interesante', 10, 5))
v_productos_facturacion_del.append((4, 10, 'Producto Interesante', 10, 5))
v_productos_facturacion_del.append((5, 10, 'Producto Interesante', 10, 5))
v_productos_facturacion_del.append((6, 10, 'Producto Interesante', 10, 5))

def expire_date(days: int):
	now = datetime.now()
	new_date = now + timedelta(days)
	return new_date

def write_token(data: dict):
	token = encode(payload = {**data, "exp": expire_date(2)},
						key = 'OPENIOT2022', algorithm = "HS256")
	return token

def validate_token(token, output = False):
	try:
		if output:
			decode(token, key = 'OPENIOT2022', algorithms = ["HS256"])
			#return decode(token, key = 'OPENIOT2022', algorithms = ["HS256"])
			return True
	except exceptions.DecodeError:
		#response = jsonify({"message": "Invalid Token"})
		#response.status_code = 401
		#return response
		return False
	except exceptions.ExpiredSignatureError:
		#response = jsonify({"message": "Token Expired"})
		#response.status_code = 401
		#return response
		return False
@app.route('/')
def indice():
	return redirect('/index', 301)

@app.route('/index')
def index():

	if verify():
		return render_template('Menu.html')

	return redirect('/inicio_sesion', 301)

@app.route('/inicio_sesion')
def inicio_sesion():
	return render_template('index.html')

@app.route('/login', methods = ['POST']) # cuando desde index.html el usuario se logea solo se acepta solicitudes POST de ahi sacamos el user y password
def login():
	if request.method == "POST": # verificamos que el metodo sea por POST
		#con = sqlite3.connect("database.db") # Conexion a la base de datos

		#cur = con.cursor() # Instanciacion de cursos de base de datos

		usuario = request.form['username']
		password = request.form['password']

		print(usuarios)

		if (usuario, password) in dict_users.keys(): # verificamos si la salida es vacia, comparando con un vector vacio
			#res = make_response("Adelante")
			res = redirect('/index', 301)
			res.set_cookie('JWT_Authorization', write_token(data = {'user': usuario, 'ci': dict_users[(usuario, password)]}))
			return res# de se asi entonces nos redireccionamos al panel principal
	return redirect('/inicio_sesion', 301)

def verify():
	try:
		token =  request.cookies['JWT_Authorization']
		if validate_token(token, output = True):
			return True
		return False
	except:
		return False

@app.route('/inventario')
def inventario():
	global productos_imprimir

	if productos_imprimir == list():
		con = sqlite3.connect("database.db")
		cur = con.cursor()
		cur.execute("SELECT xd.ID_PROD, xd.NOMBRE, xd.FECHA_VENC, xd.STOCK, xd.PRECIO, xd.PAIS_FABRICACION, xs.NOMBRE_PROV, xs.NUMERO_TELEFONO, xs.UBICACION FROM PRODUCTO xd, PROVEEDOR xs WHERE xs.ID_PROV = xd.ID_PROV")
		productos_imprimir = cur.fetchall()
	print("Imprimir: ", productos_imprimir)

	return render_template('Inventario.html', productos = productos_imprimir)

@app.route('/buscar_productos_por_categoria', methods = ['POST'])
@cache(max_age=1)
def buscar_productos_por_categoria():

	categoria = request.form['categoria']
	global productos_imprimir

	con = sqlite3.connect("database.db")
	cur = con.cursor()

	if categoria == "Crustáceos":
		print("Crustáceos")
		cur.execute("SELECT xd.ID_PROD, xd.NOMBRE, xd.FECHA_VENC, xd.STOCK, xd.PRECIO, xd.PAIS_FABRICACION, xs.NOMBRE_PROV, xs.NUMERO_TELEFONO, xs.UBICACION FROM PRODUCTO xd, PROVEEDOR xs, CATEGORIA xy WHERE xs.ID_PROV = xd.ID_PROV AND xy.NOMBRE_CAT LIKE 'Crustáceos' AND xy.ID_PROD = xd.ID_PROD")
	elif categoria == "Moluscos":
		print("Moluscos")
		cur.execute("SELECT xd.ID_PROD, xd.NOMBRE, xd.FECHA_VENC, xd.STOCK, xd.PRECIO, xd.PAIS_FABRICACION, xs.NOMBRE_PROV, xs.NUMERO_TELEFONO, xs.UBICACION FROM PRODUCTO xd, PROVEEDOR xs, CATEGORIA xy WHERE xs.ID_PROV = xd.ID_PROV AND xy.NOMBRE_CAT LIKE 'Moluscos' AND xy.ID_PROD = xd.ID_PROD")
	elif categoria == "Equinodermos":
		print("Equinodermos")
		cur.execute("SELECT xd.ID_PROD, xd.NOMBRE, xd.FECHA_VENC, xd.STOCK, xd.PRECIO, xd.PAIS_FABRICACION, xs.NOMBRE_PROV, xs.NUMERO_TELEFONO, xs.UBICACION FROM PRODUCTO xd, PROVEEDOR xs, CATEGORIA xy WHERE xs.ID_PROV = xd.ID_PROV AND xy.NOMBRE_CAT LIKE 'Equinodermos' AND xy.ID_PROD = xd.ID_PROD")
	elif categoria == "Todas":
		print("Todas las categorias")
		cur.execute("SELECT xd.ID_PROD, xd.NOMBRE, xd.FECHA_VENC, xd.STOCK, xd.PRECIO, xd.PAIS_FABRICACION, xs.NOMBRE_PROV, xs.NUMERO_TELEFONO, xs.UBICACION FROM PRODUCTO xd, PROVEEDOR xs WHERE xs.ID_PROV = xd.ID_PROV")

	productos_imprimir = cur.fetchall()
	print(productos_imprimir)

	return redirect(url_for('inventario'), 302)


@app.route('/ordenar_productos', methods = ['POST'])
@cache(max_age=1)
def ordenar_productos():

	tipo_ordenamiento = request.form['ordenamiento']
	global productos_imprimir

	con = sqlite3.connect("database.db")
	cur = con.cursor()

	if tipo_ordenamiento == "id_producto":
		print("Ordenamiento por ID")
		cur.execute("SELECT xd.ID_PROD, xd.NOMBRE, xd.FECHA_VENC, xd.STOCK, xd.PRECIO, xd.PAIS_FABRICACION, xs.NOMBRE_PROV, xs.NUMERO_TELEFONO, xs.UBICACION FROM PRODUCTO xd, PROVEEDOR xs WHERE xs.ID_PROV = xd.ID_PROV AND xy.ID_PROD = xd.ID_PROD ORDER BY xd.ID_PROD")
	elif tipo_ordenamiento == "nombre_producto":
		print("Ordenamiento por nombre de producto")
		cur.execute("SELECT xd.ID_PROD, xd.NOMBRE, xd.FECHA_VENC, xd.STOCK, xd.PRECIO, xd.PAIS_FABRICACION, xs.NOMBRE_PROV, xs.NUMERO_TELEFONO, xs.UBICACION FROM PRODUCTO xd, PROVEEDOR xs WHERE xs.ID_PROV = xd.ID_PROV AND xy.ID_PROD = xd.ID_PROD ORDER BY xd.NOMBRE")
	
	productos_imprimir = cur.fetchall()
		
	return redirect('/inventario', 302)

productos_vendidos_venta = list()

@app.route('/buscar_ventas_filtro', methods=['POST'])
@cache(max_age=1)
def buscar_ventas_filtro():
	#ImmutableMultiDict([('criterio', 'Fecha venta'), ('label_search', '2022-12-07'), ('npspec-referer', 'http://127.0.0.1:5000/ventas')])
	criterio = request.form['criterio']
	label_search = request.form['label_search']
	
	con = sqlite3.connect("database.db")
	cur = con.cursor()

	global productos_vendidos_venta

	if criterio == "fecha_venta":
		cur.execute("SELECT mago.* FROM (SELECT xd.ID_PROD, xs.NOMBRE, xd.FECHA, xl.NOMBRE_COMPLETO FROM COMPRA_DELIVERY xd, PRODUCTO xs, CLIENTE xl WHERE xd.ENTREGADO = 1 AND xs.ID_PROD = xd.ID_PROD AND xl.CI = xd.CI UNION SELECT xd.ID_PROD, xs.NOMBRE, xd.FECHA, xl.NOMBRE_COMPLETO FROM COMPRA xd, PRODUCTO xs, CLIENTE xl WHERE xs.ID_PROD = xd.ID_PROD AND xl.CI = xd.CI ORDER BY xd.ID_PROD) mago WHERE mago.FECHA LIKE '%s';" % (label_search))
	elif criterio == "nombre_producto":
		cur.execute("SELECT mago.* FROM (SELECT xd.ID_PROD, xs.NOMBRE, xd.FECHA, xl.NOMBRE_COMPLETO FROM COMPRA_DELIVERY xd, PRODUCTO xs, CLIENTE xl WHERE xd.ENTREGADO = 1 AND xs.ID_PROD = xd.ID_PROD AND xl.CI = xd.CI UNION SELECT xd.ID_PROD, xs.NOMBRE, xd.FECHA, xl.NOMBRE_COMPLETO FROM COMPRA xd, PRODUCTO xs, CLIENTE xl WHERE xs.ID_PROD = xd.ID_PROD AND xl.CI = xd.CI ORDER BY xd.ID_PROD) mago WHERE mago.NOMBRE LIKE '%s';" % (label_search))
	elif criterio == "nombre_cliente":
		cur.execute("SELECT mago.* FROM (SELECT xd.ID_PROD, xs.NOMBRE, xd.FECHA, xl.NOMBRE_COMPLETO FROM COMPRA_DELIVERY xd, PRODUCTO xs, CLIENTE xl WHERE xd.ENTREGADO = 1 AND xs.ID_PROD = xd.ID_PROD AND xl.CI = xd.CI UNION SELECT xd.ID_PROD, xs.NOMBRE, xd.FECHA, xl.NOMBRE_COMPLETO FROM COMPRA xd, PRODUCTO xs, CLIENTE xl WHERE xs.ID_PROD = xd.ID_PROD AND xl.CI = xd.CI ORDER BY xd.ID_PROD) mago WHERE mago.NOMBRE_COMPLETO LIKE '%s';" % (label_search))
	else:
		cur.execute("SELECT xd.ID_PROD, xs.NOMBRE, xd.FECHA, xl.NOMBRE_COMPLETO FROM COMPRA_DELIVERY xd, PRODUCTO xs, CLIENTE xl WHERE xd.ENTREGADO = 1 AND xs.ID_PROD = xd.ID_PROD AND xl.CI = xd.CI UNION SELECT xd.ID_PROD, xs.NOMBRE, xd.FECHA, xl.NOMBRE_COMPLETO FROM COMPRA xd, PRODUCTO xs, CLIENTE xl WHERE xs.ID_PROD = xd.ID_PROD AND xl.CI = xd.CI")

	productos_vendidos_venta = cur.fetchall()

	print(productos_vendidos_venta)

	return redirect(url_for('ventas'), 302)

@app.route('/ordenar_productos_por_orden', methods=['POST'])
@cache(max_age=1)
def ordenar_productos_por_orden():
	#ImmutableMultiDict([('criterio', 'Fecha venta'), ('label_search', '2022-12-07'), ('npspec-referer', 'http://127.0.0.1:5000/ventas')])
	ordenamiento = request.form['ordenamiento']
	
	con = sqlite3.connect("database.db")
	cur = con.cursor()

	global productos_vendidos_venta

	if ordenamiento == "fecha_venta":
		cur.execute("SELECT mago.* FROM (SELECT xd.ID_PROD, xs.NOMBRE, xd.FECHA, xl.NOMBRE_COMPLETO FROM COMPRA_DELIVERY xd, PRODUCTO xs, CLIENTE xl WHERE xd.ENTREGADO = 1 AND xs.ID_PROD = xd.ID_PROD AND xl.CI = xd.CI UNION SELECT xd.ID_PROD, xs.NOMBRE, xd.FECHA, xl.NOMBRE_COMPLETO FROM COMPRA xd, PRODUCTO xs, CLIENTE xl WHERE xs.ID_PROD = xd.ID_PROD AND xl.CI = xd.CI ORDER BY xd.ID_PROD) mago ORDER BY mago.FECHA")
	elif ordenamiento == "nombre_producto":
		cur.execute("SELECT mago.* FROM (SELECT xd.ID_PROD, xs.NOMBRE, xd.FECHA, xl.NOMBRE_COMPLETO FROM COMPRA_DELIVERY xd, PRODUCTO xs, CLIENTE xl WHERE xd.ENTREGADO = 1 AND xs.ID_PROD = xd.ID_PROD AND xl.CI = xd.CI UNION SELECT xd.ID_PROD, xs.NOMBRE, xd.FECHA, xl.NOMBRE_COMPLETO FROM COMPRA xd, PRODUCTO xs, CLIENTE xl WHERE xs.ID_PROD = xd.ID_PROD AND xl.CI = xd.CI ORDER BY xd.ID_PROD) mago ORDER BY mago.NOMBRE")
	else:
		cur.execute("SELECT xd.ID_PROD, xs.NOMBRE, xd.FECHA, xl.NOMBRE_COMPLETO FROM COMPRA_DELIVERY xd, PRODUCTO xs, CLIENTE xl WHERE xd.ENTREGADO = 1 AND xs.ID_PROD = xd.ID_PROD AND xl.CI = xd.CI UNION SELECT xd.ID_PROD, xs.NOMBRE, xd.FECHA, xl.NOMBRE_COMPLETO FROM COMPRA xd, PRODUCTO xs, CLIENTE xl WHERE xs.ID_PROD = xd.ID_PROD AND xl.CI = xd.CI")

	productos_vendidos_venta = cur.fetchall()

	print(productos_vendidos_venta)

	return redirect(url_for('ventas'), 302)

@app.route('/ventas')
def ventas():

	

		#return render_template('Ventas.html', productos_vendidos_venta = cur.fetchall())
	#elif request.method == 'GET':
	#	con = sqlite3.connect("database.db")
	#	cur = con.cursor()

	#	cur.execute("SELECT xd.ID_PROD, xs.NOMBRE, xd.FECHA, xl.NOMBRE_COMPLETO FROM COMPRA_DELIVERY xd, PRODUCTO xs, CLIENTE xl WHERE xd.ENTREGADO = 1 AND xs.ID_PROD = xd.ID_PROD AND xl.CI = xd.CI UNION SELECT xd.ID_PROD, xs.NOMBRE, xd.FECHA, xl.NOMBRE_COMPLETO FROM COMPRA xd, PRODUCTO xs, CLIENTE xl WHERE xs.ID_PROD = xd.ID_PROD AND xl.CI = xd.CI")

	#	vector_salida = cur.fetchall()

	global productos_vendidos_venta

	if productos_vendidos_venta == list():
		con = sqlite3.connect("database.db")
		cur = con.cursor()

		cur.execute("SELECT xd.ID_PROD, xs.NOMBRE, xd.FECHA, xl.NOMBRE_COMPLETO FROM COMPRA_DELIVERY xd, PRODUCTO xs, CLIENTE xl WHERE xd.ENTREGADO = 1 AND xs.ID_PROD = xd.ID_PROD AND xl.CI = xd.CI UNION SELECT xd.ID_PROD, xs.NOMBRE, xd.FECHA, xl.NOMBRE_COMPLETO FROM COMPRA xd, PRODUCTO xs, CLIENTE xl WHERE xs.ID_PROD = xd.ID_PROD AND xl.CI = xd.CI")	

		productos_vendidos_venta = cur.fetchall()

	print(productos_vendidos_venta)

	return render_template('Ventas.html', productos_vendidos_venta = productos_vendidos_venta)

@app.route('/delibery')
def delibery():

	total = 0

	for i in v_productos_facturacion_del:
		total += int(i[1]) * int(i[3]) + int(i[4])
	
	return render_template('Delibery.html', productos_venta = v_productos_facturacion_del, total = total)

@app.route('/detalles_producto_mostrar', methods = ['GET'])
@cache(max_age=1)
def detallers_producto_mostrar():
	print(request.args.get)
	#ImmutableMultiDict([('id_producto', '1'), ('nombre_producto', 'test1'), ('fecha_vencimiento', '2022-12-30'), ('proveedor', 'Proveedor 1')])>
	flash("Hola")
	return redirect('/inventario', 302)

@app.route('/delv')
def delv():
	nit_cliente = str(request.form['NIT_cliente'])
	nombre_cliente, apellido_cliente = str(request.form['Nombre_cliente']).split(' ')
	cel_cliente = str(request.form['Celular_cliente'])
	direc_cliente = str(request.form['Direccion_cliente'])
	
	token = request.cookies['JWT_Authorization']

	# Producto 

	jwt_decode = dict(decode(token, key = 'OPENIOT2022', algorithms = ["HS256"]))
	ci_delivery = jwt_decode['ci'] # de hecho no es precisamente el ci del delibery

	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT 1 FROM DELIVERY WHERE ci_divery = %s" % ci_delivery)
	
	if cur.fetchall() != list():
		now = datetime.now();
		#cur.execute("INSERT INTO COMPRA_DELIVERY(ci, ci_delivery, id_prod, nit, entregado, ubicacion_cliente, fecha, telefono) VALUES ('%s', '%s', '%s', '%s', '%s','%s', '%s', '%s','%s')" % (nit_cliente,ci_delivery,id_producto,nit_cliente,'True',direc_cliente,str(now.date+" "+now.time),cel_cliente))
		cur.execute("INSERT INTO CLIENTE(ci, nombres, apellido_paterno) VALUES ('%s', '%s', '%s')" % (nit_cliente, nombre_cliente, apellido_cliente))
		con.commit()
	return ""

empleados_negocio = list()

@app.route('/gestion_empleados')
def gestion_empleados():

	con = sqlite3.connect("database.db")
	cur = con.cursor()

	global empleados_negocio

	if empleados_negocio == list():
		cur.execute("SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'ADMINISTRADOR' CARGO FROM EMPLEADO xd, ADMINISTRADOR xs WHERE xd.CI = xs.CI_ADMINISTRADOR UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'GERENTE' CARGO FROM EMPLEADO xd, GERENTE xs WHERE xd.CI = xs.CI_GERENTE UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'DIRECTOR COMERCIAL' CARGO FROM EMPLEADO xd, DIRECTOR_COMERCIAL xs WHERE xd.CI = xs.CI_DIRECTOR_COMERCIAL UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'DELIVERY' CARGO FROM EMPLEADO xd, DELIVERY xs WHERE xd.CI = xs.CI_DELIVERY UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'VENDEDOR' CARGO FROM EMPLEADO xd, VENDEDOR xs WHERE xd.CI = xs.CI_VENDEDOR")
		empleados_negocio = cur.fetchall()

	print(empleados_negocio)

	return render_template('Gestion_Empleados.html', empleados = empleados_negocio)

@app.route('/busqueda_empleados', methods =  ['POST'])
@cache(max_age=1)
def busqueda_empleados():

	global empleados_negocio

	criterio = request.form['criterio']
	label_search = request.form['label_search']

	con = sqlite3.connect("database.db")
	cur = con.cursor()

	if criterio == "nombre":
		cur.execute("SELECT mago.* FROM (SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'ADMINISTRADOR' CARGO FROM EMPLEADO xd, ADMINISTRADOR xs WHERE xd.CI = xs.CI_ADMINISTRADOR UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'GERENTE' CARGO FROM EMPLEADO xd, GERENTE xs WHERE xd.CI = xs.CI_GERENTE UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'DIRECTOR COMERCIAL' CARGO FROM EMPLEADO xd, DIRECTOR_COMERCIAL xs WHERE xd.CI = xs.CI_DIRECTOR_COMERCIAL UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'DELIVERY' CARGO FROM EMPLEADO xd, DELIVERY xs WHERE xd.CI = xs.CI_DELIVERY UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'VENDEDOR' CARGO FROM EMPLEADO xd, VENDEDOR xs WHERE xd.CI = xs.CI_VENDEDOR) mago WHERE mago.NOMBRES LIKE '%s'" % (label_search))
		empleados_negocio = cur.fetchall()
	elif criterio == "ape_paterno":
		cur.execute("SELECT mago.* FROM (SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'ADMINISTRADOR' CARGO FROM EMPLEADO xd, ADMINISTRADOR xs WHERE xd.CI = xs.CI_ADMINISTRADOR UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'GERENTE' CARGO FROM EMPLEADO xd, GERENTE xs WHERE xd.CI = xs.CI_GERENTE UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'DIRECTOR COMERCIAL' CARGO FROM EMPLEADO xd, DIRECTOR_COMERCIAL xs WHERE xd.CI = xs.CI_DIRECTOR_COMERCIAL UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'DELIVERY' CARGO FROM EMPLEADO xd, DELIVERY xs WHERE xd.CI = xs.CI_DELIVERY UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'VENDEDOR' CARGO FROM EMPLEADO xd, VENDEDOR xs WHERE xd.CI = xs.CI_VENDEDOR) mago WHERE mago.APELLIDO_PATERNO LIKE '%s'" % (label_search))
		empleados_negocio = cur.fetchall()
	elif criterio == "ape_materno":
		cur.execute("SELECT mago.* FROM (SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'ADMINISTRADOR' CARGO FROM EMPLEADO xd, ADMINISTRADOR xs WHERE xd.CI = xs.CI_ADMINISTRADOR UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'GERENTE' CARGO FROM EMPLEADO xd, GERENTE xs WHERE xd.CI = xs.CI_GERENTE UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'DIRECTOR COMERCIAL' CARGO FROM EMPLEADO xd, DIRECTOR_COMERCIAL xs WHERE xd.CI = xs.CI_DIRECTOR_COMERCIAL UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'DELIVERY' CARGO FROM EMPLEADO xd, DELIVERY xs WHERE xd.CI = xs.CI_DELIVERY UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'VENDEDOR' CARGO FROM EMPLEADO xd, VENDEDOR xs WHERE xd.CI = xs.CI_VENDEDOR) mago WHERE mago.APELLIDO_MATERNO LIKE '%s'" % (label_search))
		empleados_negocio = cur.fetchall()
	elif criterio == "cargo":
		cur.execute("SELECT mago.* FROM (SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'ADMINISTRADOR' CARGO FROM EMPLEADO xd, ADMINISTRADOR xs WHERE xd.CI = xs.CI_ADMINISTRADOR UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'GERENTE' CARGO FROM EMPLEADO xd, GERENTE xs WHERE xd.CI = xs.CI_GERENTE UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'DIRECTOR COMERCIAL' CARGO FROM EMPLEADO xd, DIRECTOR_COMERCIAL xs WHERE xd.CI = xs.CI_DIRECTOR_COMERCIAL UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'DELIVERY' CARGO FROM EMPLEADO xd, DELIVERY xs WHERE xd.CI = xs.CI_DELIVERY UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'VENDEDOR' CARGO FROM EMPLEADO xd, VENDEDOR xs WHERE xd.CI = xs.CI_VENDEDOR) mago WHERE mago.CARGO LIKE '%s'" % (label_search.upper()))
		empleados_negocio = cur.fetchall()

	return redirect(url_for('gestion_empleados'), 302)

@app.route('/ordenar_empleados', methods =  ['POST'])
@cache(max_age=1)
def ordenar_empleados():

	global empleados_negocio

	criterio = request.form['ordenar']

	con = sqlite3.connect("database.db")
	cur = con.cursor()

	if criterio == "nombre":
		cur.execute("SELECT mago.* FROM (SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'ADMINISTRADOR' CARGO FROM EMPLEADO xd, ADMINISTRADOR xs WHERE xd.CI = xs.CI_ADMINISTRADOR UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'GERENTE' CARGO FROM EMPLEADO xd, GERENTE xs WHERE xd.CI = xs.CI_GERENTE UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'DIRECTOR COMERCIAL' CARGO FROM EMPLEADO xd, DIRECTOR_COMERCIAL xs WHERE xd.CI = xs.CI_DIRECTOR_COMERCIAL UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'DELIVERY' CARGO FROM EMPLEADO xd, DELIVERY xs WHERE xd.CI = xs.CI_DELIVERY UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'VENDEDOR' CARGO FROM EMPLEADO xd, VENDEDOR xs WHERE xd.CI = xs.CI_VENDEDOR) mago ORDER BY mago.NOMBRES")
		empleados_negocio = cur.fetchall()
	elif criterio == "ape_paterno":
		cur.execute("SELECT mago.* FROM (SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'ADMINISTRADOR' CARGO FROM EMPLEADO xd, ADMINISTRADOR xs WHERE xd.CI = xs.CI_ADMINISTRADOR UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'GERENTE' CARGO FROM EMPLEADO xd, GERENTE xs WHERE xd.CI = xs.CI_GERENTE UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'DIRECTOR COMERCIAL' CARGO FROM EMPLEADO xd, DIRECTOR_COMERCIAL xs WHERE xd.CI = xs.CI_DIRECTOR_COMERCIAL UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'DELIVERY' CARGO FROM EMPLEADO xd, DELIVERY xs WHERE xd.CI = xs.CI_DELIVERY UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'VENDEDOR' CARGO FROM EMPLEADO xd, VENDEDOR xs WHERE xd.CI = xs.CI_VENDEDOR) mago ORDER BY mago.APELLIDO_PATERNO")
		empleados_negocio = cur.fetchall()
	elif criterio == "ape_materno":
		cur.execute("SELECT mago.* FROM (SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'ADMINISTRADOR' CARGO FROM EMPLEADO xd, ADMINISTRADOR xs WHERE xd.CI = xs.CI_ADMINISTRADOR UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'GERENTE' CARGO FROM EMPLEADO xd, GERENTE xs WHERE xd.CI = xs.CI_GERENTE UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'DIRECTOR COMERCIAL' CARGO FROM EMPLEADO xd, DIRECTOR_COMERCIAL xs WHERE xd.CI = xs.CI_DIRECTOR_COMERCIAL UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'DELIVERY' CARGO FROM EMPLEADO xd, DELIVERY xs WHERE xd.CI = xs.CI_DELIVERY UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'VENDEDOR' CARGO FROM EMPLEADO xd, VENDEDOR xs WHERE xd.CI = xs.CI_VENDEDOR) mago ORDER BY mago.APELLIDO_MATERNO")
		empleados_negocio = cur.fetchall()
	elif criterio == "cargo":
		cur.execute("SELECT mago.* FROM (SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'ADMINISTRADOR' CARGO FROM EMPLEADO xd, ADMINISTRADOR xs WHERE xd.CI = xs.CI_ADMINISTRADOR UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'GERENTE' CARGO FROM EMPLEADO xd, GERENTE xs WHERE xd.CI = xs.CI_GERENTE UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'DIRECTOR COMERCIAL' CARGO FROM EMPLEADO xd, DIRECTOR_COMERCIAL xs WHERE xd.CI = xs.CI_DIRECTOR_COMERCIAL UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'DELIVERY' CARGO FROM EMPLEADO xd, DELIVERY xs WHERE xd.CI = xs.CI_DELIVERY UNION SELECT xd.CI, xd.NOMBRES, xd.APELLIDO_PATERNO, xd.APELLIDO_MATERNO, xd.FECHA_NAC, 'VENDEDOR' CARGO FROM EMPLEADO xd, VENDEDOR xs WHERE xd.CI = xs.CI_VENDEDOR) mago ORDER BY mago.CARGO")
		empleados_negocio = cur.fetchall()

	return redirect(url_for('gestion_empleados'), 302)

@app.route('/acerca-de')
def acerca_de():
	return render_template('Acerca-de.html')
@app.route('/aniadirproducto')
def aniadirproducto():

	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT nombre_prov FROM PROVEEDOR")

	proveedores = list()

	for i in cur.fetchall():
		proveedores.append(i[0])

	print(proveedores)

	return render_template('AniadirProducto.html', proveedores=proveedores)


@app.route('/aniadir_proddelivery')
def aniadir_proddelivery():
	return render_template('Aniadir_ProdDelivery.html')

@app.route('/aniadir_proveedor')
def aniadir_proveedor():
	return render_template('Aniadir_Proveedor.html')

@app.route('/aniadir_prov', methods = ['POST'])
def aniadir_prov():
	nombre_proveedor = str(request.form['n_prov'])
	telefeno_proveedor = str(request.form['n_telf'])
	email_proveedor = str(request.form['email_prov'])
	pais_proveedor = str(request.form['pais_prov'])
	direccion_proveedor = str(request.form['dir_prov'])
	
	token = request.cookies['JWT_Authorization']

	# Producto 

	jwt_decode = dict(decode(token, key = 'OPENIOT2022', algorithms = ["HS256"]))
	ci_director_comercial = jwt_decode['ci'] # de hecho no es precisamente el ci del director comercial

	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT 1 FROM DIRECTOR_COMERCIAL WHERE ci_director_comercial = %s" % ci_director_comercial)
	
	if cur.fetchall() != list():
		cur.execute("INSERT INTO PROVEEDOR(nombre_prov, numero_telefono, ubicacion, email, pais) VALUES ('%s', '%s', '%s', '%s', '%s')" % (nombre_proveedor, telefeno_proveedor, direccion_proveedor, email_proveedor, pais_proveedor))
		con.commit()
	return ""

@app.route('/aniadir_prod_factura')
def aniadir_prod_factura():
	return render_template('Aniadir_Prod_Factura.html')

@app.route('/contacto')
def contacto():
	return render_template('Contacto.html')

@app.route('/delivery-pendientes')
def delivery_pendientes():

	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT xd.NRO_FACTURA, xl.NOMBRE, xs.NOMBRE_COMPLETO, xd.FECHA, xd.UBICACION_CLIENTE FROM COMPRA_DELIVERY xd, CLIENTE xs, PRODUCTO xl WHERE xd.CI = xs.CI AND xl.ID_PROD = xd.ID_PROD AND xd.ENTREGADO = 0")

	v_clientes_delivery = cur.fetchall()

	#print(v_clientes_delivery)


	return render_template('Delivery-pendientes.html', clientes_delivery = v_clientes_delivery)

@app.route('/deliverycompletado', methods = ['GET', 'POST'])
@cache(max_age=1)
def deliverycompletado():
	# /deliverycompletado?nro_facturacion=7831197757&nombre_producto=testt&nombre_cliente=Dennis%20Fernandez%20Quito&fecha_inicio=2022-12-07&direccion=Mi%20casa%20xD
	nro_facturacion = request.args.get('nro_facturacion')
	nombre_cliente = request.args.get('nombre_cliente')
	nombre_producto = request.args.get('nombre_producto')
	fecha_inicio = request.args.get('fecha_inicio')
	direccion = request.args.get('direccion')

	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT xd.* FROM COMPRA_DELIVERY xd, CLIENTE xs, PRODUCTO xl WHERE xd.CI = xs.CI AND xs.NOMBRE_COMPLETO LIKE '%s' AND xl.ID_PROD = xd.ID_PROD AND xl.NOMBRE LIKE '%s'" % (nombre_cliente, nombre_producto))

	elemento = cur.fetchall()

	cur.execute("UPDATE COMPRA_DELIVERY SET ENTREGADO = 1 WHERE CI = %s AND ID_PROD = %s AND nro_factura = %s AND ENTREGADO = %s AND UBICACION_CLIENTE LIKE '%s' AND fecha LIKE '%s' AND TELEFONO = %s" % elemento[0])
	con.commit()
	print(elemento)

	return redirect('/delivery-pendientes', 302)

@app.route('/detalles_producto')
def detalles_producto():
	return render_template('Detalles_Producto.html')

@app.route('/facturacion')
def facturacion():

	total = 0

	for i in v_productos_facturacion:
		total += int(i[1]) * int(i[3]) + int(i[4])
	
	return render_template('Facturacion.html', productos_venta = v_productos_facturacion, total = total)

@app.route('/eliminarprodfact', methods = ['GET'])
@cache(max_age=1)
def eliminarprodfact():
	# ImmutableMultiDict([('codigo', '1'), ('cantidad', '10'), ('descripcion', 'Producto Interesante'), ('precio_unitario', '10'), ('importe', '5')])	
	codigo = int(request.args.get('codigo'))
	cantidad = int(request.args.get('cantidad'))
	descripcion = str(request.args.get('descripcion'))
	precio_unitario = int(request.args.get('precio_unitario'))
	importe = int(request.args.get('importe'))

	v_productos_facturacion.remove((codigo, cantidad, descripcion, precio_unitario, importe))
	

	return redirect('/facturacion', 302)
	#return "frengenru"

#@app.route('/eliminar_prodfact', methods = ['POST', 'GET'])

#def eliminar_prodfact():

#	print(request.args.get)
#	return redirect('/facturacion',code=302)

@app.route('/eliminarprodfact_del', methods = ['GET'])
@cache(max_age=1)
def eliminarprodfact_del():
	# ImmutableMultiDict([('codigo', '1'), ('cantidad', '10'), ('descripcion', 'Producto Interesante'), ('precio_unitario', '10'), ('importe', '5')])	
	codigo = int(request.args.get('codigo'))
	cantidad = int(request.args.get('cantidad'))
	descripcion = str(request.args.get('descripcion'))
	precio_unitario = int(request.args.get('precio_unitario'))
	importe = int(request.args.get('importe'))

	v_productos_facturacion_del.remove((codigo, cantidad, descripcion, precio_unitario, importe))

	return redirect('/delibery', 302)

@app.route('/hacer_venta', methods = ['POST'])
def hacer_venta():

	#ImmutableMultiDict([('cod_producto', '1'), ('cantidad', '2144'),
	#  ('descripcion', 'ergrthtryh'), ('formServices', '1ff519dec1e85438082e5a3ab30b1abd')])

	cod_producto = request.form['cod_producto']
	cantidad = request.form['cantidad']
	descripcion = request.form['descripcion']

	con = sqlite3.connect("database.db")
	cur = con.cursor()

	cur.execute("SELECT precio FROM PRODUCTO WHERE id_prod = '%s'" % cod_producto)

	precio = cur.fetchall()[0][0]

	cur.execute("SELECT stock FROM PRODUCTO WHERE id_prod = '%s'" % cod_producto)

	stock = cur.fetchall()[0][0]

	if stock - int(cantidad) < 0:
		print("El stock no satisface la cantidad")
	else:
		v_productos_facturacion.append((int(cod_producto), int(cantidad), descripcion, int(precio), 5))

	return redirect('/facturacion', 301)

@app.route('/aniadir_proddelivery_venta', methods=['POST'])
def aniadir_proddelivery_venta():
	print("HOLA")
	print(request.form)
	cod_producto = request.form['cod_producto']
	cantidad = request.form['cantidad']
	descripcion = request.form['descripcion']

	con = sqlite3.connect("database.db")
	cur = con.cursor()

	cur.execute("SELECT precio FROM PRODUCTO WHERE id_prod = '%s'" % cod_producto)

	precio = cur.fetchall()[0][0]

	cur.execute("SELECT stock FROM PRODUCTO WHERE id_prod = '%s'" % cod_producto)

	stock = cur.fetchall()[0][0]

	if stock - int(cantidad) < 0:
		print("El stock no satisface la cantidad")
	else:
		v_productos_facturacion_del.append((int(cod_producto), int(cantidad), descripcion, int(precio), 5))

	return redirect('/delibery', 301)

@app.route('/mas-acciones')
def mas_acciones():
	return render_template('Mas-acciones.html')

@app.route('/nuevos_pedidos')
def nuevos_pedidos():
	return render_template('Nuevos_Pedidos.html')

@app.route('/registro')
@cache(max_age=1)
def registro():

	token = request.cookies['JWT_Authorization']

	jwt_decode = dict(decode(token, key = 'OPENIOT2022', algorithms = ["HS256"]))
	ci_director_comercial = jwt_decode['ci'] # de hecho no es precisamente el ci del director comercial
	
	#print(ci_director_comercial)

	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT 1 FROM ADMINISTRADOR WHERE ci_administrador = %s" % ci_director_comercial)
	
	if cur.fetchall() != list():
		return render_template('Registro.html')
	return redirect(url_for('index'), 302)

@app.route('/registrar_empleado', methods=['POST'])
@cache(max_age=1)
def registrar_empleado():
	token = request.cookies['JWT_Authorization']

	jwt_decode = dict(decode(token, key = 'OPENIOT2022', algorithms = ["HS256"]))
	ci_director_comercial = jwt_decode['ci'] # de hecho no es precisamente el ci del director comercial
	
	#print(ci_director_comercial)

	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT 1 FROM ADMINISTRADOR WHERE ci_administrador = %s" % ci_director_comercial)
	
	if cur.fetchall() != list():
		ci = request.form['ci']
		nombres = request.form['nombres']
		ape_paterno = request.form['ape_paterno']
		ape_materno = request.form['ape_materno']
		fecha_nac = request.form['fecha_nac']
		celular = request.form['celular']
		email = request.form['email']
		cargo = request.form['cargos']
		user = request.form['user']
		password = request.form['password']
		salario = request.form['salario']

		cur.execute("INSERT INTO EMPLEADO(ci, nombres, apellido_paterno, apellido_materno, fecha_nac, celular, user, password, email, salario) VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s)" % (ci, nombres, ape_paterno, ape_materno, fecha_nac, celular, user, password, email, salario))
		con.commit()

		if cargo == "vendedor":
			cur.execute("INSERT INTO VENDEDOR(ci_vendedor) VALUES(%s)" % (ci))	
			con.commit()
		elif cargo == "director_comercial":
			cur.execute("INSERT INTO DIRECTOR_COMERCIAL(ci_director_comercial)" % (ci))
			con.commit()
		elif cargo == "gerente":
			cur.execute("INSERT INTO GERENTE(ci_gerente) VALUES (%s)" % (ci))
			con.commit()
		elif cargo == "delibery":
			cur.execute("INSERT INTO DELIVERY(ci_delivery) VALUES(%s)" % (ci))
			con.commit()
		elif cargo == "administrador":
			cur.execute("INSERT INTO ADMINISTRADOR(ci_administrador) VALUES(%s)" % (ci))
			con.commit()

	return redirect(url_for('index'), 302)

@app.route('/ubicacion')
def ubicacion():
	return render_template('Ubicacion.html')

@app.route('/vista_factura')
def vista_factura():
	#return render_template('Vista_previa-factura.html', ci_nit_cliente = ci_nit_cliente, nombre_cliente=nombre_cliente, nro_factura=nro_factura, nro_autorizacion = nro_autorizacion, nit_negocio = nit_negocio)
	print(cliente)
	
	return render_template('Vista_previa-factura.html', 
			ci_nit_cliente = cliente[1], 
			nombre_cliente=cliente[2],
			nro_factura=cliente[3], 
			nro_autorizacion = cliente[4], 
			nit_negocio = cliente[0],
			total = cliente[5],
			productos_venta = v_productos_facturacion,
			fecha_inicio = cliente[6],
			fecha_limite = cliente[7])

@app.route('/vista_previa_factura_del', methods=['POST', 'GET'])
#@cache(max_age=1)
def vista_previa_factura_del():
	print(request.form)
	print(request.args.get)
	nit_negocio = 12535474
	ci_nit_cliente = request.form['nit_cliente']
	nombre_cliente = request.form['nombre_cliente']
	nro_factura = random.randint(3333333333, 9999999999)
	nro_autorizacion = random.randint(3333333333, 9999999999)
	total = request.form['total']
	fecha_inicio = date.today()
	fecha_limite = date.today() + relativedelta(months=+3)
	celular_cliente = request.form['Celular_cliente']
	ubicacion_cliente = request.form['Direccion_cliente']
	
	cliente_delivery[0] = nit_negocio
	cliente_delivery[1] = ci_nit_cliente
	cliente_delivery[2] = nombre_cliente
	cliente_delivery[3] = nro_factura
	cliente_delivery[4] = nro_autorizacion
	cliente_delivery[5] = total
	cliente_delivery[6] = fecha_inicio
	cliente_delivery[7] = fecha_limite
	cliente_delivery[8] = celular_cliente
	cliente_delivery[9] = ubicacion_cliente
	print(cliente_delivery)
	return ""

@app.route('/vista_previa_factura', methods=['POST', 'GET'])
#@cache(max_age=1)
def vista_previa_factura():
	print(request.form)
	print(request.args.get)
	nit_negocio = 12535474
	ci_nit_cliente = request.form['nit_cliente']
	nombre_cliente = request.form['nombre_cliente']
	nro_factura = random.randint(3333333333, 9999999999)
	nro_autorizacion = random.randint(3333333333, 9999999999)
	total = request.form['total']
	fecha_inicio = date.today()
	fecha_limite = date.today() + relativedelta(months=+3)
	

	#cliente = (nit_negocio, ci_nit_cliente, nombre_cliente, nro_factura, nro_autorizacion)
	cliente[0] = nit_negocio
	cliente[1] = ci_nit_cliente
	cliente[2] = nombre_cliente
	cliente[3] = nro_factura
	cliente[4] = nro_autorizacion
	cliente[5] = total
	cliente[6] = fecha_inicio
	cliente[7] = fecha_limite

	return ""

@app.route('/vista_previa_factura_delivery')
def vista_previa_factura_delivery():

	print(cliente_delivery)
	
	return render_template('Vista_previa-factura_Delivery.html', 
			ci_nit_cliente = cliente_delivery[1], 
			nombre_cliente=cliente_delivery[2],
			nro_factura=cliente_delivery[3], 
			nro_autorizacion = cliente_delivery[4], 
			nit_negocio = cliente_delivery[0],
			total = cliente_delivery[5],
			productos_venta = v_productos_facturacion_del,
			fecha_inicio = cliente_delivery[6],
			fecha_limite = cliente_delivery[7])

@app.route('/realizar_venta')
@cache(max_age=1)
def realizar_venta():
	token = request.cookies['JWT_Authorization']

	# Producto 

	jwt_decode = dict(decode(token, key = 'OPENIOT2022', algorithms = ["HS256"]))
	ci_vendedor = jwt_decode['ci'] # de hecho no es precisamente el ci del director comercial
	
	#print(ci_director_comercial)
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT 1 FROM VENDEDOR WHERE ci_vendedor = %s" % ci_vendedor)
	
	if cur.fetchall() != list():
		try:
			print("Agregando cliente a la base de datos")

			cur.execute("INSERT INTO CLIENTE(ci, nombre_completo) VALUES(%s, '%s')" % (cliente[1], cliente[2]))
			con.commit()
		except:
			print("Este cliente ya esta registrado")
		cur.execute("INSERT INTO FACTURACION(nro_factura, nit, nro_autorizacion, fecha) VALUES (%s, %s, %s, '%s')" % (cliente[3], cliente[0], cliente[4], date.today()))
		con.commit()
		for producto in v_productos_facturacion:
			cur.execute("INSERT INTO COMPRA(ci, id_prod, nro_factura, ci_vendedor, fecha) VALUES (%s, %s, %s, %s, '%s')" % (cliente[1], producto[0], cliente[3], ci_vendedor, date.today()))
			con.commit()
			#print(producto)
	print("Venta Realizada!")
	return redirect('/facturacion', 302)

@app.route('/realizar_venta_delivery')
@cache(max_age=1)
def realizar_venta_delivery():
	token = request.cookies['JWT_Authorization']

	# Producto 

	jwt_decode = dict(decode(token, key = 'OPENIOT2022', algorithms = ["HS256"]))
	ci_vendedor = jwt_decode['ci'] # de hecho no es precisamente el ci del director comercial
	
	#print(ci_director_comercial)
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT 1 FROM VENDEDOR WHERE ci_vendedor = %s" % ci_vendedor)
	
	if cur.fetchall() != list():
		try:
			cur.execute("INSERT INTO CLIENTE(ci, nombre_completo) VALUES(%s, '%s')" % (cliente_delivery[1], cliente_delivery[2]))
			con.commit()
		except:
			print("Este cliente ya esta registrado")
		cur.execute("INSERT INTO FACTURACION(nro_factura, nit, nro_autorizacion, fecha) VALUES (%s, %s, %s, '%s')" % (cliente_delivery[3], cliente_delivery[0], cliente_delivery[4], date.today()))
		con.commit()
		for producto in v_productos_facturacion:
			cur.execute("INSERT INTO COMPRA_DELIVERY(ci, id_prod, nro_factura, fecha, ubicacion_cliente, telefono, entregado) VALUES (%s, %s, %s, '%s', '%s', %s, %s)" % (cliente_delivery[1], producto[0], cliente_delivery[3], date.today(), cliente_delivery[9], cliente_delivery[8], 0))
			con.commit()
			#print(producto)

	return redirect('/delibery', 302)

@app.route('/aniade_prod', methods=['POST'])
def aniade_prod():
	# ImmutableMultiDict([('nombre_prod', 'Prod1'), ('fecha_vencimiento', '2022-11-10'), ('categorias', 'Crustáceos'), ('proveedores', 'Proveedor1'), ('precio_compra', '123'), ('precio_venta', '4342'), ('pais_origen', 'Bolivia'), ('cantidad', '234234')])

	nombre_prod = request.form['nombre_prod']
	fecha_vencimiento = request.form['fecha_vencimiento']
	categoria = request.form['categorias']
	nombre_proveedor = request.form['proveedores']
	#precio_compra = request.form['precio_compra']
	precio_venta = request.form['precio_venta']
	pais_origen = request.form['pais_origen']
	cantidad = request.form['cantidad']
	descripcion = request.form['descripcion']
	
	token = request.cookies['JWT_Authorization']

	# Producto 

	jwt_decode = dict(decode(token, key = 'OPENIOT2022', algorithms = ["HS256"]))
	ci_director_comercial = jwt_decode['ci'] # de hecho no es precisamente el ci del director comercial
	
	#print(ci_director_comercial)

	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT 1 FROM DIRECTOR_COMERCIAL WHERE ci_director_comercial = %s" % ci_director_comercial)
	
	if cur.fetchall() != list():
		cur.execute("SELECT id_prov FROM PROVEEDOR WHERE nombre_prov = '%s'" % nombre_proveedor)

		id_prov = cur.fetchall()[0][0]

		cur.execute("INSERT INTO PRODUCTO(nombre, stock, descripcion, fecha_venc, precio, pais_fabricacion, id_prov, ci_director_comercial) VALUES ('%s', %s, '%s', '%s', %s, '%s', '%s', '%s')" % (nombre_prod, cantidad, descripcion, fecha_vencimiento, precio_venta, pais_origen, id_prov, ci_director_comercial) )
		con.commit()
		cur.execute("SELECT ID_PROD FROM PRODUCTO WHERE nombre LIKE '%s'" % (nombre_prod))

		id_prod = cur.fetchall()[0][0]

		cur.execute("INSERT INTO CATEGORIA(nombre_cat, id_prod) VALUES ('%s', %s)" % (categoria, id_prod))

		con.commit()

		
	return "prueba xd"

@app.route('/registrar_hora_entrada')
@cache(max_age=1)
def registrar_hora_entrada():

	token = request.cookies['JWT_Authorization']

	jwt_decode = dict(decode(token, key = 'OPENIOT2022', algorithms = ["HS256"]))
	ci = jwt_decode['ci']

	fecha = date.today()
	hora = "%s:%s" % (datetime.now().hour, datetime.now().minute)

	print(ci, fecha, hora)

	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("INSERT INTO ENTRADA(fecha, hora, ci) VALUES ('%s', '%s', %s)" % (fecha, hora, ci))
	con.commit()

	return redirect(url_for('index'), 302)

@app.route('/registrar_hora_salida')
@cache(max_age=1)
def registrar_hora_salida():

	token = request.cookies['JWT_Authorization']

	jwt_decode = dict(decode(token, key = 'OPENIOT2022', algorithms = ["HS256"]))
	ci = jwt_decode['ci']

	fecha = date.today()
	hora = "%s:%s" % (datetime.now().hour, datetime.now().minute)

	print(ci, fecha, hora)

	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("INSERT INTO SALIDA(fecha, hora, ci) VALUES ('%s', '%s', %s)" % (fecha, hora, ci))
	con.commit()

	return redirect(url_for('index'), 302)

@app.route('/finalizarfacturacion')
def finalizarfacturacion():
	return ""

if __name__ == "__main__":
	app.run()
