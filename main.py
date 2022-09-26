import twitter


def main():
    rules = twitter.get_rules()
    delete = twitter.delete_all_rules(rules)
    set = twitter.set_rules(delete)
    twitter.get_stream(set)


if __name__ == "__main__":
    main()
