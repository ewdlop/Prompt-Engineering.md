# generate sql statements

## 
```sql
DELIMITER //

CREATE PROCEDURE GenerateSQLStatements(IN tableName VARCHAR(255))
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE columnList TEXT;
    DECLARE columnValues TEXT;
    DECLARE sqlStatement TEXT;
    
    DECLARE cur CURSOR FOR
        SELECT GROUP_CONCAT(COLUMN_NAME)
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = tableName;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
    OPEN cur;
    FETCH cur INTO columnList;
    CLOSE cur;
    
    SET @query = CONCAT('SELECT CONCAT("INSERT INTO ', tableName, ' (', columnList, ') VALUES (", ',
                        'GROUP_CONCAT(CONCAT("'", ', columnList, ', "'")), ");") ',
                        'FROM ', tableName);
    
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //

DELIMITER ;
```
