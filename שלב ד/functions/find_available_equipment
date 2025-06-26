CREATE OR REPLACE FUNCTION find_available_equipment(
    p_date DATE,
    p_equipment_type VARCHAR DEFAULT NULL
)
RETURNS SETOF equipment AS $$
DECLARE
    v_equipment RECORD;
    v_is_available BOOLEAN;
BEGIN
    -- לולאה על כל הציוד
    FOR v_equipment IN 
        SELECT * FROM equipment e
        WHERE p_equipment_type IS NULL OR e.type = p_equipment_type
    LOOP
        v_is_available := TRUE;
        
        -- בדיקה אם הציוד מושכר בתאריך הנתון
        IF EXISTS (
            SELECT 1 
            FROM rental r
            JOIN rental_equipment re ON r.rid = re.rid
            WHERE re.eid = v_equipment.eid
              AND p_date BETWEEN r.start_date AND COALESCE(r.end_date, p_date)
        ) THEN
            v_is_available := FALSE;
        END IF;
        
        -- אם זמין, החזר אותו
        IF v_is_available THEN
            RETURN NEXT v_equipment;
        END IF;
    END LOOP;
    
    -- אם לא נמצא ציוד זמין
    IF NOT FOUND THEN
        RAISE NOTICE 'No available equipment found for date %', p_date;
    END IF;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error finding available equipment: %', SQLERRM;
        RAISE;
END;
$$ LANGUAGE plpgsql;
