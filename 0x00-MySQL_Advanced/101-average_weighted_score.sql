-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- computes and store the average weighted score for all students.

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id_param INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    OPEN cur;

    user_loop: LOOP
        FETCH cur INTO user_id_param;
        
        IF done THEN
            LEAVE user_loop;
        END IF;

        CALL ComputeAverageWeightedScoreForUser(user_id_param);
    END LOOP;

    CLOSE cur;

END //

DELIMITER ;
