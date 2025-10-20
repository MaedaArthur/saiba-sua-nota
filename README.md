# 🎵 Saiba sua Nota - Detector Musical Interativo

Um detector musical completo para aprendizado de notas musicais, com duas versões especializadas: uma para computador com interface de menu e outra para Raspberry Pi com hardware físico dedicado. Projeto educacional open-source para ensino musical.

## ✨ Funcionalidades Principais

- **🎯 Jogo de Notas Educativo**: Sistema gamificado para aprendizado musical
- **🎸 Detecção em Tempo Real**: Identificação instantânea de 12 notas musicais
- **📺 Interface Adaptativa**: Menu no computador ou display LCD no Raspberry Pi
- **🟢 Feedback Visual**: LEDs indicadores e mensagens claras
- **🔧 Múltiplos Modos**: Jogo, detector livre, teste de captura
- **⚡ Algoritmo Avançado**: FFT e análise de frequências fundamentais

## 🖥️ Versões Disponíveis

### 💻 Versão Computador
- **Interface de menu** interativa
- **Múltiplos modos** de uso
- **Seleção de dispositivos** de áudio
- **Ideal para**: Desenvolvimento, teste, uso individual

### 🍓 Versão Raspberry Pi
- **Hardware físico** completo
- **Display LCD** 16x2 com I2C
- **LEDs indicadores** (verde/vermelho)
- **Ideal para**: Ambientes educacionais, instalações fixas

## 🚀 Instalação Rápida

### Versão Computador
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar programa
python saiba_sua_nota.py
```

### Versão Raspberry Pi
```bash
# Instalar dependências
pip3 install -r "Saiba sua nota raspberry pi/requirements.txt"

# Executar com privilégios (necessário para GPIO)
sudo python3 "Saiba sua nota raspberry pi/saiba_sua_nota_raspberry_pi.py"
```

## 🎮 Como Usar

### 💻 Versão Computador

#### Menu Principal:
1. **Jogo de Notas** 🎯 - Modo educativo (recomendado)
2. **Detector Livre** 🎸 - Identificação em tempo real
3. **Teste de Captura** 🔧 - Verificar funcionamento do áudio
4. **Alterar Dispositivo** 🎛️ - Selecionar microfone
5. **Sair** ❌ - Finalizar programa

#### Controles:
- **Q**: Sair do modo atual
- **Ctrl+C**: Interrupção de emergência

### 🍓 Versão Raspberry Pi

#### Interface Física:
1. **Display LCD** mostra "Iniciando jogo..."
2. **Nota alvo** aparece: "Toque: A"
3. **Toque a nota** no instrumento
4. **Feedback visual**:
   - 🟢 **LED Verde**: Acertou a nota
   - 🔴 **LED Vermelho**: Errou a nota
5. **Próxima nota** automática
6. **Reinicialização** após completar todas as 12 notas

## 🎵 Notas Suportadas

O sistema reconhece todas as **12 notas musicais**:
- **C, C#, D, D#, E, F, F#, G, G#, A, A#, B**

### Frequências de Referência:
- **E**: 82.41 Hz, 164.81 Hz, 329.63 Hz, 659.25 Hz
- **A**: 110.00 Hz, 220.00 Hz, 440.00 Hz, 880.00 Hz
- **D**: 146.83 Hz, 293.66 Hz, 587.33 Hz, 1174.66 Hz
- **G**: 98.00 Hz, 196.00 Hz, 392.00 Hz, 784.00 Hz
- **B**: 123.47 Hz, 246.94 Hz, 493.88 Hz, 987.77 Hz
- **E (agudo)**: 329.63 Hz, 659.25 Hz, 1318.51 Hz

## 🔧 Hardware Necessário (Raspberry Pi)

### Componentes Obrigatórios:
- **Raspberry Pi** (3B+, 4B ou superior)
- **Microfone USB ** ou **módulo de áudio**
- **Display LCD 16x2** com interface I2C (PCF8574)
- **2x LEDs** (Verde e Vermelho)
- **2x Resistores** (220Ω para LEDs)
- **Protoboard** e **jumpers**

### Conexões GPIO:
| Componente | GPIO Pin | Função |
|------------|----------|--------|
| LED Verde | GPIO 22 | Indicador de acerto |
| LED Vermelho | GPIO 27 | Indicador de erro |
| Display LCD | I2C (SDA/SCL) | Interface de comunicação |

## 📊 Configurações Técnicas

### Parâmetros do Sistema:
- **Taxa de amostragem**: 48kHz
- **Duração da captura**: 0.25s (computador), 0.3s (Raspberry Pi)
- **Sensibilidade RMS**: 0.005
- **Algoritmo**: FFT com detecção de picos

### Algoritmo de Detecção:
1. **Captura de áudio** em tempo real
2. **Análise FFT** para identificar frequências
3. **Detecção de picos** para encontrar harmônicos
4. **Comparação com referências** das notas musicais
5. **Cálculo de distância logarítmica** para precisão

## 🛠️ Instalação Detalhada

### Versão Computador
```bash
# 1. Instalar dependências
pip install sounddevice numpy scipy

