# 🚀 Project Name

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo Drive Link](https://drive.google.com/file/d/1v4ZgW-nrvoXPgG_tMOPmLcJBRQKe7RxR/view?usp=sharing)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
Modern software development teams face challenges in maintaining code quality, ensuring test coverage, and accelerating code review processes. Manual testing and review cycles are time-consuming and prone to human errors, especially in banking applications where regulatory compliance is critical.

This project aims to solve this problem by building a GenAI-backed PR analysis and test generation system that:

- Automates PR code review by analyzing changes and identifying their impact.

- Generates context-aware BDD test cases using a RAG-enhanced architecture that integrates JIRA story details with code analysis.

- Improves efficiency and accuracy in testing by leveraging fine-tuned Mistral models for banking-specific insights.

## 🎥 Demo
📹 [Video Demo](https://drive.google.com/file/d/1v4ZgW-nrvoXPgG_tMOPmLcJBRQKe7RxR/view?usp=sharing) (Added drive link but available in the artifacts/demo folder as well)  
🖼️ Screenshots:

![Screenshot 1](https://github.com/ewfx/catfe-one-hit-wonder/blob/main/artifacts/demo/Screenshot%20(47).png)
![Screenshot 2](https://github.com/ewfx/catfe-one-hit-wonder/blob/main/artifacts/demo/Screenshot%20(48).png)
![Screenshot 3](https://github.com/ewfx/catfe-one-hit-wonder/blob/main/artifacts/demo/Screenshot%20(49).png)
![Screenshot 4](https://github.com/ewfx/catfe-one-hit-wonder/blob/main/artifacts/demo/Screenshot%20(50).png)
![Screenshot 5](https://github.com/ewfx/catfe-one-hit-wonder/blob/main/artifacts/demo/Screenshot%20(51).png)

## 💡 Inspiration
The project was inspired by the need to streamline code review and testing processes in banking applications, where ensuring regulatory compliance and maintaining code quality is critical. By automating PR analysis and test generation, it reduces manual effort and enhances accuracy.

## ⚙️ What It Does
The GenAI-Powered PR Analysis and Test Generation System automates code review and test creation by extracting PR details, analyzing JIRA stories with a fine-tuned Mistral model, and generating context-aware BDD test cases. It uses a RAG-enhanced architecture to include story context during code and test analysis, ensuring accuracy and compliance in banking applications.

## 🛠️ How We Built It
The project uses Flask for the backend and web UI, with SQLite for storing analysis results. It integrates with the GitHub API for fetching PR details and code changes, and uses Mistral AI APIs for story analysis, code review, and test generation. The frontend is styled with HTML, CSS, and JavaScript for a clean and intuitive user experience.

## 🚧 Challenges We Faced
One major challenge was maintaining context consistency during code analysis and test generation. To overcome this, we implemented a RAG-enhanced architecture, storing story analysis results in SQLite and feeding them back into the Mistral model for contextual accuracy.

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/ewfx/catfe-one-hit-wonder.git
   ```
2. Install dependencies  
   ```sh
   pip install -r requirements.txt
   ```
3. Run the project  
   ```sh
   python app.py
   ```

## 🏗️ Tech Stack
- 🔹 Web APP: Flask
- 🔹 Database: SQLite
- 🔹 Other: Mistral AI

## 👥 Team
- **Hariom Vyas** - [GitHub](https://github.com/hariom0159) | [LinkedIn](linkedin.com/in/hariom1509/)