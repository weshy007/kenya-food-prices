try:
    from .cli import main
except ImportError:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from kenya_food_market.cli import main


if __name__ == "__main__":
    main()
