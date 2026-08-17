"""Parse messy pasted odds into clean {canonical_team: decimal_price}.

Handles decimal (2.5, 2.50), fractional (6/4, 11/8), and loose team names
(Spurs, Man Utd, Nott'm Forest, ...). Deliberately forgiving: the whole point
is that you can paste a block straight off a bookmaker page and it just works.
"""
import re

# Canonical 20 (must match data/teams.txt names exactly).
CANON = [
    "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton",
    "Chelsea", "Coventry", "Crystal Palace", "Everton", "Fulham",
    "Hull City", "Ipswich", "Leeds", "Liverpool", "Man City",
    "Man United", "Newcastle", "Nottingham Forest", "Sunderland", "Tottenham",
]

# Aliases -> canonical. Keys are lowercased, punctuation/spaces stripped.
_ALIASES = {
    "arsenal": "Arsenal", "gunners": "Arsenal",
    "astonvilla": "Aston Villa", "villa": "Aston Villa", "avfc": "Aston Villa",
    "bournemouth": "Bournemouth", "afcbournemouth": "Bournemouth", "cherries": "Bournemouth",
    "brentford": "Brentford", "bees": "Brentford",
    "brighton": "Brighton", "brightonhovealbion": "Brighton", "seagulls": "Brighton", "bha": "Brighton",
    "chelsea": "Chelsea", "cfc": "Chelsea",
    "coventry": "Coventry", "coventrycity": "Coventry", "covcity": "Coventry", "sky blues": "Coventry",
    "crystalpalace": "Crystal Palace", "palace": "Crystal Palace", "cpfc": "Crystal Palace",
    "everton": "Everton", "toffees": "Everton",
    "fulham": "Fulham", "ffc": "Fulham",
    "hull": "Hull City", "hullcity": "Hull City", "tigers": "Hull City",
    "ipswich": "Ipswich", "ipswichtown": "Ipswich", "tractorboys": "Ipswich",
    "leeds": "Leeds", "leedsunited": "Leeds",
    "liverpool": "Liverpool", "lfc": "Liverpool", "reds": "Liverpool",
    "mancity": "Man City", "manchestercity": "Man City", "mcfc": "Man City", "city": "Man City",
    "manutd": "Man United", "manunited": "Man United", "manchesterunited": "Man United",
    "manu": "Man United", "mufc": "Man United", "united": "Man United",
    "newcastle": "Newcastle", "newcastleunited": "Newcastle", "nufc": "Newcastle", "magpies": "Newcastle",
    "nottinghamforest": "Nottingham Forest", "nottmforest": "Nottingham Forest",
    "notts forest": "Nottingham Forest", "forest": "Nottingham Forest", "nffc": "Nottingham Forest",
    "sunderland": "Sunderland", "safc": "Sunderland", "blackcats": "Sunderland",
    "tottenham": "Tottenham", "tottenhamhotspur": "Tottenham", "spurs": "Tottenham", "thfc": "Tottenham",
}


def _key(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def resolve_team(raw):
    """Loose team name -> canonical, or None if unrecognised."""
    k = _key(raw)
    if not k:
        return None
    if k in _ALIASES:
        return _ALIASES[k]
    for canon in CANON:
        if _key(canon) == k:
            return canon
    # last resort: unique prefix match against aliases/canon
    hits = {v for a, v in _ALIASES.items() if a.startswith(k) or k.startswith(a)}
    hits |= {c for c in CANON if _key(c).startswith(k) or k.startswith(_key(c))}
    return next(iter(hits)) if len(hits) == 1 else None


def parse_price(tok):
    """'2.5' | '2' | '6/4' | 'evs' -> decimal price, or None."""
    tok = tok.strip().lower()
    if tok in ("evs", "even", "evens"):
        return 2.0
    m = re.fullmatch(r"(\d+)\s*/\s*(\d+)", tok)          # fractional
    if m:
        return int(m.group(1)) / int(m.group(2)) + 1.0
    m = re.fullmatch(r"\d+(\.\d+)?", tok)                 # decimal
    if m:
        return float(tok)
    return None


def parse_block(text):
    """Extract {team: decimal_price} from a pasted block.

    Each line should contain a team name and a price somewhere. Order-agnostic:
    the price is the last price-looking token, the team is the rest.
    Returns (parsed, unmatched_lines).
    """
    parsed, unmatched = {}, []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        toks = re.split(r"[\s\t]+", line)
        price, price_i = None, None
        for i in range(len(toks) - 1, -1, -1):
            p = parse_price(toks[i])
            if p is not None:
                price, price_i = p, i
                break
        if price is None:
            unmatched.append(line)
            continue
        name = " ".join(toks[:price_i] + toks[price_i + 1:]).strip(" -|:\t")
        team = resolve_team(name)
        if team is None:
            unmatched.append(line)
            continue
        parsed[team] = price
    return parsed, unmatched


def vig_free(prices):
    """{team: decimal_odds} -> {team: P(champion)} normalised to sum 1."""
    raw = {t: 1.0 / o for t, o in prices.items()}
    s = sum(raw.values())
    return {t: v / s for t, v in raw.items()}
