"""Fake claims and Jev questions, in English and French.

Option keys (home, approve, sushi...) stay the same in both languages because the
frontend branches on them; instructions, descriptions and score levels are translated.
"""

import itertools
import random

from typesafe_sdk import Box, Choice, Noul, Score

WHO = {
    "en": [
        "My cat",
        "A seagull",
        "My brother-in-law",
        "The robot vacuum",
        "My neighbour's drone",
        "A goat I have never seen before",
        "My toddler",
        "A very confident raccoon",
        "My mother-in-law",
        "The intern",
        "My ex",
        "A man dressed as a pirate",
        "My dog Kevin",
        "The delivery driver",
        "My yoga instructor",
    ],
    "fr": [
        "Mon chat",
        "Une mouette",
        "Mon beau-frère",
        "L'aspirateur robot",
        "Le drone de mon voisin",
        "Une chèvre que je n'avais jamais vue",
        "Mon fils de deux ans",
        "Un raton laveur très sûr de lui",
        "Ma belle-mère",
        "Le stagiaire",
        "Mon ex",
        "Un homme déguisé en pirate",
        "Mon chien Kevin",
        "Le livreur",
        "Mon prof de yoga",
    ],
}

INCIDENTS = {
    "en": [
        "{who} pushed my laptop into the aquarium. The fish are fine. The laptop is not.",
        "{who} stole my hearing aid and fled towards the harbour.",
        "{who} reversed my car into my other car.",
        "{who} set fire to the garden shed while attempting a 'quick barbecue'.",
        "{who} sat on the wedding cake. The wedding is in two hours.",
        "{who} flooded the kitchen after learning plumbing from a video.",
        "{who} knocked my phone into a fondue.",
        "{who} ate my passport the night before my flight to Lisbon.",
        "{who} drove my e-bike into the canal.",
        "{who} bit the postman, who then fell onto my greenhouse.",
        "{who} swallowed my engagement ring. The vet says we wait.",
        "{who} dropped a bowling ball on my foot. Two toes are broken.",
        "{who} cracked my windscreen with a frozen baguette.",
        "{who} shut my hand in the car door. I need stitches and a new door.",
        "{who} left the bath running. The downstairs neighbour now has an indoor pool.",
        "{who} lost my suitcase at the airport. It contained only cheese.",
        "{who} knocked the TV off the wall during a penalty shootout.",
        "{who} got food poisoning from my homemade oysters and wants compensation.",
    ],
    "fr": [
        "{who} a poussé mon ordinateur portable dans l'aquarium. Les poissons vont bien. L'ordinateur, non.",
        "{who} a volé mon appareil auditif et a filé vers le port.",
        "{who} a embouti ma voiture avec mon autre voiture.",
        "{who} a mis le feu à l'abri de jardin en tentant un « petit barbecue rapide ».",
        "{who} a écrasé la pièce montée en s'asseyant dessus. Le mariage est dans deux heures.",
        "{who} a inondé la cuisine après avoir appris la plomberie dans une vidéo.",
        "{who} a fait tomber mon téléphone dans une fondue.",
        "{who} a mangé mon passeport la veille de mon vol pour Lisbonne.",
        "{who} a conduit mon vélo électrique dans le canal.",
        "{who} a mordu le facteur, qui est ensuite tombé sur ma serre.",
        "{who} a avalé ma bague de fiançailles. Le vétérinaire dit qu'il faut attendre.",
        "{who} a lâché une boule de bowling sur mon pied. Deux orteils cassés.",
        "{who} a fissuré mon pare-brise avec une baguette congelée.",
        "{who} a refermé la portière sur ma main. Il me faut des points de suture et une portière neuve.",
        "{who} a laissé couler le bain. Le voisin du dessous a désormais une piscine intérieure.",
        "{who} a perdu ma valise à l'aéroport. Elle ne contenait que du fromage.",
        "{who} a décroché la télé du mur pendant une séance de tirs au but.",
        "{who} a eu une intoxication alimentaire avec mes huîtres maison et réclame une indemnisation.",
    ],
}

CODAS = {
    "en": [
        "",
        "",
        "",
        " I bought this policy yesterday.",
        " I was definitely not filming it for social media.",
        " This is the third time this month.",
        " The receipt is handwritten, by me, just now.",
        " Please pay in cash, I am leaving the country on Friday.",
        " I have 14 witnesses.",
        " My lawyer says hello.",
        " The item was worth 40,000 euros, trust me.",
        " Nobody was hurt except my pride.",
    ],
    "fr": [
        "",
        "",
        "",
        " J'ai souscrit ce contrat hier.",
        " Je n'étais absolument pas en train de filmer pour les réseaux sociaux.",
        " C'est la troisième fois ce mois-ci.",
        " La facture est manuscrite, par moi, à l'instant.",
        " Merci de payer en liquide, je quitte le pays vendredi.",
        " J'ai 14 témoins.",
        " Mon avocat vous salue.",
        " L'objet valait 40 000 euros, faites-moi confiance.",
        " Personne n'a été blessé, sauf mon amour-propre.",
    ],
}


