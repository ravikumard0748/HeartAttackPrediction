# Heart Attack Risk Prediction System

A machine learning-powered web application that predicts heart attack risk based on medical parameters. Built with Flask and deployed on Netlify.

## Features

- **Risk Assessment**: Predicts heart attack risk percentage using machine learning
- **Interactive Dashboard**: View historical predictions and trends
- **SMS Alerts**: Automatic notifications for high-risk cases via Twilio
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Analysis**: Instant risk calculation with detailed recommendations

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **ML Model**: Scikit-learn (Logistic Regression)
- **Deployment**: Netlify (Serverless Functions)
- **Notifications**: Twilio SMS API
- **Data Storage**: JSON files

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js (for Netlify deployment)
- Twilio account (optional, for SMS alerts)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Heart_Attack_Risk_Prediction
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open http://localhost:5000 in your browser

## Netlify Deployment

### Method 1: Direct Deployment

1. **Fork this repository** to your GitHub account

2. **Connect to Netlify**
   - Go to [Netlify](https://netlify.com)
   - Click "New site from Git"
   - Connect your GitHub repository

3. **Configure build settings**
   - Build command: `npm run build`
   - Publish directory: `dist`

4. **Set environment variables** in Netlify dashboard:
   ```
   SECRET_KEY=your-production-secret-key
   TWILIO_SID=your-twilio-sid
   TWILIO_TOKEN=your-twilio-token
   TWILIO_FROM_NUMBER=+1234567890
   TWILIO_TO_NUMBER=+1234567890
   ```

5. **Deploy**
   - Click "Deploy site"
   - Your app will be available at `https://your-site-name.netlify.app`

### Method 2: Manual Deployment

1. **Build the project**
   ```bash
   npm run build
   ```

2. **Deploy to Netlify**
   ```bash
   # Install Netlify CLI
   npm install -g netlify-cli
   
   # Login to Netlify
   netlify login
   
   # Deploy
   netlify deploy --prod --dir=dist
   ```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Flask secret key for sessions | Yes |
| `TWILIO_SID` | Twilio Account SID | No |
| `TWILIO_TOKEN` | Twilio Auth Token | No |
| `TWILIO_FROM_NUMBER` | Twilio phone number | No |
| `TWILIO_TO_NUMBER` | Recipient phone number | No |
| `FLASK_ENV` | Environment (development/production) | No |
| `DEBUG` | Enable debug mode | No |
| `PORT` | Application port | No |

### Model Parameters

The ML model expects these input parameters:
- Age (years)
- Gender (Male/Female)
- Heart Rate (bpm)
- Systolic Blood Pressure (mmHg)
- Diastolic Blood Pressure (mmHg)
- Blood Sugar (mg/dL)
- CK-MB (ng/mL)
- Troponin (ng/mL)

## API Endpoints

### Serverless Functions (Netlify)

- `POST /.netlify/functions/predict` - Get heart attack risk prediction

### Flask Routes (Local/Traditional Hosting)

- `GET /` - Home page
- `GET /predict` - Prediction form
- `POST /sub` - Submit prediction
- `GET /dashboard` - View historical data
- `GET /health` - Health check endpoint

## Project Structure

```
Heart_Attack_Risk_Prediction/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── package.json          # Node.js dependencies
├── netlify.toml          # Netlify configuration
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── .env.example          # Environment variables template
├── finalfinalmodel.joblib # Trained ML model
├── netlify/
│   └── functions/
│       ├── predict.py    # Serverless prediction function
│       └── requirements.txt
├── templates/            # HTML templates
│   ├── index.html
│   ├── predict.html
│   ├── result.html
│   ├── dashboard.html
│   ├── faq.html
│   └── contact.html
├── static/              # CSS, JS, images
│   ├── style.css
│   ├── script.js
│   └── logo.jpg
└── instance/           # Data storage
    └── users.db
```

## Monitoring and Health Checks

- Health check endpoint: `/health`
- Returns JSON with application status
- Monitors model availability

## Security Features

- Environment-based configuration
- Input validation
- CORS protection
- Rate limiting (via Nginx)
- Secure headers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the [Issues](../../issues) page
2. Create a new issue with detailed description
3. Include error logs and environment details

## Acknowledgments

- Scikit-learn for machine learning capabilities
- Flask for web framework
- Netlify for serverless deployment
- Twilio for SMS notifications
