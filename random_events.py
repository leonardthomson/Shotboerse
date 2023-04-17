import random
import numpy as np

# Die Reihenfolge der Shots lautet:
# Tequila, Vodka, Mexikaner, Gimlet

event_list = [
    ["Deflation! Alles wird billiger!", (-10, -10, -10, -10)],
    ["Inflation: Alles wird teurer!", (10, 10, 10, 10)],

    ["Die Gin-Lobby hat eine Tarifverhandlung gewonnen!\n Gin wird billiger!", (0,-15,0,0)],
    ["Corona-Ausgleich für Studierende!\n Mexi wird billiger!", (-15,0,0,0)],
    ["Soergel wird Bundeskanzler!\n Er subventioniert Gin!", (0,-15,0,0)],
    ["Man findet in Junkers Büro große Mengen Vodka-Brause.\n Der Markt wird geflutet!", (0,0,0,-15)],
    ["Die Fachschaft empfängt eine großzügige Limetten-Spende.\n Gin wird billiger!", (0,-15,0,0)],
    ["Wegen des Klimawandels wachsen jetzt Agaven am Kaiserstuhl!\n Tequila wird billiger!", ( 0,0,-15,0)],
    ["Genmanipulierte Tomaten bringen den Markt ins Wanken!\n Mexikaner wird billiger!", (-15,0,0, 0)],

    ["Der Alkohol-Konsum der Assistent:innen wirkt sich beträchtlich auf den Markt aus.\n Mexikaner wird teurer!",
     (15,0, 0, 0)],
    ["Die Erstis sind frustriert über die Ana-Klausur.\n Vodka wird teurer!", (0, 0, 0, 15)],
    ["Die Mexikanische Mauer wird gebaut!\n Tequila und Mexi werden teurer!", (15, 0, 15, 0)],
    ["Huber kauft beträchtliche Mengen des Weltmarkts an Gin auf.\n Gin wird rar!", (0, 15, 0, 0)],
    ["Putin fuckt ab.\n Vodka wird teurer!", (0,  0, 0,15)],
    ["Ein kaputtes Schiff hat den Limetten Weltmarkt ins Wanken gebracht!\n Gin wird teurer!", (0,15,0,0)],

    ["Sozialverbände protestieren gegen die hohen Lebenserhaltungskosten!\n Es passiert nichts!", (0,0,0,0)],
    ["Der Bundeskanzler ist in einen Finanzskandal verwickelt!\n Es passiert nichts!", (0,0,0,0)],
    ["Der Studiengang wird reakkreditiert.\n Es passiert nichts!", (0,0,0,0)],
    ["Die Vorlesungen werden evaluiert.\n Es passiert nichts!", (0,0,0,0)],
    ["Der StuRa veröffentlich eine Pressemitteilung gegen Diskriminierung.\n Es passiert nichts!", (0,0,0,0)],
    ["Die Fachschaftssitzung geht mal wieder 3 Stunden.\n Es passiert nichts!", (0,0,0,0)],
    ["Du kriegst eine nicht deklarierte Parteispende.\n Eine Gin-Option!", (0,0,0,0)],
    ["Der mexikanische Präsident lädt Dich auf seine Jacht ein.\n Eine Mexikaner-Option!", (0,0,0,0)],
    ["Beim Golfen lernst Du Gerhard Schröder kennen.\n Eine Vodka-Option!", (0,0,0,0)],
    ["Du erhältst brisante Nachrichten über den mexikanischen Agrar-Minister.\n Um Dich zum Schweigen zu bringen, erhältst Du eine Tequila-Option!", (0,0,0,0)],
    ["Du findest auf dem Dachboden Deinen alten Bitcoin-Usb-Stick.\n Du erhältst 2 Optionen Deiner Wahl!", (0,0,0,0)],
]

def print_events():
    for event_idx in range(len(event_list)):
        print(f"{event_idx}: \t {event_list[event_idx][0]}")

def debug_event_list():
    n_shots = len(event_list[0][1])
    shot_price_sums = [0 for _ in range(n_shots)]

    for event_idx in range(len(event_list)):
        for shot_idx in range(n_shots):
            shot_price_sums[shot_idx] += event_list[event_idx][1][shot_idx]

    return shot_price_sums

def one_event(idx=None):
    if idx is None:
        idx = random.randint(0, len(event_list))
    return event_list[idx]

def get_events():
    """Returns a randomized list of events."""

    event_permutation = list(np.random.permutation(len(event_list)))
    randomized_event_list = [event_list[idx] for idx in event_permutation]
    return randomized_event_list

def do_a_random_walk(n_steps, start_value=100, step_size = 1):
    """Returns a list of n_steps random values between -1 and 1."""
    # Default start_value has to be set here
    steps = np.zeros(n_steps)
    steps[0] = start_value
    for i in range(0, n_steps-1):
        steps[i+1] = random.randint(-1, 1) * step_size + steps[i]
    return steps

def do_multiple_random_walks(n_walks, n_steps, start_value=100, step_size = 1):
    """Returns a list of n_walks random walks with n_steps each."""
    all_walks = np.zeros((n_walks, n_steps))
    for i in range(n_walks):
        all_walks[i, :] = do_a_random_walk(n_steps, start_value, step_size)
    return all_walks

def valid_random_walks(n_walks, n_steps, start_value=100, step_size=1, epsilon=15):
    all_walks = do_multiple_random_walks(n_walks=n_walks, n_steps=n_steps, start_value=start_value, step_size=step_size)
    while np.abs(error :=(sum(all_walks[:,-1]-start_value))) > epsilon:
        #error = sum(np.abs(all_walks[:,-1]-start_value))
        all_walks = do_multiple_random_walks(n_walks=n_walks, n_steps=n_steps, start_value=start_value, step_size=step_size)
    print(f"We start with an starting error of {error} cents!")
    return all_walks
def smoothen_end_of_random_walks(all_walks, n_steps, step_size=100, avg=100):
    for i in range(1, n_steps-1):
        all_walks[:, -n_steps + i] = avg + (all_walks[:, -n_steps + i - 1] - avg)/n_steps*(n_steps -i) + np.random.random(all_walks.shape[0]) * step_size
    return all_walks


if __name__ == "__main__":
    print_events()
    val_list = debug_event_list()
    print(f"Debug_sums: {val_list}")
    print(f"So the Increase through events is {sum(val_list)}")

