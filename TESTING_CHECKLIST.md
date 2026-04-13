# Testing Checklist

Use this checklist to verify all features are working correctly.

## 🚀 Initial Setup

- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Backend server starts without errors (port 5000)
- [ ] Frontend server starts without errors (port 3000)
- [ ] Browser opens to `http://localhost:3000`

## 📝 Input Screen Tests

### Form Validation
- [ ] Empty username shows error when clicking "Generate Report"
- [ ] Empty access key shows error when clicking "Generate Report"
- [ ] Filter field is optional (works with empty value)
- [ ] Password field masks access key characters

### UI Elements
- [ ] Filter tooltip displays helpful information
- [ ] "Generate Report" button is clickable
- [ ] Loading spinner appears when generating report
- [ ] Button is disabled during loading

### Error Handling
- [ ] Invalid credentials show error message
- [ ] Network errors display appropriate message
- [ ] Error message is dismissible/clearable

## 📊 Report Screen Tests

### Data Display
- [ ] Summary cards show correct totals
- [ ] Pie chart renders with correct data
- [ ] Bar chart renders with correct data
- [ ] Data table displays all test runs
- [ ] Table shows all columns correctly

### Visualizations
- [ ] Pie chart shows percentages
- [ ] Pie chart has legend
- [ ] Pie chart tooltips work on hover
- [ ] Bar chart has labeled axes
- [ ] Bar chart tooltips work on hover
- [ ] Charts use correct colors (green for passed, red for failed)

### Filtering
- [ ] Project filter works (case-insensitive)
- [ ] Active State filter works
- [ ] Run State filter works
- [ ] Multiple filters work together
- [ ] Filters update summary cards
- [ ] Filters update pie chart
- [ ] Filters update bar chart
- [ ] Filters update table rows
- [ ] Clearing filters restores all data

### Table Features
- [ ] All columns display correctly
- [ ] Status badges show correct colors
- [ ] Pass percentage shows correct color coding:
  - [ ] Green for ≥80%
  - [ ] Yellow for 50-79%
  - [ ] Red for <50%
- [ ] Table is scrollable horizontally on small screens
- [ ] Rows highlight on hover

## 💾 Download Tests

- [ ] "Download CSV" button is clickable
- [ ] CSV file downloads successfully
- [ ] CSV filename includes timestamp
- [ ] CSV contains correct headers
- [ ] CSV contains filtered data (not all data if filters applied)
- [ ] CSV opens correctly in Excel/Google Sheets
- [ ] All columns are properly formatted

## 📧 Email Tests

### Modal Functionality
- [ ] "Email Report" button opens modal
- [ ] Modal displays correctly
- [ ] Email input field is present
- [ ] "Send Email" button is present
- [ ] "Cancel" button is present
- [ ] Cancel button closes modal
- [ ] Modal shows report summary

### Email Sending (requires SMTP setup)
- [ ] Empty email shows error
- [ ] Invalid email format shows error
- [ ] Valid email triggers send process
- [ ] Loading spinner shows during send
- [ ] Success message appears after send
- [ ] Modal closes after successful send
- [ ] Email is received with attachment
- [ ] Email contains summary in body
- [ ] Attachment is valid CSV file

### Without SMTP Setup
- [ ] Appropriate error message shown
- [ ] Instructions for SMTP setup provided

## 🔄 Navigation Tests

- [ ] "New Report" button returns to input screen
- [ ] Form is cleared when returning to input
- [ ] Previous report data is cleared
- [ ] Can generate multiple reports in sequence

## 📱 Responsive Design Tests

### Desktop (>1024px)
- [ ] Full layout displays correctly
- [ ] Charts are side-by-side
- [ ] Summary cards in 4-column grid
- [ ] Table is fully visible

### Tablet (768px - 1024px)
- [ ] Layout adjusts appropriately
- [ ] Charts stack if needed
- [ ] Summary cards in 2-column grid
- [ ] Table scrolls horizontally

### Mobile (<768px)
- [ ] Single column layout
- [ ] Charts stack vertically
- [ ] Summary cards stack vertically
- [ ] Table scrolls horizontally
- [ ] Buttons are full-width
- [ ] Text is readable

## 🎨 Visual Tests

