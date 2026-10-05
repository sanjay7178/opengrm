"""Entry point for the Bazel runfiles archive used to assemble the wheel."""

from opengrm.pynini import pynini


if __name__ == "__main__":
  print(pynini.accep("wheel").string())
