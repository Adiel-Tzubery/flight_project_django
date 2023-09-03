# Flight Project

# admin user: username - adiel password - admin1234

#  לכל אורך הפרויקט השתדלתי לאזן בין דרישות הפרויקט לבין חלוקת קוד נכונה. אם יש איזה קונפליקט בין השניים אני אציין אותו במפורש פה בקובץ, ובנוסף מה עשיתי בפועל.



נקודות כלליות:
* למידע כללי על המערכת + כללים כללים להתנהלות בהת יש להיכנס ל- About ATravel שנמצא בנבבר.
 * אין הפרדה בין יצירת יוזר, ליצירת משתמש מבחינת הלקוח קצה.
 * כשעושים רג'יסטר רגיל זה אוטומטית יוצר לקוח.
* רק לאדמין יש אפשרות ליצור משתמש אדמין אחר או חברת תעופה.
* לאדמין יש גם האפשרות ליצור משתמש לקוח רגיל.

models:

* even though you have told us that the model can be treated as part of the DAL layer, i treated the model's functions
as the model's and not as the DAL's, and in the DAL i just reference to theme. (even though it may seem as redundant code, i felt the need to write my code to answer the instructions as much as i can)

* iT didn't happened a lot, but when i needed, i added functions to the models. 

~~~~~~~~~~~~~~
DAL:

* all through the project i was careful to structure my code into separate files if needed.
in the DAL specifically, there was a request to write it all in one class for the whole models, so the
file turned out to be very long.
therefore, i arranged it in such a way so it will be easy to understand the section you are in.
i divided it to three parts.  

the parts:
1. CRUD - in this part there are the CRUD functions, and they are build as generic methods.
* because in the User model i used the BaseUserManager, and there are different methods creating
    user/superuser, i had to add a condition to the CREATE method in the DAL. so it damaged the generic propose of the crude but i didn't see any way out of this situation so it's the only exception.

2. in this part there are the references to the models methods that i mentioned before.

3. in this part i included some method that i needed in addition, for specific reasons.

~~~~~~~~~~~~~~
facads:

* the facade are separated into different files for each facade and i added facade validator file.

* in the facades there is all the logics and data manipulations.

* the only place that have communication with the DAL layer.

* most of the backend data validations are in facads_validator, here and there you'll see validations in the functions itself.

* i'm using simplejwt so there is no login method in the anonymous facade, the connection to the simplejwt view is in the urls.py

* in the anonymous facade i added the create customer due the fact that you cannot register if you are already logged in (in exception of admin that can register all accounts only when logged in).

~~~~~~~~~~~~~~
views:

* the views are separated into different file for each role + base view.

* outside the anonymous_view all the views have several layer of authentications
1. check if the request came from user that is logged in.
2. rest_framework authentication that check the API request to be in the allow list (GET, POST, DELETE, htc...)
3. the third layer checks if the request came from user with the correct permission according it's group (costume decoration, stored in auth.auth).

* i designed the view in steps:
1. get the request.
2. pass the data to the relevant facade method and store the response in variable.
3. serialize the variable content
4. send the serialized data to the frontend.

* somewhere along the way i wondered if doing the serialization in the facades is making more sense then to do it in the views
that supposed only to act as data pipe. but i was so deep in the proses that i decide not to, even though it's make more sense(just wanted you to know).

~~~~~~~~~~~~~~
tests and loggs:

* I have some test but i didn't managed to cover it all 

* same with the logging, but here i just having the setup and some loggs in DAL methods. 


