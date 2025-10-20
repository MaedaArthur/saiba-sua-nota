# 🖥️ Teste no Computador - Saiba Sua Nota

Este arquivo contém instruções detalhadas para testar o detector musical no computador antes de usar no Raspberry Pi. Inclui guias completos para todos os modos disponíveis.

## 🔧 Modificações para Teste no Computador

### ✅ O que foi alterado:
- **GPIO comentado**: Todas as funções relacionadas ao RPi.GPIO foram comentadas
- **LED substituído por mensagens**: Em vez de acender LED verde, mostra mensagens no console
- **Validação de frequência**: Frequências de 0 Hz não são contabilizadas como notas
- **Sistema sem repetição**: Cada nota aparece apenas uma vez até completar todas as 12 notas
- **Contador de progresso**: Mostra quantas notas restam na rodada atual
- **Sistema de rodadas**: Quando completa todas as notas, inicia uma nova rodada embaralhada
- **Afinador integrado**: Afine sua guitarra antes de jogar
- **Filtro passa-baixo**: Remove interferência da rede elétrica (60 Hz)
- **Mensagens melhoradas**: Feedback claro de acerto ou erro

### 🎮 Como Funciona Agora:

1. **Ao acertar uma nota**:
   ```
   🟢 ✅ ACERTOU! PARABÉNS! ✅ 🟢
   🎉 Você tocou a nota correta!
   ```

2. **Ao errar uma nota**:
   ```
   ❌ Não foi dessa vez! Tente novamente.
   🎯 Continue tentando: [nota]
   ```

3. **Frequência inválida (0 Hz)**:
   ```
   (Sem mensagem - apenas ignora silenciosamente)
   ```

4. **Progresso da rodada**:
   ```
   📋 Notas restantes nesta rodada: 8
   ```

5. **Nova rodada iniciada**:
   ```
   🎊 RODADA 2 INICIADA! 🎊
   ```

6. **Afinador - Corda por corda**:
   ```
   🎯 AFINE A CORDA: E (6ª corda)
   📊 Frequência de referência: 82.4 Hz
   🎸 Toque a corda ou pressione ENTER para próxima...
   
   🟢 82.4 Hz | ✅ AFINADO | ✅ OK | +0.2 cents
   ```

7. **Afinador - Corda desafinada**:
   ```
   🎯 AFINE A CORDA: A (5ª corda)
   📊 Frequência de referência: 110.0 Hz
   🎸 Toque a corda ou pressione ENTER para próxima...
   
   🔴 108.5 Hz | ❌ DESAFINADO | ⬆️ SOBE | -23.4 cents
   ```

8. **Sequência completa**:
   ```
   🎊 TODAS AS CORDAS AFINADAS! 🎊
   🔄 Reiniciando sequência de afinação...
   ```

## 🚀 Guia de Teste Completo

### 1. Preparação do Ambiente
```bash
# Instalar dependências
pip install -r requirements.txt

# Verificar dispositivos de áudio disponíveis
python -c "import sounddevice as sd; print(sd.query_devices())"
```

### 2. Executar o Programa
```bash
python saiba_sua_nota.py
```

### 3. Menu Principal - Opções Disponíveis
- **1. Jogo de Notas** 🎯 - Modo educativo (recomendado para teste)
- **2. Detector Livre** 🎸 - Identificação em tempo real
- **3. Teste de Captura** 🔧 - Verificar funcionamento do áudio
- **4. Alterar Dispositivo** 🎛️ - Selecionar microfone específico
- **5. Sair** ❌ - Finalizar programa

## 🎯 Testando o Jogo de Notas (Modo Principal)

### Passo a Passo:
1. **Conecte um microfone** ao computador
2. **Execute o programa** e escolha **"1. Jogo de Notas"**
3. **Uma nota aleatória** aparecerá na tela (ex: "🎯 Toque a nota: A")
4. **Toque a nota** na guitarra, piano ou cante
5. **Veja o feedback**:
   - ✅ **Acertou**: "✅ Acertou!" + próxima nota
   - ❌ **Errou**: "🎵 Tocou: [nota]. Toque a nota [objetivo]"
   - 🔇 **Sem som**: Nenhuma mensagem (normal)

### Controles:
- **Q**: Sair do jogo atual
- **Ctrl+C**: Interrupção de emergência

### Sistema de Rodadas:
- **12 notas únicas** por rodada (sem repetição)
- **Progresso visual**: Mostra quantas notas restam
- **Nova rodada**: Após completar todas as 12 notas
- **Embaralhamento**: Ordem aleatória a cada rodada

## 🎸 Testando o Detector Livre

### Como usar:
1. **Escolha "2. Detector Livre"** no menu
2. **Toque qualquer nota** no instrumento
3. **Veja a identificação** em tempo real:
   ```
   🎵 Nota: A | Freq: 220.0 Hz
   🎵 Nota: C# | Freq: 277.2 Hz
   ```
4. **Ideal para**: Afinação, prática, identificação de notas

## 🔧 Testando a Captura de Áudio

### Diagnóstico:
1. **Escolha "3. Teste de Captura"** no menu
2. **Observe os valores RMS**:
   - **0.0000-0.0010**: Muito baixo (aumente volume)
   - **0.0010-0.0100**: Baixo (toque mais forte)
   - **0.0100-0.1000**: Bom (funcionando)
   - **>0.1000**: Alto (pode saturar)

