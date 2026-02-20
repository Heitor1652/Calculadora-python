print("=== CALCULADORA ===")
print("+")
print("-")
print("X")
print("÷")
opcao = input("escolha uma opção:")
n1 = float(input("digite o primeiro número"))
n2 = float(input("digite o segundo número"))
if opcao == "+":
  resultado = n1 + n2
  print("resultado:", resultado)
elif opcao == "-":
  resultado = n1 - n2
  print("resultado:", resultado)
elif opcao == "X":
  resultado = n1 * n2
  print("resultado:", resultado)
elif opcao == "÷":
  resultado = n1 / n2
  print("resultado:", resultado)
else:
  print("opção inválida")
  