CREATE VIEW `beam-dataflow-376917.dm_regional_manager.top_2_region_by_capacity`
AS 
SELECT region_id, SUM(capacity) as total_capacity
FROM `beam-dataflow-376917.raw_bikesharing.stations`
WHERE region_id != ''
GROUP BY region_id
ORDER BY total_capacity desc
LIMIT 2;