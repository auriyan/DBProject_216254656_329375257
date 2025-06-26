CREATE OR REPLACE PROCEDURE smart_price_update(
    p_analysis_days INT DEFAULT 30,
    p_increase_threshold NUMERIC DEFAULT 70,
    p_decrease_threshold NUMERIC DEFAULT 30
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_equipment_stats RECORD;
    v_new_price NUMERIC;
    v_price_changes INT := 0;
    v_utilization_percent NUMERIC;
BEGIN
    RAISE NOTICE 'Starting smart price update analysis for last % days', p_analysis_days;
    
    -- ניתוח כל פריט ציוד
    FOR v_equipment_stats IN
        SELECT 
            e.eid,
            e.type,
            e.daily_price,
            COUNT(DISTINCT r.rid) as rental_count,
            COALESCE(SUM(
                CASE 
                    WHEN r.end_date IS NOT NULL 
                    THEN r.end_date - r.start_date + 1
                    ELSE 0
                END
            ), 0) as total_days_rented
        FROM equipment e
        LEFT JOIN rental_equipment re ON e.eid = re.eid
        LEFT JOIN rental r ON re.rid = r.rid 
            AND r.start_date >= CURRENT_DATE - (p_analysis_days || ' days')::INTERVAL
        GROUP BY e.eid, e.type, e.daily_price
    LOOP
        -- חישוב אחוז ניצול
        v_utilization_percent := (v_equipment_stats.total_days_rented::NUMERIC / p_analysis_days) * 100;
        
        -- קביעת מחיר חדש
        IF v_utilization_percent > p_increase_threshold THEN
            -- ציוד פופולרי - העלאת מחיר ב-10%
            v_new_price := ROUND(v_equipment_stats.daily_price * 1.10, 2);
            
            IF v_new_price != v_equipment_stats.daily_price THEN
                UPDATE equipment 
                SET daily_price = v_new_price
                WHERE eid = v_equipment_stats.eid;
                
                v_price_changes := v_price_changes + 1;
                RAISE NOTICE 'Increased price for % (ID: %) from % to % (utilization: %)',
                    v_equipment_stats.type, v_equipment_stats.eid, 
                    v_equipment_stats.daily_price, v_new_price, 
                    ROUND(v_utilization_percent, 2);
            END IF;
            
        ELSIF v_utilization_percent < p_decrease_threshold AND v_utilization_percent > 0 THEN
            -- ציוד לא פופולרי - הורדת מחיר ב-15%
            v_new_price := ROUND(v_equipment_stats.daily_price * 0.85, 2);
            
            -- וידוא שהמחיר לא יורד מתחת ל-20
            IF v_new_price < 20 THEN
                v_new_price := 20;
            END IF;
            
            IF v_new_price != v_equipment_stats.daily_price THEN
                UPDATE equipment 
                SET daily_price = v_new_price
                WHERE eid = v_equipment_stats.eid;
                
                v_price_changes := v_price_changes + 1;
                RAISE NOTICE 'Decreased price for % (ID: %) from % to % (utilization: %)',
                    v_equipment_stats.type, v_equipment_stats.eid, 
                    v_equipment_stats.daily_price, v_new_price, 
                    ROUND(v_utilization_percent, 2);
            END IF;
        END IF;
    END LOOP;
    
    RAISE NOTICE 'Price update complete. Total changes: %', v_price_changes;
    
    IF v_price_changes > 0 THEN
        COMMIT;
        RAISE NOTICE 'All price changes have been committed to the database';
    ELSE
        RAISE NOTICE 'No price changes were necessary';
    END IF;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error in smart_price_update: %', SQLERRM;
        ROLLBACK;
        RAISE;
END;
$$;
