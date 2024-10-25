from utils.pars_wb_api import parse_wb_card


def generator_for_posts(articles: list, count_item: int = 9):
    post = []
    for art in articles:
        item = parse_wb_card(art)
        if item:
            post.append(item)
        if len(post) == count_item:
            yield post
            post = []
    if post:
        yield post
