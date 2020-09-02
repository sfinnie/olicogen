# Fractions
#
# Code to generate example fraction questions that can be uploaded to the Olico website.
#
#
import random
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import shutil
from PIL import Image
import pdf2image



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
    doc = template.render(value=value)
    fname_root = f"example-{value}"
    texfile = os.path.join(intermediate_dir, f"{fname_root}.tex")

    with open(texfile, "w") as fh:
        fh.write(doc)
        print(f"wrote `{texfile}")
    res = os.system(f"pdflatex -quiet -aux-directory={intermediate_dir} -output-directory={intermediate_dir} {texfile} ")
    pdf = os.path.join(intermediate_dir, f"{fname_root}.pdf")

    white_bg_png = os.path.join(intermediate_dir, f"{fname_root}.png")
    pdf2png(pdf, white_bg_png)

    transparent_bg_png = os.path.join(output_dir, f"{fname_root}.png")
    remove_background(white_bg_png, transparent_bg_png)

def pdf2png(pdf, png):
    """converts the pdf file into a png"""
    pages = pdf2image.convert_from_path(pdf, 500)
    page = pages[0]
    page.save(png, 'PNG')

def remove_background(source_file, target_file):
    """remove the background colour, making it transparent.
       works by getting each pixel in the image in RGBA form, where
       RGB encodes the colour (red, green, blue) and A is transparency.
       Any pixels that match white (RGB=255, 255, 255) have transparency
       set to zero.  The rest are left untouched.  The image is then saved
       to the target file
    """

    img = Image.open(source_file)
    img = img.convert('RGBA')
    data = img.getdata()

    newData = []
    for item in data:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(target_file, "PNG")
    return


if __name__ == "__main__":
    intermediate_dir = os.path.join(os.path.abspath('.'), "..", "intermediate")
    output_dir = os.path.join(os.path.abspath('.'), "..", "output")

    if not os.path.exists(intermediate_dir):
        os.mkdir(intermediate_dir)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    generate_questions(num_questions=1, min=1, max=100)

    shutil.rmtree(intermediate_dir)
    os.mkdir(intermediate_dir)
