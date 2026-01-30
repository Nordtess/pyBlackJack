<div align="center">

# 🃏 PyBlackjack: Casino Vibes, Zero Risk

**Hit or stay? Your call—but the house edge is just for show.** A polished Pygame blackjack simulator with smooth card animations, persistent balance tracking, and enough visual polish to make you forget you're not losing real money.

</div>

## 💡 Description

I built PyBlackjack to prove that you can create a genuinely enjoyable casino game in Python without resorting to bloated frameworks or sacrificing code quality. It's a fully-featured blackjack implementation with animated card dealing, a clean betting interface, balance persistence across sessions, and a custom wallpaper system—all wrapped in ~600 lines of well-architected Python.

This isn't just "deal two cards and compare numbers"—it's a showcase of **event-driven architecture**, **stateful game loops**, and **proper separation of concerns**, proving that Python game development can be elegant, maintainable, and actually fun to work on.

### Key Implementation Highlights:

- **Clean Module Structure:** The project is split into focused modules—**Card** (individual card logic), **CardDeck** (52-card deck management), **Player** (hand evaluation with ace optimization), and **main.py** (game loop & rendering). Each class has a single, well-defined responsibility.
- **Smooth Card Animations:** Initial deals feature staggered 600ms card reveals for suspense, while hits and dealer plays show cards instantly. The animation system tracks visible card counts separately from actual game state.
- **Persistent Balance System:** Your bankroll survives across sessions via file-based storage. Start with $500, build it up (or blow it all), and pick up where you left off next time.
- **Responsive UI Design:** Info panel on the right shows balance, current bet, and game status. Semi-transparent text backgrounds ensure readability over any wallpaper. Betting chips, buttons, and labels all respond to hover states with proper cursor feedback.
- **Smart Ace Handling:** Player class automatically optimizes ace values (11 or 1) to prevent busts when possible—just like a real dealer would count them.
- **Dual Input Modes:** Full keyboard shortcuts (H/S/R/Q) + mouse controls for all actions. Arrow keys adjust bets, Enter/Space to deal.

---

## 🧰 Tech Stack

<p align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="40" height="40" alt="Python" title="Python 3.12 (The Engine)"/>
  <img src="https://www.pygame.org/docs/_static/pygame_logo.svg" width="40" height="40" alt="Pygame" title="Pygame (The Graphics Layer)"/>
</p>

---

## 🎯 Features

### 🎰 Core Gameplay

- **Classic Blackjack Rules:** Dealer stands on 17, blackjack pays 3:2, player can hit until bust or 21
- **Intelligent Dealer AI:** Follows house rules—reveals hole card on stay, hits to 17, all with instant card display
- **Ace Optimization:** Automatic 11→1 conversion to prevent unnecessary busts
- **Instant Blackjack Detection:** Detects natural 21s on deal and settles immediately

### 💰 Betting System

- **Four Chip Denominations:** $10, $25, $50, $100 chips with visual feedback
- **Bet Validation:** Can't bet more than you have, minimum $10 enforced
- **Balance Persistence:** File-based storage in balance.txt—your wins/losses carry over between sessions
- **Dynamic Betting:** Adjust bets with Up/Down arrow keys or click chips directly

### 🎨 Visual Polish

- **Staggered Card Animations:** Initial 4-card deal reveals one at a time (600ms delay) for dramatic effect
- **Custom Wallpaper Support:** Drop `wallpaper1.jpg` in images folder for personalized backgrounds
- **Semi-Transparent Overlays:** All text rendered with dark backgrounds for readability on any wallpaper
- **Hover Effects:** Buttons and chips respond to mouse proximity with color shifts
- **Info Panel:** Right-side HUD shows balance, current bet, game status, and betting interface

### 🎮 Controls

- **Keyboard:** H (Hit) | S (Stay) | R (Reset) | Q (Quit) | ↑↓ (Adjust Bet) | Enter/Space (Deal)
- **Mouse:** Click all buttons, chips, and UI elements with hover feedback
- **Dual Mode:** Betting screen uses same interface—select chip → click Deal

---

## 🖼️ Screenshots

<p align="center">
  <img src="screenshots/screenshot1.png" alt="Screenshot 1: Main Menu" width="800">
</p>
<p align="center">
  <strong>Screenshot 1:</strong> Title screen with fade-in animation and custom wallpaper.
</p>

<p align="center">
  <img src="screenshots/screenshot2.png" alt="Screenshot 2: Betting Screen" width="800">
