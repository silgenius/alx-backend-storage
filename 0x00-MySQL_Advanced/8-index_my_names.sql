ALTER TABLE names 
ADD COLUMN first_letter CHAR(1) AS (LEFT(name, 1)) VIRTUAL;

CREATE INDEX idx_name_first ON names (first_letter);

