# 🚀 Python CI/CD Pipeline with GitLab Runner  
Welcome to my CI/CD project! This repository demonstrates how to set up and run a fully automated CI/CD pipeline for a Python application using **GitLab CI/CD**.  

## 🛠️ Technologies Used  
- **GitLab CI/CD**: Automating build, test, and deployment stages.  
- **GitLab Runner**: Agent for executing CI/CD pipeline jobs.  
- **Python**: Main application built with Flask.  
- **unittest**: Automated testing framework for Python.  
- **Virtual Environment (venv)**: Managing Python dependencies.  

## 📋 Project Workflow  
The pipeline consists of three main stages:  

1. **Build**  
   - Sets up a virtual environment (`venv`).  
   - Installs all required dependencies from `requirements.txt`.  

2. **Test**  
   - Executes automated tests using `unittest` to ensure the application works as expected.  

3. **Deploy**  
   - Runs the Python application if all previous stages succeed.  

## 🔧 Configuration  
### .gitlab-ci.yml  
The CI/CD pipeline configuration is defined in `.gitlab-ci.yml`:  
```yaml
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - python -m venv venv
    - source venv/bin/activate
    - pip install -r requirements.txt
  artifacts:
    paths:
      - venv/

test:
  stage: test
  script:
    - source venv/bin/activate
    - python -m unittest discover

deploy:
  stage: deploy
  script:
    - echo "Deploying the application..."
    - source venv/bin/activate
    - python app.py
```
Python Requirements
Add your dependencies to requirements.txt. Example:
```txt
flask
requests
```
Application Code
An example of a simple Flask app (app.py):
```py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, CI/CD!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```
Test Cases
Basic unit test for the application (test_app.py):
```py
import unittest
from app import app

class TestApp(unittest.TestCase):
    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Hello, CI/CD!")

if __name__ == '__main__':
    unittest.main()
```
💡 Features
Fully automated pipeline with three stages (build, test, deploy).
Ensures all dependencies are managed and installed via venv.
Simplifies deployment by automating all stages of application delivery.

📂 Folder Structure
```plaintext
project/
│
├── .gitlab-ci.yml         # CI/CD pipeline configuration  
├── app.py                 # Python Flask application  
├── requirements.txt       # Python dependencies  
├── test_app.py            # Unit tests for the application  
└── README.md              # Project documentation
```
🤔 How to Use
Clone this repository:
```bash
git clone https://github.com/your-username/ci-cd-python.git
cd ci-cd-python
```
- Push the repository to your GitLab instance.
- Configure a GitLab Runner for your project.
- Observe the automated pipeline in GitLab CI/CD dashboard.
## 🎯 Goals and Challenges
- Goal: Automate and streamline the build, test, and deployment process.
- Challenge: Debugging environment issues and ensuring compatibility with CI/CD Runner.
## 🌟 Inspiration
"Like Edison who tried 100 ways before succeeding, each challenge in this project taught me something new and brought me closer to success."

## 📈 Contributing
Contributions are welcome! If you have any suggestions or improvements, feel free to open a pull request.

## 📄 License
This project is licensed under the MIT License.
