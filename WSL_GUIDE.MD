Utilizar o WSL e uma forma rápida de rodar uma distro do Linux

Aqui tem algumas recomendações para utilizar o WSL:

1. Ativar o Control Flow Guard (CFG), deixar a opção "on by default"
2. Ativar o recurso Subsistema do Windows para Linux
3. Instalar o WSL (se necessario) 

- O item 1 pode ser feito ao acessar o Windows Defender: App & browser control > Exploit protection > System Settings > Control Flow Guard (CFG)

- O item 2 poder ser feito executando em modo administrador o powershell e rodando o comando `dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart`

- Para o item 3, ainda no powershell execute o comando `wsl --install`

- Apos a instalação recomendo utilizar a versão 2 do WSL usando o comando `wsl --set-default-version 2`

- Caso ja tenha instalado, use o comando `WSL --install -d Ubuntu` para instalar a distro (distribuição) do Ubuntu

- `Use wsl -l -v` para listar a versão do WSL e as distros

Execute o Ubuntu caso não tenha feito automaticamente e crie seu usuário.
Seu ambiente Linux esta pronto para ser utilizado.
