from pypdf import PdfReader #python reader import
import re

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


