---------------------------------- שאילתות ---------------------------------------------------
SELECT
c.full_name AS customer_name,
  c.phone,
  COUNT(r.rid) AS rentals_count,
  EXTRACT(YEAR FROM r.start_date) AS rental_year,
  EXTRACT(MONTH FROM r.start_date) AS rental_month
FROM
  customer c
  JOIN rental r ON c.cid = r.cid
WHERE
  EXTRACT(MONTH FROM r.start_date) = 11
  AND EXTRACT(YEAR FROM r.start_date) = 2024
GROUP BY
  c.full_name, c.phone,
  EXTRACT(YEAR FROM r.start_date),
  EXTRACT(MONTH FROM r.start_date)
ORDER BY
  rentals_count DESC;





SELECT
  l.lid,
  EXTRACT(YEAR FROM l.ldate) AS lesson_year,
  EXTRACT(MONTH FROM l.ldate) AS lesson_month,
  COUNT(lp.cid) AS participants_count
FROM
  lesson l
  JOIN lesson_participants lp ON l.lid = lp.lid
WHERE
  EXTRACT(YEAR FROM l.ldate)  = 2025
  AND EXTRACT(MONTH FROM l.ldate) = 1
GROUP BY
  l.lid, EXTRACT(YEAR FROM l.ldate), EXTRACT(MONTH FROM l.ldate)
ORDER BY
  participants_count DESC;





SELECT
  e.fname || ' ' || e.lname AS cashier_name,
  EXTRACT(YEAR FROM p.pdate) AS pay_year,
  EXTRACT(MONTH FROM p.pdate) AS pay_month,
  SUM(p.amount) AS total_revenue
FROM
  cashier c
  JOIN employee e ON c.eid = e.eid
  JOIN payment p  ON c.eid = p.eid
GROUP BY
  e.fname, e.lname,
  EXTRACT(YEAR FROM p.pdate),
  EXTRACT(MONTH FROM p.pdate)
HAVING
  SUM(p.amount) > 1000                      -- רק קופאים עם הכנסה גבוהה
ORDER BY
  total_revenue DESC;





SELECT
  eq.type AS equipment_type,
  ROUND(AVG(r.end_date - r.start_date), 2) AS avg_rental_days
FROM
  equipment eq
  JOIN rental_equipment re ON eq.eid = re.eid
  JOIN rental r            ON re.rid = r.rid
GROUP BY
  eq.type
ORDER BY
  avg_rental_days DESC;





SELECT
  eq.type                                AS equipment_type,
  SUM(r.end_date - r.start_date)         AS total_days_rented,
  ROUND(SUM(eq.daily_price * (r.end_date - r.start_date)), 2)  
                                          AS total_revenue
FROM
  rental r
  JOIN rental_equipment re ON r.rid = re.rid
  JOIN equipment eq       ON re.eid = eq.eid
WHERE
  EXTRACT(YEAR FROM r.start_date) = 2024
GROUP BY
  eq.type
ORDER BY
  total_revenue DESC;





SELECT
  eq.eid,
  eq.type,
  eq.daily_price
FROM
  equipment eq
WHERE
  NOT EXISTS (
    SELECT 1
    FROM rental_equipment re
    WHERE re.eid = eq.eid
  )
ORDER BY
  eq.daily_price DESC;





SELECT
  l.lid,
  l.ldate,
  ROUND(AVG(sub.count_part), 2) AS avg_participants
FROM
  lesson l
  JOIN (
    SELECT
      lid,
      COUNT(cid) AS count_part
    FROM
      lesson_participants
    GROUP BY
      lid
  ) sub ON l.lid = sub.lid
GROUP BY
  l.lid, l.ldate
ORDER BY
  avg_participants DESC
FETCH FIRST 5 ROWS ONLY;





SELECT
  EXTRACT(YEAR  FROM r.start_date) AS rental_year,
  EXTRACT(MONTH FROM r.start_date) AS rental_month,
  COUNT(r.rid)                      AS total_rentals,
  ROUND( SUM( eq.daily_price * (r.end_date - r.start_date) ), 2 ) 
                                    AS total_rental_revenue
FROM
  rental r
  JOIN rental_equipment re ON r.rid = re.rid
  JOIN equipment       eq ON re.eid = eq.eid
WHERE
  EXTRACT(YEAR FROM r.start_date) = 2024
GROUP BY
  EXTRACT(YEAR  FROM r.start_date),
  EXTRACT(MONTH FROM r.start_date)
ORDER BY
  rental_year,
  rental_month;


-------------------------------------- מחיקות ------------------------------------------------


DELETE FROM lesson
WHERE EXTRACT(MONTH FROM ldate) = 5;





DELETE FROM lesson l
WHERE NOT EXISTS (
  SELECT 1
  FROM lesson_participants lp
  WHERE lp.lid = l.lid
);





DELETE FROM customer c
WHERE NOT EXISTS (
    SELECT 1 FROM rental r                WHERE r.cid = c.cid
)
AND NOT EXISTS (
    SELECT 1 FROM payment p               WHERE p.cid = c.cid
)
AND NOT EXISTS (
    SELECT 1 FROM lesson_participants lp  WHERE lp.cid = c.cid
);



---------------------------------- עדכון ----------------------------------------------------


UPDATE equipment
SET daily_price = ROUND(daily_price * 1.10, 2)
WHERE eid IN (
  SELECT eid FROM (
    SELECT re.eid, COUNT(*) AS rentals
    FROM rental_equipment re
    GROUP BY re.eid
  ) sub
  WHERE rentals > (SELECT AVG(cnt) FROM (
                      SELECT COUNT(*) AS cnt
                      FROM rental_equipment
                      GROUP BY eid
                   ) cnts)
);





UPDATE rental
SET end_date = start_date + INTERVAL '14 days'
WHERE end_date < start_date + INTERVAL '14 days';





UPDATE cashier
SET shift = 'Extended'
WHERE eid IN (
  SELECT p.eid
  FROM payment p
  WHERE p.pdate >= DATE '2025-01-01'
    AND p.pdate < DATE '2025-02-01'
  GROUP BY p.eid
  HAVING SUM(p.amount) > 5000
);
