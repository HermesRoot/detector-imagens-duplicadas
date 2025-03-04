# Detector de Imagens Duplicadas

**Detector de Imagens Duplicadas** é uma ferramenta gráfica para Windows, desenvolvida com `wxPython`, que identifica imagens duplicadas em uma pasta. Oferece opção para exclusão automática e geração de relatórios detalhados.

## 🖥️ Captura de Tela
![Screenshot do HashCheck](https://raw.githubusercontent.com/HermesRoot/detector-imagens-duplicadas/main/screenshot.jpg
)

## ⚡ Características

- Detecção de imagens duplicadas utilizando perceptual hash (pHash).
- Interface gráfica simples e intuitiva.
- Opção para exclusão automática de duplicatas.
- Geração de relatórios completos em `.txt`.
- Configuração de sensibilidade para ajustar a precisão da detecção.
- Suporte aos formatos de imagem: `.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif`.
- Visualização rápida das duplicatas encontradas.
- Histórico e acesso ao último relatório salvo.

## 🔎 Como usar

1. Abra o aplicativo.
2. No menu **Arquivo**, defina a pasta para salvar o relatório (opcional).
3. Clique em **Selecionar Pasta** e escolha a pasta com as imagens.
4. (Opcional) Marque a opção **Excluir automaticamente duplicadas** se quiser remover as cópias.
5. Clique em **Iniciar Verificação**.
6. Aguarde a conclusão e consulte o log e o relatório gerado.
7. Visualize as duplicatas encontradas e abra o relatório diretamente pelo menu.

## 🎛️ Atalhos

| Ação                              | Atalho  |
|------------------------------------|---------|
| Salvar relatório                  | Alt + S |
| Abrir imagens                     | Alt + I |
| Abrir relatórios                  | Alt + R |
| Último relatório                  | Alt + L |
| Limpar log                        | Alt + C |
| Sair                              | Ctrl + Q |
| Configurar sensibilidade          | - |
| Verificar pasta novamente         | - |
| Sobre                             | - |
| Como usar                         | - |

## 📂 Relatório

Após a verificação, um relatório em `.txt` é gerado contendo:

- Data e hora da análise.
- Caminho da pasta analisada.
- Quantidade de duplicatas encontradas.
- Lista de duplicatas e seus respectivos originais.
- Status das imagens (se foram excluídas ou apenas identificadas).

O relatório é salvo automaticamente na pasta escolhida.

## ⚙️ Requisitos

- Python 3.8+
- wxPython
- Pillow
- ImageHash

Para instalar as dependências:

```bash
pip install -r requirements.txt
```

## 📝 Licença

Este projeto está licenciado sob a licença **MIT** — veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👤 Autor

Desenvolvido por **HermesRoot**.  
