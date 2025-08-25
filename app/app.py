# Importing libs nativas
import os

# Importing third-party libraries
import streamlit as st
from crewai import Agent, Crew, Task
from crewai.process import Process
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()


# Page configuration
st.set_page_config(page_title="Terraform AI", page_icon=":100:", layout="wide")

st.title("🤖 Gerador IA de código para Terraform")
st.markdown(
    """Esta aplicação utiliza um agente de IA especializado para converter suas
    descrições em código Terraform (HCL) pronto para uso."""
)


# Configuring CrewAI Agent
try:
    openai_llm = ChatOpenAI(model="gpt-4-turbo", api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    st.error(f"Erro ao inicializar o modelo de linguagem: {e}" "Verifique suas credenciais e tente novamente!")
    openai_llm = None


# Defining AI Agent
terraform_expert = Agent(
    role="Especialista Sênior em Infraestrutura como Código usando Terraform",
    goal="Criar scripts Terraform precisos, eficientes e seguros com base nos requisitos do usuário.",
    backstory=(
        """Você é um engenheiro de DataOps altamente experiente com uma década de experiência na automação
        de provisionamento de infraestrutura na nuvem usando Terraform. Você tem um profundo conhecimento
        dos provedores de nuvem como AWS, GCP e Azure, e é mestre em escrever código HCL (Hashicorp
        Configuration Language) limpo, modular e reutilizável. Sua missão é traduzir descrições de alto
        nível da infraestrutura desejada em código Terraform pronto para produção."""
    ),
    verbose=True,
    allow_delegation=False,
    llm=openai_llm,
)


# Configuring User Interface
st.header("Descreva a Infraestrutura Desejada")

prompt = st.text_area(
    label="Forneça um prompt claro e detalhado. Quanto mais específico você for, melhor será o resultado.",
    height=150,
    placeholder="""Exemplo: Crie o código IaC com Terraform para criar um bucket S3 na AWS com o nome 'dsa-bucket-super-seguro-12345,
    com versionamento e criptografia SSE-S3 habilitados.""",
)

if st.button(label="Gerar Script Terraform", type="primary", disabled=(not openai_llm)):
    if prompt:
        with st.spinner("O agente de IA está trabalhando... Aguarde um momento!"):
            try:
                # Defining the task for agent with base user prompt
                terraform_task = Task(
                    description=(
                        """Com base na seguint solicitação do usuário, gere um script Terraform completo e funcional.
                        A saída deve conter o bloco de código HCL e instruções detalhadas para a escrita do código.
                        O código deve ser bem formatado e pronto para ser salvo em um arquivo .tf.\n\n"""
                        f"Solicitação do Usuário: '{prompt}'"
                    ),
                    expected_output="""Um bloco de código contendo o script Terraform (HCL) e todas as instruções detalhadas do
                    desenvolvimento do código.""",
                    agent=terraform_expert,
                )

                # Creates and Executes the equip (Crew)
                terraform_crew = Crew(agents=[terraform_expert], tasks=[terraform_task], process=Process.sequential, verbose=True)

                # Start the process and get the result
                result = terraform_crew.kickoff()

                # Display the result
                st.header("Resultado Gerado")
                st.code(result, language="terraform")
                st.success("Script gerado com sucesso!")

            except Exception as e:
                st.error(f"Ocorreu um erro durante a execução: {e}")
    else:
        st.warning("Por favor, insira uma descrição da infraestrutura para gerar o script.")

st.markdown("---")
st.markdown(
    """Construído com [Streamlit](https://streamlit.io/) e [CrewAI](https://www.crewai.com/)
    por [Jadeson Bruno Albuquerque da Silva](https://github.com/JadesonBruno)"""
)
