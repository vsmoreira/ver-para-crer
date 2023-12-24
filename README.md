# Ver Para Crer
Um projeto Python que implementa um método gráfico para resolução de problemas de programação linear com 2 variáveis de decisão e um frontend para utilizar o método e consultar seus resultados.

Aplicação disponível para uso em [ver-para-crer-e578d.web.app](https://ver-para-crer-e578d.web.app)

## Frontend

O frontend foi desenvolvido com o framework [Flask](https://flask.palletsprojects.com). Para rodar o projeto em container, basta fazer o build e rodar a imagem Docker do projeto disponível na pasta server.

    docker build . -t ver-para-crer:latest

Digite o comando abaixo para rodar o container com a imagem construída anteriormente.

    docker run -p 8080:8080 --name ver-para-crer -it ver-para-crer

Para rodar o frontend localmente, é necessário instalar as dependências Flask e matplotlib.

    pip install Flask, matplotlib

É recomendada a utilização de um ambiente Python virtualizado antes de rodar o comando acima. Para tanto, siga as instruções disponiveis na [documentação](https://flask.palletsprojects.com/en/3.0.x/installation/#virtual-environments) do Flask.

## Backend
O backend é composto basicamente pelas classes Solucionador e Restricao presentes no arquivo server/src/solucionador.py.

### Classe Restricao

Define uma restrição linear para o problema de otimização matemática bem como operações para a mesma. Exemplo: ax1 + bx2 <= c

---

Modo de usar

Para instanciar uma nova restrição é necessário passar 4 parâmetros: coeficiente de x1, coeficiente de x2, sinal de igualdade/desigualdade e a constante de restrição.

Valores válidos para o sinal da restrição:

0.   Sinal de igualdade (=)
1.   Sinal menor (<)
2.   Sinal maior (>)
3.   Sinal menor e igual (<=)
4.   Sinal maior e igual (>=)

```
# 4x1 + 8x2 <= 20
r = Restricao(4,8,Restricao.SINAL_MENOR_IGUAL,20)
# x1 <= 3. Neste caso, o coeficinente de x2 deve ser igual a zero
r = Restricao(1,0,Restricao.SINAL_MENOR_IGUAL,3)
# 4x2 >= 20. Neste caso, o coeficiente de x1 deve ser igual a zero
r = Restricao(0,4,Restricao.SINAL_MAIOR_IGUAL,20)
```

### Classe Solucionador

Objeto utilizado para armazenar e solucionar um problema linear de 2 variáveis de decisão utilizando o método gráfico. Os métodos maximizar e minimizar retornam:

*   Função objetivo e restrições
*   Figura com gráfico da região factível
*   Lista de vértices da região factível e o valor da função objetivo aplicado a cada uma delas
*   Solução ótima
*   Valor ótimo da função objetivo
---
Modo de Usar

Para resolver o problema

```
Maximizar: Z = 50x1 + 75x2  
  Sujeito a: 4x1 <= 12
             4x1 + 8x2 <= 20
             8x1 + 20x2 <= 50
   Tal que:  x1, x2 >= 0
```

1.   Instanciar um novo objeto Solucionador com os coeficientes de x2 e de x2;
2.   Adicionar as restrições
3.   Chamar o método de otimização desejado

```
  # Z = 50x1 + 75x2
  s = Solucionador(50,75)
  # Restrição 1: 4x1 <= 12
  s.adicionar_restricao(Restricao(4,0,Restricao.SINAL_MENOR_IGUAL,12))
  # Restrição 2: 4x1 + 8x2 <= 20
  s.adicionar_restricao(Restricao(4,8,Restricao.SINAL_MENOR_IGUAL,20))
  # Restricao 3: 8x1 + 20x2 <= 50
  s.adicionar_restricao(Restricao(8,20,Restricao.SINAL_MENOR_IGUAL,50))
  # Objetivo maximizar
  s.maximizar()
```
