-- תוכנית ראשית 2: ניהול מלאי ומחירים דינמי
DO $$
DECLARE
    v_tomorrow DATE := CURRENT_DATE + 1;
    v_next_week DATE := CURRENT_DATE + 7;
    v_equipment RECORD;
    v_available_count INT;
    v_total_equipment INT;
    v_availability_percent NUMERIC;
    v_equipment_cursor refcursor;
    v_low_availability_items TEXT := '';
BEGIN
    RAISE NOTICE '====================================';
    RAISE NOTICE 'Dynamic Inventory Management System';
    RAISE NOTICE 'Analysis Date: %', CURRENT_DATE;
    RAISE NOTICE '====================================';
    RAISE NOTICE '';
    
    -- חלק 1: בדיקת זמינות ציוד
    RAISE NOTICE '--- PART 1: EQUIPMENT AVAILABILITY CHECK ---';
    
    -- ספירת כל הציוד
    SELECT COUNT(*) INTO v_total_equipment FROM equipment;
    
    -- בדיקת זמינות למחר
    RAISE NOTICE 'Checking availability for tomorrow (%)', v_tomorrow;
    v_available_count := 0;
    
    -- קריאה לפונקציה למציאת ציוד זמין
    FOR v_equipment IN 
        SELECT * FROM find_available_equipment(v_tomorrow)
    LOOP
        v_available_count := v_available_count + 1;
    END LOOP;
    
    v_availability_percent := ROUND((v_available_count::NUMERIC / v_total_equipment) * 100, 2);
    RAISE NOTICE 'Available: % out of % items (% percent)', 
                v_available_count, v_total_equipment, v_availability_percent;
    
    -- בדיקה לשבוע הבא
    RAISE NOTICE '';
    RAISE NOTICE 'Checking availability for next week (%)', v_next_week;
    v_available_count := 0;
    
    FOR v_equipment IN 
        SELECT * FROM find_available_equipment(v_next_week)
    LOOP
        v_available_count := v_available_count + 1;
        
        -- אם מחיר נמוך מ-50, הוסף להמלצות
        IF v_equipment.daily_price < 50 THEN
            v_low_availability_items := v_low_availability_items || 
                format('  - %s (ID: %s) - Only %s NIS/day', 
                       v_equipment.type, v_equipment.eid, v_equipment.daily_price) || E'\n';
        END IF;
    END LOOP;
    
    v_availability_percent := ROUND((v_available_count::NUMERIC / v_total_equipment) * 100, 2);
    RAISE NOTICE 'Available: % out of % items (% percent)', 
                v_available_count, v_total_equipment, v_availability_percent;
    
    -- המלצות מיוחדות
    IF v_low_availability_items != '' THEN
        RAISE NOTICE '';
        RAISE NOTICE 'SPECIAL DEALS AVAILABLE:';
        RAISE NOTICE '%', v_low_availability_items;
    END IF;
    
    -- אזהרה אם זמינות נמוכה
    IF v_availability_percent < 30 THEN
        RAISE NOTICE '';
        RAISE NOTICE 'WARNING: Low availability for next week!';
        RAISE NOTICE '   Consider encouraging early bookings.';
    END IF;
    
    -- חלק 2: עדכון מחירים דינמי
    RAISE NOTICE '';
    RAISE NOTICE '--- PART 2: DYNAMIC PRICE OPTIMIZATION ---';
    RAISE NOTICE 'Analyzing rental patterns from last 30 days...';
    
    -- קריאה לפרוצדורת עדכון מחירים
    CALL smart_price_update(30, 70, 30);
    
    -- סיכום
    RAISE NOTICE '';
    RAISE NOTICE '====================================';
    RAISE NOTICE 'INVENTORY MANAGEMENT COMPLETE';
    RAISE NOTICE 'Next Steps:';
    RAISE NOTICE '- Review price changes in equipment table';
    RAISE NOTICE '- Check special deals for marketing';
    RAISE NOTICE '- Monitor availability trends';
    RAISE NOTICE '====================================';
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error in inventory management: %', SQLERRM;
        RAISE;
END $$;
