# chest_encode.py
# Encodes a message into ONE chest; each char = ASCII count of a unique block

import sys, random, minescript

BLOCK_POOL = [
    "minecraft:stone",
    "minecraft:cobblestone",
    "minecraft:dirt",
    "minecraft:coarse_dirt",
    "minecraft:gravel",
    "minecraft:sand",
    "minecraft:red_sand",
    "minecraft:oak_log",
    "minecraft:spruce_log",
    "minecraft:birch_log",
    "minecraft:acacia_log",
    "minecraft:jungle_log",
    "minecraft:oak_planks",
    "minecraft:spruce_planks",
    "minecraft:birch_planks",
    "minecraft:deepslate",
    "minecraft:andesite",
    "minecraft:diorite",
    "minecraft:granite",
    "minecraft:clay_ball",
    "minecraft:brick",
    "minecraft:coal",
    "minecraft:iron_ingot",
    "minecraft:glass",
    "minecraft:torch",
    "minecraft:wheat",
    "minecraft:bread",
    "minecraft:ladder",
    "minecraft:stick",
    "minecraft:string",
    "minecraft:paper",
    "minecraft:leather",
    "minecraft:raw_iron",
    "minecraft:raw_copper",
    "minecraft:cooked_beef",
    "minecraft:carrot",
    "minecraft:potato"
]
MAX_STACK = 64

if len(sys.argv) > 1:
    message = " ".join(sys.argv[1:])
else:
    message = "HELLO"

px, py, pz = minescript.player().position
x, y, z = int(px), int(py), int(pz)

# Place chest
minescript.execute(f"setblock {x} {y} {z} minecraft:chest")

slot = 0
for i, ch in enumerate(message):
    ascii_val = ord(ch)
    block = BLOCK_POOL[i % len(BLOCK_POOL)]
    remaining = ascii_val
    while remaining > 0 and slot < 27:
        count = remaining if remaining <= MAX_STACK else MAX_STACK
        # Let Minecraft fill the slot with a real stack
        cmd = (
            f"item replace block {x} {y} {z} container.{slot} "
            f"with {block} {count}"
        )
        minescript.execute(cmd)
        remaining -= count
        slot += 1

minescript.echo(f"✅ Encoded '{message}' into one chest at {x},{y},{z}")
for i, ch in enumerate(message):
    minescript.echo(f"  '{ch}' → {ord(ch)} × {BLOCK_POOL[i % len(BLOCK_POOL)]}")