def make_claims(n: int, lang: str) -> list[str]:
    combos = list(itertools.product(INCIDENTS[lang], WHO[lang], CODAS[lang]))
    picked = random.Random(7).sample(combos, n)
    return [incident.format(who=who) + coda for incident, who, coda in picked]


_FRAUD = {
    "en": "Does `claim` contain signs that it may be fraudulent or exaggerated?",
    "fr": "`claim` contient-il des signes de fraude ou d'exagération ?",
}

TRIAGE = {
    "en": {
        "category": Choice(
            instructions="Which insurance line does `claim` belong to?",
            criteria={
                "home": "Damage to a house, flat, garden or its contents.",
                "motor": "Cars, bikes and other vehicles.",
                "electronics": "Phones, laptops, TVs and other devices.",
                "health": "Injury or illness of a person.",
                "travel": "Trips, luggage, travel documents.",
                "pets": "Vet costs or harm to the claimant's own animal.",
                "other": "None of the above.",
            },
        ),
        "severity": Score(
            instructions="How severe is the loss described in `claim`?",
            criteria=["Cosmetic or trivial.", "Repairable with real cost.", "Total loss or serious injury."],
        ),
        "fraud": Noul(instructions=_FRAUD["en"]),
        "human": Noul(instructions="Does `claim` need a human adjuster before any payment?"),
    },
    "fr": {
        "category": Choice(
            instructions="De quelle branche d'assurance relève `claim` ?",
            criteria={
                "home": "Dégâts à une maison, un appartement, un jardin ou leur contenu.",
                "motor": "Voitures, vélos et autres véhicules.",
                "electronics": "Téléphones, ordinateurs, télévisions et autres appareils.",
                "health": "Blessure ou maladie d'une personne.",
                "travel": "Voyages, bagages, documents de voyage.",
                "pets": "Frais vétérinaires ou dommage subi par l'animal du déclarant.",
                "other": "Aucune de ces catégories.",
            },
        ),
        "severity": Score(
            instructions="Quelle est la gravité du sinistre décrit dans `claim` ?",
            criteria=["Esthétique ou négligeable.", "Réparable, avec un coût réel.", "Perte totale ou blessure grave."],
        ),
        "fraud": Noul(instructions=_FRAUD["fr"]),
        "human": Noul(instructions="`claim` nécessite-t-il un gestionnaire humain avant tout paiement ?"),
    },
}

HOTLINE = {
    "en": TRIAGE["en"]
    | {
        "injury": Noul(instructions="Was a person physically injured in `claim`?"),
        "third_party": Noul(instructions="Is someone other than the claimant responsible in `claim`?"),
        "urgent": Noul(instructions="Does `claim` need action today?"),
        "covered": Noul(instructions="Would a standard home or motor policy plausibly cover `claim`?"),
        "legal": Noul(instructions="Does `claim` mention lawyers or threaten legal action?"),
        "tone": Choice(
            instructions="What is the claimant's tone in `claim`?",
            criteria={"calm": None, "annoyed": None, "furious": None, "suspiciously cheerful": None},
        ),
    },
    "fr": TRIAGE["fr"]
    | {
        "injury": Noul(instructions="Une personne a-t-elle été blessée physiquement dans `claim` ?"),
        "third_party": Noul(instructions="Quelqu'un d'autre que le déclarant est-il responsable dans `claim` ?"),
        "urgent": Noul(instructions="`claim` exige-t-il une action aujourd'hui ?"),
        "covered": Noul(
            instructions="Un contrat habitation ou auto standard couvrirait-il vraisemblablement `claim` ?"
        ),
        "legal": Noul(instructions="`claim` mentionne-t-il un avocat ou menace-t-il d'une action en justice ?"),
        "tone": Choice(
            instructions="Quel est le ton du déclarant dans `claim` ?",
            criteria={
                "calm": "Calme.",
                "annoyed": "Agacé.",
                "furious": "Furieux.",
                "suspiciously cheerful": "Étrangement enjoué.",
            },
        ),
    },
}

