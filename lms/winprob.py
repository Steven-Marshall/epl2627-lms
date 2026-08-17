"""Match outcome model: rating gap -> P(home win / draw / away win).

Supremacy-Poisson (the classic bookmaker shape):
    supremacy = SUP_PER_RATING * (rating_home - rating_away) + HFA_GOALS
    lambda_home = (TOTAL_GOALS + supremacy) / 2
    lambda_away = (TOTAL_GOALS - supremacy) / 2
then two independent Poissons give the scoreline grid -> H/D/A.

Constants are EPL priors, deliberately tunable. They are PROVISIONAL until real
1X2 match odds arrive: near-term rounds should be driven by market prices
directly (see round_winprob), with this model only projecting unpriced rounds
for the no-repick lookahead.
"""
import math

HFA_GOALS = 0.30        # home advantage, in expected goals
TOTAL_GOALS = 2.85      # baseline combined expected goals
SUP_PER_RATING = 0.037  # goals of supremacy per rating (expected-points) point
MAX_GOALS = 10


def _pois(lam, k):
    return math.exp(-lam) * lam ** k / math.factorial(k)


def match_probs(rating_home, rating_away):
    """(rating_home, rating_away) -> (pH, pD, pA)."""
    sup = SUP_PER_RATING * (rating_home - rating_away) + HFA_GOALS
    lam_h = max(0.12, (TOTAL_GOALS + sup) / 2)
    lam_a = max(0.12, (TOTAL_GOALS - sup) / 2)
    ph = [_pois(lam_h, k) for k in range(MAX_GOALS + 1)]
    pa = [_pois(lam_a, k) for k in range(MAX_GOALS + 1)]
    pH = pD = pA = 0.0
    for i in range(MAX_GOALS + 1):
        for j in range(MAX_GOALS + 1):
            p = ph[i] * pa[j]
            if i > j:
                pH += p
            elif i == j:
                pD += p
            else:
                pA += p
    s = pH + pD + pA
    return pH / s, pD / s, pA / s


def win_prob(rating_team, rating_opp, home):
    """P(the team of interest WINS its match)."""
    if home:
        pH, _, _ = match_probs(rating_team, rating_opp)
        return pH
    _, _, pA = match_probs(rating_opp, rating_team)
    return pA


if __name__ == "__main__":
    # calibration anchors — eyeball these to set SUP_PER_RATING
    from lms.strength import ratings
    R = ratings()
    checks = [
        ("Arsenal", "Coventry", True), ("Arsenal", "Hull City", True),
        ("Man City", "Ipswich", True), ("Liverpool", "Everton", True),
        ("Arsenal", "Man City", True), ("Everton", "Fulham", True),
        ("Coventry", "Arsenal", False), ("Chelsea", "Brentford", True),
    ]
    print(f"SUP_PER_RATING = {SUP_PER_RATING}\n")
    print(f"{'home':<12}{'away':<12}{'pH':>7}{'pD':>7}{'pA':>7}")
    print("-" * 45)
    for a, b, _ in checks:
        pH, pD, pA = match_probs(R[a], R[b])
        print(f"{a:<12}{b:<12}{pH*100:>6.1f}%{pD*100:>6.1f}%{pA*100:>6.1f}%")
