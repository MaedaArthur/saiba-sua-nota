#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Detector musical / jogo de notas.
Versão sem afinador e sem funções de filtro.
"""

import sys
import time
import threading
import random
import signal
from typing import Optional, Tuple

import numpy as np
import sounddevice as sd
from scipy import signal as spsig

# -----------------------------
# CONFIGURAÇÕES GLOBAIS
# -----------------------------
NOTAS_GUITARRA = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
HOLD_NOTA_SEGS = 1.8
CHECK_INPUT_INTERVAL = 0.05
DEFAULT_SAMPLE_RATE = 48000

stop_event = threading.Event()

# -----------------------------
# Sinal de interrupção Ctrl+C
# -----------------------------
def _signal_handler(sig, frame):
    stop_event.set()
    print("\n⚠️  Interrupção recebida (Ctrl+C).")

signal.signal(signal.SIGINT, _signal_handler)

# -----------------------------
# Checagem de tecla 'q'
# -----------------------------
if sys.platform.startswith("win"):
    import msvcrt
    def check_for_quit_nonblocking() -> bool:
        while msvcrt.kbhit():
            ch = msvcrt.getch()
            if ch in (b'q', b'Q'):
                return True
        return False
else:
    import select, tty, termios
    def check_for_quit_nonblocking() -> bool:
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        if dr:
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setcbreak(fd)
                ch = sys.stdin.read(1)
                if ch in ('q', 'Q'):
                    return True
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return False

def check_for_quit(timeout: float = 0.0) -> bool:
    steps = max(1, int(max(timeout / CHECK_INPUT_INTERVAL, 1)))
    for _ in range(steps):
        if check_for_quit_nonblocking():
            return True
        if timeout > 0:
            time.sleep(timeout / steps)
    return False

# -----------------------------
# CAPTURA DE ÁUDIO
# -----------------------------
def capturar_audio(duracao: float = 0.25, sample_rate: int = DEFAULT_SAMPLE_RATE, device=None):
    try:
        frames = int(max(1, round(duracao * sample_rate)))
        audio = sd.rec(frames, samplerate=sample_rate, channels=1, dtype='float32', device=device)
        sd.wait()
        return audio.flatten(), sample_rate
    except Exception as e:
        print(f"❌ Erro na captura: {e}")
        return np.zeros(int(max(1, duracao * sample_rate)), dtype='float32'), sample_rate

# -----------------------------
# DETECÇÃO DE FREQUÊNCIA
# -----------------------------
def detectar_frequencia_fundamental_avancado(sinal: np.ndarray, sr: int):
    try:
        if len(sinal) < 3:
            return None, 0.0
        rms = np.sqrt(np.mean(sinal ** 2))
        if rms < 0.005:
            return None, 0.0

        n_fft = max(8, 4 * len(sinal))
        freq = np.fft.rfftfreq(n_fft, d=1.0 / sr)
        fft = np.fft.rfft(sinal, n=n_fft)
        magnitude = np.abs(fft)
        if magnitude.size == 0:
            return None, 0.0

        picos, _ = spsig.find_peaks(magnitude, height=np.max(magnitude)*0.08)
        if picos.size == 0:
            return None, 0.0

        candidato = freq[picos[np.argmax(magnitude[picos])]]
        freq_fund = float(candidato)

        notas_ref = {
            'E': [82.41, 164.81, 329.63, 659.25],
            'F': [87.31, 174.61, 349.23, 698.46],
            'F#': [92.50, 185.00, 369.99, 739.99],
            'G': [98.00, 196.00, 392.00, 784.00],
            'G#': [103.83, 207.65, 415.30, 830.61],
            'A': [110.00, 220.00, 440.00, 880.00],
            'A#': [116.54, 233.08, 466.16, 932.33],
            'B': [123.47, 246.94, 493.88, 987.77],
            'C': [130.81, 261.63, 523.25, 1046.50],
            'C#': [138.59, 277.18, 554.37, 1108.73],
            'D': [146.83, 293.66, 587.33, 1174.66],
            'D#': [155.56, 311.13, 622.25, 1244.51]
        }

        nota_detectada = min(
            notas_ref,
            key=lambda n: min(abs(np.log2(freq_fund/f)) for f in notas_ref[n])
        )
        return nota_detectada, freq_fund
    except Exception as e:
        print(f"⚠️ Erro na detecção: {e}")
        return None, 0.0

def nota_fundamental(sinal, sr):
    return detectar_frequencia_fundamental_avancado(sinal, sr)

# -----------------------------
# DISPOSITIVOS
# -----------------------------
def obter_dispositivo_padrao():
    try:
        dispositivos = sd.query_devices()
        default = sd.default.device
        dispositivo_padrao = None
        if isinstance(default, (list, tuple)):
            dispositivo_padrao = default[0]
        elif isinstance(default, int):
            dispositivo_padrao = default
        if dispositivo_padrao is not None:
            return dispositivo_padrao
        for i, dev in enumerate(dispositivos):
            if dev.get('max_input_channels', 0) > 0:
                return i
    except Exception as e:
        print(f"Erro ao obter dispositivo: {e}")
    return None

def listar_dispositivos():
    try:
        for i, dev in enumerate(sd.query_devices()):
            print(f"{i}: {dev['name']} (Entradas: {dev.get('max_input_channels',0)})")
    except Exception as e:
        print(f"Erro: {e}")

# -----------------------------
# MODOS
# -----------------------------
def modo_detector_livre(device_id):
    print("\n🎸 Detector Livre ativado! (Pressione 'Q' para sair)")
    while not stop_event.is_set():
        if check_for_quit():
            break
        audio, sr = capturar_audio(0.25, DEFAULT_SAMPLE_RATE, device=device_id)
        nota, freq = nota_fundamental(audio, sr)
        if nota:
            print(f"🎵 Nota: {nota} | Freq: {freq:.1f} Hz")
        time.sleep(0.25)
    stop_event.clear()

def jogar_nota_adaptado(device_id):
    print("🎵 JOGO DE NOTAS 🎵\nPressione 'Q' para sair.")
    notas = random.sample(NOTAS_GUITARRA, len(NOTAS_GUITARRA))
    objetivo = notas.pop()
    print(f"🎯 Toque a nota: {objetivo}")
    while not stop_event.is_set():
        if check_for_quit():
            break
        audio, sr = capturar_audio(0.3, DEFAULT_SAMPLE_RATE, device=device_id)
        nota, freq = nota_fundamental(audio, sr)
        if nota:
            if nota != objetivo:
                print(f"🎵 Tocou: {nota}. Toque a nota {objetivo}")
            else:
                print("✅ Acertou!")
                time.sleep(0.5)

                if notas:
                    objetivo = notas.pop()
                    print(f"🎯 Próxima nota: {objetivo}")
                else:
                    print("🏁 Fim do jogo!")
                    break
        time.sleep(0.3)
    stop_event.clear()

def teste_captura_audio(device_id):
    print("🔧 Teste de Captura - pressione 'Q' para sair.")
    while not stop_event.is_set():
        if check_for_quit():
            break
        audio, sr = capturar_audio(0.4, DEFAULT_SAMPLE_RATE, device=device_id)
        rms = np.sqrt(np.mean(audio**2))
        print(f"RMS: {rms:.4f}")
    stop_event.clear()

# -----------------------------
# MENUS
# -----------------------------
def selecionar_dispositivo():
    listar_dispositivos()
    try:
        return int(input("Digite o ID do dispositivo: "))
    except:
        return None

def menu_principal(device_id):
    while True:
        print("\n" + "=" * 40)
        print("🎵 DETECTOR MUSICAL SIMPLIFICADO")
        print("=" * 40)
        print(f"Dispositivo: {device_id}")
        print("1. Jogo de Notas\n2. Detector Livre\n3. Teste de Captura\n4. Alterar Dispositivo\n5. Sair")
        escolha = input("Escolha (1-5): ").strip()
        if escolha == "1":
            jogar_nota_adaptado(device_id)
        elif escolha == "2":
            modo_detector_livre(device_id)
        elif escolha == "3":
            teste_captura_audio(device_id)
        elif escolha == "4":
            novo = selecionar_dispositivo()
            if novo is not None:
                device_id = novo
        elif escolha == "5":
            break
        else:
            print("Opção inválida.")
    return device_id

# -----------------------------
# EXECUÇÃO
# -----------------------------
if __name__ == "__main__":
    try:
        print("🎵 DETECTOR MUSICAL INICIANDO 🎵")
        device_id = obter_dispositivo_padrao()
        if device_id is None:
            print("Nenhum dispositivo encontrado.")
            device_id = selecionar_dispositivo()
        menu_principal(device_id)
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
    finally:
        print("👋 Programa finalizado.")
