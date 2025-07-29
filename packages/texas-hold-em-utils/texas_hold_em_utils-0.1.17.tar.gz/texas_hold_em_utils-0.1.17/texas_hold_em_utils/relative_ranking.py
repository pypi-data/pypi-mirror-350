import copy
from texas_hold_em_utils.deck import Deck
from texas_hold_em_utils.hands import HandOfFive
from texas_hold_em_utils.post_flop_stats_repository import PostflopStatsRepository
from texas_hold_em_utils.preflop_stats_repository import PreflopStatsRepository
from scipy.stats import norm

preflop_stats_repository = PreflopStatsRepository()
postflop_stats_repository = PostflopStatsRepository()

# Source: https://github.com/amarkules1/texas-holdem-notebooks/blob/main/percentiles_from_win_rates.ipynb
percentile_standard_deviations = {
    "flop": 0.20277154473723782,
    "turn": 0.23895325562434003,
    "river": 0.29411125409761246
}


def get_hand_rank_details(hand, community_cards=None, player_count=2, sample_size=1000):
    """
    Calculates win rate and percentile for a given hand at any point in the game
    :param hand: array of 2 cards
    :param community_cards: array of 3-5 cards or None for pre-flop (default None)
    :param player_count: number of players in the game (default 2)
    :param sample_size: number of simulation runs for sample based win rates (post-flop and post-river (default 1000)
    :return: a dict of:
        {
        "expected_win_rate": float between 0 and 1, based on the player_count,
        "expected_2_player_win_rate": float between 0 and 1, assumes 2 players,
        "percentile": float between 0 and 100, how the hand's win rate compares to possible hands for other players,
        "ideal_kelly_max": float between -1 and 1, how much of their stack the player should bet assuming all other players call
        }
    """
    expected_win_rate = 0.0
    expected_2_player_win_rate = 0.0
    percentile = 0.0

    # validate params
    if len(hand) != 2:
        raise ValueError("hand must contain exactly 2 cards")
    if community_cards is not None and len(community_cards) > 5:
        raise ValueError("there can only be up to 5 community cards in texas holdem")
    if player_count < 2:
        raise ValueError("player_count must be at least 2")

    # preflop
    if community_cards is None or len(community_cards) < 3:
        n_player_data = preflop_stats_repository.get_win_rate(hand[0].rank, hand[1].rank, hand[0].suit == hand[1].suit,
                                                              player_count)
        if player_count > 2:
            two_player_data = preflop_stats_repository.get_win_rate(hand[0].rank, hand[1].rank,
                                                                    hand[0].suit == hand[1].suit, 2)
        else:
            two_player_data = n_player_data
        expected_win_rate = n_player_data["win_rate"]
        expected_2_player_win_rate = two_player_data["win_rate"]
        percentile = n_player_data["percentile"]

    # flop 
    if community_cards is not None and len(community_cards) == 3:
        expected_2_player_win_rate = rank_hand_post_flop(hand, community_cards, sample_size=sample_size)

        if player_count > 2:
            expected_win_rate = rank_hand_post_flop(hand, community_cards, n_other_players=(player_count - 1),
                                                    sample_size=sample_size)
            percentile = postflop_stats_repository.get_percentile(expected_win_rate, player_count, 'flop')
        else:
            expected_win_rate = expected_2_player_win_rate
            percentile = expected_percentile(expected_2_player_win_rate, 0.5, percentile_standard_deviations['flop'])
    # turn
    if community_cards is not None and len(community_cards) == 4:
        expected_2_player_win_rate = rank_hand_post_turn(hand, community_cards, sample_size=sample_size)
        if player_count > 2:
            expected_win_rate = rank_hand_post_turn(hand, community_cards, n_other_players=(player_count - 1),
                                                    sample_size=sample_size)
            percentile = postflop_stats_repository.get_percentile(expected_win_rate, player_count, 'turn')
        else:
            expected_win_rate = expected_2_player_win_rate
            percentile = expected_percentile(expected_2_player_win_rate, 0.5, percentile_standard_deviations['turn'])
    # river
    if community_cards is not None and len(community_cards) == 5:
        expected_2_player_win_rate = rank_hand_post_river(hand, community_cards)
        expected_win_rate = expected_2_player_win_rate ** (player_count - 1)
        if player_count > 2:
            percentile = postflop_stats_repository.get_percentile(expected_win_rate, player_count, 'river')
        else:
            percentile = expected_percentile(expected_2_player_win_rate, 0.5, percentile_standard_deviations['river'])

    kelly_max = compute_kelly_max(expected_win_rate, player_count)

    return {
        "expected_win_rate": expected_win_rate,
        "expected_2_player_win_rate": expected_2_player_win_rate,
        "percentile": percentile,
        "ideal_kelly_max": kelly_max
    }


