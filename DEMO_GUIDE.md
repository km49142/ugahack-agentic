# Demo Guide: Running the AI Bot locally

This guide explains how to use the built-in demo site to test the AI Application Bot safely.

## Step 1: Start the Demo Site

In a separate terminal, run the Flask application:

```bash
pip install flask
python demo_app.py
```

The demo site will be available at `http://localhost:5000`.

## Step 2: Configure Your Profile

Make sure you have a profile set up. If not, run:

```bash
python setup_profile.py
```

## Step 3: Run the Bot

Open a new terminal and run the application script:

```bash
python apply.py
```

### When prompted:
1.  **URL**: Enter `http://localhost:5000/apply` (or `/signup` to test account creation).
2.  **AI Agent**: Say **yes** to use the local AI agent (TensorFlow).
3.  **Submit**: Say **no** for preview mode, or **yes** to see the success page!

## What to Look For

1.  **Standard Filling**: The bot should instantly fill Name, Email, University, etc.
2.  **AI Answering**: The bot will encounter questions like *"Why are you passionate about building agentic AI tools?"*. Since these aren't in your profile, the **TensorFlow Agent** will analyze your profile and generate a custom response.
3.  **Screenshots**: Check `data/screenshots/` to see the results.

---
*Happy Hacking at UgaHacks!*
