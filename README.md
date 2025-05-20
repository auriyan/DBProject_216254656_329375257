
DBProject_216254656_329375257
#Best_ReadMe_Ever

נחשון רייניץ 329375257
אוריאן גייסמן 216254656


מטרת המערכת היא ניהול השכרת ציוד סקי וחיבור בין לקוחות ומדריכים לצורכי שיעורים פרטיים
לצורך כך הגענו למסקנה שחשוב שניצור יישות עובד וממנה נורשות יישות מדריך וקופאי. בנוסף יצרנו יישות לקוח ודרכם יצרנו השכרה שיעור וכל מה שצריך לצורכי המערכת. נציין שנצרכנו ליצור טבלה lesson-participants על מנת לחבר בין השיעורים למשתתפים בקשר M:M וטבלת rental-equipments על מנת לקשר בין ציוד שנלקח בכל השכרה גם כן בM:M
דיאגרמת הERD:
![WhatsApp Image 2025-04-22 at 16 18 41_297d3c85](https://github.com/user-attachments/assets/eb9b0778-634e-4b16-8de0-cc7a92095693)
תרשים הDSD:
![WhatsApp Image 2025-04-22 at 16 18 58_d64a42d8](https://github.com/user-attachments/assets/36d5ed3c-d691-453c-a1a8-31ed15cf05ea)
יצירת הנתונים נעשתה בעזרת שלוש שיטות:
ייבוא נתונים מקבצים:

![WhatsApp Image 2025-04-22 at 18 08 50_64122377](https://github.com/user-attachments/assets/c5ae087f-a344-4b62-bf6e-e1b345e12cfd)

שימוש באתר mocaroo:

![WhatsApp Image 2025-04-27 at 19 17 56_d953d15a](https://github.com/user-attachments/assets/c9617974-a0ae-40d1-b32e-8bf618e837ac)

![WhatsApp Image 2025-04-22 at 18 36 40_0571d6b0](https://github.com/user-attachments/assets/5a821ebd-fdad-4df2-8da4-7106ee0acf06)

שימוש בסקריפט פייתון:

![image](https://github.com/user-attachments/assets/6a11614c-e384-4e92-a560-59e663ea94d0)
![image](https://github.com/user-attachments/assets/57f6506e-408d-4e71-be4f-364b4c7803d5)




לאחר מכן גיבינו את הנתונים בעצרת Docker עם pgadmin.
ראשית, יצרנו קובץ גיבוי:
![image](https://github.com/user-attachments/assets/f5b7caf6-2676-4486-88c4-410ead3c68c5)

לאחר מכן, כדי לבדוק שקובץ הגיבוי אכן עובד, מחקנו את הטבלאות אחת אחרי השניה:
![image](https://github.com/user-attachments/assets/7cd58849-5e83-4ed6-a520-6a213494af2d)

עד שכל הטבלאות לכאורה נעלמו
![image](https://github.com/user-attachments/assets/9c35bfdf-5b61-47b0-a9e0-66472d83c790)

לאחר שמחקנו את כל הטבלאות, גיבינו אותם בעזרת קובץ הגיבוי שיצרנו:
![image](https://github.com/user-attachments/assets/b8bdbf5b-53e0-4e70-a182-554ec3bef506)

ובאמת היווכחנו לגלות שאכן הקבצים שלנו חזרו במלואם!! (ברוך ה' פיווווו)
![image](https://github.com/user-attachments/assets/8736f643-a523-4c64-975a-b54921909698)

שלב ב



שאילתא מספר 1:

השאילתה עוברת על טבלת ההשכרות ומחזירה טבלה של כל הלקוחות ומספרי הטלפון שלהם יחד עם השנה והחודש של ההשכרה לפי הסדר של כמות ההשכרות בחודש נובמבר. שאילתה זו שימושית כאשר המנהל מנסה לראות מי הלקוח ששכר הכי הרבה ציוד בחודש נובמבר ומה המספר שלו.

![image](https://github.com/user-attachments/assets/ffcabce0-1099-4646-8aa6-e181ea4e38f5)

![image](https://github.com/user-attachments/assets/136006da-ffd7-4707-9eeb-5cfeffd52aa7)


שאילתא מספר 2:

השאילתה עוברת על הטבלה של השיעורים פרטיים ומחזירה את כל השיעורים שהתקיימו בחודש פברואר, עם המזהה שלהם ומספר המשתתפים בשיעור.


![image](https://github.com/user-attachments/assets/967ea4cf-b237-46ea-9bc7-643750cf1005)

![image](https://github.com/user-attachments/assets/3f76d369-56eb-4b52-87b7-aaf28b88646a)



שאילתה מספר 3:

השאילתה מחשבת את סך-הכל ההכנסות שהתבצעו על־ידי כל קופאי לפי חודש ושנה, ומציגה רק קופאים שעברו 1,000 יחידות מטבע (לטובת דוחות ניהול).

![image](https://github.com/user-attachments/assets/682d7fe1-b907-4665-b479-79af7565969f)

![image](https://github.com/user-attachments/assets/24db9e57-d9ce-4cad-8334-737bb6caa8d2)



שאילתה מספר 4:

השאילתה מחשבת את ממוצע משך ימי ההשכרה (הפרש תאריכים) לכל סוג ציוד וממיינת מהציוד הנחשק ביותר (המתהלך זמן רב ביותר). שימושי לבחינת פופולריות ומשך שימוש.


![image](https://github.com/user-attachments/assets/68ef761d-0db1-40cd-b6c8-8cb332e8fc57)

![image](https://github.com/user-attachments/assets/67fde359-1709-4157-8f86-057ead66fb3e)



שאילתה מספר 5:

בודק אילו פריטי ציוד טרם הושכרו אף פעם, וממיין לפי מחיר יומי כדי להבין אילו פריטים "תקועים במלאי".

![image](https://github.com/user-attachments/assets/1579bb2b-b536-43e3-8250-1a3f214ba36a)

![image](https://github.com/user-attachments/assets/d329a499-496b-45f5-8611-6a702cbe146d)




שאילתה מספר 6:

מוצא את 5 השיעורים עם ממוצע המשתתפים הגבוה ביותר (אחרי שאספנו מספר משתתפים לכל שיעור). מעולה לדירוג שיעורים פופולריים.


![image](https://github.com/user-attachments/assets/7f388f2d-56a1-4830-b602-c241fbc5147e)

![image](https://github.com/user-attachments/assets/1bae0238-643c-4409-b0ab-af9073855ec7)




שאילתה מספר 7:
שאילתה זו מחשבת, עבור כל סוג ציוד, את סך ימים שבהם הושכר הציוד במהלך שנת 2024 ואת סך ההכנסות (מחיר יומי × ימים), וממיינת מהציוד שהניב את ההכנסה הגבוהה ביותר


![image](https://github.com/user-attachments/assets/b4ddd214-db9e-4816-8a1c-11aded206333)

![image](https://github.com/user-attachments/assets/134209c2-4c94-4928-9817-9ccd56df4a08)



שאילתה מספר 8:
סיכום חודשי של מספר השכרות והכנסות מהשכרות במהלך 2024

![image](https://github.com/user-attachments/assets/200e7627-915d-4a87-87f9-966b2d6e4250)

![image](https://github.com/user-attachments/assets/13d1b175-fe35-48f7-a049-98fff7804c93)


לאחר ביצוע שמונת השאילתות, התנסנו בכתיבת שאילתות מסוג עדכון ומחיקה.

שאילתות מחיקה:

שאילתה מספר 1:

מחיקת שיעורים שהתבצעו בחודש מאי. שימושי עבור תיקון וניהול תקלות במערכת.

זה חלק מטבלת השיעורים לפני הרצת השאילתה:

![image](https://github.com/user-attachments/assets/c2438d1a-f452-488d-94bd-ff5b774e309c)

ניתן לראות שכל השיעורים נמצאים שם (400), ובשורה 207 יש שיעור שמתקיים בחודש מאי.
לאחר הרצת השאילתה:

![image](https://github.com/user-attachments/assets/c3620fa8-7048-4d63-9243-9f5ba3b3df4f)

לאחר הרצת השאילתה ניתן לראות כי מספר השיעורים ירד ל90.




שאילתה מספר 2:

מוחק מטבלת השיעורים את כל השיעורים שלא השתצו אליהם אף אחד.
זו טבלת השיעורים לפני הרצת השאילתה:

![image](https://github.com/user-attachments/assets/49d18b30-cd43-48fc-9cdd-095100e0e8ac)

נריץ את השאילתה:

![image](https://github.com/user-attachments/assets/660d2d74-1349-4cfa-a425-6df73f894c2f)

וקיבלנו את טבלת השיעורים המעודכנת:

![image](https://github.com/user-attachments/assets/63ee2df1-c154-4c51-b685-47c1196e49b7)





שאילתה מספר 3:

מוחק את כל הלקוחות שלא שכרו, שילמו, או השתתפו בשיעור. שימושי למקרה שהמערכת רוצה להיפטר מלקוחות ישנים שכבר לא מופיעים ברשימות האלה של המערכת.
זו טבלת הלקוחות לפני הרצת השאילתה: (400 לקוחות)

![image](https://github.com/user-attachments/assets/6a9ee121-9abf-47a5-a30a-dafcca197875)

נריץ את השאילתה ונקבל:

![image](https://github.com/user-attachments/assets/c03801ac-13e9-40b5-b963-e1e3cc6a5bae)


כפי שניתן לראות נשארו רק 385 לקוחות.




שאילתות עדכון:

שאילתה מספר 1:

מעלה את המחיר של מוצרים שהושכרו יותר פעמים מהממוצע ב10 אחוז. כך נוכל להרוויח יותר ממוצרים פופולרים יותר.
זו הטבלה לפני העדכון:

![image](https://github.com/user-attachments/assets/a65d79b8-ca04-4d34-8ce8-be382519dd87)

נריץ את השאילתה:

![image](https://github.com/user-attachments/assets/a2fbb64f-c467-4ad5-9e6f-99b348c3d44a)



כפי שניתן לראות, ישנם פריטים פופולרים שהמחיר שלהם עלה ב10 אחוז לדוגמא הקסדה בשורה מספר 1, ויש פריטים פחות פופולרים שמחירם לא השתנה, לדוגמה הסנואובורד בשורה מספר 3.




שאילתה מספר 2:

מעדכן בטבלת ההשכרות את הטבלה כך שכל השכרה שקצרה יותר משבועיים תהיה ארוכה משבועיים. לוודא שהשכרות מתבצעות ללא פחות משבועיים.
זוהי טבלת ההשכרות לפני ביצוע השאילתה:

![image](https://github.com/user-attachments/assets/6e682f9a-5dac-4fd9-bfc6-7318c8f64c06)

נשים לב לשורה מספר 5. ההשכרה כרגע עד ה27, כלומר 12 ימים. נריץ את השאילתה:

![image](https://github.com/user-attachments/assets/60f48fba-aed6-4180-b628-dd1a00bb2e07)


נראה כי שורה מספר 5 התעדכנה לתאריך ה29, שזה בדיוק שבועיים אחרי תחילת ההשכרה.






שאילתה מספר 3:

מעדכן את טבלת העובדים, עבור על עובד שהרוויח יותר מ500 שקל, השאילתה משנה את הshift שלו לextended. כלומר העובד הזה עבד יותר זמן.
זו הטבלה לפני הרצת השאילתה:

![image](https://github.com/user-attachments/assets/a7394aa1-6a89-4304-999b-b47baf6ea4c2)


כפי שניתן לראות בשורות 24-25, הshift הוא לא extended. נריץ את השאילתה:

![image](https://github.com/user-attachments/assets/2ddc97da-96e4-4960-86ae-38bcfed49a7d)


עכשיו נשים לב שהטבלה התעדכנה!

