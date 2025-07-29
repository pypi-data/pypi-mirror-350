import logging

from scripts.project_example_1.usecases.my_first_use_case import sumar_use_case

logging.basicConfig(level=logging.DEBUG)

res = sumar_use_case(5, 7, 456)

print(res)

