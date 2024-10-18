-- a SQL script that creates a stored procedure ComputeAverageScoreForUser
--  that computes and store the average score for a student

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser (
	IN p_user_id INT
)
BEGIN
	DECLARE average FLOAT;

	SELECT AVG(score) INTO average FROM corrections WHERE user_id = p_user_id;
	UPDATE users
	SET average_score = average
	WHERE id = p_user_id;
END

//

DELIMITER ;