### Solução de problemas:
- **RMS muito baixo**: Aumente volume do microfone
- **RMS zero**: Verifique conexão do microfone
- **RMS instável**: Verifique interferências

## 🎛️ Configuração de Dispositivos de Áudio

### Seleção Manual:
1. **Escolha "4. Alterar Dispositivo"** no menu
2. **Lista de dispositivos** será exibida:
   ```
   0: Microfone (Realtek High Definition Audio) (Entradas: 1)
   1: Microfone USB (Entradas: 1)
   2: Stereo Mix (Entradas: 0)
   ```
3. **Digite o número** do dispositivo desejado
4. **Teste** com o modo "Teste de Captura"

### Dispositivos Recomendados:
- **Microfone USB**: Melhor qualidade, menos ruído
- **Microfone integrado**: Funciona, mas pode ter mais ruído
- **Stereo Mix**: Captura áudio do sistema (não recomendado para instrumentos)

## 📊 Interpretação dos Resultados

### Valores RMS (Teste de Captura):
- **0.0000-0.0010**: 🚫 **Muito baixo** - Aumente volume do microfone
- **0.0010-0.0100**: 🟡 **Baixo** - Toque mais forte ou aproxime do microfone
- **0.0100-0.1000**: 🟢 **Ideal** - Funcionando perfeitamente
- **0.1000-0.5000**: 🟠 **Alto** - Pode funcionar, mas cuidado com saturação
- **>0.5000**: 🔴 **Muito alto** - Risco de saturação, diminua volume

### Detecção de Notas:
- **Frequência 0 Hz**: Normal quando não há som
- **Nota incorreta**: Verifique afinação do instrumento
- **Sem detecção**: Aumente volume ou aproxime do microfone

### Performance do Sistema:
- **Taxa de amostragem**: 48kHz (padrão)
- **Duração da captura**: 0.25s (detector livre), 0.3s (jogo)
- **Sensibilidade**: RMS mínimo de 0.005
- **Latência**: ~0.25-0.3 segundos

## 🎯 Dicas para Melhor Performance

### Configuração Ideal:
- **Ambiente silencioso**: Evite ruídos de fundo
- **Microfone próximo**: 10-30cm do instrumento
- **Volume moderado**: Nem muito baixo, nem muito alto
- **Instrumento afinado**: Use um afinador antes de testar

### Instrumentos Recomendados:
- **Guitarra**: Funciona muito bem
- **Piano/Teclado**: Excelente detecção
- **Violão**: Boa performance
- **Voz**: Funciona, mas pode ser menos preciso
- **Flauta**: Funciona bem em notas agudas

### Problemas Comuns:
- **Detecção incorreta**: Verifique afinação do instrumento
- **Sem resposta**: Aumente volume ou aproxime do microfone
- **Muitas detecções**: Ambiente muito ruidoso

## 🔄 Para Usar no Raspberry Pi

Quando estiver pronto para usar no Raspberry Pi:

1. **Descomente as linhas GPIO**:
   ```python
   import RPi.GPIO as GPIO
   PIN_ACERTO = 4
   ```

2. **Descomente as funções GPIO**:
   - `configurar_gpio_jogo()`
   - `acender_led_acerto()`

3. **Atualize o requirements.txt**:
   ```
   RPi.GPIO>=0.7.1
   ```

4. **Execute com sudo**:
   ```bash
   sudo python3 saiba_sua_nota.py
   ```

## 🐛 Solução de Problemas Detalhada

### ❌ Microfone não detectado
**Sintomas**: Erro ao iniciar, "Nenhum dispositivo encontrado"
**Soluções**:
- Verifique conexão USB/3.5mm
- Teste com gravador de voz do Windows
- Reinicie o programa
- Use seleção manual de dispositivo

### 🔇 Som não detectado
**Sintomas**: RMS sempre 0.0000, sem detecção de notas
**Soluções**:
- Aumente volume do microfone no Windows
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

### ⚡ Performance lenta
**Sintomas**: Lag na detecção, travamentos
**Soluções**:
- Feche outros programas
- Verifique CPU/RAM disponível
- Use microfone USB (menos processamento)
- Reinicie o computador

### 🔧 Erros técnicos
**Sintomas**: Mensagens de erro, crashes
**Soluções**:
- Reinstale dependências: `pip install -r requirements.txt`
- Verifique versão do Python (3.7+)
- Execute como administrador
- Verifique permissões de áudio

---

## 📋 Checklist de Teste Completo

### ✅ Antes de começar:
- [ ] Microfone conectado e funcionando
- [ ] Volume do microfone ajustado
- [ ] Ambiente silencioso
- [ ] Instrumento afinado
- [ ] Dependências instaladas

### ✅ Teste básico:
- [ ] Programa inicia sem erros
- [ ] Menu principal aparece
- [ ] "Teste de Captura" mostra RMS > 0.01
- [ ] "Detector Livre" identifica notas
- [ ] "Jogo de Notas" funciona

### ✅ Teste avançado:
- [ ] Todas as 12 notas são detectadas
- [ ] Sistema de rodadas funciona
- [ ] Controles Q e Ctrl+C funcionam
- [ ] Seleção de dispositivo funciona
- [ ] Performance estável

**🎉 Se todos os itens estão marcados, o sistema está pronto para uso! 🎸✨**
