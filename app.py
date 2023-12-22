from flask import Flask, render_template, request
from solucionador import Restricao, Solucionador
import re

app = Flask(__name__)

@app.get("/")
def ver_para_crer_get():
    return render_template('home.html', submitted=False)

@app.post("/")
def ver_para_crer_post():
    coeficientes_z = z_parser(request.form['primal'])
    restricoes = c_parser(request.form['constraints'])
    s = Solucionador(coeficientes_z[0],coeficientes_z[1])
    for r in restricoes:
        s.adicionar_restricao(Restricao(r[0],r[1],r[2],r[3]))

    if request.form['objetivo'] == 'MAX':
        solucao = s.maximizar()
    elif request.form['objetivo'] == 'MIN':
        solucao = s.minimizar()

    return render_template('home.html', submitted=True, solucao=solucao)

def z_parser(z:str):
    if z.find('x1') < 0 or z.find('x2') < 0:
        raise Exception('Expressão inválida. Problema deve ser declarado no padrão Z=ax1 + bx2')
    pattern = r'(\d+|\d+..\d+)x'
    z = z.lower()
    z = z.replace(" ","")
    z = z.replace(",",".")
    z = z.replace("=x1","=1x1")
    z = z.replace("+x2","+1x2")
    coeficientes = [float(numero) for numero in re.findall(pattern,z)]
    return coeficientes

def c_parser(c:str):
    c = c.lower()
    c = c.replace(" ","")
    c = c.replace(",",".")
    constraints = c.split("\n")
    pattern = r'(\d+|\d+..\d+)x1(\+|-)(\d+|\d+..\d+)x2(=|>|<|>=|<=)(\d+|\d+..\d+)'
    retorno = []
    for constraint in constraints:
        if constraint.find('x1') < 0 and constraint.find('x2') < 0:
            raise Exception('Expressão inválida. Restrição deve ser declarado no padrão ax1 + bx2 =|>|<|<=|<= c')
        coeficientes = re.search(pattern,constraint).groups()
        retorno.append([float(coeficientes[0]),float(coeficientes[2]),coeficientes[3],float(coeficientes[4])])
    return retorno