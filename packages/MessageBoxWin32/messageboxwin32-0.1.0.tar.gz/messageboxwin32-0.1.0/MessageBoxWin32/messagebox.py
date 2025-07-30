import ctypes

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
IDYES      = 6
IDNO       = 7
IDRETRY    = 4


def exibirMensagem(mensagem: str, titulo: str = "") -> int:
    flags: int = MB_OK
    """
    Exibe uma caixa de mensagem do Windows, apenas com a mensagem, título e um botão de OK.
    :param mensagem: A mensagem a ser exibida na caixa de diálogo.
    :param titulo: O título da caixa de diálogo.
    :return: int - Retorna um inteiro ao clicar no OK ou fechar a janela.    
    """
    return ctypes.windll.user32.MessageBoxW(None, mensagem, titulo, flags)