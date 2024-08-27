# Checkout System Asset Tracker

This application helps you manage and track shared inventory items like laptops, textbooks, video games, or any other valuable assets. The system allows users to check out and check in items, making it easy to monitor who has what and when. The app is designed to eventually send notifications to IT or administrators when items are requested, although email functionality is not yet fully implemented.

## Project History

This project started as a practical way for me to learn how to code. Back in 2015, I teamed up with an old friend, and we spent a lot of time digging up code snippets online while writing plenty of our own. We wanted to replace the old, handwritten loaner device tracking system at a company I used to work for. But, I left the company before we could finish it and the project ended up sitting on the back burner for over eight years.

Recently, I decided it was time to dust it off and give it another shot. I’m hoping to start building some practical Flask apps for my current company to help manage backend tasks and API calls, so I figured this would be a good way to refresh my memory. Plus, I’m also testing the limits of OpenAI and ChatGPT’s coding capabilities. While you only get out what you put in, it’s been really good practice for me to piece chunks of code together one function at a time. The best part is, I don’t have to troubleshoot as much as before, and I almost never run into syntax typos, so it’s saving me a ton of time overall. What started as a simple way to learn has turned into a chance to revisit an old project, tidy it up, and see how far I’ve come.

## Features

- User login with role-based permissions (in progress)
- Inventory management: Add, update, and remove devices
- Check-out and check-in scheduling
- Admin panel for managing users and devices

## Setup Instructions

To get started with the Checkout System Asset Tracker, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jessemcbrower/checkout_system.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd checkout_system
   ```
3. **Set up a virtual environment:**
   ```bash
   python3 -m venv flask
   ```
4. **Activate the virtual environment:**
   ```bash
   source flask/bin/activate
   ```
5. **Upgrade `pip` and install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
6. **Run the application:**
   ```bash
   ./run.py
   ```
7. **Access the app in your browser:**
   Open [http://localhost:5000](http://localhost:5000)

## Login Information

**Default Admin Account:**

- **Username:** `admin`
- **Password:** `admin`

**Alternative Admin Account:**

- **Username/Email:** `mcbrower.checkoutsystem@gmail.com`
- **Password:** `Checkmate`

**Note:** The email account above was originally set up for notifications but may no longer be functional. Email functionality will be revisited in future updates.

## To-Do List

1. Implement user role permissions
2. Create an admin template for managing user accounts

## Future Goals

1. **Enable device checkouts by username:** Allow users to check out devices and associate them with their account.
2. **Send notifications to IT or administrators when devices are requested:** Automate notifications for better inventory tracking.
3. **Improve inventory management:** Enhance features for adding, updating, and removing devices from the system.
4. **Complete user login with permissions:** Finalize role-based access control for users.
5. **Implement check-out/check-in scheduling:** Allow users to schedule when they will check out and return items.

## Contribution

Feel free to fork this repository, make feature requests, or submit pull requests. Any contributions to improve the system are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
