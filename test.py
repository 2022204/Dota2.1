from sql_queries import execute_postgresql_query

execute_postgresql_query("INSERT INTO maps (map_type, map_area) VALUES (%s,%s)", "ELSE", params = ('water',1300))
