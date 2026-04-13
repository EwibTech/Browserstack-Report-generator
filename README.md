# BrowserStack Test Report Generator

A modern web application for generating comprehensive test reports from BrowserStack Test Management API with visual analytics and email capabilities.

## Features

- 🔐 Secure credential input for BrowserStack authentication
- 🔍 Flexible test run filtering
- 📊 Interactive visualizations (Pie charts and Bar charts)
- 📈 Detailed analytics and statistics
- 🎯 Advanced filtering options for reports
- 📥 CSV report download
- 📧 Email report functionality
- 🎨 Modern, responsive UI built with React and TailwindCSS

## Tech Stack

### Backend
- **Flask** - Python web framework
- **Pandas** - Data manipulation and CSV generation
- **Requests** - HTTP library for BrowserStack API calls
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **React** - UI framework
- **TailwindCSS** - Styling
- **Recharts** - Data visualization
- **Axios** - HTTP client
- **Lucide React** - Icons

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask server:
```bash
python app.py
```

The backend will start on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will start on `http://localhost:3000`

## Usage

1. **Enter Credentials**: 
   - Input your BrowserStack username and access key
   - Optionally add a test run name filter to narrow down results

2. **Generate Report**:
   - Click "Generate Report" to fetch data from BrowserStack
   - The app will retrieve all matching test runs across all projects

3. **View Analytics**:
   - See overall statistics in summary cards
   - View pie chart for test status distribution
   - Analyze bar chart for test results by run
   - Browse detailed table with all test run information

4. **Filter Results**:
   - Use filters to narrow down by project, active state, or run state
   - Filters update the visualizations and table in real-time

5. **Download Report**:
   - Click "Download CSV" to export the filtered data

6. **Email Report**:
   - Click "Email Report"
   - Enter recipient email address
   - Click "Send Email" to deliver the report

## Email Configuration

To enable email functionality, you need to configure SMTP settings. You can do this by:

1. Setting environment variables:
```bash
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USERNAME=your-email@gmail.com
export SMTP_PASSWORD=your-app-password
```

2. Or modify the `send_email` function in `backend/app.py` to use your SMTP configuration.

**Note**: For Gmail, you'll need to use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

## API Endpoints

### POST `/api/generate-report`
Generate a test report from BrowserStack.

**Request Body**:
```json
{
  "username": "your-username",
  "accessKey": "your-access-key",
  "testRunFilter": "optional-filter"
}
```

### POST `/api/download-report`
Download report as CSV.

**Request Body**:
```json
{
  "reportData": [...]
}
```

### POST `/api/send-email`
Send report via email.

**Request Body**:
```json
{
  "email": "recipient@example.com",
  "reportData": [...],
  "smtpConfig": {}
}
```

### GET `/api/health`
Health check endpoint.

## Project Structure

```
BStack UI/
├── backend/
│   ├── app.py              # Flask application
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   └── ui/         # Reusable UI components
│   │   ├── App.jsx         # Main application component
│   │   ├── index.js        # React entry point
│   │   └── index.css       # Global styles
│   ├── package.json
│   ├── tailwind.config.js
│   └── postcss.config.js
├── browserstack_report.py  # Original CLI script
└── README.md
```

## Security Notes

- Never commit credentials to version control
- Use environment variables for sensitive data
- The access key input field uses password type for security
- Consider implementing proper authentication for production use

## Future Enhancements

- User authentication and session management
- Saved filter presets
- Scheduled report generation
- More chart types and visualizations
- Export to PDF
- Historical trend analysis
- Dark mode support

## License

MIT

## Support

For issues or questions, please contact your system administrator or create an issue in the project repository.
