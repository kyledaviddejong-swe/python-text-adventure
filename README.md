# Ciacco's Submarket · Python Text Adventure

A narrative-driven command-line text adventure written in Python. The player descends into a fictional "submarket," explores interconnected departments, decides whether to collect the products encountered along the way, and reaches different endings based on exploration and consumption.

The game is intentionally small and self-contained: one Python file, no external packages, and a data-driven structure for rooms, items, descriptions, and game state.

## Features

- Dictionary-based room graph with directional navigation.
- Command parsing and targeted input validation.
- Item collection with multiple accepted synonyms.
- Inventory and visited-room state tracking.
- Choice tracking that influences ending text.
- Multiple endings based on collected items, exploration, and hidden interactions.
- Narrative descriptions integrated directly with gameplay state.

## How It Works

The room layout is stored as a nested dictionary that maps each location to its available directional connections. A second dictionary stores the item associated with each room, accepted command synonyms, descriptive text, and whether the item remains available.

Player input is tokenized and validated before an action is returned to the main game loop. The loop then updates navigation, inventory, visited locations, refusal counts, and the hidden state used by the ending logic.

## Run

Requires **Python 3** with no third-party dependencies. Download or clone this repository, open a terminal in its folder, and run:

```bash
python ciaccos_submarket.py
```

On systems where Python 3 is named `python3`, use `python3 ciaccos_submarket.py` instead.

The game prints the valid command format at startup. Movement commands use the displayed direction names, such as:

```text
go North
go East
```

Items are collected with:

```text
get <Item Name>
```

Commands are case-sensitive. Use lowercase `go` and `get`, and capitalize directions as shown. After requesting an item, enter `y` to take it or `n` to decline. For example, `go North`, then `get bread`, then `y` takes the bread from the Bakery.

Reaching the Exit ends the session and displays the result of your choices. There is no save system or in-game quit command; use Ctrl+C to stop early.

## Verification

Checked with Python 3.12.14 on October 1, 2026. Scripted playthroughs reached all four main endings, with additional checks for invalid commands, pickup confirmation, refusal and repeated pickup. The source is unchanged from the existing project.

## Technical Focus

Python · Dictionaries · Lists · Functions · Input Validation · Command Parsing · State Management · Branching Logic · File-Free Console Application

## Source

The complete implementation is included in `ciaccos_submarket.py`. The program logic and gameplay implementation are unchanged from the original version; only the file header was simplified for portfolio presentation.

## Background

This project began as introductory Python coursework. I wrote the game implementation and its narrative. AI assistance was used for portfolio documentation and verification; this import preserves the existing game source without changes.
