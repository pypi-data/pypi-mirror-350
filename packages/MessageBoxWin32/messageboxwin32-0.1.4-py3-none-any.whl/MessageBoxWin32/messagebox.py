import ctypes
import wx

# Botões
MB_OK                = 0x00000000
MB_OKCANCEL          = 0x00000001
MB_ABORTRETRYIGNORE  = 0x00000002
MB_YESNOCANCEL       = 0x00000003
MB_YESNO             = 0x00000004
MB_RETRYCANCEL       = 0x00000005

# Ícones
MB_ICONHAND          = 0x00000010  # Erro
MB_ICONQUESTION      = 0x00000020  # Pergunta
MB_ICONEXCLAMATION   = 0x00000030  # Aviso
MB_ICONASTERISK      = 0x00000040  # Informação

# Outras flags
MB_DEFBUTTON1        = 0x00000000
MB_DEFBUTTON2        = 0x00000100
MB_DEFBUTTON3        = 0x00000200
MB_SYSTEMMODAL       = 0x00001000
MB_TOPMOST           = 0x00040000

# mapeamento de códigos de retorno
IDOK       = 1
IDCANCEL   = 2
IDABORT    = 3
IDRETRY    = 4
IDIGNORE   = 5
IDYES      = 6
IDNO       = 7

_app = wx.App(False)

def exibirMensagem(mensagem: str, titulo: str = "") -> int:
    """
    Exibe uma caixa de mensagem do Windows, apenas com a mensagem, título e um botão de OK.
    :param mensagem: A mensagem a ser exibida na caixa de diálogo.
    :param titulo: O título da caixa de diálogo.
    :return: int - Retorna um inteiro ao clicar no OK ou fechar a janela.    
    """
    flags: int = MB_OK
    return ctypes.windll.user32.MessageBoxW(None, mensagem, titulo, flags)

def exibirMensagemAtencao(mensagem: str, titulo: str = "Atenção!") -> int:
    """
    Exibe uma caixa de mensagem do Windows, com uma mensagem, título, botão de OK e um ícone de aviso.
    :param mensagem: A mensagem a ser exibida na caixa de diálogo.
    :param titulo: O título da caixa de diálogo.
    :return: int - Retorna um inteiro ao clicar no OK ou fechar a janela.    
    """
    flags: int = MB_OK | MB_ICONEXCLAMATION
    return ctypes.windll.user32.MessageBoxW(None, mensagem, titulo, flags)

def exibirMensagemInformacao(mensagem: str, titulo: str = "Informação") -> int:
    """
    Exibe uma caixa de mensagem do Windows, com uma mensagem, título, botão de OK e um ícone de exclamação.
    :param mensagem: A mensagem a ser exibida na caixa de diálogo.
    :param titulo: O título da caixa de diálogo.
    :return: int - Retorna um inteiro ao clicar no OK ou fechar a janela.    
    """
    flags: int = MB_OK | MB_ICONASTERISK
    return ctypes.windll.user32.MessageBoxW(None, mensagem, titulo, flags)

def exibirMensagemErro(mensagem: str, titulo: str = "Erro") -> int:
    """
    Exibe uma caixa de mensagem do Windows, com uma mensagem, título, botão de OK e um ícone de erro.
    :param mensagem: A mensagem a ser exibida na caixa de diálogo.
    :param titulo: O título da caixa de diálogo.
    :return: int - Retorna um inteiro ao clicar no OK ou fechar a janela.    
    """
    flags: int = MB_OK | MB_ICONHAND
    return ctypes.windll.user32.MessageBoxW(None, mensagem, titulo, flags)

def exibirMensagemQuestionamento(mensagem: str, titulo: str = "Erro", acao: str = "1") -> int:
    """
    Exibe uma caixa de mensagem do Windows, com uma mensagem, título, botão de OK e um ícone de interrogação.
    :param mensagem: A mensagem a ser exibida na caixa de diálogo.
    :param titulo: O título da caixa de diálogo.
    :param acao: Define os tipos de ações que o usuário pode tomar
    O parâmetro `acao` pode ser:
    - "1": OK e Cancelar
    - "2": Sim, Não e Cancelar
    - "3": Sim e Não
    - "4": Tentar Novamente e Cancelar
    - "5": Anular, Tentar Novamente e Ignorar
    - Qualquer outro valor: OK e Cancelar


    :return: int - Retorna um inteiro ao clicar no OK ou fechar a janela.  
    Dependendo da ação escolhida, o retorno pode ser:
    - 0: Se o usuário clicar em Cancelar, Não, Anular ou Ignorar
    - 1: Se o usuário clicar em OK ou Sim
    - 2: Se o usuário clicar em Tentar Novamente
    """

    if acao == "1":
        flags: int = MB_OKCANCEL | MB_ICONQUESTION       
    elif acao == "2":
        flags: int = MB_YESNOCANCEL | MB_ICONQUESTION
    elif acao == "3":
        flags: int = MB_YESNO | MB_ICONQUESTION
    elif acao == "4":
        flags: int = MB_RETRYCANCEL | MB_ICONQUESTION
    elif acao == "5":
        flags: int = MB_ABORTRETRYIGNORE | MB_ICONQUESTION
    else:
        flags: int = MB_OKCANCEL | MB_ICONQUESTION      

    validaRetorno = ctypes.windll.user32.MessageBoxW(None, mensagem, titulo, flags)

    if validaRetorno in [IDCANCEL, IDNO, IDABORT, IDIGNORE] :
        # Se o usuário clicar em Cancelar, Não, Anular ou Ignorar, retorna 0
        validaRetorno = 0
    elif validaRetorno in [IDOK, IDYES] :
        # Se o usuário clicar em OK ou Sim, retorna 1
        validaRetorno = 1
    elif validaRetorno in [IDRETRY]:
        # Se o usuário clicar em Tentar Novamente, retorna 2
        validaRetorno = 2

    return validaRetorno

def solicitarTexto(mensagem: str = "Digite algo:", titulo: str = "Entrada de Texto") -> str:
    """
    Exibe uma caixa de diálogo para solicitar entrada de texto do usuário.
    :param mensagem: A mensagem a ser exibida na caixa de diálogo.
    :param titulo: O título da caixa de diálogo.
    :return: str - Retorna o texto inserido pelo usuário ou uma string vazia se o usuário cancelar.
    """

    retorno = wx.GetTextFromUser(message=mensagem, caption=titulo, default_value="")
    return retorno