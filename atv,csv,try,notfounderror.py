import os
from dataclasses import dataclass
os.system("cls")
#--------------------Classe------------------------------------------------------------------------  
@dataclass
class Paciente:
    nome:str
    idade:int
    altura:float
    cpf:str
    def exibir_dados(self):
        print(f"nome: {self.nome} \nidade: {self.idade} \n altura: {self.altura} \n cpf: {self.cpf}") 

lista_de_pacientes=[]
  #------------------------Laço de repetição e chamar funçao--------------------------------------------------------------------  
for i in range(2):
    paciente=Paciente(
        nome=input("Digite seu nome: "),
        idade=input("Digite sua idade: "),
        altura=float(input("Digite sua altura")),
        cpf=input("Digite seu cpf:")
    ) 
    lista_de_pacientes.append(paciente)
    print() #pular uma linha
#---------------Persistencia de dados .csv -----------------------------------------------------------------------------  
nome_do_arquivo="dados_paciente.csv" 
with open(nome_do_arquivo,"a") as arquivo_pacientes:
    for paciente in lista_de_pacientes:
        arquivo_pacientes.write(f"{paciente.nome},{paciente.idade},{paciente.altura},{paciente.cpf}\n") #faltou esse \n pra a linha por linha
        print("Dados salvos com sucesso")
#-------------------------------------------------------------------------------------------------------------------------
        


#deixar organizado quando salvar o arquivo
# print("\nExibindo lista de pacientes: ")
# for paciente in lista_de_pacientes:
#     paciente.exibir_dados() 


#----------------------------------------------------------------------------------------------
    #cod do prof

    #"r" - read-leitura
    # with open(nome_do_arquivo, "r")as arquivo:
    #     linhas=arquivo.readlines()
    #     for linha in linhas:
    #         print(f"- {linhas.strip()}") 

 #    with open(nome_do_arquivo,"r") as arquivo:
 #     lista_todos_pacientes=arquivo.readline()
 #     for paciente in lista_todos_pacientes:
 #        nome,idade=paciente.strip() .split(",")
 #     dados_paciente=Paciente(nome=nome,idade=int(idade))
 #      lista.append(dados_paciente)
 #     dados_paciente.exibir_dados()
 #     for paciente in lista:
 #        paciente.exibir_dados()
  
  #------------------------------------------------------------------------------------------------------------------------ 
    #cod do chatgpt

    # with open(nome_do_arquivo, "r") as arquivo:
    #  for linha in arquivo:
    #     linha = linha.strip()
        
    #     if not linha:  # ignora linhas vazias
    #         continue
        
    #     nome, idade = linha.split(",")
    #     dados_paciente = Paciente(nome=nome, idade=int(idade))
    #     lista.append(dados_paciente)

    #   # Mostra todos os pacientes carregados
    # for paciente in lista:
    #  paciente.exibir_dados()

    # Garanta que a lista existe antes

 #------------------try e except FileNotFoundError---------------------------------

print("\nExibindo todos os pacientes:")
lista=[]
try:
    with open(nome_do_arquivo,"r",encoding="utf-8") as arquivo:
        lista_todos_pacientes=arquivo.readlines()

        for paciente in lista_todos_pacientes:
            nome,idade,altura,cpf=paciente.strip().split(",")
            dados_paciente=Paciente(nome=nome,idade=int(idade),altura=float(altura),cpf=cpf)
            lista.append(dados_paciente) 

    for paciente in lista:
        paciente.exibir_dados()
        
except FileNotFoundError:
    print("Arquivo nao encontrado")

#----------------------------------------------------------------------------------------------------------------   

# print(f"- {paciente.strip()}")
# except FileNotFoundError:
# print("o arquivo nao foi encontrado.") 

    
#ficar atento a margem e espaço 
#vai ter codigo diferente por que sao programas diferente mas a logica é a mesma 