# 2. Executar programa
python saiba_sua_nota.py

# 3. Seguir menu interativo
```

### Versão Raspberry Pi
```bash
# 1. Atualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar dependências do sistema
sudo apt install python3-pip python3-dev python3-rpi.gpio i2c-tools -y

# 3. Habilitar I2C
sudo raspi-config
# Navegue para: Interfacing Options > I2C > Enable

# 4. Instalar dependências Python
pip3 install numpy scipy sounddevice RPi.GPIO RPLCD

# 5. Executar programa
sudo python3 "Saiba sua nota raspberry pi/saiba_sua_nota_raspberry_pi.py"
```

## 🐛 Solução de Problemas

### ❌ Microfone ou módulo de áudio não detectado
**Sintomas**: Erro ao iniciar, sem detecção de áudio
**Soluções**:
- Verifique conexão USB/3.5mm
- Teste com gravador de voz
- Use seleção manual de dispositivo
- Verifique permissões de áudio

### 🔇 Som não detectado
**Sintomas**: RMS sempre 0.0000, sem detecção de notas
**Soluções**:
- Aumente volume do microfone
- Verifique se não está mudo
- Teste com "Teste de Captura"
- Aproxime instrumento do microfone

### 🎵 Detecção incorreta
**Sintomas**: Notas erradas, frequências estranhas
**Soluções**:
- Afine o instrumento primeiro
- Use ambiente mais silencioso
- Verifique qualidade do microfone
- Teste com instrumento diferente

### 🍓 Problemas Raspberry Pi
**Sintomas**: Display LCD não funciona, LEDs não acendem
**Soluções**:
- Verifique conexões I2C (SDA/SCL)
- Confirme endereço I2C: `sudo i2cdetect -y 1`
- Verifique conexões GPIO
- Teste com multímetro

## 📋 Checklist de Instalação

### ✅ Versão Computador:
- [ ] Python 3.7+ instalado
- [ ] Dependências instaladas
- [ ] Microfone ou módulo de áudio funcionando
- [ ] Programa executando
- [ ] Menu principal aparece

### ✅ Versão Raspberry Pi:
- [ ] Raspberry Pi configurado
- [ ] I2C habilitado
- [ ] Display LCD conectado
- [ ] LEDs montados
- [ ] Microfone ou módulo de áudio USB funcionando
- [ ] Programa executando com sudo

## 🎓 Aplicações Educacionais

### Para Professores:
- **Ensino de música** com feedback visual
- **Prática de instrumentos** com gamificação
- **Avaliação de progresso** dos alunos
- **Ambiente interativo** de aprendizado

### Para Estudantes:
- **Aprendizado de notas** de forma divertida
- **Prática independente** com feedback imediato
- **Desenvolvimento de ouvido musical**
- **Motivação através de gamificação**

### Para Desenvolvedores:
- **Código educacional** bem documentado
- **Algoritmos de processamento** de áudio
- **Interface com hardware** Raspberry Pi
- **Projeto open-source** para contribuições

## 📁 Estrutura do Projeto

```
saiba-sua-nota/
├── README.md                           # Documentação principal
├── requirements.txt                    # Dependências computador
├── TESTE_COMPUTADOR.md                # Guia de teste computador
├── Saiba sua nota software/
│   ├── requirements.txt               # Dependências software
│   └── saiba_sua_nota.py               # Versão computador
├── Saiba sua nota raspberry pi/
│   ├── requirements.txt               # Dependências Raspberry Pi
└──   └── saiba_sua_nota_raspberry_pi.py # Versão Raspberry Pi
```

## 🤝 Contribuição

Este é um projeto educacional open-source. Contribuições são bem-vindas!

### Como Contribuir:
1. **Fork** o repositório
2. **Crie** uma branch para sua funcionalidade
3. **Faça** suas modificações
4. **Teste** em ambas as versões
5. **Envie** um Pull Request

### Áreas de Contribuição:
- **Melhorias** no algoritmo de detecção
- **Novas funcionalidades** educacionais
- **Interface** mais intuitiva
- **Documentação** e exemplos
- **Testes** e validação

## 📄 Licença

Projeto educacional de código aberto para fins de aprendizado e ensino musical.

## 📞 Suporte

- **Issues**: Reporte bugs e sugestões
- **Discussions**: Tire dúvidas e compartilhe ideias
- **Wiki**: Documentação detalhada
- **Releases**: Versões estáveis

---

**🎸 Projeto educacional para aprendizado musical interativo! 🎵✨**

*Desenvolvido com ❤️ para a educação musical*

