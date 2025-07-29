#!/usr/bin/env python3

"""Test script for trending searches functionality."""

from src.gtrends_core.config import get_trends_client
from src.gtrends_core.services.trending_service import TrendingService


def main():
    """Test trending searches with articles."""
    print("Getting trending searches with news articles...")

    # Get the client and service
    client = get_trends_client()
    service = TrendingService(client)

    # Get trending searches with news articles
    results = service.get_trending_searches_with_articles()

    # Display the results
    print(
        f"\nFound {len(results.topics)} trending topics for region {results.region_name} ({results.region_code})"
    )

    for i, topic in enumerate(results.topics):
        print(f"{i+1}. {topic.keyword} - {topic.traffic}")

        if results.news_articles and topic.keyword in results.news_articles:
            articles = results.news_articles[topic.keyword]
            print(f"   News articles ({len(articles)}):")

            for j, article in enumerate(articles[:3]):  # Show up to 3 articles
                print(f"   {j+1}. {article.title}")
                print(f"      Source: {article.source}")
                print(f"      URL: {article.url}")
                if article.time_ago:
                    print(f"      Time: {article.time_ago}")
                print()

        if i >= 9:  # Show only 10 topics
            break

    # Check if news articles were found
    if results.has_news:
        print(
            f"\nTotal news articles: {sum(len(articles) for articles in results.news_articles.values())}"
        )
    else:
        print("\nNo news articles found")


if __name__ == "__main__":
    main()
