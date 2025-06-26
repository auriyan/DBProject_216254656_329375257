-- פונקציית הטריגר
CREATE OR REPLACE FUNCTION check_rental_dates()
RETURNS TRIGGER AS $$
BEGIN
    -- בדיקה שתאריך סיום לא לפני תאריך התחלה
    IF NEW.end_date IS NOT NULL AND NEW.end_date < NEW.start_date THEN
        RAISE EXCEPTION 'End date (%) cannot be before start date (%)', 
                        NEW.end_date, NEW.start_date;
    END IF;
    
    -- בדיקה שתאריך התחלה לא בעתיד הרחוק (יותר משנה)
    IF NEW.start_date > CURRENT_DATE + INTERVAL '1 year' THEN
        RAISE EXCEPTION 'Cannot create rental more than 1 year in advance';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- יצירת הטריגר
CREATE TRIGGER rental_date_check
BEFORE INSERT OR UPDATE ON rental
FOR EACH ROW
EXECUTE FUNCTION check_rental_dates();
