import os
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM

# ---------------------------
# CONFIGURAÇÃO DA PÁGINA (UI)
# ---------------------------
st.set_page_config(page_title="Agente de Estilo de Vida", page_icon="🛍️")
st.header("🛍️ Agente de Comércio por Estilo de Vida")
st.write("Descreva seu estilo de vida (ou hobby) e nossos agentes IA recomendarão os produtos essenciais para você.")

# --- ENTRADA DO USUÁRIO ---
# Modificado de "Tema de Estudo" para "Estilo de Vida"
estilo_de_vida = st.text_input(
    "Seu Estilo de Vida",
    placeholder="Ex.: Andarilho, Gamer, Chef de fim de semana, Minimalista, Pai/Mãe de pet"
)

executar = st.button("Gerar Recomendações")

# ---------------------------
# MELHORIA DE SEGURANÇA (IMPORTANTE)
# ---------------------------
# Carrega a chave de API de forma segura usando o Streamlit Secrets
# O usuário deve criar um arquivo .streamlit/secrets.toml

if "GROQ_API_KEY" not in st.secrets:
    st.error("Erro: A GROQ_API_KEY não foi configurada nos 'Secrets' do Streamlit.")
    st.info("Por favor, crie um arquivo .streamlit/secrets.toml e adicione sua chave: \n\nGROQ_API_KEY = 'sua_chave_gsk_...'")
    st.stop()

api_key = st.secrets["GROQ_API_KEY"]


# ---------------------------
# LÓGICA DE EXECUÇÃO
# ---------------------------
if executar:
    # Validação da entrada
    if not api_key or not estilo_de_vida:
        st.error("Por favor, informe seu estilo de vida para continuar.")
        st.stop()

    # Adiciona um "spinner" para feedback ao usuário
    with st.spinner(f"Nossos especialistas estão analisando o perfil '{estilo_de_vida}'..."):

        # ---------------------------
        # LLM (Groq / Llama 3.3 70B)
        # ---------------------------
        llm = LLM(
            model="groq/llama-3.3-70b-versatile",
            api_key=api_key,
            temperature=0.3
        )
#---------------------------------------------------------------------------------------------------------------------------------------50
        # ---------------------------
        # AGENTES (MODIFICADOS PARA COMÉRCIO)
        # ---------------------------

        # Agente 1: Focado nos itens indispensáveis
        agente_essenciais = Agent(
            role="Analista de Produtos Essenciais",
            goal=(
                "Identificar os 5-7 produtos 'must-have' absolutos para o estilo de vida: {estilo_de_vida}. "
                "Focar no que é indispensável para começar."
            ),
            backstory="Você é um especialista em eficiência e identifica o núcleo de qualquer atividade. Se um iniciante perguntasse 'o que eu REALMENTE preciso?', você daria essa lista.",
            llm=llm, verbose=False
        )

        # Agente 2: Focado em roupas e acessórios
        agente_vestuario = Agent(
            role="Especialista em Vestuário Técnico e Acessórios",
            goal=(
                "Recomendar 5-7 itens de vestuário e acessórios funcionais para {estilo_de_vida}. "
                "Focar na função (ex: impermeável, respirável, etc.)"
            ),
            backstory="Você entende que o conforto e a função da roupa são cruciais. Você sabe a diferença que o material certo (lã merino vs. algodão) faz.",
            llm=llm, verbose=False
        )

        # Agente 3: Focado em tecnologia
        agente_tecnologia = Agent(
            role="Analista de Tecnologia e Gadgets",
            goal="Listar 3-5 gadgets ou itens de tecnologia que elevam a experiência do {estilo_de_vida}.",
            backstory="Você é um 'tech reviewer' focado em encontrar as ferramentas e gadgets que trazem conveniência, segurança ou diversão para o estilo de vida.",
            llm=llm, verbose=False
        )

        # Agente 4: Focado em dicas práticas
        agente_dicas = Agent(
            role="Conselheiro de Estilo de Vida Experiente",
            goal="Dar 5 dicas práticas e curtas (1-2 frases) sobre como comprar ou usar os equipamentos para o {estilo_de_vida}.",
            backstory="Você é um veterano nesse estilo de vida. Você dá 'pro-tips' que só a experiência traz, ajudando a evitar erros comuns de compra.",
            llm=llm, verbose=False
        )