</p>
<p align="center">
  <strong>Screenshot 2:</strong> Betting interface with chip selection and current balance display.
</p>

<p align="center">
  <img src="screenshots/screenshot3.png" alt="Screenshot 3: Active Game" width="800">
</p>
<p align="center">
  <strong>Screenshot 3:</strong> Mid-game with cards dealt, player deciding to hit or stay.
</p>

---

## ⚙️ How to Play

### Prerequisites

You'll need:

- **Python 3.12+** (3.8+ probably works, but 3.12 is what I built it on)
- **Pygame 2.6+** (`pip install pygame`)

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/nordtess/pyblackjack
cd pyblackjack

# 2. Install dependencies
pip install pygame

# 3. Run the game
python main.py

# 4. Start playing!
# - Press Enter/Space or click "Play Blackjack" to start
# - Select your bet with chips or Up/Down arrows
# - Click "Deal" or press Enter to begin the round
# - Hit (H) or Stay (S) to play your hand
```

### Project Structure

```
pyblackjack/
├── main.py              # Game loop, rendering, event handling (~500 lines)
├── card.py              # Individual card representation
├── carddeck.py          # 52-card deck with shuffle and draw logic
├── player.py            # Hand evaluation and ace optimization
├── balance.txt          # Persistent balance storage (auto-created)
└── images/              # Card sprites + wallpaper
    ├── hearts_2.png     # 52 card images (4 suits × 13 ranks)
    ├── backside.png     # Card back design
    └── wallpaper1.jpg   # Custom background (1280×720)
```

---

## 🎲 Game Logic Highlights

**Card Values:**

- Number cards (2-10): Face value
- Face cards (J, Q, K): 10 points
- Aces: 11 (or 1 if 11 would bust)

**Dealer Rules:**

- Hits until reaching 17+
- Stands on soft 17 (A+6)
- Hole card revealed on player stay

**Payout Structure:**

- Blackjack (natural 21): 3:2 (bet $100 → win $250 total)
- Regular win: 1:1 (bet $100 → win $200 total)
- Push (tie): Bet returned
- Loss/Bust: Lose bet

---

## 🎨 Customization

### Change the Wallpaper

Drop any 1280×720 JPG into wallpaper1.jpg and restart. The game auto-scales and overlays semi-transparent UI elements for readability.

### Modify Starting Balance

Edit balance.txt (or delete it to reset to $500 default).

### Adjust Card Animation Speed

In main.py, change `CARD_DELAY_MS = 600` to any millisecond value (or set to 0 for instant reveals).

### Color Scheme

All colors defined as constants at the top of main.py:

```python
COLOR_GOLD = (255, 215, 0)        # Info panel title
COLOR_CHIP_RED = (210, 70, 70)    # Betting chips
COLOR_BLUE = (0, 120, 220)        # Buttons
# ... etc
```

---

## 🛠️ Technologies & Patterns Used

**Core:**

- Python 3.12
- Pygame 2.6.1 (SDL 2.28.4)

**Architecture:**

- Event-driven game loop (60 FPS)
- State machine (menu → betting → playing → game_over)
- Separation of concerns (rendering vs. logic vs. data)
- Composition over inheritance (Player has cards, doesn't extend them)

**Rendering:**

- Double buffering via `pygame.display.flip()`
- Semi-transparent overlays with alpha blending
- Custom font rendering with drop shadows
- Sprite scaling for card images (120×180)

**File I/O:**

- Balance persistence with exception handling
- Image loading with fallback to solid colors
- Cross-platform path handling via `os.path.join`

---

## 📝 Future Enhancements (Roadmap)

- [ ] Sound effects (card flip, chip clink, win/loss jingles)
- [ ] Split hands (when dealt pair)
- [ ] Double down mechanic
- [ ] Insurance bet option
- [ ] Multi-hand mode (play 3 hands simultaneously)
- [ ] Statistics tracking (win rate, biggest win, hands played)
- [ ] High score leaderboard
- [ ] Animated chip movements
- [ ] Card shuffle animation
- [ ] Configurable house rules (dealer hits soft 17, etc.)

---

## 👨‍💻 Author

**Nordtess**  
_Python Developer & Casino Game Architect (But Not a Gambler)_

---

## 📜 License

This project is licensed under the MIT License—feel free to use it, fork it, or build your own casino empire with it!

---

<div align="center">

**Built with ❤️ and way too much coffee in Sweden 🇸🇪**

_No actual money was harmed in the making of this game._

</div>
