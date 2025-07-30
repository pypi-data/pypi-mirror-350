# Python RestPkiCore Lib Auto Generation
This is a comprehensive tutorial to assist new developers when generating the lib again. This lib is generated with the help of [OpenAPI's Python Generator](https://openapi-generator.tech/docs/generators/python).

## Project Structure
As seen in the first command line in `cmd.ps1`, the output folder for all generated files is the `dist` folder. Therefore, all files in this folder will be automatically overwritten during generation. So it is important to have **static proprietary modules**. Static proprietary modules are modules which are not in the library generation but are necessary for it to work completely, such as the `RestPkiClient` class inside `restpki_ng_client.py`.

After generation, the project structure is as follows:
```
└── 📁restpkicore-python
    └── 00.pdf
    └── cmd.ps1
    └── openapitools.json
    └── python-openapi-config.json
    └── README.md
    └── restpki_ng_client.py
    └── 📁test
        └── ...
        └── __init__.py
    └── 📁dist
        └── 📁.github
            └── 📁workflows
                └── python.yml
        └── 📁.openapi-generator
            └── FILES
            └── VERSION
        └── 📁docs
            └── ...*.md
        └── 📁restpki_ng_python_client
            └── 📁api
                └── ...*.py
                └── __init__.py
            └── 📁models
                └── ...*.py
                └── __init__.py
            └── api_client.py
            └── api_response.py
            └── configuration.py
            └── exceptions.py
            └── py.typed
            └── rest.py
            └── restpki_ng_client.py
            └── __init__.py
        └── 📁test
            └── ...*.py
            └── __init__.py
        └── setup.cfg
        └── setup.py
        └── test-requirements.txt
        └── tox.ini
        └── git_push.sh
        └── pyproject.toml
        └── README.md
        └── requirements.txt
        └── .openapi-generator-ignore
        └── .travis.yml    
        └── .gitignore
        └── .gitlab-ci.yml
```

### Local files
Local files are outside the dist folder, some of them are:
* `00.pdf`: Sample PDF to perform _ad-hoc_ signatures
* `cmd.ps1`: PowerShell script to run the `cmd.ps1`, which is the file which contains automated steps such as:
1. Generating the lib using OpenAPI CLI with the configurations defined `python-openapi-config.json` (you may define new configurations as you need them, **but be aware of the new effects it may cause in this generation**)
2. Copying static proprietary modules. You are also free to add new files and copy them into the restpki_ng_python_client new steps to the `cmd.ps1` script whenever necessary. Just remember to document all new files and define their use in the project.
* `restpki_ng_client.py`: This is an example of static proprietary module file. This class contains a facade class which directly calls the APIs in the `dist/api` folder and gives them a more user-friendly name.

### Generated folder (`dist`)
The `dist` folder contains the generated files and the static proprietary modules from `cmd.ps1`. It is recommended to only add necessary files for the library and its functions. The `dist` folder contains
* An API folder, which is comprised of all endpoints as individual modules.
* Models folder, which contains all models generated from the specification.
* `gitlab-ci.yml`: Gitlab's CI file to test in different versions of Python.


## Steps 
### Generating and testing the library
1. Run `cmd.ps1`
2. Test your application, for that we have a copy of the `test` folder outside of the `dist` folder which must overwrite the `dist/test` folder with populated tests. The tests are also kept outside the dist folder so they are not overwritten during the generation process. 
* Copy and overwrite the `test` folder into `dist/test`.
* Test all modules using `pytest`, you also may test one at a time by running `pytest [filename.py]`
3. Run `python setup.py install` in the `dist` folder. This will generate a local library in your python modules as if it is already installed on your machine. However, you still need to publish it 

### Publishing

TODO

### Adding new files to the project
Adding new files is not a complex task, but it requires attention from the devs as not to break previous functionalities, so **it is vital to test them before publishing**. For this project, only integration tests were made available with only a test case for each endpoint. The tests do not cover
* Unit tests;
* Value range;
* Required values (those are inferred from the Swagger specification);

 In case you need to test a new functionality, add a new test case in the class and run it again. In case of a breaking change (i.e. a change which needs to be applied to previous test cases for them to work again), you might want to refactor previous tests and others affected from this change. Once you get them all working again, release a new version  
