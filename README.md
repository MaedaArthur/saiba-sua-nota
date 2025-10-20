# 🎵 Saiba sua Nota - Detector Musical

Um detector musical interativo em Python que identifica notas musicais em tempo real através de captura de áudio. O programa oferece diferentes modos de uso, incluindo um jogo educativo para aprender notas musicais.

## ✨ Funcionalidades

- **🎯 Jogo de Notas**: Modo educativo onde você deve tocar as notas solicitadas
- **🎸 Detector Livre**: Identifica e exibe notas musicais em tempo real
- **🔧 Teste de Captura**: Verifica se o áudio está sendo capturado corretamente
- **🎛️ Seleção de Dispositivo**: Permite escolher diferentes dispositivos de entrada de áudio
- **⚡ Detecção Avançada**: Algoritmo robusto para identificação de frequências fundamentais

## 🚀 Instalação

### Pré-requisitos
- Python 3.7 ou superior
- Microfone ou dispositivo de entrada de áudio

### Dependências
```bash
pip install -r requirements.txt
```

As dependências incluem:
- `sounddevice` - Captura de áudio
- `numpy` - Processamento numérico
- `scipy` - Análise de sinais

## 🎮 Como Usar

### Executar o programa
```bash
python saiba_sua_nota.py
```

### Modos Disponíveis

1. **Jogo de Notas** 🎯
   - O programa escolhe uma nota aleatória
   - Toque a nota solicitada no seu instrumento
   - Complete todas as 12 notas para vencer

2. **Detector Livre** 🎸
   - Identifica e exibe qualquer nota tocada
   - Mostra a frequência em Hz
   - Ideal para afinação e prática

3. **Teste de Captura** 🔧
   - Verifica se o áudio está sendo capturado
   - Mostra o nível RMS do sinal
   - Útil para diagnosticar problemas de áudio

### Controles
- **Q**: Sair do modo atual
- **Ctrl+C**: Interrupção de emergência

## 🎵 Notas Suportadas

O detector reconhece todas as 12 notas musicais:
- **C, C#, D, D#, E, F, F#, G, G#, A, A#, B**

## 🔧 Configurações

### Parâmetros Ajustáveis
- **Taxa de amostragem**: 48kHz (padrão)
- **Duração da captura**: 0.25s (detector livre), 0.3s (jogo)
- **Sensibilidade**: RMS mínimo de 0.005
- **Hold da nota**: 1.8 segundos

### Seleção de Dispositivo
O programa automaticamente detecta o dispositivo de áudio padrão, mas você pode:
- Listar todos os dispositivos disponíveis
- Selecionar um dispositivo específico
- Alterar o dispositivo durante a execução

## 🛠️ Arquitetura Técnica

### Algoritmo de Detecção
1. **Captura de áudio** em tempo real
2. **Análise FFT** para identificar frequências
3. **Detecção de picos** para encontrar harmônicos
4. **Comparação com referências** das notas musicais
5. **Cálculo de distância logarítmica** para melhor precisão

### Estrutura do Código
- **Captura de áudio**: `capturar_audio()`
- **Detecção de frequência**: `detectar_frequencia_fundamental_avancado()`
- **Gerenciamento de dispositivos**: `obter_dispositivo_padrao()`
- **Modos de jogo**: `jogar_nota_adaptado()`, `modo_detector_livre()`

## 🐛 Solução de Problemas

### Áudio não detectado
- Verifique se o microfone está conectado
- Teste com o modo "Teste de Captura"
- Verifique as permissões de áudio do sistema

### Notas incorretas
- Certifique-se de que o ambiente está silencioso
- Ajuste a sensibilidade se necessário
- Use um instrumento bem afinado

### Erro de dispositivo
- Execute `python saiba_sua_nota.py` e selecione um dispositivo manualmente
- Verifique se o dispositivo está sendo usado por outro programa

## 📋 Requisitos do Sistema

- **Windows**: Funciona nativamente
- **Linux**: Pode precisar de configurações adicionais de áudio
- **macOS**: Compatível com Core Audio

## 🤝 Contribuição

Este é um projeto educacional focado em:
- Detecção musical em tempo real
- Interface simples e intuitiva
- Aprendizado de notas musicais

## 📄 Licença

Projeto educacional de código aberto.

---

**Desenvolvido para aprendizado musical e prática de instrumentos** 🎸🎵