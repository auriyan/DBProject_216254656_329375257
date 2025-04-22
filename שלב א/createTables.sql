-- לקוח
CREATE TABLE customer (
  cid          INT            PRIMARY KEY,
  full_name    VARCHAR2(100)  NOT NULL,
  phone        VARCHAR2(20)
);

-- עובד
CREATE TABLE employee (
  eid          INT            PRIMARY KEY,
  fname        VARCHAR2(50)   NOT NULL,
  lname        VARCHAR2(50)   NOT NULL,
  start_date   DATE           NOT NULL
);

-- מדריך (יורש employee)
CREATE TABLE instructor (
  eid            INT            PRIMARY KEY,
  exp            INT,
  language       VARCHAR2(50),
  CONSTRAINT fk_inst_emp
    FOREIGN KEY (eid) REFERENCES employee(eid)
);

-- קופאי (יורש employee)
CREATE TABLE cashier (
  eid            INT            PRIMARY KEY,
  shift          VARCHAR2(20),
  age            INT,
  CONSTRAINT fk_cash_emp
    FOREIGN KEY (eid) REFERENCES employee(eid)
);

-- ציוד
CREATE TABLE equipment (
  eid            INT            PRIMARY KEY,
  type           VARCHAR2(30),
  daily_price    NUMERIC(5,2)
);

-- השכרה
CREATE TABLE rental (
  rid            INT            PRIMARY KEY,
  cid            INT,
  eid            INT,            -- קופאי
  start_date     DATE,
  end_date       DATE,
  CONSTRAINT fk_rent_cust
    FOREIGN KEY (cid) REFERENCES customer(cid),
  CONSTRAINT fk_rent_cash
    FOREIGN KEY (eid) REFERENCES cashier(eid)
);

-- שיעור
CREATE TABLE lesson (
  lid             INT            PRIMARY KEY,
  ldate           DATE,
  duration_min    INT
);

-- משתתפי שיעור (N:M לקוחות–שיעור)
CREATE TABLE lesson_participants (
  lid             INT,
  cid             INT,
  PRIMARY KEY (lid, cid),
  CONSTRAINT fk_lp_lesson
    FOREIGN KEY (lid) REFERENCES lesson(lid),
  CONSTRAINT fk_lp_customer
    FOREIGN KEY (cid) REFERENCES customer(cid)
);

-- תשלום
CREATE TABLE payment (
  pid          INT            PRIMARY KEY,
  amount       NUMERIC(6,2),
  pdate        DATE,
  lid          INT,            -- לשיעור
  cid          INT,            -- מי שילם
  eid          INT,            -- קופאי שטיפל
  CONSTRAINT fk_pay_lesson
    FOREIGN KEY (lid) REFERENCES lesson(lid),
  CONSTRAINT fk_pay_cust
    FOREIGN KEY (cid) REFERENCES customer(cid),
  CONSTRAINT fk_pay_cash
    FOREIGN KEY (eid) REFERENCES cashier(eid)
);

-- קשר השכרה–ציוד (N:M)
CREATE TABLE rental_equipment (
  rid          INT,
  eid          INT,
  PRIMARY KEY (rid, eid),
  CONSTRAINT fk_re_rental
    FOREIGN KEY (rid) REFERENCES rental(rid),
  CONSTRAINT fk_re_equipment
    FOREIGN KEY (eid) REFERENCES equipment(eid)
);
