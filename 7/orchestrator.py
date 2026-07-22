from market_research import market_research
from creative_director import creative_director
from copywriter import copywriter
from social_media import social_media
from reviewer import reviewer
from image_prompt import image_prompt

def orchestrator(product):
    print("\n" + "="*60)
    print(" STEP 1: Market Research")
    print("="*60)
    market = market_research(product)
    print(market)

    print("\n" + "="*60)
    print(" STEP 2: Creative Director Strategy")
    print("="*60)
    strategy = creative_director(product, market)
    print(strategy)

    print("\n" + "="*60)
    print("  STEP 3: Copywriting")
    print("="*60)
    copy = copywriter(strategy)
    print(copy)

    print("\n" + "="*60)
    print(" STEP 4: Social Media Posts")
    print("="*60)
    posts = social_media(copy)
    print(posts)

    print("\n" + "="*60)
    print("  STEP 5: Image Prompt")
    print("="*60)
    img = image_prompt(strategy)
    print(img)

    print("\n" + "="*60)
    print(" STEP 6: Review")
    print("="*60)
    review = reviewer(copy)
    print(review)

    return {
        "market_research": market,
        "creative_strategy": strategy,
        "copy": copy,
        "social_media": posts,
        "image_prompt": img,
        "review": review,
    }
