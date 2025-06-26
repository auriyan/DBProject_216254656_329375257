-- AlterTable.sql
-- שינויים בבסיס הנתונים עבור שלב 4

-- 1. יצירת טבלת ארכיון להשכרות ישנות
CREATE TABLE IF NOT EXISTS archived_rentals (
    rid            INT            PRIMARY KEY,
    cid            INT,
    eid            INT,
    start_date     DATE,
    end_date       DATE,
    archive_date   DATE           NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT fk_arch_cust
        FOREIGN KEY (cid) REFERENCES customer(cid),
    CONSTRAINT fk_arch_cash
        FOREIGN KEY (eid) REFERENCES cashier(eid)
);

-- 2. הוספת אינדקס לשיפור ביצועים על טבלת archived_rentals
CREATE INDEX idx_archived_rentals_dates ON archived_rentals(start_date, end_date);

-- 3. הוספת עמודה לטבלת customer לסימון VIP (אופציונלי)
ALTER TABLE customer 
ADD COLUMN IF NOT EXISTS is_vip BOOLEAN DEFAULT FALSE;

-- 4. הוספת עמודה לטבלת equipment למעקב אחר פופולריות
ALTER TABLE equipment
ADD COLUMN IF NOT EXISTS times_rented INT DEFAULT 0;
