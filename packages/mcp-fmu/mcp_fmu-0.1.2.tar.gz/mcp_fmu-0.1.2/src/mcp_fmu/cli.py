import argparse

from mcp_fmu.server import mcp


def main():
    parser = argparse.ArgumentParser(description="mcp-fmu server CLI")
    parser.parse_args()

    mcp.run()


if __name__ == "__main__":
    main()
