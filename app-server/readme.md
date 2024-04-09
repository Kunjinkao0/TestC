Using `virtualenv` is a common practice in Python development to create isolated environments for projects. This helps in managing dependencies and ensuring that different projects can have different dependency versions without conflicts. Here's a basic guide on how to use `virtualenv`:

1. **Install `virtualenv`**: If you haven't installed `virtualenv` yet, you can do so via pip:

```bash
pip install virtualenv
```

2. **Create a Virtual Environment**: Navigate to the directory where you want to create your virtual environment and run:

```bash
virtualenv venv
```

Replace `venv` with whatever name you want to give your virtual environment.

3. **Activate the Virtual Environment**: Depending on your operating system, the activation command differs:

   - **On Windows**:
     ```bash
     venv\Scripts\activate
     ```

   - **On Unix or MacOS**:
     ```bash
     source venv/bin/activate
     ```

4. **Deactivate the Virtual Environment**: To exit the virtual environment, simply type:

```bash
deactivate
```

5. **Install Dependencies**: While the virtual environment is activated, you can install packages using `pip`, and they will be isolated to that environment:

```bash
pip install -r requirements.txt
```

6. **Start app**:

```bash
python main.py
```



pip freeze > requirements.txt