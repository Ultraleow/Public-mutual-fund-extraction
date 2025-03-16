Here's the entire document in a ready-to-use `README.md` format:

```markdown
# Public Mutual Fund Extraction

Public Mutual Fund Extraction is a Python-based automation tool designed for efficient extraction and management of mutual fund data. The application automates date selection on websites using Selenium, processes extracted data using Pandas, and sends results via email as Excel files.

## 📌 Features

- **Automated Date Selection:** Leverages Selenium to interact with web interfaces automatically.
- **Data Processing:** Utilizes Pandas for seamless data manipulation.
- **Automatic Email Delivery:** Sends extracted data as Excel files through Gmail SMTP.
- **Docker Deployment:** Easy deployment support using Docker and Gunicorn for Google Cloud Functions (GCP).

## ⚙️ Technologies Used

- Python 3.8+
- Selenium
- Pandas
- Flask
- Docker
- Gunicorn

## ✅ Prerequisites

Make sure your environment meets the following requirements:

- Python 3.8 or higher
- Docker installed
- Google Cloud Platform CLI (`gcloud`)

---

## 🔧 Installation

Follow these steps to set up your local environment:

### 1\. Clone the Repository

```bash
git clone <your_repository_url>
cd public-mutual-fund-extraction
```

### 2\. Setup Virtual Environment

Create and activate a virtual environment:

- **Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

- **Linux/MacOS:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3\. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📝 Environment Configuration

Create a `.env` file in your project's root directory and configure the following variables:

```env
USERNAME=your_gmail_username
PASSWORD=your_gmail_app_password
FILE_NAME=E_SERIES
FUND_NUMBER=170,163,179,176,181,178,144,188
FUND_ARRANGEMENT=PeAITF,PeISMF,PePEF,PeIPE40F,PeAEVGF,PeEMAS,PeFAF,PeAGFF
```

**Variable Descriptions:**

| Variable         | Description                                  | Example                         |
|------------------|----------------------------------------------|---------------------------------|
| `USERNAME`       |                  |            |
| `PASSWORD`       |  |                |
| `FILE_NAME`      | Name prefix for the generated Excel file     | E_SERIES                        |
| `FUND_NUMBER`    | Comma-separated list of fund IDs             | 170,163,179,176,181,178,144,188 |
| `FUND_ARRANGEMENT`| Corresponding fund arrangement names        | PeAITF,PeISMF,...               |

> **Important:**  
> Remember to configure the receiver email address directly in your Python script (`selenium_click_date.py`).

---

## 🚀 Running the Application

Execute the main extraction script using:

```bash
python selenium_click_date.py
```

This will automatically select the date, process data, and email an Excel report.

---

## 🐳 Docker Deployment to Google Cloud Functions (GCP)

Follow these steps to containerize and deploy your application:

### 1\. Build Docker Image

```bash
docker build -t public-mutual-fund-extraction .
```

### 2\. Tag and Push to GCP Container Registry (GCR)

Replace `<your-gcp-project-id>` with your GCP Project ID:

```bash
docker tag public-mutual-fund-extraction gcr.io/<your-gcp-project-id>/public-mutual-fund-extraction
docker push gcr.io/<your-gcp-project-id>/public-mutual-fund-extraction
```

### 3\. Deploy to GCP Cloud Functions

Deploy with the following command (replace placeholders):

```bash
gcloud functions deploy public-mutual-fund-extraction \
  --region=<region> \
  --runtime=python39 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point=<your-entry-function> \
  --source=. \
  --env-vars-file=.env
```

**Placeholders:**  
- `<region>`: GCP deployment region (e.g., `us-central1`)  
- `<your-entry-function>`: Your main Python function entry point (e.g., `main`)

---

## 📂 Project Structure

Your project directory should look like this:

```bash
public-mutual-fund-extraction/
├── Dockerfile
├── requirements.txt
├── selenium_click_date.py
├── .env
└── README.md
```

---

## 🤝 Contributing

Contributions are warmly welcome. Feel free to submit pull requests or report issues to enhance this project.

---

## 📄 License

This project is open-source. See [LICENSE](LICENSE) for full details.

```
