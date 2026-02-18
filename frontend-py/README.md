# RVCE OMR Grading System - Python Frontend

A 1:1 Python Flask port of the Next.js TypeScript frontend for the RVCE OMR Grading System.

## Overview

This is a complete rewrite of the frontend using Python Flask with Jinja2 templates, replicating all functionality from the original Next.js application.

## Features

- **Dashboard**: View statistics, recent batches, and system metrics
- **Upload Center**: Upload OMR sheets and Excel answer keys
- **Processing Page**: Real-time batch processing status with polling
- **Results Page**: View and download batch results as CSV
- **Responsive Design**: Mobile-friendly interface
- **Dark Mode Support**: Automatic dark mode based on system preference

## Project Structure

```
frontend-py/
├── app.py                    # Flask application with routes
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── static/
│   ├── css/
│   │   └── styles.css       # Converted from Tailwind CSS
│   ├── js/
│   │   └── app.js           # Main JavaScript utilities
│   └── images/              # Static assets (logos, favicon)
└── templates/
    ├── base.html            # Base layout template
    ├── index.html           # Dashboard page
    ├── upload.html          # Upload center page
    ├── processing.html      # Batch processing status page
    ├── results.html         # Results view page
    └── error.html           # Error page
```

## Installation

1. Create a virtual environment:
```bash
cd frontend-py
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Set environment variables:

```bash
# API URL (default: http://localhost:8000/api)
export API_URL=http://localhost:8000/api

# Flask secret key (change in production)
export SECRET_KEY=your-secret-key-here

# Flask environment
export FLASK_ENV=development
export FLASK_APP=app.py
```

## Running the Application

### Development Mode

```bash
python app.py
```

The application will be available at `http://localhost:3000`

### Production Mode

```bash
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:3000 app:app
```

## API Endpoints

The frontend proxies all API calls to the backend:

- `GET /api/stats/dashboard` - Dashboard statistics
- `POST /api/omr/upload` - Upload OMR batch
- `POST /api/answers/upload` - Upload Excel answer key
- `GET /api/omr/status/<batch_id>` - Get batch status
- `GET /api/omr/results/<batch_id>` - Get batch results
- `GET /api/omr/results/<batch_id>/download` - Download CSV

## Pages

### Dashboard (`/`)
- Statistics cards (Total Batches, Total Scanned, Success Rate, Average Score)
- Recent batches list with status
- Tabs for OMR Upload and Excel Answers

### Upload Center (`/upload`)
- Drag-and-drop file upload for OMR images
- Excel file upload for answer keys
- Batch name input
- File validation

### Processing (`/processing/<batch_id>`)
- Real-time progress tracking
- Individual file status
- Auto-redirect to results when complete
- Polling every 2 seconds

### Results (`/results/<batch_id>`)
- Summary statistics
- Detailed results table
- CSV download functionality

## Technology Stack

- **Backend**: Flask (Python)
- **Templates**: Jinja2
- **Styling**: Vanilla CSS (converted from Tailwind)
- **JavaScript**: Vanilla JS (no frameworks)
- **API**: RESTful HTTP requests

## Differences from Original Next.js Version

1. **No Server-Side Rendering**: Uses client-side JavaScript for dynamic content
2. **No React Components**: Pure HTML templates with vanilla JS
3. **Simpler Build Process**: No build step required
4. **Python Ecosystem**: Uses Flask instead of Next.js

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Development

To add new features or modify existing ones:

1. **Templates**: Edit files in `templates/` directory
2. **Styles**: Modify `static/css/styles.css`
3. **JavaScript**: Add to `static/js/app.js` or inline in templates
4. **Routes**: Add new routes in `app.py`

## License

Same as the original project.

## Support

For issues or questions, refer to the main project documentation.
