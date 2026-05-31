# Sound Saber - Explicação Técnica

Documentação do módulo principal do EcoScreen.

O `Sound Saber` é o cursor sonoro do projeto. Ele transforma o movimento do mouse em feedback auditivo (panning + pitch), ajudando a criar a sensação de "ecrã sonoro".

## Objetivo
Criar um cursor que "canta" conforme sua posição na tela, usando apenas áudio estéreo simples (sem binaural/holofonia).

## Como funciona

### 1. Importações principais
- `numpy`: cálculos matemáticos para gerar o som
- `sounddevice`: reprodução de áudio em tempo real
- `pynput.mouse`: captura o movimento do mouse
- `pyttsx3`: síntese de voz (TTS)

### 2. Classe `SoundSaber`

#### `__init__()`
Inicializa o motor de voz e variáveis de controle.

#### `speak(text)`
Fala qualquer texto usando voz sintetizada.

#### `play_cursor_sound(x, y)`
**Coração do Sound Saber**. Faz o seguinte:
- Calcula a posição normalizada do mouse na tela
- **Panning** (esquerda/direita): o som fica mais forte no lado correspondente
- **Pitch** (altura do som): mais grave quando o mouse está embaixo, mais agudo quando está em cima
- Gera um tom curto (senoide) e aplica o efeito estéreo
- Toca o som imediatamente

#### `on_move(x, y)`
Função chamada automaticamente toda vez que o mouse se move.  
Tem um filtro (`throttle`) para não tocar som a cada pixel (evita som irritante).

#### `start()` e `stop()`
- `start()`: ativa o Sound Saber e começa a escutar o mouse
- `stop()`: desativa o sistema

## Como executar
```bash
cd ecoscreen
source venv/bin/activate
python src/sound_saber.py