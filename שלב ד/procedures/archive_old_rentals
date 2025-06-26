CREATE OR REPLACE PROCEDURE archive_old_rentals(
    OUT p_archived_count INT,
    OUT p_total_revenue NUMERIC,
	p_days_old INT DEFAULT 365
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_rental_cursor CURSOR FOR
        SELECT r.rid, r.cid, r.start_date, r.end_date
        FROM rental r
        WHERE r.end_date < CURRENT_DATE - (p_days_old || ' days')::INTERVAL
        FOR UPDATE;
    
    v_rental RECORD;
    v_rental_revenue NUMERIC;
    v_equipment_days INT;
BEGIN
    p_archived_count := 0;
    p_total_revenue := 0;
    
    -- יצירת טבלת ארכיון אם לא קיימת
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables 
                   WHERE table_name = 'archived_rentals') THEN
        CREATE TABLE archived_rentals AS 
        SELECT *, CURRENT_DATE as archive_date 
        FROM rental WHERE 1=0;
    END IF;
    
    -- עיבוד השכרות ישנות
    FOR v_rental IN v_rental_cursor LOOP
        -- חישוב הכנסה מההשכרה
        v_equipment_days := v_rental.end_date - v_rental.start_date + 1;
        
        SELECT COALESCE(SUM(e.daily_price * v_equipment_days), 0) 
        INTO v_rental_revenue
        FROM rental_equipment re
        JOIN equipment e ON re.eid = e.eid
        WHERE re.rid = v_rental.rid;
        
        p_total_revenue := p_total_revenue + v_rental_revenue;
        
        -- העברה לארכיון
        INSERT INTO archived_rentals 
        SELECT r.*, CURRENT_DATE 
        FROM rental r 
        WHERE r.rid = v_rental.rid;
        
        -- מחיקה מטבלה ראשית
        DELETE FROM rental_equipment WHERE rid = v_rental.rid;
        DELETE FROM rental WHERE rid = v_rental.rid;
        
        p_archived_count := p_archived_count + 1;
        
        -- הודעה כל 100 רשומות
        IF p_archived_count % 100 = 0 THEN
            RAISE NOTICE 'Archived % rentals so far...', p_archived_count;
        END IF;
    END LOOP;
    
    -- עדכון סטטיסטיקות
    ANALYZE rental;
    ANALYZE rental_equipment;
    
    RAISE NOTICE 'Archive complete: % rentals archived, total revenue: %', 
                 p_archived_count, p_total_revenue;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error during archiving: %', SQLERRM;
        ROLLBACK;
        RAISE;
END;
$$;
