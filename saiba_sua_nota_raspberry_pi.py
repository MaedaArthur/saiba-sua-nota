#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jogo de notas musicais para Raspberry Pi com LCD, botão, potenciômetro e LEDs.
O usuário pressiona o botão para iniciar o jogo e deve tocar as notas pedidas.
"""

import sys, time, threading, random
import numpy as np
import sounddevice as sd
from scipy import signal as spsig
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD

# -----------------------------
# CONFIGURAÇÕES DE HARDWARE
# -----------------------------
LCD_ADDRESS = 0x27       # Endereço I2C do display
LED_VERDE = 22
LED_VERMELHO = 27

# Configura GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_VERDE, GPIO.OUT)
GPIO.setup(LED_VERMELHO, GPIO.OUT)

# LCD
lcd = CharLCD('PCF8574', LCD_ADDRESS)
lcd.clear()

# -----------------------------
# CONFIGURAÇÕES GERAIS
# -----------------------------
NOTAS_GUITARRA = ['C', 'C#', 'D', 'D#', 'E', 'F',
                  'F#', 'G', 'G#', 'A', 'A#', 'B']
DEFAULT_SAMPLE_RATE = 48000
stop_event = threading.Event()

# -----------------------------
# CAPTURA DE ÁUDIO
# -----------------------------
def capturar_audio(duracao=0.25, sr=DEFAULT_SAMPLE_RATE, device=None):
    try:
        frames = int(max(1, round(duracao * sr)))
        audio = sd.rec(frames, samplerate=sr, channels=1, dtype='float32', device=device)
        sd.wait()
        return audio.flatten(), sr
    except Exception as e:
        print("Erro na captura:", e)
        return np.zeros(int(max(1, duracao * sr))), sr

# -----------------------------
# DETECÇÃO DE NOTAS
# -----------------------------
def nota_fundamental(sinal, sr):
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

        picos, _ = spsig.find_peaks(magnitude, height=np.max(magnitude) * 0.08)
        if picos.size == 0:
            return None, 0.0

        freq_fund = freq[picos[np.argmax(magnitude[picos])]]

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
            key=lambda n: min(abs(np.log2(freq_fund / f)) for f in notas_ref[n])
        )
        return nota_detectada, freq_fund
    except:
        return None, 0.0

# -----------------------------
# JOGO DE NOTAS
# -----------------------------
def jogar_nota(device_id=None):
    notas = random.sample(NOTAS_GUITARRA, len(NOTAS_GUITARRA))
    objetivo = notas.pop()
    lcd.clear()
    lcd.write_string(f"Toque: {objetivo}")

    # Mudando a posição do cursor para a linha 1, coluna 0 antes de escrever o próximo texto
    lcd.cursor_pos = (1, 0)  # Coluna 0, Linha 1
    while notas and not stop_event.is_set():
        audio, sr = capturar_audio(0.3, DEFAULT_SAMPLE_RATE, device=device_id)
        nota, freq = nota_fundamental(audio, sr)

        if nota:
            lcd.clear()
            lcd.write_string(f"Alvo: {objetivo}")

            # Mudando a posição do cursor para a linha 1, coluna 0 para a próxima mensagem
            lcd.cursor_pos = (1, 0)
            lcd.write_string(f"Tocou: {nota}")

            lcd.cursor_pos = (2, 0)


            if nota == objetivo:
                GPIO.output(LED_VERDE, True)
                GPIO.output(LED_VERMELHO, False)
                lcd.write_string("Acertou!")
                time.sleep(1)
                GPIO.output(LED_VERDE, False)
                if notas:
                    objetivo = notas.pop()
                    lcd.clear()
                    lcd.write_string(f"Prox: {objetivo}")
                    # Mudando a posição do cursor novamente
                    lcd.cursor_pos = (1, 0)
            else:
                GPIO.output(LED_VERMELHO, True)
                GPIO.output(LED_VERDE, False)
                lcd.write_string("Errou!")
                time.sleep(1)
                GPIO.output(LED_VERMELHO, False)

    lcd.clear()
    lcd.write_string("Fim do jogo!")
    time.sleep(2)

# -----------------------------
# PROGRAMA PRINCIPAL
# -----------------------------
def main():
    try:
        lcd.clear()
        lcd.write_string("Iniciando jogo...")
        time.sleep(2)

        while True:
            jogar_nota()
            lcd.clear()
            lcd.write_string("Reiniciando em 3s...")
            time.sleep(3)

    except KeyboardInterrupt:
        pass
    finally:
        lcd.clear()
        lcd.write_string("Encerrando...")
        GPIO.cleanup()

if __name__ == "__main__":
    main()
