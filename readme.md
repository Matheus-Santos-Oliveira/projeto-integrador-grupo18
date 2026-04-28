# Projeto-Integrador-Grupo18

## Integrantes

- João Paulo da Silva Barbosa
- Matheus de Oliveira Santos
- Murilo de Oliveira Santos


## Base de dados

A base de dados utilizada foi obtida no Kaggle, intitulada Spotify User Behavior and Pattern, contendo cerca de 50 mil registros que simulam o comportamento de usuários em uma plataforma de streaming de música semelhante ao Spotify.

A partir desses dados, o objetivo da análise é identificar padrões de engajamento, satisfação, adição de futuras funções para melhorar a aprovação dos usuários, conversão para planos premium, considerando variáveis como tempo de escuta, preferências musicais, funcionalidades mais desejadas pelos usuários (analisadas a partir de variáveis qualitativas do dataset) e interação com anúncios. Dessa forma, busca-se gerar insights que auxiliem na compreensão da experiência do usuário e apoiem estratégias de retenção e monetização.


## Planejamento do processo de ETL


### Semana 1 – Extração e organização dos dados

**Responsável:** Matheus

- Leitura do dataset com Pandas  
- Alocação da estrutura da base original na pasta data  
- Documentação da estrutura da base no README  

#### 📚 Dicionário de Dados

user_id
- Tipo: inteiro
- Descrição: Identificador único do usuário.

country
- Tipo: texto
- Descrição: País de origem do usuário.

age
- Tipo: inteiro
- Descrição: Idade do usuário.

signup_date
- Tipo: data (string no dataset original)
- Descrição: Data de cadastro do usuário na plataforma.

subscription_type
- Tipo: texto
- Descrição: Tipo de plano do usuário (ex: Free, Premium).

subscription_status
- Tipo: texto
- Descrição: Status da assinatura (ex: ativa, cancelada).

months_inactive
- Tipo: inteiro
- Descrição: Número de meses em que o usuário ficou inativo.

inactive_3_months_flag
- Tipo: booleano (0 ou 1 no dataset)
- Descrição: Indica se o usuário ficou inativo por 3 meses ou mais.

ad_interaction
- Tipo: texto
- Descrição: Indica se houve interação com anúncios.

ad_conversion_to_subscription
- Tipo: texto
- Descrição: Indica se o usuário converteu para assinatura após anúncio.

music_suggestion_rating_1_to_5
- Tipo: inteiro
- Descrição: Avaliação das recomendações de música (escala de 1 a 5).

avg_listening_hours_per_week
- Tipo: decimal
- Descrição: Média de horas de uso da plataforma por semana.

favorite_genre
- Tipo: texto
- Descrição: Gênero musical preferido do usuário.

most_liked_feature
- Tipo: texto
- Descrição: Funcionalidade favorita da plataforma.

desired_future_feature
- Tipo: texto
- Descrição: Funcionalidade que o usuário gostaria que fosse adicionada.

primary_device
- Tipo: texto
- Descrição: Dispositivo principal utilizado (ex: mobile, desktop).

playlists_created
- Tipo: inteiro
- Descrição: Número de playlists criadas pelo usuário.

avg_skips_per_day
- Tipo: inteiro
- Descrição: Média de músicas puladas por dia.

### Semana 2 – Limpeza e tratamento dos dados

**Responsável:** Matheus e Murilo

- Verificação de valores nulos
- Verificação de duplicidades
- Análise de inconsistências categóricas
- Conversão de tipos de dados
- Análise de outliers

Nesta etapa foi realizado o processo de ETL para preparação dos dados de comportamento de usuários, incluindo análise de consistência e tratamento das variáveis. Foram aplicados quartis (Q1 e Q3) e o intervalo interquartil (IQR) para identificação de outliers nas variáveis numéricas relacionadas ao comportamento e uso, como idade, horas médias de escuta semanal, número de playlists criadas, tempo de inatividade e skips diários, utilizando uma heurística baseada na porcentagem de valores extremos para avaliar seu impacto nas etapas posteriores da análise. Também foi realizada verificação de inconsistências em variáveis categóricas como país, tipo de assinatura, gênero favorito, dispositivo principal e preferências de recursos, por meio da normalização de texto para identificação de diferenças de escrita e capitalização, não sendo identificadas inconsistências semânticas relevantes. No ETL foram realizadas conversões de tipos de dados, incluindo transformação de datas de cadastro para datetime, variáveis categóricas para category e variáveis binárias de interação e conversão de anúncios (Yes/No) para valores booleanos. Não foi necessária uma limpeza profunda dos dados, uma vez que não foram identificados valores nulos, registros duplicados ou inconsistências estruturais relevantes no conjunto analisado.

### Semana 3 – Transformações e enriquecimento

**Responsável:** Murilo 

**Criação de novas colunas:**

- Faixa etária  
- Tipo de usuário (heavy/casual)  
- Grupo de anúncio  

**Criação de métricas derivadas:**

- Média de tempo de escuta
- Funções mais pedidas
- Média de satisfação  

- Agrupamentos e agregações  


### Semana 4 – Modelagem e carga

**Responsável:** João 

- Estruturação da tabela final (modelo analítico)  
- Exportação dos dados tratados (CSV ou banco)  
- Validação da integridade dos dados  
- Preparação da base para o dashboard  


### Semana 5 – Planejamento do dashboard e análise

**Responsável:** Todos

- Definição dos KPIs  

**Criação dos gráficos:**

- Gêneros mais ouvidos
- Funções mais pedidas
- Tempo de escuta por tipo de assinatura  
- Impacto dos anúncios na satisfação  
- Conversão para premium  
- Relação entre skips e satisfação  

- Construção do dashboard (Power BI ou similar)  
- Interpretação dos resultados e geração de insights  


### Semana 6 (meia semana) – Finalização e documentação

**Responsáveis:** Matheus, Murilo e João

- Revisão geral do projeto  
- Ajustes no dashboard  
- Escrita final do README  
- Organização do repositório  
- Preparação para apresentação  


### Conclusão

Consideraremos como métricas e indicadores o tempo médio de escuta semanal, a satisfação média dos usuários, a média de músicas puladas por dia (skips), a taxa de conversão para planos premium, o total de usuários e o percentual de interação com anúncios, permitindo analisar o engajamento, a experiência do usuário e os fatores associados à monetização da plataforma, incluindo a relação entre a exposição a anúncios e a conversão para planos premium.

A integração dessas métricas possibilita compreender o comportamento dos usuários em diferentes níveis de interação com a plataforma, identificando padrões de uso, satisfação e retenção. Além disso, a análise das funcionalidades mais desejadas pelos usuários complementa o estudo ao evidenciar oportunidades de melhoria na experiência da plataforma, contribuindo para futuras estratégias de evolução do produto e fortalecimento da proposta de valor dos planos premium.

