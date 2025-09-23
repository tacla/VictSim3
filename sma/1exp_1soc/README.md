# 1 exp 1 soc: Explorador aleatório e um socorrista em DFS
Este exemplo apresenta um agente explorador que caminha aleatoriamente pelo ambiente. Ele constrói um mapa da região explorada contendo os obstáculos e as vítimas. Em seguida, o explorador passa o mapa para o socorrista. Posteriormente, o socorrista caminha usando a busca em profundidade (DFS) dentro da região descoberta, tentando resgatar as vítimas encontradas.

## Como usar:
- copie os arquivos explorer.py, rescuer.py e main.py para alguma 'pasta'
- copie a pasta config_ag_1 para a 'pasta'
- copie a pasta 'vs' para dentro da 'pasta'

Você deverá obter esta estrutura:
- pasta
-- main.py
-- rescuer.py        
-- explorer.py
-- config_ag
  --- explorer_1.txt    # configuração para o explorador 1
  --- rescuer_1.txt     # configuração para o socorrista 1
-- vs
--- abstract_agent.py
--- constants.py
--- environment.py
--- physical_agent.py
