-- a SQL script that creates a function SafeDiv that divides (and returns) the first
-- by the second number or returns 0 if the second number is equal to 0.

DELIMITER //


CREATE FUNCTION SafeDiv(numerator INT, denominator INT)
RETURNS FLOAT
BEGIN
	IF denominator <> 0 THEN
		RETURN numerator / denominator;
	ELSE
		RETURN 	0;
	END IF;
END;

//

DELIMITER ;
