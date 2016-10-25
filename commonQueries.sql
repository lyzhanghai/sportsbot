
/*Cumulative watched for a year*/
SELECT SUM(gtime)
FROM games a
	JOIN leagues b ON a.league = b.leagues
	JOIN gametime c on b.sports = c.sport
WHERE YEAR(matchdate)=2016
