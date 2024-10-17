DELIMITER //

CREATE TRIGGER update_on_changed_email
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.email <> NEW.email THEN
        UPDATE users
        SET valid_email = 1
        WHERE id = NEW.id;  -- Ensure you're using the correct identifier
    END IF;
END;

//

DELIMITER ;

