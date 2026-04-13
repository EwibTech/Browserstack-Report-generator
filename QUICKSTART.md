# Quick Start Guide

## 🚀 Fast Setup (Recommended)

### Option 1: Using the Start Script

```bash
./start.sh
```

This will automatically:
- Set up Python virtual environment
- Install backend dependencies
- Install frontend dependencies
- Start both servers

### Option 2: Manual Setup

#### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

#### Frontend Setup (in a new terminal)
```bash
cd frontend
npm install
npm start
```

## 📧 Email Configuration (Optional)

To enable email functionality:

1. Copy the example environment file:
```bash
cd backend
cp .env.example .env
```

2. Edit `.env` and add your SMTP credentials:
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

**For Gmail users:**
- Enable 2-factor authentication
- Generate an App Password at: https://myaccount.google.com/apppasswords
- Use the App Password (not your regular password)

## 🎯 Usage

1. Open your browser to `http://localhost:3000`
2. Enter your BrowserStack credentials:
   - Username
   - Access Key
3. (Optional) Add a test run filter
4. Click "Generate Report"
5. View analytics, filter results, download CSV, or email the report

## 🔑 Getting BrowserStack Credentials

1. Log in to BrowserStack
2. Go to Account Settings
3. Find your username and access key under "Access Key" section

## 📊 Features

- **Input Form**: Secure credential entry with optional filtering
- **Visual Analytics**: Pie charts and bar charts for test distribution
- **Filtering**: Filter by project, active state, or run state
- **Download**: Export filtered data as CSV
- **Email**: Send reports directly via email
- **Responsive**: Works on desktop and mobile devices

## 🛠️ Troubleshooting

### Backend won't start
- Ensure Python 3.8+ is installed
- Check if port 5000 is available
- Verify all dependencies are installed

### Frontend won't start
- Ensure Node.js 16+ is installed
- Check if port 3000 is available
- Try deleting `node_modules` and running `npm install` again

### Email not working
- Verify SMTP credentials in `.env` file
- For Gmail, ensure you're using an App Password
- Check firewall settings

### CSS warnings in IDE
The `@tailwind` and `@apply` warnings are expected - TailwindCSS processes these directives during build time. They won't affect functionality.

## 📝 Notes

- The app runs on localhost by default
- Backend: `http://localhost:5000`
- Frontend: `http://localhost:3000`
- For production deployment, see README.md

## 🆘 Support

For detailed documentation, see [README.md](README.md)
