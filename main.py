import os
import pygame
from carddeck import CardDeck
from player import Player


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BALANCE_FILE = os.path.join(BASE_DIR, "balance.txt")
BACKSIDE_PATH = os.path.join(BASE_DIR, "images", "backside.png")


deck = CardDeck()
deck.shuffle()

player = Player()
dealer = Player()


def load_balance():
    if not os.path.exists(BALANCE_FILE):
        return 500
    try:
        with open(BALANCE_FILE, "r", encoding="utf-8") as f:
            return max(0, int(f.read().strip() or 0))
    except Exception:
        return 500


def save_balance(value):
    try:
        with open(BALANCE_FILE, "w", encoding="utf-8") as f:
            f.write(str(int(value)))
    except Exception:
        pass


game_over = False
status_message = ""
show_menu = True
betting = False
balance = load_balance()
current_bet = 50
dealer_hide_second = False

# Card animation variables
cards_to_show = 0
last_card_time = 0
card_delay = 600  # milliseconds between cards


def reset_round():
    """Reset deck and hands; betting happens before dealing."""
    global deck, player, dealer, game_over, status_message, betting, current_bet, balance, dealer_hide_second, cards_to_show, last_card_time
    deck = CardDeck()
    deck.shuffle()
    player = Player()
    dealer = Player()
    game_over = False
    status_message = ""
    betting = True
    dealer_hide_second = False
    cards_to_show = 0
    last_card_time = 0

    if balance <= 0:
        status_message = "Out of funds"
        game_over = True
        betting = False
    else:
        current_bet = max(10, min(current_bet, balance))


reset_round()

font = pygame.font.SysFont("Arial", 48, bold=True)
button_font = pygame.font.SysFont("Arial", 32, bold=True)
title_font = pygame.font.SysFont("Arial", 72, bold=True)
info_font = pygame.font.SysFont("Arial", 24)

try:
    backside_image = pygame.image.load(BACKSIDE_PATH).convert_alpha()
    backside_image = pygame.transform.scale(backside_image, (120, 180))
except Exception:
    backside_image = None

hit_button = pygame.Rect(100, 610, 160, 60)
stay_button = pygame.Rect(300, 610, 160, 60)
quit_button = pygame.Rect(20, 20, 80, 32)
play_again_button = pygame.Rect(130, 20, 160, 32)
play_button = pygame.Rect(520, 300, 240, 80)
menu_start_time = pygame.time.get_ticks()

chip_values = [10, 25, 50, 100]
chip_buttons = []
chip_start_x = 400
for idx, val in enumerate(chip_values):
    chip_buttons.append((pygame.Rect(chip_start_x + idx * 90, 240, 70, 70), val))

running = True


def settle_round(result):
    """Handle payouts and end the round."""
    global game_over, status_message, balance, betting, dealer_hide_second
    if game_over:
        return
    game_over = True
    betting = False
    dealer_hide_second = False

    if result == "blackjack":
        payout = int(current_bet * 2.5)
        balance += payout
        status_message = "Blackjack! Paid 3:2"
    elif result == "player_win":
        payout = current_bet * 2
        balance += payout
        status_message = "You win"
    elif result == "push":
        balance += current_bet
        status_message = "Push"
    elif result == "dealer_win":
        status_message = "Dealer wins"
    elif result == "bust":
        status_message = "You are bust"
    else:
        status_message = "Round over"

    save_balance(balance)


def start_round():
    """Deal initial cards after a bet is placed."""
    global betting, balance, status_message, game_over, dealer_hide_second, cards_to_show, last_card_time
    if betting is False:
        return
    if current_bet <= 0 or current_bet > balance:
        status_message = "Invalid bet"
        return
    balance -= current_bet
    save_balance(balance)

    # Deal order: player open, dealer open, player open, dealer closed
    player.add_card(deck.draw_card())
    dealer.add_card(deck.draw_card())
    player.add_card(deck.draw_card())
    dealer.add_card(deck.draw_card())
    dealer_hide_second = True

    betting = False
    game_over = False
    status_message = ""
    cards_to_show = 0
    last_card_time = pygame.time.get_ticks()


def handle_hit():
    global game_over, status_message
    if game_over or betting:
        return
    new_card = deck.draw_card()
    if new_card:
        player.add_card(new_card)
    score = player.get_value()
    if score > 21:
        settle_round("bust")
    elif score == 21:
        play_dealer()


def handle_stay():
    global game_over, status_message
    if game_over or betting:
        return
    play_dealer()


def play_dealer():
    """Reveal dealer hole and play to 17+, then settle."""
    global dealer_hide_second
    if dealer_hide_second:
        dealer_hide_second = False

    # Dealer hits until 17 or more (simple rule; stands on soft 17)
    while dealer.get_value() < 17:
        new_card = deck.draw_card()
        if new_card:
            dealer.add_card(new_card)
        else:
            break

    player_val = player.get_value()
    dealer_val = dealer.get_value()

    if player_val > 21:
        settle_round("bust")
    elif dealer_val > 21:
        settle_round("player_win")
    elif player_val > dealer_val:
        settle_round("player_win")
    elif player_val < dealer_val:
        settle_round("dealer_win")
    else:
        settle_round("push")


