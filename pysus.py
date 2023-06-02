from pysus.online_data import SINAN, FTP_Inspect, parquets_to_dataframe
import pandas as pd
import matplotlib.pyplot as plt
import math
SINAN.list_diseases()

"""Após escolher a malária como objeto de estudo, verifica-se os anos de dados disponíveis."""

anos = SINAN.get_available_years('Malaria')
print(anos)

"""Verificando se os dados são preliminares ou finais."""

lu = FTP_Inspect('SINAN').last_update_df()
lu[lu.file_name.str.startswith('MALA')]

"""Escolhendo os dados finais mais recentes = 2022"""

path = SINAN.download('Malaria', int(anos[len(anos)-1]))
df = pd.read_parquet(path)

"""Verificando a aparênia do DataFrame"""

df.to_csv('Malaria.csv', index=False)
df.head()

"""Decodificando a idade:"""

from pysus.preprocessing.decoders import decodifica_idade_SINAN

df['idade'] = decodifica_idade_SINAN(df.NU_IDADE_N)

"""Número de casos de Malária por semana em 2022"""

df.DT_DIGITA = pd.to_datetime(df.DT_DIGITA)
df1 = df.set_index('DT_DIGITA')
df1.ID_AGRAVO.resample('1W').count().plot(grid=True)

"""Número de casos de Malária por mês em 2022"""

df2 = df.set_index('DT_DIGITA')
df2.ID_AGRAVO.resample('1M').count().plot(grid=True)

"""Casos de malária por estado em 2022. Constam no gráfico apenas os ID's dos estados com um número significativo de casos."""

df_estados = df.groupby('SG_UF_NOT').size()

df_estados = df_estados[df_estados >= 20]
df_estados = df_estados.sort_values()

plt.figure(figsize=(12, 6))

df_estados.plot(kind='bar')

plt.xlabel('ID_Estado')
plt.ylabel('Contagem')
plt.title('Gráfico por Estado')
plt.show()

"""Casos de malária por município em 2022. Constam no gráfico apenas os ID's dos municípios com um número significativo de casos."""

df_municipio = df.groupby('ID_MUNICIP').size()

df_municipio = df_municipio[df_municipio >= 20]
df_municipio = df_municipio.sort_values()

plt.figure(figsize=(12, 6))

df_municipio.plot(kind='bar')

plt.xlabel('ID Município')
plt.ylabel('Contagem')
plt.title('Gráfico por Município')
plt.show()

"""Gráfico de casos de malária por faixa etária em 2022."""

df_idades = df.groupby('idade').size()

df_idades = df_idades[df_idades >= 1]

plt.figure(figsize=(12, 6))

plt.hist(df['idade'], bins=range(0, 90, 3), rwidth=0.8)

plt.xlabel('Idade')
plt.ylabel('Contagem')
plt.title('Casos por faixa etária')
plt.xticks(range(0, 90, 3))  
plt.show()

"""Gráfico de casos de malária por gênero em 2022."""

df_sexo = df.groupby('CS_SEXO').size()

df_sexo = df_sexo[df_sexo >= 1]
df_sexo = df_sexo.sort_values()

plt.figure(figsize=(10, 6))

df_sexo.plot(kind='bar')

plt.xlabel('Gêneros')
plt.ylabel('Contagem')
plt.title('Casos de Malária por Gênero')
plt.show()

"""Raça"""

df_raca = df.groupby('CS_RACA').size()

plt.figure(figsize=(10, 6))
df_raca = df_raca.sort_values()

df_raca.plot(kind='bar')

plt.xlabel('Etnia')
plt.ylabel('Contagem')
plt.title('Contagem por Etnia')
plt.show()