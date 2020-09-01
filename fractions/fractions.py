# Fractions
#
# Code to generate example fraction questions that can be uploaded to the Olico website.
#
#
import random
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os


def generate_questions(num_questions=10, min=1, max=100):
    """ generate the specified number of questions, using min and max as the upper and lower bounds
        For example:

            generate_questions(10, 1, 100) will generate 10 questions where the answer is between 1 and 100.

            So we might get questions for: 9/100, 15/100, 21/100... 97/100

            Each question comprises:
            1. The question text
            2. A diagram showing the number line
            3. The correct answer
    """
    values=random.sample(range(min, max), num_questions)
    questions = []
    for v in values:
        q = generate_question(v)
        questions.append(q)
    return questions


def generate_question(value):
    """returns a question where the correct answer is `value`"""
    diagram = generate_diagram(value)
    return diagram


def generate_diagram(value):

    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(['xml'])
    )

    template = env.get_template("hundreds.tex")
    doc = template.render(value=21)
    intermediate_dir = os.path.join(os.path.abspath('.'), "..", "intermediate")
    output_dir = os.path.join(os.path.abspath('.'), "..", "output")
    texfile = os.path.join(intermediate_dir, f"example-{value}.tex")

    with open(texfile, "w") as fh:
        fh.write(doc)
        print(f"wrote `{texfile}")

    res = os.system(f"pdflatex -quiet -aux-directory={intermediate_dir} -output-directory={output_dir} {texfile} ")


if __name__ == "__main__":
    generate_questions(1, 1, 100)
