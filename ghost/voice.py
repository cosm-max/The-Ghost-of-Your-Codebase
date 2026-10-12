"""The ghost's personality. Pure presentation: no analysis happens here."""
LINES = {
    "long_function": ["{d} drags on forever. I died of old age before the end.",
                      "{d}: even the dead need a break. Split it up."],
    "deep_nesting": ["{d} deep. This is a crypt, and I got lost in it.",
                     "So many ifs and loops ({d}). Flatten it before it buries you."],
    "too_many_params": ["{d} arguments? I can't remember that many names, and I'm immortal.",
                        "{d}. Group these into an object."],
    "mutable_default": ["In {d}, that default list or dict is shared by every call. A curse that never lifts.",
                        "{d} remembers its default between calls. Use None and build it inside."],
    "bare_except": ["A bare except catches everything, even my screams. Name the error.",
                    "Catching all errors blindly? That's how ghosts are made."],
    "swallowed_error": ["You buried this error with pass. It will rise again.",
                        "Silent failures are my favourite. Log it or handle it."],
    "unused_variable": ["'{d}' is set and never read. A restless spirit with no purpose.",
                        "I haunt '{d}' because nothing ever uses it. Delete it."],
    "syntax_error": ["I can't even read this. Python says: {d}."],
}


def speak(f):
    options = LINES[f.rule]
    return options[f.line % len(options)].format(d=f.detail)


def verdict(score):
    if score == 0:
        return "Peaceful. Nothing here to haunt."
    if score <= 25:
        return "Restless. A few spirits linger."
    if score <= 60:
        return "Haunted. This code needs an exorcism."
    return "Cursed. Rewrite with care."
