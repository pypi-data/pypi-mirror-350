# MessageBoxWin32
```
Este pacote permite criar caixas de diálogo do Windows usando a função MessageBox da API do Windows, sem depender de Tkinter. 

É ideal para aplicações que precisam de uma interface simples de alerta ou confirmação no Windows.

Esta biblioteca depende apenas do CTYPES, que vem instalado por padrão junto do Python.

Ressaltando que a mesma é para uso apenas em ambiente Windows.
```
    
Métodos disponíveis:
- `exibirMensagem`: Exibe uma caixa de mensagem simples com um botão OK.
- `exibirMensagemAtencao`: Exibe uma caixa de mensagem com um ícone de aviso.
- `exibirMensagemInformacao`: Exibe uma caixa de mensagem com um ícone de informação.
- `exibirMensagemErro`: Exibe uma caixa de mensagem com um ícone de erro.
- `exibirMensagemQuestionamento`: Exibe uma caixa de mensagem com opções de ação, como OK, Cancelar, Sim, Não, etc.

Parametros Gerais:
- `mensagem`: A mensagem a ser exibida na caixa de diálogo.
- `titulo`: O título da caixa de diálogo.

Parametros do Método `exibirMensagemQuestionamento`:
- `acao`: Define os tipos de ações que o usuário pode tomar.

- O parâmetro `acao` pode ser:


  - **`1`**: OK e Cancelar
  - **`2`**: Sim, Não e Cancelar
  - **`3`**: Sim e Não
  - **`4`**: Tentar Novamente e Cancelar
  - **`5`**: Anular, Tentar Novamente e Ignorar
  - **`Qualquer outro valor`**: OK e Cancelar

Retorno Geral:
- Retorna um inteiro ao clicar no OK ou fechar a janela.

Retorno do Método `exibirMensagemQuestionamento`:

- Dependendo da ação escolhida, o retorno pode ser:
  - **`0`**: Se o usuário clicar em Cancelar, Não, Anular ou Ignorar
  - **`1`**: Se o usuário clicar em OK ou Sim
  - **`2`**: Se o usuário clicar em Tentar Novamente