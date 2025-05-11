
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