### Colors
- [ ] Primary blue color for buttons
- [ ] Green for passed tests
- [ ] Red for failed tests
- [ ] Orange for blocked tests
- [ ] Gray for untested tests
- [ ] Purple for skipped tests

### Typography
- [ ] Headers are clear and readable
- [ ] Body text is appropriate size
- [ ] Table text is legible
- [ ] No text overflow issues

### Spacing
- [ ] Consistent padding in cards
- [ ] Appropriate margins between sections
- [ ] No overlapping elements
- [ ] Clean, organized layout

## ⚡ Performance Tests

- [ ] Report generates in reasonable time (<30s for normal datasets)
- [ ] Filtering is responsive (no lag)
- [ ] Charts render smoothly
- [ ] Table scrolling is smooth
- [ ] No console errors in browser
- [ ] No memory leaks (check browser dev tools)

## 🔐 Security Tests

- [ ] Access key is masked in input field
- [ ] Credentials are not visible in network tab
- [ ] No credentials stored in localStorage
- [ ] HTTPS used for BrowserStack API calls

## 🐛 Edge Cases

### Data Edge Cases
- [ ] Empty results (no test runs found)
- [ ] Single test run
- [ ] Very large dataset (100+ test runs)
- [ ] Test run with 0 tests
- [ ] All tests passed (100%)
- [ ] All tests failed (0%)

### Filter Edge Cases
- [ ] Filter with no matches
- [ ] Filter with special characters
- [ ] Very long filter text
- [ ] Filter with numbers only

### UI Edge Cases
- [ ] Very long project names
- [ ] Very long test run names
- [ ] Many test runs (table pagination)
- [ ] Rapid filter changes
- [ ] Multiple rapid clicks on buttons

## 🌐 Browser Compatibility

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

## 📋 API Tests

### Backend Endpoints
- [ ] `GET /api/health` returns 200
- [ ] `POST /api/generate-report` with valid credentials returns data
- [ ] `POST /api/generate-report` with invalid credentials returns error
- [ ] `POST /api/download-report` returns CSV file
- [ ] `POST /api/send-email` with SMTP config sends email
- [ ] CORS headers are present

## 🔧 Configuration Tests

### Environment Variables
- [ ] Backend reads .env file
- [ ] SMTP settings from .env work
- [ ] Missing .env file doesn't crash app
- [ ] Default values are used when env vars missing

## 📝 Documentation Tests

- [ ] README.md is complete and accurate
- [ ] QUICKSTART.md instructions work
- [ ] Code comments are helpful
- [ ] API endpoints are documented
- [ ] Setup instructions are clear

## ✅ Final Checks

- [ ] No console errors in browser
- [ ] No Python errors in backend terminal
- [ ] All features work as expected
- [ ] UI is polished and professional
- [ ] Performance is acceptable
- [ ] Ready for demo/presentation

## 🎯 Test Scenarios

### Scenario 1: First Time User
1. User opens app
2. Sees clear instructions
3. Enters credentials
4. Generates report successfully
5. Understands the data
6. Downloads report

### Scenario 2: Power User
1. User enters credentials with filter
2. Generates filtered report
3. Applies additional filters
4. Analyzes specific data
5. Downloads CSV
6. Emails to team
7. Generates new report with different filter

### Scenario 3: Mobile User
1. Opens app on mobile device
2. All elements are accessible
3. Can input credentials
4. Can view report
5. Can download CSV
6. Can navigate easily

## 📊 Success Criteria

- [ ] All critical features work (generate, display, download)
- [ ] No blocking bugs
- [ ] UI is responsive and attractive
- [ ] Performance is acceptable
- [ ] Documentation is complete
- [ ] Ready for production use

---

## 🐛 Bug Reporting Template

If you find issues, document them as:

**Bug Title**: [Brief description]

**Steps to Reproduce**:
1. 
2. 
3. 

**Expected Result**: 

**Actual Result**: 

**Browser/Environment**: 

**Screenshots**: [If applicable]

**Console Errors**: [If any]

---

## ✨ Enhancement Ideas

After testing, note any improvements:

- [ ] Feature idea 1
- [ ] Feature idea 2
- [ ] UI improvement 1
- [ ] Performance optimization 1
