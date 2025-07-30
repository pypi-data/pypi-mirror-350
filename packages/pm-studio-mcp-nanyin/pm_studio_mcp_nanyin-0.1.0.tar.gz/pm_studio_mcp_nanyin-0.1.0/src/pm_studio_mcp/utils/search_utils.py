try:
    from googlesearch import search
except ImportError:
    print("Please install googlesearch-python: pip install googlesearch-python")

try:
    import praw
    import csv
    import os
    import datetime
    import requests
    from typing import List, Dict, Any, Optional
except ImportError:
    print("Please install required packages: pip install praw requests")

class SearchUtils:
    def search_google(query: str, num_results: int = 10):
        """
        Perform a Google web search with the given query and return top 10 result URLs.
        
        Args:
            query: Search query
            num_results: Number of search results to return (default: 10)
            
        Returns:
            List of 10 search result URLs
        """
        try:
            # Perform the search and get results
            search_results = []
            for url in search(query, num_results=num_results):
                search_results.append(url)
                
            return {
                "status": "success",
                "query": query,
                "results": search_results
            }
        except Exception as e:
            return f"Error performing search: {str(e)}"
            
    @staticmethod
    def scrape_reddit(
        subreddit_name: str,
        keywords: List[str],
        client_id: str,
        client_secret: str,
        post_limit: int = 100,
        time_filter: str = "month",
        working_dir: str = ""
    ) -> Dict[str, Any]:
        """
        Scrape posts from a subreddit and filter by keywords.
        
        Args:
            subreddit_name: Name of the subreddit to scrape
            keywords: List of keywords to filter posts by
            client_id: Reddit API client ID
            client_secret: Reddit API client secret
            post_limit: Maximum number of posts to retrieve (default: 100)
            time_filter: Time filter for posts (default: "month")
            working_dir: Directory to save output file (default: current dir)
            
        Returns:
            Dictionary with status and results
        """
        try:
            # Create a user agent string
            user_agent = f"python:reddit-post-scraper:v1.0 (by u/{subreddit_name})"
            
            # Initialize Reddit API connection
            reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )
            
            subreddit = reddit.subreddit(subreddit_name)
            
            # Get posts from subreddit based on time filter
            if time_filter == "all":
                posts = subreddit.top(limit=post_limit)
            elif time_filter == "year":
                posts = subreddit.top("year", limit=post_limit)
            elif time_filter == "month":
                posts = subreddit.top("month", limit=post_limit)
            elif time_filter == "week":
                posts = subreddit.top("week", limit=post_limit)
            elif time_filter == "day":
                posts = subreddit.top("day", limit=post_limit)
            else:
                posts = subreddit.new(limit=post_limit)
                
            filtered_posts = []
            
            # Process each post
            for post in posts:
                # Check if any keyword is in title or selftext (case-insensitive)
                post_text = (post.title + " " + (post.selftext if post.selftext else "")).lower()
                
                # Check if any keyword matches
                if any(keyword.lower() in post_text for keyword in keywords):
                    post_data = {
                        "title": post.title,
                        "url": f"https://www.reddit.com{post.permalink}",
                        "author": str(post.author),
                        "score": post.score,
                        "num_comments": post.num_comments,
                        "created_utc": datetime.datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d'),
                        "selftext": post.selftext[:500] + "..." if len(post.selftext) > 500 else post.selftext
                    }
                    filtered_posts.append(post_data)
            
            # Save the results to CSV
            output_file = f"reddit_{subreddit_name}_posts.csv"
            if working_dir:
                output_file = os.path.join(working_dir, output_file)
                
            if filtered_posts:
                with open(output_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=filtered_posts[0].keys())
                    writer.writeheader()
                    writer.writerows(filtered_posts)
                
                return {
                    "status": "success",
                    "posts_found": len(filtered_posts),
                    "output_file": os.path.abspath(output_file)
                }
            else:
                return {
                    "status": "success",
                    "posts_found": 0,
                    "message": "No posts found matching the criteria."
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error scraping Reddit: {str(e)}"
            }
    
    @staticmethod
    def scrape_app_reviews(
        api_key: str,
        product_id: str,
        market: str = "google-play",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        countries: Optional[List[str]] = None,
        rating: Optional[List[int]] = None,
        version: str = "all",
        working_dir: str = ""
    ) -> Dict[str, Any]:
        """
        Fetch app reviews from data.ai API and save them to a CSV file.
        
        Args:
            api_key: data.ai API key
            product_id: App ID of the product
            market: Market - one of 'ios', 'mac', or 'google-play'
            start_date: Start date in format YYYY-MM-DD (default: 30 days ago)
            end_date: End date in format YYYY-MM-DD (default: today)
            countries: List of country codes (iOS only)
            rating: List of ratings to filter by (1-5)
            version: App version or 'all'
            working_dir: Directory to save output file (default: current dir)
            
        Returns:
            Dictionary with status and results
        """
        try:
            # Set default dates if not provided (last 30 days)
            if not end_date:
                end_date = datetime.datetime.now().strftime('%Y-%m-%d')
            
            if not start_date:
                start_date_obj = datetime.datetime.now() - datetime.timedelta(days=30)
                start_date = start_date_obj.strftime('%Y-%m-%d')
            
            # Validate market
            if market not in ["ios", "mac", "google-play"]:
                return {
                    "status": "error",
                    "message": "Market must be one of 'ios', 'mac', or 'google-play'"
                }
            
            # Build URL
            base_url = f"https://api.data.ai/v1.3/apps/{market}/app/{product_id}/reviews"
            params = {
                "start_date": start_date,
                "end_date": end_date,
                "page_size": 100,
                "page_index": 0,
                "version": version
            }
            
            # Add optional parameters
            if countries and market == "ios":
                params["countries"] = "+".join(countries)
            
            if rating:
                params["rating"] = "+".join(str(r) for r in rating)
            
            # Headers
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json"
            }
            
            all_reviews = []
            has_next_page = True
            
            while has_next_page:
                # Make API request
                response = requests.get(base_url, params=params, headers=headers)
                
                # Check if request was successful
                if response.status_code != 200:
                    return {
                        "status": "error",
                        "message": f"API returned status code {response.status_code}: {response.text}"
                    }
                
                # Parse the response
                data = response.json()
                
                # Extract reviews
                reviews = data.get("reviews", [])
                all_reviews.extend(reviews)
                
                # Check if there's a next page
                if data.get("next_page"):
                    params["page_index"] = params["page_index"] + 1
                else:
                    has_next_page = False
            
            # Create output filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"app_reviews_{market}_{timestamp}.csv"
            
            if working_dir:
                output_file = os.path.join(working_dir, output_file)
            
            # Determine fields based on market
            if market == "google-play":
                fieldnames = [
                    "review_id", "date", "rating", "text", "version", 
                    "device", "language", "language_name", "country"
                ]
            else:  # ios or mac
                fieldnames = [
                    "review_id", "date", "rating", "title", "text", 
                    "version", "device", "country"
                ]
            
            # Write to CSV (only if reviews were found)
            if all_reviews:
                with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
                    writer.writeheader()
                    
                    for review in all_reviews:
                        writer.writerow(review)
                
                return {
                    "status": "success",
                    "reviews_found": len(all_reviews),
                    "output_file": os.path.abspath(output_file),
                    "market": market,
                    "start_date": start_date,
                    "end_date": end_date
                }
            else:
                return {
                    "status": "success",
                    "reviews_found": 0,
                    "message": "No reviews found matching the criteria"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error scraping app reviews: {str(e)}"
            }