def rank_hand_post_river(hand, community_cards):
    """
    Calculates the expected win rate for a given hand post-river in a Texas Hold'em game.

    Assumes 2 players. To get the win rate for more than 2 players,
    raise the returned value to the number of players minus 1.
    Seems to work based on: https://github.com/amarkules1/texas-holdem-notebooks/blob/main/n_player_win_rates.ipynb

    :param hand: a list of 2 Card objects representing the player's hand
    :param community_cards: a list of 4 Card objects representing the flop, turn, and river
    :return: float: the expected win rate for the given hand
    """
    if len(hand) != 2 or len(community_cards) != 5:
        raise ValueError("Invalid input: hand and community_cards must be lists of 2 and 5 Card objects respectively.")

    player_hand = HandOfFive(hand, community_cards)
    deck1 = Deck()
    deck2 = Deck()
    wins = 0
    losses = 0
    ties = 0
    for card1 in deck1.cards:
        if card1 not in hand + community_cards:
            for card2 in deck2.cards:
                if card2 not in hand + community_cards and card2 != card1:
                    other_hand = HandOfFive([card1, card2], community_cards)
                    if player_hand > other_hand:
                        wins += 1
                    elif player_hand < other_hand:
                        losses += 1
                    else:
                        ties += 1
    return (wins + (0.5 * ties)) / (wins + losses + ties)


def rank_hand_post_turn(hand, flop_and_turn, n_other_players=1, sample_size=1000):
    """
    Calculates the expected win rate for a given hand post-turn in a Texas Hold'em game.

    :param hand: a list of 2 Card objects representing the player's hand
    :param flop_and_turn: a list of 4 Card objects representing the flop and turn
    :param n_other_players: number of other players, excluding the player whose hand is being analyzed (default 1)
    :param sample_size: number of simulation runs (default 1000)
    :return: float: the expected win rate for the given hand
    """
    # Validate params
    if len(hand) != 2 or len(flop_and_turn) != 4:
        raise ValueError("Invalid input: hand and flop_and_turn must be lists of 2 and 4 Card objects respectively.")

    deck = Deck()
    deck.remove(hand[0])
    deck.remove(hand[1])

    deck.remove(flop_and_turn[0])
    deck.remove(flop_and_turn[1])
    deck.remove(flop_and_turn[2])
    deck.remove(flop_and_turn[3])

    wins = 0.0

    for i in range(sample_size):
        deck_cpy = copy.deepcopy(deck)
        deck_cpy.shuffle()

        river = deck_cpy.draw()

        comm = [flop_and_turn[0], flop_and_turn[1], flop_and_turn[2], flop_and_turn[3], river]

        other_hands = []
        for j in range(n_other_players):
            other_hands.append(HandOfFive([deck_cpy.draw(), deck_cpy.draw()], comm))

        player_hand = HandOfFive(hand, comm)

        lost_to = []
        tied_with = []

        for hand_obj in other_hands:
            if player_hand < hand_obj:
                lost_to.append(hand_obj)
            elif player_hand == hand_obj:
                tied_with.append(hand_obj)

        if len(lost_to) == 0:
            wins += 1 / (len(tied_with) + 1)

    return wins / sample_size


def rank_hand_post_flop(hand, flop, n_other_players=1, sample_size=1000):
    """
    Calculates the expected win rate for a given hand post-flop in a Texas Hold'em game.

    :param hand: a list of 2 Card objects representing the player's hand
    :param flop: a list of 3 Card objects representing the flop and turn
    :param n_other_players: number of other players, excluding the player whose hand is being analyzed (default 1)
    :param sample_size: number of simulation runs (default 1000)
    :return: float: the expected win rate for the given hand
    """
    # Validate params
    if len(hand) != 2 or len(flop) != 3:
        raise ValueError("Invalid input: hand and flop must be lists of 2 and 3 Card objects respectively.")

    deck = Deck()
    deck.remove(hand[0])
    deck.remove(hand[1])

    deck.remove(flop[0])
    deck.remove(flop[1])
    deck.remove(flop[2])

    wins = 0.0

    for i in range(sample_size):
        deck_cpy = copy.deepcopy(deck)
        deck_cpy.shuffle()

        turn = deck_cpy.draw()
        river = deck_cpy.draw()

        comm = [flop[0], flop[1], flop[2], turn, river]

        other_hands = []
        for j in range(n_other_players):
            other_hands.append(HandOfFive([deck_cpy.draw(), deck_cpy.draw()], comm))

        player_hand = HandOfFive(hand, comm)

        lost_to = []
        tied_with = []

        for hand_obj in other_hands:
            if player_hand < hand_obj:
                lost_to.append(hand_obj)
            elif player_hand == hand_obj:
                tied_with.append(hand_obj)

        if len(lost_to) == 0:
            wins += 1 / (len(tied_with) + 1)

    return wins / sample_size


