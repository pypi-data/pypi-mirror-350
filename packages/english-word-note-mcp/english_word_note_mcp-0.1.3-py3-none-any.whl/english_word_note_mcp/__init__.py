from .server import server


def main() -> None:
    server.run(transport="stdio")
    # server.run(transport="sse")


if __name__ == "__main__":
    main()
