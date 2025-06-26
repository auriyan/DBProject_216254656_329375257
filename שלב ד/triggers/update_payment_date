-- פונקציית הטריגר
CREATE OR REPLACE FUNCTION update_payment_date()
RETURNS TRIGGER AS $$
BEGIN
    -- עדכון תאריך תשלום לתאריך הנוכחי אם לא הוזן
    IF NEW.pdate IS NULL THEN
        NEW.pdate := CURRENT_DATE;
        RAISE NOTICE 'Payment date automatically set to %', NEW.pdate;
    END IF;
    
    -- וידוא שסכום התשלום חיובי
    IF NEW.amount <= 0 THEN
        RAISE EXCEPTION 'Payment amount must be positive. Got: %', NEW.amount;
    END IF;
    
    -- בדיקה שהלקוח קיים
    IF NOT EXISTS (SELECT 1 FROM customer WHERE cid = NEW.cid) THEN
        RAISE EXCEPTION 'Customer % does not exist', NEW.cid;
    END IF;
    
    -- בדיקה שהקופאי קיים
    IF NOT EXISTS (SELECT 1 FROM cashier WHERE eid = NEW.eid) THEN
        RAISE EXCEPTION 'Cashier % does not exist', NEW.eid;
    END IF;
    
    -- אם זה תשלום לשיעור, בדוק שהשיעור קיים
    IF NEW.lid IS NOT NULL THEN
        IF NOT EXISTS (SELECT 1 FROM lesson WHERE lid = NEW.lid) THEN
            RAISE EXCEPTION 'Lesson % does not exist', NEW.lid;
        END IF;
        
        -- בדוק שהלקוח רשום לשיעור
        IF NOT EXISTS (SELECT 1 FROM lesson_participants 
                      WHERE lid = NEW.lid AND cid = NEW.cid) THEN
            RAISE WARNING 'Customer % is not registered for lesson %', NEW.cid, NEW.lid;
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- יצירת הטריגר
CREATE TRIGGER payment_date_update
BEFORE INSERT OR UPDATE ON payment
FOR EACH ROW
EXECUTE FUNCTION update_payment_date();
