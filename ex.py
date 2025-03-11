import matplotlib.pyplot as plt

# Dados fornecidos
torque = [0.378, 0.494, 0.613, 0.645, 0.842, 0.957, 1.059, 1.157, 1.272, 1.371, 1.466, 1.545, 1.630, 1.705, 1.773, 1.825]
rpm = [1820, 1803, 1789, 1778, 1767, 1755, 1746, 1738, 1731, 1725, 1715, 1708, 1702, 1698, 1694, 1690]

# Criando o gráfico
plt.figure(figsize=(8, 6))
plt.plot(torque, rpm, marker='o', linestyle='-', color='b', label='Curva Torque x RPM')

# Configurando os eixos
plt.xlabel("Torque (N·m)")
plt.ylabel("RPM")
plt.title("Relação entre Torque e RPM")
plt.legend()
plt.grid(True)

# Ajustando escala do eixo Y
plt.ylim(1400, 1850)

# Exibindo o gráfico
plt.show()
