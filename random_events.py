import random

# Die Reihenfolge der Shots lautet:
# Tequila, Vodka, Mexikaner, Gimlet

event_list = [
    ["Deflation: Alles wird bspw. 10ct billiger.", (-.1, -.1, -.1, -.1)],
    ["Inflation: Alles wird bspw. 10ct teurer.", (.1,.1,.1,.1)],

    ["Die Gin-Lobby hat eine Tarifverhandlung gewonnen! Gin wird billiger!", (0,0,0,-.15)],
    ["Corona-Ausgleich für Studierende! Mexi wird billiger!", (0,0,-.15,0)],
    ["Soergel wird Bundeskanzler! Er subventioniert Gin!", (0,0,0,-.15)],
    ["Man findet in Junkers Büro große Mengen Vodka-Brause, der Markt wird geflutet!", (0,-.15,0,0)],
    ["Die Fachschaft empfängt eine großzügige Limetten-Spende. Gin wird billiger!", (0,0,0,-.15)],
    ["Wegen des Klimawandels wachsen jetzt Agaven am Kaiserstuhl! Tequila wird billiger!", (-.15, 0,0,0)],
    ["Genmanipulierte Tomaten bringen den Markt ins Wanken! Mexikaner wird billiger!", (0,0, -.15,0)],

    ["Der Alkohol-Konsum der Assistent:innen wirkt sich beträchtlich auf den Markt aus. Mexikaner wird teurer!",
     (0, 0, .15, 0)],
    ["Die Erstis sind frustriert über die Ana-Klausur. Vodka wird teurer!", (0, .15, 0, 0)],
    ["Mexikanische Mauer wird gebaut! Tequila und Mexi werden teurer!", (.15, 0, .15, 0)],
    ["Huber kauft beträchtliche Mengen des Weltmarkts an Gin auf. Gin wird rar!", (0, 0, 0, .15)],
    ["Putin fuckt ab. Vodka wird teurer!", (0, .15, 0, 0)],
    ["Ein kaputtes Schiff hat den Limetten Weltmarkt ins Wanken gebracht! Gin wird teurer!", (0,0,0,.15)],

    ["Sozialverbände protestieren gegen die hohen Lebenserhaltungskosten! Es passiert nichts!", (0,0,0,0)],
    ["Der Bundeskanzler ist in einen Finanzskandal verwickelt! Es passiert nichts!", (0,0,0,0)],
    ["Der Studiengang wird reakkreditiert. Es passiert nichts!", (0,0,0,0)],
    ["Die Vorlesungen werden evaluiert. Es passiert nichts!", (0,0,0,0)],
    ["Der StuRa veröffentlich eine Pressemitteilung gegen Diskriminierung. Es passiert nichts!", (0,0,0,0)],
    ["Die Fachschaftssitzung geht mal wieder 3 Stunden. Es passiert nichts!", (0,0,0,0)],
    ["Du kriegst eine nicht deklarierte Parteispende. Eine Gin-Option!", (0,0,0,0)],
    ["Der mexikanische Präsident lädt Dich auf seine Jacht ein. Eine Mexikaner-Option!", (0,0,0,0)],
    ["Beim Golfen lernst Du Gerhard Schröder kennen. Eine Vodka-Option!", (0,0,0,0)],
    ["Du erhältst brisante Nachrichten über den mexikanischen Agrar-Minister. Um Dich zum Schweigen zu bringen, erhältst Du eine Tequila-Option!", (0,0,0,0)],
    ["Du findest auf dem Dachboden Deinen alten Bitcoin-Usb-Stick. Du erhältst 2 Optionen Deiner Wahl!", (0,0,0,0)],
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

def all_events():
    return event_list

if __name__ == "__main__":
    print_events()
    print(f"Debug_sums: {debug_event_list()}")
