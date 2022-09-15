#! /usr/bin/env python3
import sdg


def test():
    with open("tmps.html", "r") as f:
        content = f.read()
    content, matches = sdg.pdf_classification.sanitize(content)
    sentences = sdg.pdf_classification.split_sentences(content)
    output_html = sdg.pdf_classification.build_preview_html(sentences)
    plain_sentences = sdg.pdf_classification.get_plain_sentences(sentences)
    # for s, plain in zip(sentences, plain_sentences):
    #     print("-" * 50)
    #     print(s)
    #     print("-" * 10)
    #     print(plain)
    with open("output_restored.html", "w") as output:
        output.write(output_html)


if __name__ == "__main__":
    sdg.server.run()
    exit()
    html, sentences = sdg.pdf_classification.get_html("tmp/1663160412.5077848-mouse.pdf")
    with open("output_html.html", "w") as f:
        f.write(html)
    #print(sdg.pdf_classification.get_html("data/mouse.pdf"))
    