#---------------------------------------------------------------------------------------------------------------------------------------------50
        # ---------------------------
        # TAREFAS (MODIFICADAS PARA COMÉRCIO)
        # ---------------------------
        t_essenciais = Task(
            description=(
                "TAREFA: PRODUTOS ESSENCIAIS\n"
                "Liste os 5-7 itens essenciais para {estilo_de_vida}. "
                "Use bullets. Para cada item, explique em 1 frase curta por que ele é essencial. "
                "Ex: '* Bota de Caminhada: Essencial para proteger os tornozelos e...'"
            ),
            agent=agente_essenciais,
            expected_output="Uma lista (bullet points) de 5-7 itens essenciais e sua justificativa de 1 frase."
        )

        t_vestuario = Task(
            description=(
                "TAREFA: VESTUÁRIO E ACESSÓRIOS\n"
                "Liste 5-7 itens de vestuário ou acessórios funcionais para {estilo_de_vida}. "
                "Use bullets. Seja específico sobre a função. (Ex: 'Jaqueta Impermeável/Respirável', 'Meias de lã merino')."
            ),
            agent=agente_vestuario,
            expected_output="Uma lista (bullet points) de 5-7 itens de vestuário e sua função."
        )

        t_tecnologia = Task(
            description=(
                "TAREFA: GADGETS E TECNOLOGIA\n"
                "Liste 3-5 gadgets ou itens tecnológicos úteis para {estilo_de_vida}. "
                "Use bullets. Explique o que o gadget faz em 1 frase."
            ),
            agent=agente_tecnologia,
            expected_output="Uma lista (bullet points) de 3-5 gadgets e sua função."
        )

        t_dicas = Task(
            description=(
                "TAREFA: DICAS DE EXPERIENTE\n"
                "Escreva 5 dicas curtas (1-2 frases) para um {estilo_de_vida} sobre como comprar ou usar os equipamentos. "
                "Ex: '* Dica: Sempre experimente mochilas com peso dentro da loja.'"
            ),
            agent=agente_dicas,
            expected_output="Uma lista numerada de 5 dicas curtas e práticas."
        )

#-------------------------------------------------------------------------------------------------------------------------------50
        # ---------------------------
        # ORQUESTRAÇÃO (A EQUIPE)
        # ---------------------------
        # Removemos a lógica condicional; queremos todas as recomendações sempre.
        agents = [agente_essenciais, agente_vestuario, agente_tecnologia, agente_dicas]
        tasks = [t_essenciais, t_vestuario, t_tecnologia, t_dicas]

        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
        )

        # --- EXECUTAR O CREW ---
        crew.kickoff(inputs={
            "estilo_de_vida": estilo_de_vida,
        })

        # ---------------------------
        # EXIBIÇÃO (Resultados na UI)
        # ---------------------------
        
        # Coleta os resultados de cada tarefa
        essenciais_out = getattr(t_essenciais, "output", None) or getattr(t_essenciais, "result", "") or ""
        vestuario_out = getattr(t_vestuario, "output", None) or getattr(t_vestuario, "result", "") or ""
        tecnologia_out = getattr(t_tecnologia, "output", None) or getattr(t_tecnologia, "result", "") or ""
        dicas_out = getattr(t_dicas, "output", None) or getattr(t_dicas, "result", "") or ""

        # Modifica as abas para refletir as novas categorias
        aba_essenciais, aba_vestuario, aba_tecnologia, aba_dicas = st.tabs(
            ["🎒 Essenciais", "👕 Vestuário", "📱 Gadgets", "💡 Dicas"]
        )

        with aba_essenciais:
            st.markdown(essenciais_out)
        with aba_vestuario:
            st.markdown(vestuario_out)
        with aba_tecnologia:
            st.markdown(tecnologia_out)
        with aba_dicas:
            st.markdown(dicas_out)