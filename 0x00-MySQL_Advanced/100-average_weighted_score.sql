-- Update the user's average_score in the users table
-- Calculate average weighted score (avoid division by zero)

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id_param INT)
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight INT;
    DECLARE avg_weighted_score FLOAT;

    SELECT SUM(corrections.score * projects.weight), SUM(projects.weight)
    INTO total_weighted_score, total_weight
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id_param;

    IF total_weight > 0 THEN
        SET avg_weighted_score = total_weighted_score / total_weight;
    ELSE
        SET avg_weighted_score = 0;
    END IF;

    UPDATE users
    SET average_score = avg_weighted_score
    WHERE id = user_id_param;

END //
