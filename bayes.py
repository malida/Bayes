import sqlite3

# Nombre base de datos con extension .db, nombre de la tabla, numero del atributo comenzando en 0.
db_name=input('Digite nombre de la base de datos: ')
table_name=input('Digite nombre de la tabla: ')
label=input('Digite el numero del atributo label a utilizar, contando desde 0: ')
db_name="example.db"
#table_name="t2"
#label="4"

# Conexion con la base de datos.
conn = sqlite3.connect(db_name)
c = conn.cursor()

# Recuperar informacion necesaria de la base de datos.
atributos1=c.execute("PRAGMA table_info("+table_name+");")
atributos=[]
for row in atributos1:
	atributos.append(row[1])

parametros=[]
temporal=[]
for att in atributos:
	for row in c.execute("SELECT DISTINCT("+att+") FROM "+table_name+";"):
		temporal.append(row[0])
	parametros.append(temporal)		
	temporal=[]

todos=c.execute("SELECT COUNT(*) FROM "+table_name+";")
todos=int(todos.fetchone()[0])
total_label=[]
name_label=parametros[int(label)]
for row in parametros[int(label)]:
	temp=c.execute("SELECT COUNT(*) FROM "+table_name+" WHERE "+atributos[int(label)]+"='"+row+"';")
	total_label.append(int(temp.fetchone()[0])/todos)

# Determinar las probabilidades para todos los tipos de cada atributo, por cada posible valor del label.
resultado1=[]
resultado2=[]
i=0
j=0
for lab in atributos:
	if i!=(int(label)):
		for row in parametros[int(i)]:	
			for itlabel in  name_label:
				#print("SELECT COUNT(*) FROM "+table_name+" WHERE "+atributos[int(i)]+"='"+row+"' AND "+atributos[int(label)]+"='"+itlabel+"';")
				#resultado1.append("Value="+row+" & "+itlabel+": ")
				resultado1.append(atributos[int(i)]+" value="+row)
				temp=c.execute("SELECT COUNT(*) FROM "+table_name+" WHERE "+atributos[int(i)]+"='"+row+"' AND "+atributos[int(label)]+"='"+itlabel+"';")
				temp2=int(temp.fetchone()[0])/todos

				for num in range(0,len(name_label)):
					if itlabel==name_label[num]:
						resultado2.append(temp2/total_label[num])
						if temp2/total_label[num]==0:
							print('WARNING: Existe una probabilidad en 0, corrija agregando una tupla nueva. (Corrector de Laplace)')
	i=i+1

j=0
num_att=int(len(resultado1)/len(name_label)) #numero de atributos
resulttemp=[]
prob=[]
for num in range(0,num_att):
	resulttemp=[]
	for num2 in range(0,len(name_label)):
		resulttemp.append(resultado2[num+num2+j])
	prob.append(resulttemp)
	j=j+1

for num in range(0,num_att):
	print(num,resultado1[num*len(name_label)],prob[num])

prob_labels=[]
for b in range(0,len(name_label)):
	prob_labels.append(1)

# Calculo de las probabilidades segun el caso de prueba.
temp=[]
do_it=True
while(do_it):
	for a in range(0,len(atributos)):
		if a!=(int(label)):
			string="Ingrese las restricciones del atributo "+atributos[a]+": "
			i=input(string)
			for b in range(0,len(name_label)):
				temp=prob[int(i)]
				prob_labels[b]=prob_labels[b]*temp[b]

	print(prob_labels)
	swt=input('Si desea salirse, escriba 0. De lo contrario, escriba 1: ')
	if (int(swt)==0):
		do_it=False

# Cerrar conexion base de datos.
conn.close()