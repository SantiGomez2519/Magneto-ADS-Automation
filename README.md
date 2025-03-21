# Magneto-ADS-Automation

## 🚀 Running Instructions

Follow these steps to set up and run the project locally.

**1. Clone the repository**

```
git clone https://github.com/SantiGomez2519/Magneto-ADS-Automation.git
cd Magneto-ADS-Automation
```

**2. Set up a virtual environment**

Create and activate a virtual environment

- **Windows:**

```
python -m venv env
env\Scripts\activate
```

- **Mac/Linux:**

```
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```
pip install -r requirements.txt
cd theme/static_src/
npm install
cd ../../
```

**4. Run the development server (in different terminals)**

```
python manage.py tailwind start
```

**Open a new terminal**
```
# Activate the virtual environment as explained above
python manage.py runserver
``` 

The app will be available at http://127.0.0.1:8000/.
