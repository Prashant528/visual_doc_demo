# VisDoc

VisDoc is a tool to convert the onboarding documentation of OSS projects (contributing guides) to task trees.

This repository contains the backend of the VisDoc framework. To get the code for the frontend, please refer to this [repository](https://github.com/Prashant528/visdoc_framework).

## Running VisDoc backend:

This project was written using Python 3.9.6. Create a virtual environment inside the root folder:
```bash
python3 -m venv visdoc_env
source visdoc_env/bin/activate
```

VisDoc uses OpenAI APIs to make API calls. Set your OpenAI API key as a environment variable:
```bash
export OPENAI_API_KEY='YOUR_KEY'
```
Or if you want to permanently add the key to environment variables, modify your ./zshrc or ./bashrc files and add the key.

Use pip to install the requirements.

```bash
pip install -r requirements.txt
```

Finally, to run the Flask Server:
```bash
python3 app.py
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
