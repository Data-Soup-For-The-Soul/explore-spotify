from spotify.tasks import feed_spotify_charts


def run():
    feed_spotify_charts(use_async=False)


if __name__ == '__main__':
    run()
