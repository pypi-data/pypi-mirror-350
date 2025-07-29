def old_serialize_game_state(game_state: dict):
    state = game_state.copy()

    state['pile_top'] = str(state['pile_top'])
    keys: list[str] = state.keys()

    for key in keys:
        if key.startswith("player_"):
                state[key] = [str(card) for card in state[key]]

    return state

def serialize_game_state(game_state: dict):
    state = game_state.copy()

    state['pile_top'] = [{'suit': str(state['pile_top'].suit), 'face': state['pile_top'].face } ]
    keys: list[str] = state.keys()

    for key in keys:
        if key.startswith("player_"):
                state[key] = [{'suit': str(card.suit), 'face': card.face } for card in state[key]]

    return state

def serialize_game_view(view: dict):
    state = view.copy()

    state['pile_top'] = [{'suit': str(state['pile_top'].suit), 'face': state['pile_top'].face } ]
    keys: list[str] = state.keys()

    for key in keys:
        if key.startswith("player_"):
                if type(state[key]) != int:
                    state[key] = [{'suit': str(card.suit), 'face': card.face } for card in state[key]]

    return state