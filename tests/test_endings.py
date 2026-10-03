"""Exercise ending narration through real commands, without changing game state."""

from pathlib import Path
import subprocess
import sys
import unittest


GAME = Path(__file__).resolve().parents[1] / "ciaccos_submarket.py"

# Visit every department, returning from dead ends before reaching the Exit.
TOUR = [
    ("East", "spirits"), ("West", None), ("North", "bread"),
    ("East", "paper"), ("North", "beef"), ("North", "ticket"),
    ("South", None), ("West", "potato"), ("West", "milk"),
    ("North", "cleaner"), ("East", "chips"), ("South", None),
    ("East", None), ("East", None),
]


def commands_for(ending, refused=False, took_nothing=False):
    commands = []
    if took_nothing:
        commands += ["get nothing", "y"]
    if ending == "early":
        return commands + ["go North", "go North", "go East", "go East"]
    for direction, item in TOUR:
        commands.append("go " + direction)
        if item == "spirits" and refused:
            commands += ["get spirits", "n"]
        if item and (ending == "full" or (ending == "partial" and item == "spirits")):
            commands += ["get " + item, "y"]
    return commands


def play(commands, game=GAME):
    return subprocess.run(
        [sys.executable, str(game)], input="\n".join(commands) + "\n",
        text=True, capture_output=True, timeout=10, check=True,
    ).stdout


class EndingNarrationTests(unittest.TestCase):
    def assert_variant(self, output, first, second, choose_first):
        self.assertIn(first if choose_first else second, output)
        self.assertNotIn(second if choose_first else first, output)

    def test_full_cart(self):
        for refused in (False, True):
            for hidden in (False, True):
                with self.subTest(refused=refused, took_nothing=hidden):
                    output = play(commands_for("full", refused, hidden))
                    self.assertIn("Our most favored, respectable customer.", output)
                    self.assert_variant(output, "It amused us that you had to think twice",
                                        "And not for a second did you doubt", refused)
                    self.assert_variant(output, "you even took something from where there was nothing",
                                        "Though you could stand to try a little harder", hidden)
                    self.assertIn("See you tomorrow, beloved customer.", output)

    def test_partial_cart(self):
        for refused in (False, True):
            for hidden in (False, True):
                with self.subTest(refused=refused, took_nothing=hidden):
                    output = play(commands_for("partial", refused, hidden))
                    self.assertIn("Your cart isn't quite full.", output)
                    self.assert_variant(output, "But it was clearly in haste",
                                        "You're all frazzled up!", not refused)
                    self.assert_variant(output, "We know you're meant to be here.",
                                        "Though we may be in error", hidden)
                    self.assertIn("Wouldn't it be a dream to live here and eat forever?", output)

    def test_empty_cart_after_exploration(self):
        for hidden in (False, True):
            with self.subTest(took_nothing=hidden):
                output = play(commands_for("empty", took_nothing=hidden))
                self.assert_variant(output, "coveting nothing is still coveting",
                                    "You catch stray words of him amazed", hidden)
                self.assertIn("the reward of temperance.", output)

    def test_early_exit(self):
        output = play(commands_for("early"))
        self.assertIn("A quick exit means the customer left untested", output)
        self.assertNotIn("the reward of temperance.", output)
        self.assertNotIn("Our most favored, respectable customer.", output)


if __name__ == "__main__":
    unittest.main()
