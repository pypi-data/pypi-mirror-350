import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='smart_Ai_agent',
    version='0.2',
    author='Super',
    description='A lightweight Python library for generating random User-Agent headers for anonymity and testing.',
    long_description=long_description,
    long_description_content_type="text/markdown", 
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)


# import setuptools

# setuptools.setup(
#     name='smart_Ai_agent',
#     version='0.2',
#     author='Super',
    
#     description='A lightweight Python library for generating random  User-Agent headers for anonymity and testing.',
#     long_description=open("README.md", encoding="utf-8").read(),  
#     packages=setuptools.find_packages(),
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "Operating System :: OS Independent",
#         "License :: OSI Approved :: MIT License",
#     ],
# )

########## pypi-AgEIcHlwaS5vcmcCJDBlN2E4YTMwLTI3NDEtNGFkNy1iYmFjLTY2ZTdlN2IwYzJhOQACKlszLCJiN2M1ZGFhYy03MDU3LTRiMjMtOTc0NC1kNDA3YTEwYmZlMjYiXQAABiDXm0oTcVysFyFz_-Fpa9vT9swpw-FTj9q8ThpRQ0cvhg
# pypi-AgEIcHlwaS5vcmcCJGZiYWEyNzM1LTlmMDQtNGIzNi1hMDQ4LTAwNWY4NDVjMTlhMgACKlszLCJiN2M1ZGFhYy03MDU3LTRiMjMtOTc0NC1kNDA3YTEwYmZlMjYiXQAABiA9swSOGkITdre4kzyMGts6ZDFif1-Pdv74HvnlDj7l7Q

# [pypi]
#   username = __token__
#   password = pypi-AgEIcHlwaS5vcmcCJDBlN2E4YTMwLTI3NDEtNGFkNy1iYmFjLTY2ZTdlN2IwYzJhOQACKlszLCJiN2M1ZGFhYy03MDU3LTRiMjMtOTc0NC1kNDA3YTEwYmZlMjYiXQAABiDXm0oTcVysFyFz_-Fpa9vT9swpw-FTj9q8ThpRQ0cvhg
# twine upload --repository-url https://upload.pypi.org/legacy/ dist/* -u __token__ -p 