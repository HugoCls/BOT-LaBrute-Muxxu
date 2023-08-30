WITH matches AS (
SELECT
	id
    ,max(date_time) AS last_attack
	,count(*) AS matches 
	,SUM(win) AS victories 
    ,count(*) - sum(win) AS defeats 
    ,sum(win)/count(*) AS winrate
FROM `attacks_logs` 
GROUP BY id 
)

SELECT 
	*
FROM matches
LEFT JOIN brutes 
	USING(id)
ORDER BY winrate DESC, matches DESC;