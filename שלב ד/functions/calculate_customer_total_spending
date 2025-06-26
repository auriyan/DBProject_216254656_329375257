CREATE OR REPLACE FUNCTION calculate_customer_total_spending(p_customer_id INT)
RETURNS TABLE(
    customer_name VARCHAR,
    rental_costs NUMERIC,
    lesson_costs NUMERIC,
    total_spent NUMERIC,
    last_activity DATE,
    is_vip BOOLEAN
) AS $$
DECLARE
    v_rental_cursor CURSOR FOR
        SELECT r.rid, r.start_date, r.end_date
        FROM rental r
        WHERE r.cid = p_customer_id;
    v_rental_rec RECORD;
    v_equipment_cost NUMERIC;
    v_days INT;
BEGIN
    -- קבלת שם הלקוח
    SELECT full_name INTO customer_name
    FROM customer
    WHERE cid = p_customer_id;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Customer % not found', p_customer_id;
    END IF;
    
    -- חישוב עלויות השכרות
    rental_costs := 0;
    FOR v_rental_rec IN v_rental_cursor LOOP
        -- חישוב ימי השכרה
        v_days := COALESCE(v_rental_rec.end_date - v_rental_rec.start_date + 1, 1);
        
        -- חישוב עלות הציוד להשכרה זו
        SELECT COALESCE(SUM(e.daily_price * v_days), 0) INTO v_equipment_cost
        FROM rental_equipment re
        JOIN equipment e ON re.eid = e.eid
        WHERE re.rid = v_rental_rec.rid;
        
        rental_costs := rental_costs + v_equipment_cost;
    END LOOP;
    
    -- חישוב עלויות שיעורים
    SELECT COALESCE(SUM(p.amount), 0) INTO lesson_costs
    FROM payment p
    WHERE p.cid = p_customer_id;
    
    -- סך הכל הוצאות
    total_spent := rental_costs + lesson_costs;
    
    -- תאריך פעילות אחרון
    SELECT MAX(activity_date) INTO last_activity
    FROM (
        SELECT MAX(r.start_date) as activity_date FROM rental r WHERE r.cid = p_customer_id
        UNION
        SELECT MAX(p.pdate) FROM payment p WHERE p.cid = p_customer_id
    ) activities;
    
    -- האם לקוח VIP (מעל 1000 ש"ח)
    is_vip := (total_spent > 1000);
    
    RETURN NEXT;
END;
$$ LANGUAGE plpgsql
    
