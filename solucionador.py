import matplotlib, matplotlib.pyplot as plt, numpy as np, io, base64
# A linha abaixo evita o erro RuntimeError: main thread is not in main loop
matplotlib.use('agg')

class Restricao:
  SINAL_IGUAL = 0
  SINAL_MENOR = 1
  SINAL_MAIOR = 2
  SINAL_MENOR_IGUAL = 3
  SINAL_MAIOR_IGUAL = 4
  def __init__(self, coeficiente_x1:float, coeficiente_x2:float, desigualdade:str, constante=0.0):
    if (coeficiente_x1 == 0 and coeficiente_x2 == 0):
      raise Exception("Ao menos um dos coeficientes deve ser diferente de zero.")
    # ax1 + bx2 = c, logo, bx2 = -ax1 + c
    self.a = coeficiente_x1
    self.b = coeficiente_x2
    self.c = constante
    self.sinal_grafico = desigualdade
    if desigualdade == '=':
      self.sinal = Restricao.SINAL_IGUAL
    elif desigualdade == '<':
      self.sinal = Restricao.SINAL_MENOR
    elif desigualdade == '>':
      self.sinal = Restricao.SINAL_MAIOR
    elif desigualdade == '<=':
      self.sinal = Restricao.SINAL_MENOR_IGUAL
    elif desigualdade == '>=':
      self.sinal = Restricao.SINAL_MAIOR_IGUAL

  '''
  Calcula a interseção entre a restrição e outra passada como parâmetro
  '''
  def intersecao(self, L2) -> tuple:
    # a linha é uma reta horizontal
    if(self.a == 0):
      # a linha comparada também é uma reta horizontal
      if(L2.a == 0):
        return (-1,-1)
      y=self.c/self.b
      x=(L2.c - L2.b*y)/L2.a
    # a linha é uma reta vertical
    elif(self.b == 0):
      if(L2.b == 0):
        return (-1,-1)
      x=self.c/self.a
      y=(L2.c-L2.a*x)/L2.b
    elif(self.a == L2.a and self.b == L2.b):
      return (-1,-1)
    else:  
      x=((self.b*L2.c)-(L2.b*self.c))/((L2.b*self.a*-1)-(self.b*L2.a*-1))
      y=(-1*self.a*x+self.c)/self.b
    return (x,y)

  '''
  Calcula a interseção da restrição com o eixo x1
  '''
  def intersecaox(self) -> tuple:
    if self.a == 0:
      return (-1,-1)
    elif self.b == 0:
      return (self.c/self.a,0)
    else:
      return self.intersecao(Restricao(1,0,Restricao.SINAL_IGUAL,0))

  '''
  Calcula a interseção da restrição com o eixo x2
  '''
  def intersecaoy(self) -> tuple:
    if self.b == 0:
      return (-1,-1)
    elif self.a == 0:
      return (0,self.c/self.b)
    else:
      return self.intersecao(Restricao(0,1,Restricao.SINAL_IGUAL,0))

  '''
  Calcula a interseção da restrição com os eixos x1 e x2.
  A coordenada de retorno (x1,x2) representa os pontos (x1,0) e (0,x2)
  '''
  def intersecaoxy(self) -> tuple:
    if( self.a==0 ):
      return self.intersecaoy()
    elif( self.b==0 ):
      return self.intersecaox()
    else:
      int_x = self.intersecaox()
      int_y = self.intersecaoy()

      return (int_y[0],int_x[1])


