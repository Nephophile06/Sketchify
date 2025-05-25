The vision is to create a space that reduces clutter and brings visual comfort in browsing to creative minds. Moreover, there isn't any dedicated practical platform where we can get stationeries and art supplies at one place. The creators should have a place from where they can enhance their creativity. A person who can take notes beautifully, will also sketch nice. Sometimes, a person can be creative by getting a chance to use new things. So, for many reasons, I wanted to create this.

tech stack:
1. Frontend: Html, CSS, Bootstrap, JavaScript (alert message for deleting something)
2. Backend: Python, Flask
3. Database: MongoDB
4. Payment: Stripe, SSLCommerz
5. Email Sending: Flask-Mail (Backup code + invoice)
6. Flash Message: Flask - Flash
7. Authentication: Bcrypt (password Hashing), 8-digit backup code generate
8. Deployment: Render Cloud Application

website summary:
(two different interactions) USER + ADMIN 

User interaction:
1. Users can browse the whole website and show the  products + can be added to the cart
2. User Register -> email will be sent with 8-digit backup code + form validation like (password length, existing email check) + password hashing 
3. Login with password or, 8-digit backup code (if password is forgotten)
4. checkout -> Payment method -> stripe and SSLCommerz
5. User dashboard -> My orders -> showing orders with details (with list) -> invoice print (a4) + can be sent into their email 
6. Users can delete, update (email + password)

Admin interaction:
1. Username + password for login
2. Admin dashboard -> total user, total product, total order
3. Products -> read, add, update, delete
4. Orders -> every detail of each order… list can be exported as CSV file + can update the delivery status
5. Logout

Looking forward to adding more features like mobile app integration, customized theme, rider assign and many more.
