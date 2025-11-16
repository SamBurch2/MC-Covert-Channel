# music_encode.py
# Encodes a message into one chest using 4-bit music-disc encoding

import sys, minescript

# 4-bit → music disc mapping
DISC_MAP = {
    "0000": "minecraft:music_disc_5",
    "0001": "minecraft:music_disc_11",
    "0010": "minecraft:music_disc_13",
    "0011": "minecraft:music_disc_blocks",
    "0100": "minecraft:music_disc_cat",
    "0101": "minecraft:music_disc_chirp",
    "0110": "minecraft:music_disc_creator",
    "0111": "minecraft:music_disc_strad",
    "1000": "minecraft:music_disc_far",
    "1001": "minecraft:music_disc_lava_chicken",
    "1010": "minecraft:music_disc_mall",
    "1011": "minecraft:music_disc_mellohi",
    "1100": "minecraft:music_disc_otherside",
    "1101": "minecraft:music_disc_pigstep",
    "1110": "minecraft:music_disc_precipice",
    "1111": "minecraft:music_disc_stal"
}

# Get message from command args
if len(sys.argv) > 1:
    message = " ".join(sys.argv[1:])
else:
    message = "HELLO"

# Player position
px, py, pz = minescript.player().position
x, y, z = int(px), int(py), int(pz)

# Place chest
minescript.execute(f"setblock {x} {y} {z} minecraft:chest")

# Convert message → binary
binary = ""
for ch in message:
    binary += format(ord(ch), "08b")   # 8 bits per char

# Split binary into 4-bit chunks
nibbles = []
for i in range(0, len(binary), 4):
    nib = binary[i:i+4]
    if len(nib) < 4:
        nib = nib.ljust(4, "0")
    nibbles.append(nib)

slot = 0
for nib in nibbles:
    if slot >= 27:
        break
    disc = DISC_MAP.get(nib)
    if disc:
        cmd = (
            f"item replace block {x} {y} {z} container.{slot} "
            f"with {disc} 1"
        )
        minescript.execute(cmd)
        slot += 1

# place music_disc_wait as END-OF-MESSAGE marker ---
if slot < 27:
    minescript.execute(
        f"item replace block {x} {y} {z} container.{slot} "
        f"with minecraft:music_disc_wait 1"
    )
    minescript.echo(f"🔵 End-of-message marker added in slot {slot}")
# -------------------------------------------------------------------

# Output debug info
minescript.echo(f"🎵 Encoded '{message}' into {slot} music discs + end marker at {x},{y},{z}")
for nib in nibbles:
    minescript.echo(f"  {nib} → {DISC_MAP.get(nib, '???')}")