class Solucionador:
  OBJETIVO_MAXIMIZAR = 'MAX'
  OBJETIVO_MINIMIZAR = 'MIN'
  def __init__(self, coeficiente_x1:float, coeficiente_x2:float):
    self.a = coeficiente_x1
    self.b = coeficiente_x2
    self.restricoes = []
    self.vertices = []

  def adicionar_restricao(self, restricao: Restricao):
    self.restricoes.append(restricao)

  def ponto_eh_factivel(self, ponto: tuple) -> bool:
    if len(ponto) != 2:
      raise Exception("Parâmetro inválido.")
    if(ponto[0] < 0 or ponto[1]<0):
      # Ponto não satisfaz a condição x1,x2 >= 0
      return False
    for r in self.restricoes:
      if r.sinal == Restricao.SINAL_IGUAL:
        restricao_satisfeita = r.a*ponto[0] + r.b*ponto[1] == r.c
      elif r.sinal == Restricao.SINAL_MENOR:
        restricao_satisfeita = r.a*ponto[0] + r.b*ponto[1] < r.c
      elif r.sinal == Restricao.SINAL_MAIOR:
        restricao_satisfeita = r.a*ponto[0] + r.b*ponto[1] > r.c
      elif r.sinal == Restricao.SINAL_MENOR_IGUAL:
        restricao_satisfeita = r.a*ponto[0] + r.b*ponto[1] <= r.c
      elif r.sinal == Restricao.SINAL_MAIOR_IGUAL:
        restricao_satisfeita = r.a*ponto[0] + r.b*ponto[1] >= r.c
      if not restricao_satisfeita:
        return False
    return True

  def calcular_vertices(self, force = False):
    if len(self.vertices) > 0 and not force:
      return

    for i,r in enumerate(self.restricoes):
      vertice_xy = r.intersecaoxy()
      if self.ponto_eh_factivel((0.0,vertice_xy[1])):
        self.vertices.append((0.0,vertice_xy[1]))
      if self.ponto_eh_factivel((vertice_xy[0],0.0)):
        self.vertices.append((vertice_xy[0],0.0))
      for j in range(len(self.restricoes) - (i+1)):
        vertice = r.intersecao(self.restricoes[i+j+1])
        if self.ponto_eh_factivel(vertice):
          self.vertices.append(vertice)

  def calcular_valor_funcao(self, ponto: tuple):
    return self.a*ponto[0] + self.b*ponto[1]

  def solucao_otima(self, objetivo):
    self.calcular_vertices()
    valor_funcao = 0
    sol_otima = (-1,-1)
    for i,v in enumerate(self.vertices):
      valor_local = self.calcular_valor_funcao(v)
      if i == 0:
        sol_otima = v
        valor_funcao = valor_local
      else:
        if (objetivo == self.OBJETIVO_MAXIMIZAR and valor_local > valor_funcao) or (objetivo == self.OBJETIVO_MINIMIZAR and valor_local < valor_funcao):
          sol_otima = v
          valor_funcao = valor_local
    return sol_otima,valor_funcao

  def maximoxy(self):
    max_x = 0
    max_y = 0
    for v in self.vertices:
      if v[0] > max_x:
        max_x = v[0]
      if v[1] > max_y:
        max_y = v[1]
    return (max_x,max_y)

  def imprimir_dados_problema(self,objetivo):
    print('Problema de Programação Linear')
    print('Maximizar: ' if objetivo == self.OBJETIVO_MAXIMIZAR else 'Minimizar: ')
    print(f'  Z={self.a}x1 + {self.b}x2')
    print('Sujeito a:')
    for r in self.restricoes:
      sinal = '='
      if r.sinal == Restricao.SINAL_MAIOR:
        sinal = '>'
      elif r.sinal == Restricao.SINAL_MAIOR_IGUAL:
        sinal = '>='
      elif r.sinal == Restricao.SINAL_MENOR:
        sinal = '<'
      elif r.sinal == Restricao.SINAL_MENOR_IGUAL:
        sinal = '<='

      print(f'  {r.a}x1 + {r.b}x2 {sinal} {r.c}')
    print('Tal que: \n  x1, x2 >= 0')
    print('Vértices:')
    for v in self.vertices:
      print(f'  Z{v}={self.calcular_valor_funcao(v)}')

  def minimizar(self):
    return self.solucionar(Solucionador.OBJETIVO_MINIMIZAR)

  def maximizar(self):
    return self.solucionar(Solucionador.OBJETIVO_MAXIMIZAR)

  def solucionar(self, objetivo: str) -> dict:
    self.calcular_vertices()
    if len(self.vertices) == 0:
      raise Exception('Não há solução possível para o problema')
    self.imprimir_dados_problema(objetivo)
    solucao_otima,valor_otimo = self.solucao_otima(objetivo)
    print(f'Solução ótima: {solucao_otima}')
    print(f'Valor ótimo:{valor_otimo}')
    imgbase64 = self.plotar(solucao_otima)
    retorno = {
      "objetivo": "maximizar",
      "funcao_objetivo": [self.a, self.b],
      "restricoes": self.restricoes,
      "vertices": self.vertices,
      "solucao_otima": solucao_otima,
      "valor_otimo": valor_otimo,
      "grafico": imgbase64
    }
    return retorno

  def plotar(self, solucao_otima):
    constraints = 1 & 1
    max_x1_x2 = self.maximoxy()
    plt.figure()
    # Plotar restrições
    x1_values = np.linspace(0,int(max(max_x1_x2)+1),200)
    x2_values = np.linspace(0,int(max(max_x1_x2)+1),200)
    x1,x2 = np.meshgrid(x1_values,x2_values)
    for r in self.restricoes:
      if r.sinal == Restricao.SINAL_IGUAL:
        constraints &= (r.a*x1 + r.b*x2 == r.c)
      elif r.sinal == Restricao.SINAL_MENOR:
        constraints &= (r.a*x1 + r.b*x2 < r.c)
      elif r.sinal == Restricao.SINAL_MENOR_IGUAL:
        constraints &= (r.a*x1 + r.b*x2 <= r.c)
      elif r.sinal == Restricao.SINAL_MAIOR:
        constraints &= (r.a*x1 + r.b*x2 > r.c)
      elif r.sinal == Restricao.SINAL_MAIOR_IGUAL:
        constraints &= r.a*x1 + r.b*x2 >= r.c

      if r.a != 0 and r.b != 0:
        ixy = r.intersecaoxy()
        X=[x for x in range( 0, int(ixy[0] + 1) )]
        Y=[(r.c-r.a*x)/r.b for x in X]
        plt.plot(X,Y,label=f'{r.a}x1 + {r.b}x2 = {r.c}')
      elif r.b == 0:
        plt.vlines(r.c/r.a, 0, int(max(max_x1_x2)+1), label=f'{r.a}x1 = {r.c}')
      elif r.a == 0:
        plt.hlines(r.c/r.b, 0, int(max(max_x1_x2)+1), label=f'{r.b}x2 = {r.c}')

    # Preencher região factível
    plt.imshow(
        constraints.astype(int),
        extent=(x1.min(), x1.max(), x2.min(), x2.max()),
        origin='lower',
        cmap='Greys',
        alpha=0.3)

    # Anotar solução ótima
    plt.annotate(
        "S=(" + str(solucao_otima[0]) + "," + str(solucao_otima[1]) + ")",
        xy=solucao_otima
    )

    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.grid(True)
    plt.legend()
    img_stringIOBytes = io.BytesIO()
    plt.savefig(img_stringIOBytes, format='jpg')
    img_stringIOBytes.seek(0)
    img_base64_jpg = base64.b64encode(img_stringIOBytes.read()).decode()
    img_stringIOBytes.close()
    return img_base64_jpg 
    # plt.show()
