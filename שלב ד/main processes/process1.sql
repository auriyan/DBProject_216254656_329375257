-- תוכנית ראשית 1: ניהול לקוחות VIP וארכוב נתונים
DO $$
DECLARE
    v_customer RECORD;
    v_customer_stats RECORD;
    v_vip_count INT := 0;
    v_total_vip_revenue NUMERIC := 0;
    v_archived_count INT;
    v_archived_revenue NUMERIC;
    v_min_vip_spending NUMERIC := 1000;
BEGIN
    RAISE NOTICE '====================================';
    RAISE NOTICE 'VIP Customer Analysis & System Cleanup';
    RAISE NOTICE 'Date: %', CURRENT_DATE;
    RAISE NOTICE '====================================';
    RAISE NOTICE '';
    
    -- חלק 1: ניתוח לקוחות VIP
    RAISE NOTICE '--- PART 1: VIP CUSTOMER ANALYSIS ---';
    
    FOR v_customer IN 
        SELECT cid, full_name, phone 
        FROM customer 
        ORDER BY cid
    LOOP
        -- קריאה לפונקציה לחישוב הוצאות הלקוח
        SELECT * INTO v_customer_stats
        FROM calculate_customer_total_spending(v_customer.cid);
        
        -- אם הלקוח VIP, הצג פרטים
        IF v_customer_stats.is_vip THEN
            v_vip_count := v_vip_count + 1;
            v_total_vip_revenue := v_total_vip_revenue + v_customer_stats.total_spent;
            
            RAISE NOTICE 'VIP Customer #%: %', v_vip_count, v_customer_stats.customer_name;
            RAISE NOTICE '  Total Spent: ₪%', v_customer_stats.total_spent;
            RAISE NOTICE '  Rentals: ₪%, Lessons: ₪%', 
                        v_customer_stats.rental_costs, v_customer_stats.lesson_costs;
            RAISE NOTICE '  Last Activity: %', v_customer_stats.last_activity;
            
            -- בדיקה אם צריך ליצור קשר (לא פעיל יותר מ-60 יום)
            IF v_customer_stats.last_activity < CURRENT_DATE - INTERVAL '60 days' THEN
                RAISE NOTICE '  ⚠  ATTENTION: Customer inactive for % days!', 
                            CURRENT_DATE - v_customer_stats.last_activity;
            END IF;
            RAISE NOTICE '';
        END IF;
    END LOOP;
    
    -- סיכום VIP
    RAISE NOTICE '--- VIP SUMMARY ---';
    RAISE NOTICE 'Total VIP Customers: %', v_vip_count;
    RAISE NOTICE 'Total VIP Revenue: ₪%', v_total_vip_revenue;
    IF v_vip_count > 0 THEN
        RAISE NOTICE 'Average VIP Spending: ₪%', ROUND(v_total_vip_revenue / v_vip_count, 2);
    END IF;
    RAISE NOTICE '';
    
    -- חלק 2: ארכוב וניקוי
    RAISE NOTICE '--- PART 2: SYSTEM CLEANUP ---';
    RAISE NOTICE 'Starting archive process for rentals older than 1 year...';
    
    -- קריאה לפרוצדורת הארכוב
    CALL archive_old_rentals(v_archived_count, v_archived_revenue, 365);
    
    -- סיכום כללי
    RAISE NOTICE '';
    RAISE NOTICE '====================================';
    RAISE NOTICE 'PROCESS COMPLETED SUCCESSFULLY';
    RAISE NOTICE 'VIP Customers: %, Archive Records: %', v_vip_count, v_archived_count;
    RAISE NOTICE 'Total Revenue Analyzed: ₪%', v_total_vip_revenue + v_archived_revenue;
    RAISE NOTICE '====================================';
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error in main program: %', SQLERRM;
        RAISE;
END $$;
