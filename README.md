# FaceIN
FaceIN is a user management application that allows users to add, delete, and view user profiles, each associated with a captured image. The application is built using Python and leverages several libraries, including OpenCV for image capture, MySQL for database management, and CustomTkinter for a modern graphical user interface.

Key Features:

User Management:

Add User: Users can be added to the database by entering their name. The application captures an image using the device's camera and stores it alongside the user's name in a MySQL database.
Delete User: Users can be removed from the database. The application deletes the user's associated image file from the filesystem and removes their entry from the database.
View Users: Users can view a list of all registered users in the database, providing a quick overview of the current user base.
Image Capture:

The application utilizes OpenCV to access the camera and capture images. This feature is essential for associating a visual representation with each user profile.
Database Configuration:

Users can configure the database connection settings (host, user, password, and database name) through a dedicated configuration window. The application tests the connection to ensure that the settings are correct.
User Interface:

The application features a modern and user-friendly interface built with CustomTkinter, which allows for a dark mode and customizable color themes. The main window includes a canvas that displays a logo or image, enhancing the visual appeal of the application.
Error Handling:

The application includes error handling for database connections and image capture, providing informative messages to the user in case of issues.
Use Cases:
Facial Recognition Systems: FaceIN can be integrated into systems that require user identification through facial recognition.
Access Control: The application can be used in environments where access control is necessary, allowing only registered users to gain entry based on their facial data.
User Registration Systems: FaceIN can serve as a registration system for events, organizations, or applications that require user identification.
Conclusion:
FaceIN is a versatile application that combines image processing and database management to facilitate user management through facial recognition. Its modern interface and robust features make it suitable for various applications in security, access control, and user registration.
