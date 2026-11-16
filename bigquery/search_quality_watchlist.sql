-- Home Depot Retail Search Intelligence
-- Historical Kaggle search relevance data
-- Search Quality Watchlist: at least 10 labeled pairs per search term

SELECT
  search_term,
  product_matches,
  avg_relevance,
  low_relevance_pct,
  missing_descriptions
FROM `hd-retail-intelligence-2026.retail_intelligence.gold_search_quality`
WHERE product_matches >= 10
ORDER BY
  avg_relevance ASC,
  low_relevance_pct DESC
LIMIT 20;
