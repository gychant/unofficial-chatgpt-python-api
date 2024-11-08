# Unofficial ChatGPT Python API using Selenium

## Features

- Bypass Cloudflare's anti-bot protection for the ChatGPT portal using `undetected_chromedriver`
- Support users' own OpenAI accounts for login

## Getting Started

### Installation

```bash
git clone https://github.com/gychant/unofficial-chatgpt-python-api.git
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

### Usage

#### Use OpenAI account for login

* Create a file storing the credentials as shown in "./openai_auth_file_example" using the following format:
  ```
  username=user@example.com
  password=password
  ```
  You can use any name for it and choose the location that you like. You will use its path later.

* Or, pass the credentials as arguments through the constructor, see the code example below.

#### Import as a module

```python
from pychatgpt import ChatGPT

# Create a ChatGPT instance by specifying the credential file path
chat = ChatGPT(auth_file_path="./openai_auth_file")

# Or, Create a ChatGPT instance by specifying username and password in the arguments
chat = ChatGPT(username="user@example.com", password="password")

# Send a prompt to ChatGPT
chat.predict("Show me a step-by-step code example to build a beautiful web app in React.")
```
The response of ChatGPT is converted into a structured JSON object which contains the prompt and response. Specifically, the response is stored as a ordered list of text and code snippets. Sample output of the above prompt:
```
{
  'prompt': 'Show me a step-by-step code example to build a beautiful web app in React.',
  'response': [
    {
      'type': 'text',
      'content': "Certainly! Here's a step-by-step code example to build a beautiful web app using React:"
    },
    {
      'type': 'text',
      'content': 'Step 1: Set Up the Project\nCreate a new directory for your project and navigate into it. Then, initialize a new React project using create-react-app.'
    },
    {
      'type': 'code',
      'lang': 'bash',
      'content': 'npx create-react-app my-web-app\ncd my-web-app'
    },
    {
      'type': 'text',
      'content': 'Step 2: Remove Default Files\nRemove unnecessary files and folders generated by create-react-app.'
    },
    {
      'type': 'code',
      'lang': 'bash',
      'content': 'cd src\nrm -f logo.svg App.test.js setupTests.js reportWebVitals.js'
    },
    {
      'type': 'text',
      'content': "Step 3: Install Additional Dependencies\nInstall additional dependencies for styling the web app. In this example, we'll use Material-UI."
    },
    {
      'type': 'code',
      'lang': 'bash',
      'content': 'npm install @mui/material @emotion/react @emotion/styled'
    },
    {
      'type': 'text',
      'content': 'Step 4: Create a Basic Layout\nReplace the contents of src/App.js with the following code to create a basic layout for your web app.'
    },
    {
      'type': 'code',
      'lang': 'jsx',
      'content': 'import React from \'react\';\nimport { Container, Typography } from \'@mui/material\';\n\nfunction App() {\n  return (\n    <Container maxWidth="md" sx={{ paddingTop: \'2rem\' }}>\n      <Typography variant="h4" component="h1" align="center" gutterBottom>\n        Welcome to My Web App\n      </Typography>\n      <Typography variant="body1" component="p" align="center">\n        Start building your beautiful web app here!\n      </Typography>\n    </Container>\n  );\n}\n\nexport default App;'
    },
    {
      'type': 'text',
      'content': 'Step 5: Style the App\nCreate a new file src/App.css and add the following styles to customize the appearance of your web app.'
    },
    {
      'type': 'code',
      'lang': 'css',
      'content': '.App {\n  text-align: center;\n}\n\n.App-logo {\n  height: 40vmin;\n  pointer-events: none;\n}\n\n.App-header {\n  background-color: #282c34;\n  padding: 20px;\n  color: white;\n}\n\n.App-link {\n  color: #61dafb;\n}'
    },
    {
      'type': 'text',
      'content': 'Step 6: Update the App Component\nUpdate src/App.js to import the App.css file and apply the styles to the appropriate components.'
    },
    {
      'type': 'code',
      'lang': 'jsx',
      'content': 'import React from \'react\';\nimport { Container, Typography } from \'@mui/material\';\nimport \'./App.css\';\n\nfunction App() {\n  return (\n    <Container maxWidth="md" sx={{ paddingTop: \'2rem\' }}>\n      <Typography variant="h4" component="h1" align="center" gutterBottom>\n        Welcome to My Web App\n      </Typography>\n      <Typography variant="body1" component="p" align="center">\n        Start building your beautiful web app here!\n      </Typography>\n    </Container>\n  );\n}\n\nexport default App;'
    },
    {
      'type': 'text',
      'content': 'Step 7: Run the Web App\nFinally, start the development server and open the web app in your browser.'
    },
    {
      'type': 'code',
      'lang': 'bash',
      'content': 'npm start'
    },
    {
      'type': 'text',
      'content': 'Now, you can visit http://localhost:3000 in your browser to see your beautiful web app in action!'
    },
    {
      'type': 'text',
      'content': 'You can continue adding more components, styles, and functionality to your web app as per your requirements.'
    }
  ]
}
```
Other supported methods:
```
# Delete the current activate chat session
chat.delete_current_chat()

# Create a new chat session
chat.new_chat()
```

# Run as Docker container
```
docker compose down && docker compose -f docker-compose.yml up -d --build
```

## Disclaimer

This project is not affiliated with OpenAI in any way. Use the code at your own risk. The author is not responsible for any misuse or damage. Please read the [OpenAI Terms of Service](https://beta.openai.com/terms) before using this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE).