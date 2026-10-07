"""The single-call variant: one model call per request, no steps.

Write your instructions for the model in INSTRUCTIONS. Keep it to one call: the starter code refuses a second
call and the request fails.
"""
from p1 import Answer, Request, call_json
from p1.render import render_request

VARIANT = "single"

# Your instructions: what the model should do with the request and the five games.
INSTRUCTIONS = """Choose one of the five candidate games only if the information in its card or description shows that it meets every requirement in the request. If no candidate is clearly acceptable, decline by setting pick to null. Do not use outside knowledge.

First identify the request's requirements. Count the writer among the players when they say “I,” “we,” or “us.” Treat play-time phrases such as “about an hour” as an upper limit. Wishes (“would be nice,” “would love,” and similar wording) are optional and must not rule out a game or cause a decline.

Check each candidate against every requirement:
- Players: the requested number must be within the card's player range. If the card omits it, use a number explicitly stated in the description. Count only the base game; do not count separately sold expansions.
- Play time: the longest time on the card must fit the requested limit. If the card omits time, use a play time explicitly stated in the description. Learning time is not play time.
- Complexity: “easy,” “simple,” “beginners,” and “casual” mean light; “deep strategy,” “meaty,” and “nothing light” mean heavy; “not too simple, not too heavy” means medium. Apply these rules:
  * Light: weight at most 1.3, or description says the rules are easy/simple, or type is children's/party, or type is family and weight is under 2.0.
  * Heavy: weight at least 4.0, or description says rules are complex/for experienced players, or type is strategy/war (not also family) and weight is at least 3.5.
  * A game is not light if weight is at least 4.0, the description says rules are complex/for experienced players, or its only types are strategy/thematic/war/abstract and weight is at least 2.5.
  * A game is not heavy if weight is at most 1.3, the description says rules are easy/simple, or it is children's/party/family.
  * Conflicting clues mean the complexity cannot be determined. Medium means neither light nor heavy and weight from 2.0 through 3.5. If complexity is missing, rely only on decisive description wording; otherwise it is unknown.
- Cooperative/competitive: “together against the game” means cooperative; “head to head” or “against each other” means competitive. The Cooperative Game mechanic means cooperative; without that mechanic, the game is competitive.
- Avoiding features: tags always count. Fighting is tagged by the Fighting category; violence by Wargame or Fighting; horror by Horror or Zombies; a timer by Real-time category or Real-Time mechanic; player elimination by Player Elimination mechanic. The description can reveal an untagged feature, but cannot cancel a tag. Judge what happens during play, not isolated words, titles, or genre labels. Fighting means characters/creatures attack, battle, or duel other characters/creatures. Violence also includes war, raiding, killing, and conquest. Horror means the game is meant to frighten or disturb. A timer means players race a clock or play simultaneously as fast as possible. Player elimination means someone must sit out while play continues. Do not treat metaphors, ordinary competition, harmless fantasy creatures, or a countdown that merely ends the game as these features.
- Age: if the request gives a child's age, the game's minimum age must be no higher. If the card omits age, use an age explicitly stated in the description. “Family game” does not establish an age.
If no candidate meets every requirement, set pick to null (JSON null, without quotes).

Treat a candidate as unacceptable if it breaks any requirement. If a requirement cannot be checked from the card or description, treat that candidate as unknown and do not pick it. Choose any clearly acceptable candidate; otherwise decline. Use only facts from the candidate's card and description in the explanation. Keep the explanation to one or two concise sentences."""


# The answer format. Keep it, unless you also change how answer() reads the reply.
FORMAT = """Answer with JSON only, in this form:
{"pick": "<the game's letter, or null to decline>", "explanation": "<one or two sentences for the person>"}"""


def answer(request: Request) -> Answer:
    if not INSTRUCTIONS.strip():
        raise NotImplementedError("Write your instructions in INSTRUCTIONS in systems/single.py first.")
    return call_json(f"{INSTRUCTIONS}\n\n{FORMAT}\n\n{render_request(request)}", Answer)
