# Clínica API Client

Ferramenta em Python desenvolvida para extrair dados da agenda de eventos do sistema de uma clínica, estruturando-os em formato legível e pronto para análise.

# Sobre o Projeto

A ideia inicial era realizar a coleta dos dados por web scraping, capturando diretamente as informações exibidas na interface web.  
No entanto, após análise mais profunda, identificou-se que o sistema disponibiliza um endpoint que permite o consumo dos dados de forma direta, mais eficiente e confiável.  

Com isso, a solução evoluiu de um scraper para um cliente de API, simplificando a manutenção e reduzindo riscos de quebra caso o layout da página fosse alterado.

Em resumo, este projeto:  
- Consulta os dados de agenda/eventos via API.  
- Estrutura os resultados em DataFrame (pandas).  
- Permite exportação para Excel.  
- Pode ser integrado em outros sistemas de análise ou relatórios.  

# Funcionalidades

- Conexão direta com a API da Clínica  
- Filtro por intervalo de datas  
- Retorno em DataFrame  
- Exportação já formatada para arquivos CSV/Excel
- Interface gráfica para autenticar, selecionar o período e gerar o arquivo  

# Status do Projeto

Atualmente em versão inicial, com foco em consumo de dados da agenda

Possíveis atualizações futuras:
- GUI para autenticação e seleção de período - DONE!
- Suporte a outros endpoints  
- Integração com dashboards

# TODO

- GUI para autenticação e seleção de período - DONE!