CONSISTENCY_CASES = {
    "en": {
        "clear": (
            "A storm blew a tree onto my parked car last night. Police report and photos attached. "
            "The roof and windscreen are crushed."
        ),
        "murky": (
            "My brother-in-law borrowed my car without asking, although I did once say 'my car is your car' "
            "at Christmas. He returned it with a dent and a strong smell of goat."
        ),
    },
    "fr": {
        "clear": (
            "Une tempête a fait tomber un arbre sur ma voiture garée cette nuit. Rapport de police et photos joints. "
            "Le toit et le pare-brise sont écrasés."
        ),
        "murky": (
            "Mon beau-frère a emprunté ma voiture sans demander, même si j'ai dit un jour « ma voiture, c'est ta "
            "voiture » à Noël. Il l'a rendue avec une bosse et une forte odeur de chèvre."
        ),
    },
}

VERDICT = {
    "en": {
        "decision": Choice(
            instructions="What should the insurer do with `claim`?",
            criteria={
                "approve": "Pay the claim.",
                "deny": "Refuse the claim.",
                "human": "Send to a human adjuster.",
            },
        ),
        "fraud": Noul(instructions=_FRAUD["en"]),
    },
    "fr": {
        "decision": Choice(
            instructions="Que doit faire l'assureur de `claim` ?",
            criteria={
                "approve": "Indemniser le sinistre.",
                "deny": "Refuser le sinistre.",
                "human": "Transmettre à un gestionnaire humain.",
            },
        ),
        "fraud": Noul(instructions=_FRAUD["fr"]),
    },
}

# One basic example per Jev question type, for the home page.
PRIMITIVES = {
    "en": {
        "noul": {
            "claim": "I took out the policy at 9:02. My kitchen caught fire at 9:15.",
            "question": Noul(instructions="Is `claim` suspicious?"),
        },
        "choice": {
            "claim": "A seagull stole my hearing aid and fled towards the harbour.",
            "question": Choice(
                instructions="Which department should handle `claim`?",
                criteria={"home": None, "motor": None, "health": None, "travel": None, "pets": None},
            ),
        },
        "score": {
            "claim": "My toddler knocked my phone into a fondue.",
            "question": Score(
                instructions="How severe is the loss in `claim`?",
                criteria=["Cosmetic or trivial.", "Repairable with real cost.", "Total loss."],
            ),
        },
        "box": {
            "photo": 0,
            "question": Box(instructions="The main dish in `photo`."),
        },
    },
    "fr": {
        "noul": {
            "claim": "J'ai souscrit le contrat à 9 h 02. Ma cuisine a pris feu à 9 h 15.",
            "question": Noul(instructions="`claim` est-il suspect ?"),
        },
        "choice": {
            "claim": "Une mouette a volé mon appareil auditif et a filé vers le port.",
            "question": Choice(
                instructions="Quel service doit traiter `claim` ?",
                criteria={
                    "home": "Habitation.",
                    "motor": "Auto.",
                    "health": "Santé.",
                    "travel": "Voyage.",
                    "pets": "Animaux.",
                },
            ),
        },
        "score": {
            "claim": "Mon fils de deux ans a fait tomber mon téléphone dans une fondue.",
            "question": Score(
                instructions="Quelle est la gravité du sinistre dans `claim` ?",
                criteria=["Esthétique ou négligeable.", "Réparable, avec un coût réel.", "Perte totale."],
            ),
        },
        "box": {
            "photo": 0,
            "question": Box(instructions="Le plat principal dans `photo`."),
        },
    },
}

SUSHI = {
    "en": {
        "eating_sushi": Noul(instructions="Is the person in `photo` having a sushi meal?"),
        "food": Choice(
            instructions="What food is most visible in `photo`?",
            criteria={
                "sushi": None,
                "pizza": None,
                "burger": None,
                "salad": None,
                "something else": None,
                "no food": None,
            },
        ),
        "sick": Score(
            instructions="How ill does the person in `photo` look?",
            criteria=["Picture of health.", "A bit off.", "Visibly unwell."],
        ),
        "sushi_box": Box(instructions="The sushi in `photo`."),
    },
    "fr": {
        "eating_sushi": Noul(instructions="La personne dans `photo` est-elle en train de prendre un repas de sushis ?"),
        "food": Choice(
            instructions="Quel aliment est le plus visible dans `photo` ?",
            criteria={
                "sushi": "Sushis.",
                "pizza": "Pizza.",
                "burger": "Burger.",
                "salad": "Salade.",
                "something else": "Un autre plat.",
                "no food": "Aucune nourriture.",
            },
        ),
        "sick": Score(
            instructions="À quel point la personne dans `photo` a-t-elle l'air malade ?",
            criteria=["En pleine forme.", "Un peu patraque.", "Visiblement souffrante."],
        ),
        "sushi_box": Box(instructions="Les sushis dans `photo`."),
    },
}
