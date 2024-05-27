# Conferência de Caixas

## Descrição do Projeto

Este projeto foi desenvolvido para automatizar parcialmente a rotina de conferência dos caixas de pagamento pelo financeiro, reduzindo o tempo necessário para realizar etapas demoradas e repetitivas.

Projetado especificamente para processar os relatórios e recibos do sistema SIGA da Activesoft, ele pode necessitar de adaptações para ser utilizado com outros sistemas.

Este projeto utiliza técnicas como OCR (Reconhecimento Óptico de Caracteres), expressões regulares, leitura de PDF e manipulação do sistema de arquivos para garantir a precisão e segurança no processamento das informações.

## Funcionalidades Principais

### 1: Criar estrutura de pastas para os caixas
O sistema gera toda a hierarquia de pastas a serem utilizadas pelos caixas para anexarem os comprovantes e relatórios do caixa dia-a-dia, seguindo o padrão:

```plaintext
Conferir/
├── operador/
│   ├── yyyy/
│   │   ├── MM-MES
│   │   │   ├── 01
│   │   │   │   ├── Relação de movimentações por abertura de caixa.pdf
│   │   │   │   ├── [comprovantes].pdf
│   │   │   │   ├── [_arquivos_conferencia]
│   │   │   ├── ...
│   │   │   ├── 31
Conferido/
├── operador/
│   ├── yyyy/
│   │   ├── MM-MES
│   │   │   ├── 01
│   │   │   │   ├── Relação de movimentações por abertura de caixa.pdf
│   │   │   │   ├── [comprovantes].pdf
│   │   │   │   ├── [_arquivos_conferencia]
│   │   │   ├── ...
│   │   │   ├── 31
```

### 2: Padronizar a nomenclatura de pastas e arquivos
Ocasionalmente um operador ou outro não utiliza a nomenclatura certa para poder executar a automação, esta etapa realiza a normatização dessas nomenclaturas para o sistema funcionar corretamente.

### 3: Verificação mensal de um caixa

Ao informar os parâmetros do operador, mês e ano, o sistema realiza a verificação dos caixas, conferindo relatórios, comprovantes, renomeando arquivos e gerando os arquivos necessários para a conclusão da conferência manual. Este processo minimiza consideravelmente o tempo necessário para a conferência.

**Etapas**

1. **Verificação de Pastas Mensais**: Na pasta correspondente ao mês, o sistema verifica a existência dos dias de caixas, comparando as pastas com o relatório mensal do sistema SIGA. Em caso de inconsistência, são gerados arquivos de conferência.
2. **Verificação Diária**: Cada dia é verificado de forma isolada, fazendo a leitura do relatório de movimentação de caixa e extraindo informações sobre retiradas, pagamentos em cartão e online (PIX/Transferências).
3. **Processamento de Comprovantes**: Utiliza OCR para extrair informações textuais de documentos escaneados, cada arquivo de comprovante anexado ao caixa é processado, identificando a qual movimentação se refere, o tipo (dinheiro, cartão, online) e as informações do recibo do cartão, quando existente.
4. **Renomeação de Recibos**: Uma vez que o recibo é identificado, ele é renomeado com o número da sua movimentação no caixa.
5. **Geração de Arquivos de Conferência**: Por fim, são gerados os arquivos de conferência necessários.


## Configuração do Ambiente de Desenvolvimento

1. **Instalar Dependências do Sistema**:
   - Instale o Tesseract OCR e o Poppler (necessário para manipulação de PDFs).

   **Para Windows**:
   - Baixe e instale o Tesseract [aqui](https://github.com/UB-Mannheim/tesseract/wiki).
   - Baixe e instale o Poppler [aqui](https://github.com/oschwartz10612/poppler-windows).

   **Para Ubuntu**:
   ```bash
   sudo apt-get install tesseract-ocr
   sudo apt-get install poppler-utils
   ```

2. **Clonar o Repositório**:
   ```bash
   git clone <url-do-repositorio>
   cd ConferenciaCaixa
   ```

3. **Instalar Dependências com Pipenv**:
   ```bash
   pipenv install
   pipenv shell
   ```

4. **Configurar Variáveis de Ambiente**:
   - Crie um arquivo `.env` na pasta `src` com as seguintes variáveis:
     ```
     BASE_FOLDER=<caminho raiz onde estão os arquivos dos caixas>
     TESSERACT_CMD=<caminho onda está instalado o tesseract>
     ```

5. **Executar o Script Principal**:
   ```bash
   python src/main.py
   ```


---

Este projeto automatiza processos repetitivos, garantindo maior eficiência, segurança e precisão nas operações de conferência dos caixas da empresa.