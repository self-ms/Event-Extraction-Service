import sys

from allennlp.commands import main

model = "ace05-event.tar.gz"
input = "news_handler/docs.jsonl"
output = "output/dygi.jsonl "

# Assemble the command into sys.argv
sys.argv = [
    "allennlp",  # command name, not used by main
    "predict",
    model,
    input,
    "--predictor", "dygie",
    "--include-package", "dygie",
    "--use-dataset-reader",
    "--output-file", output,
    "--cuda-device", "-1",
    "--silent"
]

main()