def draw_button(rect, label, enabled=True, hovered=False):
    if not enabled:
        base_color = (70, 70, 70)
    else:
        base_color = (30, 140, 240) if hovered else (0, 120, 220)
    pygame.draw.rect(screen, base_color, rect, border_radius=8)
    pygame.draw.rect(screen, (20, 20, 20), rect, width=2, border_radius=8)
    text_surface = button_font.render(label, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_chip_button(rect, value, hovered=False, enabled=True):
    base_color = (210, 70, 70) if enabled else (90, 90, 90)
    outline = (40, 20, 20)
    if hovered and enabled:
        base_color = (230, 100, 100)
    pygame.draw.ellipse(screen, base_color, rect)
    pygame.draw.ellipse(screen, outline, rect, width=3)
    label = f"${value}"
    text_surface = button_font.render(label, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_text_with_shadow(text, font_obj, color, pos):
    shadow_color = (0, 0, 0)
    shadow_surface = font_obj.render(text, True, shadow_color)
    surface = font_obj.render(text, True, color)
    screen.blit(shadow_surface, (pos[0] + 2, pos[1] + 2))
    screen.blit(surface, pos)


def draw_hand(cards, y_pos, hide_second=False, max_cards=None):
    x_pos = 100
    cards_shown = len(cards) if max_cards is None else min(max_cards, len(cards))
    for idx in range(cards_shown):
        card = cards[idx]
        if hide_second and idx == 1 and backside_image is not None:
            screen.blit(backside_image, (x_pos, y_pos))
        else:
            screen.blit(card.image, (x_pos, y_pos))
        x_pos += 130




while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False

        if show_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    reset_round()
                    show_menu = False
                    menu_start_time = pygame.time.get_ticks()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.collidepoint(event.pos):
                    reset_round()
                    show_menu = False
                    menu_start_time = pygame.time.get_ticks()
            continue

        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_round()
            if event.key == pygame.K_h and not game_over:
                handle_hit()
            if event.key == pygame.K_s and not game_over:
                handle_stay()
            if event.key == pygame.K_q:
                running = False
            if betting and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                start_round()
            if betting:
                if event.key == pygame.K_UP:
                    current_bet = min(balance, current_bet + 10)
                if event.key == pygame.K_DOWN:
                    current_bet = max(10, current_bet - 10)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over and not betting:
            if hit_button.collidepoint(event.pos):
                handle_hit()
            if stay_button.collidepoint(event.pos):
                handle_stay()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if quit_button.collidepoint(event.pos):
                running = False
            if game_over and play_again_button.collidepoint(event.pos):
                reset_round()
            if betting and hit_button.collidepoint(event.pos):
                start_round()
            if betting:
                for rect, val in chip_buttons:
                    if rect.collidepoint(event.pos):
                        current_bet = min(balance, val)

    if show_menu:
        screen.fill((7, 96, 20))
        mouse_pos = pygame.mouse.get_pos()
        hover_play = play_button.collidepoint(mouse_pos)

        elapsed = pygame.time.get_ticks() - menu_start_time
        alpha = max(0, min(255, int((elapsed / 800) * 255)))

        title_text = title_font.render("Blackjack", True, (255, 255, 255))
        title_text.set_alpha(alpha)
        title_rect = title_text.get_rect(center=(640, 200))
        screen.blit(title_text, title_rect)

        instruction_text = info_font.render("Enter/Space: Play  |  Q: Quit", True, (255, 255, 255))
        instruction_text.set_alpha(alpha)
        instruction_rect = instruction_text.get_rect(center=(640, 400))
        screen.blit(instruction_text, instruction_rect)

        draw_button(play_button, "Play Blackjack", enabled=True, hovered=hover_play)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if hover_play else pygame.SYSTEM_CURSOR_ARROW)
        pygame.display.flip()
        clock.tick(60)
        continue

    screen.fill((7, 96, 20))

    score = player.get_value()

    text_color = (255, 255, 255)

    if score > 21 and not game_over:
        text_color = (255, 0, 0)
        settle_round("bust")
    if "bust" in status_message.lower():
        text_color = (255, 0, 0)

    # Handle card animation timing
    current_time = pygame.time.get_ticks()
    if not betting and cards_to_show < 4 and not game_over and current_time - last_card_time >= card_delay:
        cards_to_show += 1
        last_card_time = current_time
        
        # Check for blackjack after all initial cards are dealt
        if cards_to_show == 4 and len(player.hand) == 2 and len(dealer.hand) == 2:
            player_blackjack = player.get_value() == 21
            dealer_blackjack = dealer.get_value() == 21
            
            if player_blackjack or dealer_blackjack:
                dealer_hide_second = False
                if player_blackjack and dealer_blackjack:
                    settle_round("push")
                elif player_blackjack:
                    settle_round("blackjack")
                else:
                    settle_round("dealer_win")
    
    # Show cards based on animation progress
    dealer_cards_visible = min(2, (cards_to_show + 1) // 2) if not betting else 0
    player_cards_visible = min(2, cards_to_show // 2) if not betting else 0
    
    if betting:
        dealer_cards_visible = len(dealer.hand)
        player_cards_visible = len(player.hand)
    
    # Draw dealer section - smaller label above cards
    dealer_label = "Dealer: ?" if dealer_hide_second and not game_over else f"Dealer: {dealer.get_value()}"
    draw_text_with_shadow(dealer_label, info_font, (255, 255, 255), (100, 50))
    draw_hand(dealer.hand, 80, hide_second=dealer_hide_second and not game_over, max_cards=dealer_cards_visible)

    # Draw player section - smaller label above cards
    draw_text_with_shadow(f"Player Points: {score}", info_font, text_color, (100, 320))
    draw_hand(player.hand, 350, max_cards=player_cards_visible)
    
    # Right-side information panel
    info_panel_x = 900
    info_panel_y = 100
    panel_width = 340
    panel_height = 500
    
    # Draw info panel background
    panel_rect = pygame.Rect(info_panel_x, info_panel_y, panel_width, panel_height)
    pygame.draw.rect(screen, (10, 60, 15), panel_rect, border_radius=15)
    pygame.draw.rect(screen, (200, 200, 200), panel_rect, width=3, border_radius=15)
    
    # Info panel title
    draw_text_with_shadow("Game Info", button_font, (255, 215, 0), (info_panel_x + 20, info_panel_y + 20))
    
    # Balance and bet info
    draw_text_with_shadow(f"Balance: ${balance}", info_font, (255, 255, 255), (info_panel_x + 20, info_panel_y + 80))
    draw_text_with_shadow(f"Current Bet: ${current_bet}", info_font, (255, 255, 255), (info_panel_x + 20, info_panel_y + 120))

    # Status message in info panel
    if status_message:
        status_color = (255, 0, 0) if "bust" in status_message.lower() else (100, 255, 100)
        draw_text_with_shadow(status_message, button_font, status_color, (info_panel_x + 20, info_panel_y + 180))

    mouse_pos = pygame.mouse.get_pos()
    buttons_enabled = not game_over and not betting  # Dim Hit/Stay after Stay or bust
    place_enabled = betting and current_bet <= balance and balance > 0
    hover_hit = hit_button.collidepoint(mouse_pos) and (buttons_enabled or place_enabled)
    hover_stay = stay_button.collidepoint(mouse_pos) and buttons_enabled
    hover_quit = quit_button.collidepoint(mouse_pos)
    hover_play_again = game_over and play_again_button.collidepoint(mouse_pos)
    hover_chip = False
    if betting:
        for rect, val in chip_buttons:
            chip_hover = rect.collidepoint(mouse_pos)
            hover_chip = hover_chip or chip_hover

    if betting:
        draw_text_with_shadow("Place your bet", button_font, (255, 215, 0), (250, 280))
        for rect, val in chip_buttons:
            draw_chip_button(rect, val, hovered=rect.collidepoint(mouse_pos), enabled=val <= balance)
        draw_button(hit_button, "Deal", enabled=place_enabled, hovered=hover_hit)
        draw_button(stay_button, "Stay", enabled=False, hovered=False)
    else:
        draw_button(hit_button, "Hit", enabled=buttons_enabled, hovered=hover_hit)
        draw_button(stay_button, "Stay", enabled=buttons_enabled, hovered=hover_stay)
    draw_button(quit_button, "Quit", enabled=True, hovered=hover_quit)
    if game_over:
        draw_button(play_again_button, "Play again", enabled=True, hovered=hover_play_again)

    if hover_hit or hover_stay or hover_quit or hover_play_again or hover_chip:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    # Centered bottom instructions on game screen
    if betting:
        instructions = "Set bet with chips or Up/Down, then Deal (Enter/Space)   |   Q: Quit"
    else:
        instructions = "H: Hit   S: Stay   R: Reset   Q: Quit   Mouse: Buttons"
    instruction_surface = info_font.render(instructions, True, (240, 240, 240))
    instruction_rect = instruction_surface.get_rect(center=(640, 690))
    shadow_surface = info_font.render(instructions, True, (0, 0, 0))
    screen.blit(shadow_surface, (instruction_rect.x + 2, instruction_rect.y + 2))
    screen.blit(instruction_surface, instruction_rect)

    pygame.display.flip()
    clock.tick(60)


pygame.quit()