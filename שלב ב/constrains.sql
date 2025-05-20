-- CHECK: מחיר יומי חייב להיות חיובי (ציוד)
ALTER TABLE equipment
ADD CONSTRAINT chk_equipment_daily_price_positive CHECK (daily_price > 0);

-- NOT NULL: שם משפחה של עובד לא יכול להיות ריק (עובד)
ALTER TABLE employee
ALTER COLUMN lname SET NOT NULL;

-- DEFAULT: משמרת ברירת מחדל ל'בוקר' (קופאי)
ALTER TABLE cashier
ALTER COLUMN shift SET DEFAULT 'בוקר';
