from pypdf import PdfReader #python reader import
import re
from datetime import datetime

class Resume:
    def __init__(self, name, email, phone, skills, experience):
        self.name = name
        self.email = email
        self.phone = phone
        self.skills = skills
        self.experience = experience

    def display(self):
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Phone: {self.phone}")
        print(f"Skills: {', '.join(self.skills)}")
        print(f"Experience: {self.experience} years")

class JobDescription:
    def __init__(self, title, required_skills, min_experience):
        self.title = title
        self.required_skills = required_skills
        self.min_experience = min_experience

    def display(self):
        print(f"Job Title: {self.title}")
        print(f"Required Skills: {', '.join(self.required_skills)}")
        print(f"Minimum Experience: {self.min_experience} years")

# Now I need to find a way to scan resumes and filter out desired information








def extract__text(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# Resume Parser
def parse_resume(text):
    # Function should read the resume taken as argument "text" and extract the desired information
    # return None for information not found
    name = None
    email = None
    skills = []
    experience = 0

    if not text:
        return name, email, skills, experience
    

    text = text.strip()
    if not text:
        return name, email, skills, experience

    # Normalize whitespace and split into lines
    text = re.sub(r"\r\n|\r", "\n", text)
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # Extract email
    email_match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text)
    if email_match:
        email = email_match.group(0)

    # Extract name from first non-email, non-phone line
    for line in lines[:5]:
        if email and email in line:
            continue
        if re.search(r"\d", line):
            continue
        if re.search(r"\b(email|phone|mobile|linkedin|github)\b", line, re.IGNORECASE):
            continue
        if len(line.split()) <= 6 and re.match(r"^[A-Za-z .,'-]+$", line):
            name = line
            break

    # Skills dictionary
    known_skills = [
        "Python",
        "Java",
        "SQL",
        "Git",
        "AWS",
        "Docker",
        "Kubernetes",
        "JavaScript",
        "React",
        "C++",
        "C",
        "HTML",
        "CSS",
        "Pandas",
        "NumPy",
        "Spark",
        "PySpark",
        "Linux",
        "TensorFlow",
        "PyTorch",
        "Flask",
        "Django",
        "Node.js",
        "TypeScript",
        "REST",
        "GraphQL",
        "Excel",
        "Power BI",
        "Tableau",
        "Jenkins",
        "CI/CD",
        "Terraform",
        "Ansible",
    ]

    lower_text = text.lower()
    for skill in known_skills:
        if skill.lower() in lower_text and skill not in skills:
            skills.append(skill)

    # Experience extraction patterns
    month_map = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12
    }

    pattern = (
        r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})"
        r"\s*[-–]\s*"
        r"(Present|January|February|March|April|May|June|July|August|September|October|November|December)"
        r"(?:\s+(\d{4}))?"
    )

    total_months = 0
    now = datetime.now()

    for match in re.finditer(pattern, text, re.IGNORECASE):
        start_month_name = match.group(1)
        start_year = int(match.group(2))
        end_month_name = match.group(3)
        end_year = match.group(4)

        start_month = month_map.get(start_month_name.capitalize(), 1)
        if end_month_name.lower() == "present":
            end_year = now.year
            end_month = now.month
        else:
            end_month = month_map.get(end_month_name.capitalize(), 12)
            end_year = int(end_year) if end_year else now.year

        months = (end_year - start_year) * 12 + (end_month - start_month) + 1
        if months > 0:
            total_months += months

    if total_months > 0:
        experience = round(total_months / 12, 1)
    else:
        experience_patterns = [
            r"(\d+)\+?\s+years?\s+of\s+experience",
            r"(\d+)\+?\s+years?\s+experience",
            r"(\d+)\+?\s+years?\b",
            r"(\d+)\s+yrs?\b",
        ]
        for pattern in experience_patterns:
            match = re.search(pattern, lower_text)
            if match:
                try:
                    experience = int(match.group(1))
                    break
                except ValueError:
                    continue
    #         except ValueError:
    #             continue

    return name, email, skills, experience


# Job Description Parsing
# 
# Retrieve Job Description


def parse_job_description(text):
    # Skills your ATS knows about (Baseline)
    # I definitely want to expand this list in the future
    known_skills = [
        "Python",
        "Java",
        "SQL",
        "Git",
        "AWS",
        "Docker",
        "Kubernetes",
        "JavaScript",
        "React",
        "C++",
        "C#",
        "HTML",
        "CSS",
        "Pandas",
        "NumPy",
        "Spark",
        "PySpark",
        "Linux"
    ]

    required_skills = []

    for skill in known_skills:
        if skill.lower() in text.lower():
            required_skills.append(skill)

    # Find years of experience
    match = re.search(r"(\d+)\+?\s+years?", text, re.IGNORECASE)

    if match:
        min_experience = int(match.group(1))
    else:
        min_experience = 0

    return required_skills, min_experience

    # # Consider this later
    # # First non-empty line becomes the title
    # lines = [line.strip() for line in text.split("\n") if line.strip()]

    # title = lines[0] if lines else "Unknown"

    # return JobDescription(title, required_skills, min_experience)



def resume_scoring(resume, job_description):
    # resume should be an instance of the Resume class
    # Likewise with job descriptions
    # Still need to parse job description (job_skills) and such

    for skill in resume.skills:
        if skill in job_description.job_skills:
            skill_score += 1

    skill_score = skill_score/len(job_description.job_skills) * 100

    # Years of experience
    # Doesn't Check for edge cases or bad scneario (Job_experience required is less than 0)
    if resume.experience >= job_description.job_experience:
        exp_score = 100

    elif (resume.experience > job_description.job_experience - 3) and (resume.experience < job_description.job_experience - 1):
        exp_score = 50

    else:
        exp_score = 0


    # Overall Score will be the average of all subcategory scores (Currently only 2 categories)
    Ovr_score = (skill_score + exp_score)/2
    return("Experience Score: %d\n Skill Score: %d\n", exp_score, skill_score)


