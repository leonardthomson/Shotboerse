from random import randint

from TTS import _TTS


def praise_shots(idx, shot_names, price):
    """
    Funny message when shots are espacially cheap.
    """
    shot_name = shot_names[idx]
    price = price[idx]
    n_praises = 3
    random_idx = randint(0, n_praises - 1)

    shoutouts = [(f"{shot_name} ist billig! Kauft {shot_name}", f"{shot_name} nur {str(round(price))} Cent!"),
                 (f"Kauft {shot_name}!", f"Er ist billig und willig!"),
                 (f"Der {shot_name}-Markt bricht zusammen!", f"Kauft {shot_name}!")]
    shout_out = shoutouts[random_idx]
    engine = _TTS()
    engine.start(shout_out)
    del (engine)

def shoutout(text):
    engine = _TTS()
    engine.start(text)
    del (engine)