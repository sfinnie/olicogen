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
    doc = template.render()
    intermediate_dir = os.path.join(os.path.abspath('.'), "..", "intermediate")
    output_dir = os.path.join(os.path.abspath('.'), "..", "output")
    texfile = os.path.join(intermediate_dir, f"example-{value}.tex")

    with open(texfile, "w") as fh:
        fh.write(doc)
        print(f"wrote `{texfile}")

    res = os.system(f"pdflatex -quiet -aux-directory={intermediate_dir} -output-directory={output_dir} {texfile} ")

# def generate_diagram(value):
#     """ generates a number line showing `value` 100ths coloured in
#         Uses the LaTeX Tikz package
#     """
#     geometry_options = {"tmargin": "1cm", "lmargin": "10cm"}
#     doc = Document(geometry_options=geometry_options)
#
#     with doc.create(Section('The simple stuff')):
#         doc.append('Some regular text and some')
#         doc.append(italic('italic text. '))
#         doc.append('\nAlso some crazy characters: $&#{}')
#         with doc.create(Subsection('Math that is incorrect')):
#             doc.append(Math(data=['2*3', '=', 9]))
#
#         with doc.create(Subsection('Beautiful graphs')):
#             with doc.create(TikZ()):
#                 plot_options = 'height=4cm, width=6cm, grid=major'
#                 with doc.create(Axis(options=plot_options)) as plot:
#                     plot.append(Plot(name='model', func='-x^5 - 242'))
#
#                     coordinates = [
#                         (-4.77778, 2027.60977),
#                         (-3.55556, 347.84069),
#                         (-2.33333, 22.58953),
#                         (-1.11111, -493.50066),
#                         (0.11111, 46.66082),
#                         (1.33333, -205.56286),
#                         (2.55556, -341.40638),
#                         (3.77778, -1169.24780),
#                         (5.00000, -3269.56775),
#                     ]
#
#                     plot.append(Plot(name='estimate', coordinates=coordinates))
#     doc.generate_pdf(f"question-{value}.pdf")
#     return doc


if __name__ == "__main__":
    generate_questions(10, 1, 100)
