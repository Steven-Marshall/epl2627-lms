"""Punching-bag strategy vs the optimal planner.

    python bag.py [bag=Hull City] [horizon=12]
"""
import sys

from lms.bag import bag_route, repick_ok
from lms.matrix import build_matrix
from lms.planner import plan, survival_curve


def show(route, title):
    print(f"\n{title}")
    print(f"  {'rnd':>3}  {'pick':<18}{'venue':<8}{'P(win)':>7}{'P(alive)':>10}  src")
    print("  " + "-" * 55)
    soft = []
    for rnd, team, pw, alive in survival_curve(route):
        pick_home = route[rnd].get("pick_home", route[rnd].get("home"))
        venue = "HOME" if pick_home else "away"
        flag = ""
        if not pick_home:
            flag += " away"
        if pw < 0.55:
            flag += " SOFT"
            soft.append(rnd)
        print(f"  {rnd:>3}  {team:<18}{venue:<8}{pw*100:>6.1f}%{alive*100:>9.1f}%  "
              f"{route[rnd]['src']}{flag}")
    return soft


def main():
    bag = sys.argv[1] if len(sys.argv) > 1 else "Hull City"
    horizon = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    cells = build_matrix()

    route = bag_route(bag, horizon=horizon, cells=cells)
    ok = repick_ok(route)
    soft = show(route, f"PUNCHING BAG = {bag} (pick its opponent every round)")
    print(f"\n  no-repick legal over {horizon} rounds: {ok}")
    print(f"  soft rounds (P(win) < 55%): {soft or 'none'}")

    opt, _ = plan(horizon=horizon, cells=cells)
    show(opt, "OPTIMAL PLANNER (for comparison)")

    # headline: survival to a few checkpoints
    bag_curve = {r: a for r, _, _, a in survival_curve(route)}
    opt_curve = {r: a for r, _, _, a in survival_curve(opt)}
    print("\n  P(still alive) — bag vs optimal:")
    print(f"  {'after round':<14}{'bag':>8}{'optimal':>10}{'gap':>8}")
    for r in (4, 6, 8, 10, 12):
        if r in bag_curve and r in opt_curve:
            b, o = bag_curve[r], opt_curve[r]
            print(f"  {r:<14}{b*100:>7.1f}%{o*100:>9.1f}%{(o-b)*100:>+7.1f}")


if __name__ == "__main__":
    main()