def expected_percentile(win_rate, mean, std_dev):
    """
    Calculates the expected percentile for a given win rate based on a normal distribution.

    :param win_rate: the expected win rate (e.g., 0.25 for a 25% chance of winning)
    :param mean: the mean of the normal distribution (e.g., 0.5 )
    :param std_dev: the standard deviation of the normal distribution (e.g., 0.2 for a 20% std. deviation)
    :return: the expected percentile (e.g., 10.0 for a win rate in the 10th percentile)
    """
    z_score = (win_rate - mean) / std_dev
    return norm.cdf(z_score) * 100


def compute_kelly_max(win_rate, player_count):
    """
    computes the kelly max for a given win rate and player count
    :param win_rate: win rate as a proportion (0-1)
    :param player_count: player count including bettor
    :return: kelly max assuming all other players call and win rate is accurate (they won't and it's not)
    """
    p_loss = (1 - win_rate)
    b = player_count - 1
    return win_rate - (p_loss / b)


def compare_hands(hands, community_cards=None, sample_size=1000):
    """
    computes win percentages for each hand of cards in hands
    :param hands: list containing 2-12 lists of exactly two Card() objects each
    :param community_cards: if provided, a list of 3-5 Card() objects representing the community cards (flop/turn/river)
    :param sample_size: number of random samples to take to determine win rates (default 1000)
    :return: an array of floats between 0 and 1, representing the win rates for each hand in order
    """
    # validate
    if len(hands) < 2 or len(hands) > 12:
        raise ValueError("Please provide a number of hands between 2 and 12")
    for i in range(len(hands)):
        if len(hands[i]) != 2:
            raise ValueError(f"Hand at index {i} must have exactly 2 cards")
    if community_cards and (len(community_cards) < 3 or len(community_cards) > 5):
        raise ValueError(f"Community cards must be None or a list of 3-5 cards, found {len(community_cards)}")

    # if there are 5 community cards there's no need to take a sample. outcome is always the same
    if not community_cards:
        community_cards = []

    if len(community_cards) == 5:
        winner_indices = []
        winner = None
        for i in range(len(hands)):
            if len(winner_indices) == 0:
                winner_indices = winner_indices + [i]
                winner = HandOfFive(hands[i], community_cards)
            else:
                hand_of_five = HandOfFive(hands[i], community_cards)
                if hand_of_five > winner:
                    winner_indices = [i]
                    winner = hand_of_five
                elif hand_of_five == winner:
                    winner_indices = winner_indices + [i]
        return [1.0 if i in winner_indices else 0.0 for i in range(len(hands))]

    wins = [0] * len(hands)
    deck = Deck()
    for hand in hands:
        deck.remove(hand[0])
        deck.remove(hand[1])
    for i in range(sample_size):
        sample_deck = copy.deepcopy(deck)
        sample_deck.shuffle()
        community_cards_copy = community_cards.copy()
        while len(community_cards_copy) < 5:
            community_cards_copy.append(sample_deck.draw())
        winner_indices = []
        winner = None
        for i in range(len(hands)):
            if len(winner_indices) == 0:
                winner_indices = winner_indices + [i]
                winner = HandOfFive(hands[i], community_cards_copy)
            else:
                hand_of_five = HandOfFive(hands[i], community_cards_copy)
                if hand_of_five > winner:
                    winner_indices = [i]
                    winner = hand_of_five
                elif hand_of_five == winner:
                    winner_indices = winner_indices + [i]
        for i in winner_indices:
            wins[i] += (1.0 / len(winner_indices))

    win_rates = [win / sample_size for win in wins]
    return win_rates
