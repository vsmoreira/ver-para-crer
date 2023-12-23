from flask import Flask, render_template, request, abort
from solucionador import Restricao, Solucionador
import re, os

app = Flask(__name__)

@app.get("/")
def ver_para_crer_get():
    return render_template('home.html', submitted=False)

@app.post("/")
def ver_para_crer_post():
    coeficientes_z = z_parser(request.form['primal'])
    restricoes = c_parser(request.form['constraints'])
    try:
        s = Solucionador(coeficientes_z[0],coeficientes_z[1])
        for r in restricoes:
            s.adicionar_restricao(Restricao(r[0],r[1],r[2],r[3]))

        if request.form['objetivo'] == 'MAX':
            solucao = s.maximizar()
        elif request.form['objetivo'] == 'MIN':
            solucao = s.minimizar()
    except Exception as err:
        abort(500, err)
    return render_template('home.html', submitted=True, solucao=solucao)

@app.errorhandler(500)
def erro_execucao(error: str=None):
    return render_template("error.html", error=error), 500

def z_parser(z:str):
    """Retorna um array com os coeficientes de x1 e de x2 da função objetivo."""
    if z.find('x1') < 0 or z.find('x2') < 0:
        raise Exception('Expressão inválida. Problema deve ser declarado no padrão Z=ax1 + bx2')
    pattern = r'(\+|-)?(\d+|\d+..\d+)x1(\+|-)(\d+|\d+..\d+)x2'
    z = z.lower()
    z = z.replace(" ","")
    z = z.replace(",",".")
    z = z.replace("=x1","=1x1")
    z = z.replace("=-x1","=-1x1")
    z = z.replace("+x2","+1x2")
    z = z.replace("-x2","-1x2")
    coeficientes_grp = re.search(pattern,z).groups()
    coeficientes = [float(coeficientes_grp[1]),float(coeficientes_grp[3])]
    if coeficientes_grp[0] == '-':
            coeficientes[0] = -1*coeficientes[0]
    if coeficientes_grp[2] == '-':
        coeficientes[1] = -1*coeficientes[1]
    return coeficientes

def c_parser(c:str):
    """Retorna um array com os coeficientes de x1 e x2, com o sinal de desiguladade e com a constante de restrição."""
    c = c.lower()
    c = c.replace(" ","")
    c = c.replace(",",".")
    constraints = c.split("\n")
    pattern = r'^(\+|-)?((\d+|\d+..\d+)?x1)?((\+|-)?(\d+|\d+..\d+)?x2)?(=|>|<|>=|<=)(\d+|\d+..\d+)'
    retorno = []
    for constraint in constraints:
        if constraint.find('x1') < 0 and constraint.find('x2') < 0:
            raise Exception('Expressão inválida. Restrição deve ser declarado no padrão ax1 + bx2 =|>|<|<=|<= c')
        coeficientes_grp = re.search(pattern,constraint) #.groups()
        if coeficientes_grp == None:
            abort(500,constraint)
        else:
            coeficientes_grp = coeficientes_grp.groups()
        # print(coeficientes_grp)
        # tratamento do coeficiente de x1
        if coeficientes_grp[1] != None:
            if coeficientes_grp[2] == None:
                coeficiente_x1 = 1.0
            else:
                coeficiente_x1 = float(coeficientes_grp[2])
            if coeficientes_grp[0] == '-':
                coeficiente_x1 *= -1
        else:
            coeficiente_x1 = 0.0
        # tratamento do coeficiente de x2
        if coeficientes_grp[3] != None:
            if coeficientes_grp[5] == None:
                coeficiente_x2 = 1.0
            else:
                coeficiente_x2 = float(coeficientes_grp[5])
            if coeficientes_grp[4] == '-':
                coeficiente_x2 *= -1
        else:
            coeficiente_x2 = 0.0
        coeficientes = [coeficiente_x1, coeficiente_x2,coeficientes_grp[6],float(coeficientes_grp[7])]
        
        retorno.append(coeficientes)
    return retorno

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))