# Python-Capstone-Project
1.	Multi-Source Financial Sentiment & Price Oracle<br>
A dashboard that correlates Hype (social media) with Reality (market prices).<br>
The Workflow:<br>
•	APIs: Pull real-time price data for Stocks or Crypto using Alpha Vantage or CoinGecko API.<br>
•	Web Scraping: Scrape financial news sites ,Reuters/CNBC, or Reddit threads.<br>
•	Regex: Parse ticker symbols e.g. $AAPL, $BTC and identify bullish or bearish keywords within the scraped text.<br>
•	Databases: Use SQL for the time-series price data. Use NoSQL,MongoDB for the high-volume, varying schemas of social media posts/comments.<br>
•	Best Practices: Modularize your code into data_ingestion, processing, and storage modules. Use pytest to verify your API connection logic.<br>
<br>
2.	Global Job Market Skill-Mapper<br>
A career-planning tool that identifies which technical skills are currently in demand and what they pay.<br>
•	Web Scraping: Scrape job boards  to get raw job descriptions.<br>
•	APIs: Use the Adzuna or Indeed to get structured job data and salary estimates.<br>
•	Regex: This is key here—use Regex to extract specific technical keywords e.g., Python, AWS, Tableau from the raw text descriptions.<br>
•	OOP: Implement Encapsulation by creating a JobEntry class where the salary data is protected and can only be accessed/modified through specific methods.<br>
•	Databases: Store the raw scraped job postings in MongoDB and the Skills vs. Salary relationship table in SQL.<br>
•	Best Practices: Write a suite of Unit Tests to ensure your Regex doesn't miss variations of keywords .

